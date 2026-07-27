# Context — trace-prod — 2026-07-27T14:48:39+00:00

**Branche** : main
**Dernier commit** : 5cf8c50 — feat: schema v20 — 5 métriques mito (retd_suivis, liquid)
**Status** : clean (17 untracked préexistants : backups .duckdb, CSV dev/, rapports HTML)

## Où j'en suis
Schema v20 (5 métriques mito dans retd_suivis, liquid only) implémenté de bout en
bout via le skill add-trace-prod : étapes A→D validées et poussées. Le backfill
tourne encore en tmux `tp_mito` (script scratchpad/backfill_mito.sh, log
backfill_mito.log) : 4/10 update-column faits à 14h48, puis 2 export --gsheet
avec retry 503 en fin de script.

## Ce qui marche / ce qui foire
- ✓ Code v20 complet et vérifié : DDL + migration v20 en base, 5 checkers testés
  (HCL Colon_1 = 18,23/100/5,133307299/1,1007/150,066 = référence Boris), NULL→NA,
  export TSV headers en positions 36-40/52 avec arrondi 2 déc (base = précision complète).
- ✓ Doc à jour : CLAUDE.md, README.md, mémoire project_schema_v20_mito.md + MEMORY.md.
- ✗ Backfill NON terminé au moment du snapshot — les 6 update-column restants et les
  2 exports gsheet n'ont pas encore été vérifiés. Compteurs par labo à contrôler.
- ⚠ Piège rencontré : `Colon_1` existe en CGFL ET HCL avec des valeurs mito différentes.
- ⚠ Piège rencontré : `update-column -s` sur un sample absent du labo ciblé affiche
  « N samples mis à jour » sans toucher aucune ligne (compteur d'itérations) — un test
  négatif fait sur le mauvais labo semble passer à tort.

## Prochaine étape
Relire scratchpad/backfill_mito.log : confirmer 10/10 update-column, les comptages
par labo (~582 CGFL / ~513 HCL non-NULL attendus) et le succès des 2 exports gsheet.
Si un export a épuisé ses 5 retries 503, le relancer seul.
