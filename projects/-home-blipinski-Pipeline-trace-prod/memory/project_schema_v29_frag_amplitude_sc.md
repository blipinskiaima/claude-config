---
name: project-schema-v29-frag-amplitude-sc
description: "Schema v29 — colonne frag_amplitude_sc (retd_suivis, liquid only), amplitude fragmentomique softclipped lue dans Fragmentomics/filtered_softclipped/{s}.amplitude_fragmento_qc.tsv ligne 2 col 2, pleine précision virgule, export 'Amplitude Frag' après Sex Predicted. Backfill 100 % (1362), 0 KO"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54e5f0c9-d216-4cd6-a2ba-d4c358e273a5
  modified: 2026-09-02T16:36:43.515Z
---

# Schema v29 — frag_amplitude_sc (septembre 2026)

Colonne `frag_amplitude_sc VARCHAR DEFAULT 'KO'` dans `retd_suivis`, **liquid uniquement**
(`LiquidChecker` seul, Solid intact — 0 fichier en solid, vérifié 0/147). Hors
`STATUS_COLUMNS` et `NUMERIC_COLUMNS` → virgule décimale préservée.

**Why:** Boris veut tracer l'amplitude fragmentomique produite par le pipeline, exportée juste
après `Sex Predicted`.

## Source

`{sample}/Fragmentomics/filtered_softclipped/{sample}.amplitude_fragmento_qc.tsv` — **même
dossier que `frag_score_v2_sc` (v11) et `frag_mode*_sc` (v10)**, d'où le suffixe `_sc`.

```
name        amplitude          <- 2 colonnes, séparateur \t
26BM01841   232.794114117482   <- ligne 2, cols[1]
```

**Format vérifié sur les 1362 fichiers, pas sur un échantillon** (avant d'écrire le checker) :
header identique 1362/1362, exactement 2 lignes et 2 colonnes, `col1 == nom du sample` partout,
**0 valeur non numérique, 0 notation scientifique, 0 vide**. Plage `0,113` → `309,238`,
médiane `234,66`. Ce contrôle amont vaut la précaution prise en v26 (le passage v1.3→v1.4 avait
déplacé la colonne sans prévenir).

## Les deux décisions qui comptent

**1. VARCHAR et non DECIMAL.** La demande disait « stocké comme valeur numérique » **et**
« fichier absent → KO ». Les deux sont incompatibles : une colonne `DECIMAL` ne peut pas porter
`KO`. C'est le KO qui tranche → VARCHAR libre, comme tous les autres scores de `retd_suivis`.
Pas une ambiguïté à arbitrer, une contradiction que la donnée résout.

**2. Pleine précision, aucun arrondi.** Le dossier source donne deux précédents **contradictoires** :
`frag_score_v2_sc` / `themelio_score` gardent la précision complète, `Mode1`/`Mode2` sont arrondis
à 2 décimales à l'export via `ROUND2_HEADERS`. Choix Boris : pleine précision
(`232,794114117482`) en base **et** à l'export, via `format_comma`. Évite un edit dans
`lib/utils.py` hors du point d'extension prévu.

## Câblage (4 fichiers, 29 lignes)

- `lib/duckdb.py` (5 edits) : `SCHEMA_VERSION 28→29` · DDL après `frag_score_v2_sc` · migration
  idempotente v29 · `TSV_TO_DB_RETD["Amplitude Frag"]` · description.
- `lib/checkers.py` (3) : `check_frag_amplitude_sc` (BaseChecker) — **calque de
  `check_frag_score_v2_sc`, son voisin immédiat**, seuls changent le nom de fichier, `cols[1]`
  au lieu de `cols[0]`, et le fallback `KO` au lieu de `NA`. Câblé `LiquidChecker.check_sample()`
  + fallback dict (groupe `"KO"`, aux côtés de `Read Start Time`/`Bootstrap`). Pas dans SolidChecker.
- `database/check_samples.py` (1) : `COLUMN_CHECKERS['frag_amplitude_sc']` (pattern simple).
- `lib/utils.py` (1) : `"Amplitude Frag"` dans `_LIQUID_QC` après `"Sex Predicted"` → **25/55**.

**Position DDL ≠ position export** (choix réversible signalé) : la colonne est déclarée à côté de
`frag_score_v2_sc` (famille `frag_*_sc`, même dossier source) mais exportée après `Sex Predicted`.
Sans effet — `ALTER TABLE` la place de toute façon en dernier physiquement et tout l'accès se
fait par nom (cf [[project-schema-v21-n50]]).

## Gotchas

- ⚠ **`_LIQUID_QC` et `_SOLID_QC` sont textuellement identiques autour de `Sex Predicted`**
  (`"Sex Predicted", "Read Start Time",` aux lignes 95-96 **et** 133-134 de `lib/utils.py`).
  Un `Edit` à 2 lignes de contexte aurait touché le solid ou échoué. Élargir jusqu'à
  `"Small Fragments"` (liquid-only). Même piège que les blocs liquid/solid de `checkers.py`
  signalé en [[project-schema-v21-n50]] — il vit aussi dans `utils.py`.
- ⚠ **`update-column` convertit `KO` → NULL** (`check_samples.py:1039`) : le littéral `KO` ne
  survit que par le `check` général. Un futur sample sans fichier alimenté par `update-column`
  sortira donc `NA`, pas `KO`. Quirk du projet depuis v10, **validé tel quel par Boris**
  (« ok pour NA »), non corrigé.
- ⚠ **Chemin `KO` non observable en prod** : couverture 100 %, aucun sample n'a de fichier
  manquant. Prouvé sur un sample inexistant, pas sur de la donnée réelle — même situation que
  [[project-schema-v21-n50]] et [[project-schema-v26-mvaf-v15]].
- **Homonyme `Colon_1`** correctement discriminé : CGFL `181,010240561518` vs HCL
  `265,417735963807` (cf [[project-schema-v20-mito]]).

## Backfill (02/09/2026) — couverture 100 %

**849 CGFL + 513 HCL = 1362 samples, 0 KO, 0 NULL, 0 erreur**, ~20 min à `-j 4` (CGFL 12 min
puis HCL 7 min, séquentiel pour le single writer lock). Correspondance fichiers ↔ base parfaite
dès le départ : 0 sample sans fichier, 0 fichier orphelin.

**Vérifs** : contrôle croisé **exhaustif** base ↔ 1362 fichiers source (`diff` complet, pas un
échantillon) → **0 écart** ; relecture gsheet ↔ base sur les 2 onglets → **0 écart**, colonne en
position 25 sur les deux ; solid resté à 147 `KO` et 41 colonnes sans `Amplitude Frag` ;
`frag_score_v2_sc` intact.

⚠ **Non vérifié** : les **formats de cellule** de la feuille. `clear()` ne les efface pas, donc
l'insertion en position 25 décale d'un cran tout ce qui était à droite, qui hérite du format de
la position précédente. Aucun effet sur les données (relecture à 0 écart) — même mécanique que
celle documentée pour les retraits dans [[project-export-retraits-et-fallback-indication]].

Checkpoint `checkpoint-pre-amplitude-frag` (sur `97e56e4` = v28), commit `f1f6785`.

Liens : [[project-schema-v11-mvaf-v13-frag-score]] (calque direct, `frag_score_v2_sc`),
[[project-schema-v10-frag-sc]] (famille `frag_*_sc`, même dossier),
[[project-schema-v18-themelio]] (même choix de pleine précision), [[project_columns_index]].
