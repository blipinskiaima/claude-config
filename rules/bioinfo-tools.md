# Outils bioinformatiques AIMA — Conventions d'usage

## modkit (ONT methylation)
- TOUJOURS utiliser : `modkit pileup --cpg --combine-strands --combine-mods`
- Produit des fichiers bedMethyl (colonnes : chrom, start, end, ..., coverage, percent_modified)
- Les fichiers de sortie sont par chromosome (chr1-22)

## dorado (ONT basecalling)
- Voir `~/.claude/rules/dorado-reference.md` pour la référence complète (images Docker, modèles, trimming)
- TOUJOURS utiliser `--modified-bases-models` (chemin explicite), PAS `--modified-bases` (télécharge au runtime)
- TOUJOURS utiliser `--kit-name SQK-NBD114-24 --trim all` pour HCL simplex (delta=0 avec MinKNOW)
- Kit CGFL multiplex : `SQK-NBD114-96` avec `--barcode_sheet`
- ATTENTION : V5.2.0 (Dorado 1.4.0) perd ~24% des reads vs versions précédentes (filtre qualité plus strict)
- ATTENTION au batch effect entre versions de modèles Dorado — TOUJOURS tracer la version dans les métadonnées

## samtools
- TOUJOURS vérifier le exit code après merge/sort/index
- Pour les BAM merge : `samtools cat` + `samtools sort` (pas `samtools merge` — contexte AIMA spécifique)
- Les BAM horaires sont 100% redondants avec les BAM mergés (vérifié 2026-03-13)

## raima (scoring R)
- Package R maintenu par Florian Privé — NE PAS modifier sans coordination
- Fonctions clés : `model_v1`, `model_v2`, `evaluate_score`, `compute_betas`, `prop_loyfer`
- Mise à jour raima → qualification non-régression Bam2Beta obligatoire

## ichorCNA
- Estimation de la fraction tumorale via HMM/CNA
- Résultats peu concluants pour l'instant (n'apporte pas d'info supplémentaire significative)

## Référentiels génomiques
- hg38 (défaut) : `/scratch/dependencies/genomes/hg38/hg38.fa` (UCSC, chr prefix, avec alt)
- GRCh38 : `/scratch/dependencies/genomes/GRCh38/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa`
- Les deux produisent des résultats identiques (vérifié sur Healthy_826)

## Pipeline AIMA — flux de données
```
POD5 → Pod2Bam (Dorado) → BAM → Bam2Beta (34 proc NF) → bedMethyl → raima → score
                                                                                 │
                                                                           trace-prod
                                                                                 │
                                                                    ┌────────────┴────────────┐
                                                                    │                         │
                                                              exploratory-analysis      IA-for-IA
                                                                    │
                                                              Aima-Tower
```
