---
name: project-rename-nb-lignes-molecule-cols
description: "Sept. 2026 — renommage des colonnes DuckDB nb_reads_total → nb_lignes_total et nb_reads_aligned → nb_molecule (14 colonnes, 7 tables). ⚠⚠ Un sed global sur le dépôt réécrit l'intérieur de la migration elle-même et la transforme en no-op SILENCIEUX. ⚠ Les noms de fichiers S3 {s}.nb_reads_total.tsv ne se renomment pas."
metadata:
  node_type: memory
  type: project
---

# Renommage `nb_reads_total` / `nb_reads_aligned` (08/09/2026)

Colonnes DuckDB renommées **`nb_reads_total` → `nb_lignes_total`** et
**`nb_reads_aligned` → `nb_molecule`** (sans accent : un accent obligerait à quoter la colonne
partout). Aligne le nom technique sur les étiquettes d'export adoptées en septembre —
lesquelles **ne changent pas** (`Nb lignes total` / `Nb molécule`, cf
[[project_rename_labels_nb_lignes_molecule]], qui n'avait touché que les libellés).

**14 colonnes, 7 tables** : `qc_metrics` + les suffixées de `small_fragments_metrics`,
`dilution`, `dilution_lung`, `rarefaction`, `rarefaction_horaire`,
`rarefaction_horaire_threshold`. ⚠ `dilution_lung` manquait à la liste initiale — la table v33
est récente ; **recenser les colonnes en base (`information_schema`) plutôt que se fier à une
liste de tables donnée de mémoire**.

## ⚠⚠ Le piège central : le sed mange sa propre migration

La pré-migration `_migrate_reads_columns_rename()` contient nécessairement les **anciens** noms
(`LIKE 'nb_reads_total%'`, `col.replace('nb_reads_total', …)`). Le renommage automatique appliqué
ensuite sur tout le dépôt les a réécrits en **nouveaux** noms :

```python
LIKE 'nb_lignes_total%'                       # ne matche plus rien
col.replace('nb_lignes_total','nb_lignes_total')
```

→ **no-op parfaitement silencieux** : aucune exception, aucun message, la commande s'exécute
normalement et la base n'est **jamais** migrée. Découvert par le contrôle de non-régression
(`Binder Error: column "nb_lignes_total" not found`), pas par l'exécution.

**Règle** : la fonction de migration est le **seul endroit du dépôt** où l'ancien nom doit
survivre. L'exclure explicitement du remplacement, ou la relire après. Un avertissement est
désormais inscrit dans sa docstring.

## ⚠ Les noms de FICHIERS ne se renomment pas

13 occurrences protégées par le motif `nb_reads_total(_filtered_softclipped)?\.tsv` :
`QC/Samtools/{s}.nb_reads_total.tsv` (checkers.py:606, checkers_qc.py:111) et
`{s}.nb_reads_total_filtered_softclipped.tsv` (checkers_qc.py:114) + mentions en commentaires et
README. **Ces fichiers sont produits par Bam2Beta** — trace-prod ne contrôle pas leur nom, les
renommer casse la lecture S3. Toujours stasher les motifs de chemins avant un sed d'identifiants.

## Autres points

- **`ALTER TABLE … RENAME COLUMN` préserve PK, FK et NOT NULL** (revérifié : 19 contraintes
  identiques). La règle d'or « `CREATE TABLE AS SELECT` perd les PK/FK » ne s'applique pas —
  même conclusion qu'en [[project_schema_v27_small_fragments]].
- **Pré-migration placée AVANT les `CREATE TABLE IF NOT EXISTS`**, comme v27. Générique : une
  requête `information_schema` + une boucle, plutôt que 14 `ALTER` en dur.
- `nb_reads_epic` (7 colonnes) **n'est pas concernée** — ne matche aucun des deux préfixes.
  La table `qc` (`reads_total`, `reads_frag`…) non plus : noms sans préfixe `nb_`.
- **Non touchés** (choix assumés) : `docs/superpowers/` (64 occurrences, archives de conception
  datées — même traitement qu'en v27), le worktree `.claude/worktrees/`, et les étiquettes
  d'import anciennes `"Nb reads total"` / `"Nb read alignés"` (seules leurs *valeurs* changent).
- **`SCHEMA_VERSION` volontairement PAS bumpé** (reste à 33) : la v33 `dilution_lung` appartient
  à une session parallèle non commitée, bumper aurait risqué le télescopage v23/v24 documenté
  dans [[project_schema_v24_pct_mass_removed]].

**Non-régression prouvée** : 9 275 lignes comparées **ligne à ligne** contre le backup
(0 écart sur les 14 colonnes), 19 contraintes identiques, 1 512 samples d'export identiques,
11 exports lancés sans erreur. 159 identifiants renommés dans 15 fichiers.
Backup `samples_status.backup-pre-rename-reads-cols-20260908_111742.duckdb`.
