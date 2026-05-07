---
name: Cascade des filtres cohorte (Feature/ → Aima-Tower)
description: Documente la cascade exacte de filtres appliqués pour construire la cohorte d'évaluation des features cancer/healthy. Utilisable pour afficher en temps réel dans Aima-Tower l'effet de chaque filtre.
type: project
originSessionId: 35ba0796-87d1-48a8-900c-d868f78cbadf
---
# Cascade des filtres — projet Feature/ et Aima-Tower

Documentation des 7 étapes de filtrage qui transforment **les 1309 samples bruts de trace-prod**
en **454 samples scorés** par le top combo XGBoost (état du 2026-05-07).

## Pipeline complet (7 étapes)

```
ÉTAPE 0 : trace-prod brut                                                   1309
   └── tous les samples liquid + solid

ÉTAPE 1 : refresh_cohort.py — filtres techniques (snapshot Parquet)          709
   ├── sample_type = 'liquid'
   ├── prod_status = 'OK'
   ├── sample_name NOT LIKE '%_Alc_%'
   ├── sample_name NOT LIKE '%rebasecalled1%'
   ├── mvaf_v1 IS NOT NULL
   ├── dorado_model_version LIKE 'v5%'
   └── dedup unique_id (prefer_trimmed + pénalité bis/ter/quater/rep/moche)

ÉTAPE 2 : build_combined_score_flex — exclusion analytique 1                 685   (-24)
   └── NOT name LIKE '%(rep|moche|bis|ter|quater)%'
       (= duplicatas / reruns techniques NON éliminés à l'étape 1
          si le suffixe n'était pas en fin de nom)

ÉTAPE 3 : exclusion analytique 2                                             602   (-83)
   └── NOT name LIKE '%(TNE|Nuclear|Bladder_Blood)%'
       (= indications HCL R&D + bladder sang exclu de la grid)

ÉTAPE 4 : filtre profondeur                                                  557   (-45)
   └── depth >= 0.25
       (= pseudo-quantification minimale pour scorer un échantillon)

ÉTAPE 5 : dedup unique_id (slice 1)                                          557   (-0)
   └── group_by(unique_id) keep first
       (généralement no-op à ce stade car déjà fait à l'étape 1)

ÉTAPE 6 : label défini                                                       459   (-98)
   ├── is_healthy        = name LIKE '%Health%' (case insensitive)
   ├── is_mutated        = vaf_gene1_pct > 0
   ├── is_active_no_mut  = (vaf NA/0) AND active_cancer IN ('Yes','oui','TRUE','True')
   └── label = healthy ? 0 : (mutated OR active_no_mut) ? 1 : NA → exclus

   Les 98 retirés ici = samples sans label clair :
     - active_cancer = "probable" / "Suspicion" / "image suspecte"
     - active_cancer = "External quality control sample"
     - vaf NA + active_cancer NA / autre

ÉTAPE 7 : NOT NA sur les features XGBoost utilisées                          454   (-5)
   └── pour le top combo : mvaf_v1, mvaf_v2, ichor_tf, score_cnv,
                            frag_mode1, frag_mode2, loyfer_non_wbc
       (les 5 retirés = samples sans Loyfer 28M — props_loyfer_status = KO)
```

## Composition finale (top combo — état 2026-05-07)

```
                        Cancer    Healthy
   CGFL                   142        42
   HCL                    119       150
   ──────────────────────────────────────
   TOTAL                  262       192     →  454 samples
```

Cancers par indication × centre :
```
                Breast  Colon  Lung  Ovary  Pancreas  Prostate  Total
   CGFL            45     32    11      4         9        41    142
   HCL              0     37    76      0         6         0    119
```

## Pour Aima-Tower : afficher la cascade en temps réel

L'utilisateur fixe les filtres dans la sidebar `/exploration` ou `/analytics` Avancé.
Le compteur de cohorte affiche **après chaque filtre** :

```
   N samples : 459 (192H + 267C)         ← après filtres techniques + analytiques
   N modèle  : 454 (192H + 262C)         ← après NA sur features sélectionnées (-5)
   Threshold : quantile(healthy, 0.95) = X
   Sens      : 86.14% (sur 262 cancers)
```

Idéalement la sidebar liste **les 7 étapes** avec le compteur restant à chaque step,
en mode collapse pour ne pas saturer.

## Code reproductible (Python)

Le filtrage exact (étapes 2-7) est dans `score_one_combo.R` qui appelle
`build_combined_score_flex.R`. Pour Aima-Tower (Python), l'équivalent :

```python
def filter_cohort(df, feature_cols):
    """Reproduit les filtres de build_combined_score_flex.R"""
    n0 = len(df)
    df = df[~df["name"].str.contains("rep|moche|bis|ter|quater", na=False)]
    df = df[~df["name"].str.contains("TNE|Nuclear|Bladder_Blood", na=False)]
    df = df[df["depth"] >= 0.25]
    df = df.drop_duplicates("unique_id", keep="first")
    df["is_healthy"]  = df["name"].str.contains("Health", case=False, na=False)
    df["is_mutated"]  = df["vaf_gene1_pct"].fillna(0) > 0
    df["is_active_no_mut"] = (
        (df["vaf_gene1_pct"].isna() | (df["vaf_gene1_pct"] == 0))
        & df["active_cancer"].isin(["Yes", "oui", "TRUE", "True"])
    )
    df["label"] = pd.NA
    df.loc[df["is_healthy"],       "label"] = 0
    df.loc[df["is_mutated"],       "label"] = 1
    df.loc[df["is_active_no_mut"], "label"] = 1
    df = df.dropna(subset=["label"])
    df = df.dropna(subset=feature_cols)
    return df
```

## Lien avec le tableau final KPI

Toutes les colonnes du `tableau-final-kpi.md` reposent sur la même cascade.
Le `n_samples` reporté dans le tableau correspond au compteur final (étape 7,
post-filtre NA).

Voir aussi : `target-specificity.md` pour la définition du seuil utilisé.
