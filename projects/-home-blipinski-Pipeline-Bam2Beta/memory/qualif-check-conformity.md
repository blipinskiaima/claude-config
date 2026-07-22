---
name: qualif-check-conformity
description: "Refonte de conformity/check-conformity.sh (2026-07-22) — qualif en 6 etapes, pattern valeur figee inline, 3 helpers d'extraction, cartographie valeur->fichier, etape 6 non-regression PROD bloquante"
metadata: 
  node_type: memory
  type: project
  originSessionId: f286615f-e72b-4c0e-819c-bfa96f4dc0b5
  modified: 2026-07-22T12:32:53.984Z
---

# Qualification Bam2Beta — refonte check-conformity.sh (2026-07-22)

Refactor complet de `conformity/check-conformity.sh` pilote par Boris (workflow code-workflow-feature).
Objectif : qualif rapide, lisible, maintenable, logique de controle unifiee. Tag rollback
`pre-refactor-check-conformity` (sur `03ffa1c`). **Teste 54/54 CONFORME** (PROD=V2.1.0 -> QUALIF=V2.2.0,
upload dry-run). Remplace l'ancienne description de qualif dans [[too-module]] et [[themelio-module]].

## Structure : 6 etapes sequentielles, meme pattern partout

```
1. Fichiers resultats   sous-ensemble Healthy_826 + 2 fichiers Lung_9 (too5/themelio_predictions.csv) : existence + non-vide
2. mVAF v1.4 + frag     Healthy_826, TSV natifs : 0.58 / -0.0682464198886691
3. TOO                  Lung_9, too5_predictions.csv (natif) : 8 valeurs
4. THEMELIO             Lung_9, themelio_predictions.csv (natif) : 4 valeurs
5. metadata.json        H826 (tf) + Lung_9 (13 champs) : les memes valeurs revues dans le JSON
6. Non-regression PROD  compare DIRECTEMENT PROD vs QUALIF (PAS vs figee) : (a) les 14 valeurs
                        natives (TSV/CSV, fichiers deja telecharges aux etapes 2-4) ; (b) metadata.json
                        champ par champ sur TOUS les champs communs (hors volatils)
```

**Regle "meme mecanique pour tout le monde"** (Boris) : chaque valeur est lue dans le **fichier natif**
du module PUIS **revue dans metadata.json** (etape 5). Samples reduits a **Healthy_826 + Lung_9**
(**Lung_100 SUPPRIME**). Pattern **inline repete** par valeur (pas de fonction de check — choix Boris),
comparaison de CHAINES.

## 3 helpers d'extraction (seules fonctions ; le check reste inline)

- `tsv_val f col`  -> `sed -n '2p' | cut -f<col>` (mVAF col 2, frag col 1)
- `json_val f key` -> sed, valeur **brute** (garde les quotes : `"M"` reste `"M"`, `0.58` reste `0.58`)
- `csv_val f col`  -> awk **quote-aware** par nom de colonne (retire les quotes -> `M`). OBLIGATOIRE :
  le split naif casse sur la virgule interne de `confidence_stratum` (`too_prob_Lung` sortait `TRUE`).

## Cartographie valeur -> fichier (verifiee sur QUALIF V2.2.0, fichiers reels)

Toutes les valeurs ne vivent PAS dans tous les fichiers -> 3 asymetries assumees :

| Valeur | Vit dans | Absent de | Verifiee |
|---|---|---|---|
| `result_category` (Suspicious) | CSV THEMELIO | metadata.json | etape 4 seule |
| `fragmentomics` (-0.0682…) | TSV | metadata.json | etape 2 seule |
| `exis_positivity`/`exis_quantification` (0.0042/0.11) | metadata.json | tout CSV (params nextflow.config) | etape 5 seule |

**Noms de colonnes CSV TOO != noms JSON** : `prob_Lung`->`too_prob_Lung`,
`clinical_maxp_thr`->`too_CupMaxProba_threshold`, `clinical_gate_thr`->`exis_classification_threshold`.

## Etape 6 = non-regression PROD, BLOQUANTE (decision Boris)

L'etape 6 compare **DIRECTEMENT PROD vs QUALIF** (valeur cote prod vs valeur cote version actuelle),
PAS PROD vs la figee. Boris (2026-07-22) : *"PROD vs figee n'a pas vraiment de sens, faire comme avec
les json : PROD vs qualif"*. La figee ne sert plus qu'aux etapes 2-5 (conformite de QUALIF a la
reference certifiee) ; l'etape 6 est de la non-regression pure entre 2 versions. Les fichiers QUALIF
natifs sont deja en `$TEMP_DIR/qualif_*` (telecharges aux etapes 2-4) -> reutilises, pas de re-download.

