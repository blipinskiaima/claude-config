# Pod2Bam Memory

## Priorités utilisateur
- **GRCh38 en premier** : uniquement GRCh38 no_alt. hg38 plus tard.
- **Exécution séquentielle GPU** : ne JAMAIS lancer 2 basecalls en parallèle
- **tmux pour les longs jobs** : l'utilisateur lance lui-même dans tmux
- **POD5 index 0** : toujours utiliser `_0.pod5` pour les tests

## Décisions pipeline (mis à jour 2026-03-25, V0.2.0)
- **Simplex** : `dorado basecaller --reference --kit-name SQK-NBD114-24 --trim all`
- **Multiplex Pipeline B** : `basecall --trim adapters --min-qscore 9` → `demux` (trim par défaut) → `aligner --threads` (lr:hq) → `sort+index`
- **Trim gate terminé** : trim réduit mapping rate ~5pts, 0 perte primary reads → voir `memory/trim-investigation.md`
- **--BASECALL false** : skip basecall, réutilise BAM existant dans `{output}/basecall/` (pattern Bam2Beta --MERGE)
- **docker_nogpu** : profil Docker sans GPU pour demux/align/sort sans basecall
- **publishDir V0.2.0** : `demux_trimmed/`, `align_trimmed/` — ne jamais écraser `demux/`, `align/` existants
- **--threads** : ajouté à `dorado demux` (16 cpus) et `dorado aligner` (4 cpus)
- **Nommage** : `{ID}.basecall.bam`, `{ID}_barcode*.bam`, `{ID}.bam` + `.bai`, `{ID}.log`
- Docker : `sg docker -c "..."`, `nohup` obligatoire pour longs jobs
- AWS CLI : `--profile=scw --endpoint-url https://s3.fr-par.scw.cloud`
- **Choix documentés dans README.md** (section "Choix de configuration du pipeline")

## Arborescence output (mis à jour 2026-03-25, V0.2.0)
```
{OUTPUT}/
├── basecall/          → {ID}.basecall.bam + .basecall.log (inchangé)
├── demux/             → V0.1.0 (--no-trim) — NE PAS ÉCRASER
├── align/             → V0.1.0 (--no-trim) — NE PAS ÉCRASER
├── demux_trimmed/     → V0.2.0 (trim par défaut)
├── align_trimmed/     → V0.2.0 (trim par défaut)
│   ├── {sample}.log
│   └── {sample}/      → {sample}.bam + .bam.bai
└── log/               → reports Nextflow
```

## Script de production Pod2Bam.sh (2026-03-10)
- **Smart scheduling** : prefetch POD5 (max 3 locaux) + GPU handoff via trace file + finalize background
- **23 runs** split en 2 groupes : RUNS_FR (10 runs) et RUNS_WS (13 runs, en commentaire)
- **4 runs retirés du batch principal** → 3 traités dans batch Colon (voir `memory/batch-colon.md`), 1 manquant (877aac92)
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

## Production batch FR (2026-03-11) — TERMINÉ
- **10/10 runs** traités, **0 erreur**, tous sync S3 vérifiés OK (fichiers + taille identiques)
- **Durée totale** : ~21h (20:22 → 17:20), moyenne ~2h31/run
- **Ratio basecall** : ~5.5 min/Go de POD5 sur H100
- **Smart scheduling** : fonctionne parfaitement (prefetch, GPU handoff, finalize background)
- **Log global** : `s3://aima-bam-data/processed/Pod2Bam/RetD/Pod2Bam_20260310_202241.log`
- **Bug connu non corrigé** : `EXIT_CODE=0` hardcodé dans finalize() ligne 72 — à corriger avant batch WS
- **Résultats locaux** supprimés après vérification sync S3
- **Vérification sync** : `find -type f | wc -l` + `du -sb` local vs `aws s3 ls --recursive --summarize` S3

