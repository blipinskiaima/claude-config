# Métriques suivies, réglages Exis et baseline T0

## Réglages de référence (figés)

Le suivi QARA se fait **toujours** dans le mode Exis 1.1. Ces réglages sont codés en dur
dans `scripts/qara_lib.py` et ne doivent pas changer (sinon la comparaison temporelle
perd son sens) :

| Réglage | Valeur | Rôle |
|---|---|---|
| `score_source` | `mvaf_v14` | Exis 1.1 = mVAF v1.4 |
| `cohort_mode` | `advanced` | cancers avancés, hors Lung-DI précoce (Exis §2.2) |
| `target_specificity` | `0.95` | calibration du seuil de positivité |
| `dorado_version` | `v5.0.0` + `v5.2.0` | versions de basecalling retenues |
| `min_depth` | `0.25` | profondeur de séquençage minimale |
| indications exclues | TNE, Nuclear, Bladder_Blood, Bladder_Urine | hors-cible, défaut UI |

## Baseline T0 — 24 juillet 2026

Valeurs mesurées à l'initialisation, alignées sur le rapport Exis 1.1 (SD-02) :

| Métrique | T0 |
|---|---|
| trace-prod — total | 1 471 (1 324 liquides + 147 solides) |
| Cohorte de calcul | 485 (261 cancers + 224 sains) |
| Sans étiquette (hors calcul) | 91 |
| Seuil de positivité | 0,0042 % |
| Sensibilité | 82 % (214/261) |
| Spécificité | 95,1 % (213/224) |
| VAF>2 % / VAF≤2 % / actif-sans-mut | 100 % (107/107) · 78,7 % (37/47) · 65,4 % (70/107) |
| Mode Précoce (§2.3, info) | 40,7 % (11/27) |

**Seul écart accepté vs le PDF** : `Prostate_21` (passé cancer le 23/07, après l'édition du
PDF du 06/07). C'est une différence de données, pas de méthode.

## Définitions métier (sources dans le code de la Tower)

Le skill n'implémente aucune de ces règles : il appelle les fonctions qui les contiennent.
Elles sont listées ici pour interpréter correctement les deltas.

- **Seuil de positivité** — quantile `type=1` (valeur observée chez un sujet sain, sans
  interpolation) du score des sains, au niveau de spécificité cible.
  `src/exploratory_compute.py::_quantile_r_type1`. Positif si `score > seuil`.
- **`cancer_truth`** — mutation détectée (`vaf > 0`) **OU** cancer actif déclaré
  (`active_cancer ∈ {yes,oui,y,1,true}`). `src/exploratory_compute.py::_add_flags`.
- **`healthy_flag`** — le nom de l'échantillon contient « Health ».
- **Cohorte Avancés** — exclut les échantillons `cohort = 'Lung-DI précoce'` (dépistage
  précoce, suivi à part). Sains toujours conservés (calcul du seuil).
- **Cohorte Précoce** — uniquement `cohort = 'Lung-DI précoce'` **et** `active_cancer = Yes`
  (règle stricte du §2.3 Exis).
- **Exclusion nommée** — `CGFL_26BM01841` est retiré (liste `_EXCLUDED_UNIQUE_IDS`).

## Ce que le skill mesure à chaque point

1. **Effectifs** — trace-prod (total et par type) vs cohorte de calcul de la Tower.
2. **Seuil** de positivité (recalculé à chaque fois sur les sains courants).
3. **Sensibilité** et **spécificité** globales, + strates VAF + par indication.
4. **Cascade** de filtrage (14 étapes, volumes).
5. **Statut par échantillon** (`unique_id → statut`) pour le diff nominatif.

## Statuts possibles d'un échantillon

Attribués aux échantillons qui passent les filtres techniques + profondeur + indications :

| Statut | Sens |
|---|---|
| `cancer` | compté cancer en mode Avancés (`cancer_truth`, hors précoce) |
| `sain` | donneur sain de référence (`healthy_flag`) |
| `sans_etiquette` | dans la cohorte Avancés mais ni cancer ni sain (statut clinique inconnu) |
| `precoce` | `cohort = 'Lung-DI précoce'` (exclu de la cohorte Avancés) |

Un échantillon **absent** du dictionnaire n'a pas passé les filtres amont (mauvaise version
dorado, profondeur insuffisante, réplicat technique, indication hors-cible, etc.).
