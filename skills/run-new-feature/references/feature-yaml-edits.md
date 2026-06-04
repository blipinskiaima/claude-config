# Édition de `data/feature.yaml`

## Anatomie du fichier

Format YAML simple, 1 entrée par feature candidate. Lu par `02_test_combo.py:148`.

```yaml
<nom_logique>:
  required: true           # OPTIONNEL — uniquement pour mvaf
  source_col: <col_tsv>    # PLURIEL → bloc, voir ci-dessous
  description: <texte fr>  # optionnel mais recommandé
```

## Pattern 1 — Feature simple (1 colonne)

Une feature simple = 1 colonne dans `cohort.tsv` → 1 colonne XGBoost.

```yaml
mvaf_v1_short_read:
  source_col: mvaf_v1_short_read
  description: mVAF v1 raima sur BAM filtré reads 75-200 bp (short-read)
```

**Convention** :
- `nom_logique` (clé du dict) = identifiant utilisé dans les combos, par convention identique à `source_col`
- Si différents (ex: `mvaf` → `mvaf_v1` après mutate côté R) : le mapping est géré par `score_one_combo.R:53-60` (mutate aliases)

## Pattern 2 — Feature bloc (≥ 2 colonnes)

Un bloc = N colonnes regroupées en 1 candidate. Le grid voit ce bloc comme 1 case à cocher, mais XGBoost reçoit les N colonnes.

```yaml
probs_epic_short_read:
  source_cols:
    - prop_blood_0_short_read
    - prop_breast_0_short_read
    - prop_breast_1_short_read
    - prop_colon_0_short_read
    - prop_colon_1_short_read
    - prop_kidney_1_short_read
    - prop_liver_0_short_read
    - prop_liver_1_short_read
    - prop_lung_0_short_read
    - prop_lung_1_short_read
    - prop_muscle_0_short_read
    - prop_ovary_0_short_read
    - prop_ovary_1_short_read
    - prop_prostate_0_short_read
    - prop_prostate_1_short_read
    - prop_testis_0_short_read
  description: Bloc 16 probs EPIC v1 calculées sur BAM filtré reads 75-200 bp
```

**Règles** :
- Le `expand_features()` de `02_test_combo.py:71-83` détecte `source_cols` (pluriel) et déplie automatiquement
- Aucune modification de code Python/R nécessaire pour supporter un nouveau bloc

## Où ajouter dans le fichier

Toujours **à la fin du fichier**, après la dernière entrée existante. Ordre conservé pour lisibilité et stabilité du combo_id (qui trie en interne via `sorted()`).

## Vérification post-édition

```bash
# 1. Syntaxe YAML valide
python3 -c "import yaml; yaml.safe_load(open('data/feature.yaml'))"

# 2. Compter les candidates dans le pool
python3 -c "import yaml; p=yaml.safe_load(open('data/feature.yaml')); print(f'{len(p)} features, {sum(1 for v in p.values() if v.get(\"required\"))} required')"

# 3. Estimer le nombre de combos
python3 -c "
import yaml, math
p = yaml.safe_load(open('data/feature.yaml'))
n_opt = sum(1 for v in p.values() if not v.get('required'))
total = sum(math.comb(n_opt, k-1) for k in range(3, 9))
print(f'{n_opt} optionnelles → {total} combos k=3..8')
"
```

## Anti-patterns

❌ Ne PAS dupliquer une feature existante avec le même `source_col`
❌ Ne PAS rendre une nouvelle feature `required: true` (seul `mvaf` doit l'être)
❌ Ne PAS mélanger `source_col` (singulier) et `source_cols` (pluriel) dans la même entry
❌ Ne PAS supprimer/renommer une feature existante depuis ce skill (impact cache + combos historiques)
