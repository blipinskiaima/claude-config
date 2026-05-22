---
name: feedback-manual-finish-pattern
description: "Pattern — finir manuellement un job bash quand le check final fail mais l'output est valide, au lieu de tout re-run"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37da32d5-7cbd-4dc3-8643-5111d2fb4e16
---

**Règle** : quand un script bash long (samtools, build, etc.) fail à la dernière étape (vérif/upload) mais a produit un output valide intermédiaire, finir manuellement les étapes restantes au lieu de re-run depuis zéro.

**Why:** Vérifié le 2026-05-22 — Phase 1 du worker `generate_dilution.sh` a fail au check MM/ML (bug pipefail/SIGPIPE cf [[feedback-bash-pipefail-sigpipe]]) après 10 min de samtools sort/merge. Le BAM dilué dans `/scratch/boris/dilution/.../{NAME}.merged.bam` était parfaitement valide (count, tags MM/ML, header). Re-runner aurait coûté 10 min de recalculs pour rien. Boris a explicitement demandé "tu peux pas t'assurer que ça aille jusqu'au bout après la génération du bam? on va reperdre 10 min sinon".

**How to apply:**
- Si trap cleanup garde le workdir sur erreur (pattern recommandé), inspecter ce qui a été produit avant de relancer.
- Si l'output est valide selon les critères du script (vérifier manuellement) → exécuter les étapes restantes à la main (vérif → upload S3 → manifest → cleanup).
- S'applique aux runs longs uniquement (>5 min). Pour les jobs courts, re-run est plus simple.
- Bien noter ce qui a été fait manuellement pour pouvoir reproduire si besoin.

**Anti-pattern** :
- ❌ Réflexe automatique de "cleanup + re-run" sans regarder l'output
- ❌ Modifier le script pendant qu'il tourne pour fixer le bug à la volée (bash peut lire en cours, ou pas)

Liens : [[feedback-bash-pipefail-sigpipe]] [[project-phase1-state]]
