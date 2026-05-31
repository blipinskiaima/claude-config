---
name: pipeline-3-etapes
description: Architecture réelle du pipeline Feature (compute→model→eval CENTRALISÉ) + verdict refresh_cohort = portage du 01 R + scripts/ standardisés (01 compute, 02 train, 03 eval)
metadata: 
  node_type: memory
  type: project
  originSessionId: c2f7cad8-b1a9-4dd5-93ee-f14009c1102c
---

Le pipeline 3 étapes de Feature (compute→model→eval) est **CENTRALISÉ**, pas un compute par dossier (la `.claude/rules/07-feature-structure.md` est désynchronisée du réel : elle décrit encore `compute.py → matrix.parquet` par feature).

**Étape 1 — COMPUTE (centralisée, 2 scripts) :**
- `cohort/refresh_cohort.py` : lit trace-prod read_only → SQL extrait mvaf_v1/v2, score_cnv, ichor_tf, frag_mode1/2, 16 probs EPIC, 31 Loyfer, short_read (mvaf_v1_short_read, ichorcna_short_read), QC, clinique+truth ; parse virgule→point ; filtres techniques (liquid, prod OK, dorado v5%, mvaf_v1 not null, !_Alc_, !rebasecalled1) ; dedup `unique_id` prefer_trimmed via `QUALIFY ROW_NUMBER` → `cohort/snapshot_YYYY-MM-DD.parquet` (figé, gitignoré).
- `experiments/prepare_inputs.py` : charge snapshot, dérive `frag_diff=m1-m2`, `ichor_x100=ichor_tf*100`, `ichor_short_read_x100`, `loyfer_non_wbc=1-Σ(4 WBC)` ; teste redondance `mvaf_v12` (exclu si Pearson>0.99) → `experiments/input.tsv`.
- `experiments/pool.yaml` = catalogue 11 features candidates (mvaf obligatoire). Features lourdes DÉJÀ calculées en amont (raima/Bam2Beta) → étape 1 = extraction+dérivation, PAS calcul from scratch.

**Étapes 2+3 — MODEL+EVAL :**
- `experiments/grid_search.py` orchestre les combos (mvaf + 2..7 features), lance en parallèle `experiments/score_one_combo.R`.
- `score_one_combo.R` : lit input.tsv, **RECALCULE à la volée** indication/score/mvaf/vaf/ichorcna depuis colonnes brutes (name, mvaf_v1, vaf_gene1_pct, ichor_tf), appelle `features/_shared/build_combined_score_flex.R`, calcule KPI (AUC ALL/CGFL/HCL + Sens@95/90% × {all,low_vaf,high_vaf,active_nomut}) → JSON.
- `build_combined_score_flex.R` : XGBoost 5-fold stratifié OOF, hyperparams identiques au `09_*.R` Michael (binary:logistic, max_depth=3, lr=0.1, subsample=0.8, colsample_bytree=0.8, nrounds=100, seed=42). required cols : `unique_id, name, which, indication, depth, vaf, active_cancer, mvaf` + features. Label : healthy=0, (mutated OR active_no_mut)=1, reste NA. Filtres analytiques ICI (rep/moche/bis/ter/quater, TNE/Nuclear/Bladder_Blood, depth>=0.25, dedup).

**Verdict (28/05/2026) :** `cohort/refresh_cohort.py` EST le portage trace-prod fidèle du `01_prepare_datasets.R` d'exploratory (cf [[convergence-exploratory-analysis]]). Les "diffs" de forme (colonnes R standardisées, 5 variantes raw/v4.3/v5.0, split centre, .rds) sont **non pertinentes** car `score_one_combo.R` recalcule à la volée et filtre par `which`. SEULE vraie diff = pas de `fill downup` (propagation vaf/ichor/frag entre réplicats avant dedup) — **NON reproduit** (choix Boris : mélanger réplicats techniques discutable).

**Travail 28/05 :** créé `scripts/01_prepare_cohort.py` = copie fidèle de refresh_cohort.py (seul `COHORT_DIR` redirigé vers `cohort/` + docstring), untracked sur main, **pas commité**. RESTE (phase 2, non démarrée) : migrer prepare_inputs/grid_search/analyze/score_one_combo/_shared dans `scripts/`, corriger les chemins relatifs (les `compute.py` des livrables pointent vers `../../../cohort/...`), supprimer le doublon `cohort/refresh_cohort.py`.

**`scripts/02_train_combined.R` (28/05) :** script R autonome d'ENTRAÎNEMENT standardisé. `--features "mvaf_v1"` → baseline brut (court-circuit, pas d'XGBoost, = 02 exploratory) ; `--features "mvaf_v1,frag_mode2,ichor_x100,..."` → XGBoost 5-fold OOF (= 08/09). Reproduit le 09 strict : suspects (`imagerie suspecte`, 25 dans le snapshot) scorés par inférence (`model_inference`) + heatmaps 2D pseudo-log (si ≥2 features scalaires ; clés `SCALAR_LABELS` = noms de COLONNES TSV, pas noms logiques du pool). KPI (AUC ALL/CGFL/HCL + Sens@95/90 × 4 groupes) intégrés, calculés sur samples LABELLISÉS uniquement (suspects exclus des métriques sinon AUC faussée par NA). Non-régression vs `score_one_combo.R` PROUVÉE (KPI identiques sur même input.tsv). Consolide `build_combined_score_flex.R` + `score_one_combo.R` (doublon temporaire). `--features` = noms de colonnes TSV (mvaf_v1, pas mvaf). Untracked sur main, pas commité. Reste : `scripts/03` (éval détaillée) puis migration (bascule grid_search → scripts/02).

**`scripts/03_evaluate.R` (28/05) :** éval standardisée. Input = CSV du 02 (combined_score + mvaf + truth). Seuil `quantile(healthy, target_spec, type=1)` — aligné sur le 02, PAS `raima::evaluate_score` (couplé GSheet + type=6). Reproduit le protocole exploratory : tables `summary_cancer_detection` (seuil ALL→ALL/CGFL/HCL + seuils par centre) + `summary_stratified` + misclassified FN/FP (= 02_sensitivity), courbes sens/spé mVAF vs Combined 4 groupes (= 10, généralise le 07), dotplot par indication×centre (= 05), scatter combined_score vs VAF + R² (= 06). Non-régression PROUVÉE (Sens_Cancer_AI ALL = sens_95_all du 02 = 78.1% ; Sens_Active_NoMut = 61.3% = 02). **Découverte** : exploratory n'a PAS d'éval standardisée — 3 méthodes (raima::evaluate_score couplé GSheet/type=6 à éviter ; 02_sensitivity tables mVAF ; 10 courbes type=1, le plus proche/cohérent). Cohorte unique (pas la double-distinction bladder du 02_sensitivity) car le CSV du 02 est déjà filtré.

**Pipeline scripts/ COMPLET (28/05) :** `01_prepare_cohort.py` → `02_train_combined.R` → `03_evaluate.R` (compute→train→eval standardisé depuis trace-prod). Committé sur branche dédiée. RESTE : migration (basculer grid_search.py vers scripts/02 ; supprimer doublons cohort/refresh_cohort.py + score_one_combo.R + build_combined_score_flex.R ; corriger chemins compute.py des livrables).

Voir aussi [[cohort-filters-cascade]], [[trace-prod-schema]], [[livrables-actuels]].
