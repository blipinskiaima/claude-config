---
name: pod5_verification script
description: Script pod5_verification_gen.py pour générer pod5_verification.tsv (vérification croisée POD5 AWS/SCW CGFL liquid)
type: reference
---

Script : `pod5_verification_gen.py` à la racine du projet.

**Usage** : `python3 pod5_verification_gen.py`

**Prérequis** :
- DuckDB avec bam_metadata (stockage_pod5, pod5_adresse)
- aws CLI configuré avec profils `aws` et `scw`
- `/tmp/metadata_CGFL.tsv` (via `python3 database/check_samples.py fetch-gsheet metadata_CGFL`)

**4 étapes en un seul script** :
1. Correspondance DB → S3 : query DuckDB + listing des runs AWS/SCW
2. Nombre et taille par adresse unique : `aws s3 ls --summarize --recursive`
3. Concordance gsheet : croisement run_id (DB) vs Run number (metadata_CGFL)
4. Ratio contiguïté : indices POD5 (`_N.pod5`) par run, `actual/expected (%)`

**Colonnes (13)** : Sample, Stockage DB, Adresse POD5 AWS, Adresse POD5 SCW, Nombre AWS, Taille AWS (GiB), Nombre SCW, Taille SCW (GiB), Identique nombre, Identique taille, Concordance, Ratio AWS, Ratio SCW
