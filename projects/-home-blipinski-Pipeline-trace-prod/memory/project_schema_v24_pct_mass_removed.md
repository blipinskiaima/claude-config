---
name: project-schema-v24-pct-mass-removed
description: "Bascule des métriques de longueur LIQUID vers QC/Samtools/{s}.n50_ratio.tsv bloc *_filtered (reads > 1kb écartés) via override LiquidChecker — le solid reste sur cramino — + schema v24 pct_mass_removed DECIMAL(5,2) liquid only, exporté sous '% Masse > 1kb'"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6a5dcc87-06b5-4ed0-8355-81a5e4b56941
  modified: 2026-08-12T10:57:08.780Z
---

# Bascule source liquid + schema v24 — pct_mass_removed (août 2026)

Deux changements du 11-12/08/2026, indissociables car **même fichier source**.

## 1. Bascule : le liquid ne lit plus cramino

| Scope | Source | Colonnes |
|---|---|---|
| **liquid** CGFL+HCL | `{s}/QC/Samtools/{s}.n50_ratio.tsv` | `n50_filtered`, `n75_filtered`, `ratio_n50_n75_filtered`, `pct_mass_removed` |
| **solid** CGFL | `{s}/QC/Cramino/{s}.merged.cramino.tsv` | `n50`, `n75` (ratio calculé) |

Le fichier a **12 colonnes** : un bloc brut (`n50`, `n75`, `ratio_n50_n75`) et un bloc filtré
(`*_filtered`, index 6-8), plus `pct_mass_removed` (idx 10) et `length_threshold` (idx 11, = 1000).

**Why:** Boris veut les métriques de longueur calculées **sans les reads > 1 kb**, qui écrasaient
la statistique sur certaines matrices.

**How to apply:**
- **Override dans `LiquidChecker`** (`_n50_ratio_value` + `_n50_ratio_decimal` + 4 getters).
  `BaseChecker` garde cramino → **le solid n'est pas touché**. Choix retenu contre une bascule
  globale (qui aurait mis le solid à `NA` au prochain check, régression différée) et contre un
  fallback automatique (qui aurait masqué la différence de définition).
  Précédent maison : `ShortReadChecker` override 4 méthodes de `BaseChecker`.
- ⚠ **`n50_ratio.tsv` n'existe pas en solid** (0/40 sondés) : le périmètre liquid est une
  **contrainte de données**, pas une préférence.
- ⚠ **La colonne `N50` a donc DEUX définitions selon l'onglet** : samtools filtré en liquid,
  cramino non filtré en solid. À dire avant toute comparaison liquid↔solid.
- Le **ratio est LU** dans le fichier (`ratio_n50_n75_filtered`), pas recalculé — demande explicite.
- ⚠ **Cramino et samtools ne donnent pas les mêmes chiffres même sur le bloc NON filtré**
  (`Healthy_13` : cramino 170/151 vs n50_ratio brut 171/154). La bascule n'est donc pas un simple
  retrait des reads longs : c'est aussi un changement d'outil.

**Effet mesuré sur 1324 liquides** : 805 n50 modifiés, 1148 n75, 1258 ratio ; **66 inchangés**
(aucun read > 1 kb). Le max n50 chute **6010 → 574**, le ratio max **20,58 → 2,20**, la
**médiane ne bouge pas** (174) — signature d'un filtre qui coupe une queue, pas d'un décalage global.

## 2. Schema v24 — `pct_mass_removed`

`qc_metrics.pct_mass_removed DECIMAL(5,2)`, **liquid uniquement**, export `% Masse > 1kb`
juste après `Ratio N50/N75` (position 11/55). Absent de `_SOLID_QC`.

= **% du yield porté par les reads > 1 kb**, donc écarté par le filtre. Mesuré : min `0,00`,
médiane `2,39`, max `81,40` (n=1324).

- ⚠ **`0,00` est une valeur légitime** (filtre sans effet — `Breast_49`, `Breast_50`), à ne pas
  confondre avec `NA` (fichier absent).
- Cette colonne **explique l'écart** entre valeurs cramino et valeurs filtrées, sample par sample :
  `TNE_2` 81,40 % (n50 6010 → 174), `Bladder_Urine_02_098` 75,67 %, `Colon_22_rep1/rep2`
  64,91/62,62 % — la cohérence entre réplicats se retrouve aussi ici.
- Type `DECIMAL(5,2)` : le fichier donne toujours exactement 2 décimales, jamais > 99,99.

## Gotchas transverses

- **`float('NaN')` / `float('inf')` ne lèvent PAS `ValueError`**, et `n50/inf = 0.0` est *fini*.
  Une garde `isfinite(résultat)` laisse donc passer un `0,0000` silencieusement faux.
  **Valider les deux OPÉRANDES.** Factorisé dans `_n50_ratio_decimal`.
- **Coordination multi-sessions** : une session parallèle a pris **v23** (table `qc`, cascade de
  comptage) et l'avait **déjà appliquée en base** — d'où v24 et non v23. ⚠ **Toujours vérifier
  `SCHEMA_VERSION` dans le working tree ET `_schema_version` en base** avant de bumper : le
  fichier `lib/duckdb.py` peut porter le bump non commité d'un autre chantier.
- **Backfill** : 811/819 CGFL + 513/513 HCL. Les 8 manquants sont des `Bladder_Urine_02_*`
  arrivés pendant la session, dont le pipeline n'a pas encore produit le fichier — pas un défaut.

**Vérifié** : contrôle croisé indépendant du fichier sur 4-6 samples à chaque étape (0 écart) ;
13 cas limites pour le ratio, 7 pour pct ; non-régression du solid (147/147 cramino intacts) ;
`typeof` = `DECIMAL(5,2)` ; relecture des onglets gsheet en valeurs brutes.

Liens : [[project-schema-v21-n50]] (état d'origine, resitué), [[project-schema-v22-n75-ratio]].
