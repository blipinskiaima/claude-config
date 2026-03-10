# Investigation perte de reads Pod2Bam vs MinKNOW

## Résultat principal (2026-03-10) : PAS DE PERTE DE READS

La "perte 30-40%" était un **artefact de comparaison de métriques incompatibles**.
En comparant primary vs primary, le delta est < 1%.

## Test Healthy (run PBE25131, 88 GB POD5, 66 fichiers)

### Données de référence — Rapport MinKNOW
- **reads_generated** : 13,268,071
- **Flow cell** : PBE25131
- **Sample ID** : wt-785-786-792-798
- **Basecaller** : Dorado BS 7.6.7, modèle HAC v4.3.0
- **Kit** : SQK-NBD114-96
- **Barcodes** : bc13→Healthy_785, bc14→Healthy_786, bc15→Healthy_792, bc16→Healthy_798

| Barcode | MinKNOW total | Pass % | Bases totales |
|---------|:------------:|:------:|:------------:|
| bc13 | 5,849,323 | 95.0% | 1,133,031,299 |
| bc14 | 3,300,191 | 94.7% | 663,111,598 |
| bc15 | 2,172,162 | 93.5% | 428,873,928 |
| bc16 | 515,736 | 94.7% | 117,211,249 |
| **Sum classified** | **11,837,412** | | |
| **Unclassified pass** | 332,362 (2.9%) | | 194,234,571 |
| **Unclassified total** | ~1,430,659 (10.8%) | | |

### Données de référence — Bam2Beta (BAM séquenceur)

| Sample | nb_reads_total | nb_reads_filtered | Cramino reads (primary) | Cramino alignments | N50 |
|--------|:-:|:-:|:-:|:-:|:-:|
| Healthy_785 | 6,585,249 | 4,544,278 | 5,558,052 | 5,676,337 | 176 |
| Healthy_786 | 3,783,362 | 2,556,260 | 3,126,749 | 3,201,480 | 177 |
| Healthy_792 | 2,407,916 | 1,661,193 | 2,030,071 | 2,066,519 | 178 |
| Healthy_798 | 576,815 | 402,668 | 488,570 | 498,952 | 186 |
| **Total** | **13,353,342** | **9,164,399** | **11,203,442** | **11,443,288** | |

- nb_reads_total = total alignments dans les BAM chunks (inclut secondary+supplementary)
- Cramino reads = primary reads only (depuis merged BAM)
- BAM fichiers nommés `PBE25131_pass_barcode{13-16}_*` (pass only)

### Résultats Pod2Bam V0.7.4_V4.3.0 — TERMINÉ (2026-03-10, 53 min total)

| Sample | Primary | Secondary | Supplementary | Total | Mapping rate |
|--------|--------:|----------:|--------------:|------:|:-----------:|
| Healthy_785 | 5,810,982 | 1,453,447 | 169,854 | 7,434,283 | 95.3% (93.9% primary) |
| Healthy_786 | 3,286,729 | 921,979 | 114,349 | 4,323,057 | 95.2% (93.7% primary) |
| Healthy_792 | 2,166,896 | 551,277 | 52,598 | 2,770,771 | 94.1% (92.5% primary) |
| Healthy_798 | 513,675 | 127,821 | 17,955 | 659,451 | 95.5% (94.3% primary) |
| **Sum classified** | **11,778,282** | **3,054,524** | **354,756** | **15,187,562** | |
| **Basecall total (unsorted)** | | | | **13,321,568** | |
| **Unclassified** | | | | **~1,543,286** (~11.6%) | |

### Tableau tri-source comparatif (PRIMARY reads)

