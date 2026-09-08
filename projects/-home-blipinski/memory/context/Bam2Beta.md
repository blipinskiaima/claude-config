# Context — Bam2Beta — 2026-09-08T09:04+00:00

**Branche** : main
**Dernier commit** : 62d9bf9 — chore(launchers): rarefaction_horaire_threshold, prod Bladder_Urine + probs trace-prod, plateforme PROD
**Status** : 1 fichier modifié (`workflow/qc.nf`, Mosdepth_qc EPIC commenté — Boris le réactive lui-même)

## Où j'en suis

Module `DILUTION_LUNG` livré, commité et pushé (`18d9e57`) : BAM dilué 50/50 lung/healthy par
paire de `early_lung_dilution_pairs.tsv` (220 paires HCL). Validé par run synthétique + vérification
indépendante sur `Lung_100_Healthy_16_50_50` (50/50 exact, 0 écart sur 45 459 407 ids healthy,
MM 100 %). Lanceur `dev/SCW/dilution_lung.sh` (Temps 1 dilution + Temps 2 EXIS) prêt, 1 paire
faite sur S3. Orphelins `RETRO_FRAG_AMPLITUDE` retirés (`ec22851`). Détail : memory/dilution-lung.md.

## Ce qui marche / ce qui foire

- ✓ 5 commits pushés (dilution lung, trace 480 dilués, refactor rapport.nf csv_to_kv, lanceurs)
- ✓ Lung_100_Healthy_16_50_50 sur S3 (40,7 Go, ~1 h), fichiers de contrôle dans
  `/scratch/boris/dilution_lung_check/` (16 Go, supprimables)
- ✗ 219 paires restantes à générer (Temps 1), puis EXIS sur les 220 (Temps 2) — ~1 h/paire
- ✗ `workflow/qc.nf` : `Mosdepth_qc` EPIC commenté non commité ; `check-run-output.sh:63` exige le
  summary EPIC → à réactiver avant tout `/test_bam2beta` (Boris s'en charge)
- ✗ `--input` obligatoire dans `main.nf` alors que DILUTION_LUNG ne le lit pas — Boris veut y revenir
- ✗ Hérité V2.3.0 : `docker push raima:latest/0.5.6`, tarball 0.5.6 → S3, backfill amplitude
  (plus de voie rétro), trace-prod lit des sorties coupées, Temps 2 rarefaction threshold à agréger

## Prochaine étape

Réactiver `Mosdepth_qc` dans `qc.nf`, puis lancer `dev/SCW/dilution_lung.sh` dans un tmux depuis
`~/Run3` pour les 219 paires restantes.
