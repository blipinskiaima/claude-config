---
name: bam2beta_architecture
description: Architecture Bam2Beta — workflow, inputs BAM, conventions naming, scoring RAIMA, outputs S3, profiles
metadata:
  type: project
---

## Bam2Beta V1.2.0 — Architecture et conventions

**Version manifest** : V1.1.2 (nextflow.config) mais README dit V1.2.0 (IV module ajouté 2026-05-11)

### Input BAM
- `--input` = chemin S3 vers un **dossier** contenant des `.bam` (pas un fichier individuel)
- Bam2Beta découvre les BAMs via `find "${BAM}/" -maxdepth 1 -type f -name "*.bam"` (workflow/merge.nf:47)
- L'ID sample = **nom du dossier** (path.name dans main.nf:125)
- Pas de validation explicite ni de check de headers/tags en entrée — samtools merge/sort sans contrainte
- Le BAI est **généré par le pipeline** (BAM_sort produit .bam + .bai) — pas nécessaire en input
- Pas de vérification de read groups ni MD tag — modkit pileup travaille sur les mod-tags ONT (MM/ML)
- Profil liquid : rarefaction `merged,20M,15M,10M,5M,2M,1M`

### Naming samples
- L'ID = nom du dossier S3 passé à --input, sans contrainte regex
- Pas de routing automatique tumoral vs healthy — le pipeline traite tout identiquement
- Le naming `${SAMPLE}_Healthy_${X}_target_${Y}` est compatible (juste un ID string opaque)
- Le rapport PDF utilise `cut -d '.' -f 1` sur l'ID pour extraire le "name" patient (beta.nf:326)

### Scoring RAIMA / mVAF (TF)
- `raima_score.R` : appelle `raima::model_v1()` + `raima::model_v2()` sur le bedMethyl
- Output TSV : colonnes model / score / mVAF (alias TF depuis V1.0.1)
- Le mVAF est extrait pour le rapport via `awk -F'\t' '$4 == "v1"' | cut -f 3` (beta.nf:354)
- Pas de seuil positif/négatif codé dans Bam2Beta — le seuil est dans le package `raima` R (opaque)
- `raima_score_v1.2.R` : scoring rétrospectif v1.2 (range_w=c(0,10) selon changelog)
- `raima_score_cnv.R` : scoring CNV via raima (depths + score_cnv.tsv)

### Outputs S3
- Arborescence : `{OUTPUT}/{SAMPLE_ID}/BETA/{ID}.merged.epic.raima_score.V2.tsv`
- JSON : `{OUTPUT}/{SAMPLE_ID}/REPORT/{ID}.merged.epic.raima_score.V2.json` (champs: score, tf, nb_reads_raw, depth)
- 17 fichiers attendus par sample (critère conformité)

### Profils
- `prod` : MERGE+BETA+FRAG+CNV+IV, rarefaction=merged, cpus_max=8, mem=32GB
- `liquid` : tous modules + rarefaction 7 niveaux (merged,20M,...,1M)
- `scw` : profil AWS Scaleway fr-par

