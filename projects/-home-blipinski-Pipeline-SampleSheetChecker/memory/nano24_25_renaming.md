---
name: NANO24/25 - renommage S3 effectué
description: Historique du renommage des runs NANO24_N4b et NANO24_N4 sur S3 (renommage effectué le 2026-05-04)
type: project
originSessionId: 2debb934-7b3e-46ad-992a-d94bed3d0396
---
**Renommage S3 effectué le 2026-05-04** (avant : variants b mal nommés ; après : noms corrects) :

- ex-`NANO24_26_N4b` → renommé en **NANO24_26_N4** (le vrai N4)
- ex-`NANO24_26_N4` → renommé en **NANO25_26_N1** (avec ajout des BAM/FASTQ qui manquaient)

**Why:** Erreur de nommage côté MinKNOW au séquençage initial : le vrai NANO25_N1 avait été uploadé sous l'étiquette NANO24_N4, et le vrai NANO24_N4 sous NANO24_N4b.

**How to apply:** Sur S3 raw/, utiliser directement les noms `NANO24_26_N4` et `NANO25_26_N1` — ils sont corrects depuis le 2026-05-04. NANO25_N1 contient maintenant 5100 BAM, 1410 POD5 et FASTQ complet (uploadés le 04/05 entre 14:53 et 15:53). Run dirs : `20260427_0958_2D_PBK97199_599ae895` pour NANO25_N1, `20260427_1000_2F_PBM05208_e30cd064` pour NANO24_N4.
