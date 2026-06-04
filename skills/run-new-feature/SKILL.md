---
name: run-new-feature
description: Workflow guidé pour tester l'ajout d'une ou plusieurs nouvelles features au pool du projet ~/Pipeline/Feature/. Étend scripts/01_prepare_cohort.py + data/feature.yaml, regénère snapshot + cohort.tsv, lance test_combo (scripts/02_test_combo.py), identifie le best combo, exécute scripts/02–04 et crée un livrable figé sous result/{slug}/. Use when the user says "/run-new-feature", "ajoute la feature X au pool", "teste de nouvelles features", "nouveau test de feature short_read", or any variation of adding/testing new candidates in the Feature/ pipeline.
---

<objective>
Automatiser le cycle complet de test d'une nouvelle feature dans `~/Pipeline/Feature/`, via le **pipeline standardisé** (`scripts/01` → `scripts/02_test_combo` → `scripts/02`–`04`). Boris donne 1+ noms de features candidates ; le skill orchestre les modifications, l'exécution et la restitution.

**Scope** : features **déjà dans trace-prod** (colonnes SQL). Pas de Bam2Beta, pas de recalcul scientifique. Colonne absente → orienter vers `/add-trace-prod`.

**Hors scope** : ne pas modifier `scripts/02_train_combined.R` sauf bug ; le grid et le pool suffisent pour tester de nouvelles colonnes.

**Archives** : l'ancien dossier `features/` (livrables v2/v3/v4, compute/model/eval dupliqués) est dans `archives/features/`. Ne plus y créer de sous-dossiers.
</objective>

<workflow>

## Step 0 — Vérification du contexte

**Actions** :
1. `pwd` = `/home/blipinski/Pipeline/Feature/`
2. Fichiers clés présents :
   - `scripts/01_prepare_cohort.py`
   - `data/feature.yaml`
   - `scripts/02_test_combo.py`
   - `scripts/03_get_best_combo.py`
   - `scripts/02_train_combined.R`, `03_evaluate.R`, `04_plot_investigation.R`
3. `git status --short` — demander confirmation si modifs non commitées sur ces fichiers.
4. État cohorte / pool :
   ```bash
   ls -t data/snapshots/snapshot_*.parquet | head -1
   python3 -c "import yaml; print(list(yaml.safe_load(open('data/feature.yaml')).keys()))"
   ```

## Step 1 — Parsing des features à tester

1. Noms depuis les arguments du skill (ex. `mvaf_v1_short_read`, `ichor_short_read_x100`).
2. Pour chaque feature, valider avec Boris (`AskUserQuestion` si besoin) :
   - Table + colonne(s) trace-prod
   - Type : `source_col` (simple) ou `source_cols` (bloc) dans `feature.yaml`
   - Pas de collision avec une clé existante du pool
3. Vérifier les colonnes (read-only) :
   ```python
   import duckdb
   con = duckdb.connect("/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb", read_only=True)
   con.execute("DESCRIBE <table>").fetchdf()
   ```
   Colonne manquante → **ARRÊTER**, suggérer `/add-trace-prod`.

## Step 2 — Plan & confirmation Boris

Présenter :
- Modifications prévues dans `scripts/01_prepare_cohort.py` (SQL `WITH base AS`)
- Entries `data/feature.yaml`
- Estimation combos ajoutées (~957 total pour pool actuel ; delta selon N optionnelles)
- Nom livrable proposé : `result/combined_v{N}_{slug}/` (pas `features/`)
- Temps grid (~2–3 s/combo × nouvelles combos / 6 workers)

**OK explicite** avant d'éditer.

## Step 3 — Édition de `scripts/01_prepare_cohort.py`

1. Lire le fichier ; étendre le bloc SQL (TRY_CAST + LEFT JOIN si nouvelle table).
2. Même patterns que l'ancien `refresh_cohort.py` — voir [references/refresh-cohort-edits.md](references/refresh-cohort-edits.md) (**remplacer mentalement** `refresh_cohort.py` par `01_prepare_cohort.py`).

Sortie : SQL prêt ; le script écrit snapshot + `data/cohort.tsv` en une commande.

## Step 4 — Édition de `data/feature.yaml`

Ajouter les entries (`source_col` ou `source_cols`). Voir [references/feature-yaml-edits.md](references/feature-yaml-edits.md).

## Step 5 — Régénérer snapshot + cohort.tsv

```bash
cd /home/blipinski/Pipeline/Feature/
python scripts/01_prepare_cohort.py
```

