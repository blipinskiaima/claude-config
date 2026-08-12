# Bam2Beta Project Memory

## Key Facts

- **Version courante : V2.2.0** (2026-07-21) — module THEMELIO actif prod+liquid ; `metadata.json` devient le **contrat de sortie UNIQUE** (29 champs). BREAKING : `raima_score.V2.json` supprimé, `RAPPORT` requiert `TOO` (+ `THEMELIO` ssi `FRAG` actif), params `too_version`/`themelio_version` supprimés. ⚠️ casse `trace-platform/check_platform.py` non traitée. Voir [themelio-module.md](themelio-module.md)
- Historique versions : **V2.1.0** module TOO + refonte JSON ([too-module.md](too-module.md)) · **V2.0.0→V2.0.2** `tf` = mVAF v1.4 bootstrap 28M, tri déterministe clé 3 colonnes, `set.seed(1)` retiré (inerte, prouvé bit-à-bit) ([bootstrap-model-v1.md](bootstrap-model-v1.md))
- Containers : `bam2beta:latest` + `raima:latest` (**0.5.3** depuis V2.0.0) + `too:0.4.1`. ⚠️ Les scripts R de TOO **ne sont pas dans l'image** (chargés via `${projectDir}`) → modifier `bin/TOO/` ne nécessite aucun rebuild. Vérifier une version : `docker run --rm raima:latest R -e 'packageVersion("raima")'`
- Modules : MERGE, BETA (EPIC), BETA_28M (Loyfer + mVAF), FRAG (v2 softclip-removed), CNV, ICHORCNA, IV, MITO, TOO, THEMELIO, RAPPORT, bootstrap (R&D), QC, SMALL_FRAGMENTS
- **Prod** active : MERGE + BETA + BETA_28M + FRAG + CNV + IV + TOO + RAPPORT. ⚠️ `ICHORCNA=false` en prod mais **true en liquid/solid** — or les lanceurs `dev/SCW/` utilisent `-profile docker,tower,$TYPE,scw` (donc sans `prod`)
- Retry : doublement CPU/RAM par tentative, max 10, plafond `cpus_max`/`memory_max`

## Modules — fiches détaillées

