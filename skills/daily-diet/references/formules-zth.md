# Formules ZTH — moteur de recalcul

> Formules EXACTES du calculateur officiel Zero_to_Hero_Calculator.xlsx (vérifiées cellule par cellule — voir docs/zth-calculator.md du projet ZTHapp). À utiliser pour tout recalcul de cibles ou rééquilibrage de repas.

## Cibles caloriques et macros

```
BMR1 = 13.707×poids + 492.3×taille_m − 6.673×âge + 77.607
BMR2 = 21.6×poids×(100−BF)/100 + 370          (Katch-McArdle)
BMR  = (BMR1 + BMR2) / 2
Maintenance = BMR × 1.5                        (facteur fixe du programme)

Masse maigre (LBM) = poids × (100−BF)/100
Protéines (g) = (poids×1.5 + LBM×2) / 2        VERROUILLÉ toutes phases
Lipides   (g) = 1.2 × LBM                      VERROUILLÉ toutes phases
Glucides  (g) = (kcal_phase − P×4 − L×9) / 4   seule variable
```

Phases P3 : maintien = Maintenance · initiale = −300 · étape 1 = −500 (si stagnation ≥2 sem) · JAMAIS au-dessus du maintien. Règle d'ajustement universelle : **−100 kcal = −25 g de glucides** (P et L intouchés).

Vérification (Boris 30 ans / 1.67 m / 64.5 kg / 20 %) : BMR1 1583.7 · BMR2 1484.6 → BMR 1534.1 → maintenance 2301 → déficit 2001 · P 100 · L 62 · G 261.

## Valeurs nutritionnelles des aliments du plan (par unité, source app/lib/foods.ts)

| Aliment | Unité | Kcal | P | L | G |
|---|---|---|---|---|---|
| Œuf | 1 | 70 | 6.3 | 5 | 0.4 |
| Tomate moyenne | 1 | 22 | 1 | 0.2 | 4 |
| Pomme Golden | g | 0.54 | 0.003 | 0.002 | 0.135 |
| Huile d'olive | g | 9 | 0 | 1 | 0 |
| Riz cru | g | 3.4 | 0.075 | 0.012 | 0.748 |
| Pain de mie complet | g | 2.51 | 0.092 | 0.038 | 0.45 |
| Aiguillettes poulet | g | 1.17 | 0.235 | 0.02 | 0 |
| Leerdammer | g | 3.56 | 0.275 | 0.27 | 0.005 |
| Mayonnaise | g | 6.6 | 0.012 | 0.73 | 0.01 |
| Mâche | g | 0.18 | 0.02 | 0.003 | 0.014 |
| Banane | g | 0.89 | 0.011 | 0.003 | 0.228 |
| Miel | g | 3.04 | 0 | 0 | 0.82 |
| Pomme de terre | g | 0.79 | 0.02 | 0.001 | 0.18 |
| Pâtes crues | g | 3.65 | 0.13 | 0.013 | 0.74 |
| Steak haché 5% | g | 1.55 | 0.21 | 0.05 | 0 |
| Thon émietté | g | 0.94 | 0.21 | 0.01 | 0 |

## Méthode de rééquilibrage d'un dîner (verrou lipides)

Budget dîner = kcal_phase − 896 (Raptor Club fixe).

1. Poser les protéines du repas (fixes : 4 œufs, ou 125 g steak, etc.)
2. Calculer L du repas hors huile et féculent → **huile (g) = L_cible_dîner − L_déjà_présent** où L_cible_dîner = 62 − 33.9 (Club) ≈ 28
3. Le féculent comble les kcal restantes : **féculent (g) = (budget − kcal_déjà_posées − 9×huile) / kcal_par_g**
4. Arrondir à des quantités pesables (multiples de 5 g), vérifier total ±15 kcal

Exemple (Riz Œuf, déficit 2001) : base 4 œufs+pomme 250+3 tomates = 481 kcal, L 21.1 → huile ≈ 5 g → riz = (1105−481−45)/3.4 ≈ 170 g → 1104 kcal, L repas 28.1, L jour 62 ✓.

## Rythme attendu (pour interpréter les bilans)

- Déficit −300 + 10 000 pas : −0.25 à −0.35 kg de gras/semaine sur le poids bas hebdo
- 1 kg de gras ≈ 9 000 kcal (référentiel PDF pour chiffrer les écarts)
- Semaine avec 1 resto : déficit hebdo ≈ −1800 kcal ≈ −0.23 kg — le resto est budgété, pas un échec
