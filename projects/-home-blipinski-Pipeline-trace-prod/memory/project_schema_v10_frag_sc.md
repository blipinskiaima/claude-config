---
name: schema-v10-frag-sc
description: "Schema v10 — colonnes retd_suivis frag_status_sc/frag_mode1_sc/frag_mode2_sc, calque EXACT du frag v1 mais source Fragmentomics/filtered_softclipped"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c54cc63-d28c-4cda-b1b4-1ae5ca177de5
---

# Schema v10 — colonnes frag softclipped (juin 2026)

3 colonnes dans `retd_suivis`, **calque exact du frag v1 (schema v2)** — seule différence : dossier source `Fragmentomics/filtered` → `Fragmentomics/filtered_softclipped`. Le fichier dedans porte le **même nom** (`{sample}.fragmentomics_modes.tsv`).
- `frag_status_sc VARCHAR DEFAULT 'KO'` — OK si `Fragmentomics/filtered_softclipped/` non vide
- `frag_mode1_sc VARCHAR DEFAULT 'NA'` — mode1 (ligne 2 col 1, virgule décimale) ou KO si absent
- `frag_mode2_sc VARCHAR DEFAULT 'NA'` — mode2 (ligne 2 col 2)

**Why:** Boris calcule une v2 du module FRAG (softclipped), produite dans `Fragmentomics/filtered_softclipped/`. Besoin de tracer dans trace-prod **exactement** comme la fragmentomique initiale — ni plus ni moins, aucune invention. Demande verbatim : « calquer la traçabilité du dossier initial sur la nouvelle version ».

**How to apply:**
- Scope (= calque du v1) : `frag_status_sc` = **liquid uniquement** (CGFL+HCL) ; `frag_mode1_sc`/`frag_mode2_sc` = **liquid + solid** (les modes v1 sont dans LiquidChecker ET SolidChecker, le statut FRAG seulement dans liquid).
- Checkers (`lib/checkers.py`) : `check_frag_sc()` (dir_not_empty), `check_frag_mode1_sc()`/`check_frag_mode2_sc()` délèguent à `_check_frag_mode(..., subdir="filtered_softclipped")`. Le helper `_check_frag_mode` a été **paramétré** (`subdir="filtered"` par défaut) — les v1 l'appellent sans subdir, les _sc avec `filtered_softclipped`. Aucun code dupliqué, même chemin S3-aware (SmartPath fallback).
- Câblage : `LiquidChecker.check_sample()` success (FRAG SC + 2 modes) + fallback (FRAG SC seul, comme FRAG v1) ; `SolidChecker.check_sample()` success (2 modes seuls, **pas** de FRAG SC).
- `update-column` (`database/check_samples.py`) : 3 entrées `'checker'` dans `COLUMN_CHECKERS` (`frag_status_sc`/`frag_mode1_sc`/`frag_mode2_sc`). Passe par le `check` général **et** rétroactivement via `update-column` (les 2 chemins demandés par Boris).
- Export (`lib/utils.py`) : `FRAG SC` après `FRAG` dans `_LIQUID_QC` ; `Frag Mode1 SC`/`Frag Mode2 SC` après `Frag Mode2` dans `_LIQUID_QC` **et** `_SOLID_QC`. Mappings `TSV_TO_DB_RETD` ajoutés (clé gsheet → db_col).
- `STATUS_COLUMNS` : `frag_status_sc` ajouté (comme `frag_status`). Les modes **NON** (pas dans `NUMERIC_COLUMNS` non plus → virgule décimale préservée, calque).

**Quirk NA vs KO (connu, non corrigé — Boris : « on fixera ça plus tard ») :** pour un sample SANS le dossier softclipped, le rendu gsheet diffère selon le chemin (identique au frag v1) :
- via `check` général → `frag_status_sc` stocké littéral `"KO"` (route `_parse_status` car ∈ STATUS_COLUMNS) → export **"KO"**
- via `update-column frag_status_sc` → KO converti en NULL (check_samples.py, dispatch 'checker') → export **"NA"**

Le remplissage rétroactif de Boris (Étape E) passe par `update-column` → les samples sans softclipped afficheront **"NA"**, pas "KO". C'est le comportement du v1 à l'identique.

Liens : [[schema-v9-dilution]] (schema précédent) · [[schema-v6-iv-qc]] (mêmes patterns STATUS_COLUMNS / VARCHAR libre / default 'KO'). Le frag v1 (schema v2) est documenté dans `project_columns_index.md`.
