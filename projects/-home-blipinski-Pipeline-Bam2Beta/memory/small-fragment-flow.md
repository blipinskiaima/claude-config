---
name: small-fragment-flow
description: "Flux small_fragment (ex short_read) - strategie ultra-simple 2-temps (BAM filtre 75-200 se fait passer pour merged.bam dans CGFL_small_fragments, coeur pipeline inchange). Rename SHORT_READ->SMALL_FRAGMENTS commit d6d4556. Gotcha stageAs collision. TODO rename S3. Phase 2 (v1.3/v1.4/bootstrap) bloquee par 28M merged-hardcode."
metadata: 
  node_type: memory
  type: project
  originSessionId: f4459926-e806-4050-9be4-f1985b4f7380
---

# Flux small_fragment (renommage de short_read, 2026-06-25)

Flux **parallèle** au flux prod (liquid/solid) pour analyser les reads courts 75-200 bp.
Renommage complet `short_read` → `small_fragment`, **R&D, non qualifié**.

## Stratégie retenue : ULTRA-SIMPLE, 2 temps, cœur inchangé

Décision Boris (après avoir rejeté 2 approches plus invasives : chaînage in-line + paramétrage
`depth_ref`). Le principe : **le BAM filtré se fait passer pour le `merged.bam`** dans une arbo
S3 dédiée `CGFL_small_fragments`. Le pipeline ne voit aucune différence → **zéro modif du cœur**
(`beta.nf`, branches merge/rétro de `main.nf` intactes ; `merged` jamais paramétré).

```
TEMPS 1 — run filtre SEUL (module Small_Fragment)
  --input  .../RetD/liquid/CGFL/${ID}     --output .../RetD/liquid/CGFL   --MERGE false --SMALL_FRAGMENTS true
  → lit le merged.bam PROD (via branche rétro existante, depuis --output=CGFL)
  → publie ${ID}.merged.bam (filtré 75-200) dans ${output}_small_fragments/${ID}/BAM/  = CGFL_small_fragments/

TEMPS 2 — pipeline rétro INCHANGÉ sur la nouvelle arbo
  --input  .../CGFL_small_fragments/${ID}  --output .../CGFL_small_fragments  --MERGE false --BETA true --ICHORCNA true
  → lit ${output}/${ID}/BAM/${ID}.merged.bam (= le filtré), tourne normalement, tag "merged"
```

Conséquence assumée : sorties nommées `.merged.` (pas `.minLen75_maxLen200.`). La traçabilité
small_fragment vient **du chemin S3** (`CGFL_small_fragments`), pas du nom de fichier.
`metadata.json` + `Raima_process_CNV` tournent (tag=merged) sauf si coupés via flags.

## Implémentation (commit d6d4556)

- Tag rollback **`pre-small-fragment`** (sur 5d6e1b0) avant la feature.
- `workflow/short_read_filter.nf` → `workflow/small_fragment.nf` (git mv).
- workflow `Short_Read_Filter`→`Small_Fragment`, process `Filter_Short_Reads`→`Small_Fragment_Filter`.
- flag `params.SHORT_READ`→`SMALL_FRAGMENTS` (nextflow.config, conf/{base,prod,liquid,solid}.config, main.nf).
- `publishDir "${params.output}_small_fragments/${ID}/BAM"`, sortie `${ID}.merged.bam`.
- **Gotcha collision** : la sortie `${ID}.merged.bam` et l'entrée (merged.bam prod) ont le même nom →
  samtools `-o` tronque l'entrée. Fix : `path(BAM, stageAs: 'source.merged.bam')` + lire `source.merged.bam`.
- `CHANGELOG.md` historique laissé intact (rename uniquement dans le code vivant + CLAUDE.md).
- **Temps 1 testé OK** sur Bladder_Blood_01_001 (Boris, 2026-06-25). Pas de profil dédié (flags CLI).

## TODO (sous contrôle Boris)

- **Rename S3** `CGFL_short_read` → `CGFL_small_fragments` : **copy d'abord, jamais delete** (règle d'or S3).
  L'ancien run S3 `CGFL_short_read/Bladder_Blood_01_001` (mai 2026) contenait v1/v1.2/v2 + ichorCNA + CNV
  + REPORT(pdf), tag `minLen75_maxLen200`, issu d'une édition destructive du pipeline depuis revertée.
- Export trace-prod existant vers la gsheet **Small Fragments**.

## Phase 2 différée — v1.3 / v1.4 / bootstrap (BLOQUÉE par couplage 28M)

Boris veut à terme ajouter mVAF v1.3 + v1.4/bootstrap au small_fragment. **Bloqueur connu** :
le sous-système 28M ([beta_28M.nf]) est **hardcodé `merged`** à 4 niveaux (filtre l.26, groupTuple
qui DROP le DEPTH, noms de sortie `.merged.` dans bootstrap_model + `raima_score_loyfer.R` l.19 qui
RECONSTRUIT les chemins `.merged.all.chr*.bgzf`). L'ancien run short_read n'avait d'ailleurs PAS de
28M. Avec la stratégie "masquerade" (tag=merged), ça marcherait sans modif — mais il faut décider si
on coupe loyfer/metadata/Raima_process_CNV. Voir [[bootstrap-model-v1]].
