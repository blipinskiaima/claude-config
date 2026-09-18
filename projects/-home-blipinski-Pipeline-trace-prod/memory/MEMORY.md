# trace-prod Memory

Index. Le détail vit dans les topic files — les ouvrir avant d'agir sur le sujet.

## Feedback / règles de travail
- [Réponses courtes](feedback_reponses_courtes.md) — 1-3 phrases, pas de récap final, pas de proposition non sollicitée
- [Scratch workspace + BAM read-only](feedback_scratch_workspace.md) — analyses ad-hoc dans `/scratch/boris/<topic>/`, source BAM/POD5 en lecture seule
- [Rebasecalled POD5 — ne pas propager](feedback_rebasecalled_pod5.md) — laisser NULL après `update-column stockage_pod5`
- [STATUS_COLUMNS = OK/KO/WARNING strict](feedback_status_columns.md) — une VARCHAR libre y passerait en KO via `_parse_status()`
- [Probs loyfer manquantes](feedback_probs_loyfer_lag.md) — loyfer NULL + epic OK = décalage d'extraction, pas un bug. Fix `probs -P` ; `-s` est mono-sample

## Colonnes & schemas (retd_suivis / qc_metrics / qc)
- [Colonnes v2-v7 — index](project_columns_index.md) — + patterns transversaux (collision `TSV_TO_DB`, gene1_vaf raima, propagation rebasecalled, NFS-first)
- [v6 — IV/QC](project_schema_v6_iv_qc.md) — ancestry, sex_proba/predicted, read_start_time. ⚠ `IV/` est sœur de `QC/`
- [v7 — short_read](project_schema_v7_short_read.md) — 6 dossiers du miroir S3. ⚠ `s3 ls --recursive` rend les clés **complètes**
- [v10 — frag softclipped](project_schema_v10_frag_sc.md) — calque exact du frag v1. Quirk NA vs KO selon `check` / `update-column`
- [v11 — mvaf_v13 + frag_score_v2_sc](project_schema_v11_mvaf_v13_frag_score.md) — liquid only
- [v12 — bootstrap](project_schema_v12_bootstrap.md) — présence S3 via `_s3_exists`, pattern preserve
- [v13 — mvaf_v14](project_schema_v13_mvaf_v14.md) — ⚠ `cols[1]` (V1.4 a 3 colonnes) + `format_mvaf4()` : jamais de notation scientifique
- [v14 — bootstrap_props](project_schema_v14_bootstrap_props.md) — calque exact de v12
- [v18 — themelio_score](project_schema_v18_themelio.md) — ⚠ chemin réel `THEMELIO/`, pas `OUTPUT/THEMELIO/`
- [v19 — TOO](project_schema_v19_too.md) — ⚠ module `csv` OBLIGATOIRE : virgule interne dans `confidence_stratum`
- [v20 — 5 métriques mito](project_schema_v20_mito.md) — `split("\t")`, arrondi 2 déc. à l'export via `ROUND2_HEADERS`. ⚠ homonyme `Colon_1` CGFL≠HCL
- [v21 — n50](project_schema_v21_n50.md) — lu **par nom d'en-tête**. Reste la référence du **solid** (le liquid a basculé en v24). ⚠ `QC/Cramino/` à plat, jamais de glob
- [v22 — n75 + ratio](project_schema_v22_n75_ratio.md) — ⚠ `n75` mappé en écriture mais **jamais exporté**. ⚠ `NaN`/`inf` ne lèvent pas `ValueError` : valider les 2 opérandes, pas le résultat
- [v24 — bascule liquid + pct_mass_removed](project_schema_v24_pct_mass_removed.md) — le liquid lit `n50_ratio.tsv` (bloc `*_filtered`) via override `LiquidChecker` ⚠ **N50 a 2 définitions selon l'onglet**
- [v25 — qc.reads_with_cpg + 28M](project_schema_v25_qc_28m_cpg.md) — table `qc` (≠ `qc_metrics`), backfill TSV ponctuel, **pas de checker permanent**
- [v26 — mvaf_v15](project_schema_v26_mvaf_v15.md) — ⚠ **s'ajoute** à v1.4, ne la remplace pas. ⚠ relecture gsheet = faux écarts (nombre vs chaîne à virgule)
- [v27 — short_read → small_fragments](project_schema_v27_small_fragments.md) — ⚠ **pré-migration AVANT les `CREATE TABLE`**. `ALTER RENAME` préserve PK/FK. ⚠ onglet `'Small Fragments'`
- [v29 — frag_amplitude_sc](project_schema_v29_frag_amplitude_sc.md) — ⚠ `_LIQUID_QC` et `_SOLID_QC` textuellement identiques autour de `Sex Predicted` : élargir le contexte de l'Edit
- [v30/v31 — sequencing_time + multi_run](project_schema_v30_v31_sequencing_time.md) — ⚠⚠ le fichier suit l'ordre du BAM, et **le max n'est pas échantillonnable** : scan intégral obligatoire. 2 colonnes d'UN balayage
- [v34 — statuts QC Exis/Thémélio](project_schema_v34_qc_status.md) — 4 colonnes lues dans `metadata.json`, preserve si JSON absent/ancien
- [v35 — QC post-filtre 80 < L < 1 kb](project_schema_v35_qc_80_1000.md) — import one-shot, aucun checker. ⚠ 16 flux = optimum, 32 s'effondre

