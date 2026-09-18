---
name: bp5base-deux-apps-basespace-healthy634
description: "BP_5base n'est pas homogène : 7 samples via DRAGEN Germline 4.4.6, Healthy634 via DRAGEN Methylation Pipeline 4.4.6000. Le README dit le contraire."
metadata:
  type: project
---

Les 8 samples BP_5base n'ont **pas** tous été traités par la même app BaseSpace, contrairement à ce qu'affirment `BP_5base/README_bp_5base.md` et le `README.md` racine.

- **7 samples** (Breast18, Colon25, Colon50, Colon62, Healthy767, Lung12, Lung8) → **DRAGEN Germline 4.4.6**, 4 AppSessions entre le 2026-02-03 et le 2026-02-04. Bloc QC avec ~60 clés `variants_*` : le variant calling germline a tourné, les VCF existent côté BaseSpace mais `bp_5base.sh` ne télécharge que `CX_report.txt.gz` + `metrics.json` — ils n'ont jamais été récupérés.
- **Healthy634** → **DRAGEN Methylation Pipeline 4.4.6000**, relancé seul le 2026-02-05. Zéro clé `variants_*`.

**Why:** Healthy634 est un des deux contrôles sains qui définissent le plancher mVAF ~1,7 du 5base. Le traiter comme comparable aux 7 autres est une erreur de lecture. Corroboré par deux signaux : son `mapped %` = **86,19** contre 96,34–99,22 pour les 7 autres, et `info.txt` qui porte deux scorings distincts pour ce sample (mVAF 1,525 puis 1,745, archivé à 1,742). La conclusion « plancher ~1,7 » survit quand même, car Healthy767 (Germline, 1,70) donne la même valeur.

**How to apply:** La source de vérité est le fichier `{SAMPLE}_ds.<hash>.json` archivé dans `s3://aima-bam-data/processed/short-read/result/BP_5base/{SAMPLE}/` — champ `.AppSession.Application.Name`. Le CLI `bs` (v1.7.0, configuré) renvoie aujourd'hui des listes **vides** (plus aucun projet ni appsession) : ce `_ds.json` est la seule trace exploitable, et il ne couvre que le dataset effectivement téléchargé. Ne pas conclure sur l'absence d'autres sessions BaseSpace.

Attention : le chemin S3 du README (`.../result/BP_5base/`) est le bon ; celui codé dans `bp_5base.sh` (`.../short-read/BP_5base/`, sans `result/`) n'existe pas.

Voir [[project_bp5base_colon50_62_mvaf]] pour l'autre particularité du jeu (Colon50/Colon62 identiques par arrondi).
