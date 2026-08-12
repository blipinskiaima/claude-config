---
name: iv-module
description: "Module IV (Identite de Vigilance) — sexe + ancestry via raima, sorties, tests de validation"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c6971ef-9e62-46ae-935a-5026efb56aa3
  modified: 2026-08-11T08:47:52.662Z
---

# Module IV — Identite de Vigilance (2026-05-07)

- **Container** : `blipinskiaima/raima:latest`
- **Workflow** : `workflow/IV.nf` — 1 process `IV_call`
- **Script** : `bin/iv_score.R` — appelle `raima::infer_sex` + `raima::infer_ancestry`
- **Dependance** : `/scratch/dependencies/raima-model/model_ancestry_data.tsv.gz` (1.5 GB)

## Sorties (`{OUTPUT}/{ID}/IV/`)

- `{ID}.sex.tsv` — 1 ligne, 1 valeur scalaire
- `{ID}.ancestry.tsv` — 2 lignes (header + valeurs), **18 colonnes nommees** : Africa W/S/E/N,
  Middle East, Ashkenazi, Italy, Europe E/NW/SW, Finland, South America, Sri Lanka, Pakistan,
  Bangladesh, Asia E, Japan, Philippines

## Activation

Actif par defaut en prod / liquid / solid. Mode retrospectif supporte (chaine `BAM_FILE` quand
`--MERGE false`). **Hors strategie de qualification** (pas de check-conformity).

Consomme en aval par **TOO** (`IV.out.tsv` fournit le sexe au modele TOO5). Le sexe est converti
en `TRUE`/`FALSE` en bash en amont car `normalize_sex` upstream est casse — voir [[too-module]].

## Tests de validation

| sample | contexte | resultat |
|---|---|---|
| Healthy_826 | CGFL solid | sex = 0.9974 · ancestry max Europe (NW) 0.4641 + Italy 0.3437 — PASS |
| Healthy_4 | HCL liquid, retrospectif | sex = 0.0005 · ancestry Europe (SW) 0.579 + (NW) 0.4055 — PASS |
