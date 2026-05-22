---
name: run-new-feature
description: Workflow guidé pour tester l'ajout d'une ou plusieurs nouvelles features au pool du projet ~/Pipeline/Feature/. Étend cohort/refresh_cohort.py + experiments/pool.yaml, regénère snapshot + input.tsv, lance le grid search complet, identifie le best combo et crée un livrable features/{nom}/ reproductible avec comparaison vs le best combo sans les nouvelles features. Use when the user says "/run-new-feature", "ajoute la feature X au pool", "teste de nouvelles features", "nouveau test de feature short_read", or any variation of adding/testing new candidates in the Feature/ pipeline.
---

<objective>
Automatiser le cycle complet de test d'une nouvelle feature dans le projet ~/Pipeline/Feature/, en suivant la procédure validée des 9 briques du workflow (cf. WORKFLOW.md à la racine). Boris donne 1+ noms de features candidates ; le skill orchestre tout : modifications de code, exécution du pipeline, archivage du livrable, comparaison.

**Scope du skill** : extension du pool actuel avec des features **déjà présentes dans trace-prod**. Pas de modification de Bam2Beta, pas de recalcul scientifique. Si la colonne n'existe pas dans trace-prod → orienter Boris vers le skill `/add-trace-prod`.

**Non-scope** : ne touche pas à `score_one_combo.R`, `grid_search.py`, `build_combined_score_flex.R` — ces fichiers sont stables et leur API supporte déjà l'ajout de candidates simples/bloc.
</objective>

<workflow>

## Step 0 — Vérification du contexte

