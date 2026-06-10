---
name: project_frag_softclip_trim
description: "AlCapone/Lung_Alc = re-basecalls offline hétérogènes (trim barcode ON/OFF). frag_mode v1 (filtered) gonflé jusqu'à +148bp sur ~81 samples ; seul frag_mode_sc (filtered_softclipped) donne le vrai mode mononucléosome. Delta filtered−sc = détecteur du trim manquant."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1e9a80d5-2319-41ac-9f79-1b0e706fbd39
---

Découverte juin 2026 (en analysant Lung_Alc_6_av puis toute la cohorte liquid).

**Les BAM Lung_Alc / cohorte AlCapone sont produits par re-basecalling OFFLINE manuel** (`ont_basecall_client` lisant des POD5 archivés sur disques externes WD My Book Duo, `--save_path /data/[Aa]lcapon/...`), PAS par le séquenceur en live. C'est pourquoi `pod5_adresse` est NULL (jamais passés par l'arborescence S3 standard) et qu'**aucun rapport HTML MinKNOW n'existe** côté AIMA (resté sur la machine d'acquisition CGFL). Le `@RG DT` du header donne la vraie date de run (Lung_Alc_6 = 2025-01, Lung_Alc_02 = 2024-11), ≠ date d'upload S3 (souvent +1 an).

**Lots hétérogènes** : versions client 7.6.7 → 7.9.8, `--config *.cfg` (ancien) vs `--model ...hac@v5.0.0`, qscore 8 vs 9, et surtout **`--enable_trim_barcodes` présent OU absent** selon le lot. Tous en `--barcode_kits SQK-NBD114-96` (barcode classé → SM:barcodeNN, mais pas toujours trimmé).

**Mécanique softclip vs trim** :
- `--enable_trim_barcodes` (basecall) retire physiquement le barcode du read par reconnaissance de séquence.
- S'il est absent, le barcode reste dans le read → non aligné à la réf → **softclippé** (CIGAR `S`, bases présentes mais non alignées).
- Retirer les softclips après alignement « rattrape » l'absence de trim : barcode non trimmé → dans le softclip → retiré.

**Impact fragmentomique** (frag_mode = mode de la distribution de longueurs) :
- `frag_mode1/2` (filtered, schema v2) = longueur **AVEC** softclips → barcode non trimmé gonfle le mode (~267 bp au lieu de ~167).
- `frag_mode1_sc/2_sc` (filtered_softclipped, schema v10) = longueur **APRÈS retrait** des softclips → vrai mode mononucléosome (~167 bp), **invariant au mode de basecalling**.

**Données (1214 liquid avec les 2 versions, juin 2026)** : delta médian `frag_mode1 − frag_mode1_sc` = 0,9 bp ; 1111 propres (Δ<5) ; **81 samples gonflés (Δ≥30, jusqu'à 148 bp)** = basecallés sans `--enable_trim_barcodes`. Ex : Lung_Alc_28_av 267,7 → 165,0 (Δ≈102 = barcode+adaptateur × 2 bouts).

**Preuve causale** : Lung_Alc_6_av (Δ≈0) header AVEC `--enable_trim_barcodes` ; Lung_Alc_02_av (Δ=123) header SANS (grep = 0).

**À retenir pour l'analyse** : pour toute fragmentomique cross-cohorte, utiliser **`frag_mode*_sc` exclusivement** — `frag_mode*` (v1) contient ~81 valeurs faussées. Le delta `frag_mode1 − frag_mode1_sc` est un détecteur fiable du trim manquant / des softclips résiduels.

Voir [[project_schema_v10_frag_sc]], [[project_schema_v11_mvaf_v13_frag_score]], [[project_columns_index]].
