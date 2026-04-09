---
name: Colon CGFL liquid — 12 samples NO_TRIM à re-traiter
description: 12 Colon_*_rep* liquid CGFL avec adaptateur ONT non trimmé, POD5 en Glacier dégelés, tables barcode créées
type: project
originSessionId: 2b9dcc8a-acfe-4021-8624-386dfb8960d0
---
## Contexte (2026-04-08)

Scan trim sur 1148 BAMs `*.merged.bam` via `samtools view | head -50 | grep TTGCTAAGGTTAA` (motif adaptateur LA ONT). 12 samples liquid CGFL identifiés NO_TRIM (adaptateur encore présent dans les reads) → à re-basecaller/re-trimmer.

**Why:** les BAMs MinKNOW de ces runs n'ont pas eu `dorado trim`/`demux` avec trim activé, contrairement à la majorité. Impact suspecté sur alignement (secondary/supplementary), cf `memory/trim-investigation.md`.

**How to apply:** utiliser les 3 TSV barcode sheets créés dans `tables/` pour lancer Pod2Bam sur ces runs quand le restore Glacier sera terminé.

## Les 12 samples NO_TRIM + mapping POD5 S3

| Sample | Run ID | Barcode | POD5 S3 subdir |
|---|---|---|---|
| Colon_17_rep1 | 962143e5 | barcode19 | `962143e5 = OK/pod5_rep1/` |
| Colon_18_rep1 | 962143e5 | barcode28 | `962143e5 = OK/pod5_rep1/` |
| Colon_19_rep1 | 962143e5 | barcode30 | `962143e5 = OK/pod5_rep1/` |
| Colon_20_rep1 | 962143e5 | barcode32 | `962143e5 = OK/pod5_rep1/` |
| Colon_17_rep2 | 674c0e00 | barcode19 | `962143e5 = OK/pod5_rep2/` |
| Colon_18_rep2 | 674c0e00 | barcode28 | `962143e5 = OK/pod5_rep2/` |
| Colon_19_rep2 | 674c0e00 | barcode30 | `962143e5 = OK/pod5_rep2/` |
| Colon_20_rep2 | 674c0e00 | barcode32 | `962143e5 = OK/pod5_rep2/` |
| Colon_21_rep1 | 2347816e | barcode22 | `2347816e=OK/pod5_rep1/` |
| Colon_22_rep1 | 2347816e | barcode23 | `2347816e=OK/pod5_rep1/` |
| Colon_23_rep1 | 2347816e | barcode27 | `2347816e=OK/pod5_rep1/` |
| Colon_24_rep1 | 2347816e | barcode29 | `2347816e=OK/pod5_rep1/` |

Bucket : `s3://aima-pod-data/CGFL/liquid/`

Note : les rep2 de Colon_17-20 sont un run **différent** (674c0e00, flowcell PBE78709) mais leurs POD5 sont stockés sous le préfixe 962143e5 dans un sous-dossier `pod5_rep2/`.

## Samples déjà TRIMMED (pas besoin de retraiter)

- **Colon_21/22/23/24_rep2** (run c73e2cf4, POD5 dans `2347816e=OK/pod5_rep2/`) → déjà TRIMMED (0/50). Sont dégelés quand même car le restore prend tout le préfixe.

## Restore Glacier

Script : `restore_glacier_cgfl.sh`. Dégèle tous les objets DEEP_ARCHIVE des 2 préfixes :
- `CGFL/liquid/20250917_1048_P2I-00117-A_PBG10934_962143e5 = OK/` → couvre pod5_rep1 + pod5_rep2
- `CGFL/liquid/20250917_1218_P2S-01677-B_PBE78731_2347816e=OK/` → couvre pod5_rep1 + pod5_rep2
- Tier Bulk, 7 jours.

## TSV barcode sheets créés

Dans `tables/` :
- `20250917_1048_P2I-00117-A_PBG10934_962143e5_pod5_rep1.tsv` (4 rep1 Colon_17-20)
- `20250917_1048_P2I-00117-A_PBG10934_962143e5_pod5_rep2.tsv` (4 rep2 Colon_17-20)
- `20250917_1218_P2S-01677-B_PBE78731_2347816e_pod5_rep1.tsv` (4 rep1 Colon_21-24)

## Script de lancement GPU

`dev/Pod2Bam_retrim_colon_cgfl.sh` — copie surgicale de `Pod2Bam_colon.sh`.
- VERSION `V0.9.6_V5.0.0` (Dorado 0.9.6 + modèle V5.0.0)
- Pipeline V0.2.0 : basecall → demux_trimmed → align_trimmed → sort/index
- Sliding window `MAX_LOCAL=3` : prefetch POD5 en background, GPU handoff via trace file, finalize/upload background
- `S3_POD5_MAP` bash assoc array pour paths Scaleway non-standard (espaces, `=`)
- `SCRIPT_DIR="$(dirname)/.."` car script dans `dev/`, racine projet au-dessus
- Paramètres NF : `--kit_name SQK-NBD114-96 --min_qscore 9 -profile docker,tower,scw`
- **Lancement** : `tmux new -s retrim_colon "bash ~/Pipeline/Pod2Bam/dev/Pod2Bam_retrim_colon_cgfl.sh"`
- **Prêt à lancer** : dégel Glacier terminé, POD5 disponibles sur Scaleway

## Vérif avant lancement

1. `aws s3 ls --profile aws "s3://aima-pod-data/CGFL/liquid/20250917_1048_P2I-00117-A_PBG10934_962143e5 = OK/pod5_rep1/" | head` — doit renvoyer des POD5 (pas Glacier)
2. `bash -n dev/Pod2Bam_retrim_colon_cgfl.sh` — syntax OK
3. `ls tables/20250917_*.tsv` — 3 TSV présents
4. GPU libre (pas de basecall en cours)
5. `/scratch` dispo (prévoir ~500 Go pour 3 POD5 + résultats)

## Méthode de détection trim utilisée

```bash
samtools view /mnt/.../{sample}.merged.bam | head -50 | awk -F'\t' '{print substr($10,1,60)}' | grep -c TTGCTAAGGTTAA
```
- `>=10/50` = NO_TRIM (adaptateur LA ONT visible)
- `0/50` = TRIMMED
- entre = UNCERTAIN
- Streaming depuis le mount, pas de copie locale, quelques secondes par BAM.

Résultats complets : `/scratch/colon_17_rep_invest/trim_scan_all.tsv` (1148 samples)
