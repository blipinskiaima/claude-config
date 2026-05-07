---
name: Upload planifié NANO22/23 - vendredi 8 mai 22h
description: Upload programmé des runs initiaux manquants pour NANO22 et NANO23, prévu le 8 mai 22h, réception attendue lundi 11 mai
type: project
originSessionId: 2debb934-7b3e-46ad-992a-d94bed3d0396
---
**Upload programmé : vendredi 2026-05-08 à 22h00.**

Runs initiaux manquants à uploader (9 runs au total — N2 déjà sur S3 depuis le 24/04) :

- **NANO22** : N1, N2B, N3, N4 (N2 déjà reçu)
- **NANO23** : N1, N2, N3, N4
- **NANO14_26_N3** : run historique (Healthy_83-86) supprimé le 12 mars, jamais re-uploadé jusqu'ici

**Réception attendue : lundi 2026-05-11** (l'upload se déroule pendant le week-end).

**Why:** Sur S3 raw/, on a actuellement les variants `NXb`/`NXc` (re-séquences) mais pas les runs initiaux. Boris a planifié l'upload de ces originaux pour combler les trous.

**How to apply:**
- Ne pas s'inquiéter si rien n'est uploadé entre le 4 et le 8 mai côté NANO22/23.
- À partir du lundi 11 mai, vérifier l'arrivée des 9 runs sur S3 : `aws s3 ls s3://aima-bam-data/data/HCL/raw/`.
- Croiser avec la gsheet metadata_HCL pour générer les samplesheets correspondantes.