- [Cascade de comptage des reads](read-counting-cascade.md) — **schéma de référence** : 4 strates A/B/C/D → `nb_reads_total` 100 % → `num_alignments` 85,6 % → `num_reads` 84,9 % → primaires mappées 75,8 % → FRAG 72,6 % → `Preprocess_28M` 66,0 %. ⚠️ `nb_reads_aligned` **inclut les non alignées** (+12 à 22 %). `flagstat` n'apporte rien (dup + QC-failed = 0 sur 10/10). Validé au read près
- [metadata.json](metadata-json.md) — contrat unique : provenance de chaque champ, **2 constructeurs exclusifs** (`rapport.nf` nominal / `Check_Input` dégradé), gotcha `status` absent = OK, `.combine(by:0)` pas `.join`
- [Module TOO](too-module.md) — TOO5 v0.4.1 : vendoring vs wrapper, seuils dans le **bundle** (pas `too_common.R`), gotchas parse quote-aware / apostrophe awk / `pred$x <- NULL`
- [Module MITO](mito-module.md) — QC mitochondrien : 11 colonnes, mosdepth merged non filtré, `-F 3840`, dual BETA/rétro, pas de `metadata.json`. ⚠ **Actif liquid + solid + prod depuis le 2026-08-12** (`fca2844`) — l'activation prod corrige le KO systématique de l'étape 2 de `/test_bam2beta` ; jamais exécuté sur du solid
- [Figure distribution de longueur](length-distribution-figure.md) — process `Length_Distribution_Plot` (`e8eac18`) : PNG 4 courbes vs 3 références embarquées, seuil 1 kb, **pondéré par la masse d'ADN** (la médiane est aveugle à la contamination, seul le N50 la voit)
- [QC N50/N75](n50-ratio-qc.md) — détecteur de **contamination gDNA** du plasma, dans `Extract_read` (`a95a36b`) → `QC/Samtools/{ID}.n50_ratio.tsv`, 12 colonnes. Plasma médiane **1,10**, urine 1,78 ; `Breast_6` 24,44 → **1,11** après filtre 1 kb. ⚠️ **les 2 jeux avant/après sont indispensables** · ⚠️ **non comparable à cramino** (4 643 vs 3 808). 1 324 TSV rétrospectifs déjà sur S3. **SEUILS FIXÉS le 2026-08-12** : `1,26` / `1,43` (92,7 % / 2,4 % / 4,9 %), placés dans des **intervalles vides** de la distribution, sans aucun label. ⚠️ **angle mort** : ne voit pas la contamination qu'il filtre (`Breast_6` et `TNE_2` en zone A) → toujours accompagner de `pct_mass_removed`. Les **12 contrôles qualité externes** CGFL sont tous en zone grise (1,329–1,365, masse < 0,2 %) — attendu, ce n'est pas une alerte
- [Palier 1 — candidats écartés](qc-palier1-candidats-ecartes.md) — **MAD ichorCNA** et **`coverage_percent`** instruits sur 1 471 samples puis **écartés** : le MAD ne rejette **rien** que la paire 5 M/0,25× ne rejette déjà (à tous les seuils publiés), `coverage_percent` est `depth` réécrite (corr **0,968** en log). ⚠️ « MAD indépendant de la longueur » est **faux** (corr +0,41). **Ne pas réinstruire.** Corrige aussi 2 lectures du doc : 29/41 des « fragments longs » sont des solides, les « reads de 1-95 pb » font 127-341 pb
- [Google Doc QC — Ratio N50/N75](gdoc-qc-ratio-n50.md) — document de restitution, accès API Docs v1 via credentials gspread (`includeTabsContent=true` obligatoire). Figures 1-2 refaites en **logique autosomes chr1-22** le 2026-08-12. **Réécrit intégralement le 2026-08-12 (soir)** : 9 sections, 5 figures, **5 tableaux**, 3 listes nominatives, ~16 400 car. — ouvre sur `Breast_6`, paragraphes courts + puces, section 8 « qui tombe hors zone verte » (zones + Imagenome + contrôles externes)
- [Module ichorCNA](ichorcna-module.md) — container, panels, gotchas d'installation, `GC-Map correction MAD` dans `params.txt`
- [Module IV](iv-module.md) — sexe + ancestry (18 colonnes), consommé par TOO, hors qualification
- [Check_Input](check-input-qc.md) — QC d'entrée en amont du merge, chemin gracieux input-KO (run SUCCESS + `status=FAILED_QC_INPUT`) ; retrait du rapport PDF (2026-06-23) ; ✅ risque emit levé 2026-07-20
- [bootstrap mVAF v1/v1.4](bootstrap-model-v1.md) — `--bootstrap` (200 scores, 3 sorties) et `--MVAF1_4` rétrospectif ; reproductibilité par seeding interne raima + tri déterministe
- [Rarefaction cascade](rarefaction-cascade.md) — 20M→1M nestés. **GOTCHA** : `samtools view -s` = hash absolu du read-name → seed **incrémenté** par niveau obligatoire
- [Flux small_fragment](small-fragment-flow.md) — filtre 75-200 bp, le BAM filtré se fait passer pour `merged.bam`, cœur inchangé
- [Refactors 2026-05](refactors-2026-05.md) — QC (BAM_Count/Read_ST dans Beta_epic), Raima (3 process → 1), nettoyage code mort
- [Rapport PDF Typst V2](report_pdf_typst_v2.md) — pivot LaTeX → Typst 0.14.2, direction GRAIL Galleri (génération PDF désactivée depuis 2026-06-23)
- [Qualif check-conformity](qualif-check-conformity.md) — refonte 2026-07-22 : 6 étapes, valeur figée inline, Lung_100 retiré, étape 6 non-régression PROD bloquante

## Verified Findings

