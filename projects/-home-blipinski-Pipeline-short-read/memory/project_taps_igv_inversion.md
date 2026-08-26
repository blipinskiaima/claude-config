---
name: TAPS IGV color inversion fix
description: IGV bisulfite mode inverts TAPS methylation colors (blue=methylated instead of red). Fix by adding MM/ML tags to BAM and using Base Modification coloring mode.
type: project
---

IGV has no TAPS mode — bisulfite coloring shows inverted colors for Watchmaker TAPS data (blue=methylated, red=unmethylated). Script `add_mmml_taps.py` rewrites C→T (fwd) / G→A (rev) back to canonical bases and adds MM/ML tags encoding 5mC, enabling correct IGV "Color by Base Modification" display (red=methylated).

**Why:** TAPS chemistry converts methylated C→T (opposite of bisulfite where unmethylated C→T). IGV bisulfite mode is hardcoded for bisulfite convention — confirmed by IGV maintainer (issue #955), no fix planned.

**How to apply:** Use `add_mmml_taps.py <input.bam> <output.bam> <ref.fa>` then in IGV: right-click BAM → Color alignments by → Base Modification (5mC). Script location: `/scratch/short-read/Methylseq/add_mmml_taps.py` — **PERDU** : jamais commite, et `/scratch/short-read/` a ete nettoye. A rerecrire si besoin : lire le tag `XM:Z` sur les BAM DRAGEN (present sur 89,5 % des reads MAPQ>=20 proper-pair), comparer read vs reference sur les BAM BWA-mem2 (aucun tag de methylation).
