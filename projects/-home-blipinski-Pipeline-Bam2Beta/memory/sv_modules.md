---
name: Modules SVs Sniffles2 + Severus + Decoil
description: Détection de variants structuraux ONT - architecture, containers, dépendances, caveats cliniques
type: project
originSessionId: 613eeff2-6b1f-420e-aaf2-3c2272f88dd3
---
Modules ajoutés en V1.2.0 (2026-04-28) pour la détection de SVs et reconstruction ecDNA, complémentaires aux modules méthylation/CNV existants.

## Architecture

| Workflow | Process | Container | Flag CLI |
|---|---|---|---|
| `workflow/Sniffles2.nf` | Sniffles2_call + Decoil_call | `blipinskiaima/sniffles2:latest`, `blipinskiaima/decoil:latest` | `--SNIFFLES2 true` |
| `workflow/Severus.nf` | Severus_clair3 + Severus_longphase + Severus_call | `blipinskiaima/severus:latest` (les 3) | `--SEVERUS true` |

Decoil est intégré DANS le workflow Sniffles2 (pas de flag séparé) — un seul flag active les 2 process.

Activation par défaut : `liquid.config` uniquement. Hors `prod.config` (R&D).
Channel d'entrée : `BAM_METADATA = [ID, DEPTH, BAM, BAI]` → contrôle via `params.rarefaction`.

## Severus — décisions techniques

**Why:** ctDNA plasma sans tissu normal apparié + maximisation du recall.

- **Mode tumor-only** + Panel of Normals (`PoN_1000G_hg38_extended.tsv.gz` de KolmogorovLab/Severus)
- **Phasing activé** (Boris a explicitement choisi pour maximiser les chances de réussite) :
  - Step 1 : Clair3 SNV calling (`run_clair3.sh --platform=ont --model_path=...`)
  - Step 2 : LongPhase phase + haplotag (BAM haplotagged + VCF SNV phasé)
  - Step 3 : Severus avec `--phasing-vcf` + `--target-bam` haplotagged
