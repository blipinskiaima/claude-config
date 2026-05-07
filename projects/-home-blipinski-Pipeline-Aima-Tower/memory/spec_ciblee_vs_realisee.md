---
name: Spec ciblée vs Spec réalisée — explication synthétique
description: Différence entre target_specificity (slider) et Spec_AI calculée — pourquoi ça diverge
type: project
originSessionId: e7cf4774-71b7-41ae-a4bc-9bc5a148a559
---
# Spec ciblée vs Spec réalisée

## Définitions

| Terme | Code | Signification |
|---|---|---|
| **Spec ciblée** | `target_specificity` | Slider sidebar /exploration. Ce que l'utilisateur **demande** (par défaut 85%) |
| **Spec réalisée** | `Spec_AI` (= colonne tableau Detection) | Spec **vraiment obtenue** = `nb_healthy_score≤threshold / nb_healthy_total` |

## Pourquoi ça diverge (cas typique 85% → 89.1%)

Le seuil est calculé par `quantile(healthy_scores, target_specificity, type=6)` (méthode R Weibull, validée bit-exact vs R main).

Sur **N healthy fini** (192), le quantile retombe sur des valeurs discrètes : tu ne peux pas demander "exactement 85% spec" → le système retombe sur l'incrément le plus proche. Plus la distribution des scores healthy est **plate / quantifiée** (beaucoup de scores à 0 ou très bas), plus l'écart spec ciblée → réalisée peut être grand.

Exemple Boris (cohorte par défaut, 192 healthy) :
- target_specificity = 0.85 → quantile retombe sur threshold = 0.0
- 171/192 healthy ont un score ≤ 0 → **spec réalisée = 89.1%**

## Lecture

- **réalisée ≥ ciblée** (cas standard) : tu obtiens au moins ce que tu voulais. Plus c'est au-dessus, plus le seuil est conservateur (moins de FP, mais peut faire perdre de la sensibilité).
- **réalisée < ciblée** : seuil instable. Typique quand `n_healthy < 20` → l'UI flag en orange.

## Localisation UI

Bandeau collapse en haut de l'onglet Tableaux `/exploration` :
```
ⓘ Cohorte Sens/Spé ALL : 458 samples = 266 cancer + 192 healthy ▼
   └ Spec ciblée 85.0% (réalisée 89.1%) · Threshold 0.0000
```

## Pour aligner réalisée ≈ ciblée

Si l'écart est grand et qu'on veut serrer la spec :
1. Augmenter `target_specificity` (95% au lieu de 85%) si la distribution healthy le permet
2. Re-cibler la cohorte healthy (filtrer les outliers à score nul)
3. Améliorer le scoring (mvaf v2, calibration isotonic, etc.)

Voir aussi : `~/.claude/projects/-home-blipinski-Pipeline-Feature/memory/target-specificity.md` (convention 0.95 standard pour KPI Sens@95%).
