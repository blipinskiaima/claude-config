---
name: livrables-actuels-du-projet-feature
description: Décisions features + emplacement livrables — juin 2026
metadata: 
  node_type: memory
  originSessionId: b3ac9798-fbc1-465e-a927-aad831034f9b
---

# Livrables Feature (juin 2026)

## Décisions scientifiques (inchangées, voir archives)

| Test | KPI Sens@95% Active_NoMut | Décision |
|------|---------------------------|----------|
| combined_v2_probs (+ EPIC + Loyfer) | +14.5 pp vs baseline | Adopté pool |
| combined_v4_short_read (short-read rigoureux) | +4.6 pp vs baseline v2 | Recommandé adoption |

Détail artefacts : **`~/Pipeline/Feature/archives/features/combined_v*/`**

## Où vivent les livrables maintenant (post-refactor juin 2026)

- **Run détaillé** : `result/{std_N}/{combo}/` (scores.csv, stratified_sensitivity.csv, PNG) — via `launch.sh`
- **Comparaison inter-runs** : `feature_runs.duckdb` (racine) via `scripts/feature_db.py`
- **Cohorte figée** : `data/cohorts/{std_N}/` (manifest.json + samples.tsv) ; pipeline cf. [[pipeline-3-etapes]]

## Ne plus utiliser (archivés)

- `runs/`, `experiments/`, `scripts/bin/`, `scripts/0[1-6]_*` (ancien grid → `archives/`)
- `features/` et `memory/` à la racine (→ `archives/`)
