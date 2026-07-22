# Context — Bam2Beta — 2026-07-22T14:06:06+0000

**Branche** : main
**Dernier commit** : 7e7d90e — feat(too): mode retrospectif --TOO_RETRO (miroir de --THEMELIO_RETRO)
**Status** : clean (0 fichier modifié)

## Où j'en suis
Ajout du mode rétrospectif **`--TOO_RETRO`** (miroir strict de `--THEMELIO_RETRO`) : score TOO
depuis les 4 sorties déjà sur S3, sans recalcul. **Terminé, vérifié au lint, commité et poussé**
(7e7d90e). En amont, fix de `THEMELIO_RETRO` (crash sur input manquant) commité séparément
(4d9fcdb). Chantier clos.

## Ce qui marche / ce qui foire
- ✓ **`--TOO_RETRO`** : bloc `if (params.TOO_RETRO)` dans main.nf (4 fichiers : bootstrap props +
  Loyfer + raima_score.V1.4 + `IV/sex.tsv`), includes `TOO_build_input`/`TOO_score`, param dans
  nextflow.config. Réutilise les process de too.nf tels quels, écrit uniquement dans `TOO/`.
- ✓ **fix `THEMELIO_RETRO`** : `checkIfExists: true` → `.filter { .exists() }` + `log.warn` →
  skip silencieux des samples incomplets au lieu de tuer tout le run batch.
- ✓ **Vérif lint NF 25.04** : +0 erreur (13 avant = 13 après), +1 warning de style préexistant.
- ✓ Doc à jour : CLAUDE.md (params `--TOO_RETRO` + `--THEMELIO_RETRO` oublié), MEMORY.md (gotcha checkIfExists).
- ✗ **Pas encore testé sur un vrai run rétrospectif** (prod S3 — Boris garde la main).
- ⚠ **`--bootstrap` et `--METHYL_FEATURES` gardent `checkIfExists: true`** → même crash possible en batch multi-samples (candidats au même fix).

## Prochaine étape
Optionnel : lancer un vrai run `--MERGE false --TOO_RETRO` depuis `~/Run` sur un batch de samples
ayant déjà leurs sorties S3, pour valider en conditions réelles. Sinon, appliquer le même skip-silencieux
à `--bootstrap` / `--METHYL_FEATURES`.