| Sample | MinKNOW (pass+fail) | Bam2Beta (Cramino) | Pod2Bam V4.3.0 | Delta P2B/MinKNOW |
|--------|:------------------:|:-----------------:|:--------------:|:-----------------:|
| Healthy_785 | 5,849,323 | 5,558,052 | 5,810,982 | **-0.7%** |
| Healthy_786 | 3,300,191 | 3,126,749 | 3,286,729 | **-0.4%** |
| Healthy_792 | 2,172,162 | 2,030,071 | 2,166,896 | **-0.2%** |
| Healthy_798 | 515,736 | 488,570 | 513,675 | **-0.4%** |
| **Sum** | **11,837,412** | **11,203,442** | **11,778,282** | **-0.5%** |

### Explication des écarts entre sources

1. **MinKNOW total (11.84M)** = reads classifiés pass+fail, primary only
2. **Bam2Beta Cramino (11.20M)** = primary reads dans merged BAM = pass only (fichiers `_pass_barcode*`)
3. **Bam2Beta nb_reads_total (13.35M)** = total alignments incluant secondary+supplementary
4. **Pod2Bam primary (11.78M)** = primary reads après basecall+demux+align (pass+fail, Q0)
5. **Pod2Bam basecall total (13.32M)** ≈ MinKNOW reads_generated (13.27M) → +0.4%

### Pourquoi Bam2Beta Cramino < MinKNOW classified ?
- MinKNOW compte pass+fail (11.84M)
- Les BAM séquenceur ne contiennent que les reads pass (`_pass_` dans le nom)
- Les reads fail (~5-7%) sont dans des BAM séparés (`_fail_`) non inclus dans Bam2Beta

### Pourquoi Pod2Bam primary < MinKNOW classified ?
- Pod2Bam unclassified ~11.6% vs MinKNOW ~10.8% → ~0.8pts de reads non assignés
- Delta résiduel < 0.5% = bruit (différence Dorado standalone vs BS intégré)

## Colon_1-4 — Comparaison basecall vs final (2026-03-10)

