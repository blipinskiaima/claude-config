# Pod2Bam Memory

## Priorités utilisateur
- **GRCh38 en premier** : uniquement GRCh38 no_alt. hg38 plus tard.
- **Exécution séquentielle GPU** : ne JAMAIS lancer 2 basecalls en parallèle
- **tmux pour les longs jobs** : l'utilisateur lance lui-même dans tmux
- **POD5 index 0** : toujours utiliser `_0.pod5` pour les tests

## Décisions pipeline (mis à jour 2026-03-10)
- **Simplex** : `dorado basecaller --reference --kit-name SQK-NBD114-24 --trim all`
- **Multiplex Pipeline B** : `basecall --trim adapters --min-qscore 9` → `demux --no-trim` → `aligner` (lr:hq défaut) → `sort+index`
- **publishDir local + aws s3 sync** : Nextflow publie en local, script bash fait `aws s3 sync --profile=scw` après
- **Nommage** : `{ID}.basecall.bam`, `{ID}_barcode*.bam`, `{ID}.bam` + `.bai`, `{ID}.log`
- Docker : `sg docker -c "..."`, `nohup` obligatoire pour longs jobs
- AWS CLI : `--profile=scw --endpoint-url https://s3.fr-par.scw.cloud`
- **Choix documentés dans README.md** (section "Choix de configuration du pipeline")

## Arborescence output (mis à jour 2026-03-10)
```
{LOCAL_OUTPUT}/
├── basecall/    → {ID}.basecall.bam + .basecall.log
├── demux/       → {ID}_barcode01-96.bam + _unclassified + _mixed + .demux.log
├── align/
│   ├── {sample}.log (x N)
│   └── {sample}/    → {sample}.bam + .bam.bai (x N)
└── log/         → Pod2Bam_report.html, _trace.txt, _timeline.html, _dag.html, nextflow.log, Pod2Bam.log
```

## Script de production Pod2Bam.sh (2026-03-10)
- **Smart scheduling** : prefetch POD5 (max 3 locaux) + GPU handoff via trace file + finalize background
- **23 runs** split en 2 groupes : RUNS_FR (10 runs) et RUNS_WS (13 runs, en commentaire)
- **4 runs retirés** (POD5 absents sur S3) : 877aac92 (Colon_21-24), 05ab4dea (Colon_17-20), b4caa48f (Colon_13-16), f181e139 (Colon_9-12)
- RUNS_FR en variable active, RUNS_WS en commentaire — décommenter pour le 2e serveur
- **S3 output** : `s3://aima-bam-data/processed/Pod2Bam/RetD/{RUN_ID}/{VERSION}/`
- **Local output** : `/scratch/results/{RUN_ID}/{VERSION}/` (persiste après sync)
- **Cleanup** : POD5 + workdir supprimés après upload, résultats conservés
- **Logs** : GLOBAL_LOG (`/scratch/run/Pod2Bam_*.log`) + RUN_LOG par run + upload S3
- **Reporting Nextflow** : report, trace, timeline, dag activés dans `nextflow.config`
- **Profils** : `-profile docker,tower,scw`

### Validation pré-lancement (2026-03-10)
- 10 TSV FR : OK (4 samples chacun)
- 13 TSV WS : OK (4-5 samples)
- 10 S3 POD5 FR : OK (vérifié aws ls)
- 13 S3 POD5 WS : OK (vérifié aws ls)
- Reference GRCh38 + .fai : OK (/scratch/dependencies/)
- Docker pod2bam:0.9.6 : OK (10.7 GB)
- GPU H100 80GB : OK
- CPU oversubscription lors du chevauchement : impact minimal (basecall GPU-bound, overlap ~30 min)

## Bugs fixes (2026-03-10)
- **wait $NF_PID dans subshell** : `wait` ne peut attendre qu'un enfant direct → fix : poll `kill -0`
- **Samtools_sort_index absent base.config** : process renommé mais config pas mise à jour → ajouté (16 CPU, 16 GB, 6h)
- **Tous les timeouts** : uniformisés à `6.hour * task.attempt`

## Serveur GPU
- **Scaleway H100-1-80G** : 1x H100 80GB, 24 vCPU, 240 GB RAM
- Images : `pod2bam:0.9.6` (Dorado 0.9.6), `pod2bam:1.4.0` (Dorado 1.4.0), `pod2bam:0.7.4` (Dorado 0.7.4)
- Dorado 100% GPU-bound, CPU n'accélère pas

## Pipeline Nextflow DSL2
- **Fichiers** : `main.nf`, `nextflow.config`, `conf/base.config`, `workflow/basecall.nf`
- **Process** : Dorado_basecall → Dorado_demux → Dorado_align → Samtools_sort_index
- **maxForks 1** sur Dorado_basecall (GPU séquentiel)
- **Dorado_align** : `dorado aligner` sans `--mm2-opts` → utilise lr:hq par défaut (cohérent MinKNOW)
- **Dorado_demux** : flatten output (Dorado 1.4.0 nested dirs fix)

### Versions Dorado — voir `nextflow.config` pour la table complète
- **V0.9.6_V5.0.0** = choix retenu pour production (compatibilité cohorte V5.0.0)
- **Détails benchmark 5 versions** : voir `memory/investigation-read-loss.md`
- **Benchmark Q9** : voir `memory/benchmark-q9.md`

### Minimap2 preset lr:hq vs map-ont
- **lr:hq** (défaut Dorado ≥0.6.0) : k=19, w=19, strict, pour Q20+
- **map-ont** : k=15, w=10, permissif, pour ONT classique
- **Choix** : lr:hq (défaut) pour cohérence MinKNOW. map-ont = alternative positive documentée dans README

### Benchmark Q9 (--min-qscore 9, PBE25131)
- Filtre 13.5% reads, unclass 10.3%→3.2%, map rate +2pts, perte nette -4.9% classifiés
- **Retenu comme défaut pipeline**

### Résolutions bugs importants
- **publishDir S3 crash** : fichiers >10 GB → publishDir local + aws s3 sync
- **OOM inline** : `--reference` inline >230 GB RAM → séparer basecall/align
- **Dorado 1.4.0 demux** : sortie nested → flatten via find+mv
- **Nextflow cache** : toute modif basecall.nf invalide TOUS les process

## S3 paths CGFL
- POD5 : `s3://aima-pod-data/data/CGFL/liquid/{run_id}/pod5/`
- BAM production RetD : `s3://aima-bam-data/processed/Pod2Bam/RetD/{run_id}/{version}/`
- BAM anciens : `s3://aima-bam-data/data/CGFL/liquid/{sample}_rebasecalled_{VERSION}/`
- Test DEV : `s3://aima-bam-data/processed/Pod2Bam/DEV/`

## Tests terminés (2026-03-10)
- **Test 2** : V0.9.6_V5.0.0 standard PBE29634 — terminé, résultats en local
- **Test 3** : V0.9.6_V5.0.0 Q9 PBE29634 — terminé, résultats en local
- NB : ces tests utilisent l'ancien code (map-ont, anciens noms de process)

## Autres projets
- **Bam2Beta** : BAM → modkit → RAIMA. Containers `blipinskiaima/bam2beta:latest`, `blipinskiaima/raima:latest`
- **Investigation RAIMA V5.x** : seuil modkit chute ~0.96→~0.78. Fix : `--filter-threshold C:0.965`
