# Création du livrable `result/{slug}/`

> **Mise à jour 2026-06** : le dossier racine `features/` est archivé dans `archives/features/`. Les nouveaux livrables utilisent **`scripts/02`–`04`**, pas `train.R` / `evaluate.py` maison.

## Structure cible

Suit `.claude/rules/07-feature-structure.md`.

```
result/combined_v{N}_{slug}/
├── README.md
├── config.yaml
├── cohort/
│   ├── snapshot_YYYY-MM-DD.parquet
│   └── input.tsv
├── new/
│   ├── scores.csv
│   ├── scores.json
│   ├── eval/                    # scripts/03
│   └── eval/plots/              # scripts/04
└── old/
    └── (même structure)
```

Tableau `comparison_new_vs_old.csv` : KPIs NEW vs OLD (depuis les `.json` ou tables eval).

## Choix du nom du dossier

```python
# 1. Lister les dossiers existants combined_v*_*
import re, glob
existing = glob.glob('result/combined_v*_*') + glob.glob('archives/features/combined_v*_*')
versions = [int(re.search(r'combined_v(\d+)_', d).group(1)) for d in existing if re.search(r'combined_v(\d+)_', d)]
next_v = max(versions, default=1) + 1
# next_v = 3 si on a déjà v2_probs

# 2. Construire le slug court à partir des features ajoutées
# Exemples :
#   ["mvaf_v1_short_read"]                                          → "short_read"
#   ["mvaf_v1_short_read", "ichor_x100_short_read"]                 → "short_read"
#   ["probs_loyfer_normalized"]                                     → "loyfer_normalized"
slug = <descripteur court>

nom_dossier = f"combined_v{next_v}_{slug}"
```

## Template `compute/compute.py`

Document l'origine des inputs gelés.

```python
#!/usr/bin/env python3
"""
Étape 1 — COMPUTE ({nom_dossier})

Pas de calcul de feature spécifique : ce test consomme directement les
features déjà calculées par Bam2Beta / raima et exposées par trace-prod.

Les fichiers sont figés ici pour reproductibilité ISO 15189 :
  - snapshot_YYYY-MM-DD.parquet  ({n} samples)
  - input.tsv                    (TSV consommable par R)

Features ajoutées dans ce test :
  - {nom_feature_1}              (source : trace-prod.{table}.{col})
  - {nom_feature_2}
  - ...

Régénération depuis zéro :
  python3 ../../../cohort/refresh_cohort.py
  python3 ../../../experiments/prepare_inputs.py
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    snap = pd.read_parquet(HERE / "snapshot_*.parquet")  # use glob if needed
    tsv = pd.read_csv(HERE / "input.tsv", sep="\t")
    print(f"snapshot : {len(snap)} samples × {snap.shape[1]} cols")
    print(f"input.tsv: {len(tsv)} samples × {tsv.shape[1]} cols")
```

## Template `model/train.R`

Entraîne le best combo NEW + le best combo OLD sur les mêmes folds (seed=42).

```r
# ÉTAPE 2 — MODEL ({nom_dossier})
suppressPackageStartupMessages({
  library(dplyr); library(stringr)
})

source("/home/blipinski/Pipeline/Feature/features/_shared/build_combined_score_flex.R")

HERE   <- "/home/blipinski/Pipeline/Feature/features/{nom_dossier}/model"
TSV_IN <- "/home/blipinski/Pipeline/Feature/features/{nom_dossier}/compute/input.tsv"

# ---- expand : noms logiques → colonnes TSV ----
pool_groups <- list(
  probs_epic = c("prop_blood_0", ..., "prop_testis_0"),                      # 16 cols
  probs_loyfer = c("loyfer_1_fibroblast_heart", ..., "loyfer_31_muscle_skeletal"),  # 31 cols
  # ← AJOUTER ICI LES NOUVEAUX BLOCS introduits par ce test
  probs_epic_short_read = c("prop_blood_0_short_read", ..., "prop_testis_0_short_read")
)

expand_features <- function(logical_names) {
  out <- c()
  for (f in logical_names) {
    if (f %in% names(pool_groups)) out <- c(out, pool_groups[[f]])
    else out <- c(out, f)
  }
  out
}

extract_indication <- function(sample_name) {
  sample_name |>
    str_remove("_?rebasecalled.*$") |>
    str_remove("_(rep|bis|ter|quater|moche)$") |>
    str_extract("^[A-Za-z]+(?:_[A-Za-z]+)*")
}

# ---- combos à entraîner (REMPLIR depuis l'analyse) ----
NEW_LOGICAL <- c("mvaf", "frag_diff", "frag_mode1", "probs_epic_short_read")  # best NEW
OLD_LOGICAL <- c("mvaf", "frag_diff", "frag_mode1", "probs_epic")              # best OLD

NEW_COLS <- expand_features(NEW_LOGICAL)
OLD_COLS <- expand_features(OLD_LOGICAL)

# ---- load + mutate ----
cat("Reading input.tsv ...\n")
df_raw <- read.table(TSV_IN, sep = "\t", header = TRUE,
                     na.strings = c("","NA","None"),
                     stringsAsFactors = FALSE, quote = "", check.names = FALSE)

df <- df_raw |>
  mutate(
    indication = extract_indication(name),
    vaf        = vaf_gene1_pct,
    ichorcna   = ichor_tf,
    mvaf       = mvaf_v1
  )

# ---- run NEW ----
cat("\n=== NEW combo ===\n")
cat("Logical features :", paste(NEW_LOGICAL, collapse = ", "), "\n")
cat(sprintf("XGBoost cols     : %d\n", length(NEW_COLS)))
res_new <- build_combined_score_flex(df, feature_cols = NEW_COLS, seed = 42)
write.csv(res_new$predictions, file.path(HERE, "predictions_new.csv"), row.names = FALSE)

# ---- run OLD ----
cat("\n=== OLD combo ===\n")
cat("Logical features :", paste(OLD_LOGICAL, collapse = ", "), "\n")
cat(sprintf("XGBoost cols     : %d\n", length(OLD_COLS)))
res_old <- build_combined_score_flex(df, feature_cols = OLD_COLS, seed = 42)
write.csv(res_old$predictions, file.path(HERE, "predictions_old.csv"), row.names = FALSE)

cat("\nDone.\n")
```

