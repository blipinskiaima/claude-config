---
name: project-active-cancer-audit
description: "Audit active_cancer (11/09/2026) — active_cancer_clinical est une colonne MORTE (0 valeur, clé gsheet inexistante) ; la colonne vivante est active_cancer. Définition opérationnelle en aval (Aima-Tower), pas dans trace-prod. L'historique d'une gsheet s'exporte révision par révision via l'API Drive."
metadata: 
  node_type: memory
  type: project
  originSessionId: ba1678a2-e07b-4afd-a724-0181a1d96f61
  modified: 2026-09-11T15:14:13.039Z
---

# Audit `active_cancer` — gsheet CGFL (11/09/2026)

Demande Boris : vérifier que toute l'info de la gsheet `metadata_CGFL` est en base, puis lister
les échantillons dont le statut « active cancer » est douteux. **Aucune modification appliquée**
au titre de l'investigation (seul un import de rattrapage a été lancé, voir plus bas).

## ⚠⚠ `active_cancer_clinical` est une colonne MORTE — ne pas la prendre pour la bonne

| Colonne gsheet | Colonne DB | Réalité |
|---|---|---|
| `Presence of an active cancer (sampling at active disease, no post-op)` | **`active_cancer`** | CGFL 365 valeurs, HCL 251 — **c'est la vraie** |
| `…, according clinical files, needed for cancer samples without mutation` | `active_cancer_clinical` | **n'existe dans AUCUNE des 2 gsheets → 0 valeur sur 1136 lignes** |

Ajoutée au commit `6ebd388` (schema v2) **dans le littéral `CREATE TABLE` sans `ALTER TABLE`** —
donc sur une base déjà existante le code n'a jamais pu la créer. Côté HCL il existe une
`[DEPRECATED] Presence of an active cancer (…), according mutations detected on ctDNA` (col 25)
au libellé différent, **non mappée** : jamais importée.

**How to apply:** toute question sur le cancer actif se traite sur `metadata.active_cancer`.
Si quelqu'un (y compris Boris) désigne `active_cancer_clinical`, le dire : elle est vide.

## La définition n'est pas dans trace-prod

`active_cancer` est un VARCHAR libre, pass-through, **jamais interprété par trace-prod**. Seules
gloses : le header gsheet lui-même (`lib/duckdb.py:1011`) et `README.md:224` (« Cancer actif
(oui/non) »). La définition **littérale** tient dans le header : prélèvement fait *en maladie
active*, et *pas en post-opératoire*.

La définition **opérationnelle** vit dans Aima-Tower (`src/exploratory_compute.py:33,326-339`),
portée depuis `exploratory-analysis-CGFL-HCL/02_sensitivity_specificity.R:46-48` :

```python
ACTIVE_CANCER_TRUE = {"yes","oui","y","1","true"}        # casse ignorée
cancer_truth = mutated_flag | active_cancer_flag | indication ∈ {TNE,Nuclear,Bladder_*}
```

→ `Suspicion`, `imagerie suspecte`, `probable`, `External quality control sample` comptent
**comme non-actifs**. ⚠ 3 règles divergentes coexistent : raima (`R/evaluate-score.R:268`) compte
`SUSPICION` comme actif (branche probablement morte : le gsheet brut dit « image suspecte »),
`Feature` isole `imagerie suspecte` dans un bucket « suspect » hors-KPI, Bam2Beta/TOO est
case-sensitive.

## Trou d'harmonisation côté HCL

`HARMONIZATION_RULES["active_cancer"]` (`lib/harmonization.py:29`) n'attend que
`image suspecte` → **`imagerie suspecte` (25 lignes HCL) n'est jamais harmonisée**, et
`probable` (13 HCL) / `External quality control sample` (13 CGFL) ne sont couverts par aucune
règle. Le CGFL est propre (saisie déjà en anglais).

## Concordance gsheet ↔ base, et import de rattrapage

`active_cancer` : **0 divergence** sur les 412 samples comparés, propagation rebasecalled exacte
(222/51/16/12 des deux côtés). Manquaient en revanche 97 lignes `metadata` entières
(90 `Bladder_Urine` + 7 `Twist`), 60 `stage` et 4 `class` — base en retard sur la gsheet.
`import-metadata liquid CGFL` lancé par Boris le 11/09 : 526 → **623** lignes, 0 divergence
résiduelle sauf l'écart voulu ci-dessous.

