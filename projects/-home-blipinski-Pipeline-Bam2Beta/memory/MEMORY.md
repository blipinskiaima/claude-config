# Bam2Beta Project Memory

## Key Facts

- Current version: **V1.3.1** (tag 2026-05-27, ajout metadata.json natif dans Raima_report)
- Container: `blipinskiaima/bam2beta:latest` + `blipinskiaima/raima:latest`
- Raima package version: **0.4.17** dans raima:latest depuis rebuild 2026-05-27 (avant: 0.4.13 par accident de build du 2026-05-09)
  - Retrocompatibilite 0.4.13 -> 0.4.17 confirmee bit-a-bit sur Healthy_826 CGFL liquid (test 2026-05-27 vs V1.1.2)
  - Image `raima:0.4.17` (tag dedie) existait deja depuis 2026-05-07 mais `raima:latest` etait reste sur 0.4.13
  - Gotcha : verifier la version effective avec `docker run --rm raima:latest R -e 'packageVersion("raima")'` apres tout bump
- Pipeline modules: MERGE, BETA (EPIC), BETA_28M (Loyfer), FRAG, CNV, ICHORCNA, IV, QC (SCORE block removed 2026-05-26)
- Prod profile enables: MERGE + BETA + FRAG + CNV + IV
- Retry strategy: doublement CPU/RAM par tentative, max 10, plafond cpus_max/memory_max

## Verified Findings

- **GRCh38 vs hg38**: resultats strictement identiques sur Healthy_826 (2026-02-20)
  - Les deux FASTA utilisent la convention `chr` prefix
  - GRCh38 "no alt analysis set" = pas de contigs alt/random
  - Scores raima, CNV, fragmentomics, QC metrics: tous identiques
  - See [test-results.md](test-results.md) for details

- **BAM merge verification** (2026-03-13): le merge (samtools cat + sort) ne perd aucune donnee ni metadonnee
  - 3/3 PASS : Breast_1 (CGFL liquid, 44 BAM), Nuclear_4 (HCL liquid, 433 BAM), Colon_0001N8M (CGFL solid, 129 BAM)
  - Reads : Δ=0 flagstat sur toutes les metriques. Metadonnees : 0 @RG/@PG absent, @SQ identiques
  - Headers intra-horaires : 44/44 identiques (verification exhaustive Breast_1)
  - BAM horaires 100% redondants avec le merge
  - See [bam-merge-verification.md](bam-merge-verification.md) for details

- **Volumetrie S3** (2026-03-13): quantification complete des buckets
  - BAM horaires : 30.67 To (supprimables). BAM merges : 18.62 To. RetD complet : 24.86 To
  - POD5 SCW : 75.12 To. POD5 AWS : 66.76 To. Doublons : 11.81 To
  - Total stockage S3 : ~186 To. Economies possibles : ~42.5 To (BAM horaires + doublons POD5)
  - See [s3-volumetry.md](s3-volumetry.md) for details

- [Batch effect investigation](batch-effect-investigation.md) — Investigation complète CGFL vs HCL : 17% FP Healthy HCL (V1), CNV biaisé, pas d'effet taille fragments
- [Soft clipping & longueur FRAG](softclip-fragmentomics-length.md) — FRAG = length(SEQ), soft clips inclus ; vérifié Lung_115/95, ne pas migrer vers span réf

## Debugging Insights

- **raima 0.4.5 casse Raima_process_CNV** : `depth_per_region` n'est pas exportee dans 0.4.5. Fix: utiliser raima 0.4.3 dans le Dockerfile.
- **Container raima:latest doit etre rebuild** apres modification du Dockerfile — sinon Docker utilise l'ancienne image cachee.
- Le test GRCh38 a fonctionne avec l'ancien cache Docker (raima 0.3.2 dans le container) car `Raima_process_CNV` n'appelle pas `depth_per_region` dans cette version.

## Architecture Notes

- `main.nf` orchestre les modules via conditionals (`params.BETA`, `params.FRAG`, etc.)
- Channels: BAM_METADATA fournit [sample_id, bam, bai] a tous les modules
- BED files en `/scratch/dependencies/bed/` ciblent chr1-22+X+Y uniquement
- CNV utilise des bins de 100kb avec filtres de longueur de reads configurable
- Le champ `mVAF` a ete renomme `TF` (tumor fraction) dans commit 7837cd0
- `raima_score_loyfer.R` : `max_read_len` conditionnel (solid=Inf, liquid=1000) via `--type` param
- `params.cpu`/`params.memory` remplaces par `params.cpus_max`/`params.memory_max` en V1.0.1

## User Preferences