- Modèle Clair3 : `r1041_e82_400bps_sup_v500` (Dorado V5.0.0 simplex hac, cohérent avec dorado-reference.md)
- `--min-sv-size 50` en dur (`< 50` crash issue #76)
- Container : `graphviz` apt INDISPENSABLE avant `conda install severus` (pygraphviz crash sinon)

## Sniffles2 — décisions techniques

- **Mode `--mosaic` activé en dur** (basse fréquence ctDNA)
- `--output-rnames` pour Decoil downstream
- TRF BED partagé avec Severus VNTR (même fichier) : `human_GRCh38_no_alt_analysis_set.trf.bed`
- Image officielle BioContainers existe (`quay.io/biocontainers/sniffles:2.7.5--pyhdfd78af_0`) mais on rebuild en `blipinskiaima/sniffles2:latest` pour cohérence

## Decoil — décisions techniques + ⚠️ caveat clinique

- Image officielle existe : `madagiurgiu25/decoil:1.1.2-slim` → on rebuild `blipinskiaima/decoil:latest` en ajoutant `deeptools` (pour générer le bigwig coverage requis)
- Mode **`decoil reconstruct` standalone** (pas `decoil-pipeline sv-reconstruct` qui réutilise Sniffles v1 en interne — incohérent avec notre Sniffles2)
- Inputs : BAM + Sniffles2 VCF + bigwig (généré inline par bamCoverage) + ref FASTA
- Pas de Gurobi — utilise LASSO scikit-learn (open-source)
- Decoil **ne supporte PAS Severus VCF** nativement — uniquement Sniffles2

⚠️ **Caveat clinique** : Decoil n'est PAS validé sur plasma 5-30x. Le signal ecDNA ne sera reconstruit que si TF > 20% (amplification massive). Sur Healthy_826, attendu : `reconstruct.ecDNA.filtered.bed` vide. À considérer comme criblage : signal positif = confirmation forte ; signal négatif n'exclut pas l'ecDNA. Decoil/CoRAL sur plasma reste un sujet de recherche en 2026.

## Dépendances /scratch/dependencies/

```
sniffles2/human_GRCh38_no_alt_analysis_set.trf.bed
severus/vntrs/human_GRCh38_no_alt_analysis_set.trf.bed   (symlink → sniffles2/)
severus/pon/PoN_1000G_hg38_extended.tsv.gz
severus/clair3/r1041_e82_400bps_sup_v500/                (modèle ONT)
```

Les 2 premiers fichiers sont du repo `fritzsedlazeck/Sniffles/annotations/`.
Le PoN vient de `KolmogorovLab/Severus/pon/`.
Le modèle Clair3 se télécharge manuellement depuis nanopore.box (lien officiel ONT, non scriptable).

## Coûts en temps par sample (estimés)

- Sniffles2_call : ~30 min
- Decoil_call : ~15-30 min
- Severus_clair3 : ~1-2h
- Severus_longphase : ~30 min
- Severus_call : ~1-2h
- **Total** : ~4-5h/sample en mode liquid (les 2 modules activés ensemble)

## Outputs S3

```
${output}/${ID}/Sniffles2/
  ├── ${ID}.${DEPTH}.sniffles.vcf.gz / .snf / .coverage.bw / .sniffles2_call.log
  └── Decoil/
      └── ${ID}.${DEPTH}.reconstruct{,.ecDNA,.ecDNA.filtered}.bed + summary.txt + .decoil_call.log

${output}/${ID}/Severus/
  ├── ${ID}.${DEPTH}.clair3.snv.vcf.gz
  ├── ${ID}.${DEPTH}.haplotagged.bam{,.bai} + .phased.snv.vcf
  ├── ${ID}.${DEPTH}.severus.somatic.vcf / .all.vcf
  ├── ${ID}.${DEPTH}.severus.breakpoint_clusters.tsv / .severus.html
  └── ${ID}.${DEPTH}.severus_{clair3,longphase,call}.log
```

## Hors check de conformité

Modules R&D — non ajoutés à `conformity/check-run-output.sh`. Décision Boris.

## Pièges Docker découverts

- **`procps` requis dans images `python:3.x-slim`** : Nextflow utilise `ps` pour collecter les métriques de tâche. Les images slim n'incluent pas procps par défaut → erreur `Command 'ps' required by nextflow to collect task metrics cannot be found`. Fix : `apt-get install -y procps` dans le Dockerfile. Découvert en relançant le test V1.2.0 (Sniffles2_call exit 1 immédiat). `continuumio/miniconda3` et `madagiurgiu25/decoil:1.1.2-slim` ont déjà procps-ng inclus.
- **Conflit conda `htslib`/`libdeflate`** entre conda-forge et bioconda : Severus + Clair3 + LongPhase ne peuvent pas être installés ensemble en `channel_priority strict`. Fix : utiliser `channel_priority flexible` + `--override-channels -c bioconda -c conda-forge` + 1 environnement conda séparé par outil (severus py3.13, clair3 py3.10, longphase+samtools+bcftools dans le 3e env).
- **Severus VS Clair3 Python conflict** : Severus requiert Python 3.13, Clair3 requiert Python 3.10 → impossible dans un seul env conda. 3 envs séparés + symlinks `/usr/local/bin/` pour exposer les binaires.
- **Modèle Clair3 ONT** : le mirror HKU-BAL n'a que jusqu'à `sup_v420`. Pour V5.0.0+ (Dorado V5.0.0/V5.2.0), utiliser le CDN ONT direct : `https://cdn.oxfordnanoportal.com/software/analysis/models/clair3/r1041_e82_400bps_{hac,sup}_v{500,520}.tar.gz`. Pointers dans le repo `nanoporetech/rerio/clair3_models/`.
