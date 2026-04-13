---
paths:
  - "**/Pod2Bam/**"
  - "**/basecall/**"
  - "**/pod2bam*"
  - "**/Dockerfile*"
---

# Référence Dorado & Pod2Bam — Oxford Nanopore

## Images Docker AIMA

| Image | Dorado | Modèles intégrés | Usage |
|-------|--------|-----------------|-------|
| `pod2bam:0.9.6` | 0.9.6+0949eb8d | V5.0.0 (simplex + 5mCG_5hmCG@v3) | Production HCL/CGFL |
| `pod2bam:1.4.0` | 1.4.0 | V5.2.0 (simplex + 5mCG_5hmCG@v2) | Investigation multi-version |

## Modèles de basecalling

| Version | Simplex | Modification | Localisation |
|---------|---------|-------------|-------------|
| V4.2.0 | `dna_r10.4.1_e8.2_400bps_hac@v4.2.0` | `..._5mCG_5hmCG@v2` | Host `/scratch/basecall/dorado/models/` |
| V4.3.0 | `dna_r10.4.1_e8.2_400bps_hac@v4.3.0` | `..._5mCG_5hmCG@v1` | Host `/scratch/basecall/dorado/models/` |
| V5.0.0 | `dna_r10.4.1_e8.2_400bps_hac@v5.0.0` | `..._5mCG_5hmCG@v3` | Dans image `pod2bam:0.9.6` `/opt/models/` |
| V5.2.0 | `dna_r10.4.1_e8.2_400bps_hac@v5.2.0` | `..._5mCG_5hmCG@v2` | Dans image `pod2bam:1.4.0` `/opt/models/` |

## Mapping MinKNOW ↔ Dorado

Pas de table officielle ONT. Mapping AIMA confirmé expérimentalement :

```
MinKNOW 6.5.14 → Dorado BS 7.9.8 → Dorado standalone 0.9.6
```

Les deux builds (CDN standalone 0.9.6+0949eb8d et BS 7.9.8 dorado 0.9.6+49e25e9) produisent des résultats **strictement identiques**.

## Conventions de trimming

| Option | Effet | Delta vs MinKNOW |
|--------|-------|-----------------|
| `--trim adapters` | Coupe adaptateurs ONT (~22 bases) | ~90 bases de soft-clip restantes |
| `--trim all` | Identique à adapters (pas de primers/barcodes supplémentaires) | ~90 bases |
| `--kit-name SQK-NBD114-24 --trim all` | Coupe adaptateurs + barcodes | **delta = 0** (identique à MinKNOW) |

**TOUJOURS** utiliser `--kit-name SQK-NBD114-24 --trim all` pour les samples HCL (simplex).
Le kit CGFL multiplex est `SQK-NBD114-96`.

## Configuration Docker run

```bash
DOCKER_RUN=(docker run --rm
    --gpus all
    --user "$(id -u):$(id -g)"
    --group-add 1007          # accès /scratch
    -v /scratch:/scratch
    -w /workspace
    "$DORADO_IMAGE"
)
```

`--group-add 1007` est obligatoire pour accéder à `/scratch` sur le serveur GPU.

## Commande de basecalling standard

```bash
"${DOCKER_RUN[@]}" dorado basecaller \
    "${MODEL_DIR}/${MODEL}" \
    "$pod5_dir" \
    --modified-bases-models "${MODEL_DIR}/${MOD_MODEL}" \
    --reference "$ref_path" \
    --kit-name SQK-NBD114-24 \
    --trim all \
    --device cuda:all \
    > "$output_bam"
```

TOUJOURS utiliser `--modified-bases-models` (chemin explicite) et PAS `--modified-bases 5mCG_5hmCG` (qui tente de télécharger au runtime).

## Observations clés (investigation multi-version)

1. **V5.2.0 (Dorado 1.4.0) perd ~24% des reads primaires** vs les autres versions — filtre qualité plus strict. Impact sur mVAF à évaluer.
2. **Dorado >= 1.0 tente de migrer les POD5 v3→v4** — Dorado 0.9.6 ne le fait PAS (avantage).
3. **Les appels de méthylation concordent** entre les versions sur les sites CpG communs.
4. **Les portions alignées sont identiques** entre rebasecalled et original (même chr, pos, MAPQ, strand).

## Chemins S3

- POD5 : `s3://aima-pod-data/data/{labo}/{type}/{sample}/` (profil scw)
- BAM originaux : `s3://aima-bam-data/data/{labo}/{type}/{sample}/`
- BAM rebasecallés : `s3://aima-bam-data/data/HCL/liquid/{sample}_rebasecalled_{VERSION}/`

## Référentiels génomiques

| Genome | Chemin | Notes |
|--------|--------|-------|
| hg38 | `/scratch/dependencies/genomes/hg38/hg38.fa` | UCSC, chr prefix, avec alt contigs |
| GRCh38 no_alt | `/scratch/dependencies/genomes/GRCh38/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa` | NCBI, sans alt contigs |

Les deux produisent des résultats identiques (vérifié sur Healthy_826).
