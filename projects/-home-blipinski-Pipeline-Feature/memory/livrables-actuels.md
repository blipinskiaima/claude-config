---
name: livrables-actuels-du-projet-feature
description: Décisions features + emplacement livrables — juin 2026
---

# Livrables Feature (juin 2026)

## Décisions scientifiques (inchangées, voir archives)

| Test | KPI Sens@95% Active_NoMut | Décision |
|------|---------------------------|----------|
| combined_v2_probs (+ EPIC + Loyfer) | +14.5 pp vs baseline | Adopté pool |
| combined_v4_short_read (short-read rigoureux) | +4.6 pp vs baseline v2 | Recommandé adoption |

Détail artefacts : **`~/Pipeline/Feature/archives/features/combined_v*/`**

## Où vivent les livrables maintenant

- **Nouveau test** : `runs/combined_v{N}_{slug}/` (pas `features/`)
- **Comparaison grid** : `experiments/feature_runs.duckdb` + `scripts/bin/analyze.py`
- **Run détaillé** : `scripts/02` → `03` → `04` sous `runs/<nom>/`

## Ne plus utiliser

- `features/` à la racine du repo (archivé)
- `memory/` à la racine du repo (archivé → `archives/memory/`)
