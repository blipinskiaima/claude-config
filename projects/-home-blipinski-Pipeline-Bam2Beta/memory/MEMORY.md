# Bam2Beta Project Memory

## Key Facts

- Current version: **V2.1.0** (2026-07-16, minor : **module TOO** (Tumor of Origin, TOO5 v0.4.1) actif en prod + refonte du `raima_score.V2.json`. **BREAKING** : `score` supprimé du JSON (doublon strict de `tf`), `model` passe de `"v1"` à `"v1.4"`, `RAPPORT` requiert `TOO`. JSON à 18 champs : + `sex`, `coverage`, 5 probas TOO, 4 seuils. Les 2 seuils TOO sortent du **bundle** (`run_too5.R` → CSV → `rapport.nf`), pas d'un param → le JSON ne peut pas contredire la décision qu'il publie. Qualif refondue : Lung_9 en 2e sample, 12 valeurs nommées, **bit-à-bit abandonné**. TEST OK 27/27. Voir [too-module.md](too-module.md))
- V2.0.2 (2026-07-07, patch : **suppression `set.seed(1)` R** dans bootstrap_model_v1.1.R = code mort. raima::bootstrap_model_v1 seede furrr en interne (parallel-safe, invariant ncores) → set.seed R écrasé/ignoré. Prouvé bit-à-bit inerte : 2 runs indépendants sans seed → 200 scores identiques entre eux ET à QUALIF V2.0.0 (md5 6ebc706). Repro = seeding interne raima + tri déterministe. **QUALIF OK** (QUALIF/V2.0.2 écrit ; 200 scores bootstrap md5 6ebc706 identiques sur les 3 QUALIF V2.0.0=V2.0.1=V2.0.2). Voir [bootstrap-model-v1.md](bootstrap-model-v1.md))
- V2.0.1 (2026-07-07, patch : tri déterministe pré-bootstrap passe du `sort` full-line à une **clé unique 3 colonnes** read_id+ref_position+mod_code (`-k1,1 -k3,3n -k14,14`). read_id+position seuls = 576k ex-æquo (2 lignes m/h par site CpG). Bit-à-bit conforme V2.0.0, TEST OK + **QUALIF OK** (QUALIF/V2.0.1 écrit, bit-à-bit vs V2.0.0) Healthy_826 tf=0.58, 200 scores bootstrap + V1.4 identiques. Voir [bootstrap-model-v1.md](bootstrap-model-v1.md))
- V2.0.0 (2026-07-06, BREAKING : le champ `tf` du rapport = mVAF v1.4 bootstrap 28M au lieu de l'ancienne mVAF ; `Raima_report` sorti de `Beta_epic` -> module `rapport` dans main.nf, param `--RAPPORT` ; BETA_28M actif prod ; raima:latest promu 0.5.3 ; repro v1.4 via tri bgzf `LC_ALL=C` + `set.seed(1)`). Qualif Healthy_826 tf=0.58 bit-a-bit vs V1.3.3 ; repro prouvee Healthy_826 (0.58 ×3) + Breast_48 (64.91 ×3). Voir [bootstrap-model-v1.md](bootstrap-model-v1.md)
- Container: `blipinskiaima/bam2beta:latest` + `blipinskiaima/raima:latest` (**0.5.3** depuis V2.0.0, promu depuis le tag 0.5.3 ; superset de 0.5.0, scores V2/frag/CNV/bedMethyl bit-a-bit inchanges) + `blipinskiaima/too:0.4.1` (TOO5 depuis V2.1.0 ; **les scripts R ne sont PAS dans l'image**, charges via `${projectDir}` -> modifier bin/TOO/ ne necessite aucun rebuild)
- Raima package version: **0.5.0** dans raima:latest depuis 2026-06-05 (requis par mVAF v1.3 + fragmento v2). Avant: 0.4.17 (2026-05-27)
  - Retrocompatibilite 0.4.13 -> 0.4.17 confirmee bit-a-bit sur Healthy_826 CGFL liquid (test 2026-05-27 vs V1.1.2)
  - Image `raima:0.4.17` (tag dedie) existait deja depuis 2026-05-07 mais `raima:latest` etait reste sur 0.4.13
  - Gotcha : verifier la version effective avec `docker run --rm raima:latest R -e 'packageVersion("raima")'` apres tout bump
- Pipeline modules: MERGE, BETA (EPIC), BETA_28M (Loyfer + score mVAF v1.3), FRAG (v2 softclip-removed), CNV, ICHORCNA, IV, **TOO** (Tumor of Origin TOO5 v0.4.1, prod, container too:0.4.1), **RAPPORT** (workflow/rapport.nf, requiert BETA+BETA_28M+TOO), bootstrap (R&D, raima:0.5.3), QC, SMALL_FRAGMENTS (filtre 75-200 bp, ex SHORT_READ)
- **Rarefaction cascade** (`workflow/rarefaction.nf`, 2026-07-07, R&D) : BAM rarifies nestes 20M->10M->5M->2M->1M via `samtools -s`, 2 temps facon small_fragment. **GOTCHA** : `samtools view -s` = hash absolu du read-name ; meme seed en cascade -> seuils composes en MIN -> comptes faux (frac x N_merged, trop hauts). Fix = seed **incremente** par niveau. Valide (comptes +/-0.13%, nesting 0 orphelin, bug reproduit sur donnee reelle). Tag rollback `pre-rarefaction`. Voir [rarefaction-cascade.md](rarefaction-cascade.md)
- **Flux small_fragment** (ex short_read, rename commit d6d4556, 2026-06-25) : stratégie ultra-simple 2-temps, le BAM filtré 75-200 se fait passer pour `merged.bam` dans `CGFL_small_fragments`, **cœur inchangé**. Tag rollback `pre-small-fragment`. TODO rename S3 + Phase 2 (v1.3/v1.4) bloquée par 28M merged-hardcode. Voir [small-fragment-flow.md](small-fragment-flow.md)
- `--MVAF1_4` (remplace `--MVAF1_3`, supprime): transfo mVAF v1.4 = `mean(sqrt(scores))^2` sur les 200 scores bootstrap. Rétrospectif : lit `BOOTSTRAP/${ID}.merged.all.bootstrap_v1.tsv` sur S3, aucun recalcul. Process `bootstrap_transfo` (script `bin/bootstrap_trasnfo.R`, container défaut bam2beta), importé dans main.nf. Voir [bootstrap-model-v1.md](bootstrap-model-v1.md)
- `--bootstrap`: bootstrap du score mVAF v1 (raima::bootstrap_model_v1, 200 scores) sur les 22 extract_full_table.bgzf. From-scratch (Beta_28M) + retrospectif (lit EXTRACT_FULL_28M/*.bgzf sur S3). **3 sorties** (file 1 `bootstrap_model_v1.1.R`): scores + props + `raima_score.V1.4`. Container `raima:0.5.3`. Validé bit-à-bit Breast_10 (0.5.1) + Lung_138 (0.5.2). Voir [bootstrap-model-v1.md](bootstrap-model-v1.md)
- **Check_Input** (workflow Merge, en amont du merge, 2026-06-23) : QC des fichiers d'entree. Input non conforme (BAM corrompu/0 read, fichier non whiteliste, 0 .bam) -> run **SUCCESS**, seul Check_Input, publie `REPORT/metadata.json` (status=FAILED_QC_INPUT + reason). Input OK -> pipeline normal ; autre erreur -> crash normal. Gate via `.branch` sur `env('QC_STATUS')`. Voir [check-input-qc.md](check-input-qc.md)
- **Rapport PDF retire** (2026-06-23) : generation desactivee (output `rapport` + `rmarkdown::render` commentes dans beta.nf), PDF retire de la conformite (check-run-output/check-conformity) + doc. `Raima_report` ne produit plus que les JSON (raima_score.V2.json + metadata.json). Container rapportv2 conserve. Voir [check-input-qc.md](check-input-qc.md)
- Prod profile enables: MERGE + BETA + BETA_28M + FRAG + CNV + IV + **TOO** + **RAPPORT**
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

- [Module TOO](too-module.md) — Tumor of Origin TOO5 v0.4.1 : vendoring vs wrapper, source de verite des seuils (le bundle, pas too_common.R), gotchas parse quote-aware / apostrophe awk / `pred$x <- NULL`, qualification Lung_9
- [Batch effect investigation](batch-effect-investigation.md) — Investigation complète CGFL vs HCL : 17% FP Healthy HCL (V1), CNV biaisé, pas d'effet taille fragments
- [Soft clipping & longueur FRAG](softclip-fragmentomics-length.md) — FRAG = length(SEQ), soft clips inclus ; vérifié Lung_115/95, ne pas migrer vers span réf
- [Coverage analysis CGFL vs HCL](coverage-analysis-cgfl-hcl.md) — outil dev/coverage_analysis (binning per-base mosdepth 100kb) ; couverture autosomale équivalente CGFL/HCL, trous = non-mappable, pas d'effet labo ; Healthy_780 per-base corrompu
- [covdepth QC valorization](covdepth-qc-valorization.md) — chantier R&D QC depth/coverage ; **Étape 1 livrée** (Fig.1 cumulative depth-vs-breadth + Fig.2 positionnelle multi-échelle/bandes déplétion, 4 samples) ; finding 067 vide (34M reads alignés, depth=0) + concordance mosdepth↔trace-prod ; roadmap multi-échelle

## Debugging Insights

- [gh release 403 → fallback token](github-release-token.md) — `gh release create` échoue en 403 avec le `GITHUB_TOKEN` de `github.sh` (PAT sans perm releases) ; fix `env -u GITHUB_TOKEN gh release ...`

- **raima 0.4.5 casse Raima_process_CNV** : `depth_per_region` n'est pas exportee dans 0.4.5. Fix: utiliser raima 0.4.3 dans le Dockerfile.
- **Container raima:latest doit etre rebuild** apres modification du Dockerfile — sinon Docker utilise l'ancienne image cachee.
- Le test GRCh38 a fonctionne avec l'ancien cache Docker (raima 0.3.2 dans le container) car `Raima_process_CNV` n'appelle pas `depth_per_region` dans cette version.
- **Container assigne par `withName:` dans conf/base.config, PAS dans le process** : tout nouveau process raima doit avoir son entree withName sinon il herite du default `bam2beta:latest`. Ex : Raima_score_all, bootstrap_model (→ raima:0.5.2).
- **Channel vide → emit de sous-workflow qui plante** (gotcha NF 25.04, 2026-06-23) : couper l'aval via un channel vide fait planter a la CONSTRUCTION si le sous-workflow a un `emit:` referencant un process aval (`No such property: X for DataflowBroadcast`). Fix : retirer les emits inutilises (Beta_epic/Frag/IV n'avaient aucun consommateur). Voir [check-input-qc.md](check-input-qc.md).

- **Channel.fromPath = queue channel a 1 item** (gotcha NF, 2026-07-16) : consomme en `path()` simple, il limite le process a **UNE execution par invocation**, quel que soit le nombre de samples. Sans effet en prod (1 sample par run -> 1 item suffit) ; en multi-samples, 7/10 samples perdaient leur `props_loyfer` et etaient droppes par le join TOO. **Fait manquer des sorties, jamais de resultat faux.** Fix `.first()` (-> value channel reutilisable). Pose sur RAIMA_LOYFER + RAIMA_V1_WL ; **le motif subsiste sur RAIMA_MODEL1/2, ANCESTRY_MODEL, BED, FASTA, FAI** (inoffensif en prod, candidat patch). Voir [too-module.md](too-module.md)

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
