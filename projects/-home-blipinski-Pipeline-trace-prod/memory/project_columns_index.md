---
name: columns-index
description: "Index des colonnes ajoutées en v2-v7 dans trace-prod (retd_suivis, qc_metrics, bam_metadata). Détails techniques dans README.md et topic files dédiés."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5d22bc11-28bd-47de-a329-672d09636c7c
---

# Colonnes ajoutées v2-v7 — index

Référence rapide. Détails complets dans `~/Pipeline/trace-prod/README.md` (Tables 2/3/4) et `~/Pipeline/trace-prod/CLAUDE.md`.

## Schema v2 (avril 2026)
- `qc_metrics.mvaf_v1_10m`, `qc_metrics.mvaf_v1_20m` DECIMAL(10,4) — mVAF raréfiée 10M/20M reads
- `retd_suivis.frag_mode1`, `frag_mode2` VARCHAR DEFAULT 'NA' (PAS dans STATUS_COLUMNS) — Fragmentomics modes
- `bam_metadata.bam_horaire` VARCHAR DEFAULT 'KO' — présence BAM raw horaires S3 (pattern preserve)
- `metadata.{gene1_detailed_variant,active_cancer_clinical,stage,commentaire_global}` — colonnes gsheet additionnelles

## Schema v3-v5 (avril-mai 2026, metadata gsheet)
- v3 : `metadata.grade` — source "Grade" gsheet CGFL VAF (HCL NULL)
- v4 : `metadata.speedvac` — `SpeedVac` (CGFL) + `SpeedVAc` (HCL), harmonisé `Yes/No`
- v4 (fix) : `"Stage" → stage` ajouté (CGFL stage était 100% NULL avant)
- v5 : `metadata.cohort` — `Cohorte` (col 48 des 2 gsheets). Valeurs : Validation tech, AlCapone, Bladder, Brenus, MSD, Lung-DI précoce. `HARMONIZATION_RULES["cohort"]` défensif

## Schema v6 (mai 2026, IV/QC)
4 colonnes `retd_suivis` (toutes VARCHAR libre, PAS dans STATUS_COLUMNS) :
- `read_start_time` DEFAULT 'KO' — présence `QC/Samtools/{sample}.read_start_time.tsv` (3-4 GB, pas de lecture)
- `ancestry` DEFAULT 'NA' — argmax sur `IV/{sample}.ancestry.tsv` (18 ancestries)
- `sex_proba` DEFAULT 'NA' — proba arrondie au millième
- `sex_predicted` DEFAULT 'NA' — F si p<0.5, M si p≥0.5

Path IV/ : **sœur de QC/, pas dedans**. Voir [[schema-v6-iv-qc]].

## Schema v7 (mai 2026, short_read)
- `retd_suivis.short_read` VARCHAR DEFAULT 'KO' — subsampling short-read (75-200 bp)
- Listing récursif `aws s3 ls --recursive` sur bucket mirror `{LABO}_short_read`
- 6 dossiers requis (BAM, BETA, CNV, QC, REPORT, ichorCNA) chacun non vide
- Pattern preserve (None → skip UPDATE), `_update_short_read()` dédié
- **Gotcha critique** : `aws s3 ls --recursive` retourne clés S3 COMPLÈTES, stripper avec `sample_prefix`. Voir [[schema-v7-short-read]].

## Patterns transversaux

**Collision mapping TSV_TO_DB_METADATA** (`upsert_metadata`, avril 2026)
- Plusieurs `tsv_col` peuvent pointer vers le même `db_col` (variantes casse/long/court entre labos)
- Fix : `if new is not None or db_col not in data: data[db_col] = new` — préserve la 1re valeur non-None
- Sans ce fix, ajouter un mapping casse silencieusement les imports précédents (ex : ajout `"Stage": "stage"` cassait HCL stage existant 185 → 0)

**gene1_vaf Raima Logic** (avril 2026, BREAKING)
- `gene1_vaf = max(gene1_freq.split(" / "))` **uniquement si `gene1_mutation_status == "Tumoral"`**, sinon NULL
- Raison : les freq Non-tumoral/Unknown ne doivent pas alimenter la VAF raima
- Impact : réimporter peut vider des gene1_vaf précédemment remplis

**Metadata Rebasecalled Propagation** (avril 2026)
- `import-metadata` re-propage TOUTES les variantes `{sample}_rebasecalled*` à chaque exécution (pas seulement celles sans metadata)
- 113 CGFL + 71 HCL = 184 rebasecalled re-propagés à chaque import
- Lookup fallback : si "Old sample name" échoue, retente avec "Sample name" (cas `*bis`)
- Exception : POD5 storage NE PAS propager — laisser NULL côté rebasecalled. Voir [[feedback-rebasecalled-pod5]]

**NFS-First Priority** (avril 2026, BREAKING)
- `TSVExtractor._read_lines()` lit NFS d'abord, S3 en fallback (avant : S3 d'abord)
- Raison : NFS plus rapide que S3 pour petits TSV quand mount dispo
- `_s3_read_text()` reste utilisé ailleurs (checkers `check_ichorcna`, `check_mvaf_v12`) avec priorité S3

**BAM Completude Fallback via bam_list.txt** (mars 2026)
- Quand `_update_bam_sizes()` ne trouve pas de BAM sur S3, lit `{sample}_bam_list.txt`
- Affecte les Bladder_Blood (BAM raw plus sur S3, seuls les txt restent)
- Calcule count + max_index pour reconstituer la complétude

**Export ONT Sample** (avril 2026)
- Commande `export-ont-samples` : DuckDB.metadata fusionnée (CGFL+HCL liquid) → onglet 'ONT Sample'
- Méthode : `DuckDBService.get_metadata_unified(exclude_rebasecalled=True)` + `GSheetsService.export_ont_samples()`
- 51 cols (3 tech + 44 metadata dédupliquées + 2 calculées)
- Dédup TSV_TO_DB_METADATA : garde la 1re entrée par `db_col` (gère collisions `"SpeedVac"/"SpeedVAc"`)
- Coverage : 687 lignes (357 CGFL + 330 HCL)