## Tables autonomes (lots hors `samples`)
- [v9 — dilution](project_schema_v9_dilution.md) — PK `sample_name`, pas de FK, préfixe `.merged` → BaseChecker sans override
- [v16/v17 — rarefaction](project_schema_v16_rarefaction.md) — PK composite depuis v17 (collision inter-labo). ⚠ un lot en production n'a que **5 des 10** sous-dossiers → PROD=KO et `nb_lignes_total` = **`0,00`, pas NA**
- [v28 — rarefaction_horaire](project_schema_v28_rarefaction_horaire.md) — PK composite dès le DDL. ⚠⚠ **Loyfer non bootstrapable** (epic = moyenne des 200, Loyfer = valeur unique). ⚠ `LOG/` à exclure
- [v32 — rarefaction_horaire_threshold](project_schema_v32_rarefaction_horaire_threshold.md) — 1620 lignes. ⚠⚠ **un BAM re-sous-échantillonné rend son aval périmé et trace-prod ne peut pas le détecter** (le cas dangereux est celui sans aucun `NA`) ; comparer les dates S3 `BAM/` vs `BOOTSTRAP/`
- [v33 + v36 — dilution_lung](project_schema_v33_dilution_lung.md) — ⚠ calquer sur **threshold**, pas sur `dilution` : lister le dossier avant de choisir le modèle. ⚠ `aws s3 ls` matche par préfixe (un `.bai` orphelin = faux SKIP)
- [v8 — small_fragments_metrics](project_schema_v8_short_read_metrics.md) — FK `sample_id`, CLI indépendante

