# Context — Bam2Beta — 2026-06-17

**Branche** : main
**Dernier commit** : b36adba — chore(raima): bump image bootstrap raima:0.5.1 -> 0.5.2
**Status** : clean (seul dev/SCW/bacasable.sh untracked, sandbox exclu)

## Où j'en suis
Feature bootstrap mVAF v1 complète, image bumpée sur raima:0.5.2 (sortie Florian), commitée + pushée (b36adba).
Validée bit-à-bit (200/200) sur 2 samples : Breast_10 (CGFL, image 0.5.1) et Lung_138 (HCL, image 0.5.2).
Aucune tâche en cours.

## Ce qui marche / ce qui foire
- ✓ raima:0.5.2 buildée (future+withr, bootstrap_model_v1 exporté) ; latest 0.5.0 + 0.5.1 intactes
- ✓ Lung_138 HCL liquid : 200/200 scores bit-à-bit identiques réf Florian (image 0.5.2)
- ✓ Breast_10 CGFL liquid : 200/200 identiques (image 0.5.1)
- ✓ Commit b36adba pushé ; CLAUDE.md + MEMORY + topic file à jour 0.5.2
- ⏳ Images 0.5.1/0.5.2 NON pushées sur Docker Hub (OK mono-nœud SCW ; push si multi-nœuds)
- ⏳ Preuve non-régression S3 Colon_2 (inventaire avant/après) jamais finalisée — optionnel, feature déjà validée sur 2 samples

## Prochaine étape
Rien de bloqué. Pour un rollout bootstrap large : adapter le grep de dev/SCW/launch_SCW.sh et lancer sur la cohorte. Push Docker Hub si run hors mono-nœud.
