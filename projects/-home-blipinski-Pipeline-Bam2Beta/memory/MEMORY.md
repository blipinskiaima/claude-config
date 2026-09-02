# Bam2Beta Project Memory

## Key Facts

- **Version courante : V2.3.0** (2026-09-02) — restructuration EXIS (fusion QC+BETA+BETA_28M), raima **0.5.6 = latest**, métrique `amplitude_fragmento_qc` (+ rétro), **BREAKING** : scores EPIC (bedMethyl/V2/V1.2/props_v1) et CNV raima coupés, `RAPPORT=false` sur solid. TEST OK vs QUALIF V2.2.0. Voir [restructuration-v2.3.0.md](restructuration-v2.3.0.md)
- Historique : **V2.2.0** THEMELIO + metadata.json contrat unique ([themelio-module.md](themelio-module.md)) · **V2.1.0** TOO ([too-module.md](too-module.md)) · **V2.0.x** tf = mVAF v1.4 bootstrap, tri déterministe ([bootstrap-model-v1.md](bootstrap-model-v1.md))
- Containers : `bam2beta:latest` + `raima:latest` (**0.5.6** depuis V2.3.0, locale non poussée ; 0.5.3/0.5.4 en rollback) + `too:0.4.1` + `themelio:1.0.0`. ⚠️ Scripts R de TOO hors image (chargés via `${projectDir}`)
- Modules (V2.3.0) : MERGE, **EXIS**, FRAG (+ amplitude), CNV (log2ratio seul), ICHORCNA, IV, MITO, TOO, THEMELIO, RAPPORT, RETRO_FRAG_AMPLITUDE, SMALL_FRAGMENTS, RAREFACTIONS, RAREFACTION_HORAIRE
- **Prod** active : MERGE + EXIS + FRAG + CNV + IV + TOO + THEMELIO + RAPPORT + MITO. ⚠️ `ICHORCNA=false` en prod mais **true en liquid/solid** (lanceurs `dev/SCW/` sans `prod`)
- Retry : doublement CPU/RAM par tentative, plafond `cpus_max`/`memory_max`

## Modules — fiches détaillées

- [Restructuration V2.3.0](restructuration-v2.3.0.md) — EXIS, coupe EPIC, raima 0.5.6, amplitude + rétro, renommages, gotchas DSL2, points en suspens (docker push, tarball S3, backfill amplitude)
- [mVAF v1.5](mvaf-v1.5.md) — v1.4 corrigée par la couverture EPIC, déployée 1 362/1 362 liquides. ⚠️ `nb_read_epic` en MILLIONS ; Healthy_826 sature la correction
- [Cascade de comptage des reads](read-counting-cascade.md) — 4 strates A/B/C/D, table de vérité, matérialisée en base `qc` v23 ; le seuil « > 97 % mapping » de la littérature RÉFUTÉ
- [Comptage 28M et CpG](reads-28m-cpg-counting.md) — `uniq+skipped` ±0,002 %, backfill 1 506 samples, ~35 % des reads 28M sans CpG ; ⚠️ clé TYPE+LABO+ID
- [QC primaire / QC contributif](qc-deux-niveaux.md) — architecture 2 niveaux (5 M / 4 M), non implémentée ; seuil 5 M appliqué nulle part sauf Aima-Tower
- [metadata.json](metadata-json.md) — provenance des champs, 2 constructeurs exclusifs, gotcha `status` absent = OK
- [Module TOO](too-module.md) — vendoring vs wrapper, seuils dans le bundle, parse quote-aware
- [Module MITO](mito-module.md) — 11 colonnes, mosdepth merged non filtré ; ⚠️ V2.3.0 : requiert EXIS, mode rétro retiré
- [Figure distribution de longueur](length-distribution-figure.md) — PNG vs 3 références, pondéré par la MASSE d'ADN
- [QC N50/N75](n50-ratio-qc.md) — détecteur de contamination gDNA, seuils 1,26/1,43 + masse 22 %, grille croisée, backfill `dev/archive/backfill_n50_ratio.sh`, câblage trace-prod v22/v24
- [Onglet Synthèse — 5 QC liquid](gdoc-synthese-qc.md) — 1 324 samples, cascade → 1 168 conformes (88,2 %) ; 3 métriques à apport net NUL, ne pas réinstruire
- [Palier 1 — candidats écartés](qc-palier1-candidats-ecartes.md) — MAD ichorCNA et coverage_percent écartés, ne pas réinstruire
- [Fano — homogénéité de couverture](fano-couverture-qc.md) — Fano EPIC : 48 outliers dont 47 invisibles aux seuils actuels ; génomique brut inutilisable
- [Recensement QC Lung_Alc](lung-alc-qc-recensement.md) — 226 samples, 94,2 % conformes ; texte final retravaillé par Boris
- [Google Doc QC](gdoc-qc-ratio-n50.md) — accès API Docs (gspread + requests), ⚠️⚠️ `tabId` obligatoire dans chaque batchUpdate
- [Module ichorCNA](ichorcna-module.md) — container, panels, MAD dans params.txt ; ⚠️ non-déterministe de quelques octets entre runs (TFx stable)
- [Module IV](iv-module.md) — sexe + ancestry, consommé par TOO, hors qualification
- [Check_Input](check-input-qc.md) — QC d'entrée, chemin gracieux input-KO (SUCCESS + `FAILED_QC_INPUT`)
- [bootstrap mVAF v1/v1.4](bootstrap-model-v1.md) — reproductibilité (tri déterministe + seeding raima) ; retro archivé en V2.3.0
- [Rarefaction cascade](rarefaction-cascade.md) — GOTCHA : seed incrémenté par niveau obligatoire (`samtools -s` = hash absolu)
- [Flux small_fragment](small-fragment-flow.md) — BAM filtré 75-200 se fait passer pour merged, cœur inchangé
- [Refactors 2026-05](refactors-2026-05.md) — QC/Raima refactors, code mort (purgé en V2.3.0)
- [Rapport PDF Typst V2](report_pdf_typst_v2.md) — pivot Typst, génération désactivée depuis 2026-06
- [Qualif check-conformity](qualif-check-conformity.md) — 6 étapes, valeurs figées inline, étape 6 non-régression PROD bloquante

