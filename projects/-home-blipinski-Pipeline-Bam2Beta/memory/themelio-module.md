---
name: themelio-module
description: "Module THEMELIO (depistage cancer, Themelio 1.0.0) — wrapper minimal sans vendoring, metadata.json contrat unique, versions lues des artefacts, gardes-fous SCRIPT_FOR_MODEL, saturation mVAF"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2e80e615-d3d7-48d3-8939-11babb7ea6db
  modified: 2026-07-22T09:08:29.351Z
---

# Module THEMELIO — Depistage cancer (V2.2.0, 2026-07-21)

Score P(cancer) via XGBoost Top 10, entraine sur un pool bladder + lung early screening
(301 samples : 77 cancers, 224 sains). Decision **dual-threshold** : `Detection` (> 0.9210),
`Suspicious` (0.7250 < s <= 0.9210), `Negative` (<= 0.7250). Requiert `BETA_28M` + `FRAG`.
**Actif en prod et liquid**, OFF sur solid. Voir [[too-module]] pour le module frere.

## Wrapper minimal — decision structurante, opposee a TOO5

`bin/THEMELIO/run_themelio.R` (~60 l.) est **notre seul fichier R, aucun vendorise**.
Le `predict_themelio.R` du depot de recherche charge **16 fichiers en `source()` top-level**
(bootstrap/, misc_analyses/, tumor_of_origin/, bladder/, R/) dont **11 sont de l'infra
d'entrainement/evaluation jamais executee au scoring**. Le bundle `.rds` etant autosuffisant
(booster_raw + top_features), le wrapper se limite au chemin reel : ordonner les 10 features
selon `bundle$top_features` -> `xgb.DMatrix` -> `predict` -> classer par s1/s2.

Boris a d'abord demande une execution "strictement identique au depot" ; c'est la
**decomposition** (5 fichiers portant le modele vs 11 d'infra morte) qui a fait basculer le
choix. Ne pas re-proposer le vendoring complet sans raison nouvelle.

## Provenance des 10 features

**7 sur 10 sont deja produites verbatim par `TOO_build_input`** (6 Loyfer + `colon_1`) : meme
logique d'extraction reutilisee, **verifiee identique a 1e-12** sur Healthy_826 vs le CSV TOO5.
Les 3 autres : `mean_sqrt` = colonne `mvaf` de `raima_score.V1.4.tsv` (**echelle POURCENTAGE**,
identite avec `mvaf_v1_4` de TOO5 confirmee : 0.58 = 0.58), `frag_score_v2` = colonne `score`
et `frag_mode2` = colonne `mode2` des sorties FRAG.

Le CSV intermediaire porte le **pool complet des 51 features** (mVAF + 2 frag + 16 EPIC + 31
Loyfer) ; le wrapper ne consomme que les 10 du bundle. Evite de cueillir 6 colonnes Loyfer par
nom (fragile) et reste valable si un Themelio 1.x change de sous-ensemble.

## metadata.json = contrat de sortie UNIQUE (29 champs)

`raima_score.V2.json` **n'est plus produit** (output NF commente + awk redirige vers /dev/null,
le bloc est conserve intact -> reactiver tient en une ligne). `metadata.json` en est un
sur-ensemble strict. Non repris du V2 : `sample_id` (doublon) et `patient_id` — ce dernier
**contenait le nom du SAMPLE et non l'identifiant patient**, c'etait un bug ; `patient_name`
porte la vraie valeur.

Les valeurs cliniques sont relues des `*_kv.tsv` construits pour le V2 -> **meme source**,
aucune 2e extraction, aucune divergence possible. Chemin degrade (`Check_Input`) : memes clefs,
les nouvelles a `null`.

**CASSES CONNUES non traitees** : `trace-platform/check_platform.py:265,327` exige
`rapport_json`/`clinical_report_json` pour `bioit_status=OK` -> tous les samples passeront
FAILED au dashboard. `dev/PLT/Bam2Beta_SCW_plateforme.sh:136` (livrable client) commente par
Boris. A traiter apres le chantier Bam2Beta.

## Versions : lues de l'artefact, JAMAIS d'un param

| Champ | Source |
|---|---|
| `version_bam2beta` | `workflow.manifest.version` (V -> v) |
| `version_raima` | `packageVersion("raima")` **interroge au runtime** (`raima_version.txt`) |
| `version_too` | `bundle$model_version`, publie par `run_too5.R` |
| `version_themelio` | `bundle$themelio_version`, publie par `run_themelio.R` |

Les params `too_version` / `themelio_version` sont **SUPPRIMES** : ils ne servaient plus qu'a
l'affichage log et pouvaient diverger du bundle. Les logs lisent `{too,themelio}_version.txt`.
Prefixe `v` pose **a la publication** -> les CSV restent fideles a la valeur brute du bundle.

Cablage raima : `emit: raima_version` passe de `path` nu a `tuple(ID, path)` (joignable par
sample), expose par `Beta_28M`, transmis a `rapport`. Necessaire car **`rapportv2` (le container
qui ecrit metadata.json) n'embarque pas raima**.

## Garde-fou SCRIPT_FOR_MODEL (les 2 wrappers)

