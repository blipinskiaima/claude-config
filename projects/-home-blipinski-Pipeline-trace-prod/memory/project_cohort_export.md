---
name: cohort-export
description: "export-cohort — audit d'inclusion cohorte Sens/Spé (gsheet 'Trace COHORT' / onglet 'Exis Multi', 1324 lignes liquid × 10 col, 485 inclus). Famille d'exports `exis_*` par indication, distincte de la gsheet trace-prod. Le script importe les prédicats d'Aima-Tower au lieu de les réimplémenter ; motifs évalués indépendamment (≠ cascade) donc le PREMIER motif = palier de chute"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4c0cc1e-b20b-4f48-bb7a-87640e0b5b07
  modified: 2026-08-10T09:07:07.232Z
---

# Export Cohort (juillet 2026)

Commande `export-cohort` : rend traçable, sample par sample, pourquoi on passe des 1324
liquides de trace-prod aux **485** retenus dans le calcul de sensibilité/spécificité de la
Tower (mVAF v1.4 / Exis 1.1). **Aucune table créée** — extraction dérivée, rien de persisté
en DB. Destination depuis août 2026 : onglet `'Exis Multi'` (voir section famille `exis_*`).

**Why:** Boris voulait auditer l'arbre de décision d'inclusion et savoir quelle métadonnée
est responsable de chaque exclusion, avec la valeur de chaque métadonnée déterminante.

## La décision d'architecture qui compte

Trois options se présentaient : réimplémenter l'arbre en SQL dans trace-prod, ajouter une
fonction dans la Tower, ou faire un script trace-prod qui **importe** la Tower. Boris a
tranché pour la 3ᵉ.

Raison : le skill `qara-tower` impose « aucun recalcul maison ». Réimplémenter les ~11
prédicats aurait dupliqué `_prepare_base_dataset`, `_filter_by_version`, `_apply_user_filters`,
`_add_flags`, `_RE_FILTER_CANCER`, `_EXCLUDED_UNIQUE_IDS` — ~200 lignes de règles ISO qui
divergent au premier changement côté Tower. `dev/cohort_extraction.py` les **importe** ;
l'import est lazy dans la commande CLI, donc trace-prod ne casse pas si la Tower est absente.

## Famille d'exports `exis_*` (août 2026, commit 30a810f)

La destination a quitté la gsheet trace-prod pour une gsheet dédiée **« Trace COHORT »**
(`1gSp7d146Qfu2QJcaUc63rZweA4HFnxPY_u7GTUUfvOU`), onglet `'Exis Multi'`. Elle accueillera
**un onglet par indication** (Colon, Poumon, Pancréas) en plus du multicancer.

**Why:** Boris veut séparer les cohortes par indication de la gsheet de suivi trace-prod —
c'est une famille d'exports distincte de toutes les autres (liquid/probs/ONT Sample/Short
Read Like/Dilution/Rarefaction pointent toutes vers `1gm_vB7v…`).

**How to apply:**
- `export_cohort(matrix, key="exis_multi")` — la clé de config est **paramétrée**. Ajouter
  une indication = **1 entrée JSON `exis_<indication>` + 1 argument**, zéro ligne dupliquée
  dans `gsheets.py`. Convention de nommage calée sur le nom d'onglet réel : `exis_multi` →
  `"Exis Multi"`, `exis_colon` → `"Exis Colon"`, etc.
- `export_cohort` était **déjà générique** (reçoit une matrice formatée, ignore le métier) :
  seule la chaîne `"cohort"` était en dur ×3. C'était le seul verrou.
- **Le défaut `worksheet="Cohort"` a été supprimé** : avec une clé paramétrée, un défaut en
  dur devient un piège (`exis_colon` sans `worksheet` aurait écrit silencieusement dans
  `Exis Multi`). La config est validée sur `url` **ET** `worksheet`, erreur explicite sinon.
- **Deux points d'entrée** appellent `export_cohort`, pas un : la CLI `export-cohort` et le
  `main()` du script standalone (`python3 dev/cohort_extraction.py --gsheet`). Toute
  modification de destination doit traiter les deux (+ README + CLAUDE.md).
- L'ancien onglet `'Cohort'` de trace-prod n'est **plus alimenté** — laissé figé, non supprimé.

### Exports par indication (`--indication`, commits 7d929d5 / 200855c)

`export-cohort --indication Colon|Lung|Pancreas` → filtre les lignes et route vers l'onglet
dédié. **Ajouter une indication = 1 ligne dans `EXIS_TABS` + 1 entrée JSON**, rien d'autre.
Sans `--indication` : les 1324 liquides → `Exis Multi`.