**Actions** :
1. Vérifier le `pwd` : on doit être dans `/home/blipinski/Pipeline/Feature/` (ou s'y placer)
2. Vérifier que les 4 fichiers clés existent :
   - `cohort/refresh_cohort.py`
   - `experiments/pool.yaml`
   - `experiments/prepare_inputs.py`
   - `experiments/grid_search.py`
3. Vérifier le statut git :
   ```bash
   git status --short
   ```
   Si des modifs non commitées sur ces fichiers, **demander confirmation** avant de poursuivre (risque d'écraser le travail en cours).
4. Identifier le snapshot le plus récent et l'état actuel du pool :
   ```bash
   ls cohort/snapshot_*.parquet | tail -1
   python3 -c "import yaml; p=yaml.safe_load(open('experiments/pool.yaml')); print(list(p.keys()))"
   ```

**Sortie** : confirmation que le projet est dans un état utilisable.

## Step 1 — Parsing des features à tester

**Actions** :
1. Récupérer les noms de features depuis les arguments du skill (1 ou plus).
   - Exemples : `mvaf_v1_short_read`, `ichor_x100_short_read`, `probs_epic_short_read`
2. Pour chaque feature, demander à Boris **interactivement** via `AskUserQuestion` (1 batch si possible) :
   - **Source dans trace-prod** : nom de la table + nom(s) de colonne(s)
     - Ex: `qc_metrics.mvaf_v1_short_read` (1 colonne)
     - Ex: `probs.short_read_prop_blood_0, short_read_prop_breast_0, ...` (16 colonnes)
   - **Type** : simple (1 colonne) ou bloc (≥ 2 colonnes regroupées en 1 candidate)
   - **Suffixe nom logique** : déjà fourni par l'argument, mais vérifier qu'il ne collisionne pas avec un nom existant du pool
3. Vérifier dans trace-prod que les colonnes existent :
   ```python
   import duckdb
   con = duckdb.connect('/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb', read_only=True)
   con.execute("DESCRIBE <table>").fetchdf()
   ```
   Si une colonne manque → ARRÊTER, signaler à Boris, suggérer `/add-trace-prod`.

**Sortie** : un mapping clair `{nom_logique → {table, cols, type}}` validé.

## Step 2 — Plan de modifications & confirmation

**Actions** :
1. Présenter à Boris un **résumé synthétique** des modifications prévues :
   - Quelles lignes ajoutées à `refresh_cohort.py` (extraction trace-prod)
   - Quelles entries ajoutées à `pool.yaml`
   - Estimation du nombre de combos générés en plus (= `C(8+N, k-1)` pour `k=3..8`)
   - Estimation du temps de calcul (~2-3 min par 200 combos)
   - Nom proposé pour le livrable : `combined_v{N+1}_{slug}` (où `slug` = description courte des features ajoutées)
2. Demander **OK explicite** à Boris avant de modifier le code.

**Si Boris refuse ou veut ajuster** : arrêter, attendre les instructions.

## Step 3 — Édition de `cohort/refresh_cohort.py`

**Actions** :
1. Lire `cohort/refresh_cohort.py` pour identifier la zone SQL à étendre.
2. Pour chaque nouvelle colonne à extraire :
   - Localiser le bloc `WITH base AS ( SELECT ... FROM samples ... LEFT JOIN <table> ... )`
   - Ajouter une ligne `TRY_CAST(<alias>.<col> AS DOUBLE) AS <nom_export>,` au bon endroit
3. Préserver la cohérence du nommage (ex: `loyfer_3_myeloid_granulocyte` → on garde le pattern `<source_table_short>_<col>`).
4. Si jointure nouvelle nécessaire (ex: colonnes dans une nouvelle table de trace-prod), ajouter le `LEFT JOIN` correspondant.

Voir [references/refresh-cohort-edits.md](references/refresh-cohort-edits.md) pour les patterns d'édition validés.

**Sortie** : `cohort/refresh_cohort.py` modifié, prêt à régénérer un snapshot.

## Step 4 — Édition de `experiments/pool.yaml`

**Actions** :
1. Lire `experiments/pool.yaml` pour identifier la fin du fichier (après la dernière entry).
2. Ajouter les nouvelles entries selon leur type :
   - **Feature simple** : `source_col: <nom_colonne_input_tsv>`
   - **Bloc (groupe)** : `source_cols: [col1, col2, ...]`
3. Garder la cohérence avec la convention du fichier (description en français, suffixe sur le nom logique).

Voir [references/pool-yaml-edits.md](references/pool-yaml-edits.md) pour les exemples.

**Sortie** : `experiments/pool.yaml` étendu avec les nouvelles candidates.

## Step 5 — Régénérer snapshot + input.tsv

**Actions** :
1. Lancer en séquence :
   ```bash
   cd /home/blipinski/Pipeline/Feature/
   python3 cohort/refresh_cohort.py
   python3 experiments/prepare_inputs.py
   ```
2. Vérifier que le nouveau snapshot a bien les nouvelles colonnes :
   ```python
   import pandas as pd, glob
   latest = sorted(glob.glob('cohort/snapshot_*.parquet'))[-1]
   df = pd.read_parquet(latest)
   # Check que les nouvelles colonnes sont là et non-NA
   ```
3. Si les nouvelles colonnes sont entièrement NA → ARRÊTER, signaler à Boris (possible problème de jointure ou de table source).

**Sortie** : `cohort/snapshot_YYYY-MM-DD.parquet` et `experiments/input.tsv` à jour.

## Step 6 — Lancer le grid search

**Actions** :
1. Calculer le nombre attendu de combos :
   - N_total = somme(C(N_optional, k-1) pour k=3..8) où N_optional = (pool actuel - mvaf) + features ajoutées
   - Estimer le temps ≈ N_nouveaux × 2.5s / 6 workers
2. Demander confirmation à Boris **si N_nouveaux > 500** (run long).
3. Lancer en background :
   ```bash
   python3 experiments/grid_search.py --workers 6 > /tmp/grid_run.log 2>&1 &
   ```
4. Surveiller via le PID jusqu'à completion :
   ```bash
   while kill -0 $PID 2>/dev/null; do sleep 5; done
   ```

**Sortie** : nouveaux combos insérés dans `experiments/feature_runs.duckdb`.

## Step 7 — Identifier le best combo

**Actions** :
1. Requête SQL sur `feature_runs.duckdb` (READ-ONLY) :
   ```sql
   SELECT features, n_samples, auc_all, sens_95_active_nomut, sens_90_active_nomut
   FROM runs
   WHERE n_samples = <n_du_nouveau_snapshot>
   ORDER BY sens_95_active_nomut DESC, auc_all DESC
   LIMIT 10
   ```
2. Identifier aussi le best combo "avant" (sans les nouvelles features) pour la comparaison :
   ```sql
   SELECT features, n_samples, auc_all, sens_95_active_nomut
   FROM runs
   WHERE n_samples = <n_du_nouveau_snapshot>
     AND features NOT LIKE '%<nouvelle_feature_1>%'
     AND features NOT LIKE '%<nouvelle_feature_2>%'
     ...
   ORDER BY sens_95_active_nomut DESC, auc_all DESC
   LIMIT 1
   ```

**Sortie** : 2 combos identifiés (NEW = best avec nouvelles features, OLD = best sans).

## Step 8 — Créer le livrable `features/{nom}/`

**Actions** :
1. Choisir le nom du dossier (proposé en Step 2) : `combined_v{N}_{slug}`
   - Convention : incrémente `vN` (regarder les dossiers existants `features/combined_v*_*`)
2. Créer la structure :
   ```bash
   mkdir -p features/{nom}/{compute,model,eval/plots}
   ```
3. Copier les inputs gelés dans `compute/` :
   ```bash
   cp cohort/snapshot_*.parquet features/{nom}/compute/
   cp experiments/input.tsv features/{nom}/compute/
   ```
4. Créer `compute/compute.py` (documenter l'origine — cf. template livrable).
5. Créer `model/train.R` à partir du template `references/livrable-creation.md` :
   - Combo NEW = best identifié en Step 7
   - Combo OLD = best identifié en Step 7
   - 2 runs `build_combined_score_flex` avec mêmes folds (seed=42)
6. Lancer `train.R` :
   ```bash
   cd features/{nom}/model && Rscript train.R 2>&1 | tee train.log
   ```
7. Créer `eval/evaluate.py` (peut être un copy-edit de `features/combined_v2_probs/eval/evaluate.py`).
8. Lancer `evaluate.py` :
   ```bash
   cd /home/blipinski/Pipeline/Feature/
   python3 features/{nom}/eval/evaluate.py 2>&1 | tee features/{nom}/eval/eval.log
   ```
9. Créer `README.md` + `config.yaml` (cf. template livrable).

Voir [references/livrable-creation.md](references/livrable-creation.md) pour les templates complets.

**Sortie** : livrable complet et reproductible dans `features/{nom}/`.

## Step 9 — Restitution finale à Boris

**Actions** :
1. Présenter à Boris un résumé court :
   - Liste des features ajoutées
   - Best combo NEW + ses KPIs (AUC, Sens@95% Active_NoMut)
   - Comparaison NEW vs OLD (Δ sur chaque KPI principal)
   - Chemin du livrable créé
   - Suggestions : si les nouvelles features sont dans le top, garder ; sinon, éventuellement retirer du pool
2. **Ne PAS commit** automatiquement. Laisser Boris décider.

</workflow>

<references>

| Fichier | Quand le charger |
|---|---|
| `references/refresh-cohort-edits.md` | À l'étape 3, pour étendre les jointures et les TRY_CAST dans refresh_cohort.py |
| `references/pool-yaml-edits.md` | À l'étape 4, pour formater correctement les nouvelles entries |
| `references/livrable-creation.md` | À l'étape 8, pour générer train.R + evaluate.py + README + config |

</references>

<rules>

1. **Toujours read-only sur trace-prod** : `duckdb.connect(db, read_only=True)`. Jamais d'écriture (cf. golden rule `~/.claude/rules/duckdb.md` et CLAUDE.md du projet Feature/).
2. **Demander confirmation avant** : édition de fichier sources, lancement du grid (si > 500 combos), création du livrable.
3. **Pas de commit automatique** — Boris décide quand committer.
4. **Si une colonne n'existe pas dans trace-prod** : ARRÊTER et orienter vers `/add-trace-prod`. Ne JAMAIS modifier le schéma de trace-prod depuis ce skill.
5. **Snapshot existant : ne JAMAIS écrasé** — `refresh_cohort.py` fait déjà le versioning `_v2`, `_v3`. Respecter ce comportement.
6. **Si erreur en cours de pipeline** : remonter l'erreur clairement à Boris, ne pas continuer aveuglément.

</rules>
