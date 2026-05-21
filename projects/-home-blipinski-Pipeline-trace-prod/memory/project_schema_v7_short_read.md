---
name: schema-v7-short-read
description: Schema v7 — colonne retd_suivis.short_read tracke le subsampling short-read (75-200bp) sur S3 short_read mirror
metadata: 
  node_type: memory
  type: project
  originSessionId: 5d22bc11-28bd-47de-a329-672d09636c7c
---

# Schema v7 — colonne `short_read` (mai 2026)

`retd_suivis.short_read VARCHAR DEFAULT 'KO'` — tracke si le sample a son homologue subsamplé short-read (reads 75-200 bp) avec les 6 dossiers requis (BAM, BETA, CNV, QC, REPORT, ichorCNA) chacun non vide.

**Why:** Boris a lancé en parallèle une analyse Bam2Beta sur les BAM subsamplés short-read. Besoin de tracer dans trace-prod si le subsampling a bien tourné pour chaque sample, à l'image des autres checks. Source de vérité = présence des 6 dossiers sur S3 dans le bucket mirror `{labo}_short_read`.

**How to apply:** 
- S3 source : `s3://aima-bam-data/processed/MRD/RetD/liquid/{LABO}_short_read/{sample}/` (LABO = CGFL ou HCL, scope liquid uniquement)
- Méthode `BaseChecker.check_short_read(sample_dir, sample)` : 1 appel `aws s3 ls --recursive`, parsing du préfixe sample, set des sous-dossiers vus avec ≥1 fichier size>0
- Retourne `"OK"`, `"KO"`, ou `None` (erreur S3 transient → skip UPDATE pour preserve)
- Câblé dans `LiquidChecker.check_sample()` uniquement (pas dans SolidChecker — solid×short_read pas demandé, à étendre si besoin)
- `update-column short_read liquid CGFL|HCL` via fonction dédiée `_update_short_read()` (pattern bam_horaire, skip UPDATE si None)
- Export GSheet : header `"Short Read"` entre `"Read Start Time"` et `"BAM"` dans `_LIQUID_QC`
- Mapping `TSV_TO_DB_RETD["Short Read"] → "short_read"` (pas dans STATUS_COLUMNS — VARCHAR libre comme [[schema-v6-iv-qc]] read_start_time)

**Gotcha S3 ls --recursive** : retourne les clés S3 **complètes** (pas relatives au dossier listé). Toujours stripper avec un `sample_prefix` connu avant de faire `key.split("/", 1)[0]`. Sinon on récupère "processed" au lieu de "BAM" → faux KO systématique.

**Fonction utilitaire ajoutée** : `_s3_ls_recursive(dir_path)` dans `lib/extractors.py` (timeout 30s, retourne None sur échec).

Liens : [[schema-v6-iv-qc]] (mêmes patterns VARCHAR libre, default 'KO', preserve sur erreur S3).
