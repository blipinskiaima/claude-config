---
name: restructuration-v2-3-0
description: "V2.3.0 (2026-09-02) — module EXIS (fusion QC+BETA+BETA_28M), raima 0.5.6 latest, metrique amplitude_fragmento_qc + retro, coupe des scores EPIC et du CNV raima, gotchas DSL2 decouverts"
metadata: 
  node_type: memory
  type: project
  originSessionId: 330ade70-5566-438a-a5d4-abcaab9e189a
  modified: 2026-09-02T15:50:33.823Z
---

# Restructuration V2.3.0 (2026-09-01/02)

Menee dans le worktree `~/Pipeline/Bam2Beta-restructuration` (branche `restructuration`),
rapatriee par fast-forward dans `main` le 2026-09-02. TEST OK officiel (Healthy_826 + Lung_9
vs QUALIF V2.2.0). 33 commits, 66 fichiers, +4167/−1139.

## Architecture EXIS

`--EXIS` remplace `QC`+`BETA`+`BETA_28M` (flags supprimes des configs). `workflow/exis.nf` :
`QC_merged` (BAM_Count, BAM_Idxstats, Read_Start_Time, cramino/mosdepth merged, **assemble le
report_input**) → `Beta_epic` (subsampling + BAM EPIC, **sans scores**) → `QC_epic` (cramino
EPIC → `nb_read_epic` mVAF v1.5, seul emit) → `Beta_28M` (Loyfer + `Raima_score_mVAF`).
`Exis` pre-assemble `report_input` (+mvaf14 +raima_version) → `Rapport` a 3 arguments.
Gardes fail-fast en tete de `main.nf` ; TOO requiert EXIS+IV, THEMELIO EXIS+FRAG,
**RAPPORT requiert EXIS+TOO+THEMELIO+FRAG (garde plate) → RAPPORT=false sur solid**.

## Coupe des scores EPIC (BREAKING)

`Modkit_adjust`/`Modkit_pileup`/`Raima_score_epic` commentes dans `beta.nf` → plus de
bedMethyl EPIC, `raima_score.V2`, `V1.2`, `props_v1`, **ni CNV raima** (`score_cnv`/`depths`,
qui vivaient dans le meme process apres fusion). La branche BAM EPIC subsiste UNIQUEMENT pour
le cramino EPIC (v1.5) + publication `merged.epic.bam`. `metadata.json` strictement inchange
(le champ `tf` = mVAF v1.4 vient du 28M). Les 3 fichiers de props :
`BETA/props_v1.tsv` (EPIC ponctuel, v1.0) **coupe** · `BOOTSTRAP/bootstrap_v1.props.tsv`
(16 classes, 200 lignes, source mVAF v1.4, conso TOO/THEMELIO) **conserve** ·
`EXTRACT_FULL_28M/props_loyfer.tsv` (31 classes, 1 ligne) **conserve**.

## raima 0.5.6 = latest + amplitude_fragmento_qc

- Tarball `/mnt/temp/florian/raima_0.5.6.tar.gz`, image locale non poussee sur Docker Hub
  (Hub reste a 0.5.3 — **push en suspens**). 0.5.3/0.5.4 en tags de rollback. Les 6 process
  raima sur `latest`. Les 11 fonctions utilisees verifiees exportees avant bascule.
- `amplitude_fragmento_qc(csv)` : histogramme longueurs 80-600 pb → baseline scam → FFT →
  amplitude max periode 130-200 pb. **Scalaire deterministe.** Refs : Healthy_826 236.0128,
  Lung_9 225.7892, Lung_4 (retro) 216.6840. Sortie `{ID}.amplitude_fragmento_qc.tsv`
  (name/amplitude) dans `Fragmentomics/filtered_softclipped/`. **Hors contrat de qualif**
  (choix Boris). Mode retro `--RETRO_FRAG_AMPLITUDE` : patron MVAF15_RETRO (skip si CSV
  absent, skip si TSV present, `overwrite: false`) ; ⚠ jamais execute en vrai run Nextflow
  (valide via la commande R exacte en docker manuel sur Lung_4).

## Renommages / rangements

`too`→`TOO`, `themelio`→`Themelio`, `rapport`→`Rapport`, `Raima_score_all`→`Raima_score_epic`,
`bootstrap_model`→`Raima_score_mVAF`, `methyl_features`→`Methyl_features` (withName suivis —
critique pour `Raima_score_mVAF`). `bin/bootstrap_model_v1.2.R`→`bin/raima_score_mVAF1.5.R`.
`workflow/BAM/` (small_fragment, rarefaction, rarefaction_horaire), `workflow/ARCHIVES/` +
`bin/archive/` (retros TOO/THEMELIO/MVAF15/METHYL_FEATURES/bootstrap sortis du code vivant —
**params subsistent sans effet**). Scissions `BAM_Count`/`BAM_Idxstats`,
`Extract_read`/`Ratio_N50_N75`. Le log " ✓ Version raima" vient de `Raima_score_mVAF`.
`MERGE=false` : retour au patron simple SANS filter (echec franc si BAM absent — batchs =
listes propres obligatoires).

## Gotchas Nextflow decouverts

- **L'ordre d'ECRITURE des invocations suit les dependances** : `X.out` n'est referencable
  qu'apres la ligne `X(...)` — 2 crashs vecus (`QC_merged.out` dans exis.nf, `IV.out` dans
  main.nf apres reagencement en sections). L'ordre d'execution reel reste dataflow.
- **Un fichier .nf ne peut PAS s'auto-inclure** (`include ... from './qc.nf'` dans qc.nf) :
  le lint (parser v2) accepte, le runtime (parser v1) plante `parsing failed`.
- **Deux workflows DISTINCTS peuvent chacun invoquer le meme process** (instances
  namespacees W1:P / W2:P) — c'est ce qui a permis de fusionner qc_process.nf dans qc.nf
  (QC_merged et QC_epic partagent Mosdepth_qc/Cramino_qc sans alias).
- **`--help` ne valide que le parse**, pas la construction du DAG (les erreurs "not invoked
  before accessing" surviennent apres l'exit 0 du help).
- **ichorCNA est non-deterministe de quelques octets** entre runs (cna.seg, correctedDepth,
  log) mais TFx/ploidy identiques — motif a connaitre pour les comparaisons bit-a-bit.
- Le hook `pretool-bash-guard` (regle 9) lit le **cwd de session** (pas le `cd` de la
  commande) : lancer nextflow via un script lanceur ecrit avec Write, ou `cd` en appel separe.

## En suspens apres release

- `docker push blipinskiaima/raima:latest` + `:0.5.6` (Hub a 0.5.3, divergence si autre noeud)
- Tarball 0.5.6 → `s3://aima-resources/raima-model/` (n'existe que sur /mnt/temp/florian)
- Token Tower en dur dans `nextflow.config:59` (golden rule, preexistant)
- Backfill amplitude des ~1500 samples RetD via `--RETRO_FRAG_AMPLITUDE` (glob batch valide
  sur le papier, a exercer sur 2-3 samples d'abord)
- Lung_4 n'est plus testable from-scratch (BAM horaires purges, comme Breast_28/Breast_6)