## Verified Findings

- [GRCh38 vs hg38](test-results.md) — résultats identiques sur Healthy_826 (2026-02-20)
- [BAM merge](bam-merge-verification.md) — aucune perte, BAM horaires 100 % redondants (3/3 PASS)
- [Volumétrie S3](s3-volumetry.md) — ~186 To, ~42,5 To récupérables (2026-03-13)
- [Batch effect CGFL vs HCL](batch-effect-investigation.md) — 2 causes racines (EPIC→ONT + kit extraction) ; ComBat-met rejeté
- [Soft clipping & longueur FRAG](softclip-fragmentomics-length.md) — FRAG = length(SEQ) − softclips depuis V1.3.2
- [Coverage CGFL vs HCL](coverage-analysis-cgfl-hcl.md) — couverture équivalente, trous = non-mappable
- [covdepth QC valorization](covdepth-qc-valorization.md) — Fig.1/2 livrées ; finding 067 requalifié (reads non alignées)
- [Reads non alignés des urines](unmapped-reads-urines.md) — 2 populations, 6 espèces bactériennes, souches distinctes → pas une contamination labo ; référence d'alignement = MinKNOW/GRCh38 no_alt (PAS le hg38 UCSC des modules)

## Debugging Insights

- [Gotchas outils & debugging](debugging-gotchas.md) — withName/containers, channels NF (fromPath 1 item, emit vide, checkIfExists rétro), s3fs vs aws cp, bedtools -sorted karyotypique, mosdepth options, index plus vieux que les BAM, 75 sample_name dupliqués, unités trace-prod, kraken2
- [Gotchas DSL2 V2.3.0](restructuration-v2.3.0.md) — ordre de déclaration des invocations, auto-include interdit, 2 workflows partagent un process, `--help` ≠ DAG, hook pretool cwd
- [gh release 403](github-release-token.md) — fix `env -u GITHUB_TOKEN gh release ...`

## User Preferences

- Communication en **français**, réponses concises ; [réponses courtes dans le chat](feedback_reponses_courtes.md) — les longs messages le font décrocher
- Runs Nextflow depuis `~/Run*`, jamais depuis le répertoire du pipeline
- [S3 Never Delete](feedback_s3_no_delete.md) — ne **jamais** rien supprimer sur S3
- [Bash inline dans les process NF](feedback_bash_inline.md) — `script:"""…"""` plutôt que scripts externes
- [Versioned template swap](feedback_versioned_template_swap.md) — jamais modifier en place un fichier référencé par un workflow actif
- [Google Doc — jamais de réécriture de section](feedback_gdoc_no_overwrite.md) — remplacements de chaînes exactes uniquement (incident 2026-08-14)
- [Concision dans les docs de restitution](feedback_doc_concision.md) — une case incomprise se retire, ne se ré-explique pas
