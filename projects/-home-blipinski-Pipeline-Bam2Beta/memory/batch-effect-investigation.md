---
name: Batch effect investigation CGFL vs HCL
description: Résultats complets de l'investigation batch effect inter-centres sur les scores raima, CNV, fragmentomics et déconvolution Loyfer. Findings clés et recommandations.
type: project
originSessionId: 1cb84555-6983-469f-8367-fa21820effb5
---
# Investigation Batch Effect CGFL vs HCL — 2026-04-13

## Contexte
- 680 samples CGFL liquid, 353 HCL liquid dans trace-prod
- 4 générations techniques CGFL (Guppy R9→Dorado v5.0.0), 1 config HCL
- Kit extraction : Apostle (CGFL) vs Maxwell RSC (HCL) — CONFOUNDED avec centre
- Kit barcoding : NBD114-96 multiplex (CGFL) vs NBD114-24 simplex (HCL) — CONFOUNDED

## Findings confirmés

### 1. mVAF V1 — Effet centre sur taux de faux positifs Healthy
- CGFL Healthy : 2% FP (3/149), seuil optimal = 0.000
- HCL Healthy : 17% FP (26/151), seuil optimal = 0.389 @ spec 90%
- Stable à toutes les profondeurs de rarefaction (pas un effet couverture)
- Les FP HCL ont : moins de composante sanguine Loyfer (-2.5% blood_0), plus de T-cell (+1.6%), erythroid (+1.2%)
- Distribution de longueur des reads : CGFL a des reads PLUS longs (mean 260bp epic, 7.2% >500bp) vs HCL (mean 222bp, 3.9% >500bp)
- → L'hypothèse "Maxwell co-extrait du gDNA long" est REJETÉE
- → Biais de profil de méthylation, pas de taille de fragments

### 2. mVAF V1.2 — Même pattern atténué
- CGFL Healthy : 0.7% FP
- HCL Healthy : 2.7% FP
- V1.2 (range_w=c(0,10)) réduit les FP mais le ratio HCL/CGFL reste ~4×

### 3. mVAF V2 — Faux positifs Healthy HCL
- HCL Healthy v5.0.0 : médiane V2 = 1.152 (devrait être ~0)
- CGFL Healthy v4.3.0 : médiane V2 = 0.000
- V2 systématiquement plus élevé HCL sur tous les cancer types

### 4. Score CNV — BATCH EFFECT TECHNIQUE CONFIRMÉ
- Cause : matrice regions_CNV dans raima contient 50 Healthy 100% CGFL
- HCL Healthy médiane = 4.54 (FP systématique) vs CGFL = 0.0
- Pas de corrélation avec la couverture (artefact de Simpson globalement)
- Fix : reconstruire regions_CNV avec mix CGFL+HCL

### 5. Fragmentomics mode1 — PAS de batch effect en v5.0.0
- Le "+14bp" initial était un artefact des samples rebasecallés HCL
- En v5.0.0 sans rebasecallés : Δ mode1 = 0.2bp (rien)

### 6. Déconvolution Loyfer — PAS de batch effect majeur
- Distributions cellulaires proches entre centres
- Léger excès érythroïde CGFL (+1.6%)

### 7. ichorCNA — Pas de batch effect
- Corrèle avec la charge tumorale (panel VAF)
- Healthy : CGFL 0.68% vs HCL 0.45% (proche)

### 8. Composition biologique — CONFOUNDANT MAJEUR
- CGFL Colon : 33% Cat 4 (VAF panel médiane 28%), HCL : 3% Cat 4 (VAF 1.2%)
- 234 CGFL sans metadata = 226 Lung_Alc + 8 rebasecallés/bis
- À même catégorie + même version Dorado : scores mVAF V1 proches

## Données exploratory-analysis-CGFL-HCL
- Seuil global poolé biaisé par HCL (110 sains vs 42 CGFL)
- CGFL sur-spécifique (97.6%) avec seuil global, HCL sous-spécifique (83.6%)
- Comparaisons inter-centres invalides sans harmonisation

## Recommandations
- P0 : Tester ComBat-met sur beta values pour corriger le batch effect méthylation
- P0 : Reconstruire regions_CNV dans raima avec Healthy mixtes CGFL+HCL
- P1 : Exclure les 46 rebasecallés HCL des analyses
- P2 : Harmoniser les protocoles wet-lab entre centres (long terme)

**Why:** Écart de performance du modèle ctDNA entre CGFL (100% sens MutHigh) et HCL (83.3%). L'investigation montre que les différences de scores bruts sont principalement biologiques (composition dataset), mais un batch effect réel existe sur le taux de FP Healthy (17% HCL vs 2% CGFL) et sur le score CNV.
**How to apply:** Utiliser ces findings pour guider la correction ComBat-met et la reconstruction du modèle raima.
