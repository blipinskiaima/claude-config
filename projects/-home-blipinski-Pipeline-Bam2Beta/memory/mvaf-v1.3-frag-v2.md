---
name: mvaf-v1-3-frag-v2
description: V1.3.2 - score mVAF v1.3 (retrospectif --MVAF1_3) + migration fragmentomics v2 (softclip-removed) + pattern backfill QUALIF retrospectif
metadata: 
  node_type: memory
  type: project
  originSessionId: ffb7e039-3b1b-4757-bc29-445dd460ad09
---

# V1.3.2 (2026-06-05) — mVAF v1.3 + fragmentomics v2

## Score mVAF v1.3

- Script `bin/raima_score_v1_3.R` : 2 appels separes a `raima::model_v1(files, radii=1:100, tgz_model_v1_data=whitelist)`
  - 1er appel -> `${ID}.${DEPTH}.epic.raima_score.V1.3.tsv` (mVAF)
  - 2e appel `return_all_props=TRUE` -> `${ID}.${DEPTH}.epic.props_v1.3.tsv` (16 classes EPIC)
  - `files` = vecteur des 22 bedMethyl_28M (model_v1 accepte un vecteur en 0.5.0)
- Process `Raima_score_v1_3` defini dans `workflow/beta_28M.nf`, container raima:latest (withName dans conf/base.config)
- Param `raima_model_v1_whitelist = ${dependencies}/raima-model/model_v1_data_whitelist.tsv.gz` (230 MB)
- Outputs dans BETA/ avec prefixe `.epic.` (convention EPIC, pas .merged.all. du 28M) — choix Boris assume
- N'ecrase rien : noms `.V1.3`/`.props_v1.3` distincts de `.V2`/`.V1.2`/`props_v1`

### Deux chemins d'execution
1. **from-scratch** : `--BETA_28M true` -> Beta_28M calcule les bedMethyl puis appelle Raima_score_v1_3
2. **retrospectif** : `--MVAF1_3 true` -> collecte les 22 bedMethyl deja sur S3 (`${output}/${ID}/BETA_28M/${ID}.merged.all.chr{1..22}.bedMethyl.gz`), aucun recalcul. Process importe dans main.nf, collecte via `BAM_PATH.map` + `file(checkIfExists:true)` (calque fallback BAM merged ligne 147)
- **Limite (simple par choix)** : `RAIMA_V1_WL` est un channel queue -> 1 sample par run retrospectif. Multi-sample necessiterait `.collect()`. Meme limite que loyfer.
- Validation : run `--BETA_28M true` Healthy_826 CGFL liquid, mVAF=2.581, props somme≈1, 71 process OK

## Fragmentomics v2 (softclip-removed)

- `bin/fragmentomics_score.R` : `fragmento_model_v1` -> `fragmento_model_v2`, `plot_dist_lengths(softclip_removed=TRUE)`
- `workflow/frag.nf` : output renomme `${ID}.fragmentomics_score.V2.tsv`, publishDir `Fragmentomics/filtered_softclipped/` (remplace `filtered/`)
- **v2 remplace v1** : l'ancien `filtered/.tsv` disparait du contrat de sortie
- Format de sortie change : v1 = 1 valeur brute (~-158.9), v2 = header `score\tmodel` + `-0.0682...\tfragmento v2`
- Migration complete : `conformity/check-run-output.sh`, `check-conformity.sh` (valeur ref `-0.0682464198886691`), `check_samples_status.sh`, `dev/PLT/Bam2Beta_SCW_plateforme.sh`, doc (README/CLAUDE/overview)

### Gotcha rencontre
- Le 1er `/test-bam2beta` a plante a l'ETAPE 1 : `frag.nf` produisait `.V2.tsv` (via `-o`) mais le bloc `output:` attendait encore `.tsv` -> "Missing output file". Fix : aligner le `path()` du output sur `.V2.tsv`.

## Pattern reutilisable : backfill QUALIF retrospectif

Quand un changement de contrat de sortie (renommage/dossier) casse la comparaison vs QUALIF :
- **Ne pas** tolerer un WARNING dans check-conformity, **backfiller** le nouveau fichier DANS la QUALIF de reference via un run retrospectif
- Ex : `--MERGE false --FRAG true --output s3://...QUALIF/V1.3.1` lit le BAM merged existant de la QUALIF et genere le frag v2 dedans (13s)
- N'ecrase rien (le nouveau dossier `filtered_softclipped/` n'existe pas encore), l'ancien `filtered/` reste intact -> conforme regles S3
- Resultat : `/test-bam2beta` TEST OK 3/3, frag v2 bit-a-bit identique entre run et QUALIF backfillee
- Wrapper : `dev/SCW/backfill_frag_v2_qualif_V1.3.1.sh` (untracked)

## Validation finale
- `/test-bam2beta` Healthy_826 CGFL liquid : **TEST OK** (ETAPE 1+2+3, fragmento_score.V2 IDENTIQUE a PROD)
- 3 commits : feat(mvaf) bdb984d, feat(frag) 06b2f67, chore(raima 0.5.0) 7d09cc6
