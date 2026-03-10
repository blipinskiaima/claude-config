# Pod2Bam Memory

## Priorités utilisateur
- **GRCh38 en premier** : se concentrer uniquement sur GRCh38 no_alt pour les tests. hg38 plus tard.
- **Exécution séquentielle GPU** : ne JAMAIS lancer 2 basecalls en parallèle (batch size réduit + résultats tronqués)
- **tmux pour les longs jobs** : l'utilisateur veut lancer lui-même dans tmux, donner la commande
- **POD5 index 0** : toujours utiliser les fichiers `_0.pod5` pour les tests (pas d'autre index)

## Décisions pipeline
- `--kit-name SQK-NBD114-24 --trim all` : nécessaire pour obtenir les mêmes longueurs de reads que MinKNOW (delta=0 vérifié sur 10 reads)
- `--trim adapters` seul ne suffit pas (delta ~90 bases)
- Docker nécessite `sg docker -c "..."` sur ce serveur (user dans groupe docker mais session Claude hérite pas)
- `nohup` obligatoire pour les longs jobs lancés par Claude (sinon tué au changement de session)
- AWS CLI : `/usr/local/bin/aws` (dans PATH), profil `--profile scw`
- S3 upload path : `s3://aima-bam-data/data/HCL/liquid/{sample}_rebasecalled_{VERSION}/`
- S3 processed path : `s3://aima-bam-data/processed/MRD/RetD/liquid/HCL/{sample}/` (bedMethyl, RAIMA scores, props)

## Serveur GPU
- **Scaleway H100-1-80G** : 1x H100 80GB, 24 vCPU, 240 GB RAM (serveur actuel, mars 2026)
- Ancien : 2x NVIDIA L4 (23 GB VRAM chacune)
- Images buildées : `pod2bam:0.9.6` (Dorado 0.9.6), `pod2bam:1.4.0` (Dorado 1.4.0), `pod2bam:0.7.4` (Dorado 0.7.4)
- `/scratch/` en root, user blipinski peut écrire (groupe docker/1007)
- Dorado est 100% GPU-bound : 4→32 CPU = ~2% speedup seulement

## Structure données
- BAM originaux du séquenceur rangés dans `data/{sample}/bam/` (pas dans compare/)
- Résultats multi-version dans `result/GRCh38/{version}/{sample}/`
- Logs dans `/scratch/basecall/dorado/logs/`
- POD5 Colon_1-4 (FC-A) : `/scratch/basecall/dorado/data/Colon_1-4/pod5/` (218 fichiers, 452 GB)

## Pipeline Nextflow DSL2
- **Converti** de bash vers Nextflow DSL2 (2026-02-25), style identique à Bam2Beta
- **Fichiers clés** : `main.nf`, `nextflow.config`, `conf/base.config`, `workflow/basecall.nf`
- **Single-version** : `--version V4.3.0` (multi-version retiré, boucle externe dans launch.sh)
- **GPU séquentiel** : `maxForks 1` sur `Dorado_basecall`, sort/index parallèle
- **Logs Dorado** : `.basecall.log`, `.demux.log`, `.align.log` publiés dans `${output}/${VERSION}/logs/`
- **publishDir** (mis à jour 2026-03-10) : TOUTES les sorties publiées via publishDir S3 :
  - `${output}/${VERSION}/basecall/` → unsorted BAM
  - `${output}/${VERSION}/demuxed/` → BAMs demultiplexés par barcode
  - `${output}/${VERSION}/align/` → BAMs alignés (pré-sort)
  - `${output}/${VERSION}/${ID}/` → BAM sorted + BAI final
  - `${output}/${VERSION}/logs/` → tous les logs
  - **Risque** : fichiers >10 GB peuvent crasher l'upload S3 (java.io.IOException). Accepté par l'utilisateur.
- **Convention output S3** : `s3://aima-bam-data/processed/Pod2Bam/DEV/{run_id}/{version}/` (run_id = nom de la table TSV)
- **Anciens scripts bash** conservés dans `bash/` pour référence

### Pipeline B — conformation optimale multiplex (implémenté 2026-03-09, validé 2026-03-10)
- **Workflow** : basecall --trim adapters → demux uBAM → align map-ont par barcode → sort → index
- **Avant** (Pipeline C) : basecall → align → demux → sort → index (perdait secondary/supplementary au demux)
- **Avantages Pipeline B** : conserve tous les reads (primary + secondary + supplementary), mapping rate 86.2% (map-ont vs 81.3% lr:hq)
- **Validé full-scale** : 452 GB POD5 → 153.3M reads, 4h47m sur H100, 4 BAMs sorted+indexed
- **Dorado_align** : utilise `--mm2-opts '-x map-ont'` (hardcodé)
- **Dorado_demux** : timeout augmenté à 24h (1h insuffisant pour 130M reads / 45 GB uBAM, exit 143)

### Versions Dorado supportées dans nextflow.config
| Version key | Dorado | Simplex model | Mod model | Image |
|-------------|--------|---------------|-----------|-------|
| V4.2.0 | 0.9.6 | hac@v4.2.0 | 5mCG_5hmCG@v2 | pod2bam:0.9.6 |
| V4.3.0 | 0.9.6 | hac@v4.3.0 | 5mCG_5hmCG@v1 | pod2bam:0.9.6 |
| V5.0.0 | 0.9.6 | hac@v5.0.0 | 5mCG_5hmCG@v3 | pod2bam:0.9.6 |
| V5.2.0 | 1.4.0 | hac@v5.2.0 | 5mCG_5hmCG@v2 | pod2bam:1.4.0 |
| V0.7.4_V4.3.0 | 0.7.4 | hac@v4.3.0 | 5mCG_5hmCG@v1 | pod2bam:0.7.4 |
| V0.7.4_V5.0.0 | 0.7.4 | hac@v5.0.0 | 5mCG_5hmCG@v1 | pod2bam:0.7.4 |
| V0.9.6_V5.0.0 | 0.9.6 | hac@v5.0.0 | 5mCG_5hmCG@v3 | pod2bam:0.9.6 |
| V1.4.0_V5.0.0 | 1.4.0 | hac@v5.0.0 | 5mCG_5hmCG@v3 | pod2bam:1.4.0 |
| **V1.4.0_V5.2.0** | **1.4.0** | **hac@v5.2.0** | **5mCG_5hmCG@v2** | **pod2bam:1.4.0** |

- **V1.4.0_V5.2.0 = MEILLEURE COMBINAISON** : 8.7% unclassified, +2.8% reads vs MinKNOW
- **V0.7.4 + V5.0.0** : simplex model OK, mais mod model `5mCG_5hmCG@v3` indisponible → fallback `@v1`
- **V1.4.0_V5.0.0** : modèles V5.0.0 sur le host `/scratch/basecall/dorado/models/` (pas dans image 1.4.0)
- **Modèles V0.7.4** : sur le host `/scratch/basecall/dorado/models/` (pas dans l'image Docker)
- **Modèles V5.0.0/V5.2.0** : dans l'image Docker `/opt/models/`
- **Modèles V4.2.0/V4.3.0** : sur le host `/scratch/basecall/dorado/models/`

### Benchmark versions Dorado — taux unclassified (1 POD5 FC-A, SQK-NBD114-96)
| Version Dorado | Classified | Unclassified | % unclass |
|----------------|-----------|-------------|-----------|
| 0.7.4 | 522,228 | 83,311 | **13.8%** |
| 0.9.6 | 529,715 | 75,793 | **12.5%** |
| 1.4.0 | 537,906 | 67,604 | **11.2%** |
| MinKNOW BS 7.6.7 | ~97.8% | | **2.2%** |

- Tendance claire : plus Dorado est récent, moins d'unclassified. Mais même 1.4.0 reste loin de MinKNOW.

### Investigation perte reads Pod2Bam vs MinKNOW — RÉSOLU (2026-03-10)
- **Résultat** : PAS DE PERTE DE READS. Delta < 1% en comparant primary vs primary.
- **La "perte 30-40%"** = artefact de comparaison métriques incompatibles (nb_reads_total inclut sec/sup, pass vs pass+fail, unclassified rate)
- **Test run** : PBE25131 (88 GB, 66 POD5, 4 samples Healthy_785/786/792/798, bc13-16)
- **Basecall total** : Pod2Bam 13,321,568 vs MinKNOW 13,268,071 = **+0.4%**
- **Primary classified** : Pod2Bam 11,778,282 vs MinKNOW 11,837,412 = **-0.5%**
- **Scripts** : `~/Pipeline/Pod2Bam/test/best_strat_healthy/`
- **Détails complets** : voir `memory/investigation-read-loss.md`

### Test full-scale Colon_1-4 — TERMINÉ (2026-03-10)
- **Run** : 20250325_1444_P2I-00117-A_PBA39351_14c189c8 (FC-A)
- **POD5** : 218 fichiers, 452 GB, dans `/scratch/basecall/dorado/data/Colon_1-4/pod5/`
- **Barcode sheet** : `tables/barcode_colon_1-4.tsv` (bc41→Colon_1, bc42→Colon_2, bc43→Colon_3, bc44→Colon_4)

#### Test 1 : V0.7.4_V4.3.0 — SUCCESS (Pipeline B, 4h47m)
- **S3** : `s3://aima-bam-data/processed/Pod2Bam/DEV/Colon_test/V0.7.4_V4.3.0/`
- **Workdir local** : `/scratch/nxf-work/colon_v43_fresh2/`
- **Résultats finaux** (sorted+indexed, primary+secondary+supplementary) :

| Sample | Barcode | Reads | BAM size |
|--------|---------|-------|----------|
| Colon_1 | bc41 | 19.2M | 6.1 GB |
| Colon_2 | bc42 | 27.7M | 9.5 GB |
| Colon_3 | bc43 | 56.3M | 20 GB |
| Colon_4 | bc44 | 33.6M | 12 GB |
| Unclassified | — | 16.5M | — |
| **Total** | | **153.3M** | **47.6 GB** |

- **% unclassified** : 16.5M / 153.3M = **10.8%** (full-scale, vs 13.8% sur 1 POD5)
- BAMs + BAI + logs uploadés sur S3

#### Test 2 : V0.7.4_V5.0.0 — EN ATTENTE (Colon_1-4)

### Tests Healthy run PBE25131 — EN COURS (2026-03-10)
- **Run** : 20250528_1415_P2I-00117-B_PBE25131_0c54a6da (88 GB, 66 POD5)
- **S3 base** : `s3://aima-bam-data/processed/Pod2Bam/DEV/20250528_1415_P2I-00117-B_PBE25131_0c54a6da/`
- **Scripts** : `~/Pipeline/Pod2Bam/test/best_strat_healthy/`

| Test | Script | Status | Notes |
|------|--------|--------|-------|
| V0.7.4_V4.3.0 | launch_v43.sh | DONE | 13.3M reads, résultats manuellement uploadés |
| V0.7.4_V4.3.0 no-trim | test_no_trim.sh | DONE | 13,321,568 reads = 0% delta, trim n'affecte que taille BAM |
| V0.7.4_V5.0.0 | launch_v074_v50.sh | DONE | 46 min, 11,922,765 primary classifiés, 10.5% unclass |
| V0.9.6_V5.0.0 | launch_v096_v50.sh | DONE | 34 min, 11,954,972 primary classifiés, 10.3% unclass |
| V1.4.0_V5.0.0 | launch_v140_v50.sh | DONE | 31 min, 11,877,865 primary classifiés, 10.8% unclass |
| V1.4.0_V5.2.0 | launch_v140_v52.sh | DONE | 35 min, 12,168,156 primary classifiés, 8.7% unclass |

- **MEILLEURE COMBINAISON : V1.4.0_V5.2.0** (Dorado 1.4.0 + hac@v5.2.0 + mod@v2)
  - +2.8% reads classifiés vs MinKNOW, +3.3% vs V0.7.4_V4.3.0
  - 8.7% unclassified (le plus bas de tous, vs 11.6% pour V0.7.4_V4.3.0)
  - 35 min pipeline complet (88 GB POD5)
  - Modèles dans l'image Docker pod2bam:1.4.0 `/opt/models/`
- **Détails complets benchmark 5 versions** : voir `memory/investigation-read-loss.md`

### Stratégie basecall/demux (décidée 2026-03-06, mise à jour 2026-03-09)
- **Simplex** : `dorado basecaller --reference --kit-name SQK-NBD114-24 --trim all` (inchangé, pas de demux)
- **Multiplex Pipeline B** : `dorado basecaller --trim adapters` → `dorado demux --kit-name SQK-NBD114-96 --no-trim` → `dorado aligner --mm2-opts '-x map-ont'`
- **Pourquoi Pipeline B** : conserve secondary/supplementary, mapping rate +5pts avec map-ont
- **Pourquoi pas --reference inline** : OOM kill sur gros datasets (>230 GB RAM sur 329 GB POD5)
- **Pourquoi pas --trim all en multiplex** : supprime les barcodes → 97% unclassified au demux

### OOM kill — cause racine perte 2x reads CGFL (2026-03-06)
- **Symptôme** : Healthy_643 rebasecalled V5.0.0 = 32M reads vs 73M attendus
- **Cause** : `dorado basecaller --reference` lance minimap2 inline → consomme >230 GB RAM sur 329 GB POD5 → OOM kill (signal 9, exit 137)
- **Preuve** : `.command.log` dans nxf-work : `line 10: 74 Killed dorado basecaller ...`
- **BAM tronqué** : pas de EOF marker, `samtools quickcheck` le détecte
- **Fix** : séparer basecall et alignment en 2 process Nextflow
- **Test OOM 452 GB** : script prêt pour confirmer OOM sur Colon_1-4 (test_oom_inline.sh)

### Tests demux — variables éliminées (2026-03-06 à 2026-03-09)
| Variable | Config | Classified | Unclass | % |
|----------|--------|-----------|---------|---|
| Trim | no_trim/trim_adapters/trim_all | 529,715 | 75,793 | 12.5% |
| Ordre | Pipeline B ou C | 529,715 | 75,793 | 12.5% |
| Dorado | 0.7.4 | 522,228 | 83,311 | 13.8% |
| Dorado | 0.9.6 | 529,715 | 75,793 | 12.5% |
| Dorado | 1.4.0 | 537,906 | 67,604 | 11.2% |
| Q-score | Q9 | 493,208 | 27,603 | 5.3% |
| Custom TOML | relaxed | 529,715 | 75,793 | 12.5% |
| MinKNOW | BS 7.6.7 | ~97.8% | | 2.2% |

- **Conclusion** : gap 12.5% vs 2.2% MinKNOW = limitation fondamentale du classifieur standalone
- **Profil unclassified** : Q moyen=15.1, longueur=324bp, barcode illisible (Q bas)

### Investigation minimap2 preset lr:hq vs map-ont (2026-03-07)
- map-ont = 86.2% mapping rate vs lr:hq = 81.3% (+5 points)
- Plus de secondary/supplementary avec map-ont (725K vs 676K total reads)
- Pipeline B + map-ont = conformation optimale

### Benchmark dual flow cell Colon_1-8 (2026-03-09)
- Chaque FC ne contient QUE ses propres barcodes (FC-A=bc41-44, FC-B=bc45-48)
- Combiner FC-A+B ajoute les barcodes de l'autre FC, ne change pas les counts existants

### S3 paths CGFL
- POD5 : `s3://aima-pod-data/data/CGFL/liquid/{run_id}/pod5/`
- BAM originaux mergés : `s3://aima-bam-data/processed/MRD/RetD/liquid/CGFL/{sample}/BAM/`
- BAM originaux séquenceur : `s3://aima-bam-data/data/CGFL/liquid/{sample}/`
- BAM rebasecallés : `s3://aima-bam-data/data/CGFL/liquid/{sample}_rebasecalled_{VERSION}/`
- Rapports séquenceur : dans le dossier pod5 sur S3 (HTML)
- Logs Pod2Bam production : `s3://aima-bam-data/processed/Pod2Bam/logs/`
- Test DEV : `s3://aima-bam-data/processed/Pod2Bam/DEV/Colon_test/`

## Observations clés
- **`dorado demux` supprime secondary+supplementary** : Pipeline B (demux uBAM → align) les préserve
- **`--reference` inline = identique à `dorado aligner`** : même résultat, mais risque OOM sur gros datasets
- **V5.2.0 meilleur classifieur** : 8.7% unclassified vs 10-12% pour les autres versions (benchmark Healthy PBE25131). La "perte 24%" précédemment notée était un artefact de comparaison (pass-only count ou contexte différent).
- **Dorado 1.4.0 demux breaking change** : sortie imbriquée `demuxed/{experiment}/{sample}/{run}/bam_pass/barcode{N}/file.bam` au lieu de `demuxed/hash_barcode{N}.bam` (0.7.4/0.9.6). Fix : aplatir après demux via `find + mv` dans le process Nextflow.
- **Dorado stdout = SAM texte** (pas BAM compressé), unsorted.bam ~2.4x plus gros que sorted BAM
- **Bug bash `((var++))`** : avec `set -e`, `((0++))` retourne exit code 1
- **Nextflow publishDir S3** : fichiers >10 GB crashent l'upload (java.io.IOException), tue le pipeline. Même 16 GB crash. Solution : désactiver publishDir, uploader manuellement.
- **Nextflow -resume** : ne retente pas le publishDir des process cached
- **Nextflow -resume cache invalide** : toute modif de basecall.nf (même un commentaire) change le script hash et invalide le cache de TOUS les process du fichier. Ne jamais modifier le fichier pendant un run.
- **Nextflow + CUDA OOM** : si un dorado est tué mais le container docker pas nettoyé, la VRAM reste réservée → le basecall suivant échoue en CUDA OOM. Toujours `docker kill` les containers résiduels avant de relancer.

## Investigation faux positifs RAIMA V5.x (2026-02-24)
- Cause racine : seuil adaptatif modkit chute de ~0.96 (V4.x) à ~0.78 (V5.x)
- Correction : `--filter-threshold C:0.965` dans modkit pileup
- Détails : voir `/scratch/healthy4_investigation/`

## Analyse thresholds modkit large cohorte (2026-02-24)
- 292 samples, thresholds par version : v3.3 ~0.75, v4.3.0 ~0.95, v5.0.0 ~0.79
- Fichiers : `figure/modkit_thresholds.csv`, `figure/plot_modkit_thresholds.R`

## Pipeline Bam2Beta
- Container modkit : `blipinskiaima/bam2beta:latest` (modkit 0.5.1)
- Container RAIMA : `blipinskiaima/raima:latest` (RAIMA 0.4.3)
- Workflow : BAM → samtools view -L epic.bed → modkit adjust → modkit pileup → RAIMA scoring

## Plan de test (10 samples)
### False Positive (mVAF > 0) : Healthy_4, 11, 12, 25, 34
### True Negative (mVAF = 0) : Healthy_14, 3, 8, 23, 26
### Avancement : Healthy_4 DONE (4/4), Healthy_11 DONE (4/4), Healthy_8 DONE (V5.0.0)
