---
name: small-fragment-mvaf-degradation
description: Le filtrage Small_Fragment dégrade la mVAF — zéro gain de sensibilité et 3x plus de faux positifs, mesuré sur 990 échantillons appariés
metadata:
  type: project
---

Mesuré le 2026-09-15 sur la base trace-prod, **990 échantillons liquid appariés** ayant à la fois `qc_metrics.mvaf_v1` et `small_fragments_metrics.mvaf_v1_small_fragments`.

**Le filtrage en fragments courts n'apporte rien à la mVAF, et dégrade la spécificité.**

```
TUMORAUX (n=704)
  mVAF complet        moy 3.344   médiane 1.223
  mVAF small_frag     moy 3.370   médiane 1.239
  sur les 425 avec mVAF>1 : delta moyen −0.020, 46 % en hausse  → pile ou face

SAINS (n=286)
  faux positifs (mVAF>1)   complet     8/286
                           small_frag 25/286     → ×3
```

**Mécanisme** : le filtre `length(seq) 75-200` de `Small_Fragment_Filter` coûte **36 % de profondeur** (2,07× → 1,24× en médiane sur 993 échantillons). La mVAF devient plus bruitée, et le bruit se traduit directement en faux positifs chez les sains.

**Why** : l'hypothèse « le cfDNA tumoral est plus court, donc filtrer les fragments courts enrichit le signal tumoral » est plausible mais **fausse en pratique ici** — l'enrichissement ne compense pas la perte de profondeur.

**How to apply** : ne pas proposer le filtrage par longueur de fragment comme levier d'amélioration de la mVAF, et ne pas relancer ce test. Si la piste est rouverte malgré tout, la fenêtre 75-200 est trop large — elle coupe un tiers de la profondeur sans cibler ; il faudrait tester 100-150 (vraie zone d'enrichissement tumoral) avec `Small_Fragment` qui existe déjà, pas avec un outil externe.

**Contexte connexe** : question posée initialement pour savoir s'il valait le coup de faire passer un BAM par `cfdna bam-to-bam` avant la mVAF. Réponse non, pour trois raisons cumulées — en mode défaut bam-to-bam ne filtre que 0,36 % des reads primaires, les poids GC qu'il écrit en tags AUX sont ignorés par modkit, et en mode filtrage agressif on retombe sur `Small_Fragment` dont ce document montre qu'il dégrade.

**Résultat annexe utile** : le biais GC n'affecte pas la mVAF (r = −0,18 chez les sains comme chez les tumoraux, n=28). L'absence de correction GC dans la chaîne méthylation — la seule de Bam2Beta est dans CNV, au niveau bin, LOWESS façon ichorCNA — **n'est donc pas un manque**. Rappel de la chaîne : `Preprocess_28M` filtre `-q 20 -F 3844`, puis 200 réplicats bootstrap, mVAF v1.4 = `mean(sqrt(scores))²` sans aucune correction, et v1.5 = v1.4 corrigée par la couverture EPIC (`raima::transfo_mvaf_by_cov`).
