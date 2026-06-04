---
name: softclip-fragmentomics-length
description: "FRAG mesure la longueur via length(SEQ) (soft clips inclus) ; quantification empirique du soft clipping ONT sur Lung_115/95 confirme que c'est le bon choix"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0e896600-72e8-497f-9e6f-ebe884380583
---

# Soft clipping & calcul de longueur fragmentomique (module FRAG)

**Fait** : `workflow/frag.nf:50-51` extrait la longueur des fragments via
`samtools view -F 3840 -L bed_fragmentomics | cut -f10 | awk '{print length($0)}'`
= **`length(SEQ)`** (longueur du read brut, **soft clips INCLUS**). Pas le span de
référence (CIGAR), pas TLEN (= 0 en ONT single-molecule). `-F 3840` exclut
secondary + qcfail + duplicate + supplementary → primaires seuls (chimère comptée 1×).
BED = `hg38_chr1_22.bed` (autosomes seuls). Modes par densité KDE dans
`bin/fragmentomics_score.R:42-45` : mode1 ∈ [80,270] bp (mononucléosome),
mode2 ∈ [280,470] bp (dinucléosome). Score = `raima::fragmento_model_v1` (boîte noire).

**Why** : Quantification empirique du soft clipping (session trace-prod "Info BAM",
2026-06-01) sur 2 BAM HCL liquid alignés **live par minknow 6.8.11** (basecaller
hac@v5.2.0, GRCh38/hg38, samtools merge v1.13 + sort v1.22.1) :
- Lung_115 (59.3 M reads primaires) : clip moyen 6.9 bp/extrémité, 13.8 bp/read,
  taux 7.85 % des bases, 70.5 % des reads avec ≥1 clip. Read moyen ~175 bp.
- Lung_95 (13.7 M reads) : clip moyen 11.2 bp/extrémité, 22.4 bp/read, taux 9.84 %,
  54.5 % des reads avec clip. Read moyen ~227 bp.
- Reads anormaux (>50 % clippés) : 0.71 % / 0.88 % — colle à la littérature
  (~0.5 % sur humain, PLoS ONE 2021), donc normal, pas pathologique.
- Chimères/concatémères : clip max 364 kb / 169 kb mais reads avec clip >1000 bp =
  ~0–0.1 % (marginal en NOMBRE, gonfle le taux de bases mais pas le compte).
- Cause du clip = instabilité du signal ONT en entrée/sortie de pore (~130 bp
  dégradés) + Z-drop minimap2 (`-z 400,200`), PAS des adaptateurs (dorado --trim all).
- Script : `/scratch/boris/soft-clip/softclip_analyze.sh` (parse CIGAR, read-only).

**How to apply** :
- **length(SEQ) est le BON choix** pour le cfDNA ONT : capte la longueur physique
  réelle du fragment, soft clips inclus (vraies bases dégradées en bout, pas adaptateurs).
  Le span de référence SOUS-ESTIMERAIT de ~14–22 bp.
- **NE PAS migrer FRAG vers `reference_end - reference_start`** : serait une régression
  pour le cfDNA, malgré la reco FLARE 2026 (qui vise les adaptateurs non-trimmés, cas
  non applicable ici car trimming dorado maîtrisé).
- Borner les longueurs : impact **négligeable sur mode1/mode2** (déjà fenêtrés 80–470) ;
  effet seulement sur le score `fragmento_model_v1` (voit toute la distribution) s'il
  est sensible aux ~0.1 % de chimères longues. Histogramme exact des length(SEQ) jamais
  produit (read_lengths.csv = 220 Mo sur Lung_115) — à faire pour trancher définitivement.
- Filtre **mapQ ≥ 20** pertinent (jamais filtrer sur la simple présence de `S`).
  Impact modéré (anormaux déjà ~0.8 %).
- Pont méthylation (module BETA) : le hard clip sur les alignements supplémentaires
  casse les tags MM/ML → `minimap2 -Y` (soft clip forcé) recommandé pour la méthylation
  des split-reads.

Voir aussi [[bam-merge-verification]] (BAM HCL, GRCh38/hg38). Finding importé de la
session trace-prod "Info BAM" (cliSessionId 9c09127f), croisé 2026-06-01.
