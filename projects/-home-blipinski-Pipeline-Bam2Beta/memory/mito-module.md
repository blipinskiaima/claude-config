---
name: mito-module
description: "Module MITO — QC mitochondrien (mosdepth merged + BAM, actif liquid+solid+prod depuis 2026-08-12, mode rétro, 11 colonnes, pas metadata.json)"
metadata:
  node_type: memory
  type: project
  originSessionId: mito-qc-2026-07-24
  modified: 2026-07-27T17:14:00.000Z
---

# Module MITO — QC mitochondrien (2026-07-24)

QC d’abondance mitochondrienne uniquement (pas de score diagnostique). Parse les sorties
**Mosdepth merged déjà publiées** + calcule longueurs chrM depuis le BAM (convention FRAG).
**Actif liquid + solid + prod** depuis le 2026-08-12 (`fca2844`) ; `false` seulement hors profil ;
override CLI `--MITO`. L'activation en prod corrige le KO systématique de l'étape 2 de
`/test_bam2beta` : `check-run-output.sh` exige `mito_qc.tsv` dès que le sample est liquid, alors
que le profil `prod` désactivait le module. ⚠ **Jamais exécuté sur du solid à ce jour.**
Aucun re-run mosdepth, aucun modkit.

Workflow : `workflow/mito.nf` (process `Mito_qc`, bash **inline** dans `script:` — préférence
Boris). Câblé dans `main.nf` derrière `if (params.MITO)`.

## Contrat de sortie

- **Un seul fichier** : `MITO/{ID}.mito_qc.tsv`
- **Pas** de champs dans `metadata.json` → **pas** d’impact Aima-Tower / trace-prod / `rapport.nf`
- Contig mito : `chrM` (`LN=16569`)

### 11 colonnes ordonnées (TSV)

| # | Colonne | Source / déf. |
|---|---|---|
| 1 | `sample_id` | Nextflow |
| 2 | `mt_n_reads_total` | `samtools view -c BAM chrM` |
| 3 | `mt_n_reads_aligned` | `samtools view -c -F 0x900 BAM chrM` (déf. Cramino / JSON, scopée chrM) |
| 4 | `mt_depth` | col4 ligne `chrM` du summary mosdepth |
| 5 | `mt_coverage_percent` | breadth ≥1× chrM (`fraction × 100`, même formule que `coverage_percent`) |
| 6 | `autosomal_depth` | mean depth pondéré length **chr1–22** (summary) |
| 7 | `autosomal_coverage_percent` | breadth ≥1× chr1–22, pondérée length |
| 8 | `mt_autosomal_depth_ratio` | `mt_depth / autosomal_depth` |
| 9 | `mt_autosomal_coverage_ratio` | `mt_coverage_percent / autosomal_coverage_percent` (`NA` si dénominateur 0) |
| 10 | `mt_mean_length` | moyenne longueurs chrM (conv. FRAG) |
| 11 | `mt_median_length` | médiane longueurs chrM (conv. FRAG) |

Pas de counts genome-wide dans le TSV (déjà dans `metadata.json`).

## Source Mosdepth = merged **non filtré**

Chemin : `{OUTPUT}/{ID}/QC/Mosdepth/merged/{ID}.merged.mosdepth.{summary,global.dist}.txt`

**Même source** que `depth` / `coverage_percent` de `metadata.json`. **PAS** le mosdepth EPIC
filtré (présent sur S3 mais n’alimente pas le JSON) — ne jamais l’utiliser pour MITO.
Aucun re-run mosdepth.

## Longueurs = convention FRAG (`-F 3840`)

`samtools view -F 3840 BAM chrM` → longueur = `length(SEQ) − soft-clips CIGAR` ; **pas de MAPQ**.
Identique à `frag.nf`. Mean + median sur le même filtre. `NA` si 0 reads.

## Dual mode BETA / !BETA (rétro)

| Mode | Condition | Source |
|---|---|---|
| From-scratch | `MITO && BETA` | `BAM_FILE.join(Beta_epic.out.qc_mosdepth_merged)` |
| Rétro | `MITO && !BETA` | BAM + mosdepth déjà sous `params.output` |

Rétro : patron **TOO_RETRO** — `.filter { … .exists() }` + `log.warn`, **skip silencieux** des
samples incomplets. **Pas** de `checkIfExists: true` dans un `.map` (gotcha : tue tout le run
batch). Même process `Mito_qc`, même contrat TSV.

## NUMT différé

Tri NUMT méthylation (MitSorter-like / modkit / `mt_numt_flagged_pct`) **hors v1** — « on
verra plus tard ». Pertinence faible pour un QC d’abondance ; validation MitSorter sur gDNA
LR ≠ cfDNA court. Pas abandonné, juste hors prérequis.

## Smoke vs validation empirique

| Sample | Rôle |
|---|---|
| **Healthy_826** | Smoke câblage uniquement (~6 reads chrM) — sortie TSV présente, **pas** golden valeurs |
| **Colon_1** | Sample plus profond pour validation empirique des métriques |

Fixtures unitaires : `conformity/fixtures/mito/` + `conformity/test-mito-qc.sh` (awk mosdepth
sans BAM → longueurs NA). Check présence : `check-run-output.sh` ajoute
`MITO/{ID}.mito_qc.tsv` **si** `TYPE=liquid`. Pas encore dans `check-conformity.sh` (QUALIF
sans MITO).

## Hors scope (fermé)

- Champs `metadata.json` / rapport / Tower / trace-prod
- THEMELIO / TOO / score mito autonome
- Re-run mosdepth / source EPIC
- Bug préexistant `assets/themelio_absent.csv` (`main.nf` + `checkIfExists: true` alors que le
  fichier a été supprimé → run **solid + RAPPORT** planterait) — **signalé seulement**, ne pas
  corriger dans le chantier MITO