`EXIS_TABS = {label CLI: (clé de config, tuple d'indications)}` — un onglet peut couvrir
**plusieurs** indications (la structure est passée de `{label: clé}` à ce tuple au commit
fea394d, quand `Exis Lung` a dû absorber les Alcapone).

| Onglet | Indications retenues | Lignes | Inclus | Colonnes |
|---|---|---|---|---|
| `Exis Multi` | toutes | 1324 | 485 (261 cancers + 224 sains) | 10 |
| `Exis CRC` | `Colon` | 209 | 70 cancers | 20 |
| `Exis Lung` | `Lung` + `Lung_Alc` | 436 | 85 cancers | 20 |
| `Exis Pancreas` | `Pancreas` | 32 | 15 cancers | 20 |
| `Exis Healthy` | `Healthy` | 329 | 224 **sains** | 20 |

- **`Exis Healthy`** = les contrôles négatifs de la cohorte. Vérifié : les 224 sains inclus ont
  **tous** l'indication `Healthy` (aucun sain inclus ailleurs), donc cet onglet + un onglet
  cancer reconstituent une cohorte Sens/Spé. Les 105 exclus le sont surtout par version de
  basecalling (66 en v4.3.0) et par dédup. Metadata sans objet pour des sains : `Metastatic`,
  `PFS`, `Progression`, `Comments`, `Grade`, `Comment (Gene 1)` à **0/329**.

- **`Exis Lung` inclut les 229 Alcapone** (choix Boris) : tous exclus, « cohorte Alcapone » en
  premier motif sur les 229. Le total d'inclus reste donc 85. La distinction est portée par la
  colonne `Indication` déjà exportée — aucune colonne ajoutée.

- **Choix Boris (10/08/2026) : contenu = l'indication SEULE, statut inchangé** — pas de
  recalcul avec `inds_keep={indication}`. Conséquence assumée : **aucun sain dans ces
  onglets → pas de spécificité calculable** depuis ces feuilles. L'alternative (cancers de
  l'indication + les 224 sains = cohorte Sens/Spé) a été écartée explicitement.
- **`META_COLUMNS`** : 10 metadata ONT Sample ajoutées après `Label / Raisons`, **exports par
  indication uniquement** (`Exis Multi` reste à 10 colonnes). **Aucune jointure nécessaire** :
  `_DUCKDB_QUERY` de la Tower charge déjà ces champs. ⚠ `metastatic_raw` / `category_raw` —
  la requête de la Tower renomme `m.metastatic`/`m.category` avec le suffixe `_raw` ; c'est
  bien la valeur DB harmonisée, pas une variante brute. `stage` n'a pas ce suffixe.
- `compute_stats(rows)` factorisé (`build_audit` + filtre CLI). Garde sur indication inconnue
  **avant** `build_audit` → pas de 2 min de calcul pour rien.

**Gotchas découverts en production :**
- ⚠ **Un nom d'onglet avec espace final crée un onglet fantôme.** Boris avait créé `'Exis CRC '`
  (espace final) ; `spreadsheet.worksheet("Exis CRC")` ne l'a pas matché et le fallback
  `add_worksheet` a créé un **second** onglet. Toujours lister `sh.worksheets()` avant
  d'exporter vers un onglet censé exister.
- ⚠ **`get_all_values()` renvoie les valeurs FORMATÉES par la feuille.** Un format de cellule
  « 0,00 » sur la colonne VAF affiche `1,12` pour un `1.124` réel → une comparaison naïve
  entre deux onglets fait croire à une divergence de données. Comparer avec
  `value_render_option="UNFORMATTED_VALUE"` avant de conclure.
- **`Lung` et `Lung_Alc` sont deux indications distinctes** : `Exis Lung` ne contient pas les
  229 Alcapone (tous exclus par « cohorte Alcapone »).
- **Données, pas bugs** : `gene1_mutated` vaut la **chaîne littérale `'None'`** sur 50 Colon
  (VARCHAR en base, saisie gsheet) ; `Grade` (98/1324 liquides) et `Comment (Gene 1)` (6/1324)
  sont **vides sur Colon comme sur Lung**.
- **`Column 43` n'existe nulle part** (ni `TSV_TO_DB_METADATA`, ni onglet ONT Sample où la 43ᵉ
  est `Freq (Gene 3)`, ni les gsheets sources où c'est `Gene 5 mutated`) → non exportée, en
  attente du vrai nom. `Presence of an active cancer (...)` mappe sur `active_cancer` = la
  colonne 8 `Active Cancer` déjà présente → non dupliquée.

