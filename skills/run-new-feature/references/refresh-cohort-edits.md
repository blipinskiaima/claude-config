# Édition SQL cohorte — `scripts/01_prepare_cohort.py`

> **Mise à jour 2026-06** : remplace `archives/cohort/refresh_cohort.py`. Même logique SQL ; le script 01 écrit aussi `data/cohort.tsv` et les features dérivées.

## Anatomie du fichier

`scripts/01_prepare_cohort.py` extrait la cohorte depuis `trace-prod` (read-only), écrit un snapshot Parquet versionné et `data/cohort.tsv`.

Structure principale :
```python
con = duckdb.connect(TRACE_DB, read_only=True)
df = con.execute("""
    WITH base AS (
        SELECT ...                       ← bloc à étendre
        FROM samples s
        LEFT JOIN qc_metrics   q  ON s.id = q.sample_id
        LEFT JOIN retd_suivis  r  ON s.id = r.sample_id
        LEFT JOIN bam_metadata b  ON s.id = b.sample_id
        LEFT JOIN probs        p  ON s.id = p.sample_id
        LEFT JOIN metadata     m  ON s.id = m.sample_id
        WHERE ...
    ),
    ranked AS ( ... dedup unique_id ... )
    SELECT * FROM ranked WHERE rn = 1
""").fetchdf()
df.to_parquet(out_path)
```

## Pattern 1 — Nouvelle colonne dans une table existante

La table cible (ex: `qc_metrics`) a déjà un `LEFT JOIN`. Ajouter une ligne `TRY_CAST` :

```python
# AVANT
TRY_CAST(q.mvaf_v1     AS DOUBLE) AS mvaf_v1,
TRY_CAST(q.mvaf_v2     AS DOUBLE) AS mvaf_v2,
TRY_CAST(q.score_cnv   AS DOUBLE) AS score_cnv,

# APRÈS — ajout de la nouvelle colonne
TRY_CAST(q.mvaf_v1               AS DOUBLE) AS mvaf_v1,
TRY_CAST(q.mvaf_v2               AS DOUBLE) AS mvaf_v2,
TRY_CAST(q.score_cnv             AS DOUBLE) AS score_cnv,
TRY_CAST(q.mvaf_v1_short_read    AS DOUBLE) AS mvaf_v1_short_read,  ← nouveau
```

**Règles** :
- Utiliser `TRY_CAST(... AS DOUBLE)` (jamais `CAST` brut) pour gérer les NULL et les chaînes
- L'alias `AS <nom>` doit matcher le `source_col` qu'on mettra dans `feature.yaml`
- Préserver l'indentation existante (4 espaces, alignement des `AS`)

## Pattern 2 — Plusieurs nouvelles colonnes (bloc EPIC ou Loyfer)

Pour un bloc de N colonnes, ajouter N lignes `TRY_CAST` groupées avec un commentaire explicatif :

