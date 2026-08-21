# Context — trace-prod — 2026-08-21T08:41:38+00:00

**Branche** : main
**Dernier commit** : 91e4d53 — feat: schema v26 — mvaf_v15 (retd_suivis, liquid only)
**Status** : propre, synchronisé avec origin/main (untracked : backups .duckdb, CSV dev/,
rapports HTML, metadata_HCL.tsv, .claude/skills-worktrees — inchangés depuis avant la session)

## Où j'en suis
Tâche terminée de bout en bout : schema v26 — colonne `mvaf_v15` dans `retd_suivis` (liquid only),
calque exact de `mvaf_v14`, source `BETA/{s}.merged.epic.raima_score.V1.5.tsv`. Backfill complet,
exports gsheet passés, doc (README Table 3 + section dédiée, CLAUDE.md) et mémoire à jour,
commit pushé. Rien en attente.

## Ce qui marche / ce qui foire
- ✓ Backfill 100 % : 849 CGFL + 513 HCL = 1362 samples, 0 erreur, 0 NA, 0 KO résiduel
  (~18 min en tmux, exports gsheet OK 1re tentative, aucun 503)
- ✓ Contrôle croisé DB↔fichier source (20 samples) et gsheet↔DB (1362 lignes) : 0 écart.
  Colonne `mVAF v1.5` en position 16, contiguë à `mVAF v1.4`
- ✓ Coexistence demandée par Boris respectée : v1.3/v1.4/v1.5 côte à côte, `mvaf_v14` toujours
  à 1497 non-NULL et `mvaf_v13` à 1464 (inchangés). v1.4 ≠ v1.5 sur 443 CGFL + 94 HCL
- ✓ Structure du V1.5 vérifiée sur fichier réel AVANT codage (3 col, `cols[1]`, comme V1.4 —
  le V1.3 en avait 4) ; `format_mvaf4` neutralise la notation scientifique (3e-06 → 0,000003000)
- ○ Chemin `NA → NULL` non observable en prod (couverture 100 %) : prouvé par monkeypatch,
  vraie valeur restaurée ensuite
- ○ `dilution` / `rarefaction` ont leur propre `mvaf_v14_*` — v1.5 volontairement non propagé

## Prochaine étape
Aucune action requise — tâche fermée. Trois fils ouverts si besoin :
1. `update-column mvaf_v14 liquid CGFL` comblerait 12 `Bladder_Urine_*` à NULL dont le fichier
   V1.4 est arrivé après le dernier backfill v14 (décalage temporel, pas un bug)
2. Reste du snapshot v25 : 27 `Bladder_Urine_02_*` jamais passés par `check-qc` (→ pas de
   `reads_total`, donc 28M/CpG incalculable) ; câblage réel de `QCChecker` quand Bam2Beta
   publiera nativement `Preprocess_28M`
3. Reste du snapshot du 14/08, jamais retraité depuis : rarefaction Bladder_Blood (2e vague
   Bam2Beta) — statut inconnu à ce jour
