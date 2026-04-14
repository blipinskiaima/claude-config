---
name: Batch effect investigation CGFL vs HCL
description: Résultats complets de l'investigation batch effect inter-centres sur les scores raima, CNV, fragmentomics et déconvolution Loyfer. Identification des 2 batch effects racines (EPIC→ONT + kit extraction) et conclusions sur ComBat-met.
type: project
originSessionId: 1cb84555-6983-469f-8367-fa21820effb5
---
# Investigation Batch Effect CGFL vs HCL — 2026-04-13/14

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

## Test ComBat-met (2026-04-14) — Non retenu

4 variantes testées (group=H/C, rebalancé, ref.batch=CGFL, Healthy only). Aucune ne fonctionne :
- Option A (rebalancé) : 3.1% → 30.6% FP HCL Healthy (pire)
- Option B (ref=CGFL) : perte totale TP CGFL (0%), FP HCL 92.9% (catastrophique)
- Option C (Healthy only) : 3.1% → 10.2% FP (dégradation)

**Finding inattendu** : la simple reconstruction du bedMethyl (coverage fixé à 10, filtre CpGs modèle V1, présence ≥80%, imputation NAs) réduit 17% → 3% de FP HCL Healthy **sans appliquer ComBat-met**. Le problème est en grande partie technique (couverture variable, CpGs manquants) et pas biologique.

**Conclusion** : ComBat-met crée une dépendance batch-spécifique incompatible avec la production ISO 15189. Non retenu. Infrastructure conservée dans `~/Pipeline/ComBat-Met/`.

## Les 2 batch effects racines identifiés

### 1. Batch effect cross-technologie : EPIC → ONT (MAJEUR)

Le modèle raima V1 a été entraîné sur **19 références EPIC bisulfite microarray** (REF1_breast_0, REF2_blood_0, REF3_liver_1...). Il est appliqué en production sur des données ONT nanopore. Ces deux technologies produisent des profils de méthylation **non strictement comparables** :
- Bisulfite microarray : conversion chimique puis hybridation
- ONT direct : lecture directe de 5mC/5hmC par nanopore

Conséquence : tous les samples ONT ont un biais par rapport aux références EPIC. Ce biais n'est **jamais corrigé** dans le pipeline actuel.

### 2. Batch effect inter-kit extraction : Apostle vs Maxwell (AMPLIFICATEUR)

Chaque centre utilise un kit d'extraction différent :
- **CGFL : Apostle MiniMax** (nanoparticules propriétaires, optimisé cfDNA court)
- **HCL : Maxwell RSC Rapid ccfDNA** (billes magnétiques standards Promega)

Les 2 kits ont des **chimies de surface différentes** → biais de capture CpG différent :
- Quels CpGs sont capturés
- Dans quelles proportions
- Avec quelles probabilités de modification

Par chance, **Apostle produit des profils ONT plus proches des références EPIC** que Maxwell. C'est ce qui fait que CGFL a 2% FP et HCL 17%. Ce n'est pas que CGFL est "meilleur" — c'est qu'il matche mieux le biais technologique du modèle.

### Interaction des 2 effets

```
Référence raima V1
  = 19 EPIC bisulfite arrays
         │
         │ (biais de technologie)
         ↓
  Appliqué à ONT modkit pileup
         │
    ┌────┴────┐
    ↓         ↓
  CGFL       HCL
 Apostle   Maxwell
  ↓           ↓
Biais kit   Biais kit
proche      éloigné
des refs    des refs
EPIC        EPIC
  ↓           ↓
 2% FP      17% FP
```

### Comment trancher kit vs centre

Expérience contrôlée (wet-lab) : même plasma sain → aliquote 1 avec Apostle → ONT → score A ; aliquote 2 avec Maxwell → ONT → score B. Si A ≠ B → kit extraction confirmé comme driver. Nécessite négociation avec un des centres pour tester les 2 kits.

## Données exploratory-analysis-CGFL-HCL
- Seuil global poolé biaisé par HCL (110 sains vs 42 CGFL)
- CGFL sur-spécifique (97.6%) avec seuil global, HCL sous-spécifique (83.6%)
- Comparaisons inter-centres invalides sans harmonisation

## Recommandations finales (révisées 2026-04-14)

### P0 — Fix les 2 batch effects en même temps
- **Ré-entraîner raima V1 avec références ONT** — remplacer les 19 EPIC arrays par des Healthy ONT mixés (CGFL + HCL). Résout EPIC→ONT **et** compense le biais Apostle/Maxwell puisque les 2 kits sont dans la référence. Nécessite Florian.
- **Reconstruire regions_CNV raima avec Healthy mixtes CGFL+HCL** — fix spécifique au module CNV (matrice 100% CGFL actuellement).

### P1 — Quick wins / long terme
- **Normaliser la couverture et filtrer CpGs bien couverts en pré-scoring** — réduit 17% → 3% FP HCL sans re-entraînement.
- **Exclure les 46 rebasecallés HCL** des analyses (artefacts fragmentomics).
- **Harmoniser les protocoles wet-lab entre centres** — seule solution durable pour le batch effect kit (mais long terme, négociation labos).
- **Expérience contrôlée Apostle vs Maxwell sur même plasma** — tranche définitivement si le driver est le kit ou un autre facteur wet-lab.

### P2 — Documentation qualité
- **Documenter le biais EPIC→ONT** dans le dossier qualité ISO 15189 — finding clé, doit être tracé.
- **Documenter le batch effect kit extraction** comme variable confondante connue.

**Why:** Écart de performance du modèle ctDNA entre CGFL (100% sens MutHigh) et HCL (83.3%). L'investigation (12 pistes explorées) révèle 2 batch effects racines superposés : technologique (EPIC→ONT, majeur) et chimique (Apostle vs Maxwell, amplificateur). ComBat-met ne résout ni l'un ni l'autre (dépendance batch-spécifique + incompatible avec les refs EPIC). Le fix durable est de ré-entraîner raima avec des références ONT mixtes.
**How to apply:** En cas de nouveau problème batch effect, vérifier d'abord la matrice de référence raima et le kit d'extraction. Ne pas retester ComBat-met.