- Langue de communication: francais
- Utilise skills Claude Code (test_bam2beta, save-code, etc.)
- Prefere les reponses concises avec tableaux de comparaison
- Travaille depuis ~/Run ou ~/Run2 pour les runs Nextflow

## ichorCNA Module (2026-03-20)

- Container: `blipinskiaima/ichorcna:latest` (R + hmmcopy readCounter + ichorCNA + BSgenome.Hsapiens.UCSC.hg38)
- Workflow: `workflow/ichorCNA.nf` — 2 processus (readCounter → runIchorCNA)
- Scripts: `bin/ichorCNA/` (run_readCounter.sh, run_ichorCNA.R, create_panel_of_normals.sh)
- Panel par défaut: Florian (`ichorCNA-panel-of-normals_median.rds`), Broad et custom aussi disponibles
- Dependencies: `/scratch/dependencies/ichorCNA/` (gc_wig, map_wig, centromere, panels)
- Test Healthy_826: TFx=0.026, ploidy=2.306 — PASS
- `getwilds/ichorcna` testé et rejeté (pas de readCounter, pas de libs graphiques png)
- `remotes::install_github` n'installe pas `inst/scripts/` → scripts clonés séparément dans Dockerfile
- `runIchorCNA.R` ne crée pas le outDir → `mkdir -p` nécessaire dans le process NF

## IV Module (2026-05-07)

- Container: `blipinskiaima/raima:latest` (raima 0.4.17)
- Workflow: `workflow/IV.nf` — 1 process `IV_call`
- Script: `bin/iv_score.R` — appelle `raima::infer_sex` + `raima::infer_ancestry`
- Dependency: `/scratch/dependencies/raima-model/model_ancestry_data.tsv.gz` (1.5 GB)
- Outputs publies dans `${output}/${ID}/IV/`:
  - `${ID}.sex.tsv` — 1 ligne, 1 valeur scalaire
  - `${ID}.ancestry.tsv` — 2 lignes (header + valeurs), 18 colonnes nommees (Africa W/S/E/N, Middle East, Ashkenazi, Italy, Europe E/NW/SW, Finland, South America, Sri Lanka, Pakistan, Bangladesh, Asia E, Japan, Philippines)
- Active par defaut en prod/liquid/solid. Mode retrospectif supporte (BAM_FILE chain quand `--MERGE false`).
- Hors strategie de qualification (pas de check-conformity).
- Test Healthy_826 (CGFL solid): sex=0.9974, ancestry max Europe (NW)=0.4641 + Italy=0.3437 — PASS
- Test Healthy_4 (HCL liquid, retrospectif): sex=0.0005, ancestry Europe (SW)=0.579 + (NW)=0.4055 — PASS

## Refonte rapport PDF ctDNA — Typst V2 (2026-05-07)

- Pivot LaTeX/XeLaTeX → **Typst 0.14.2** (binaire Rust 40MB, compile <1s, pas de math mode buggé, Unicode natif)
- Direction retenue : **GRAIL Galleri** (Result en grande card colorée centrale, accessible patient + clinicien)
- Template final : `test/V2final/report-grail-v2.typ` + 4 PDFs de test (NEG/POS × clean/warning)
- Container futur : `blipinskiaima/rapportv4:latest` (à créer 2026-05-11)
- Charte AIMA + Éxís hybride dans `~/.claude/rules/aima-brand.md`
- See [report_pdf_typst_v2.md](report_pdf_typst_v2.md) for full details

## QC Refactor (2026-05-26 → 2026-05-27)

### Phase 1 (2026-05-26, commit 12c5026)
- BAM_Count + Extract_Read_Start_Time deplaces vers `workflow/qc.nf` (process atomiques importables)
- Workflow `Merge` ne fait plus que merger (BAM_mergering + BAM_sort) — plus aucun couplage avec BAM_Count
- `checkIfExists: true` ajoute sur le fallback BAM merged en mode retrospectif (fix bug latent main.nf ancien:163)
- Fichier `workflow/read_start_time.nf` supprime (wrapper inutile)
- Workflow `QC` dans `qc.nf` reste appele par `beta.nf` (QC_epics + QC_sub sur BAM filtre/subsampled) — INCHANGE
- Test `/test_bam2beta` sur Healthy_826 CGFL liquid: TEST OK (1m41, RUN CONFORME 17/17, QUALIF identique bit-a-bit a V1.1.2)
- Commits: `979e31b` (cleanup main.nf : drop SCORE block) + `12c5026` (refactor QC phase 1)

