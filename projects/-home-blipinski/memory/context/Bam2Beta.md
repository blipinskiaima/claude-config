# Context — Bam2Beta — 2026-08-21T09:15:00+00:00

**Branche** : main
**Dernier commit** : 983af28 — feat(mvaf): mVAF v1.5 — correction par la couverture EPIC
**Status** : 7 fichiers non propres, tous PRÉEXISTANTS (2 dev/SCW/*.sh + 5 non trackés)

## Où j'en suis

**Deux chantiers ouverts, sans rapport entre eux.**

**(A) mVAF v1.5 — COMMITÉE** (`983af28`). Nouveau score = v1.4 corrigée par la couverture
EPIC (`raima::transfo_mvaf_by_cov`, raima 0.5.4). Voie standard + voie rétro
`--MVAF15_RETRO`, validées identiques sur `Healthy_826`. Boris a lancé un batch CGFL liquid.

**(B) Google Doc QC — onglet Synthèse livrable** (session parallèle du 21/08 au matin) :
5 QC liquid chiffrés sur 1 324 échantillons, 5 sous-onglets, arbres de décision.

## Ce qui marche / ce qui foire

**(A) mVAF v1.5**
- ✓ V1.5 standard vs rétro : `cmp` identiques · V1.4 vs QUALIF V2.2.0 : `cmp` identiques
- ✓ 200 scores bootstrap du jour == ceux de juillet → bootstrap déterministe confirmé
- ✓ Triple garde anti-écrasement testée (2e passage → `WARN`, aucun écrasement)
- ✗ **`raima:0.5.4` est LOCALE, non poussée** — le pipeline commité ne tourne que sur
  cette machine. Boris s'en occupe plus tard
- ✗ **Jamais testé en régime normal** : `Healthy_826` n'a que 6 561 reads EPIC et sature
  la correction (0,58 → 1,1e-06). Chercher un sample à 2-5 M reads EPIC
- ✗ Le nombre de samples ayant un `/BOOTSTRAP` sur S3 n'a **pas été compté**

**(B) Google Doc QC**
- ✓ Onglet Synthèse en paysage, 2 flowcharts (Exis / Thémélio), tableaux croisés
- ✗ Aucun QC implémenté — ni en base, ni dans le pipeline, ni dans `check-run-output.sh`
- ✗ « Zone grise » subsiste 15× dans le Deep Dive, 1× Lung_Alc, 1× On site

## Prochaine étape

Au choix :
- **(A)** vérifier le batch `--MVAF15_RETRO` CGFL liquid, puis tester la chaîne sur un
  sample à 2-5 M reads EPIC ; pousser `raima:0.5.4` avant toute qualification
- **(B)** aligner « zone grise » → « suspicion d'artefact » dans le Deep Dive
  (15 occurrences), en `replaceAllText` avec `tabsCriteria` et phrases entières