Constante declarant le bundle que le script sait traiter, verifiee au chargement. Swapper un
bundle sans adapter le wrapper -> **echec bruyant**. **Declenchement prouve** : bundle etiquete
1.1.0 face au wrapper 1.0.0 -> arret, message explicite, aucune sortie produite.
Couvre la direction dangereuse ; une retouche de script sans changement de modele reste tracee
par git et `version_bam2beta`.

## THEMELIO conditionnel

```
RAPPORT requiert BETA + BETA_28M + TOO            toujours
+ THEMELIO  si et seulement si  FRAG est actif    liquid, prod
```

Contrainte adossee a **FRAG et non au nom du profil** : c'est la vraie precondition technique.
Sur solid `FRAG=false` -> THEMELIO impossible ET hors domaine (modele entraine sur biopsie
liquide ; la fragmentomique ne mesure pas le meme phenomene sur tissu solide). Le repli est
`assets/themelio_absent.csv` (en-tete seul) : le bloc awk NR==2 ne se declenche pas,
`themelio_kv.tsv` reste vide, les champs sortent a `null`. **Verifie en execution**
(`--FRAG false --THEMELIO false` sur Healthy_826) : 29 champs, `themelio_*` ET
`version_themelio` a `null`, reste du JSON complet.

## Gotchas

- **`check.names = FALSE`** obligatoire a la lecture du CSV : sinon R renomme
  `7_Epithelium_Colon_Intestinal` en `X7_...` et la feature disparait silencieusement.
- **Ordre des colonnes = `bundle$top_features`** : XGBoost matche par POSITION, une inversion
  donne un score faux sans erreur.
- **Parse quote-aware obligatoire** sur `too5_predictions.csv` : `confidence_stratum` vaut
  `"(iii) Gate reached, low confidence"` -> virgule DANS un champ quote. Un `awk -F','` naif
  decale les colonnes 11+. **Le piege s'est reproduit pendant le dev** (diagnostic sortant
  `0.32` au lieu de `0.4.1`) -> d'ou le fichier `*_version.txt` dedie plutot qu'une relecture
  du CSV cote Groovy.
- **xgboost 3.2.1.1 exige R >= 4.3.0** : `ubuntu:22.04` + `r-base` donne 4.1.2, incompatible.
  L'image ajoute le depot APT CRAN. xgboost **epingle** + `stopifnot` fail-closed (corrige le
  caveat de `Dockerfile.too`, non-pinne).
- **Bundle re-etiquete 1.0 -> 1.0.0 a la main** : notre `.rds` n'est plus bit-a-bit identique a
  celui du depot recherche (reste en `1.0`). Un futur bundle 1.1 fera echouer le garde-fou
  (comportement voulu), mais la convention 3 chiffres sera a re-appliquer.

## Comportement du modele (observations)

- **Score sature en mVAF** au-dela d'environ 2.7 : `mean_sqrt` de 2.74 a 45.53 donne exactement
  0.855261. Le modele utilise la mVAF quasiment en **binaire** (nulle / non nulle), coherent
  avec sa distribution d'entrainement (mediane 0, 207/301 sains a zero). Consequence clinique :
  un patient a 45 % de fraction tumorale et un a 2,7 % recoivent la meme contribution mVAF.
- **`frag_score_v2` (rang SHAP 1, 0.943) est le vrai pilote**, avec bascule etroite :
  -0.0682 -> 0.9300 `Detection`, -0.10 -> 0.8846 `Suspicious`. **0.03 d'ecart change la
  categorie.** La feature s'est revelee parfaitement deterministe entre 2 runs, donc pas
  d'instabilite reelle — mais toute derive de la fragmentomique se verra d'abord ici.

## Qualification (methode en 2 niveaux, definie par Boris)

> **MAJ 2026-07-22** — check-conformity refondu : **Lung_100 retire** (seul Lung_9 + Healthy_826), 6 etapes, valeurs lues du CSV natif PUIS du JSON, etape 6 non-regression PROD bloquante. Voir [[qualif-check-conformity]].

Le **bit-a-bit vis-a-vis du depot de recherche est hors d'atteinte par construction** : le
pipeline recalcule les features au lieu de lire un snapshot trace-prod. D'ou :

| Niveau | Critere | Resultat |
|---|---|---|
| 1 | meme interpretation que le git | `Lung_100` -> 0.852987 / Suspicious = MANIFEST (0.853) |
| 2 | bit-a-bit entre 2 runs du pipeline | 15/15 fichiers identiques (Healthy_826 + Lung_9) |

`check-conformity.sh` : 13 valeurs nommees (10 TOO/exis + 3 Themelio), lues dans
**`metadata.json`**. `themelio_score` de Lung_9 = **0.855261** a ete fige **avant** que le
pipeline ne l'ait jamais produit (valeur etablie hors pipeline depuis les features QUALIF
V2.1.0) : le premier run l'a confirmee, prouvant que `THEMELIO_build_input` reproduit
l'extraction verifiee a la main. Ce n'etait donc pas une reference auto-generee.

Test isole : `bin/THEMELIO/test/run_test.sh` — 4 cas couvrant les 3 categories, sans Nextflow
ni S3. Le cas `SYNTH_Detection` est **synthetique** (vecteur Lung_9, `frag_score_v2` porte a
-0.02) : aucun sample reel disponible n'atteint s1.
