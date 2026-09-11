# Context — trace-prod — 2026-09-11T09:54:04+00:00

**Branche** : main
**Dernier commit** : 2444113 — docs: schema v32 — état final du lot threshold + gotcha BAM périmé
**Status** : propre (untracked inchangés : backups .duckdb, CSV dev/, rapports HTML, metadata_HCL.tsv)

## Où j'en suis
Schema v32 (`rarefaction_horaire_threshold`) terminé et le lot est **clos** : 1620 lignes
(456 CGFL / 1164 HCL, 405 bases × 4 paliers), PROD/mVAF/epic/Loyfer à **1620/1620**, les
2 onglets de la gsheet dédiée `1FG4KfL4…` à jour. 9 passes `check` + export du 03 au 09/09
ont accompagné la montée en charge (308 → 1620). Doc README + CLAUDE.md remises à niveau et
poussées. Rien en attente côté code.

## Ce qui marche / ce qui foire
- ✓ Table complète, 0 valeur manquante ; 0 fantôme `LOG`, 0 base incomplète, 0 ligne sans
  parent dans `samples`, 92 collisions inter-labo conservées par la PK composite
- ✓ Relecture gsheet ↔ base à chaque passe : **0 cellule divergente** (25 920 + 82 620 valeurs)
- ✓ Aucune duplication de code : le checker importe `_bootstrap_means` et `_read_props`, les
  2 exports réutilisent `_export_rarefaction_horaire`
- ✗ **`Lung_77_20M` reste périmé** : BAM réécrit le 09/09 à 13:02, BOOTSTRAP du 09/09 à 03:15
  → ses 12 valeurs sont calculées sur un autre tirage. **Aucun `NA` ne le signale**, c'est le
  cas dangereux du gotcha. Les 11 autres pseudo-samples des 3 bases relancées sont sains
- ✗ Piège systémique : un BAM re-sous-échantillonné rend son aval périmé et **trace-prod ne
  peut pas le détecter** (il lit des fichiers, pas leurs dates relatives)
- ✗ Contention DuckDB régulière avec les sessions parallèles (dilution_lung, Twist) —
  single writer, mes vérifs ont dû attendre le lock jusqu'à 75 s

## Prochaine étape
Relancer l'aval Bam2Beta sur `Lung_77_20M` (décision Boris), puis
`check-rarefaction-horaire-threshold HCL -s Lung_77_20M` + les 2 exports — commandes prêtes,
même schéma que les recheck ciblés de cette session.
