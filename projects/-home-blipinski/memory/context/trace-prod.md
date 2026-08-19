# Context — trace-prod — 2026-08-19T13:26:56+00:00

**Branche** : main
**Dernier commit** : 151e4ff — feat: schema v25 — qc.reads_with_cpg + alimentation ponctuelle 28M/CpG
**Status** : propre, synchronisé avec origin/main (untracked : backups .duckdb, CSV dev/, rapports HTML, .claude/skills-worktrees — inchangés depuis avant la session)

## Où j'en suis
Tâche terminée de bout en bout : ajout de `qc.reads_with_cpg`/`reads_with_cpg_pct` (schema v25) +
alimentation ponctuelle des 4 champs 28M/CpG depuis un backfill TSV rétrospectif
(`/scratch/boris/nb_read_28M/nb_reads_28M.tsv`). Export gsheet fait, doc (README Table 11 + CLAUDE.md)
et mémoire à jour, commit pushé.

## Ce qui marche / ce qui foire
- ✓ 1332/1506 lignes du TSV alimentées (819 CGFL + 513 HCL liquid) — vérifié sample par sample
  (Bladder_Blood_01_101, Healthy_826, Lung_9 CGFL/HCL homonyme, Lung_1_rebasecalled) : brut et %
  identiques au TSV/formule attendue
- ✓ Export `export-qc` → onglet 'QC read' : 1362 lignes, 16 colonnes, contrôle croisé TSV local OK
- ○ Exclus volontairement, sans écriture : 147 solid CGFL (table `qc` structurellement liquid-only)
  + 27 liquid CGFL `Bladder_Urine_02_*` (jamais passés par `check-qc`, donc pas de `reads_total`)
- ○ `checkers_qc.py`/`check-qc`/`update-column` volontairement PAS câblés sur ces 2 champs — décision
  explicite de Boris (pas de procédure automatisée tant que Bam2Beta ne publie pas ces comptages)

## Prochaine étape
Aucune action immédiate requise — tâche fermée. Si Boris veut compléter les 27 `Bladder_Urine_02_*` :
lancer `check-qc liquid CGFL` dessus (remplit `reads_total`), puis rejouer une alimentation ciblée
depuis `nb_reads_28M.tsv` pour ces 27 seulement. Câblage du vrai checker (`QCChecker`) = tâche séparée,
à faire quand Bam2Beta publiera nativement `Preprocess_28M`/CpG.

⚠ Ce snapshot remplace celui du 14/08 (rarefaction Bladder_Blood, 2ᵉ vague Bam2Beta) — sujet non
retraité dans cette session, statut inconnu à ce jour si toujours pertinent.
