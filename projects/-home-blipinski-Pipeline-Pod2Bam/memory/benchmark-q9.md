# Benchmark --min-qscore 9 (2026-03-10)

## Contexte
- `--min-qscore 9` filtre les reads de qualité Q<9 au basecall (avant demux)
- Paramètre ajouté dans `nextflow.config` : `min_qscore = null` (null = pas de filtre)
- Dans `basecall.nf` : `def qscore_opt = params.min_qscore ? "--min-qscore ${params.min_qscore}" : ""`

## Résultats PBE25131 — V0.9.6_V5.0.0 Standard vs Q9

### Basecall
| Métrique | Standard | Q9 | Delta |
|----------|----------|-----|-------|
| Simplex basecalled | 13,260,467 | 11,714,403 | -1,546,064 (-11.7%) |
| Reads filtrés Q<9 | 8,445 (0.06%) | 1,585,569 (13.5%) | +1,577,124 |
| Durée basecall | 21 min | 22 min | +1 min |

### Demux — impact sur unclassified
| Métrique | Standard | Q9 | Delta |
|----------|----------|-----|-------|
| Unclassified reads | 1,366,337 | 369,777 | **-996,560 (-73%)** |
| % unclass / basecalled | 10.3% | 3.2% | **-7.1 pts** |

### Par sample (primary reads dans BAM final sorted)
| Sample | Standard primary | Q9 primary | Delta |
|--------|-----------------|------------|-------|
| Healthy_785 (bc13) | 5,912,314 | 5,642,764 | -269,550 (-4.6%) |
| Healthy_786 (bc15) | 3,328,275 | 3,173,378 | -154,897 (-4.7%) |
| Healthy_792 (bc14) | 2,194,601 | 2,064,732 | -129,869 (-5.9%) |
| Healthy_798 (bc16) | 519,782 | 493,745 | -26,037 (-5.0%) |
| **Total classifié** | **11,954,972** | **11,374,619** | **-580,353 (-4.9%)** |

### Mapping rate (primary mapped)
| Métrique | Standard | Q9 |
|----------|----------|-----|
| Mapping rate moyen | ~94% | ~96% (+2 pts) |

## Conclusions clés
- **Q9 filtre 13.5% des reads** au basecall (1.6M reads de Q<9)
- **Unclassified chute de 10.3% → 3.2%** : la majorité des unclassified étaient des reads de mauvaise qualité
- **Mapping rate augmente** de ~94% → ~96% (+2 pts) — meilleure qualité globale
- **Perte nette de primary classifiés** : -580K (-4.9%)
- **Trade-off** : on perd ~5% des reads classifiés mais qualité bien supérieure
- **Durée quasi identique** : le filtrage Q9 n'accélère pas significativement le basecall

## Commandes lancées
```bash
# Standard V0.9.6_V5.0.0 PBE25131 (déjà fait)
# Q9 V0.9.6_V5.0.0 PBE25131
nohup bash ~/Pipeline/Pod2Bam/test/best_strat_healthy/launch_v096_v50_q9_pbe25131.sh > /scratch/run/launch_v096_v50_q9_pbe25131.out 2>&1 &
```

## Tests PBE29634 — EN COURS (2026-03-10)
- **Run** : 20250602_1538_P2I-00117-B_PBE29634_025176a5 (110 GB, 71 POD5)
- **Barcodes** : bc21→Healthy_805, bc22→Healthy_807, bc23→Healthy_808, bc24→Healthy_815
- **Test 2** : V0.9.6_V5.0.0 standard → en cours (basecall terminé, demux en cours)
- **Test 3** : V0.9.6_V5.0.0 Q9 → en attente
- Scripts : `launch_v096_v50_pbe29634.sh`, `launch_v096_v50_q9_pbe29634.sh`
- Workdir : `/scratch/nxf-work/pbe29634_v096_v50/` et `pbe29634_v096_v50_q9/`