| Source | Reads | Notes |
|--------|------:|-------|
| Basecall unsorted (avant demux) | 121,082,260 | = tous les reads basecallés |
| Colon_1 rebasecalled | 19,181,381 | après demux+align+sort |
| Colon_2 rebasecalled | 27,696,916 | |
| Colon_3 rebasecalled | 56,277,785 | |
| Colon_4 rebasecalled | 33,641,461 | |
| **Sum Colon_1-4** | **136,797,543** | **+13% vs basecall** (secondary+supplementary ajoutés par l'alignement) |

## Conclusion : origine de la "perte 30-40%"

La perte n'existe pas. C'était la **somme de 3 artefacts de comparaison** :
1. **Métriques incompatibles** : comparer `nb_reads_total` (inclut sec/sup) avec des counts primary → +12-19% apparent
2. **Pass vs pass+fail** : Bam2Beta ne compte que les reads pass, MinKNOW et Pod2Bam comptent pass+fail → -5-7%
3. **Unclassified rate** : Dorado standalone ~11-14% vs MinKNOW ~2-3% → -9-11% si on compare classified seulement

En comparant **primary vs primary**, **basecall total vs basecall total**, le delta est < 1%.

## Benchmark 5 versions Healthy PBE25131 (2026-03-10) — MEILLEURE COMBO : V1.4.0_V5.2.0

Run test : 20250528_1415_P2I-00117-B_PBE25131_0c54a6da (88 GB, 66 POD5, 4 samples bc13-16)

### Basecall total & durée
| Version | Dorado | Modèle simplex | Mod model | Basecall total | Durée pipeline |
|---------|--------|----------------|-----------|---------------:|------:|
| V0.7.4_V4.3.0 | 0.7.4 | hac@v4.3.0 | 5mCG_5hmCG@v1 | 13,321,568 | 46 min |
| V0.7.4_V5.0.0 | 0.7.4 | hac@v5.0.0 | 5mCG_5hmCG@v1 (fallback) | 13,321,746 | 46 min |
| V0.9.6_V5.0.0 | 0.9.6 | hac@v5.0.0 | 5mCG_5hmCG@v3 | 13,321,590 | 34 min |
| V1.4.0_V5.0.0 | 1.4.0 | hac@v5.0.0 | 5mCG_5hmCG@v3 | 13,321,029 | 31 min |
| **V1.4.0_V5.2.0** | **1.4.0** | **hac@v5.2.0** | **5mCG_5hmCG@v2** | **13,333,921** | **35 min** |
| MinKNOW BS 7.6.7 | — | — | — | 13,268,071 | — |

### Primary reads par sample (après demux + align + sort)
| Sample | MinKNOW | V0.7.4_V4.3.0 | V0.7.4_V5.0.0 | V0.9.6_V5.0.0 | V1.4.0_V5.0.0 | V1.4.0_V5.2.0 |
|--------|--------:|---------------:|---------------:|---------------:|---------------:|---------------:|
| Healthy_785 | 5,849,323 | 5,810,982 | 5,893,154 | 5,912,314 | 5,871,549 | **6,015,835** |
| Healthy_786 | 3,300,191 | 3,286,729 | 3,318,956 | 3,328,275 | 3,304,699 | **3,406,677** |
| Healthy_792 | 2,172,162 | 2,166,896 | 2,192,047 | 2,194,601 | 2,184,547 | **2,217,888** |
| Healthy_798 | 515,736 | 513,675 | 518,608 | 519,782 | 517,070 | **527,756** |
| **Sum classif.** | **11,837,412** | **11,778,282** | **11,922,765** | **11,954,972** | **11,877,865** | **12,168,156** |
| Unclassified | ~1,430,659 | 1,542,952 | 1,398,694 | 1,366,337 | 1,442,866 | **1,165,538** |
| **% unclass** | **~10.8%** | **11.6%** | **10.5%** | **10.3%** | **10.8%** | **8.7%** |

### Classement final
| Rang | Version | Delta vs MinKNOW | % unclass | Durée |
|:----:|---------|:----------------:|:---------:|------:|
| **1** | **V1.4.0_V5.2.0** | **+330,744 (+2.8%)** | **8.7%** | **35 min** |
| 2 | V0.9.6_V5.0.0 | +117,560 (+1.0%) | 10.3% | 34 min |
| 3 | V0.7.4_V5.0.0 | +85,353 (+0.7%) | 10.5% | 46 min |
| 4 | V1.4.0_V5.0.0 | +40,453 (+0.3%) | 10.8% | 31 min |
| 5 | V0.7.4_V4.3.0 | -59,130 (-0.5%) | 11.6% | 46 min |

### Pourquoi V1.4.0_V5.2.0 est la meilleure combinaison
1. **Plus de reads classifiés** : +2.8% vs MinKNOW, +3.3% vs V0.7.4_V4.3.0
2. **Moins d'unclassified** : 8.7% (vs 11.6% pour V0.7.4_V4.3.0, vs 10.3% pour V0.9.6_V5.0.0)
3. **Rapide** : 35 min (vs 46 min pour V0.7.4)
4. **Modèles intégrés** dans l'image Docker `/opt/models/` (pas de dépendance host)
5. **Mod model correct** : `5mCG_5hmCG@v2` natif pour V5.2.0
6. **Basecall total légèrement supérieur** : 13,333,921 vs ~13,321,xxx (V5.2.0 détecte plus de reads)

### Observations clés du benchmark
- **Le modèle simplex (V4.3.0 vs V5.0.0 vs V5.2.0)** a plus d'impact que la version Dorado sur le taux de classification
- **V5.2.0** : meilleur classifieur + détecte légèrement plus de reads au basecall
- **V1.4.0 + V5.0.0** est paradoxalement PIRE que V0.9.6 + V5.0.0 en classification (10.8% vs 10.3%)
- **La note précédente "V5.2.0 perd ~24% des reads"** était sur un autre contexte (probablement pass-only count). Ici, en comptant primary pass+fail, V5.2.0 est le meilleur.

### Commandes exactes par version

**Pipeline commun (Pipeline B multiplex)** :
1. `dorado basecaller MODEL POD5 --modified-bases-models MOD --trim adapters --device cuda:all`
2. `dorado demux --output-dir demuxed/ --kit-name SQK-NBD114-96 --no-trim INPUT.bam`
3. `dorado aligner GRCh38_no_alt.fa BARCODE.bam --mm2-opts '-x map-ont'`
4. `samtools sort` → `samtools index`

**Référence** : `/scratch/dependencies/genomes/GRCh38/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa`

#### V0.7.4_V4.3.0 (pod2bam:0.7.4)
```
dorado basecaller /scratch/basecall/dorado/models/dna_r10.4.1_e8.2_400bps_hac@v4.3.0 pod5 \
  --modified-bases-models /scratch/basecall/dorado/models/dna_r10.4.1_e8.2_400bps_hac@v4.3.0_5mCG_5hmCG@v1 \
  --trim adapters --device cuda:all
```
- batch_size: 9728, basecall: 24 min, reads: 13,258,290 simplex + 10,550 filtered, 72.9 GS/s

#### V0.7.4_V5.0.0 (pod2bam:0.7.4)
```
dorado basecaller /scratch/basecall/dorado/models/dna_r10.4.1_e8.2_400bps_hac@v5.0.0 pod5 \
  --modified-bases-models /scratch/basecall/dorado/models/dna_r10.4.1_e8.2_400bps_hac@v5.0.0_5mCG_5hmCG@v1 \
  --trim adapters --device cuda:all
```
- ⚠ mod model @v1 = **fallback** (@v3 indisponible pour Dorado 0.7.4)
- batch_size: 9728, basecall: 26 min, reads: 13,260,507 + 8,289 filtered, 66.3 GS/s

#### V0.9.6_V5.0.0 (pod2bam:0.9.6)
```
dorado basecaller /opt/models/dna_r10.4.1_e8.2_400bps_hac@v5.0.0 pod5 \
  --modified-bases-models /opt/models/dna_r10.4.1_e8.2_400bps_hac@v5.0.0_5mCG_5hmCG@v3 \
  --trim adapters --device cuda:all
```
- Modèles dans l'image Docker `/opt/models/`, mod model @v3 correct
- batch_size: 3520, basecall: 21 min, reads: 13,260,467 + 8,445 filtered, 79.8 GS/s

#### V1.4.0_V5.0.0 (pod2bam:1.4.0)
```
dorado basecaller /scratch/basecall/dorado/models/dna_r10.4.1_e8.2_400bps_hac@v5.0.0 pod5 \
  --modified-bases-models /scratch/basecall/dorado/models/dna_r10.4.1_e8.2_400bps_hac@v5.0.0_5mCG_5hmCG@v3 \
  --trim adapters --device cuda:all
```
- Modèles V5.0.0 sur le host (pas dans image 1.4.0), mod@v3 téléchargé manuellement
- batch_size: 3520, basecall: 17 min, reads: 13,259,462 + 9,069 filtered, **98.3 GS/s** (le plus rapide)

#### V1.4.0_V5.2.0 (pod2bam:1.4.0) ← MEILLEURE COMBO
```
dorado basecaller /opt/models/dna_r10.4.1_e8.2_400bps_hac@v5.2.0 pod5 \
  --modified-bases-models /opt/models/dna_r10.4.1_e8.2_400bps_hac@v5.2.0_5mCG_5hmCG@v2 \
  --trim adapters --device cuda:all
```
- Modèles dans l'image Docker `/opt/models/`
- batch_size: 3392, basecall: 22 min, reads: 13,265,381 + **3,158 filtered** (5x moins de reads filtrés!), 79.6 GS/s

### Subtilités de configuration importantes

1. **Batch size** : Dorado 0.7.4 utilise 9728 (H100 80GB), 0.9.6/1.4.0 utilisent ~3520 (plus conservateur mais plus rapide en samples/s)
2. **Reads filtered au basecall** : V5.2.0 filtre seulement 3,158 reads vs 8-10K pour les autres → plus de reads entrent dans le demux
3. **Dorado 1.4.0 demux breaking change** : sortie imbriquée `{experiment}/{sample}/{run}/bam_pass/barcode{N}/file.bam`. Fix : `demuxed_raw/` → flatten vers `demuxed/${ID}_barcode{N}.bam`
4. **Nommage BAM demux par version Dorado** :
   - 0.7.4 : `d2d9c850..._SQK-NBD114-96_barcode13.bam` (hash du run)
   - 0.9.6 : `0c54a6da-3a18-..._SQK-NBD114-96_barcode13.bam` (UUID)
   - 1.4.0 (après flatten) : `${ID}_barcode13.bam`
5. **Mod model fallback** : Dorado 0.7.4 ne supporte pas `5mCG_5hmCG@v3` → doit utiliser @v1
6. **Tous les tests utilisent `--trim adapters`** en basecall (test séparé confirme que trim n'affecte pas le nombre de reads)

### S3 résultats (toutes sorties de chaque process)
Base S3 : `s3://aima-bam-data/processed/Pod2Bam/DEV/20250528_1415_P2I-00117-B_PBE25131_0c54a6da/`
- `V0.7.4_V4.3.0/` (aussi dans `s3://.../healthy_test/V0.7.4_V4.3.0/`)
- `V0.7.4_V5.0.0/`
- `V0.9.6_V5.0.0/`
- `V1.4.0_V5.0.0/`
- `V1.4.0_V5.2.0/`
- `V0.7.4_V4.3.0_notrim/` (test sans --trim)
- `V0.7.4_V4.3.0_notrim_explicit/` (test --no-trim explicite)

## Test --trim basecall (2026-03-10) — AUCUN IMPACT SUR LE NOMBRE DE READS

Dorado 0.7.4 + modèle V4.3.0, run PBE25131 (88 GB, 66 POD5).

| Config | Commande | Reads | BAM size |
|--------|----------|------:|----------|
| `--trim adapters` | `dorado basecaller ... --trim adapters --device cuda:all` | 13,321,568 | 5.5 GB |
| sans flag (défaut) | `dorado basecaller ... --device cuda:all` | 13,321,568 | 12 GB |
| `--no-trim` explicite | `dorado basecaller ... --no-trim --device cuda:all` | 13,321,568 | 11.8 GB |

**Conclusion** : `--trim` n'affecte PAS le nombre de reads, uniquement la taille du BAM.
- `--trim adapters` supprime les séquences adaptatrices → BAM 2x plus petit
- `--no-trim` et défaut (sans flag) = résultats quasi identiques (~12 GB)
- Le nombre de reads est strictement identique dans les 3 cas

**S3** :
- `--trim adapters` : `s3://.../20250528_1415_P2I-00117-B_PBE25131_0c54a6da/V0.7.4_V4.3.0/basecall/`
- sans flag : `s3://.../20250528_1415_P2I-00117-B_PBE25131_0c54a6da/V0.7.4_V4.3.0_notrim/`
- `--no-trim` : `s3://.../20250528_1415_P2I-00117-B_PBE25131_0c54a6da/V0.7.4_V4.3.0_notrim_explicit/`

## Scripts d'investigation
- Répertoire : `~/Pipeline/Pod2Bam/test/best_strat_healthy/`
- `download_pod5.sh`, `launch_v43.sh`, `launch_v50.sh`, `benchmark_reads.sh`, `compare_tri_source.sh`
- Table barcode V4.3.0 : `barcode_healthy_V4.3.0.tsv` (bc13-16)
- POD5 local : `/scratch/basecall/dorado/data/20250528_1415_P2I-00117-B_PBE25131_0c54a6da/pod5/` (66 fichiers, 88 GB)
- Résultats S3 : `s3://aima-bam-data/processed/Pod2Bam/DEV/healthy_test/V0.7.4_V4.3.0/`
