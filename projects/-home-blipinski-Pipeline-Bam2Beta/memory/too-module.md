---
name: too-module
description: "Module TOO (Tumor of Origin, TOO5 v0.4.1) — vendoring, source de vérité des seuils, gotchas parse/R, qualification Lung_9"
metadata: 
  node_type: memory
  type: project
  originSessionId: 19867b45-e45c-44b5-8bc4-85e392acf56f
  modified: 2026-07-22T09:08:26.751Z
---

# Module TOO — Tumor of Origin (V2.1.0, 2026-07-16)

Prédit 5 classes tumorales (Lung, Colon, Prostate, Bladder_Pancreas, Breast) depuis 16 props EPIC
bootstrap + 31 Loyfer + mVAF v1.4 + sexe. **Actif en prod.** Requiert `BETA_28M` + `IV`.
Décision 2 étages : gate mVAF v1.4 ≥ 0.32, puis max_p ≥ 0.825743846152373 sinon `Unresolved`.

## Vendoring — ne pas confondre les 4 scripts

| Fichier | Origine | Modifiable ? |
|---|---|---|
| `too_common.R` (568 l.) | **Vendorisé** @ `exploratory-analysis-CGFL-HCL:too5_v0_4_1` | NON |
| `too5_utils.R` (958 l.) | **Vendorisé** | NON |
| `functions_prepare_data.R` (716 l.) | **Vendorisé** | NON |
| `run_too5.R` (54 l.) | **Notre wrapper** Nextflow | OUI — toute adaptation va ici |

**Les scripts R ne sont PAS dans l'image Docker** : `Dockerfile.too` n'a aucun `COPY`, le process
charge `${projectDir}/bin/TOO/run_too5.R`. Donc : modifier `bin/TOO/` ne nécessite **aucun rebuild** ;
à l'inverse `too:0.4.1` **ne garantit pas** la version des scripts.

`params.too_version` désigne le **modèle** (bundle + vendorisés), pas le wrapper — celui-ci est
versionné par le pipeline. Un re-vendoring impose de mettre à jour à la main `too_version`,
`too_model` et les en-têtes des 4 scripts. Le container ne bouge que si l'env R change.

## Source de vérité des seuils : le bundle, PAS too_common.R

`too5_utils.R:818-819` applique `bundle$clinical_{gate,maxp}_thr`. Les constantes
`too_common.R:56-57` ne servent qu'à **construire** le bundle et de fallback — s'y fier serait faux.
Il existe même une 4e copie déjà désynchronisée : `too5_utils.R:803` dit `max_p 0.826` (arrondi).

Depuis V2.1.0, `run_too5.R` publie les 2 seuils appliqués dans son CSV → `rapport.nf` les recopie
dans le JSON. Le JSON ne peut donc plus annoncer un seuil différent de celui qui a produit
`final_decision`, même après un bump. Voir [[bootstrap-model-v1]] pour la mVAF v1.4 en entrée.

| Seuil | Source | v0.4.1 |
|---|---|---|
| `too_CupMaxProba_threshold` | bundle `.rds` | 0.825743846152373 |
| `exis_classification_threshold` | bundle `.rds` | 0.32 |
| `exis_positivity_threshold` | param `nextflow.config` | 0.0042 |
| `exis_quantification_threshold` | param `nextflow.config` | 0.11 |

Les 2 seuils `exis_*` n'existent nulle part ailleurs (ni R, ni bundle) : constantes d'affichage
pures, aucun risque de dérive → les params sont leur bonne place.

## Gotchas (tous rencontrés et vérifiés)

- **Parse CSV quote-aware OBLIGATOIRE** dans `rapport.nf` : `confidence_stratum` vaut
  `"(ii) Gate reached, high confidence"` → virgule DANS un champ quoté. Un `awk -F','` naïf décale
  les colonnes 11+ donc les 5 probas (vérifié : `too_prob_Lung` sortait à `TRUE`).
- **Pas d'apostrophe dans les commentaires du bloc awk** de `rapport.nf` : il est entre quotes
  simples dans le shell, un `d'appliquer` ferme la chaîne.
- **`pred$x <- NULL` SUPPRIME la colonne** en R au lieu de la créer → `thr_or_na()` renvoie un
  `NA_real_` explicite.
- **`normalize_sex` upstream est cassé** (`x | logical(0)` si `sex_predicted=NULL`) : le sexe est
  converti en `TRUE`/`FALSE` en bash en amont, ce qui emprunte la branche `is.logical`.
- **Bug channel latent** : `Channel.fromPath()` = queue channel à 1 item ; consommé en `path()`
  simple il limite le process à **une exécution par invocation**. Sans effet en prod (1 sample par
  run) ; en multi-samples, 7/10 samples perdaient leur `props_loyfer`. **Fait manquer des sorties,
  jamais de résultat faux.** `.first()` posé sur `RAIMA_LOYFER` + `RAIMA_V1_WL` ; le motif subsiste
  sur `RAIMA_MODEL1/2`, `ANCESTRY_MODEL`, `BED`, `FASTA`, `FAI` (candidat patch V2.1.1).

## Qualification

> **MAJ 2026-07-22** — check-conformity refondu (6 etapes, **Lung_100 retire**, valeurs figees lues du CSV natif PUIS du JSON, etape 6 non-regression PROD). Voir [[qualif-check-conformity]]. Ci-dessous = etat V2.1.0.

Règle : **Healthy_826 qualifie les process actuels, Lung_9 (HCL liquid) qualifie TOO5**. Les 2
tournent en parallèle, 2 lignes Nextflow, même output, même profil.

`check-conformity.sh` fige **12 valeurs nommées** (5 probas + `sex` + 4 seuils sur Lung_9 ; mVAF
v1.4 + fragmentomics sur Healthy_826) → `VALEUR KO - <métrique> : lu X != qualifié Y`, greppable.
**Bit-à-bit abandonné** : casse dès qu'on ajoute un champ, et ne nomme pas la métrique fautive.

**Piège de méthode** : régénérer une référence depuis le run qu'on qualifie compare le run à
lui-même → ne prouve que la reproductibilité, jamais la non-régression. Règle : KO → lire le diff
→ juger si le changement est voulu → alors seulement mettre à jour.

Références : Lung_9 bit-à-bit identique au 1er run S3 (`DEV/TOO_test/loop_20260715_091150`,
15/07) sur les 20 colonnes communes. Golden = `conformity/example_ensemble_scores_10_samples.csv`
(10 samples) : interprétation identique, écarts ≤ 1.6e-03 dus à la graine du bootstrap mVAF v1.4
(`mvaf_v1_4` 2.73 golden vs 2.74 pipeline), marge de 16 points sous le seuil.
