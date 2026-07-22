---
name: Todo optimisation Claude Code & projets
description: Liste des tâches en cours (par priorité) et historique des tâches complétées (par jour).
type: project
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
# Todo — Optimisation Claude Code & Projets

**Dernière mise à jour : 2026-04-15 (ajout tâches post-Batches A-F + planification HCL)**

---

# Partie 1 — À faire (par priorité)

## Pour demain (2026-04-16)

- [ ] **Nouveau client** — suivre la prise en charge (relance / réponse au premier mail).
- [ ] **Seqera AI** — finir la prise en main du CLI et de l'API.

## Haute priorité

- [ ] **Sécurité secrets — étape 1** : migrer `~/Pipeline/export/` vers des fichiers `.env` avec `chmod 600`. Documenter le pattern pour les autres projets (tokens Tower dans nextflow.config).

## Moyenne priorité

- [ ] **Terminer reclassification concurrents (22 articles restants)** — script `~/Pipeline/Aima-Survey/scripts/reclassify_competitors.py` killé après 75/97 articles (2026-04-22). Les 22 restants ont `sector IS NULL` → cron daily Aima-Survey (`classify_pending`) les picke automatiquement. Vérifier demain que l'onglet Concurrence de `/survey` affiche bien les articles IMBdx (+ autres co-signatures concurrent). Si besoin relance manuelle : `bash ~/Pipeline/Aima-Survey/run_veille.sh --no-fetch --no-score --report`.
- [ ] **Rotation secrets Aima-Tower compromis** — `.env` était tracked dans git jusqu'au 2026-04-21 (historique pushé sur `aima-dx/Aima-Tower`, repo privé). Révoquer `ANTHROPIC_API_KEY` (console.anthropic.com > API Keys) + `accessToken` Seqera (cloud.seqera.io > Tokens), regénérer les 2 et mettre à jour `.env` local + `docker compose restart`. Voir `~/.claude/projects/-home-blipinski-Pipeline-Aima-Tower/memory/project_env_leak.md`.
### Skills bioinformatiques
- [ ] **Améliorer skills v1 avec /meta-skills-creator** — sample, debug-nf, check-consistency sont fonctionnels mais créés sans le processus rigoureux. Raffiner après usage.

### Projets bioinformatiques
- [ ] **Aima-Tower — évolutions post-Batches A-F** (socle livré 04-14) :
  - [ ] **Remplacer "Distribution scores Healthy par kit" par scatter TF mVAF v1 vs TF panel génétique** (dans `/analytics` Avancé). X = VAF panel génétique (gene1_vaf, %), Y = mVAF v1 (score méthylation). Trace la corrélation TF_meth ↔ TF_gen. Couleur par indication ou centre, ligne y=x en référence, R² ou Spearman affiché.
  - [ ] **Comprendre et améliorer le Calibration plot** (`/analytics` Avancé). Actuel : qcut en déciles de score + fraction cancer_truth observée + diagonale "calibration parfaite si score = probabilité". Questions à creuser : (1) la diagonale est-elle la bonne référence alors que mVAF v1 n'est pas une probabilité brute mais un score continu ? (2) ajouter un reliability diagram avec CI Wilson par bin, (3) calculer Brier score ou ECE (Expected Calibration Error), (4) envisager isotonic regression ou Platt scaling pour calibrer le score, (5) doc explicative dans le modal `?`.
  - [ ] **Ajouter un backlog dans `/qualite`** — liste persistante d'items à suivre côté surveillance qualité (incidents, anomalies détectées, actions correctives, audits à faire). Champs : date, titre, description, statut (open/in_progress/closed), priorité, lien snapshot/permalien associé. Stockage JSON simple dans `/app/data/qualite_backlog.json` (comme pour les snapshots). UI : tableau CRUD dans une nouvelle carte de la page `/qualite`.
  - [ ] **Enrichir les agents IA (/analytics IA)** avec accès aux métriques exploratory-analysis et aux filtres (actuellement l'agent n'a pas ce contexte).
  - [ ] **Intégrer IGV.js via dash-bio** (visualisation bedMethyl) — reporté, prérequis : réduire la charge de la page /exploration.
  - [ ] **Précompute client-side (point 10)** — reporté : architectural refactor vs ROI limité au vu des temps actuels <200ms. À réactiver si cohorte dépasse 5000 samples.
  - [ ] **Cron alertes dérive (/qualite)** — actuellement les snapshots sont manuels. Ajouter un cron hebdo qui appelle `check_drift()` et envoie email/Slack si alerte (prerequis : SMTP ou webhook configuré).
  - [ ] **Pytest en CI** — les 11 tests tournent en local, les intégrer à un workflow GitHub Actions ou hook pre-commit.
  - [ ] **Feedback itératif** sur usage réel : layout Confrontation, ergonomie des 4 filtres avancés, pertinence des bins VAF, lisibilité ISO 15189 report.
- [ ] **Explorer MethylBERT** — Transformer read-level (Nat Comm 2025) pour améliorer sensibilité basse VAF (<5%). Nécessite GPU. ~2-3 jours.

## Basse priorité

- [ ] **Sécurité secrets — étape 2** : installer `gitleaks` en pre-commit hook sur les projets gittés.
- [ ] **Sécurité secrets — étape 3** : évaluer un gestionnaire de secrets (sops, age, vault).
- [ ] **Skills Pod2Bam** — créer test/qualif/maj analogues à Bam2Beta. Pas urgent tant que Pod2Bam n'est pas soumis à audit qualité.

---

# Partie 2 — En cours

- [ ] **Prise en charge nouveau client** — premier mail envoyé, en attente de retour.

---

# Partie 3 — Complété (par jour)

## 2026-07-22 — Bam2Beta V2.2.0 (module THEMELIO)

- [x] **Module THEMELIO (dépistage cancer) en production** — Themelio 1.0.0 câblé (`workflow/themelio.nf`), score P(cancer) XGBoost Top10 + catégorie dual-threshold, actif en prod/liquid. Wrapper minimal (aucun vendorisé), versions lues des artefacts, mode rétro `--THEMELIO_RETRO`, gardes-fous `SCRIPT_FOR_MODEL`. V2.2.0 taguée, publiée et **qualifiée** (QUALIF/V2.2.0, 37/37). Détails dans [themelio-module.md](../../-home-blipinski-Pipeline-Bam2Beta/memory/themelio-module.md).
- [x] **metadata.json devient le contrat de sortie unique (29 champs)** — BREAKING : `raima_score.V2.json` supprimé, `metadata.json` en est un sur-ensemble strict + bloc versions (`version_bam2beta/raima/too/themelio`) lu de l'artefact, jamais d'un param.
- [x] **Qualif THEMELIO 2 niveaux** — Lung_9 (0.855261) + Lung_100 (0.846397) figés dans `check-conformity.sh` (score + catégorie) ; 6 samples `example_scores` du dépôt reproduits au dernier chiffre via `--THEMELIO_RETRO`, tracés (non rejoués). Comparaison QUALIF vs plateforme TESTV220 : 0 différence de résultat.

## 2026-07-17 — Bam2Beta V2.1.0 (module TOO)