### Paths S3 inputs connus
- Données CGFL liquid : `s3://aima-bam-data/data/CGFL/liquid/`
- Sample test : `Healthy_826` dans `s3://aima-bam-data/data/CGFL/liquid/`
- BAM merges R&D : `s3://aima-bam-data/processed/MRD/RetD/*.merged.bam` (~18.62 To)
- Profil AWS : toujours `scw` (endpoint https://s3.fr-par.scw.cloud)

### Points d'attention pour dilutions in silico
- Pas de stress-test documenté sur 0.1% VAF — territoire inconnu pour Bam2Beta
- BAM_Subsampling skipe silencieusement si total_reads <= target (ex: 1M skip si BAM < 1M reads)
- Modkit pileup filtre avec `--include-bed epic850K.extended.100.clean.bed` — les reads hors EPIC sont exclus
- La profondeur effective sur les CpGs EPIC est ce qui compte pour la qualité du score

### Rarefaction horaire (12h/24h/48h) — workflow/rarefaction_horaire.nf
- Process unique `Rarefaction_Horaire_Cascade` (1 process produit les 3 points via `saveAs`). Source = BAM merged COMPLET (non epic, non subsample) du sample standard.
- t0 = MIN(epoch absolu des tags `st:Z:` de tous les reads PRIMAIRES `-F 0x900`), calculé PAR OFFSET horaire puis arbitré en epoch (gère un run à cheval sur un changement d'heure — bug réel corrigé sur Prostate_31, 1h d'erreur). Code STRICTEMENT identique (même awk) au process `Read_Start_Time` de beta.nf:104-122, mais RECALCULÉ inline — ne lit PAS `QC/Samtools/{s}.read_start_time.tsv`, aucune dépendance fichier entre les deux.
- Cascade DÉCROISSANTE 48→24→12h, chaque point réutilise le bam du point précédent comme source (12h⊂24h⊂48h). Seuil = t0+POINTh, réexprimé par offset. Sélection : `samtools view -b -N ids.txt`. Point écarté (log WARN) si durée séquençage ≤ POINT (bam identique à la source).
- **2 passes Nextflow séparées** (script réel : `dev/SCW/rarefaction_horaire.sh`) :
  1. `--input .../CGFL/${ID} --output .../CGFL --MERGE false --RAREFACTION_HORAIRE true -profile scw,docker` → produit les 3 BAM horaires, publiés à `${output}_rarefaction_horaire/${ID}_{12,24,48}h/BAM/` (suffixe ajouté par le `publishDir` lui-même, rarefaction_horaire.nf:18)
  2. Pour chaque `{ID}_{TIME}h` : `--input .../CGFL_rarefaction_horaire/${ID}_${TIME}h --output .../CGFL_rarefaction_horaire --MERGE false -profile scw,docker --BETA true --BETA_28M true --RAPPORT false` → fait tourner le pseudo-sample dans le pipeline STANDARD (Beta_epic + Beta_28M), pas un code dédié.
  - Modules non passés en CLI restent au DEFAULT de nextflow.config (params{} racine, AUCUN profil liquid/prod/solid appliqué) : CNV=false, FRAG=false, IV=false, ICHORCNA=false, MITO=false, TOO=false, THEMELIO=false → explique pourquoi le pseudo-sample horaire n'a QUE 7 dossiers (pas de REPORT/Fragmentomics/IV/ichorCNA/TOO/THEMELIO).
  - Dossier `CNV/` quand même présent : vient de `Raima_process_CNV` (beta.nf:229-248), appelé SANS garde `if` À L'INTÉRIEUR de `Beta_epic` (déclenché par BETA=true, indépendant de params.CNV qui contrôle un AUTRE module, cf. plus bas).

### Chaîne EPIC (Beta_epic, workflow/beta.nf) — mVAF V1/V2/V1.2, props_v1, CNV score
- `BAM_Count` (beta.nf:80-103) : `samtools view -c` (aucun filtre) → `QC/Samtools/{ID}.nb_reads_total.tsv` ; + `samtools idxstats` → `.idxstats.tsv` (même process)
- `Read_Start_Time` (beta.nf:104-122) : `samtools view -F 0x900` + awk extrait tag `st:Z:` → `QC/Samtools/{ID}.read_start_time.tsv` (fichier volumineux, jamais parsé par trace-prod, existence seule)
- `BAM_Subsampling` (beta.nf:123-149) : si DEPTH≠"merged" ET total_reads>target, `samtools view -s 42.FRACTION` (seed 42) ; sinon (dont TOUJOURS le cas "merged") passthrough silencieux, aucune commande
- `BAM_filtering` (beta.nf:150-167) : `samtools view -L bed_epic -F 3840 -b` → `.{DEPTH}.epic.bam`. `-F 3840` = exclut secondaire+QCfail+dup+supplémentaire (PAS de filtre MAPQ ici). `bed_epic` = `epic850K.extended.100.clean.bed` (nextflow.config:161)
- `Modkit_adjust` (beta.nf:168-182) : `modkit adjust-mods --convert h m` (5hmC→5mC AVANT pileup) → `.epic.converted.bam`
- `Modkit_pileup` (beta.nf:183-204) : `modkit pileup -r FASTA --cpg --combine-strands --include-bed BED` → `BETA/{ID}.{DEPTH}.epic.bedMethyl(.gz)`
- `Raima_score_all` (beta.nf:205-228, script `bin/raima_score_all.R`, fusion de 3 anciens scripts) — sur le bedMethyl EPIC :
  - `raima::model_v1()` + `raima::model_v2()` → **rbind** dans **un seul fichier** `BETA/{ID}.{DEPTH}.epic.raima_score.V2.tsv` (2 lignes : model="v1" ET model="v2" ; le nom "V2" = version du FICHIER/script, pas "modèle v2 seul" — trace-prod filtre `$4=="v1"` dans ce même fichier pour sa colonne mvaf_v1)
  - `model_v1(range_w=c(0,10))` → `BETA/{ID}.{DEPTH}.epic.raima_score.V1.2.tsv` (même modèle v1, poids différents)
  - `model_v1(return_all_props=TRUE)` transposé → `BETA/{ID}.{DEPTH}.epic.props_v1.tsv` (16 classes, estimation ponctuelle SANS bootstrap — ne pas confondre avec `BOOTSTRAP/*.props.tsv`)
  - Version package capturée (`packageVersion('raima')`) → `raima_version.txt` **JAMAIS publié** (absent des patterns `publishDir`) — perdu au `cleanup=true` du workDir (nextflow.config:21). Seule trace : `log.info` console (beta.nf:46-49) et `metadata.json`/`raima_score.V2.json` SI RAPPORT=true.
- `Raima_process_CNV` (beta.nf:229-248, script `bin/raima_score_cnv.R`) sur le BAM merged BRUT (ni epic ni subsample) : `raima::depth_per_region()` puis `raima::model_CNV_v1()` → `CNV/{ID}.depths.tsv` + `CNV/{ID}.score_cnv.tsv`. **Mécanisme totalement distinct** du workflow `CNV`/`CNV_analysis.nf` (params.CNV, défaut false, segmentation/log2ratio/bin_coverage — sorties `*.cnv_segments.tsv`, `*.log2ratio.tsv.gz`, jamais `score_cnv.tsv`).

### Chaîne genome-wide "28M" (Beta_28M, workflow/beta_28M.nf) — Loyfer, bootstrap V1.4/V1.5, ex-V1.3
- "28M" = **modèle 28M CpG (genome-wide)**, par opposition au panel ciblé EPIC 850K (CHANGELOG.md ligne ~388 "Beta_28M : nouveau workflow pour le modèle 28M CpG Loyfer"). Ce n'est PAS un nombre de reads garanti — note manuelle non datée `NOTE_READ.txt` (sample Lung_9, 44,37M reads total) montre un exemple réel où le stade Preprocess_28M atterrit à 29,27M reads (65,97%), simple coïncidence d'ordre de grandeur pour CE sample.
- `Preprocess_28M` (beta_28M.nf:69-89) PAR CHROMOSOME chr1-22 (pas de chrX/Y/M) : `samtools view -h -q 20 -F 3844 BAM chr${CHR}` (MAPQ≥20 EN PLUS de -F3840, absent de la branche EPIC) puis reconstruction d'un header restreint au chr courant
- `Modkit_extract_full_28M` (beta_28M.nf:90-109) : `modkit extract full --cpg --interval-size 500000 --bgzf` → `EXTRACT_FULL_28M/{ID}.merged.all.chr{N}.extract_full_table.bgzf` (table brute read×CpG, PAS un pileup)
- `Modkit_pileup_28M` (beta_28M.nf:110-129) : `modkit pileup --cpg --combine-strands --combine-mods` (PAS de `--include-bed`, `--combine-mods` remplace le `Modkit_adjust` de la branche EPIC) → `BETA_28M/{ID}.merged.all.chr{N}.bedMethyl.gz`
- `Raima_process_loyfer` (beta_28M.nf:130-152, script `bin/raima_score_loyfer.R`) sur les 22 bgzf : `raima::bedmethyl_prob()` (filtre `max_read_len=1000` si liquid, `Inf` si solid — filtre INTERNE au script R, indépendant du filtre samtools n50/pct_mass_removed de trace-prod v24) puis `raima::prop_loyfer(bedMethyl_select=1:4, model_loyfer)` transposé → `EXTRACT_FULL_28M/{ID}.merged.all.props_loyfer.tsv` (31 classes, estimation ponctuelle, PAS bootstrapée). Méthode de déconvolution interne au package `raima` — opaque (pas de détail dans Bam2Beta)
- `bootstrap_model` (beta_28M.nf:174-211, script `bin/bootstrap_model_v1.2.R`) sur les 22 bgzf TRIÉS (tri déterministe read_id+position+mod_code, `LC_ALL=C sort`, car modkit extract écrit en ordre non déterministe multi-thread — nécessaire pour reproductibilité du bootstrap) :
  - `raima::bootstrap_model_v1(paths, return_all_props=TRUE, whitelist)` → 200 réplicats × 16 proportions (rééchantillonnage interne au package raima, méthode non documentée dans Bam2Beta — probablement resampling des CpG/reads du genome-wide dataset, PAS visible dans le code Nextflow)
  - `BOOTSTRAP/{ID}.merged.all.bootstrap_v1.tsv` = 200 scores = `rowSums(props[,c("colon_1","lung_1","breast_1","ovary_1")])` (SEULEMENT 4 des 16 classes sommées = classes tumorales)
  - `BOOTSTRAP/{ID}.merged.all.bootstrap_v1.props.tsv` = les 200×16 proportions brutes
  - mVAF **V1.4** = `mean(sqrt(scores))^2 * 100` (transfo racine-carrée puis moyenne puis carré, réduit le biais d'une moyenne de ratios) → `BETA/{ID}.merged.epic.raima_score.V1.4.tsv`
  - mVAF **V1.5** = `raima::transfo_mvaf_by_cov(V1.4, nb_read_epic_millions)` — correction par la profondeur EPIC réelle (`nb_read_epic` = colonne 6 de la dernière ligne de `QC/Cramino/{ID}.merged.epic.cramino.tsv`, DOIT être divisé par 1e6, requiert raima≥0.5.4) → `BETA/{ID}.merged.epic.raima_score.V1.5.tsv`. Mode rétrospectif dédié `mvaf_v1_5_retro` (beta_28M.nf:212-231, `--MVAF15_RETRO`) rejoue VERBATIM ces 2 dernières lignes depuis le bootstrap_v1.tsv déjà sur S3, sans rejouer le bootstrap.
  - `raima_version.txt` ici aussi **NON publié** (absent des patterns `bootstrap_model`)
  - **V1.3 = ARCHIVÉ** (`bin/archive/raima_score_v1_3.R`, process `Raima_score_v1_3` commenté dans beta_28M.nf:44-54) : ancienne version point-estimate (pas bootstrap) du modèle genome-wide, `raima::model_v1(radii=1:100, whitelist)` sur les 22 bedMethyl_28M. Plus jamais recalculé nativement.

### epic / merged / 28M(all) — définitions
- `merged` = sortie brute de `Merge` (workflow/merge.nf) : `samtools merge`(ou copie si 1 seul bam) + `sort` + `index`. Aucun filtre.
- `epic` = merged (ou merged-subsample à un DEPTH donné) restreint via `-L bed_epic -F 3840` (panel EPIC850K étendu 100bp, PAS de filtre MAPQ)
- `all` (28M) = merged restreint via `-q 20 -F 3844`, PAR chr1-22 uniquement (pas MT/X/Y), genome-wide (aucun bed panel)

### Traçabilité version pipeline (limite connue, utile pour doc qualité)
- `manifest.version` (nextflow.config:15) = source de vérité déclarative, actuellement `V2.2.0`. Container docker `blipinskiaima/bam2beta:latest` (nextflow.config:53) — tag MUTABLE, pas de pin par run.
- Pour un run donné, la version n'est écrite dans `metadata.json`/`REPORT/*.json` QUE si `RAPPORT=true` (merge.nf:111, uniquement branche FAIL sinon voir rapport.nf) — les runs horaire (`RAPPORT false`) n'ont **aucune trace de version dans leurs outputs S3**. `trace{}`/`report{}`/`timeline{}` Nextflow sont `enabled=false` par défaut (nextflow.config:228-247), non réactivés par le profil `scw,docker`.
- Donc : version exacte utilisée pour un lot horaire déjà calculé = **non traçable depuis les données produites**, seulement approximable via `git log -- nextflow.config` croisé avec la date S3 (`LastModified`) du lot.