```
PROD == QUALIF       -> CONFORME (aucune regression)
PROD absent          -> WARNING non-bloquant (feature pas dans la version precedente ; teste : V2.1.0 sans THEMELIO)
PROD present mais !=  -> NON CONFORME bloquant
```
Consequence assumee : un **bump volontaire** rend PROD != QUALIF -> etape 6 KO -> upload auto annule ->
**upload manuel** (le script affiche la commande). Boris : *"en bloquant, chaque MAJ sera manuellement
revue"* (coherent ISO 15189).

**Non-regression du metadata.json (contrat de sortie UNIQUE)** ajoutee a l'etape 6 (demande Boris :
"absolument attester une non-regression sur le json entre 2 versions"). Boucle sur TOUS les champs du
JSON QUALIF hors volatils (`generated_at`, `version_*`) ET hors champs de CONTEXTE de lancement
(`patient_name` = valeur du `--mode` : QUALIF/DEV/PROD ; `client_uuid`, `analysis_name` = identite du
run), compare a PROD champ par champ :
- champ commun different -> `NON CONFORME - REGRESSION JSON <sample> <cle> : PROD=X != QUALIF=Y` (greppable, bloquant)
- champ present en QUALIF absent de PROD -> compte comme "nouvelle feature", **1 ligne WARNING recap** par sample (pas 1/champ)
- sinon -> `CONFORME - JSON <sample> : non-regression OK (N champs identiques a PROD)`
Fait pour Healthy_826 + Lung_9. **Detection prouvee** : 2 valeurs falsifiees dans un JSON PROD -> les 2
capturees. Cas V2.1.0->V2.2.0 (schema 10->29 champs) : 24 identiques + WARNING recap des nouveaux (tf,
too_prob_*, themelio_* : le metadata.json V2.1.0 etait minimaliste, enrichi en V2.2.0).

**Valide sur un vrai run de test (2026-07-22)** : `/test_bam2beta` V2.2.1 (Healthy_826 + Lung_9 via le
run-test.sh 2-samples) vs QUALIF/V2.2.0 -> 54/54 CONFORME apres exclusion des champs contextuels. Le
1er passage sortait 2 `REGRESSION patient_name : PROD="QUALIF" != QUALIF="DEV"` (le run de qualif porte
`--mode QUALIF`, le run de test `--mode DEV`) -> ce n'etait PAS une regression, d'ou l'exclusion de
`patient_name`/`client_uuid`/`analysis_name`. Le test a donc prouve a la fois que la detection marche ET
a revele les 3 champs a exclure.

## Alignement production (2026-07-22)

Les scripts qui produisent les samples ont ete alignes sur le check (2 samples : Healthy_826 + Lung_9) :
- `skills/qualif-bam2beta/scripts/run-qualif.sh` : **Lung_100 (Sample 3, ~60 min) retire** — il etait
  produit mais plus verifie par le check, et pouvait faire echouer l'etape 1 pour rien. Ne lance plus
  que Healthy_826 (~/Run) + Lung_9 (~/Run2) en parallele.
- `conformity/test.sh` (script manuel simple, 3 etapes) : mis a jour pour lancer **Healthy_826 + Lung_9**
  a l'etape 1 (le nouveau check exige Lung_9), profil `docker,tower,prod,scw`, reference QUALIF/V2.2.0.
- `skills/test-bam2beta/scripts/run-test.sh` : deja a 2 samples, rien a changer.
- `skills/maj-bam2beta` : n'utilise PAS check-conformity (commit/tag/release seulement).

Les 3 skills appellent check-conformity avec la meme signature : `check-conformity.sh $PROD_REF $OUTPUT
$VERSION $SAMPLE_ID` (PROD_REF = QUALIF precedente = reference ; OUTPUT = run a valider ; ID = Healthy_826
en $4, Lung_9 hardcode dans le script). L'ordre positionnel n'a pas change avec la refonte.

## Corrections annexes integrees

- **Compteur corrige** : chaque check = +1 sur UN seul compteur (fini le `conforme--/non_conforme++` ;
  l'ancien total sortait 37 au lieu du vrai nombre car les CONFORME de mVAF/frag ne comptaient pas).
- `usage()` : ordre `PROD_REF` / `QUALIF` remis coherent avec le code (`PROD=$1 QUALIF=$2`).
- Supprimes : pave methodo ~50 lignes (justif historique THEMELIO, plus necessaire), diff bit-a-bit
  fragmentomics, redondance Lung_9 (score+seuils lus 2x sans intention).

**Non commite au 2026-07-22** (Boris garde la main -> /save-code ou maj-bam2beta). 479 -> 526 lignes.
