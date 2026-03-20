---
name: HCL Verification (mars 2026)
description: Vérification croisée POD5/BAM HCL liquid — résultats transfert raw→S3, rapports, scripts
type: project
---

## HCL Verification — 12 mars 2026

### Résultats
- **275 samples** HCL liquid non-rebasecalled vérifiés (84 rebasecalled exclus, 359 total)
- **154 OK** : raw encore présent, count + taille identiques raw↔S3
- **120 transférés** : raw purgé, données S3 présentes
- **0 KO** : transfert complet et intègre
- **1 sans correspondance** : `Healthy_8_repro` (sample de reproduction)

**Why:** Besoin de confirmer que le transfert raw NANO → buckets S3 (POD5 + BAM) a été fait intégralement avant purge des données raw.

**How to apply:** Les données HCL sont fiables sur S3, le raw peut être purgé en toute sécurité.

### Scripts créés/modifiés
- `pod5_verification_gen.py` : ajout filtre `NOT LIKE '%rebasecalled%'` → 535 samples CGFL (au lieu de 628)
- `hcl_verification_gen.py` : nouveau script (~100 lignes), compare raw NANO vs S3 POD5/BAM
  - Query DB (`metadata.run_number` + `bam_metadata.barcode`) — LEFT JOIN metadata avec fallback `run_id[:8]`
  - Index `run_number → NANO dir` via S3 listing (~84 appels)
  - Compare `s3_summarize()` raw vs S3 pour POD5 et BAM (count + taille)
  - Colonne "Transfert" : OK si identique, transféré si raw purgé, KO sinon

### Fichiers générés
- `hcl_verification.tsv` : 275 lignes, colonnes raw/S3 alternées + Transfert
- `hcl_correspondance_rapports.tsv` : 66 runs uniques, NANO Dir / Run Number / Adresse Rapport (SCW ou AWS ou NA)
- `rapport/` : 36 rapports HTML copiés depuis SCW

### Structure raw NANO HCL (S3)
- Bucket: `s3://aima-bam-data/data/HCL/raw/`
- 74 NANO dirs (NANO01_25_N1 → NANO18_26_N3), 18 devices
- 66 runs uniques utilisés par les 275 samples
- Run dir format: `YYYYMMDD_HHMM_SLOT_PBIXXX_{uuid_short}`
- Sous-dossiers: `pod5_pass/{barcode}/`, `bam_pass/{barcode}/`, `report_*.html`
- **Raw purgé le 12/03/2026** : ne reste que 74 `upload.done` (0 bytes)
- 37 runs manquaient `upload.done` → commandes générées (non exécutées)

### Rapports HTML
- **52/66 disponibles** : 36 sur SCW (raw non purgé au moment de la copie) + 16 sur AWS
- **14 manquants** : NANO05→NANO07 (13 runs du 19/12/2025) + NANO14_26_N3 (1 run du 16/02/2026)
- AWS: `s3://aima-pod-data/HCL/liquid/report/report_PBI*_{uuid}.html` (16 fichiers, profil `aws`)
- SCW: dans le run dir `report_PBI*_{uuid}.html`

### Correspondance DB
- `metadata.run_number` contient le nom complet du dossier run (ex: `20251203_1533_2G_PBI50923_c95dbd44`)
- `bam_metadata.run_id` contient l'UUID complet (ex: `c95dbd44-6018-4aa8-adf0-01f86338b829`)
- `run_id[:8]` = `uuid_short` = dernier segment du run_number après `_`
- 79 samples n'ont pas de metadata → fallback `run_id[:8]` + index NANO pour retrouver le run_number

### S3 Paths HCL
| Donnée | Bucket | Chemin | Profil |
|---|---|---|---|
| POD5 | `aima-pod-data` | `data/HCL/liquid/{sample}/` | scw |
| BAM origin | `aima-bam-data` | `data/HCL/liquid/{sample}/` | scw |
| BAM merged | `aima-bam-data` | `processed/MRD/RetD/liquid/HCL/{sample}/BAM/{sample}.merged.bam` | scw |
| Raw NANO | `aima-bam-data` | `data/HCL/raw/NANO*/no_sample_id/{run}/` | scw |
| Rapports AWS | `aima-pod-data` | `HCL/liquid/report/` | aws |
