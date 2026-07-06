# Context — Bam2Beta — 2026-07-06T13:42:06+0000

**Branche** : main
**Dernier commit** : a32c09b — chore(dev): maj scripts de lancement pour V2.0.0
**Status** : 2 fichiers laissés (launch_SCW.sh modifié, bacasable.sh untracked — perso Boris)

## Où j'en suis
V2.0.0 **livrée et qualifiée en production** (QUALIF/V2.0.0 écrit). Feature = le champ `tf`
du rapport porte désormais la mVAF v1.4 (bootstrap 28M) au lieu de l'ancienne mVAF.
Chantier bouclé de bout en bout : feature → repro → docker → test → maj → qualif.

## Ce qui marche / ce qui foire
- ✓ Module `rapport` (main.nf) : injecte mVAF v1.4 dans `tf` (JSON) + `mvaf` (metadata.json)
- ✓ Repro mVAF v1.4 : `set.seed(1)` + tri déterministe des bgzf (`LC_ALL=C`) avant bootstrap
- ✓ QUALIF OK : tf=0.58, scores V2/frag/bedMethyl/CNV bit-à-bit identiques vs V1.3.3
- ✓ Repro prouvée : Healthy_826 (0.58 ×3) + Breast_48 (64.91 ×3), 6 runs complets
- ✓ Docker `raima:latest`=0.5.3 poussé sur Docker Hub + tag/release GitHub V2.0.0
- ✗ Token Tower en clair dans `nextflow.config` (~L59), committé — hors périmètre, à traiter

## Prochaine étape
Sécuriser le token Tower (`nextflow.config` ~L59) : sortir en var d'env / `.env` gitignoré
(violation golden rule secrets). Sinon V2.0.0 est complète.