## Template `eval/evaluate.py`

Le mieux est de **copier-éditer** depuis `features/combined_v2_probs/eval/evaluate.py` (déjà validé).

Les modifs typiques nécessaires :
- Header (commentaire) : changer `combined_v2_probs` → `{nom_dossier}`
- `HERE`, `MODEL`, `PLOTS` : automatique via `Path(__file__).resolve().parent`
- Le reste du code est générique (lit `predictions_new.csv` / `predictions_old.csv`, sort plots et CSVs)

Donc en pratique :
```bash
cp features/combined_v2_probs/eval/evaluate.py features/{nom_dossier}/eval/evaluate.py
```
puis éditer le bloc commentaire en tête.

## Template `README.md`

```markdown
# {nom_dossier}

Test d'ajout au pool de la (ou des) feature(s) suivante(s) :
- `{nouvelle_feature_1}` (source : trace-prod.{table}.{col})
- `{nouvelle_feature_2}` ...

## Hypothèse testée

L'ajout de {description courte des nouvelles features} au pool actuel
améliore-t-il le KPI clé `Sens@95% Active_NoMut` ?

## Méthode

3 étapes : compute → model → eval. Le snapshot et l'input.tsv sont figés
dans `compute/`. Le modèle XGBoost 5-fold (seed=42) est dans `model/`.
L'évaluation et la comparaison NEW vs OLD sont dans `eval/`.

## Combinaisons comparées

| | NEW (avec nouvelles features) | OLD (sans nouvelles features) |
|---|---|---|
| Features logiques | {liste NEW} | {liste OLD} |
| XGBoost cols | {n_new} | {n_old} |
| n scoring | {n_samples} | {n_samples} |

## Résultats (à target_spec = 0.95)

| KPI | NEW | OLD | Δ |
|---|---|---|---|
| AUC ALL | ... | ... | ... |
| Sens@95% ALL | ... | ... | ... |
| **Sens@95% Active_NoMut** ⭐ | ... | ... | ... |

## Conclusion

{conclusion : les nouvelles features apportent / n'apportent pas}

## Reproductibilité

\```bash
cd /home/blipinski/Pipeline/Feature/
cd features/{nom_dossier}/model && Rscript train.R
cd ../../.. && python3 features/{nom_dossier}/eval/evaluate.py
\```
```

## Template `config.yaml`

```yaml
cohort:
  snapshot: compute/snapshot_YYYY-MM-DD.parquet
  input_tsv: compute/input.tsv
  n_after_filters: {n}

target_specificity: 0.95

xgboost:
  objective: binary:logistic
  eval_metric: auc
  max_depth: 3
  learning_rate: 0.1
  subsample: 0.8
  colsample_bytree: 0.8
  nrounds: 100
  nfold: 5
  seed: 42

combos:
  new:
    logical: [{liste NEW}]
    xgboost_cols: {n_new}
    source: best combo du grid sur pool étendu avec {nouvelles features}

  old:
    logical: [{liste OLD}]
    xgboost_cols: {n_old}
    source: best combo du grid sur pool actuel SANS les nouvelles features

label:
  rule: healthy=0, (mutated OR active_no_mut)=1
  filter_indications_excluded: [TNE, Nuclear, Bladder_Blood]
  filter_name_excluded: [rep, moche, bis, ter, quater]
  min_depth: 0.25
  dedup: unique_id (1 sample par unique_id)

new_features_tested:
  - name: {nouvelle_feature_1}
    source_trace_prod: {table}.{col}
    type: {simple|bloc}
```

## Anti-patterns

❌ Ne PAS dupliquer la logique XGBoost ailleurs — toujours `source()` le `build_combined_score_flex.R` partagé
❌ Ne PAS hardcoder un seed différent de 42 (sinon comparaisons cassées)
❌ Ne PAS écraser un dossier `features/{nom}/` existant — incrémenter `vN`
❌ Ne PAS oublier d'ajouter les nouveaux blocs dans `pool_groups` du `train.R` (sinon `expand_features()` rate)
