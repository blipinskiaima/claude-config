# Dorado Custom Barcode TOML — Recherche complète

## Format TOML pour SQK-NBD114-96

### Scoring par défaut (built-in)

| Paramètre | Défaut | Description |
|---|---|---|
| `max_barcode_penalty` | 11 | Max edit distance pour classifier |
| `min_barcode_penalty_dist` | 3 | Gap min entre top-1 et top-2 candidats |
| `min_separation_only_dist` | 6 | Gap min quand max_barcode_penalty pas atteint |
| `barcode_end_proximity` | 75 | Barcode doit être à ≤75bp des extrémités |
| `flank_left_pad` | 5 | Bases supplémentaires flanc gauche |
| `flank_right_pad` | 10 | Bases supplémentaires flanc droit |
| `front_barcode_window` | 175 | Fenêtre de recherche début du read |
| `rear_barcode_window` | 175 | Fenêtre de recherche fin du read |
| `midstrand_flank_score` | 0.95 | Score min pour rejeter barcode mid-strand |

Score formula: `score = 1.0 - edit_distance / length(target_seq)`

### Flanking sequences SQK-NBD114-96

- Forward (mask1): `5' - ATTGCTAAGGTTAA - [barcode] - CAGCACCT - 3'`
- Reverse (mask2): `5' - GGTGCTG - [barcode_RC] - TTAACCTTAGCAAT - 3'`
- Pattern: `NB%02i` (NB01-NB96, built-in dans Dorado)

### TOML complet (défaut)

```toml
[arrangement]
name = "SQK-NBD114-96"
kit = "SQK-NBD114-96"
mask1_front = "ATTGCTAAGGTTAA"
mask1_rear = "CAGCACCT"
mask2_front = "GGTGCTG"
mask2_rear = "TTAACCTTAGCAAT"
barcode1_pattern = "NB%02i"
barcode2_pattern = "NB%02i"
first_index = 1
last_index = 96

[scoring]
max_barcode_penalty = 11
min_barcode_penalty_dist = 3
min_separation_only_dist = 6
barcode_end_proximity = 75
flank_left_pad = 5
flank_right_pad = 10
front_barcode_window = 175
rear_barcode_window = 175
midstrand_flank_score = 0.95
```

### TOML relaxé (pour réduire unclassified)

```toml
[scoring]
max_barcode_penalty = 14         # 11→14 : accepte plus d'erreurs
min_barcode_penalty_dist = 2     # 3→2 : moins de discrimination requise
min_separation_only_dist = 4     # 6→4
barcode_end_proximity = 100      # 75→100 : barcode plus loin des extrémités OK
front_barcode_window = 200       # 175→200
rear_barcode_window = 200        # 175→200
midstrand_flank_score = 0.98     # 0.95→0.98 : rejet mid-strand plus strict
```

### CLI

```bash
# Custom arrangement (override built-in)
dorado demux --barcode-arrangement /path/to/custom.toml input.bam --output-dir output/

# Si séquences custom (pas nécessaire pour NB01-96 built-in)
dorado demux --barcode-arrangement custom.toml --barcode-sequences custom_seqs.fasta input.bam
```

### Caveats

- **Bug scoring ignoré** : versions < ~0.8 ignoraient silencieusement les scoring params (issue #1490, résolu)
- Dorado 0.9.6 devrait supporter les scoring overrides
- `name` doit être unique (ne pas réutiliser "SQK-NBD114-96" exactement)
- `max_barcode_penalty` est le levier le plus impactant (au coût de potentiels faux positifs entre barcodes similaires)
- Issue #1178 : barcode_end_proximity 75→100 et windows 175→200 donnaient <1% amélioration seuls
- Causes architecturales d'unclassified : reads avec top-1 et top-2 barcodes différents aux 2 extrémités → toujours unclassified

### Sources
- GitHub dorado CustomBarcodes.md
- Issues #1178, #1490, #1124, #770, #626, #558
- ONT docs: software-docs.nanoporetech.com/dorado/latest/barcoding/custom_barcodes/

## Résultats investigation unclassified (2026-03-09)

### Tableau récap complet

| Variable | Config | Classified | Unclass | % unclass |
|----------|--------|-----------|---------|-----------|
| Trim | no_trim | 529,715 | 75,793 | 12.5% |
| Trim | trim_adapters | 529,715 | 75,793 | 12.5% |
| Trim | trim_all | 529,715 | 75,793 | 12.5% |
| Ordre | Pipeline C (align→demux) | 529,715 | 75,793 | 12.5% |
| Ordre | Pipeline B (demux uBAM) | 529,715 | 75,793 | 12.5% |
| Dorado | 0.9.6 | 529,715 | 75,793 | 12.5% |
| Dorado | 1.4.0 (V5.2.0) | 537,906 | 67,604 | 11.2% |
| Q-score | Q0 | 529,715 | 75,793 | 12.5% |
| Q-score | Q9 | 493,208 | 27,603 | 5.3% |
| MinKNOW | BS 7.6.7 | ~97.8% | ~2.2% | 2.2% |

### Profil reads unclassified (Q0)
- Q moyen = 15.1 (vs 27.4 classifiés)
- Longueur moyenne = 324bp (vs 231bp classifiés)
- Distribution Q : 12% Q<5, 52% Q5-8, 26% Q9-14, 8% Q15-19, 2% Q20+
- Distribution taille : bimodale (courts <50bp + longs >500bp max 25kb)

### Run Colon FC-A (PBA39351)
- 218 POD5, ~2.07 GB chacun, 452.6 GB total
- Run 66h, config "1 file/hour or 500M bases/batch"
- MinKNOW 24.11.8, Dorado BS 7.6.7
- Tests sur 1 POD5 (index 0) = 0.5% du dataset
