---
name: project-schema-v6-iv-qc
description: "Schema v6 (mai 2026) — 4 colonnes IV/QC dans retd_suivis pour ancestry, sex, read_start_time"
metadata: 
  node_type: memory
  type: project
  originSessionId: 98d94d3a-db3d-4234-8ea7-4543301c6796
---

Schema v6 ajoute 4 colonnes dans `retd_suivis` (toutes VARCHAR, hors STATUS_COLUMNS) :

| Colonne | Default | Source | Format |
|---|---|---|---|
| `read_start_time` | 'KO' | `QC/Samtools/{sample}.read_start_time.tsv` | OK/KO (présence, **pas de lecture** ~3-4 GB) |
| `ancestry` | 'NA' | `IV/{sample}.ancestry.tsv` | nom de colonne argmax ligne 2 (header + 1 ligne, 18 ancestries) |
| `sex_proba` | 'NA' | `IV/{sample}.sex.tsv` | p arrondi au millième, virgule (PAS de header, 1 valeur ligne 1) |
| `sex_predicted` | 'NA' | dérivé de `check_sex_proba()` | F si p<0.5, M si p≥0.5 |

**Why:** Boris a ajouté l'extraction IV (ancestry + sex predicted depuis méthylation) au pipeline Bam2Beta. Les 4 colonnes sont indépendamment populables via `update-column` (un seul appel par colonne, pas besoin de re-check complet).

**How to apply:** Path IV/ est **sœur de QC/** (pas dans QC/IV/ comme je l'avais initialement supposé). Migration idempotente dans `_init_schema()` via `ALTER TABLE retd_suivis ADD COLUMN IF NOT EXISTS`. Headers GSheet : entre `Frag Mode2` et `BAM` dans `_LIQUID_QC` et `_SOLID_QC`. Commande update : `python3 database/check_samples.py update-column {col} {liquid|solid} {CGFL|HCL} [-s sample]`.

Méthodes dans `BaseChecker` (lib/checkers.py) : `check_read_start_time`, `check_ancestry`, `check_sex_proba`, `check_sex_predicted`. Câblées dans `LiquidChecker.check_sample()` ET `SolidChecker.check_sample()` (success path + fallback dict).
