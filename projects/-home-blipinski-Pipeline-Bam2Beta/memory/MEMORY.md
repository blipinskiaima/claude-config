# Bam2Beta Project Memory

## Key Facts

- Current version: **V1.3.2** (2026-06-05, score mVAF v1.3 + fragmentomics v2 softclip-removed + raima 0.5.0)
- Container: `blipinskiaima/bam2beta:latest` + `blipinskiaima/raima:latest` (0.5.0) + `blipinskiaima/raima:0.5.2` (bootstrap only, latest reste intacte)
- Raima package version: **0.5.0** dans raima:latest depuis 2026-06-05 (requis par mVAF v1.3 + fragmento v2). Avant: 0.4.17 (2026-05-27)
  - Retrocompatibilite 0.4.13 -> 0.4.17 confirmee bit-a-bit sur Healthy_826 CGFL liquid (test 2026-05-27 vs V1.1.2)
  - Image `raima:0.4.17` (tag dedie) existait deja depuis 2026-05-07 mais `raima:latest` etait reste sur 0.4.13
  - Gotcha : verifier la version effective avec `docker run --rm raima:latest R -e 'packageVersion("raima")'` apres tout bump
- Pipeline modules: MERGE, BETA (EPIC), BETA_28M (Loyfer + score mVAF v1.3), FRAG (v2 softclip-removed), CNV, ICHORCNA, IV, MVAF1_3 (retrospectif), bootstrap (R&D, raima:0.5.2), QC
- `--MVAF1_3`: mode retrospectif score v1.3 (collecte 22 bedMethyl_28M deja sur S3, aucun recalcul). Process `Raima_score_v1_3` importe de beta_28M.nf dans main.nf. Voir [mvaf-v1.3-frag-v2.md](mvaf-v1.3-frag-v2.md)
- `--bootstrap`: bootstrap du score mVAF v1 (raima::bootstrap_model_v1, 200 scores) sur les 22 extract_full_table.bgzf. From-scratch (Beta_28M) + retrospectif (lit EXTRACT_FULL_28M/*.bgzf sur S3, miroir MVAF1_3). Container `raima:0.5.2` (bump 0.5.1→0.5.2 le 2026-06-17). Validé bit-à-bit Breast_10 (0.5.1) + Lung_138 (0.5.2). Voir [bootstrap-model-v1.md](bootstrap-model-v1.md)
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
- [Coverage analysis CGFL vs HCL](coverage-analysis-cgfl-hcl.md) — outil dev/coverage_analysis (binning per-base mosdepth 100kb) ; couverture autosomale équivalente CGFL/HCL, trous = non-mappable, pas d'effet labo ; Healthy_780 per-base corrompu

## Debugging Insights

- **raima 0.4.5 casse Raima_process_CNV** : `depth_per_region` n'est pas exportee dans 0.4.5. Fix: utiliser raima 0.4.3 dans le Dockerfile.
- **Container raima:latest doit etre rebuild** apres modification du Dockerfile — sinon Docker utilise l'ancienne image cachee.
- Le test GRCh38 a fonctionne avec l'ancien cache Docker (raima 0.3.2 dans le container) car `Raima_process_CNV` n'appelle pas `depth_per_region` dans cette version.
- **Container assigne par `withName:` dans conf/base.config, PAS dans le process** : tout nouveau process raima doit avoir son entree withName sinon il herite du default `bam2beta:latest`. Ex : Raima_score_all, bootstrap_model (→ raima:0.5.2).

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

## Refactors 2026-05-27 (détail complet dans git + commits cités)

- **QC Refactor** (commits 12c5026, 0eec4c4, tag `pre-raima-refactor`) : `BAM_Count` + `Read_Start_Time` encapsulés dans `workflow Beta_epic` (beta.nf), plus invoqués au top-level. Process defs locaux à beta.nf. `Merge` ne fait plus que merger. Sémantique : BAM_Count/Read_ST ne tournent plus si `--BETA false`. `params.READ_ST` retiré. Régression assumée : backfill Read_ST standalone via launch_SCW.sh KO (décision Boris). TEST OK, QUALIF bit-à-bit vs V1.1.2.
- **Raima Refactor** (commit 591733b) : 3 process (Raima_process/_v1_2/_probs) fusionnés en 1 `Raima_score_all` (bin/raima_score_all.R) → -50% containers BETA. Outputs V2/V1.2/props_v1 + raima_version.txt bit-à-bit identiques vs V1.1.2. 3 scripts orig dans bin/archive/. (Gotcha container withName → voir Debugging Insights.)
- **Dead Code Cleanup** : supprimé params orphelins nextflow.config (SCORE*, windows, mike_pct), log --cpu, rename withName Read_Start_Time, 2 withName orphelins prod.config. Gardé volontairement (futures features) : process Nanoplot_qc/Plot_Coverage_By_Chromosome/Samtools_qc, params CNV/ichorCNA, mode/date_tag/sample/run. TEST OK.

## metadata.json natif (V1.3.1, 2026-05-27)

- `Raima_report` génère nativement `REPORT/metadata.json` (DEPTH=merged uniquement), schéma trace-platform 10 champs : client_uuid, analysis_name, patient_name (=patient_id), sample_name, nb_reads_total (BAM_Count), nb_reads_aligned (cramino col6), depth (mosdepth summary col4 total), coverage_percent (mosdepth global.dist), mvaf (raima_score.V2 col3 v1), generated_at (ISO 8601 UTC). Remplace le script externe build_metadata_json.sh.
- **Gotcha** : `.combine(by: 0)` (PAS `.join`) pour broadcaster nb_reads_total (1 file/sample) sur les N entrées combined_results (1/depth) — sinon N-1 entrées droppées. TEST OK bit-à-bit vs V1.3.0.

## Feedback

- [S3 Never Delete](feedback_s3_no_delete.md) - NEVER delete anything from S3 buckets
- [Bash inline dans process Nextflow](feedback_bash_inline.md) - Boris préfère bash inline dans `script:""""""` plutôt que scripts externes dans `bin/Module/`
- [Versioned template swap](feedback_versioned_template_swap.md) - Ne jamais modifier en place un fichier référencé par un workflow NF actif — utiliser une copie versionnée et basculer au moment du switch container
