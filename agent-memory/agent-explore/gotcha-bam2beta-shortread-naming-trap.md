---
name: gotcha-bam2beta-shortread-naming-trap
description: dans l'historique Bam2Beta avant 2026-06-25, "short_read"/SHORT_READ désignait un filtre de longueur de fragment (75-200bp), pas du séquençage court-lu
metadata:
  type: project
---

Avant le commit `d6d4556` (2026-06-25) dans `~/Pipeline/Bam2Beta`, `params.SHORT_READ` et
`workflow/short_read_filter.nf` filtraient des reads ONT de 75-200bp (petits fragments cfDNA) —
aucun rapport avec du séquençage Illumina/DRAGEN/rastair. Renommé en `SMALL_FRAGMENTS` /
`workflow/small_fragment.nf` précisément pour lever cette ambiguïté de nom.

**Why:** un grep "short" sur l'historique git de Bam2Beta remonte massivement ce flux de longueur
de fragment, pas des traces de vrai séquençage court-lu.
**How to apply:** en explorant Bam2Beta (ou tout projet Pipeline) pour des traces de "short-read"
(plateforme de séquençage), écarter les résultats "short_read"/SMALL_FRAGMENTS — ils désignent la
longueur de fragment, pas la techno de séquençage. Les vraies traces short-read-sequencing sont à
chercher via "rastair", "DRAGEN", "CX_report", "Watchmaker".