- [x] **Module TOO (Tumor of Origin) en production** — TOO5 v0.4.1 câblé (`workflow/too.nf`), 5 classes tumorales, actif en profil prod. V2.1.0 taguée, publiée et **qualifiée** (QUALIF/V2.1.0, 27/27 conformes). Détails dans [too-module.md](../../-home-blipinski-Pipeline-Bam2Beta/memory/too-module.md).
- [x] **raima_score.V2.json refondu (18 champs)** — BREAKING : `score` supprimé (doublon de `tf`), `model` → `"v1.4"`. Les 2 seuils TOO sortent du bundle (pas d'un param) → le JSON ne peut pas contredire la décision publiée.
- [x] **Qualification refondue autour de 12 valeurs nommées** — Lung_9 comme 2e sample, flag `VALEUR KO` greppable, abandon du bit-à-bit ; fix race `.git/index.lock` (runs qualif séquentiels).

## 2026-07-07 — Bam2Beta module raréfaction cascade

- [x] **Bam2Beta module raréfaction cascade** — nouveau `Rarefaction_Cascade` (BAM rarifiés nestés 20M→10M→5M→2M→1M via `samtools -s`, 2 temps façon small_fragment). Bug racine trouvé + corrigé : `samtools -s` = hash absolu du read-name, même seed en cascade → seuils composés en MIN → comptes faux ; fix = seed incrémenté par niveau. Validé (±0,13 %, nesting 0 orphelin, bug reproduit sur donnée réelle). Commit `b2648b5`, détails [rarefaction-cascade.md](../-home-blipinski-Pipeline-Bam2Beta/memory/rarefaction-cascade.md).

## 2026-07-06 — Bam2Beta V2.0.0 (mVAF v1.4 dans le rapport)

- [x] **Bam2Beta V2.0.0 — mVAF v1.4 dans le champ `tf` du rapport** — `Raima_report` sorti de `Beta_epic` → module `rapport` (main.nf), injecte la mVAF v1.4 (bootstrap 28M) dans `tf` (JSON) + `mvaf` (metadata.json), remplace l'ancienne mVAF. Repro assurée : `set.seed(1)` + tri déterministe des bgzf (`LC_ALL=C`) corrige l'ordre non déterministe de modkit. QUALIF OK (tf=0.58 bit-à-bit vs V1.3.3), repro prouvée Healthy_826 (0.58 ×3) + Breast_48 (64.91 ×3). Docker raima:latest=0.5.3 poussé, release GitHub V2.0.0. Clôt le « gate qualif restant » du 2026-06-25. Détails : [bootstrap-model-v1.md](../-home-blipinski-Pipeline-Bam2Beta/memory/bootstrap-model-v1.md).

## 2026-07-03 — Tower toggle mVAF v1.4 + trace-prod v14/v15 + probs_bootstrap
- [x] **Toggle Score mVAF v1 / v1.4 sur /exploration** — sélecteur pilotant toute la page (tables Sens/Spé + graphes) via `score_source` ; mvaf_v14 lu depuis retd_suivis (VARCHAR virgule FR, KO exclu de la cohorte). Fix bundlé : 4 endpoints graphes (qc/dotplot/methylation/bladder) qui plantaient sur main. Validé live (v1 78.5%/88.4%, v1.4 81.7%/85.3%). Détails : `memory/exploration_score_source_toggle.md`.
- [x] **trace-prod schema v14 — bootstrap_props** — colonne `retd_suivis.bootstrap_props` OK/KO (présence S3 `bootstrap_v1.props.tsv`), liquid only, calque exact de `bootstrap` v12 (pattern preserve). Ajout via `/add-trace-prod`, backfill CGFL 804 + HCL 513 + exports. Commit `b9abd0c`.
- [x] **trace-prod mode `probs --probs_bootstrap`** — probs epic = moyenne des 200 réplicats bootstrap (`extract_bootstrap_means`, vérifié == awk), écrase epic / préserve loyfer, NULL si absent, réversible via `probs --probs`. Backfill CGFL 791/804 + HCL 502/513. Commit `b9abd0c`. Détails : mémoire `probs-bootstrap-mode`.
- [x] **trace-prod schema v15 — dilution enrichie** (session //) — table `dilution` + frag SC + mvaf_v14 + bootstrap_props, retrait frag v1. Commit `b9abd0c`.
- [x] **Feature — Bladder exclu du KPI (--exclude-bladder)** — flag eval.R (câblé main.sh) retire le Bladder sang des unités active/active_nomut ; contre-intuitif : Sens_Active_NoMut +2 à +6 pts (cas difficiles, pas gonflage). Reste dans le train. Commits `885658b`+`1086238`, mémoire `bladder-kpi-exclusion.md`.

## 2026-06-26 — Feature/Tower unité d'éval "suspect" (imageries suspectes)

- [x] **Feature/ + Tower — unité d'éval "suspect"** — flag `--include-suspicious` (`select_cohort_eval.py`) empile 25 imageries suspectes (HCL Lung-DI précoce, `unit='suspect'`, label NULL, hors KPI) ; additivité prouvée 2 variantes (eval_kpis byte-identique, scores existants 0 diff). Tower : onglet "Suspects" (dotplot scores + seuil + compteur N/25), backend `get_suspect_scores` + route, frontend hook + `SuspectChart`. Commits Feature `f08e582`/`47ce642` + Tower `e76f3c3`→`040e515`. Détails : [suspect-eval-unit.md](../-home-blipinski-Pipeline-Feature/memory/suspect-eval-unit.md).
- [x] **Bam2Beta — flux small_fragment (rename short_read)** — stratégie ultra-simple 2-temps : le BAM filtré 75-200 se fait passer pour `merged.bam` dans `CGFL_small_fragments`, cœur du pipeline inchangé. Rename `SHORT_READ`→`SMALL_FRAGMENTS` + module `Small_Fragment`, gotcha `stageAs` anti-collision, Temps 1 testé OK. Commit `d6d4556`, tag rollback `pre-small-fragment`. Détails : [small-fragment-flow.md](../-home-blipinski-Pipeline-Bam2Beta/memory/small-fragment-flow.md).
- [x] **Bam2Beta — arrondi sortie mVAF v1.4** — `mvaf` exprimé en % (×100) puis `x>=1 → round(x,2)` / `x<1 → signif(x,2)`, bloc identique dans bootstrap_trasnfo.R + bootstrap_model_v1.1.R. Commit `f99812e`.
- [x] **Backfill cohort=NULL + régén cohortes/KPI Feature** — 32 healthy HCL (`cohort=NULL` → 'Validation tech') récupérés ; speedvac_yes 192→224 H, no 50→82 H. Cause = filtre `--cohort` (`in_or_null` n'ajoute IS NULL que si 'NULL' listé). 2 variantes re-run (tmux, 2047 combos × 12 unités, 0 erreur), result/ à jour.

## 2026-06-25 — Aima-Tower mvaf_v14 sélecteur /combined + trace-prod schema v13 + Bam2Beta score mVAF v1.4

- [x] **Aima-Tower — mvaf_v14 dans sélecteur /combined** — feature mVAF 1.4 ajoutée à `FEATURE_NAMES` (combined-data.ts), buildé + déployé (conteneur healthy). Gotcha gravé : liste figée à synchroniser à la main avec `Feature/script/main.sh` (combos lus dynamiquement). Commit `9a87362`.
- [x] **trace-prod — colonne mVAF v1.4 (schema v13)** — calque de mvaf_v13 (extraction `cols[1]`, colonne mvaf du fichier V1.4 à 3 colonnes `name·mvaf·model`) + helper `format_mvaf4` (4 décimales, ou 4 chiffres significatifs si <1e-4, jamais de notation scientifique). Câblé check + update-column + export `_LIQUID_QC` après mVAF v1.3. Commit `cd72c61`. Backfill rétrospectif à lancer par Boris. Détails : [project_schema_v13_mvaf_v14.md](../-home-blipinski-Pipeline-trace-prod/memory/project_schema_v13_mvaf_v14.md).
- [x] **Bam2Beta — score mVAF v1.4 (R&D)** — `mean(sqrt(scores))²` sur les 200 scores bootstrap. file 1 `bootstrap_model_v1.1.R` (3 sorties scores+props+V1.4) + file 2 `bootstrap_trasnfo.R` (transfo seule, `--MVAF1_4` rétrospectif). Renommage `--MVAF1_3`→`--MVAF1_4`. Commit `5d6e1b0`. ⚠️ Gate bit-à-bit SORTIE 1 + qualif restant. Détails : [bootstrap-model-v1.md](../-home-blipinski-Pipeline-Bam2Beta/memory/bootstrap-model-v1.md).

## 2026-06-24 — Aima-Tower scission /database + ID sample monitoring + trace-workflow catch-up

- [x] **Scission page /database en 2 pages** — onglets R&D/Platform éclatés en 2 pages sidebar autonomes : R&D (`/database`) + Plateforme (`/database-platform`, `DatabasePlatform.tsx`). 0 backend. Commit `519348e`.
- [x] **ID sample sur Monitoring › Récents** — `--patient_id` parsé depuis `wf.command_line` affiché à droite de `CompletedRow` (`—` si absent). Commit `519348e`.
- [x] **trace-workflow — rattrapage 11→24 juin** — base passée de 152 à 1525 workflows (user + pipeline-prod) via pagination `offset` ; 4 zombies RUNNING du 17 juin (non annulables par Tower car runs non orchestrés) marqués UNKNOWN en base.
- [x] **trace-workflow — catch-up daemon** — `sync --catchup` + rattrapage auto au démarrage du daemon (pagine jusqu'à recouper la base, arrêt à 2 pages stériles) ; testé (trou de 250 comblé en 7,5 s). 3 commits poussés sur `main`.

## 2026-06-23 — Bam2Beta Check_Input + retrait rapport PDF V1.3.3 + trace-prod bootstrap/data HCL-CGFL

- [x] **Bam2Beta V1.3.3 — Check_Input + retrait rapport PDF** — process QC des fichiers d'entrée en amont du merge (input KO → run SUCCESS + REPORT/metadata.json status=FAILED_QC_INPUT, seul Check_Input ; input OK → pipeline normal ; autre erreur → crash) + désactivation du rapport PDF (Raima_report → JSON only). Gotcha NF (channel vide → emit sous-workflow qui plante) fixé par retrait des emits inutilisés (Beta_epic/Frag/IV). TEST OK 3/3 + QUALIF OK 3/3 bit-à-bit vs V1.3.2, release publiée. Détails : [check-input-qc.md](../-home-blipinski-Pipeline-Bam2Beta/memory/check-input-qc.md).
- [x] **Rapport Typst V2 — abandonné** — la migration `rmarkdown → Typst` (Dockerfile.rapportv4) est sans objet : le rapport PDF a été retiré du pipeline en V1.3.3, `Raima_report` ne produit plus que les JSON.
- [x] **trace-prod — bootstrap backfill complet + data HCL/CGFL** — colonne `bootstrap` au plateau (CGFL 788/790, HCL 513/513, 2 KO structurels = Bladder_Urine_02_090 + Twist_10_8) ; +32 HCL Healthy_151-182 intégrés (import-metadata + BAM/POD5) ; remplissages ciblés frag_sc/modes_sc/dorado/extract_full. Routine update-column + exports, zéro code.
- [x] **trace-platform — refonte modèle de statuts (schema v9→v11)** — Ajout WAITING (état 0, pas de `.dl-complete`), ARCHIVED + commande `archive` (DEV >2 mois, sticky), granularité PROD sample-level (`samples.case` v10, `PROD_CUTOFFS` → Compte 1 Romain prod depuis upload ≥2026-06-15), suppression `report_date` (v11), JSON = livrable rapport (PDF non requis → 4 Breast_Demo récupérés FAILED→SUCCESSED). DB recomputée + gsheet ré-exporté (281). Commits `86f3b84`→`c878c33`.
- [x] **Aima-Tower — platform view case effectif + statuts** — Fix bug Samples 15 ≠ Successed 17 (totals regroupés par (client, case effectif) niveau sample), WARNING séparé de SUCCESSED, badges WAITING/ARCHIVED + cartes, retrait report_date. Validé via API (281 réconcilient). Commits `04720af`→`2f70f88`.

## 2026-06-22 — Feature/ dilution (Twist) + Tower /combined refonte+Dilution + Bam2Beta covdepth Étape 1

- [x] **Feature/ — unité d'éval "dilution" (Twist)** — mécanisme `unit` empilant les 22 Twist valides (reps inclus, `Twist_10_8` KO exclu) dans `cohort_eval.csv` aux côtés d'Alc, scorés par les modèles entraînés sur 1023 combos × 2 variantes speedvac → `scores.csv` (`unit='dilution'`, lu par Tower). Additif prouvé : train+Alc + eval_kpis.csv byte-identiques au baseline ; train_combined/infer_eval intacts. Commit `029021f`. Détails : [dilution-eval-unit.md](../-home-blipinski-Pipeline-Feature/memory/dilution-eval-unit.md).
- [x] **Bam2Beta — covdepth Étape 1 (figures QC depth/coverage)** — Fig.1 cumulative depth-vs-breadth (merged vs epic) + Fig.2 positionnelle multi-échelle avec bandes de déplétion systématique, sur 4 samples. Finding : 067 pathologique (34 M reads alignés mais depth=0), concordance parfaite mosdepth↔trace-prod. Scripts versionnés `dev/coverage_analysis/fig{1,2}_*.R`, commit `f1d75be`. Détails : [covdepth-qc-valorization.md](../-home-blipinski-Pipeline-Bam2Beta/memory/covdepth-qc-valorization.md).
- [x] **Aima-Tower — refonte page Combined (ex-/exploration-beta)** — renommage complet (fichiers/route/endpoints) + Résultat en 3 onglets (Initial/Lung-DI/Dilution), suppression panneaux Cohorte/État + orphelins back, défaut SpeedVac, sélecteurs d'éval regroupés à gauche. Commit `0fb9357`, déployé.
- [x] **Aima-Tower — onglet Dilution piloté par le combo** — courbes Twist du combo sélectionné via source unique `scores.csv` (unité `dilution`, archi α : pipeline Feature score les Twist, Tower reste reader) ; lookup colonne `features.replace(',','+')` ; mono ET multi-features XGBoost ; page `/dilution` autonome retirée. Commit `80f6330`, déployé. Détails : [combined_dilution_tab.md](../-home-blipinski-Pipeline-Aima-Tower/memory/combined_dilution_tab.md).

## 2026-06-19 — Aima-Tower /dilution + Feature/Tower dimension depth + Bam2Beta couverture mosdepth

- [x] **Bam2Beta — analyse couverture mosdepth CGFL vs HCL** — outil `dev/coverage_analysis/` (binning per-base→100kb, lecture NFS streaming, parallèle idempotent) + figures cumulative/positionnelle. Finding : couverture autosomale équivalente entre labos, trous = régions non-mappables hg38 (pas d'effet labo, contrairement aux scores). 1 per-base corrompu détecté (Healthy_780). Commit `e1362a1`. Détails : [coverage-analysis-cgfl-hcl.md](../-home-blipinski-Pipeline-Bam2Beta/memory/coverage-analysis-cgfl-hcl.md).
- [x] **Aima-Tower page `/dilution`** — nouvelle page : séries de dilution Twist (principale/Rep2) en 2 panneaux, sélecteur stat mVAF / mVAF v1.3 + toggle spécificité 95/98/99 % (seuil `quantile_type1` healthy speedvac_yes du pipeline Feature, recalculé par stat). Livrée en TDD (17 tests), déployée en prod, documentée. Détails : `feature_dilution_page.md`.
- [x] **Feature/ + Tower — dimension depth à l'éval** — décline sens/spéci à `depth ≥ 0.25/0.5/1/2×` (en plus de target_spec) : `eval.R --depths` + colonne `depth` (scores.csv/eval_kpis.csv), `<select>` Profondeur dans `/exploration-beta` (tables depth==, courbes depth>=). Scores XGBoost bit-identiques (passthrough). Commits Feature `1a90cac` + Tower `5255ac9`, déployé. Détails : [depth-dimension.md](../-home-blipinski-Pipeline-Feature/memory/depth-dimension.md).

## 2026-06-17 — Loyfer déconvolution short-read + Bam2Beta bootstrap raima:0.5.2

- [x] **Loyfer prop sur short-read (2/4 pipelines)** — déconvolution cellulaire (31 types) calculée sur NF_Watchmaker_Methylseq (16×9 rastair) + BP_5base (8, DRAGEN), versionnés `short-read/loyfer_short_read/` (eb235e7+92be8f7). Décrochage high-TF reproductible (Breast_18/Lung_8 → Erythroid_Progenitor, signal TF pas artefact) ; reste NF_Aima/BP_Watchmaker/ONT.
- [x] **Bam2Beta — image bootstrap raima:0.5.2** — bump de l'image dédiée `bootstrap_model` 0.5.1→0.5.2 (Dockerfile + base.config), rebuild + validé bit-à-bit (200/200) sur Lung_138 HCL liquid vs réf Florian (après Breast_10 en 0.5.1). `raima:latest` 0.5.0 intacte. Commit `b36adba`.
- [x] **trace-prod schema v12 — colonne `bootstrap`** — `retd_suivis.bootstrap` OK/KO (liquid only) trackant la présence S3 de `BOOTSTRAP/{sample}.merged.all.bootstrap_v1.tsv` (module Bootstrap Bam2Beta). Pattern preserve via `_s3_exists`. Ajout via skill `/add-trace-prod` (A→E). Backfill CGFL 247 OK/542 KO, HCL 2 OK/511 KO. Commit `ac7f0f5`. Détails : [project_schema_v12_bootstrap.md](../-home-blipinski-Pipeline-trace-prod/memory/project_schema_v12_bootstrap.md).
- [x] **trace-prod — refresh probs + metadata/ONT** — recalcul probs epic v1.3 + Loyfer liquid CGFL (771/772) + HCL (513/513) ; import metadata CGFL+HCL + export ONT Sample (834 lignes) ; 17 nouveaux samples CGFL (Bladder_Urine/Twist) intégrés. Exports gsheet régénérés.

## 2026-06-12 — Feature Lung-DI stades + Aima-Tower Scaleway + Bam2Beta bootstrap mVAF v1

- [x] **Feature/ — 5 unités Lung-DI par stade** — `stage` propagée trace-prod → eval ; 5 strates `lung_I_III`…`lung_NR` dans `eval.R` + section dédiée Tower `/exploration-beta` (best combos étendu). Commit Feature `4ac2adb`. +9/+10 nouveaux cancers trace-prod identifiés (Bladder sang CGFL + HCL_Colon_2).
- [x] **Liens Scaleway désactivés (Aima-Tower)** — tous les liens cliquables vers la console Scaleway retirés (`/database›Platform`, `/monitoring`, `/sample` bouton « Exporter rapport ») ; chemins S3 conservés en texte non cliquable ; Dash legacy `callbacks.py` neutralisé + helpers `s3ToScaleway`/`_s3_to_scaleway` supprimés. Commit `5744647` poussé + déployé, tag rollback `pre-disable-scaleway`.
- [x] **Bam2Beta — feature bootstrap mVAF v1** — process `bootstrap_model` (`raima::bootstrap_model_v1`, 200 scores) câblé en from-scratch (Beta_28M) + rétrospectif (`--bootstrap`), image `raima:0.5.1` (future+withr ; `latest` 0.5.0 intacte). Validé bit-à-bit vs réf Florian (Breast_10). Commit `57b4deb`. Détails : [bootstrap-model-v1.md](../-home-blipinski-Pipeline-Bam2Beta/memory/bootstrap-model-v1.md).

## 2026-06-11 — Feature canon labels + eval sens-spé

- [x] **Feature/ — canon labels + logique eval sens-spé** — effectifs std_359 (359 scorés = 335 labellisés + 24 imagerie suspecte), définitions label dans `label-definitions.md`, inputs et calcul sens/spé `eval.R` clarifiés en session.
- [x] **Feature/ + Tower — pipeline script/ multi-combos × speedvac × 7 unités** — refonte `script/` (select_cohort_train/eval, train.R 1023 combos OOF + inférence eval en mémoire, eval.R baseline vs combiné), cohortes train std_335/std_522 (`--speedvac`), 7e strate `lung_di` (Lung-DI précoce). Tower `/exploration-beta` branchée direct sur `result/speedvac_{no,yes}/` (sélecteur speedvac + spec 98% + best combos par unité + export CSV scores + 7e facette/colonne). Commits Feature `52aa974` / Aima-Tower `0960bbd`.

## 2026-06-10 — Feature train/eval découplé + Alc + Tower Plotly

- [x] **Feature/ — cohorte eval Alc + DB runs/eval_kpis** — train std_335 fixe, inférence Alc (`EVAL_ALC=1`), 6 unités d'éval (`eval_kpis.csv`), DB `runs`+`eval_kpis`, `main_bench.sh` 1023 combos × Alc × spec 0.90/0.95. Bench lancé en tmux.
- [x] **Aima-Tower /exploration-beta — Plotly 6 facettes** — PNG remplacé par courbes sens/spec (5 strates + Alc), CSV legacy reconstruit depuis `scores.csv`/`eval_kpis.csv`, `feature_curves.py` + schéma `runs`/`eval_kpis`, cohorte std_335. Commit `6048729`.

## 2026-06-09 — Feature feature_db + select_cohort + trace-prod loyfer + Tower /exploration-beta

- [x] **Feature/ — feature_db best_combo + chemins PNG/CSV** — `publish` enregistre `png_path`/`csv_path` absolus ; `python3 scripts/feature_db.py best_combo` classe par `delta_sens_active_nomut`. Leader provisoire `mvaf_v1,probs_loyfer` (+21.8 pp). Commit `6188844`.
- [x] **Fix probs loyfer manquantes (HCL V6.0.0)** — 9 samples rebasecalled sans loyfer (décalage temporel d'extraction, pas un bug : fichier `props_loyfer` généré après dernière passe) ré-extraits en `-P` → HCL loyfer 481/481 + export gsheet. Diagnostic : [feedback_probs_loyfer_lag.md](../-home-blipinski-Pipeline-trace-prod/memory/feedback_probs_loyfer_lag.md).
- [x] **Feature/ — extraction select_cohort + fix déterminisme** — sélection cohorte sortie de `train.R` vers `scripts/select_cohort.py` (lignes+labels, gel `data/cohorts/{ref}`, `train.R --cohort`). **Fix repro clé** : `ORDER BY unique_id` rend le combo OOF déterministe (l'ancien code variait ~±2pp sur Sens_Active_NoMut selon l'ordre DuckDB) ; baseline bit-identique. Commits b225ad6..88a12b3, spec/plan `docs/superpowers/{specs,plans}/2026-06-08-select-cohort*`.
- [x] **Aima-Tower /exploration-beta — connexion pipeline Feature** — nouvelle page lecture seule : sélection de features → CSV sensibilité stratifiée (Combined coloré vert/rouge vs baseline mVAF) + PNG + best combos top 5 (réplique read-only `feature_db.py best_combo`) + état cohorte std_359. Aucune exécution conteneur (pas de R, mount `/pipeline:ro`). Commit `b18c572` (v4.3.0). Détails : [feature_pipeline_integration.md](../-home-blipinski-Pipeline-Aima-Tower/memory/feature_pipeline_integration.md).

## 2026-06-08 — Feature pipeline CLI + benchmark 511 combos

- [x] **Feature/ — select_cohort CLI + main.sh + main_bench** — filtres paramétrables (`filtres_cohorte_colonnes.tsv`), `train.R` blocs `probs_epic`/`probs_loyfer`, `./main.sh FEATURES` + bench 511 combos → `feature_runs.duckdb`. Commit `c6b3eb4` push `main`.
- [x] **Feature/ — main.sh --features** — argument explicite `--features` (fini l'argument positionnel), `main_bench.sh` + README/CLAUDE alignés. Commit `f39b7ba`.

## 2026-06-08 — trace-prod schema v11 (mvaf_v13 + frag_score_v2_sc) + bascule props epics v1.3

- [x] **trace-prod schema v11 — mvaf_v13 + frag_score_v2_sc** — 2 colonnes VARCHAR dans `retd_suivis` (liquid only) : `mvaf_v13` (calque `mvaf_v12`, source `raima_score.V1.3.tsv` col 3) + `frag_score_v2_sc` (nouveau checker, `fragmentomics_score.V2.tsv` col 1). Vérifié sur Healthy_826 (mVAF v1.3=2,581) + 26BM01841 (Frag Score v2=0,00755156001789226). Commit `251326e`. Détails : [project_schema_v11_mvaf_v13_frag_score.md](../-home-blipinski-Pipeline-trace-prod/memory/project_schema_v11_mvaf_v13_frag_score.md).
- [x] **trace-prod bascule source props epics → props_v1.3.tsv** — `check_props_epic` + extraction `probs_cmd` lisent `props_v1.3.tsv` (avant `props_v1.tsv`). Recalcul liquid CGFL+HCL (Healthy_826 blood_0 : 0,945857 → 0,8239526) + re-export gsheet (753 + 481). Non répercuté sur short_read/dilution (pipelines séparés). Commit `251326e`.
- [x] **Skill save-code pour trace-prod** — workflow `/save-code` + `/end-session` validé de bout en bout sur trace-prod (analyse → README → CLAUDE.md/mémoire → commit/push → snapshot → todo).

## 2026-06-04 — trace-prod schema v10 frag_sc + Feature pipeline minimal + Pod2Bam V6.0.0

- [x] **Feature/ — pipeline minimal train.R + eval.R** — remplace scripts 01–06 : lecture trace-prod (preset lung/valtech/no SpeedVac/bladder sang), XGBoost OOF → `scores.csv`, eval 5× Sens_* + PNG ; ancien code sous `archives/`. Cohorte SQL 486 → 335 labellisés (50 H). Commit `e5d7d1e` push `main`. Contexte : `memory/context/Feature.md`.
- [x] **trace-prod schema v10 — colonnes frag softclipped** — commit du code non commité (3 colonnes `frag_status_sc`/`frag_mode1_sc`/`frag_mode2_sc` dans `retd_suivis`, calque du frag v1, source `Fragmentomics/filtered_softclipped`). Commit `59dafcb`. Détails : [project_schema_v10_frag_sc.md](../-home-blipinski-Pipeline-trace-prod/memory/project_schema_v10_frag_sc.md).
- [x] **trace-prod nettoyage export liquid** — retrait de 8 colonnes display-only (mVAF v1.2/v2, Score CNV, Frag Mode1/2, Sex Proba, Rarefaction, FRAG), renommage Frag Mode1/2 SC → `Mode1`/`Mode2`, arrondi 2 décimales (`format_round2_comma`). Solid inchangé. Commit `ebf738b`. Exports gsheet CGFL 753 + HCL 472 régénérés.
- [x] **Pod2Bam — support Dorado 2.0.0 / modèle V6.0.0** — image `pod2bam:2.0.0` (Dorado 2.0.0 + hac@v6.0.0 + 5mCG_5hmCG@v1 baked), entrée V6.0.0 dans nextflow.config. `Pod2Bam.sh` devenu LE launcher unique bi-mode (MODE=simplex|multiplex) + durci (retry-loop upload S3, succès=présence BAM vs EXIT_CODE=0, glob trace, upload auto GLOBAL_LOG). Validé en prod : Healthy_11/12/14 basecallés V6.0.0, sync S3 vérifié. Détails : `setup-v6.0.0.md`. Commits `cf0213e` (projet) + `a6e1b63` (config).

## 2026-05-31 — Feature/ pipeline scripts/ standardisé + archive sessions Claude

- [x] **Feature/ — pipeline scripts/ standardisé (01-02-03)** — portage du process exploratory-analysis-CGFL-HCL vers `scripts/` unifié : `01_prepare_cohort.py` (229L) + `02_train_combined.R` (426L, baseline mvaf seul OU XGBoost 5-fold OOF + suspects + heatmaps pseudo-log, non-régression validée vs `score_one_combo.R`, 3 bugs attrapés en séance) + `03_evaluate.R` (284L, BLOC 1 tables validé : Sens_Cancer_AI ALL 78.1% = 02 sens_95_all 0.7812 ; BLOC 2 courbes/dotplot/scatter à écrire). Branche `feat/scripts-standardises` mergée dans `main` (commit `dc732d9` → push `e15233a`). Audit `ARCHITECTURE.md` mermaid sur `exploratory-analysis-CGFL-HCL/understanding`. Session terminée brutalement sur API error 400 (thinking blocks). Détails archive : `~/Pipeline/Feature/memory/session-export-2026-05-31-pipeline-scripts-standardises.md`.

## 2026-05-28 — trace-prod schema v9 table dilution (suivi 480 samples)

- [x] **trace-prod schema v9 — table `dilution`** — suivi du lot autonome de 480 samples Dilution (PK `sample_name`, sans FK) : 2 statuts dérivés bam/prod (1 listing S3/sample) + 13 métriques + 47 probs (16 epic v1 + 31 Loyfer). CLI `check-dilution` / `update-column-dilution` / `export-dilution` (onglet 'Dilution', 19 colonnes dont 3 dérivées du nom, probs exclues = DB only). `DilutionChecker` réutilise BaseChecker (préfixe `.merged`). 8 commits (`4ab208f`→`751fae5`). Détails : [project_schema_v9_dilution.md](../-home-blipinski-Pipeline-trace-prod/memory/project_schema_v9_dilution.md).

## 2026-05-27 — Dilution worker hardening + Bam2Beta V1.3.0 + V1.3.1 releases + trace-prod fix sex_predicted

- [x] **Dilution worker — 3 fixes + audit complet** — fixes accumulés depuis le 22/05 : `e023058` aws s3 ls filter par basename exact (prefix match écartait .bai), `fa9ff27` seed tumor varie par healthy_id (40 réplicats tumoraux indépendants au lieu d'un set partagé), `e3c38cb` @SQ check via capture en variable + test bash pur (même bug pipefail/SIGPIPE que MM/ML). Audit complet validé : aucune commande destructive S3, 40 healthys + 3 tumors paths vérifiés, 480 OUTPUT_NAME uniques. CLAUDE.md gotcha #3 généralisé (`1c2314d`). Détails : memory `feedback_bash_pipefail_sigpipe.md` + `project_phase1_state.md`.
- [x] **Bam2Beta release V1.3.0** — V1.3.0 absorbe V1.2.0 (raima 0.4.17 effectif dans `raima:latest` après rebuild — image était restée 0.4.13 par accident de build du 09/05) + module IV + archive SV modules. QUALIF officielle CONFORME bit-à-bit vs V1.1.2. Tag V1.3.0 + release GitHub publiés. Cross-validation : Healthy_826, Bladder_Blood_02_110, Bladder_Urine_02_050 tous identiques bit-à-bit vs RetD baseline.
- [x] **Refactor architecture Bam2Beta V1.3.0** — 5 refactors structurels : `Raima_score_all` (fusion 3 process en 1, -50% containers Docker BETA), `Beta_epic` (encapsule `BAM_Count` + `Read_Start_Time`), `Merge` (chain propre `BAM_sort → BAM_index` sans redondance `samtools index`), `QC` (`BAM_Count` regroupé dans `qc.nf`, découplé MERGE), suppression workflow `Beta_filter` (R&D non maintenu). 14 commits, 133 fichiers (+2826 / -19339 lignes net).
- [x] **trace-prod fix sex_predicted labels F/M inversés** — bug détecté par Boris en relisant la gsheet : `check_sex_predicted` retournait F si p<0.5 (devait être M, convention biologique). Fix 6 lignes (`lib/checkers.py:309` + docstring + CLAUDE.md + 3 mentions README) + UPDATE SQL atomique swap F↔M sur `retd_suivis.sex_predicted` (732↔567 lignes, NULL=60 préservés) + 3 exports gsheet régénérés (liquid CGFL 741 + liquid HCL 471 + solid CGFL 147 = 1359 samples corrigés). Commit `36748ac`.
- [x] **Bam2Beta V1.3.1 — metadata.json natif** — génération native d'un `metadata.json` dans `REPORT/` par sample (DEPTH=merged uniquement, 10 champs schema trace-platform : client_uuid, analysis_name, patient_name, sample_name, nb_reads_total, nb_reads_aligned, depth, coverage_percent, mvaf, generated_at). Remplace le script externe `~/Pipeline/trace-platform/scripts/build_metadata_json.sh`. 3 fichiers modifiés (`nextflow.config` + `workflow/qc.nf` + `workflow/beta.nf`). 2 commits (feat + docs). Tag V1.3.1 + release GitHub + QUALIF officielle vs V1.3.0 (bit-à-bit identique).

## 2026-05-26 — trace-prod export-short-read-like + cleanup samples Twist + Feature/ pool étendu short_read

- [x] **trace-prod export-short-read-like** — nouvel export gsheet fusionné CGFL+HCL liquid (1199 samples, 13 colonnes) vers l'onglet 'Short Read Like' de la gsheet trace-prod. Inclut `mVAF v1` initial côte à côte avec `mVAF v1 short read` pour comparaison directe. Pattern strictement aligné sur `export-ont-samples`. Commit `3ff5373`. Détails : section Export dans [project_schema_v8_short_read_metrics.md](../-home-blipinski-Pipeline-trace-prod/memory/project_schema_v8_short_read_metrics.md).
- [x] **Cleanup samples Twist test** — suppression de 5 samples Twist (Twist_0%, Twist_0.1%, Twist_0.25%, Twist_0.5%, Twist_1%) via `delete liquid CGFL -s {sample} -f` (cascade sur 6 tables liées), conservation de `Twist_1pct`. Re-export liquid CGFL → gsheet (737 samples).
- [x] **Feature/ — pool étendu 7→11 + 3 livrables + skill `/run-new-feature`** — ajout probs_epic (bloc 16 EPIC v1), probs_loyfer (bloc 31 Loyfer 28M), mvaf_v1_short_read, ichor_short_read_x100 ; infrastructure blocs (`source_cols` pluriel) dans grid_search.py via expand_features(). 3 livrables rule 07 : combined_v2_probs (probes +14.5 pp KPI Sens@95% Active_NoMut), combined_v3 (exploratoire 76% couverture), combined_v4 (rigoureux 99.6%, +4.6 pp KPI). Commit `55c4136` + push initial `github.com/aima-dx/Feature.git`. Skill `/run-new-feature` créé pour orchestrer les futurs tests (9 briques), testé 2 fois. Détails : memory `livrables-actuels.md`.
- [x] **Feature/ documentation visuelle** — WORKFLOW.md Mermaid 9 briques (rendu Cursor/GitHub) + README.md actualisé avec arborescence livrables et mode automatisé. Skill `mermaid-diagrams` installé (softaworks/agent-toolkit, 4.1K installs).

## 2026-05-22 — Skills save-context/get-context + câblage end-session & agent-explore-quick + trace-prod schema v8 short_read_metrics + Projet Dilution (480 BAMs in silico)

- [x] **Skills save-context + get-context** — pattern save/restore du contexte de tâche en cours (comble le trou entre MEMORY.md long terme et agent-explore-quick live). Câblage : `/end-session` Step 2 = `/save-context`, `agent-explore-quick` Étape 2 = lecture inline du snapshot. Snapshots stockés dans `~/.claude/projects/-home-blipinski/memory/context/{projet}.md`. Commits 8a581f0 + 4ba2729.
- [x] **trace-prod schema v8 — table `short_read_metrics`** — nouvelle table 28 colonnes (10 DECIMAL + 16 probs v1 epic) + CLI `check-short-read {liquid} {CGFL|HCL}` indépendante du `check` standard. `ShortReadChecker(BaseChecker)` override seulement 4 méthodes (prefix `merged`→`minLen75_maxLen200`, copie 1:1 du pattern initial). Backfill complet : 426/728 CGFL + 384/471 HCL avec mvaf_v1 extraite. Commit `9af554b`. Détails : [project_schema_v8_short_read_metrics.md](../-home-blipinski-Pipeline-trace-prod/memory/project_schema_v8_short_read_metrics.md).
- [x] **Projet Dilution — Phase 1 + tooling Phase 2** — création from scratch `~/Pipeline/Dilution` pour génération de 480 BAMs dilués in silico (3 tumeurs × 40 healthy × 4 targets). Worker `generate_dilution.sh` (cache flock, log S3, samtools `-@ 2`) + orchestrateur `run_all.sh` (filtres `--tumor`/`--target`). Phase 1 (`Colon_7_Healthy_807_target_1_0`) uploadée S3 + validée end-to-end Bam2Beta (mVAF=0 cohérent sous seuil à 0.28% VAF effective). Bug `bash pipefail/SIGPIPE` en command substitution identifié + fix via fichier temp (commit `30ff946`). Détails : `~/Pipeline/Dilution/docs/design.md` + memory `feedback_bash_pipefail_sigpipe.md`.

## 2026-05-21 — trace-prod schema v7 + skill add-trace-prod + démo platform Bladder/Breast

- [x] **trace-prod schema v7 — colonne `short_read`** — tracke le subsampling 75-200 bp (liquid uniquement) via listing récursif S3 sur bucket mirror `{LABO}_short_read` : OK si les 6 dossiers (BAM, BETA, CNV, QC, REPORT, ichorCNA) sont présents et non vides. Pattern preserve sur erreur S3 (`_update_short_read` dédié). Gotcha attrapé : `aws s3 ls --recursive` retourne clés S3 complètes → stripper avec `sample_prefix`. Commit `71937aa` (+496 lignes dont 381 de doc README v2→v7).
- [x] **Skill `add-trace-prod`** — workflow guidé pour reproduire l'ajout de colonne trace-prod : 5 étapes A→E avec validation utilisateur entre chaque, arrêt avant exécution rétrospective. 10 fichiers (SKILL.md + 4 steps/ + 3 patterns/ + 1 decisions/ + 1 gotchas/). Validé via `quick_validate.py`. Skill global `~/.claude/skills/add-trace-prod/`.
- [x] **Memory trace-prod compactée** — MEMORY.md passé de 222 → 146 lignes (sous la limite 200). 13 sections détaillées déportées vers nouveau topic `project_columns_index.md` (v2-v7 synthèse + patterns transversaux : collision mapping, gene1_vaf raima, rebasecalled propagation, NFS-first, export ONT, BAM completude fallback).
- [x] **Démo samples client CGFL — 82 Bladder + 4 Breast** — copié `aima-bam-data/processed/MRD/RetD/liquid/CGFL/{Bladder_Blood_*,Bladder_Urine_*,Breast_*}` vers `aima-platform/data/198e71d4-.../MRD/` (3-4 fichiers/sample + metadata.json depuis trace-prod). Patient `Breast_Demo` avec 4 mVAF diversifiés (0 / 0.41 / 1.06 / 2.58). Schema metadata.json final : 9 champs (suppression `nb_reads_epic` + `ratio_percent`).
- [x] **eCRF_bladder.csv** — export 82 samples Bladder × 48 colonnes depuis trace-prod (`samples` + `metadata`) à la racine de trace-platform. Commit `a7efc7d`.

## 2026-05-20 — trace-prod schema v6 IV/QC (4 colonnes retd_suivis)

- [x] **trace-prod schema v6 — colonnes IV/QC (Vérifier qualité IV via trace-prod)** — ajout `read_start_time`, `ancestry`, `sex_proba`, `sex_predicted` dans `retd_suivis` (VARCHAR libre, pas STATUS_COLUMNS). Sources : `IV/{sample}.ancestry.tsv` (argmax sur 18 ancestries), `IV/{sample}.sex.tsv` (proba arrondie au millième + F/M selon seuil 0.5), `QC/Samtools/{sample}.read_start_time.tsv` (check présence sans lecture, fichier 3-4 GB). Path IV/ : **sœur de QC/, pas dedans**. Câblé dans `Liquid` + `SolidChecker`, 4 entrées `COLUMN_CHECKERS`. Commit `c5aa8a2`. Détails : `project_schema_v6_iv_qc.md`.

## 2026-05-13 — Aima-Tower v4.2.0 pages /samples + /sample/:id

- [x] **Pages /samples + /sample/:id Tower v4.2.0** — liste samples R&D (~1100, filtres labo/type/statut) + vue détail mockup-style avec KPIs trace-prod (TF=mvaf_v1, Negative/Positive strict ==0/>0, depth≥0.25×). Backend `DatabaseService.get_sample_detail()` JOIN 5 tables. Animation `aima-rise` cascade sur toutes les pages via `key={location.pathname}`. Commits `7a71ae0` + `a7cbf85`, tag `v4.2.0` (Docker rebuild prod healthy). Détails : `feature_sample_detail.md`.

## 2026-05-12 — Audit & purge raw HCL bucket BAM + trace-platform onboarding IRCCS

- [x] **Purge raw HCL bucket BAM (111 NANO)** — audit complétude raw → liquid sur 37 NANO actifs (112 samples), correction de 2 mismatches (NANO14_N3 BAM + NANO22_N2b POD5 ~111 GB), sauvegarde de 29 rapports HTML MinKNOW localement, puis `aws s3 rm` + création `upload.done` (taille raw 0). Découverte chemin BAM mergé `processed/MRD/RetD/liquid/HCL/{sample}/BAM/`. Détails : `audit_nano_2026-05-11.md` + `suppression_raw.md` + `last_clean.sh`. Commit `a6312c1`.
- [x] **trace-platform — onboarding IRCCS (Matteo) + 4 nouveaux UUID + scan** — ajout 5 users dans `export_labs_users.tsv` (1 PROD IRCCS Matteo Allegretti / 4 DEV dont 2e UUID Romain CGFL + 3 sandbox Unknown), `check --new` ajoute 36 samples (16 Bladder/FR Romain SUCCESSED, 12 baseline/c3d4 Romain SUCCESSED, 2 T0 Matteo, 3 Frederic, 3 sandbox FAILED). pt100/pt107 IRCCS forcés SUCCESSED manuellement (BAM uploadés sans `.bai`, override cascade).
- [x] **trace-platform — fix `dorado_model_version` + feat GSheet manual columns** — `extract_metadata()` oubliait de copier `dorado_model_version` depuis samtools_meta (laissait None même quand BAM contenait `@v5.0.0`). Ajout colonnes manuelles `Commentaire` + `Cancer type` préservées entre exports (matching Sample+Patient+Client UUID, méta-catégorie `Informations complémentaires`). Commits `80b1a07` (typo Plateform→Platform), `c8a5cdc` (fix version), `300a239` (feat manual cols).

## 2026-05-09 — Aima-Tower fix Home stockage + URLs Scaleway + SampleSheetChecker consolidation NANO22-23

- [x] **Aima-Tower v3 — fix jauge stockage Home + URLs Scaleway Monitoring** — bind-mount /scratch et /scratch2 dans le container + whitelist `MONITORED_DISKS` (root + scratch) avec label disque mis en valeur (dot coloré, font 15px semibold). `s3ToScaleway` concatène désormais le path après `/files/` au lieu de `?path=...` (l'ancien format ouvrait la racine du bucket). Fige `name: aima-tower` dans docker-compose pour éviter la divergence images/containers depuis Aima-Tower-main. Commit `f136e7a`. Détails : [feedback_compose_project_name.md](../-home-blipinski-Pipeline-Aima-Tower/memory/feedback_compose_project_name.md).
- [x] **SampleSheetChecker — sample sheets ss5-ss9** — création de 8 TSV (Healthy_59-66/111-150 + Lung_81-144 + Nuclear_13-16) pour les batchs reçus du 21/03 au 09/05 (NANO13-25). Sync ss5 bam+pod5 validé. Commit `1675155`.
- [x] **NANO14_N3 retrouvé (Healthy_83-86)** — run historique perdu depuis le 12/03 re-uploadé le 8-9 mai (1.4 TB). Total 9/9 runs reçus comme planifié (NANO22 N1/N2b/N3/N4 + NANO23 N1-N4 + NANO14_N3) via cron `at` jeudi 21h.
- [x] **Consolidation variants b/c → originaux NANO22/23 (bam_pass)** — fusion de 9 paires de runs via `aws s3 cp --recursive` (61.8 GB / 33 156 fichiers, **0 collision**) grâce à l'unicité `{run_id}_{acquisition_id}` dans les noms MinKNOW. Pod5_pass restant à faire. Détails : [MEMORY.md](../-home-blipinski-Pipeline-SampleSheetChecker/memory/MEMORY.md).

## 2026-05-07 — trace-prod schema v5 cohort + Feature/ grid search + Tower v3.0.0 cutover + Bam2Beta module IV / raima 0.4.17 + rapport PDF Typst V2

- [x] **Refonte rapport PDF ctDNA en Typst V2 (R&D)** — pivot LaTeX/XeLaTeX → Typst 0.14.2 + direction GRAIL Galleri retenue (donut TF + ✓/✗ vectoriel cetz + KPI cards + palette hybride AIMA/Éxís). Source `test/V2final/report-grail-v2.typ` + 4 PDFs de test (NEG/POS × clean/warning). Intégration pipeline prévue lundi 2026-05-11. Commit Bam2Beta `574e779`. Détails : [report_pdf_typst_v2.md](../-home-blipinski-Pipeline-Bam2Beta/memory/report_pdf_typst_v2.md).
- [x] **trace-prod schema v5 — colonne metadata.cohort** — ajout `metadata.cohort` (VARCHAR) + mapping `Cohorte → cohort` (col 48 gsheets CGFL+HCL) + `HARMONIZATION_RULES["cohort"]` défensif (casse/accent). 924 samples remplis via `import-metadata` (479 CGFL + 445 HCL). README + CLAUDE.md à jour. Commit `f433341`.
- [x] **Projet Feature/ — base de connaissance + grid search XGBoost** — création projet séparé `~/Pipeline/Feature/` avec contexte des 4 projets sources (CLAUDE.md + 7 rules + memory) + pipeline validation Michael ↔ Feature (poc bit-exact + current à jour) + grid search exhaustif 957 combos (taille 3-8) qui identifie une combo +12 pp Sens@95% Active_NoMut vs config initiale Michael (`mvaf+mvaf_v2+ichor+score_cnv+frag1+frag2+loyfer_non_wbc`). Tableau final KPI en mémoire pour comparer futures features. Repo git local seul.
- [x] **Réimport metadata HCL trace-prod** — récup de 44 nouveaux Lung HCL sans metadata + transition `oui → probable` pour Lung_19/23/83/84 (modif GSheet post-27/04). 378 importés, 12 manquants (Lung_133-144 pas encore checkés via `tp check`).
- [x] **Aima-Tower v3.0.0 — cutover Plan G en prod** — refonte UI complète (FastAPI + Vite + React + Tailwind v4) mergée sur main + tag `v3.0.0` (`d91f80b`). Tower main Dash archivée en `v2.3.0` (point de retour). Container `aima-tower-dashboard` actif sur tower.aima-diagnostics.com avec basic auth Caddy. Validation cell-by-cell vs v2.3.0 : 266 cancer / 192 healthy / Sens 84.6% / Spec 89.1%. Plan C (`feat/ui-refresh-c`, DMC sur Dash) conservé. Détails : [project_v3_cutover.md](../-home-blipinski-Pipeline-Aima-Tower/memory/project_v3_cutover.md).
- [x] **Aima-Tower /exploration — cascade cohorte + UI cleanup multi-utilisateurs** — intégration feature cohort cascade (backend `compute_cohort_cascade()` `@lru_cache(64)` + endpoint `/api/exploration/cohort-cascade` + frontend `useCohortCascade` TanStack Query lazy + `useDebouncedValue(250ms)`). Cleanup multi-utilisateurs : thème light par défaut, retrait mentions "Boris" / "Plan G" / "feat/ui-refresh-g" / "Internal · v3 preview" sur Sidebar + Home + Exploration. Rebuild Docker + redéploiement prod. Commit `9327e1b`. Détails : [feature_cohort_cascade_integration.md](../-home-blipinski-Pipeline-Aima-Tower/memory/feature_cohort_cascade_integration.md).
- [x] **Tower v3 — cascade cohorte étendue + liste samples + fluidité** — extension `/exploration` v3 : cascade 14 paliers descriptifs, filtre `cohort` opérationnel (m.cohort ajoutée à la query DuckDB), liste samples cohorte (TP/TN/FP/FN avec recherche), fix dedup misclassified (82 FN → 41), debounce sliders 250ms + keepPreviousData TanStack.
- [x] **Bam2Beta — préparation V1.2.0 (commit `dbb174c`)** — bump raima 0.4.13→0.4.17 (test Healthy_826 identique bit-à-bit V1.1.2) + modules Sniffles2/Severus/Decoil archivés vers `dev/archive/` + doc/memory à jour. Tag V1.2.0 + release reportés à lundi 2026-05-11.
- [x] **Bam2Beta — nouveau module IV (Identité de Vigilance)** — `workflow/IV.nf` + `bin/iv_score.R` (raima `infer_sex` + `infer_ancestry`). Outputs `${ID}.{sex,ancestry}.tsv` (1+2 lignes tab-séparées, 18 colonnes nommées). Activé prod/liquid/solid + mode rétrospectif. Validé Healthy_826 (CGFL solid) + Healthy_4 (HCL liquid retro).

## 2026-04-30 — Refonte Aima-Tower /exploration v2.3 + onglet Avancé graphique + validation R

- [x] **Refonte page /exploration v2.3** — layout 25/75 sticky (radio Centre + sliders inline ultra-réactifs), ~50 filtres dynamiques pattern Analytics (multi/range/date/text) avec helpers no-op (`_legacy_set_or_none`, `_active_cancer_param`), nouvel onglet **Avancé** graphique (boxplot ad-hoc reuse `build_boxplot`), 2 cohortes distinctes Sens/Spé (R02) vs Graphique (R04). Tests SpeedVac (snapshot + partition invariant). Mémoire : [exploration_v2_3_design.md](../-home-blipinski-Pipeline-Aima-Tower/memory/exploration_v2_3_design.md) + [dash_4_gotchas.md](../-home-blipinski-Pipeline-Aima-Tower/memory/dash_4_gotchas.md).
- [x] **Validation Tower ≡ R main cell-by-cell** — confirmé sur DB actuelle aux targets 0.85 et 0.90, mode=ge5 : detection_global, stratified_global, by_indication_global tous identiques au pipeline R `~/Pipeline/exploratory-analysis-CGFL-HCL` branch main.
- [x] **Refresh README Aima-Tower** — sections `/exploration` + `/qualite` ajoutées au README + changelog v2.3.0 (refonte filtres + onglet Avancé graphique). Section `/survey` post-v6.2 reste à faire si nécessaire.

## 2026-04-29 — trace-prod schema v4 + ONT Sample export

- [x] **trace-prod schema v4 — colonne speedvac** — ajout `metadata.speedvac` (VARCHAR), mappings `SpeedVac`/`SpeedVAc` → speedvac (gère casse différente CGFL/HCL), harmonisation Yes/No via `HARMONIZATION_RULES["speedvac"]`. Coverage : 471/708 CGFL liquid + 401/401 HCL liquid. Commit `aafc159`.
- [x] **Fix stage CGFL silencieux** — ajout mapping `"Stage" → stage` (la col HCL longue `"Stage (I, II, III...)"` n'existait pas côté CGFL, stage CGFL était 100% NULL). 0 → 281/708 CGFL liquid. Commit `aafc159`.
- [x] **Fix collision mappings TSV_TO_DB_METADATA** — `upsert_metadata` ne doit pas écraser une valeur déjà non-None par None quand 2 `tsv_col` pointent vers le même `db_col`. Sans ce fix, ajouter `Stage`/`SpeedVAc` cassait silencieusement les imports précédents. Commit `aafc159`.
- [x] **Export ONT Sample — metadata fusionnée → gsheet trace-prod** — nouvelle commande CLI `export-ont-samples` qui exporte la table `metadata` fusionnée (CGFL+HCL liquid) vers l'onglet `'ONT Sample'`. 51 cols (3 tech + ~46 metadata + 2 calculées), rebasecalled exclus par défaut, headers dédupliqués par db_col. 687 lignes (357 CGFL + 330 HCL), SpeedVac 100%, Stage 53%. Commit `8d0cb12`.

## 2026-04-28 — Aima-Tower Overview + figures /exploration + trace-prod fix BETA_28M/audit 6mA + Bam2Beta V1.2.0 SVs

- [x] **Page Overview Aima-Tower — 2 onglets** — Infrastructure (S3.md existant) + nouveau Database (synthèse des 94 filtres visibles de `/analytics > Avancé` avec valeurs distinctes et nb samples par choix). Refactor : extraction `_get_visible_filter_columns()` réutilisable + `get_value_counts()` + cache `_counts_cache`. Commit `309c983`.
- [x] **Aima-Tower /exploration — figures R04-R07 vers Graphiques** — déplacement de QC reads, QC depth, mVAF, TF/VAF, Bladder de l'onglet Tableaux vers 5 nouveaux sous-onglets de Graphiques (en amont des 4 existants Scores/ROC/Sens/Sens-profondeur). Conditions d'affichage et réactivité aux sliders préservées. Commit `4bfcdda`.
- [x] **Fix check_beta_28m faux-positif ghost** — exigence 44 fichiers réels (size>0) + ≤1 ghost (size=0), évite le cas "43 réels + 1 ghost = 44 total". 1 faux-positif débusqué : `Healthy_26_rebasecalled_V4.3.0` (HCL) — `chr18.bedMethyl.gz` absent. Commit `0b49cb5`.
- [x] **Audit modification 6mA ('a' col4) sur bedMethyl liquid** — scan exhaustif 7247 fichiers + recheck 1114 `.merged.epic.bedMethyl.gz` → 0 match. Aucun sample liquid (CGFL+HCL) ne contient de 6mA dans BETA. Cohérent avec pipeline ciblant 5mC only.
- [x] **Audit 6mA sur 4 premiers Colon_ solid** — les 4 ont des matches dans `.merged.epic.bedMethyl.gz` (45k–86k lignes 'a' sur ~2.6M lignes total). Comportement asymétrique liquid vs solid à investiguer.
- [x] **Bam2Beta V1.2.0 — modules Sniffles2 + Decoil + Severus** — détection SVs ONT (mode mosaic Sniffles2) + reconstruction ecDNA (Decoil) + SVs somatiques tumor-only avec phasing Clair3+LongPhase (Severus). 3 nouveaux containers + 2 workflows (`workflow/Sniffles2.nf` 2 process, `workflow/Severus.nf` 3 process). Validation Healthy_826 OK, Colon_3 en cours (Severus_clair3). Caveat : Decoil non validé plasma 5-30x. Commit `23bcf54`. Détails : `~/.claude/projects/-home-blipinski-Pipeline-Bam2Beta/memory/sv_modules.md`.

## 2026-04-27 — exploratory-analysis-CGFL-HCL : pipeline 04-07 + DuckDB enrichi + doc sync

- [x] **Pipeline R étendu 04-07** — `run_pipeline.R` orchestre maintenant 01→07 : `04_qc_plot.R` (QC reads/depth), `05_mvaf_dotplot_by_center.R` (log1p), `06_plot_methylation_tf_vs_genomic_vaf.R` (concordance TF méth ↔ VAF génomique), `07_bladder_sensitivity_and_mvaf.R` (stage/grade, grille spec 0.85→0.99). Ajout `nb_reads_total`.
- [x] **Export DuckDB enrichi** — `00_export_from_duckdb.py` exporte désormais Comments / Stage / Grade en plus des colonnes existantes.
- [x] **`multicentric_results/` ajouté** — scripts `01_barplot_counts.R` + `02_speci_sensi.R` (analyses multicentriques standalone).
- [x] **Doc sync README + CLAUDE.md** — sections 04-07 documentées, wrapper `run_all.sh` + `run_pipeline.R` clarifié. `.gitignore` étendu (`rds_duckdb_run/`, `Rplots.pdf`). Branche `tower` push complète (11 commits dont `0f9925a`).

## 2026-04-24 — Clean-skill (création + audits Tower) + Aima-Survey v6.2 + Refonte /analytics Avancé

- [x] **Refonte onglet `/analytics` Avancé** — suppression des 4 figures du Batch A (distribution kit / calibration / stats CGFL-HCL / clustering FN-FP). Remplacé par panneau de **148 filtres dynamiques** auto-détectés depuis trace-prod (nouveau `src/filters_service.py`, 207 L) + 1 figure boxplot paramétrable (17 métriques Y en radio, split/group/color, pseudo-valeur "ALL" dans labo, échelle log Y, QC thresholds 5M / 0.25). Les 2 tâches Partie 1 "Remplacer Distribution scores Healthy" et "Améliorer Calibration plot" deviennent caduques (cartes sources supprimées).
- [x] **Clean-skill Aima-Survey v6.2** — nettoyage exhaustif −1446 lignes net (19 fichiers). Suppressions : support biorxiv/medrxiv dormant (`lib/sources/biorxiv.py` + 17 queries + tests), migration v5→v6 one-shot (`lib/migrate.py` + CLI `migrate` + `scoring_cache.db`), `upsert_synthesis` + colonnes `synthesis_*` (Tower cache RAM, aucun SELECT sur la colonne), 2 scripts one-shot (`backfill_entrez_date`, `reclassify_2026_04_20`). 8 tests cassés par fusion v6.1 réparés (`ctDNA_methylation_ONT` → `cancer_detection_cfDNA`). 69 tests verts, pyflakes 0 warning, smoke fetch réel OK. Commit `1609ce1`.
- [x] **Refresh README Aima-Survey** — réécrit pour refléter v6.2 : 13 queries PubMed (suppression des 17 preprints dormantes), DuckDB single-table, `CLAUDE_CODE_OAUTH_TOKEN`, classification sector/org_type, retrait refs `scoring_cache`/`ANTHROPIC_API_KEY`/`migrate`. Partie Aima-Tower du bullet initial reste à faire.
- [x] **Skill `/clean-skill` créé** — nettoyage code multi-langage (Python/Nextflow/R/Bash) générique pour projets `~/Pipeline/`. Checkpoint git obligatoire (commit + tag) avant modif, rapport classifié 🟢/🟡/🔴 par niveau de confiance, `Edit` chirurgical, respect Karpathy + Golden Rules. Installé dans `~/.claude/skills/clean-skill/SKILL.md` (228 lignes).
- [x] **Audit clean Aima-Tower (test `/clean-skill`)** — codebase confirmée propre : 29 lignes mortes détectées sur 9712 (0.3 %), aucune duplication pathologique, aucun over-engineering. Refactor senior Python chiffré à 40-50 % code touché pour +25-40 % lignes (tests) et 50-80 h — non rentable au profil bus-factor=1. Aucune modif appliquée, checkpoint rollback OK.
- [x] **Audit arborescence Aima-Tower** — identifié à nettoyer : `launch.sh` (92 L, jamais utilisé ni dans CLAUDE.md), `VERSION` (6 B, jamais lu), `.pytest_cache/` à ajouter au `.gitignore`, `scripts/update_bookmark_categories.py` (migration one-shot idempotente déjà appliquée). Sécurité à re-vérifier : `.env` encore tracked selon `git ls-files` (contradiction avec memory du 2026-04-21).

## 2026-04-22 — Aima-Survey entrez_date + Tower vues temporelles first_seen_at + panel filtres Survey + preprints dormants + Tower multi-source

- [x] **Fix cron Aima-Survey (PATH)** — `run_veille.sh` exporte `PATH=~/.local/bin:$PATH` pour que `subprocess["claude"]` soit trouve (scoring + classification Haiku). Cron du 22/04 avait crash sur `FileNotFoundError: claude`.
- [x] **Colonne `entrez_date` Aima-Survey** — PubMed EDAT stockee comme source de verite d'indexation. Schema + parser XML (`PubmedPubDate[@PubStatus="entrez"]`) + `first_seen_at = entrez_date` a l'insert. Backfill one-shot 439/439 articles (`scripts/backfill_entrez_date.py`), range 2025-03-19 → 2026-04-21.
- [x] **Vues temporelles Tower pilotees par first_seen_at** — filtres Week/Month/Year basculent de `pub_date` (sujet aux dates futures genre 2026-12) a `first_seen_at` (EDAT immuable). Vue Jour migree DuckDB (`DATE(first_seen_at) = ?`), avec selecteur conditionnel alimente par `list_first_seen_dates()`. Fenetres post-backfill : Week=15 / Month=92 / Year=436 (vs 411/411/411 avant).
- [x] **Affichage card Survey** — 2 dates distinctes : "Indexé : YYYY-MM-DD • Publié : YYYY-MM-DD". Plus d'ambiguite entre date cron et date journal.
- [x] **Redesign panel filtres /survey** — aligne patterns Tower (Card+CardHeader, g-3, Row Vue+Jour conditionnel+Reset ms-auto / Row Recherche+Priorite+Rubrique+Journal+Secteur+Etat). Suppression bouton "Tout marquer lu" + callback `bulk_mark_seen`.
- [x] **IMBdx ajoute aux concurrents** — entree tier_2 dans `competitors.json` (threat MOYENNE). Article PMID 42014847 remonte dans onglet Concurrence via `org_name` substring.
- [x] **`is_competitor_article` etendu** (variant B') — matche desormais `org_name` OR `last_author_affiliation`. Nouveau champ `Article.last_author_affiliation` propage via SELECT DuckDB. Passe de 11 a 29 articles concurrents.
- [x] **Aima-Survey — preprints biorxiv/medrxiv (dormant)** — `lib/sources/biorxiv.py` (web scraping medrxiv.org/search + meta `citation_*`), 17 queries calquées sur PubMed, 16 tests verts. Désactivé en final (`build_sources()` commenté) : moteur medrxiv.org retourne trop de faux positifs sur les queries OR-groupées (seul `fragmentomics` matchait vraiment le papier Sauer ciblé). Code conservé, réactivable en décommentant 2 lignes quand les queries seront affinées.
- [x] **Aima-Tower /survey multi-source** — filtre `WHERE source='pubmed'` retiré de `survey_service.py:392`, badge source (PubMed bleu / preprints cyan) + labels génériques "Indexé/Publié" dans `survey_render.py`. 7 tests duckdb verts. Changements conservés (inoffensifs même sources dormantes).

## 2026-04-21 — Aima-Tower sécurisation + HCL runs + backup S3 + check Healthy + import metadata + migration IA Max + Aima-Survey classif concurrents

- [x] **Import metadata HCL + CGFL depuis gsheets** — 314 HCL + 341 CGFL importés (tous les samples de la table `samples` matchés), logique VAF Tumoral-only appliquée, 184 rebasecalled re-synchronisés.
- [x] **Fix import-metadata fallback Sample name** — les `*bis` cherchés via `Old sample name="Breast_1_bis"` (legacy underscore) alors que DB stocke `"Breast_1bis"`. Fallback ajouté. +4 samples récupérés. Commit `5ab85ac`.
- [x] **Force re-propagation rebasecalled systématique** — re-sync auto metadata vers TOUTES les variantes `*rebasecalled*` à chaque import-metadata (évite divergences `stage="stade IV"` vs `"IV"`). 184 rebasecalled alignés. Commit `65ac91b`.
- [x] **Sécurisation Aima-Tower HTTPS + basic auth** — Caddy reverse proxy + cert Let's Encrypt auto (TLS-ALPN-01) + `basic_auth` bcrypt cost=14 (user `aima`), port 8050 fermé à Internet (`expose:` au lieu de `ports:`), `SECRET_KEY` Flask depuis `.env` + `SESSION_COOKIE_SECURE=True`. `.env` retiré du tracking git (était pushé sur `aima-dx/Aima-Tower` — incident détecté et documenté). Rotation secrets Anthropic/Seqera reportée (repo privé, Boris seul dev). Commits `a2321e1` (Aima-Tower) + `bee7b2e` (claude-config). URL prod : `https://tower.aima-diagnostics.com`. Détails mémoire : `security_setup.md`, `project_env_leak.md`.
- [x] **32 samples HCL Bam2Beta** — lancés en PROD, nouveaux samples intégrés dans la cohorte exploratory.
- [x] **Sauvegarde HCL sur S3** — BAM + POD5 des 32 samples uploadés, counts vérifiés.
- [x] **Check prod Healthy** — état de production des samples Healthy vérifié.
- [x] **Migration IA Tower vers Claude Max (abonnement Pro)** — 5 appels API Anthropic (Survey + Analytics ×2 + DB Q&A ×2) basculés vers CLI `claude -p` + token OAuth long-lived, modèle unifié `claude-sonnet-4-6`, contexte injecté = 14 CLAUDE.md `~/Pipeline/*/` (16-20K tokens). Nouveau `src/claude_cli.py`, Dockerfile + Node.js + @anthropic-ai/claude-code global, `ANTHROPIC_API_KEY` retiré du container (priorité sur OAuth quand coexistent), HOME override au subprocess pour isoler totalement `~/.claude` du host. Plan : `~/.claude/plans/c-avec-sonnet-4-6-indexed-bubble.md`.
- [x] **Aima-Survey v6.1 — classification sector/org_type via Haiku** — +8 colonnes DB (affiliations, last_author_affiliation, sector, org_type, org_name, classification_why/model/at), `lib/classifier.py` avec batch N=5 + IDs explicites, short-circuit gratuit si pas d'affiliation. Migration complète vers abonnement Claude Pro/Max via `lib/claude_cli.py` (fin crédits API, pattern copié de Aima-Tower). 353 articles classifiés. Mémoire : `aima_survey_v61.md`, `claude_pro_auth_pattern.md`.
- [x] **Aima-Survey — veille active concurrents** — 22 entreprises identifiées (recherche web approfondie via agent-websearch + `/prompt-creator`), `data/competitors.json` + `docs/COMPETITORS.md` versionnés (3 tiers + aliases PubMed-ready + synthèse stratégique). Query PubMed `competitive_affiliations` dans queries.json (19 acteurs ciblés). Mémoire : `competitive_landscape.md`.
- [x] **Aima-Tower — onglet Concurrence + page /competitors + vue Année** — onglet "Concurrence" dans `/survey` basé sur `org_name` matching competitors.json (fix bug : Volition/GRAIL apparaissent, Stanford/Mayo/Karolinska filtrés automatiquement). Nouvelle page `/competitors` (3 tiers + synthèse stratégique + stats publis DB). Dropdown "Secteur / Organisation" multi-select (93 options). Vue Semaine passée sur DuckDB 7j glissants (stable vs 7 rapports), nouvelle vue "Année" 365j.
- [x] **Batch processing classifier (N=5)** — `classify_batch()` avec IDs explicites, re-indexing défensif contre inversion Haiku, fallback individuel par article si batch fail. Gain ~2× vs séquentiel (smoke test 2 articles = 16s).
- [x] **Slider depth min=0 aligné 3 pages** — `/exploration`, `/qualite`, `/analytics` Avancé : slider depth accepte la valeur 0 (`min=0.10`→`0.0`), marks ajustés. Commit `6b792ff`.
- [x] **Figure sensibilité par stade cancer** — nouvelle section en bas de `/exploration` > Graphiques : forest plot (CI Wilson 95%) + bar plot (gradient couleur) par stade I/II/III/IV/NR, visibles dans 3 onglets (ALL/CGFL/HCL). Stage lu depuis `metadata.stage`, CGFL tous en NR (colonne vide côté CGFL). Commit `3a60af3`.

## 2026-04-20 — Aima-Survey refonte v6 + Aima-Tower /survey + /exploration

### Aima-Survey — refonte v6 (8 commits)

- [x] **Aima-Survey v6 — DuckDB single-table multi-source** — `lib/db.py` + table `articles` avec colonnes `external_id`, `source`, `score`, `score_why`, `first_seen_at` (commits `636f83b`, `a65a4e7`, `af1341b`, `fa13c65`, `30b6587`, `939a0bd`).
- [x] **Aima-Survey v6 — CLI Click complet** — `cli.py` : `add`/`remove`/`list`/`query`/`stats`/`export`/`backfill`. `veille.py` refactoré pour lire la DB + nouveau `lib/render.py` dédié markdown.
- [x] **Aima-Survey — fusion rubriques + +5 rubriques** — fusion ctDNA+cancer, fusion outils, suppression high_impact_journals (`4fec01a`) ; ajout MRD, MCED, tissue-origin, ML classifiers, EPIC/Illumina (`73ff597`). Total 12 rubriques.

### Aima-Tower /survey — intégration DuckDB v6 (13 commits)

- [x] **Tower /survey — lit `aima_survey.duckdb`** — `SurveyService._articles_from_duckdb` pour vues mois/all (READ_ONLY + retry backoff), fallback markdown si DB KO. Config paths + mount Docker Aima-Survey (commits `93958bd`, `2183bc3`).
- [x] **Tower /survey — 5 vues temporelles** — jour / semaine (défaut) / mois / all / **Favoris** (5e mode, `4d5cd27`). Semaine par défaut à chaque ouverture (`7a10c12`), suppression DatePickerRange + slider Score IA min (`702f520`), suppression onglet "Top articles" vue Semaine (`19f1197`).
- [x] **Tower /survey — fixes parser + onglets** — un article ne peut être que dans un seul onglet rubrique (`de66540`), vue Mois filtre strictement `pub_date` (retire OR first_seen_at, `cb75f4f`), `get_article_by_pmid` lit aussi la DuckDB (`acfce9e`), catégories obsolètes → "Autres", traduction vieilles descriptions markdown, filtre catégories obsolètes parser + maj labels.
- [x] **Tower /survey — UX polish** — spinner `dots` pendant génération synthèse IA, header "Vue Jour" harmonisé, script one-shot maj descriptions favoris post-fusion. Pagination 50 par onglet testée puis revert.

### Aima-Tower /exploration — refresh + UX filtres + slider VAF

- [x] **Aima-Tower /exploration — bouton Refresh** — bouton dans le header qui appelle `exploratory_service.reload()` + invalide le cache LRU + toast de confirmation. Évite le `docker compose restart` quand de nouveaux samples arrivent dans trace-prod.
- [x] **Aima-Tower /exploration — défaut Dorado = ge5** — filtre version Dorado par défaut passé de `v5.0.0` strict à `Toutes (≥ 5.0)` (option en première position). Reset filters aligné. Couvre v5.0.0 + v5.2.0 d'office (~270 healthy au lieu de 148).
- [x] **Aima-Tower /exploration — filtres avancés en collapse** — selects (indications, cancer actif, dorado, kit, rebasecalled) déplacés dans un `dbc.Collapse` togglé par bouton "Filtres avancés ▾". Bouton aligné avec Seuils/Cohorte/Reset/Export sur une seule barre du bas.
- [x] **Aima-Tower /exploration — slider VAF_LIMIT** — `VAF_LIMIT` (seuil high/low VAF du tableau stratifié) exposé en slider 0.5–5.0 (défaut 2.0) à côté de Spec/Profondeur. Câblé dans `compute()`, `_compute_stratified()`, callbacks tab/thresholds/reset/permalink/restore_url/download.
- [x] **Aima-Tower /exploration — headers dynamiques tableau stratifié** — colonnes `VAF > X%` / `0 < VAF <= X%` du tableau Sensibilité Stratifiée suivent le slider VAF en temps réel (format `:g`, ex. 2.0 → "2"). `vaf_limit` threadé via `_build_one_side` → `_build_tables_content`.

## 2026-04-16 — trace-prod schema v2 + colonnes avril

- [x] **trace-prod schema v2** — bump `SCHEMA_VERSION` 1→2, migration idempotente `ALTER TABLE bam_metadata ADD COLUMN bam_horaire`. Nouvelles colonnes : `qc_metrics.mvaf_v1_10m/20m`, `retd_suivis.frag_mode1/2`, `bam_metadata.bam_horaire`, `metadata` (+gene1_detailed_variant, active_cancer_clinical, stage, commentaire_global).
- [x] **mVAF raréfiée 10M/20M** — extraction depuis `BETA/{sample}.{depth}.epic.raima_score.V2.tsv` via `BaseChecker.get_mvaf_rarefied()`. Colonnes export "mVAF v1 10M" / "mVAF v1 20M" dans liquid + solid.
- [x] **Frag modes 1/2** — extraction depuis `Fragmentomics/filtered/{sample}.fragmentomics_modes.tsv` (ligne 2, col 1/2). Colonnes export entre IchorCNA et BAM. NA si fichier absent.
- [x] **update-column bam_horaire** — sous-commande dédiée qui met à jour UNIQUEMENT `bam_horaire` (OK/clean/KO) sans toucher nb_bam/taille_bam/bam_completude. Via `aws s3 ls --recursive --profile scw` sur `s3://aima-bam-data/data/{labo}/{type}/{sample}/`.
- [x] **gene1_vaf logic raima (BREAKING)** — `gene1_vaf = max(gene1_freq)` uniquement si `mutation_status == "Tumoral"`, sinon NULL. Avant : toujours rempli depuis freq. Impact : réimport metadata vide certains gene1_vaf.
- [x] **Propagation metadata rebasecalled** — `import-metadata` copie auto depuis sample original vers `{sample}_rebasecalled*` sans metadata. Compteur `{propagated}` en sortie.
- [x] **TSVExtractor NFS-first** — `_read_lines()` priorité NFS (plus rapide), fallback S3. Avant : S3-first.
- [x] **CLI jobs default 12→4** — le 12 saturait S3 pour `check`/`update-column`/`probs`.
- [x] **Cleanup `.claude/` dans trace-prod** — suppression des skills/agents dupliqués du repo trace-prod (gérés dans claude-config).
- [x] **Commit `6ebd388`** — `feat: schema v2 (bam_horaire), mVAF rarefied, frag modes, metadata propagation`.

## 2026-04-16 — Aima-Survey + Aima-Tower : email quotidien + page Survey intégrée

- [x] **Aima-Tower — page Survey intégrée** — nouvelle route `/survey` consommant les rapports markdown Aima-Survey. Vue Jour/Semaine avec onglets rubriques, filtres combinables (recherche + priorité + rubrique + journal + date + état lu/non-lu), synthèse IA par article à la demande (claude-sonnet-4-6), marquage vu/non-vu avec badge navbar, favoris avec notes inline. Bug `TOP_N=10` fixé côté `veille.py` (tous les articles exportés). Commit `91c545d`.
- [x] **Aima-Survey — envoi email quotidien** — `veille.py` refactoré : envoi via email-hub (Redis/BullMQ), contourne le port 587 bloqué Scaleway. Badges date/priorité HTML, dédup par PMID + tri priorité > date. `run_veille.sh` wrapper + `.env` chmod 600 gitignoré. Cron daily 8h00 opérationnel (email envoyé uniquement si ≥1 publication).
- [x] **Aima-Survey — requêtes PubMed enrichies** — 10 requêtes (vs 6) avec filtres `humans[mesh]` sur axes cliniques + `NOT review[Publication Type]` partout + 3 nouveaux axes (fragmentomics, modkit/dorado, 5hmC) + filet haut-impact (Nature/Genome Biology/NAR...).
- [x] **Prendre en main automate veille scientifique** — projet exploré en profondeur (agent-explore), flux cron → PubMed E-utilities → markdown compris, évolutions majeures apportées dans la foulée (cf. entrées ci-dessus).
- [x] **Aima-Tower — page Survey polish & perf** — filtres redesignés (InputGroup avec icônes, persistence session, compact `size="sm"`), lazy-render des onglets (payload Day 170→15 KB soit -91%, Week 278→104 KB soit -62%), `dbc.Collapse` par card remplacé par `html.Div` + toggle `style.display` (mount React plus rapide), UI note retirée (backend préservé). Commit `d1d8486`.
- [x] **Agent de veille enrichi** — `scorer.py` Claude Haiku 4.5 : score 0-10 + why + tags par article dans Aima-Survey, cache SQLite `scoring_cache.db`, rendu via span `score-badge` + bullet `**IA**` dans le markdown. Commit Aima-Survey `85036d0`.
- [x] **Aima-Tower — scoring IA intégré dans /survey** — parser étendu (`score`, `why`), badge `IA X/10` coloré (vert ≥7 / jaune 4-6 / gris <4), ligne justification en italique, slider "Score min" 0-10, tri multi-critères `(priorité, score desc, None en fin, date desc)`, rétrocompatible rapports pré-scoring.
- [x] **Aima-Survey — dédup cross-jours + fenêtre 7j + docs** — table SQLite `sent_articles` qui filtre les PMIDs déjà envoyés (évite le spam quand cron passe à `--days 7`). Cron daily 1j → 7j : rattrape les papiers avec `pdat` indexé en retard (ex: fRagmentomics PMID 41886314 loupé en `--days 1`). README.md créé, CLAUDE.md réécrit (stack + conventions + historique v1→v5), 2 mémoires Claude : `email_sending.md`, `scoring_and_dedup.md`. Commit Aima-Survey `08328ae`.

## 2026-04-15 — Housekeeping projets

- [x] **Renommage projet `veille-scientifique` → `Aima-Survey`** : dossier renommé, 2 lignes crontab mises à jour, skill `/veille` migré (2 refs), CLAUDE.md du projet corrigé.
- [x] **Git push Aima-Survey sur GitHub** : branche renommée `master` → `main`, remote `origin` configuré sur https://github.com/aima-dx/Aima-Survey.git, 2 commits poussés. Aucun secret dans les fichiers trackés (clé NCBI via `NCBI_API_KEY` env var).
- [x] **Todo list restructurée** : ajout d'une Partie 2 "En cours" (entre À faire et Complété). Routing par section sauvé en mémoire Aima-Tower (`feedback_todo_sections.md`).
- [x] **trace-workflow multi-workspace** — ajout workspace `aima-diagnostics` en plus du perso via filtre `ALLOWED_ORGS`. Migration DB idempotente (`workspace_id`), 15 957 workflows existants préservés.
- [x] **Prise en main CLI Seqera** — `seqera ai --headless` (via skill `/seqera`) pour les questions NL, et API REST directe (`/user-info`, `/workflow?workspaceId=`) utilisée par `trace-workflow`.
- [x] **Traduction user manual plateforme** — terminée.

## 2026-04-14 — Aima-Tower : Batches A-F + refonte navigation

Session de développement intensif post-Batches de base. Aima-Tower passe d'un dashboard d'exploration à un **outil ISO 15189 opérationnel**.

### Refonte navigation
- [x] **Navbar recomposée** : `Database | Monitoring | Analytics | Exploration | Qualité | Overview`. Suppression de `/compute` (contenu fondu dans `/monitoring`). Nouvelle page `/qualite` dédiée à la surveillance longitudinale ISO 15189.
- [x] **Ressources système (CPU + Mémoire)** déplacées de `/compute` vers `/monitoring` en carte compacte sous le tableau "Workflows terminés". Front adapté (labels inline, plus de headers de cartes séparées).

### /analytics refondu (Batch A)
- [x] **Suppression "Reads par Tissu"** + ses filtres (sample-type, labo, tissue) et callbacks associés.
- [x] **Tabs IA | Avancé** :
  - **IA** : regroupe "Draw with Aima Analyser" + "Ask to Aima Analyser" (inchangés).
  - **Avancé** : sidebar filtres indépendante (target, depth, dorado, indications, active, rebase) + 4 analyses.
- [x] **Distribution des scores Healthy par kit** : histogramme overlay Apostle / Maxwell / Autre — visualise le batch effect kit (amplificateur EPIC→ONT).
- [x] **Calibration plot** : déciles de score (qcut) vs fraction cancer_truth observée + diagonale référence.
- [x] **Stats comparatives CGFL vs HCL** : Δ Sens_AI, Δ Spec_AI et Fisher exact 2×2 (scipy).
- [x] **Clustering FN/FP** : PCA 2D (sklearn) sur features score+vaf+depth+indication+kit+version — visualise les groupes d'erreurs.

### /qualite nouvelle page (Batch B + D + F)
- [x] **Création page** : navbar, route, factory, layout (filtres gauche + content droite).
- [x] **Drift temporel Sens/Spec** : bucket par fenêtre (semaine/mois/trimestre), seuil global stable, baseline horizontale pointillée, markers ∝ N par fenêtre. `m.date_of_run` ajoutée à la query DuckDB.
- [x] **Snapshots persistants** : `qualite_snapshots.py` (JSONL `/app/data/qualite_snapshots.jsonl`), bouton "Enregistrer snapshot", tableau historique (20 derniers).
- [x] **Alertes dérive** : `check_drift()` compare dernier snapshot à moyenne des 5 précédents, seuil 3 pp. Banner warning en tête de page si alerte.
- [x] **Rapport ISO 15189** : bouton "Rapport ISO 15189" → download HTML imprimable (filtres + tables + figures Plotly via CDN + SHA-256 hash + timestamp). Utilisateur imprime en PDF via Ctrl+P.

### /database nouvel onglet (Batch F)
- [x] **Onglet "Détails ML"** : tableau sample-level avec sort/filter/pagination natifs (dash_table). Colonnes Sample/Centre/Indication/Label/Score/Seuil/AI/VAF/Depth/Kit/Dorado. Code couleur vert/rouge/jaune pour TP/FN/FP.

### /exploration améliorations (Batch C)
- [x] **depth_sweep vectorisé** : une passe numpy au lieu de 38 computes pandas. **~10× plus rapide** (2-3s → 200ms).
- [x] **Correction date parsing** : `pd.to_datetime(dayfirst=True)` pour les dates FR `%d/%m/%Y`.
- [x] **Presets nommés** (essai → retrait) : créés puis supprimés à la demande (redondant avec le permalien URL). Suppression du module `bookmarks.py`, menu dropdown, modal, 4 callbacks.

### Qualité (Batch D)
- [x] **11 snapshot tests pytest** dans `tests/test_exploratory_compute.py` — **11/11 PASS**. Couvre la régression R (Phase 1b), le default v5.0.0 strict, la stabilité des filtres, le quantile seuil.
- [x] **scipy + scikit-learn** ajoutés à `requirements.txt` + Docker rebuild.

### Fix UI post-session
- [x] **Drift plot ne rendait pas** : 2 bugs — `alert_banner = None` injecté comme children + `Input("qualite-snapshot-save-feedback")` référencé depuis l'intérieur du callback Output (circular). Hoist feedback div hors de qualite-content, filtrage des None children.

### Commits (8)
- `99a86da` slider dynamique + plots (phase 1+2+3)
- `50eb016` cohort filters (indication, active, depth)
- `cac96f4` Dorado version, kit, rebasecalled filters
- `050c915` cohort counts match R + dual bars
- `4bf1c90` Batch 1-3 UX + depth sweep + VAF bin + info modal
- `828c72b` comparison mode A|B (reverté)
- `09dfd93` A|B → onglet Confrontation dédié
- `b7044cc` Batch A+B (analytics refactor + /qualite création)
- `050c915` (fix cohort counts)
- `4bf1c90` UX + depth sweep + VAF
- Batch C+D+E+F (perf, snapshots, bookmarks, exports, ML tab)
- `260ec61` remove presets + fold Compute into Monitoring + fix drift freq
- `2d5fb78` fix drift plot render (hoist feedback, strip None children)

## 2026-04-14 — Aima-Tower exploratory-analysis : UX complète + 4e onglet Confrontation

Session de livraisons successives post-phase-3, page `/exploration` refondue :

### Filtres & interactivité (priorité 2)
- [x] **Filtres cohorte** : multi-select indications (default = toutes), select cancer actif (Tous/Actif/Non actif), slider depth (0.10–2.00, défaut 0.25). Healthy toujours conservés pour calibrage seuil. Commit `50eb016`.
- [x] **Filtres avancés** : version Dorado (défaut v5.0.0 strict, option v5.2.0, option "Toutes ≥5.0" = R), kit extraction (Apostle/Maxwell/Autre, normalisé depuis `extraction_protocol`), rebasecalled (Inclure/Exclure/Uniquement). Commit `cac96f4`.
- [x] **Dédup par version** : préparation paramétrée par `version_mode`, original préféré + rebasecallé en fallback. Cache prep keyé par `(centre, analysis_type, version_mode)`.
- [x] **Counts cohorte alignés sur R** : `_compute_cohort_counts` retire seulement rep/moche/bis/ter/quater (garde TNE/Nuclear/Bladder_Blood), 48/48 lignes identiques aux CSV R à 0.85 mode ge5. Commit `050c915`.

### Graphiques (priorité 3)
- [x] **Distribution scores** : overlay healthy vs cancer + ligne verticale seuil.
- [x] **ROC curve** : TPR vs FPR à tous seuils + marker ambre mobile au seuil courant + AUC dans le titre.
- [x] **Forest plot** : sens par indication avec CI 95% Wilson.
- [x] **Depth sweep** : courbe Sens/Spec vs depth_min (0.10–2.00).
- [x] **VAF bin plot** : Sens_AI par bin VAF (0-0.5 / 0.5-1 / 1-2 / 2-5 / 5-10 / ≥10% / Non-muté).
- [x] **Cohort bar plot dual** : barres grises background (total depth=0) + barres bleues foreground (depth filtré), label `N_filtré / N_total` au-dessus.

### UX & ergonomie (Batches 1-2)
- [x] **Sous-onglets Tableaux / Graphiques** (persistence session, pills styled) dans chaque onglet centre.
- [x] **Badges sens/spec** : dégradé HSL rouge→jaune→vert (30%→100%), saturation 80%.
- [x] **CI Wilson 95% inline** : format `81.2% [76.3–85.4] (242/298)` sur tous les badges (validation R inchangée, computed en display layer).
- [x] **Reset button** : remet tous les filtres aux défauts en un clic.
- [x] **Indicateur cohorte live** : "Cohorte ALL : 298 cancer + 140 healthy" mis à jour avec filtres. Warning "seuil instable" si healthy < 20.
- [x] **Modal info "Comment ça marche ?"** : doc détaillée pipeline R→Python (étapes 01/02/03, filtres analytiques vs cohort counts, normalisation kit, CI Wilson, validation R).
- [x] **Export CSV par table** : dropdown menu avec les 14 clés exportables (détection, par indication, stratifié, misclassified, counts). Filtres courants intégrés au nom du fichier.
- [x] **Permalien** : dcc.Clipboard copie l'URL `/exploration?target=0.90&kit=Apostle&...`. Restore depuis URL query string au chargement.
- [x] **Plotly modeBar** : réactivé au hover, export PNG 2×, logo plotly retiré.
- [x] **Slider compact** : handle plus petit, marks 0.7rem, track réduit, focus avec halo bleu.
- [x] **Colonne Depth ajoutée** aux tableaux misclassified FN/FP.

### 4e onglet Confrontation
- [x] **Mode comparaison A|B dédoublement de la carte filtres** : tentative abandonnée (surcharge UI). Remplacé par onglet dédié.
- [x] **4e onglet "Confrontation CGFL vs HCL"** : affiche CGFL (header vert) et HCL (header violet) côte à côte avec les filtres principaux partagés. UI propre, pas de doublon de contrôles. Commit en cours.

### Commits
- `99a86da` feat(exploration): slider dynamique + plots (phase 1+2+3)
- `50eb016` feat(exploration): cohort filters (indication, active, depth)
- `cac96f4` feat(exploration): Dorado version, kit, rebasecalled filters
- `050c915` fix(exploration): cohort counts match R + dual bars
- `4bf1c90` feat(exploration): Batch 1-3 UX + depth sweep + VAF bin + info modal
- `828c72b` feat(exploration): comparison mode A|B toggle (reverté ensuite)

## 2026-04-14 — Aima-Tower exploratory-analysis (recalcul dynamique, 5 phases)

- [x] **Phase 1a — ExploratoryAnalysisService Python** : `src/exploratory_compute.py` créé, réimplémente `run_pipeline.R` + `functions_prepare_data.R` en pandas/numpy. Charge trace-prod DuckDB, prépare datasets (filter v≥5.0, depth≥0.25, dedup unique_id), threshold via `np.quantile method='weibull'` (= R `type=6`), expose `compute(target_specificity)` avec cache LRU.
- [x] **Phase 1b — Validation croisée Python vs R** : **28/28 tests PASS** (14 tableaux × 2 targets 0.85 + 0.90). Outputs identiques aux CSV R (`figures_and_tables_085_new/` et `figures_and_tables_090_new/`). Key learning : R `type=6` = numpy `method='weibull'` (pas `'hazen'`).
- [x] **Phase 2a — UI slider** : `_threshold_slider_card()` (0.80–0.99, step 0.01, default 0.85) ajouté au-dessus des tabs dans `exploration_page()`. Persistence session.
- [x] **Phase 2b — Callback dynamique** : `update_exploration_tab` modifié pour prendre `exploration-target-slider` en Input → recalcule tab content. Nouveau callback `update_exploration_thresholds` affiche target% + seuils ALL/CGFL/HCL live. `_build_exploration_content(centre, target_spec=0.85)` utilise `exploratory_service.compute()` via mapping `_CENTRE_KEYS`.
- [x] **Phase 3 — Cleanup** : suppression `ExplorationService` CSV-based + `_CSV_MAP` + `exploration_service` dans services.py, `exploration_csv_path` dans config.py, volume `/exploratory-analysis` dans docker-compose.yml, import dans pages.py. Rebuild Docker OK, 1033 samples chargés depuis trace-prod.
- [x] **Checkpoint git** : branche `backup-pre-exploratory` (commit `8df0502`) créée pour rollback.

## 2026-04-14 — Investigation batch effect CGFL vs HCL

- [x] **Investigation systématique batch effect CGFL vs HCL** — exploration de 12 pistes via trace-prod + exploratory-analysis + lecture BAM/bedMethyl :
  - composition biologique (Cat 1/2/3/4, VAF panel)
  - kit barcoding (NBD114-96 vs NBD114-24) — confounded
  - kit extraction (Apostle vs Maxwell) — confounded, Maxwell n'a PAS plus de gDNA long (hypothèse inverse)
  - version Dorado / GPU — pas significatif en v5.0.0
  - couverture — FP stables à toutes profondeurs
  - taille des fragments — CGFL a en fait des reads plus longs (mean 260bp vs 222bp)
  - fragmentomics mode1 — artefact des rebasecallés, pas un batch effect
  - modkit auto-threshold — déjà testé, ne change rien
  - score CNV — batch effect confirmé (matrice 100% CGFL dans raima)
  - ichorCNA — OK, corrèle avec charge tumorale
  - déconvolution Loyfer — distributions proches
  - profil cfDNA FP HCL — signal tissulaire subtil (moins de blood_0)
  - Voir `~/.claude/projects/-home-blipinski-Pipeline-Bam2Beta/memory/batch-effect-investigation.md`
- [x] **Création projet `~/Pipeline/ComBat-Met/`** — CLAUDE.md, .claude/rules, Docker (R 4.4 + ComBatMet 0.99.3), 9 scripts R/bash pour extraction, correction, scoring parallèle.
- [x] **Test ComBat-met** — 4 variantes testées (group=H/C, rebalancé, ref.batch=CGFL, Healthy only). **Aucune ne fonctionne**. Finding inattendu : la simplification du bedMethyl seule réduit 17% → 3% FP HCL sans ComBat-met.
- [x] **Identification des 2 batch effects racines** :
  1. **EPIC → ONT** (majeur) : raima V1 entraîné sur 19 EPIC bisulfite microarrays, appliqué à ONT → biais technologique jamais corrigé
  2. **Apostle vs Maxwell** (amplificateur) : kits d'extraction ADN cfDNA avec chimies différentes (Apostle = nanoparticules propriétaires, Maxwell = billes magnétiques Promega) → biais de capture CpG différent ; Apostle produit des profils ONT plus proches des refs EPIC **par hasard** → explique les 2% FP CGFL vs 17% HCL
  - Les 2 effets sont liés : le kit crée une composante de biais ONT qui interagit avec le biais EPIC. Confounded avec centre (pas de Maxwell CGFL, pas d'Apostle HCL).
- [x] **Conclusion ComBat-met** : **non retenu pour la production**. Documenté dans `~/Pipeline/ComBat-Met/README.md`. Dépendance batch-spécifique incompatible ISO 15189 + simplification technique suffit pour 80% du problème.
- [x] **Mise à jour mémoire Claude** : `batch-effect-investigation.md` + pointeur dans MEMORY.md Bam2Beta.
- [x] **Restructuration todo list** : séparation tâches à faire (par priorité) / tâches complétées (par jour).
- [x] **Skill `/audit-trail`** — créé, traçabilité ISO 15189 (changelog + diff + hashes containers + non-régression) pour les versions Bam2Beta/Pod2Bam.
- [x] **Skills analyse scientifique** — `/compare-batches` (Wilcoxon/Fisher + confounders), `/qc-report` (rapport standardisé avec seuils), `/correlation` (Spearman + paradoxe de Simpson) créés et pushés sur claude-config.
- [x] **Centralisation doc effet batch** — tout regroupé dans `~/Pipeline/batch_effect/` : README central (12 pistes + 2 batch effects racines + ComBat-met), CLAUDE.md workflow de reprise, `ComBat-Met/` déplacé en sous-dossier, mémoire Claude `batch-effect-investigation.md` mise à jour.

## 2026-04-13 — Rétrospective et setup Claude Code

- [x] **Nettoyage config Claude** — skills, plugins, agents dupliqués supprimés.
- [x] **Golden rules globales** — s3-safety, duckdb, nextflow, secrets dans `~/.claude/rules/`.
- [x] **CLAUDE.md global** — profil Boris (bioinfo AIMA, bus factor 1) réécrit.
- [x] **MCP installés** — pubmed, duckdb, memory, ensembl, ncbi, s3.
- [x] **Hooks** — protection S3, notification.
- [x] **Veille scientifique automatisée** — cron + skill `/veille`.
- [x] **Skill `/export-gsheet`** pour trace-prod.
- [x] **Profil utilisateur complet** — technique + scientifique dans `~/.claude/projects/-home-blipinski/memory/`.
- [x] **Skills bioinformatiques v1** — `/sample`, `/debug-nf`, `/check-consistency`, `/batch-effect`.
- [x] **Références techniques** — bedMethyl, troubleshooting, stats-guide, dorado-reference.md.
- [x] **Contexte pipeline AIMA** dans 7 CLAUDE.md projets.
- [x] **Instructions compaction intelligente** — garder fichiers modifiés, commandes testées, décisions, état runs NF, bugs.
- [x] **Aliases et template CLAUDE.md** standardisés.
- [x] **Agent explore bioinfo** avec détection automatique Phase 6.

---

# Partie 4 — En stand-by

Tâches identifiées mais bloquées (dépendance externe, info manquante, décision en attente). Ne pas mélanger avec "basse priorité" — ici c'est **bloqué**, pas juste **pas prioritaire**.

Format : `- [ ] **Titre** — raison du blocage. **Débloquer quand :** condition concrète.`

---

**Why:** Issue de la rétrospective complète Claude Code du 13/04/2026 + investigation batch effect du 14/04/2026. Format 4-parties : à faire (Partie 1) / en cours (Partie 2) / complété (Partie 3) / en stand-by (Partie 4).
**How to apply:** Consulter la Partie 1 en début de session. Déplacer une tâche en Partie 2 quand elle démarre activement. Ajouter en tête de Partie 3 à chaque fin de session avec la date. Utiliser Partie 4 pour les tâches bloquées qu'on ne veut pas perdre mais qu'on ne peut pas avancer.

**Routing des requêtes utilisateur :**
- "qu'est-ce qui est à faire" / "todo" / "à faire" → Partie 1
- "qu'est-ce qui est en cours" / "en cours" → Partie 2
- "qu'est-ce qui est fait" / "complété" / "historique" → Partie 3
- "qu'est-ce qui est en stand-by" / "bloqué" → Partie 4
- "montre la todo list" (sans précision) → Partie 1 + 2 (actif uniquement)