### Phase 2 (2026-05-27)
- BAM_Count + Extract_Read_Start_Time **encapsules dans `workflow Beta_epic`** (beta.nf), ne sont plus invoques au top-level dans main.nf
  - `bam_merged = bam_metadata.filter{DEPTH=="merged"}.map{ID,DEPTH,BAM,BAI -> tuple(ID,BAM,BAI)}` extrait depuis bam_metadata
  - `BAM_Subsampling(bam_metadata, BAM_Count.out.nb_reads_total)` chaine direct
- **Process definitions deplacees de qc.nf vers beta.nf** (intervention Boris) : BAM_Count et Extract_Read_Start_Time sont desormais des process locaux a beta.nf (lignes 418, 435). qc.nf ne contient plus que workflow QC + Mosdepth_qc + Cramino_qc.
- Signature `Beta_epic` perd le param `bam_count` (passe de 7 a 6 inputs)
- **Extract_Read_Start_Time non-conditionnel** : tourne systematiquement dans Beta_epic (le `if params.READ_ST` retire)
- `params.READ_ST` retire de `nextflow.config` (devenu orphelin apres retrait du conditionnel)
- **Changement de semantique** : BAM_Count et Read_ST ne tournent plus si `--BETA false` (vs avant ils tournaient au top-level independamment de BETA)
  - Acceptable car BAM_Count n'a aucun consommateur sans BETA (BAM_Subsampling est dans Beta_epic)
  - Read_ST devient un sous-module de BETA
- **Regression connue (acceptee)** : `dev/SCW/launch_SCW.sh` (backfill Read_ST standalone via `--BETA false --READ_ST true`) ne fonctionne plus. Script laisse intact volontairement, decision Boris 2026-05-27.
- Files: `main.nf` (-11), `workflow/beta.nf` (+46, dont +37 process defs deplaces), `workflow/qc.nf` (-37 process defs deplaces), `nextflow.config` (-1), `merge.nf` intact
- Test `/test_bam2beta` (Healthy_826 CGFL liquid, 2026-05-27): **TEST OK**
  - RUN CONFORME (17/17 fichiers)
  - QUALIFICATION CONFORME vs V1.1.2 (raima_score V2, fragmentomics, bedMethyl 14289 lignes, score_cnv : tous identiques bit-a-bit)
- Commit: `0eec4c4` + tag `pre-raima-refactor`

## Raima Refactor (2026-05-27)

Fusion des 3 process Raima_process / _v1_2 / _probs en 1 seul process Raima_score_all (optimisation ressources Docker/R).

### Avant
- 3 process NF: `Raima_process` (V2), `Raima_process_v1_2` (V1.2), `Raima_process_probs` (props)
- 3 scripts R: `bin/raima_score.R`, `bin/raima_score_v1.2.R`, `bin/raima_score_probs.R`
- 3 containers Docker `raima:latest` demarres par sample
- 3x chargement `library(raima)`, 3x lecture bedMethyl, 3x chargement modeles

### Apres
- 1 process NF: `Raima_score_all` (V2 + V1.2 + props dans le meme run)
- 1 script R: `bin/raima_score_all.R` (44 lignes vs 79 lignes des 3 scripts orig)
- 1 container Docker `raima:latest` demarre par sample (-50% containers BETA)
- 1x lib R, 1x bedMethyl, 1x modeles
- 3 scripts orig archives dans `bin/archive/`

### Cleanup additionnel
- `main.nf`: retire 5 includes Raima_process* orphelins + commentaire mort
- `conf/base.config`: retire `withName: Raima_process / _v1_2 / _probs / _filter` + entrees orphelines Modkit_adjust_filter / Modkit_pileup_filter (Beta_filter supprime au commit precedent)

### Outputs preserves (bit-a-bit identique vs V1.1.2)
- `${ID}.${DEPTH}.epic.raima_score.V2.tsv` (publishDir BETA/)
- `${ID}.${DEPTH}.epic.raima_score.V1.2.tsv` (publishDir BETA/)
- `${ID}.${DEPTH}.epic.props_v1.tsv` (publishDir BETA/)
- `raima_version.txt` (consomme par log Beta_epic)

### Bug rencontre durant l'implementation
- 1er test KO: Raima_score_all utilisait container default `bam2beta:latest` (pas raima). Fix: ajouter `withName: Raima_score_all { container = 'blipinskiaima/raima:latest' }` dans conf/base.config.
- Apprentissage: dans Bam2Beta, le container est assigne par `withName:` dans conf/base.config, PAS dans le process lui-meme. Tout nouveau process Raima_* doit avoir son entree withName ou il herite du container default.

### Validation
- Test `/test_bam2beta` (Healthy_826 CGFL liquid, 2026-05-27): **TEST OK**
- RUN CONFORME (17/17 fichiers) + QUALIFICATION CONFORME vs V1.1.2 bit-a-bit