⚠⚠ **Écart volontaire non verrouillé** : les 4 `Lung_13*` restent `class='Lung'` alors que la
gsheet dit `Endometrium` (choix de Boris : ne pas changer l'indication, qui alimente la Tower).
**Le prochain `import-metadata liquid CGFL` le réécrasera.** Rejouer alors :
`query "UPDATE metadata SET class='Lung' WHERE sample_id IN (SELECT id FROM samples WHERE
labo='CGFL' AND sample_name IN ('Lung_13','Lung_13bis','Lung_13ter','Lung_13quater'))"`.

## Méthode réutilisable : lire l'HISTORIQUE d'une gsheet

L'API Drive expose les révisions d'un Google Sheet **et les exporte** :

```
GET https://www.googleapis.com/drive/v3/files/{id}/revisions        → 54 révisions (mars→sept)
GET https://docs.google.com/spreadsheets/export?id={id}&revision={rev}&exportFormat=tsv
```

Session authentifiée = `gspread.oauth().http_client.session` (gspread 6.x — **`gc.auth` vaut
`None`**, ne pas chercher là). L'export TSV ne rend que la **première feuille** du classeur
(ici `VAF`, ce qui tombe bien). ⚠ **HTTP 429 systématique** au-delà de ~9 exports d'affilée :
sleep 2,5 s entre requêtes + retry à backoff croissant, et rendre le script idempotent
(skip si le fichier existe déjà).

Diffé révision par révision sur `{Sample name → active_cancer}`, cela donne l'historique complet
de la colonne. Résultat : **une seule vraie correction de statut** en 6 mois —
`Prostate_21` `No → Yes` le 23/07/2026 (R. Boidot). Tout le reste = remplissages de cases vides.

## Le livrable

16 lignes à trancher (dont `Prostate_21` en référence), écrites dans l'onglet **`Active-cancer`**
du Google Doc **QC** (`1X1KxOCR-eHRU04R3eSfyTlxa_C47R114pCw_BkoUHwQ`, tabId `t.hxxxukelxa80`) —
le même doc que l'arbre de décision QC de [[schema-v34-qc-status]]. TSV source :
`/scratch/boris/active-cancer/candidats_active_cancer.tsv`.

Candidats principaux : **`Prostate_25`** (jumeau exact de `Prostate_21`, seul `No` des 46
Prostate), **`Breast_46`** (`Cat 2 Post-op` contredit par « ensemble lésionnel de 75x25x55 mm »),
11 `Suspicion` en `Stage IV` + `Cat 1: **Active**/No panel detection`, **`Pancreas_7`**
(« progression … avérée en 02/25 »). Anomalies hors statut : **`Pancreas_14`** =
« Pancréatite à IgG4 » (pathologie **bénigne** dans une cohorte cancer), **`Colon_34`**
(commentaire « Cancer du sein localisé » sur un Colon). **Aucun des 222 `Yes` n'est contredit.**

## Gotchas d'analyse

- **`Category` porte la définition** : `Cat 2: Post-op no detection` reprend littéralement le
  « no post-op » du header → 35 `No` / **0 `Yes`** ; `Cat 3/4` (VAF tumorale) → 79 `Yes` /
  **0 `No`**. Croiser cette colonne avant toute conclusion.
- **`Progression = YES` ne contredit PAS un `No`** : la progression est postérieure au
  prélèvement (8 cas écartés du livrable pour cette raison).
- **Les commentaires TNM font foi** : `pT3 N1a M0 R0` = post-op sans maladie résiduelle → `No`
  légitime. Le préfixe `p` (pathologique) signale une pièce opératoire, donc du post-op.
- ⚠ **Écrire dans un Google Doc à onglets** : API Docs v1, `includeTabsContent=true` à la
  lecture, et **`tabId` dans chaque `location`/`range`** à l'écriture. Pour remplir un tableau,
  insérer les cellules **par index décroissant** (sinon tout se décale). Les colonnes naissent à
  **175 pt** chacune — soit 1225 pt pour **451 pt utiles** en A4 marges 72/72 : le tableau
  déborde tant qu'on n'a pas passé `updateTableColumnProperties`.
- L'onglet `Count_category` du classeur donne les libellés officiels des 4 catégories ;
  l'onglet `NOTICE – PatientID` ne concerne que le PatientID.

Liens : [[project_columns_index]] (les colonnes metadata), [[feedback_status_columns]]
(pourquoi `active_cancer` n'est pas dans STATUS_COLUMNS), [[cohort-export]] (consommateur des
flags Tower), [[schema-v34-qc-status]] (même Google Doc QC).
