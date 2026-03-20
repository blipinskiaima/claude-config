---
name: BP_5base Colon50/Colon62 identical mVAF explained
description: Colon50 and Colon62 show identical mVAF (2.185) in BP_5base - confirmed as rounding, not a bug
type: project
---

Colon50 et Colon62 affichent le même mVAF (2.185) dans BP_5base_summary.tsv. Re-run complet depuis les CX_report le 2026-03-12 confirme :

- Colon50 : score PCA = 0.0432962 → mVAF = 2.185
- Colon62 : score PCA = 0.0432839 → mVAF = 2.185

**Why:** Les scores PCA sont très proches mais différents. L'arrondi à 3 décimales par raima::model_v1() fait converger les deux mVAF à la même valeur affichée. Ce n'est pas un bug.

**How to apply:** Si la question revient, c'est un arrondi confirmé par re-run. Les données d'entrée (CX_report, bed.gz) sont bien distinctes.
