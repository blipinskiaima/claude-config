---
name: twist-samples
description: "Twist_* = série de titration liquid/CGFL (chimie d'enrichissement Twist), ni type ni cohorte ni commande. 22 samples en base dont une série _rep_2 (réplicats inter-run)."
metadata: 
  node_type: memory
  type: project
  originSessionId: c981991f-4725-46fb-89ec-2c8c8270a5f5
---

« twist » n'est **ni un sample_type, ni une cohorte, ni une commande** dans trace-prod (zéro occurrence dans le code). Ce sont des samples `Twist_*` stockés comme `liquid` / `CGFL`, une série de titration pour la validation de la chimie d'enrichissement **Twist** (concurrent de Watchmaker). Leur `metadata.class` vaut `Test dilution Twist_0.1pc`, le reste des metadata est vide (pas de patient réel).

## État base (27/08/2026) — 22 samples

Première série (mai-juin 2026) : `Twist_0pct`, `Twist_0_1pct`, `Twist_0_25pct`, `Twist_0_5pct`,
`Twist_1pct`, `Twist_10_1`→`Twist_10_7`, `Twist_Diluant_RB`.
Série **`_rep_2`** (15/06/2026) : `Twist_10_1_rep_2`→`Twist_10_8_rep_2`, `Twist_Diluant_RB_rep_2`.

⚠ **Périmé dans la version précédente de cette note** : elle annonçait 12 samples et
`Twist_10_5` « hors DB » — il y est depuis le 12/06/2026, et toute la série `_rep_2` a suivi.
Liste à jour : `query "SELECT sample_name FROM samples WHERE LOWER(sample_name) LIKE '%twist%' ORDER BY sample_name"`.

## Les `_rep_2` sont des réplicats INTER-RUN, pas des rebasecalled

`Twist_10_3` (run 29/05, barcode19, **multiplex** 4 samples/run, 61,73 M reads) et
`Twist_10_3_rep_2` (run 12/06, barcode59, **simplex**, 26,24 M reads) sont deux passages
séquençage distincts du même matériel. Ils portent donc des `run_id`/`barcode` différents et
**ne sont pas** traités par la propagation `*_rebasecalled*` d'`import-metadata`.

Ce couple sert de **témoin de reproductibilité** : ×2,35 de profondeur d'écart, mais mVAF v1
1,25 vs 1,231, Mode1 SC 166,86 vs 166,45, `blood_0` 0,879 vs 0,877. Ce qui diverge, ce sont les
**classifieurs**, pas les métriques quantitatives : TOO `Colon` vs `Bladder+Pancreas` (les deux
`Unresolved: uncertain tumor class` → la classe affichée n'a pas de portée) et `ancestry`
Europe (South West) vs (North West). À garder en tête avant de lire une divergence de
classifieur comme un signal.

## Gotchas données

- **`pod5_adresse` NULL sur les Twist multiplexés** (dont `Twist_10_3`) → `taille_pod5` /
  `pod5_completude` vides. Les `_rep_2` simplex ont leur adresse (342 GiB, 70 POD5, 100 %).
  Fait partie des 15 samples du fil ouvert « retrouver l'adresse POD5 » (12 Twist + 3 Ma_SAB).
- **`frag_status` KO / `frag_mode1`/`frag_mode2` NULL** : seul `Fragmentomics/filtered_softclipped`
  existe → n'utiliser que les `*_sc`, cf [[project_frag_softclip_trim]].
- **`small_fragments` KO** : le miroir `CGFL_small_fragments/Twist_10_3_rep_2/` existe mais ne
  contient que `BAM` (il en faut 6) → le KO est exact, ce n'est pas le décalage de nommage de
  [[project-schema-v27-small-fragments]]. `small_fragments_metrics` : 0 ligne.
- Seuils de raréfaction 1M→20M **tous KO**, aucune ligne dans `rarefaction` ni `dilution`.
- Profils mVAF ~0 attendus : blanc `Twist_Diluant_RB` **et** `Twist_10_7` (contrôle négatif).

## Écart données S3 ↔ base (juin 2026, à revérifier)

Dossier **`Twist_0%/`** parasite dans `processed` uniquement (nom malformé, `Twist_0pct`
existe déjà proprement) — ne pas y toucher (règle S3).

## Workflow "check twist + export"

```bash
python3 database/check_samples.py check liquid CGFL -s Twist_10_1 -s Twist_10_2 -s Twist_10_3 -j 4
python3 database/check_samples.py export liquid CGFL --gsheet
```
L'export `liquid CGFL --gsheet` pousse **toute** la table liquide CGFL, Twist inclus — il n'est
pas filtrable par sample. Voir [[project_columns_index]].