**COLUMNS passé de 17 à 10** au même commit : retrait de `Sample`, `Centre`, `Rebasecalled`,
`Muté`, `Cancer actif`, `Cancer truth`, `Healthy` ; `Version Dorado`→`Dorado` ;
`Gene1 VAF`→`VAF`. **La logique d'inclusion est intacte** (485 inclus identiques) : `_add_flags`
n'utilise pas `rebasecalled`, et le dédup lit `prepared`, pas `b` — vérifié avant de trancher.

**Vérifié (10/08/2026)** par **relecture de la gsheet** (pas seulement le message CLI) :
1325 lignes × 10 colonnes uniformes, 485 inclus = 261 cancers + 224 sains, **0 cellule
divergente** sur 13 250 vs le TSV local. Checkpoint `checkpoint-pre-exis-multi` (1a8e05e) +
patch `/scratch/boris/trace-exis/pre-exis-multi.patch`.

## Le piège conceptuel : cascade vs multi-motifs

La Tower filtre en **cascade** (un sample écarté au palier N n'est plus évalué ensuite).
Boris voulait TOUS les motifs d'un sample → les prédicats sont évalués **indépendamment**
sur les 1324.

Conséquence à ne pas oublier : **la somme des motifs ne redonne pas les deltas de la
cascade** (un sample en porte souvent 3 ou 4). C'est le **premier motif** d'une ligne qui
indique son palier de chute — les motifs sont listés dans l'ordre des paliers exprès pour ça.
Vérifié : premier-motif → 242/254/25/30/134/63/91, exactement les deltas du Doc QARA.

Un palier n'est pas évaluable sample par sample : le **dédup `unique_id`** (on est écarté
parce qu'un autre run est préféré) → motif relationnel `doublon de {labo}_{nom}`.

## Preuves de fidélité (à refaire si le code Tower bouge)

- Correspondance **nominative** avec `svc.compute_cohort_samples()` : 485 communs, 0 manquant,
  0 en trop, 0 label divergent. C'est LE test — l'égalité des totaux ne prouve rien.
- Les 7 deltas de la cascade reproduits exactement via le premier motif.
- Audit adversarial (12 agents, 7 lots de prédicats) → **0 divergence confirmée**.
- Contrôle élégant trouvé par l'audit : neutraliser `_EXCLUDED_UNIQUE_IDS` fait passer la
  cohorte de 485 à 486, delta = exactement `['CGFL_26BM01841']`.

## Gotchas

- **1324 ≠ toute la base.** `_DUCKDB_QUERY` de la Tower contient déjà
  `WHERE sample_type='liquid'` : les 147 solides ne sont JAMAIS chargés. Le « 1471 » du Doc
  QARA est un comptage externe, pas une étape de la cascade.
- **`get_indications()` ne retourne pas `Lung_Alc`** (les Alcapone sont filtrés en amont, et
  la fonction passe par `_get_prepared_for_graphics` en version `ge5`). Les 229 Alcapone
  reçoivent donc « indication hors-cible (Lung_Alc) » en plus de « cohorte Alcapone » :
  fidèle à la Tower, mais redondant à la lecture. Laissé tel quel.
- **mVAF ~1e-7 écrasés en `0`** : un `f"{v:.6f}"` naïf détruit 6 valeurs réelles
  (`Lung_89` = 4,9e-8). Même philosophie que `format_mvaf4` — jamais de notation
  scientifique, chiffres significatifs pour les très petites valeurs.
- **`cancer_truth` a un 3ᵉ terme** que `metrics-baseline.md` omet : `mutated OR active_cancer
  OR indication ∈ {TNE, Nuclear, Bladder_*}` (`_add_flags`). Se caler sur le code, pas la doc.
- La `vaf` est propagée par `ffill/bfill` par `unique_id` **avant** le dédup — elle peut donc
  venir d'un autre run du même patient et changer `mutated_flag`.
- `sample_centre` = `{sample_name}_{labo}` : clé unique de la feuille (les homonymes
  inter-labos existent, ex `Colon_1` CGFL exclu v4.3.0 / HCL inclus cancer).

Liens : [[project_schema_v20_mito]] (session précédente), [[feedback_status_columns]].
Doc QARA : Google Doc `1dOYIB-NDehUZYsuJi6hKalyG3YpvseSgNCDUqhdtZvs`.