Vérifier les nouvelles colonnes dans le dernier `data/snapshots/snapshot_*.parquet` et `data/cohort.tsv`. Si tout NA → ARRÊTER (jointure / table source).

## Step 6 — Grid search

1. Estimer le nombre de combos **non cachées** (DuckDB `runs` existantes).
2. Si > 500 nouvelles combos → confirmation Boris.
3. Lancer :
   ```bash
   python3 scripts/02_test_combo.py --workers 6
   ```
   (`--smoke` pour test ; logs erreur dans `log/grid/`)

## Step 7 — Identifier best NEW vs best OLD

```bash
python3 scripts/03_get_best_combo.py --top 10
```

SQL complémentaire (read-only) sur `result/feature_runs.duckdb` :
- **NEW** : meilleur combo **incluant** au moins une des nouvelles clés pool
- **OLD** : meilleur combo **sans** ces clés (même `n_samples` si possible)

Noter : features logiques du pool (ex. `mvaf_v1_short_read`) vs colonnes TSV passées à `--features` (via `expand_features()` dans test_combo).

## Step 8 — Livrable `result/{slug}/` (remplace `features/{nom}/`)

Structure cible — voir [references/livrable-creation.md](references/livrable-creation.md) :

```
result/combined_v{N}_{slug}/
├── README.md              # hypothèse, combos NEW/OLD, KPIs, conclusion
├── config.yaml            # snapshot, pool entries, target_spec, seed
├── data/                  # copies figées snapshot + cohort.tsv
│   ├── snapshot_*.parquet
│   └── cohort.tsv
├── new/                   # best combo avec nouvelles features
│   ├── train.json         # copie KPI 02
│   ├── scores.csv         # sortie 02
│   ├── eval/              # sortie 03
│   └── eval/plots/        # sortie 04
└── old/                   # best combo sans nouvelles features (même structure)
```

**Actions** :
1. Déduire `slug` et `vN` (lister `result/combined_v*` ou `archives/features/combined_v*` pour le numéro).
2. `mkdir -p result/{slug}/{cohort,new/eval/plots,old/eval/plots}`
3. Copier snapshot + `cohort.tsv` dans `data/` du livrable
4. Pour **NEW** et **OLD**, déplier les colonnes TSV depuis `feature.yaml` (`expand_features` comme dans test_combo) puis :
   ```bash
   Rscript scripts/02_train_combined.R --tsv data/cohort.tsv \
     --features "<cols>" --out result/{slug}/new
   Rscript scripts/03_evaluate.R --csv result/{slug}/new/scores.csv \
     --out result/{slug}/new/eval --target-spec 0.95
   Rscript scripts/04_plot_investigation.R --csv result/{slug}/new/scores.csv \
     --out result/{slug}/new/eval --target-spec 0.95
   ```
   Répéter pour `old/` avec le combo OLD.
5. Rédiger `README.md` + `config.yaml` ; tableau `comparison_new_vs_old.csv` (KPIs clés).

## Step 9 — Restitution à Boris

- Features ajoutées + colonnes trace-prod
- Best NEW vs OLD (Δ `sens_95_active_nomut`, `auc_all`, etc.)
- Chemin `result/{slug}/`
- Recommandation : garder au pool ou retirer
- **Pas de commit automatique**

</workflow>

<references>

| Fichier | Usage |
|---|---|
| [references/refresh-cohort-edits.md](references/refresh-cohort-edits.md) | Patterns SQL — appliquer à **`scripts/01_prepare_cohort.py`** (pas `archives/cohort/refresh_cohort.py`) |
| [references/feature-yaml-edits.md](references/feature-yaml-edits.md) | Format `data/feature.yaml` |
| [references/livrable-creation.md](references/livrable-creation.md) | Structure **`result/{slug}/`** (mis à jour ; ignore les chemins `features/`) |

| Projet | Doc |
|---|---|
| Pipeline | `README.md`, `CLAUDE.md`, `.claude/rules/07-feature-structure.md` |
| Livrables historiques | `archives/features/` |

</references>

<rules>

1. **trace-prod read-only** toujours.
2. **Confirmation** avant edit sources, grid massif (>500 combos), création livrable.
3. **Pas de commit** automatique.
4. Colonne absente → `/add-trace-prod`, pas de hack SQL.
5. Snapshots : pas d'écrasement (`snapshot_YYYY-MM-DD_vN.parquet`).
6. **Ne pas recréer** `features/` à la racine — livrables dans `result/{slug}/`.

</rules>