```python
# AVANT
TRY_CAST(p.testis_0    AS DOUBLE) AS prop_testis_0,
-- Loyfer 28M : 31 composantes tissulaires

# APRÈS — ajout d'un bloc EPIC short_read
TRY_CAST(p.testis_0    AS DOUBLE) AS prop_testis_0,
-- EPIC v1 SHORT READ : 16 composantes (BAM filtré 75-200 bp)
TRY_CAST(p.blood_0_short_read       AS DOUBLE) AS prop_blood_0_short_read,
TRY_CAST(p.breast_0_short_read      AS DOUBLE) AS prop_breast_0_short_read,
TRY_CAST(p.breast_1_short_read      AS DOUBLE) AS prop_breast_1_short_read,
TRY_CAST(p.colon_0_short_read       AS DOUBLE) AS prop_colon_0_short_read,
TRY_CAST(p.colon_1_short_read       AS DOUBLE) AS prop_colon_1_short_read,
TRY_CAST(p.kidney_1_short_read      AS DOUBLE) AS prop_kidney_1_short_read,
TRY_CAST(p.liver_0_short_read       AS DOUBLE) AS prop_liver_0_short_read,
TRY_CAST(p.liver_1_short_read       AS DOUBLE) AS prop_liver_1_short_read,
TRY_CAST(p.lung_0_short_read        AS DOUBLE) AS prop_lung_0_short_read,
TRY_CAST(p.lung_1_short_read        AS DOUBLE) AS prop_lung_1_short_read,
TRY_CAST(p.muscle_0_short_read      AS DOUBLE) AS prop_muscle_0_short_read,
TRY_CAST(p.ovary_0_short_read       AS DOUBLE) AS prop_ovary_0_short_read,
TRY_CAST(p.ovary_1_short_read       AS DOUBLE) AS prop_ovary_1_short_read,
TRY_CAST(p.prostate_0_short_read    AS DOUBLE) AS prop_prostate_0_short_read,
TRY_CAST(p.prostate_1_short_read    AS DOUBLE) AS prop_prostate_1_short_read,
TRY_CAST(p.testis_0_short_read      AS DOUBLE) AS prop_testis_0_short_read,
-- Loyfer 28M : 31 composantes tissulaires
```

## Pattern 3 — Nouvelle table à joindre

Si la nouvelle feature vient d'une table de `trace-prod` qui n'est PAS encore jointe (ex: nouvelle table `short_read_metrics`) :

```python
# AVANT
FROM samples s
LEFT JOIN qc_metrics   q  ON s.id = q.sample_id
LEFT JOIN retd_suivis  r  ON s.id = r.sample_id
LEFT JOIN bam_metadata b  ON s.id = b.sample_id
LEFT JOIN probs        p  ON s.id = p.sample_id
LEFT JOIN metadata     m  ON s.id = m.sample_id

# APRÈS — ajout du LEFT JOIN
FROM samples s
LEFT JOIN qc_metrics         q  ON s.id = q.sample_id
LEFT JOIN retd_suivis        r  ON s.id = r.sample_id
LEFT JOIN bam_metadata       b  ON s.id = b.sample_id
LEFT JOIN probs              p  ON s.id = p.sample_id
LEFT JOIN metadata           m  ON s.id = m.sample_id
LEFT JOIN short_read_metrics sr ON s.id = sr.sample_id      ← nouveau
```

Puis utiliser l'alias `sr.` dans le SELECT :
```python
TRY_CAST(sr.mvaf_v1_short_read AS DOUBLE) AS mvaf_v1_short_read,
```

## Vérification post-édition

```bash
# 1. Syntaxe Python valide
python3 -m py_compile cohort/refresh_cohort.py

# 2. Test à blanc — n'écrit pas mais valide la requête
python3 -c "
import duckdb
con = duckdb.connect('/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb', read_only=True)
# Lire le SELECT du script et l'exécuter avec LIMIT 1
"

# 3. Run complet
python3 cohort/refresh_cohort.py

# 4. Vérifier que les nouvelles colonnes sont dans le snapshot
python3 -c "
import pandas as pd, glob
latest = sorted(glob.glob('data/snapshots/snapshot_*.parquet'))[-1]
df = pd.read_parquet(latest)
new_cols = [c for c in df.columns if 'short_read' in c]
print(f'{len(new_cols)} nouvelles colonnes short_read :', new_cols[:5])
print(f'NA sur {new_cols[0]} : {df[new_cols[0]].isna().sum()}/{len(df)}')
"
```

## Anti-patterns

❌ Ne PAS modifier les filtres `WHERE` (filtres techniques validés)
❌ Ne PAS modifier la logique de dedup `unique_id` / `ranked` CTE
❌ Ne PAS écraser un snapshot existant — laisser la logique `_v2`, `_v3` faire son travail
❌ Ne PAS lire/écrire trace-prod sans `read_only=True`
❌ Ne PAS ajouter de nouvelles colonnes hors du bloc base de CTE — risque de casser la stratégie de dedup