## Dead Code Cleanup (2026-05-27)

Cleanup cible code mort post-refactor BAM_Count/Read_ST/Raima_score_all. Validation item par item (Boris a choisi de garder une partie pour future-features).

### Supprime
- **`nextflow.config`** (5 params orphelins, 0 usage code):
  - `SCORE`, `SCORE2`, `SCORE_V1_2` (bloc SCORE supprime commit 979e31b)
  - `windows = 0`, `mike_pct = "True"` (CNV legacy)
- **`main.nf`**: log "--cpu INT" dans help (params.cpu n'existe pas, remplace par cpus_max)
- **`conf/base.config`**: rename `withName: Extract_Read_Start_Time` -> `withName: Read_Start_Time` (process renomme dans commit 0eec4c4)
- **`conf/prod.config`**: 2 blocs `withName` orphelins (Raima_process et Raima_process_probs supprimes commit 591733b)

### Garde volontairement (Boris)
- Process orphelins `Nanoplot_qc`, `Plot_Coverage_By_Chromosome`, `Samtools_qc` dans qc.nf (reserve future)
- Params CNV/ichorCNA `bin_size`, `penalty`, `gain/loss_threshold`, `min_segment_size`, `ref_bins_bed`, `ichorcna_panel_broad/_custom`, `sep` (futures features)
- Params `mode`, `date_tag`, `sample`, `run` (futures features)
- Log-only params `date`, `subsample_fraction` (info au runtime)
- Comment `//Raima_process_CNV (minLen75_maxLen200)` (R&D snippet)
- Commentaire debug `//BAM_PATH.view()` dans main.nf

### Validation
- Test `/test_bam2beta` Healthy_826 CGFL liquid: TEST OK (RUN + QUALIF CONFORME bit-a-bit)

## metadata.json natif (V1.3.1, 2026-05-27)

Le pipeline Bam2Beta genere desormais nativement un `metadata.json` dans `REPORT/` pour chaque sample (DEPTH=merged uniquement), schema trace-platform 10 champs complet :

- `client_uuid` (string, vide par defaut, surchargeable via `--client_uuid`)
- `analysis_name` (string, vide par defaut, surchargeable via `--analysis_name`)
- `patient_name` (= `params.patient_id`, default "DEV")
- `sample_name` (= ${ID})
- `nb_reads_total` (int, depuis BAM_Count `${ID}.nb_reads_total.tsv`)
- `nb_reads_aligned` (int, depuis cramino `${SAMPLE}.merged.cramino.tsv` col 6)
- `depth` (float, depuis mosdepth summary.txt col 4 ligne `total`)
- `coverage_percent` (float, depuis mosdepth global.dist.txt ou `$1==total && $2==1` * 100)
- `mvaf` (float, depuis raima_score.V2.tsv col 3 ligne `v1`)
- `generated_at` (ISO 8601 UTC, `date -u +%Y-%m-%dT%H:%M:%SZ`)

Remplace le script externe `~/Pipeline/trace-platform/scripts/build_metadata_json.sh` (generation desormais native dans le process Nextflow `Raima_report`).

**Implementation** :
- `Mosdepth_qc` emit additionnel `dist_tuple` (tuple ID/DEPTH/path pour global.dist.txt)
- `BAM_Count` emit additionnel `nb_reads_total_tuple` (tuple ID/path)
- `Beta_epic` `combined_results` chain : +2 joins (`.join(dist, by:1)` + `.combine(nb_reads_total_tuple, by:0)`)
- `Raima_report` input etendu (+2 paths) + output `metadata.json` `optional: true` + bloc script conditionnel `if [ "${DEPTH}" == "merged" ]`

**Gotcha** : utiliser `.combine(by: 0)` (pas `.join(by: 0)`) pour broadcaster `nb_reads_total` (1 file/sample) sur les N entrees de `combined_results` (1 par depth) — sinon N-1 entrees sont dropped.

Test `/test_bam2beta` Healthy_826 CGFL liquid 2026-05-27 : TEST OK (RUN + QUALIF CONFORME bit-a-bit vs V1.3.0) + metadata.json 10 champs valides.

## Feedback

- [S3 Never Delete](feedback_s3_no_delete.md) - NEVER delete anything from S3 buckets
- [Bash inline dans process Nextflow](feedback_bash_inline.md) - Boris préfère bash inline dans `script:""""""` plutôt que scripts externes dans `bin/Module/`
- [Versioned template swap](feedback_versioned_template_swap.md) - Ne jamais modifier en place un fichier référencé par un workflow NF actif — utiliser une copie versionnée et basculer au moment du switch container
