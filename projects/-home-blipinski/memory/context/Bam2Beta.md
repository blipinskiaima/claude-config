# Context — Bam2Beta — 2026-09-28 14:25

**Branche** : main
**Dernier commit** : 777aa9b — fix(prod): plafonner un run plateforme a 6h
**Status** : clean (2 non suivis : pair_current.tsv, qualifStatus.txt — résidus de run)

## Où j'en suis

Deux versions livrées et qualifiées d'affilée. **V2.3.1** : inventaire des 14 commits
depuis V2.3.0, diagnostic du warning Seqera de fin de run. **V2.3.2** : recalibrage du
profil `prod` sur la machine de production (8 cpus / 32 Go) après l'échec
`req: 40 GB; avail: 31.3 GB` sur BAM_sort. Les deux qualifiées 54/54, releases publiées,
`QUALIF/V2.3.2` est la référence. Le 28/09, ajout d'un `timeout 6h` sur le lanceur
plateforme après le run figé AIMA_013.

## Ce qui marche / ce qui foire

- ✓ `--ncores` 4→8 **prouvé sans effet** sur raima : 200 scores bootstrap identiques au
  `cmp`. Lève le ⚠ « A/B non fait » qui traînait dans `ressources-dimensionnement`
- ✓ Warning Seqera élucidé : script de `Raima_report` à 14 755 car. contre un plafond
  `tasks.script = 10240` du plugin nf-tower. **Déjà corrigé** par le refactor `csv_to_kv`
  (7858fe7) — 0 ligne à écrire, confirmé absent des 4 runs de validation
- ✓ Cause racine de la panne prod : le right-sizing V2.3.1 avait été calibré sur le serveur
  de calcul (32c/125 Go) et appliqué au profil de la plateforme. Leçon écrite dans CLAUDE.md
  et `ressources-dimensionnement`
- ✗ Le commentaire d'en-tête de `prod.config` disait déjà « CPU max 8, RAM max 32GB » — il
  n'avait pas été lu avant de remonter les plafonds
- ⚠ `Raima_process_loyfer` reste à 14 Go pour 16 alloués (87 %), inchangé dans les 3
  versions — le plus tendu du pipeline, cédera en premier sur un sample hors norme
- ⚠ Les tags `pre-*` locaux sont partis sur GitHub avec le `git push --tags`
- ⚠ `Modkit_adjust`, `Modkit_pileup`, `Raima_score_epic` toujours définis dans `beta.nf`
  sans appelant depuis V2.3.0 (les autres retraits sont dans `workflow/ARCHIVES/`)

## Prochaine étape

Rien de bloquant. Deux points ouverts au choix : retirer les tags `pre-*` du remote, et
archiver les 3 process EPIC morts dans `workflow/ARCHIVES/`.
