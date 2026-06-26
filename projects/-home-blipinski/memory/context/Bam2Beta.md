# Context — Bam2Beta — 2026-06-26T07:46:51+0000

**Branche** : main
**Dernier commit** : d6d4556 — refactor(small_fragment): renomme flux short_read -> small_fragment + module filtre Temps 1
**Status** : clean côté pipeline (seuls dev/SCW/launch_SCW.sh modifié + bacasable.sh untracked, sandbox)

## Où j'en suis
Flux **small_fragment** (ex short_read) — rename complet committé+pushé (d6d4556, R&D non qualifié).
Stratégie **ultra-simple 2-temps** : le BAM filtré 75-200 bp se fait passer pour `merged.bam` dans
l'arbo `CGFL_small_fragments`, **cœur du pipeline strictement inchangé** (beta.nf + branches merge/rétro
intactes, `merged` jamais paramétré). Temps 1 (run filtre seul) testé OK sur Bladder_Blood_01_001.

## Ce qui marche / ce qui foire
- ✓ Rename `SHORT_READ`→`SMALL_FRAGMENTS` + `Short_Read_Filter`→`Small_Fragment` + fichier→`small_fragment.nf`, parse Nextflow OK
- ✓ Temps 1 : `--MERGE false --SMALL_FRAGMENTS true`, lit merged.bam prod, publie `${ID}.merged.bam` dans `${output}_small_fragments/` — testé OK
- ✓ Gotcha collision résolu : input stagé `stageAs: 'source.merged.bam'` (sinon samtools -o tronque l'entrée)
- ✓ CHANGELOG historique laissé intact ; CLAUDE.md + mémoire à jour
- ✗ Temps 2 (pipeline rétro BETA+ichorCNA sur la nouvelle arbo) **pas encore lancé** — attendre baisse du load serveur (était à ~546/32 cœurs)
- ✗ Rename S3 `CGFL_short_read`→`CGFL_small_fragments` **non fait** (copy only, jamais delete — sous contrôle Boris)

## Prochaine étape
Lancer le **Temps 2** sur Bladder_Blood_01_001 (`--input .../CGFL_small_fragments/${ID} --output .../CGFL_small_fragments --MERGE false --BETA true --ICHORCNA true`) quand le load serveur sera retombé, puis vérifier les sorties. Phase 2 (v1.3/v1.4/bootstrap) différée (bloquée par hardcode `merged` du 28M).