- **GRCh38 vs hg38** (2026-02-20) : résultats strictement identiques sur Healthy_826, tous scores confondus. Voir [test-results.md](test-results.md)
- **BAM merge** (2026-03-13) : aucune perte de donnée ni métadonnée, 3/3 PASS. BAM horaires 100 % redondants. Voir [bam-merge-verification.md](bam-merge-verification.md)
- **Volumétrie S3** (2026-03-13) : ~186 To au total, ~42,5 To récupérables. Voir [s3-volumetry.md](s3-volumetry.md)
- [Batch effect CGFL vs HCL](batch-effect-investigation.md) — 17 % FP Healthy HCL (V1), CNV biaisé, pas d'effet taille de fragments ; ComBat-met **rejeté**
- [Soft clipping & longueur FRAG](softclip-fragmentomics-length.md) — FRAG = `length(SEQ)`, soft clips inclus ; ne pas migrer vers span référence
- [Coverage CGFL vs HCL](coverage-analysis-cgfl-hcl.md) — couverture autosomale équivalente, trous = non-mappable ; `Healthy_780` per-base corrompu
- [covdepth QC valorization](covdepth-qc-valorization.md) — étape 1 livrée (Fig.1 cumulative + Fig.2 positionnelle) ; finding `067` : 34 M reads alignés pour depth = 0

## Debugging Insights

- [gh release 403](github-release-token.md) — fix `env -u GITHUB_TOKEN gh release ...`
- **Container assigné par `withName:` dans `conf/base.config`**, pas dans le process : tout nouveau process raima sans entrée `withName` hérite du défaut `bam2beta:latest`
- **`raima:latest` doit être rebuild** après modification du Dockerfile, sinon Docker sert l'image cachée. (Historique : raima 0.4.5 casse `Raima_process_CNV`, `depth_per_region` non exportée)
- **Channel vide → emit de sous-workflow qui plante** (NF 25.04) : `No such property: X for DataflowBroadcast` à la CONSTRUCTION. Ne frappe que les emits **jamais consommés**. Voir [check-input-qc.md](check-input-qc.md)
- **`Channel.fromPath` = queue channel à 1 item** (2026-07-16) : limite le process à **une exécution par invocation**. Sans effet en prod (1 sample/run), mais droppe des samples en batch. Fix `.first()`. Posé sur RAIMA_LOYFER + RAIMA_V1_WL ; **subsiste sur RAIMA_MODEL1/2, ANCESTRY_MODEL, BED, FASTA, FAI**. Voir [too-module.md](too-module.md)
- **`checkIfExists: true` dans un `.map` de mode rétro tue TOUT le run batch** (2026-07-22) : exception levée à la construction du channel. Fix : `.filter { … .exists() }` + `log.warn` → skip silencieux. Posé sur THEMELIO_RETRO + TOO_RETRO. ⚠️ **`--bootstrap` et `--METHYL_FEATURES` le gardent encore**
- **Code mort confirmé (2026-08-11)** : `Samtools_qc` et `Nanoplot_qc` (`qc.nf`, bloc commentaire Groovy), `Raima_score_v1_3` et `bootstrap_transfo` (`beta_28M.nf`, plus d'appelant)

## Architecture Notes

- `main.nf` orchestre les modules via conditionals (`params.BETA`, `params.FRAG`, …)
- Channels : `BAM_METADATA` fournit `[sample_id, bam, bai]` à tous les modules
- BED en `/scratch/dependencies/bed/` — ciblent chr1-22+X+Y uniquement
- CNV : bins de 100 kb, filtres de longueur configurables. ⚠️ En liquid/prod `bin_coverage` **ne filtre aucun flag** (seule la longueur 120-400 filtre) ; solid applique `-F 260`
- `raima_score_loyfer.R` : `max_read_len` conditionnel (solid = Inf, liquid = 1000) via `--type`
- `mVAF` renommé `TF` au commit 7837cd0 ; `params.cpu`/`memory` → `cpus_max`/`memory_max` en V1.0.1
- **Le BAM merged est traversé ~4 fois par run rien que pour compter** (BAM_Count, cramino, Extract_read, 22× Preprocess_28M)

## User Preferences

- Communication en **français**, réponses concises avec tableaux de comparaison
- Runs Nextflow depuis `~/Run` ou `~/Run2`, jamais depuis le répertoire du pipeline
- [S3 Never Delete](feedback_s3_no_delete.md) — ne **jamais** supprimer quoi que ce soit sur S3
- [Bash inline dans les process NF](feedback_bash_inline.md) — préférer `script:"""…"""` aux scripts externes `bin/Module/`
- [Versioned template swap](feedback_versioned_template_swap.md) — ne jamais modifier en place un fichier référencé par un workflow actif
