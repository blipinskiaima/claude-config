# Context — Bam2Beta — 2026-09-08

**Branche** : main
**Dernier commit** : 62d9bf9 — chore(launchers): rarefaction_horaire_threshold, prod Bladder_Urine + probs trace-prod, plateforme PROD
**Status** : 1 fichier modifié (workflow/qc.nf, Mosdepth_qc EPIC commenté — Boris le réactive)

## Où j'en suis

Session du 2026-09-04→08 : module `DILUTION_LUNG` livré et commité (`18d9e57`), trace
`dilution_trace.nf` du worker des 480 dilués commitée (`641c93e`), rétro amplitude retiré
(`ec22851`), `rapport.nf` refactorisé par Boris (`7858fe7`), lanceurs (`62d9bf9`). Tout est
poussé. Une autre session a validé le module en réel sur Lung_100 + Healthy_16 (50/50 exact,
0 écart, MM 100 %) — détail dans memory/dilution-lung.md.

## Ce qui marche / ce qui foire

- ✓ `DILUTION_LUNG` : run synthétique local + Lung_100/Healthy_16 réel conformes, lanceur
  `dev/SCW/dilution_lung.sh` (1 run par paire, témoin S3, Temps 2 EXIS) prêt
- ✓ Origine des 480 dilués prouvée par les `@PG` : `~/Pipeline/Dilution/scripts/generate_dilution.sh`
- ✗ `workflow/qc.nf:59` `Mosdepth_qc(bam_epic)` commenté et NON commité : `check-run-output.sh:63`
  exige encore `merged.epic.mosdepth.summary.txt` → à réactiver avant tout `/test_bam2beta`
- ✗ `dev/SCW/rarefaction_horaire_threshold.sh` : la 1re boucle CGFL teste `${ID}_12h` comme
  témoin au lieu de `${ID}_20M` → relance des samples déjà faits (la boucle HCL teste `_5M`, OK)
- ✗ Temps 2 rarefaction threshold (récap mVAF v1.4/v1.5 par palier) toujours pas agrégé
- ⚠ `--input` obligatoire dans main.nf alors que DILUTION_LUNG ne le lit pas — Boris veut y revenir
- ⚠ Hérité V2.3.0 : `docker push raima:latest`/`0.5.6`, tarball 0.5.6 → S3, trace-prod lit des
  sorties coupées ; backfill amplitude plus possible par le pipeline (rétro retiré)

## Prochaine étape

Réactiver `Mosdepth_qc(bam_epic)` dans `qc.nf` (ou retirer la ligne 63 du contrat), commiter,
puis lancer `dev/SCW/dilution_lung.sh` depuis `~/Run3` sur les 220 paires (tmux).