### Prochaine étape : batch WS (13 runs)
- Décommenter RUNS_WS dans Pod2Bam.sh, commenter RUNS_FR
- Corriger le bug EXIT_CODE dans finalize() avant lancement
- Serveur FR libre et nettoyé (scratch 4%)

### Timings par run (basecall + demux + align + sort + upload)
| Run | POD5 | Durée |
|-----|------|-------|
| PBE25131 | 88 Go | 44 min |
| PBA88487 | 311 Go | 2h19 |
| PBA89966 | 321 Go | 2h25 |
| PBA39351 | 451 Go | 3h49 |
| PAY45185 | 303 Go | 2h29 |
| PBE05840 | 330 Go | 2h37 |
| PBA39359 | 436 Go | 3h34 |
| PAY45111 | 565 Go | ~2h33 |
| PBE96775 | 622 Go | ~4h57 |
| PBE35117 | 643 Go | ~4h41 |

## Tests terminés (2026-03-10)
- **Test 2** : V0.9.6_V5.0.0 standard PBE29634 — terminé, résultats en local
- **Test 3** : V0.9.6_V5.0.0 Q9 PBE29634 — terminé, résultats en local
- NB : ces tests utilisent l'ancien code (map-ont, anciens noms de process)

## Batch Colon (2026-03-12) — voir `memory/batch-colon.md`
- 4 runs (f181e139, b4caa48f, 05ab4dea_rep1, 05ab4dea_rep2) — terminé 23:32, ~11h35
- Script `Pod2Bam_colon.sh` avec `S3_POD5_MAP` pour chemins POD5 custom
- S3 sync vérifié OK (386 fichiers), résultats locaux nettoyés
- 877aac92 (Colon_21-24) : complété 2026-03-19 (rep1+rep2, POD5 copiés manuellement)

## Investigation Trim Demux (2026-03-24) — voir `memory/trim-investigation.md`
- Test impact retrait `--no-trim` au demux sur l'alignement (secondary/supplementary)
- Script `trim_gate_test.sh`, données dans `/scratch/trim_gate/`
- Run 3b1c780b_sub, V4.3.0, Lung_10 + Breast_1
- Comparaison flagstat condition trim vs BAMs existants (baseline notrim)

## Batch 3b1c780b_sub (2026-03-19) — voir `memory/batch-3b1c780b-sub.md`
- Run 3b1c780b, subset Breast_1 + Lung_10 en V4.3.0 et V0.7.4_V4.3.0
- S3 output : `s3://.../3b1c780b_sub/V4.3.0/` et `V0.7.4_V4.3.0/`
- Dorado 0.7.4 : demux 10x plus lent, basecall 2x plus lent, VRAM 48-68G vs 29G
- Image `pod2bam:0.7.4` buildée sur le serveur (Dockerfile.0.7.4)

## Sample list courante (2026-04-07)
- Voir `sample_list_current.md` — 33 samples (20 Lung_Alc, 11 Colon, Breast_1, Lung_10)

## Re-trim Colon CGFL (2026-04-08) — voir `memory/retrim-colon-cgfl.md`
- 12 Colon_*_rep* liquid CGFL NO_TRIM détectés (adaptateur LA ONT visible)
- 3 TSV créés dans `tables/` (962143e5 rep1/rep2, 2347816e rep1)
- Script `dev/Pod2Bam_retrim_colon_cgfl.sh` — V0.9.6_V5.0.0, sliding window MAX_LOCAL=3, prêt à lancer
- Méthode détection : `samtools view | head -50 | grep TTGCTAAGGTTAA` sur `/mnt/...merged.bam`

## Autres projets
- **Bam2Beta** : BAM → modkit → RAIMA. Containers `blipinskiaima/bam2beta:latest`, `blipinskiaima/raima:latest`
- **Investigation RAIMA V5.x** : seuil modkit chute ~0.96→~0.78. Fix : `--filter-threshold C:0.965`
