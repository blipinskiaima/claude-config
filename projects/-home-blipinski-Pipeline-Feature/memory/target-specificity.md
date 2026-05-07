---
name: Target specificity (convention Feature/ et Aima-Tower)
description: Convention sur la spécificité ciblée pour calculer le seuil de classification — utilisée dans tous les KPI du tableau final et de l'évaluation Michael / Feature.
type: project
originSessionId: 35ba0796-87d1-48a8-900c-d868f78cbadf
---
# Spécificité ciblée — convention

Standard pour les comparaisons inter-features.

## Définition

```
   target_specificity = paramètre fixé qui décide où on coupe le score

   Algorithme :
     1. healthy_scores = scores_combined[is_healthy]
     2. threshold = quantile(healthy_scores, target_specificity, type=1)   # R type=1 = lower
     3. sens = mean(scores_cancer > threshold)
     4. spec_realized = mean(scores_healthy <= threshold)

   spec_realized peut différer légèrement de target_specificity à cause
   de la quantification (peu de healthy → peu de "marches" possibles
   pour le seuil).
```

## Valeurs utilisées

| `target_specificity` | Usage | Source |
|---|---|---|
| **0.95** | **STANDARD du tableau final** (KPI principal `Sens@95%`) | `09_*.R` Michael : `summary_at_95pct_specificity.csv` |
| 0.90 | Reporté en complément (Sens à un seuil plus permissif) | `02_sensitivity_specificity.R` legacy : `target_specificity = 0.90` |
| grille 0.80–1.00 par 0.01 | Pour les courbes Sens vs Spec dans `10_*.R` | `specificity_grid <- seq(0.80, 1.00, by = 0.01)` |

## Pour Aima-Tower — affichage utilisateur

Pour rendre la donnée auto-explicative dans l'UI, à chaque tableau de KPI,
afficher en haut :

```
   Cohorte : 454 samples (192 Healthy + 262 Cancer)
   Spécificité ciblée : 95.0%   ← spec_realized = 95.31% (172/192 healthy < threshold)
   Seuil correspondant : 0.7232 (sur le score combiné XGBoost)
```

Le `spec_realized` doit être lu comme "ce qu'on a réellement obtenu", pas
ce qui était demandé. Pour 192 healthy, la quantification donne des
incréments de 1/192 ≈ 0.5pp, donc spec_realized ∈ {94.79%, 95.31%, 95.83%}
autour d'une cible 0.95.

## Lien avec les autres KPI du tableau

Toutes les lignes `Sens@95%` du `tableau-final-kpi.md` reportent la
sensibilité au seuil défini par `target_specificity = 0.95` sur les
healthy de la cohorte de chaque combo. Toutes les lignes `Sens@90%`
utilisent target_specificity = 0.90.

Pour l'**AUC ALL/CGFL/HCL**, la valeur ne dépend pas du seuil (calculée
sur tous les rangs).

## Pourquoi 0.95

Choix arbitraire mais standard ISO 15189 / régulatoire : 95% spec = 5% FP
maximum, équivaut à un seuil de tolérance acceptable pour un test de
détection de cancer en routine clinique.

Pour le KPI **`Sens_Active_NoMut`** (KPI clé), la cible 95% reflète la
contrainte clinique : on accepte 5% de faux positifs sur des healthy en
échange d'un maximum de détection sur les cancers actifs sans mutation
détectable.
