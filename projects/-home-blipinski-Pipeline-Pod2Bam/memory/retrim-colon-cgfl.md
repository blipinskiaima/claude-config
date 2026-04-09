---
name: Colon CGFL liquid — 5 runs re-basecallés V5.0.0 (TERMINÉ)
description: 5 runs Colon CGFL re-basecallés V0.9.6_V5.0.0 (2 _OK subset + 3 full dataset), 20 BAMs produits
type: project
originSessionId: 2b9dcc8a-acfe-4021-8624-386dfb8960d0
---

## Statut : TERMINÉ 2026-04-09

5 runs Colon CGFL re-basecallés avec pipeline V0.2.0 (trim gate actif). Tous les résultats sync S3 OK.

## Les 5 runs traités

| Run ID | S3 préfixe | POD5 | Samples |
|---|---|---|---|
| `962143e5_pod5_rep1_OK` | `...962143e5 = OK/pod5_rep1/` | 23 / 62G | Colon_17-20_rep1 (subset) |
| `962143e5_pod5_rep2_OK` | `...962143e5 = OK/pod5_rep2/` | 37 / 62G | Colon_17-20_rep2 (subset) |
| `2347816e_pod5_rep1` | `...2347816e=OK/pod5_rep1/` | 90 / 469G | Colon_21-24_rep1 |
| `962143e5_pod5_rep1` | `...962143e5/pod5_rep1/` | 66 / 308G | Colon_17-20_rep1 (full) |
| `962143e5_pod5_rep2` | `...962143e5/pod5_rep2/` | 50 / 144G | Colon_17-20_rep2 (full) |

**Important** : les préfixes `= OK/` contiennent un **sous-ensemble** du dataset (BAMs ~6x plus petits), les préfixes sans `= OK` contiennent le **full dataset**. On traite les deux pour comparer.

## Bug S3 sync Scaleway — FIX dans prefetch()

**Why:** `aws s3 sync` sur Scaleway skip silencieusement des fichiers (observé 3-5 manquants sur 23-90, de façon aléatoire). Cause probable : race condition pendant sync multipart ou eventually-consistent listing.

**How to apply:** `prefetch()` dans `dev/Pod2Bam_retrim_colon_cgfl.sh` retry le sync jusqu'à 5 fois tant que `local_count < s3_count`. Reproductible sur plusieurs runs : 2 tentatives suffisent généralement.

## Bug S3 path — fix

Le chemin correct est `s3://aima-pod-data/**data/**CGFL/liquid/...` et pas `s3://aima-pod-data/CGFL/liquid/...`. Le script initial utilisait le mauvais préfixe → `aws s3 sync` retournait silencieusement 0 fichier (au lieu d'une erreur).

## Résultats S3

**BAMs align_trimmed** : `s3://aima-bam-data/processed/Pod2Bam/RetD/{RUN_ID}/V0.9.6_V5.0.0/align_trimmed/{sample}/{sample}.bam`

**Log global batch** : `s3://aima-bam-data/processed/Pod2Bam/RetD/Pod2Bam_20260409_120015.log`

**Copies BAM → data/CGFL/liquid/** (20 copies, pattern `{sample}_OK/{sample}.bam` pour runs _OK et `{sample}/{sample}.bam` pour full) : destinations vérifiées inexistantes avant copie, aucun écrasement. Lignes `aws s3 cp` listées explicitement (préférence utilisateur : pas de boucle, lisibilité).

## Config finale du script

- `RUNS` : 5 clés
- `S3_POD5_MAP` : 5 entrées avec préfixe `data/`
- `MAX_LOCAL=4` (sliding window prefetch)
- `prefetch()` : retry loop 5x
- VERSION `V0.9.6_V5.0.0`
- Pipeline V0.2.0 : `basecall --trim adapters` → `demux_trimmed` → `align_trimmed` → sort/index

## TSV barcode sheets (5)

Dans `tables/` :
- `20250917_1048_P2I-00117-A_PBG10934_962143e5_pod5_rep1.tsv` (Colon_17-20_rep1)
- `20250917_1048_P2I-00117-A_PBG10934_962143e5_pod5_rep1_OK.tsv` (même contenu, suffix `_OK`)
- `20250917_1048_P2I-00117-A_PBG10934_962143e5_pod5_rep2.tsv` (Colon_17-20_rep2)
- `20250917_1048_P2I-00117-A_PBG10934_962143e5_pod5_rep2_OK.tsv` (même contenu, suffix `_OK`)
- `20250917_1218_P2S-01677-B_PBE78731_2347816e_pod5_rep1.tsv` (Colon_21-24_rep1)

## Timings (batch 2026-04-09, début 12:00)

| Run | Basecall |
|---|---|
| rep1_OK (62G) | ~18 min |
| rep2_OK (62G) | ~20 min |
| 2347816e (469G) | ~1h50 |
| rep1 (308G) | ~2h15 |
| rep2 (144G) | ~47 min |

Durée totale batch : ~5h30 (12:00 → 17:21). Aucune erreur, tous pipelines exit=0.
