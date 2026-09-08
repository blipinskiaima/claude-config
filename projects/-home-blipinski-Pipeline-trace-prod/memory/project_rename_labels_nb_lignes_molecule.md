---
name: rename-labels-nb-lignes-total-nb-molecule
description: "Sept. 2026 : étiquettes d'export `Nb reads total` → `Nb lignes total` et `Nb read alignés` → `Nb molécule` (gsheet/TSV, tous exports). Colonnes DuckDB inchangées. ⚠ raima et exploratory-analysis lisent l'export PAR EN-TÊTE → à adapter côté R."
metadata:
  type: project
---

# Renommage d'étiquettes `Nb lignes total` / `Nb molécule` (08/09/2026)

Demande Boris : renommer **les étiquettes seulement**, « pas changer le process ». Donc :
- `Nb reads total` → **`Nb lignes total`**, `Nb read alignés` → **`Nb molécule`** dans `_BASE_COLS` (liquid + solid),
  `Small Fragments`, `Dilution`, `Rarefaction`, et dans les clés des dicts de résultat des checkers
  (`lib/checkers.py`) mappées par `TSV_TO_DB_QC`. Horaire / threshold / dilution_lung les avaient déjà.
- **Colonnes DuckDB `nb_reads_total` / `nb_reads_aligned` inchangées** (les renommer = migration = process).
- Anciennes clés conservées dans `TSV_TO_DB_QC` (import d'anciens TSV) — sûr car `_prepare_data` fait
  `if tsv_col not in raw_data: continue` → jamais d'écrasement par `None` quand une clé manque.

**Why:** harmoniser avec le nommage adopté sur les gsheets v28/v32/v33 (`Nb lignes total` / `Nb molécule`).

**How to apply:**
- Un renommage d'étiquette touche **4 endroits** : listes d'export (`lib/utils.py`, `lib/gsheets.py`),
  mapping d'import (`TSV_TO_DB_QC`), clés produites par les checkers (`lib/checkers.py`, 2 blocs liquid/solid),
  docs (README/CLAUDE.md). Oublier les checkers = le `check` n'écrit plus la colonne (clé absente → `continue`).
- Test minimal : `check -s <sample>` puis vérifier `nb_reads_total` en base, et `export -o x.tsv` pour l'en-tête.
- ⚠ **Consommateurs externes qui lisent l'export par en-tête** (cassent après re-export) :
  `raima/R/evaluate-score.R:237,240` (`download_trace_prod_metadata()` → `~/Downloads/{CGFL,HCL}_Trace_PROD.tsv`,
  lit `` `Nb reads total` ``), `raima/code-save/model-CNV-v1-vaf-transfo.R:10` (`Nb read alignés`),
  `exploratory-analysis-CGFL-HCL/dev/run_legacy_pipeline.R:50`, `misc/generate_results.R`,
  `misc/results_londoncalling2026.R:156`. Sans impact : Aima-Tower (`SampleDetail.tsx:211`, libellé UI sur la
  colonne DB), `04_qc_plot.R` (liste de candidats), `build_raima_cache.py` (alias SQL).
- ⚠ Un `retry` sur `Could not set lock` avec une connexion `read_only=True` **n'aide pas** : le lock DuckDB est
  exclusif, la lecture attend autant que l'écriture (30 min d'ABANDON dans le test du 08/09).

Lié : [[project_export_retraits_et_fallback_indication]] (autre cas « export ≠ base »).