## Exports
- [Export Cohort](project_cohort_export.md) — onglets `Exis *` par indication, prédicats **importés** d'Aima-Tower. ⚠ motifs indépendants ≠ cascade : le **premier** motif donne le palier de chute
- [Export run](project_export_run.md) — une ligne par run. ⚠ `reads_per_flowcell` sommait les rebasecallés (corrigé 08/09). ⚠ `sequencing_time` est une donnée de **barcode**, pas de run
- [Retraits d'export + fallback Indication](project_export_retraits_et_fallback_indication.md) — masquer = retirer de `_LIQUID_QC` **en gardant le mapping**. ⚠ `clear()` sans `resize()` laisse une colonne fantôme
- [Renommage étiquettes](project_rename_labels_nb_lignes_molecule.md) — 4 endroits dont les dicts des checkers. ⚠ raima et exploratory-analysis lisent l'export **par en-tête**
- [Renommage colonnes DuckDB](project_rename_nb_lignes_molecule_cols.md) — ⚠⚠ un sed global réécrit **l'intérieur de la migration** → no-op silencieux
- [Mode probs --probs_bootstrap](project_probs_bootstrap_mode.md) — epic = moyenne des 200 réplicats, réversible

## Rétrospectif / pipeline
- [Rattrapage QC + TSV plateforme](project_qc_status_retro_backfill.md) — ⚠⚠ **`--RETRO_REPORT` écrit DEUX fichiers** : le TSV *et* `metadata.json` réécrit, qui y perd `version_raima`. Lire le `publishDir` de **chaque** process avant un retro sur du client. Flag `RETRO_QC_ONLY`. ⚠ jamais `-profile liquid`. **Méthode : snapshot S3 → 1 sample → diff exigeant 0 ligne `<` → le lot**

## Données & analyses
- [Infra POD5/BAM/export](reference_infra_pod5_bam_export.md) — barcode, POD5 storage, S3 AWS/SCW, BETA_28M, IchorCNA, gsheet config, CLI defaults
- [Frag softclip vs trim barcode](project_frag_softclip_trim.md) — **seul `frag_mode_sc` est fiable** en cross-cohorte (~81 samples faussés)
- [Samples Twist](project_twist_samples.md) — titration CGFL. `_rep_N` = réplicats **inter-run** : mVAF stable, seuls les classifieurs divergent
- [Audit active_cancer](project_active_cancer_audit.md) — ⚠⚠ `active_cancer_clinical` est une colonne **morte** ; la vraie est `active_cancer`. ⚠ écart `Lung_13*` **non verrouillé**
- [Pièges de requêtage](project_pieges_requetes_homonymes.md) — `sample_name` n'est **pas unique** entre labos ; sains et tumoraux ne partagent jamais un run
- [Analyse pore scan MinKNOW](project_pore_scan_analyse.md) — le nb de pores est dans les **logs** du HTML. La réserve = les pores **totaux**. Aucune différence CGFL/HCL
- [HCL Verification](project_hcl_verification.md) — 275 samples, transfert raw→S3 intègre, raw purgé 12/03/2026
- [Script pod5_verification](reference_pod5_verification.md) — génération de `pod5_verification.tsv`

## Architecture
- CLI : `database/check_samples.py` (Click) — Core : `lib/checkers.py`, `lib/duckdb.py`, `lib/utils.py`, `lib/extractors.py`
- S3 fallback : `lib/s3_fallback.py` — `SmartPath` hérite de `Path`, download S3 transparent
- DB : `database/samples_status.duckdb`. Schéma = source unique `DuckDBService.SCHEMA`
- Checkers dédiés : `checkers_small_fragments.py` (override 4 méthodes, préfixe `minLen75`), `checkers_dilution.py` / `checkers_rarefaction.py` (BaseChecker sans override, préfixe `.merged`)

## Key Mappings (lib/)
- `COLUMN_MAPPING` : display → DB. `NUMERIC_COLUMNS` : cast DECIMAL. `STATUS_COLUMNS` : OK/KO/WARNING **strict**
- `LIQUID_HEADERS` / `SOLID_HEADERS` (utils.py) : ordre d'export. `_BAM_COLS` : ordre export BAM
- `COLUMN_CHECKERS` (check_samples.py) : colonne → checker pour `update-column` (+ variantes `DILUTION_` / `RAREFACTION_`)

## DuckDB Gotchas
- **`CREATE TABLE AS SELECT` perd les PK/FK** → DDL original + `INSERT INTO ... SELECT`. (`ALTER ... RENAME` les préserve, lui)
- UPSERT = blocs morts → `clean-database`. ⚠ ajouter toute nouvelle table à `compact()`
- **Single writer lock** → `check` / `update-column` séquentiels, jamais en parallèle. Même en `read_only`, la lecture attend
- Conversion euro : virgule→point + KO/NA→NULL avant insert

## Conventions
- Combos valides : liquid×(CGFL|HCL), solid×CGFL. Solid×HCL invalide
- Statuts : OK, KO, WARNING (+ RUNNING pour `prod_status`). Format euro : virgule décimale, DD-MM-YYYY
- Manquant : `NA` en export, NULL en DB. Table `samples` : colonne `sample_type` (pas `type`)

Détails par colonne : `~/Pipeline/trace-prod/README.md` (Tables 2/3/4) et `CLAUDE.md`.
