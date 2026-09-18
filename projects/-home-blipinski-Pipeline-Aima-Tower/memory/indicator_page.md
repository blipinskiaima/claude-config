---
name: indicator-page
description: "Page /indicator : périmètre production de trace-platform, jointure aux tâches Seqera, flux mesuré et non supposé, et le mécanisme de déclinaison qui a remplacé la version câblée en dur."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-18T13:45:48.456Z
  originSessionId: b486e4ec-8e81-4f3a-ab7e-dd938e21bf46
---

# Page `/indicator` — performance du pipeline en production (2026-09-18, v5.8.0)

Deux parties : les indicateurs (10 figures) et le diagramme de flux. Première page du
projet à **joindre deux bases**.

## Le périmètre production — deux erreurs de lecture avant la bonne

La règle est celle de trace-platform (`lib/platform_db.py:810`) :

```
case_eff = COALESCE(samples.case, labs_users.case, 'PROD')
                                  └─ jointure sur user_id, PAS lab_id
                                                          └─ ⚠ le défaut est PROD
```

⚠ **Le défaut est PROD** : un `client_uuid` détecté sur S3 mais absent du TSV `labs_users`
compte comme production. L'absence de flag DEV ne veut pas dire « test ».

Deux erreurs commises en route, toutes deux silencieuses :
1. Joint sur `labs_users.lab_id` → **0 correspondance**, d'où un faux « 11 échantillons
   PROD ». La bonne clé est `user_id`. Résultat réel : **51 PROD / 322 DEV**.
2. `COUNT(*)` après LEFT JOIN compté pour des échantillons → « 87 PROD » sur 51.

ℹ `PROD_CUTOFFS` (`check_platform.py:683`) ne couvre qu'un client (CGFL, prod depuis le
2026-06-15) : c'est lui qui pose les 11 `samples.case = 'PROD'` au niveau échantillon.

⚠ Les 32 échantillons d'Imagenome Labosud (63 % du périmètre) se nomment `Sample4_2`,
`Sample5`… — nomenclature de validation, mais le compte est déclaré PROD. **Décision
Boris : la base fait foi**, la Tower ne réinterprète pas la qualification.

## Deux bases, sans quoi le pipeline reste une boîte noire

trace-platform ne stocke qu'un `start` et un `done` pour le pipeline. Le détail par module
est dans `trace_workflow.seqera_tasks` (286 934 tâches, `process` / `realtime` /
`start_time`). Le JOIN existait déjà dans `PlatformService.get_samples_overview()` :
`split_part(input_path,'/',5)` = client_uuid, `,7)` = patient_name, `,8)` = sample_name.

⚠ **La clé de jointure a trois champs** : `(client_uuid, patient_name, sample_name)`.
`sample_name` seul n'est pas unique (260 noms pour 373 lignes) et joindre dessus fabrique
des lignes — c'est le piège déjà documenté dans [[qara_comparaison_dynamique]], où j'étais
déjà tombé. `labs_users.user_id` ne l'est pas non plus (la chaîne vide 5 fois), d'où le
`GROUP BY` que fait aussi `PlatformService`.

## Plusieurs workflows par échantillon — et ce ne sont pas des relances

Sur 36 échantillons PROD ayant un workflow, 13 en ont plusieurs réussis. En les examinant :

```
10 × Patient-1..10   run complet 20-21/07  puis  THEMELIO seul le 10/08 (passe groupée)
 2 × Bladder_Urine   Merge seul 13:48      puis  run complet 19:00, même jour
 1 × Ma_SAB_Run_1    run sans Beta_28M     puis  run complet 4 h après
 1 × Patient-8       deux runs complets à 33 min   ← seul vrai doublon, 1 sur 36
```

Ils se **complètent** au lieu de se répéter. Garder le workflow le plus récent coupait le
parcours en deux et vidait Merge/Beta_epic/CNV/Frag/IV de 9 échantillons. La page retient
donc **la dernière exécution réussie de chaque module** : les n par nœud passent de 21 à 32.

## Le flux est mesuré, pas supposé

Sur les 117 workflows complets :

```
Merge          rang 1 sans exception (min=max=1)
5 branches     rangs 2-6, chevauchement 67-100 % deux à deux  → parallèles
themelio, too, rapport   rangs 5-8, toujours en fin
```

⚠ **Les temps ne s'additionnent donc pas** : CPU cumulé médian 16,4 min contre 7,5 min
d'horloge. Le diagramme n'affiche **aucun total**, et les barres se comparent à l'intérieur
d'une rangée seulement. Bascule horloge / CPU cumulé : leur rapport est le parallélisme.

ℹ Normalisation des modules (table explicite, pas de règle) : `Beta` → `Beta_epic` (mêmes
sous-process, ancien nom) ; `THEMELIO_build_input` / `THEMELIO_score` → `themelio`
(process de premier niveau avant que le module existe).

## Le contre-intuitif à retenir

**Les étapes lourdes ne suivent pas le volume, les étapes qui le suivent sont légères.**

```
attente   29,6 min  r=0,35     ← premier poste de la chaîne, indépendant des reads
transfert 17,4      r=0,48
Beta_epic  4,7      r=0,37     ← le module le plus lourd, le moins prévisible
CNV        4,1      r=0,98     ← presque parfaitement prédit, mais léger
```

Doubler les reads ne doublera pas le délai de rendu : c'est l'ordonnancement qui le fixe.

## Déclinaison : un mécanisme, pas une dimension câblée

Première version : « version du pipeline » codée en dur dans cinq figures. Retour Boris —
*« l'information de déclinaison par version noie l'information principale »*. Remplacé par :

```
grouper(rows, dim)
  dim = null  → [{cle: "Ensemble", rows}]   ← défaut : aucune déclinaison
  dim = "..."  → un groupe par valeur
```

Un seul chemin de code dans les figures, qu'il y ait un groupe ou douze. Six axes
(version, laboratoire, produit, statut, dorado, mode d'upload) ; en ajouter un = une ligne.

⚠ « Comparaison » et « Couverture des métriques » **n'apparaissent qu'avec un axe actif** :
elles n'existent que pour comparer des groupes.
⚠ L'écart du tableau compare **à l'ensemble du périmètre**, pas au groupe précédent — un
« précédent » n'a de sens que sur un axe chronologique, et l'axe est au choix.
⚠ Un écart sur moins de 5 échantillons est affiché **en italique avec ⚠** : sans cela
« ↑ 546 % » sur 2 points était la première chose que l'œil accrochait.

## Le détecteur a trouvé quelque chose de réel

La grille de couverture, sans qu'on cherche :

```
score_cnv renseigné   V1.0.0→V2.0.0 100 %   V2.0.2 55 %   V2.3.0 0 %
```

Le pipeline a cessé d'écrire cette métrique à partir de Bam2Beta V2.3.0.

Et la déclinaison par laboratoire montre ce que la version masquait : GenDx à 1,93 min/M
contre 1,07 pour Imagenome (n=5, à instruire, pas à conclure).

## Trouvé en chemin : `/database-platform` était morte

`PlatformService.get_samples_overview()` interrogeait `upload_date`, supprimée par la
migration v15 de trace-platform le 2026-09-17. Le service **avalait** le `Binder Error` et
renvoyait `[]` → tableau vide, sans message. Corrigé dans une session séparée (`081a03f`).
C'est ce qui a motivé le choix de **laisser remonter l'erreur** dans le router Indicator.

## Pièges techniques

- ⚠ Plotly coupe les lignes sur `<br>`, **pas** `\n` — avec `\n` le texte des cellules de
  heatmap se rend sur une ligne et déborde.
- ⚠ Les typings `plotly.js` déclarent `text` en `string[]` ; une heatmap accepte une
  matrice → double cast `as unknown as Data`.
- ⚠ `pkill -f "<motif>"` tue le shell qui contient le motif — piège déjà noté dans
  [[charte_site_tokens]], refait quand même. Tuer par PID.
- ⚠ `hostname -I` renvoie l'**IP publique** du serveur : binder un serveur d'aperçu sur
  `0.0.0.0` exposerait la Tower sans authentification. Rester sur `127.0.0.1`.
- Aperçu sans rebuild Docker : Chromium de `~/.cache/ms-playwright/` en `--headless=new
  --screenshot`, sur un petit serveur Python qui sert `frontend/dist` et proxifie `/api`
  vers l'IP du container. ~1 min par itération contre ~3 pour un rebuild.

Voir aussi : [[qara_comparaison_dynamique]] (clé `unique_id`), [[duckdb-patterns]]
(ATTACH in-memory), [[migration_v34_colonnes_reads]] (renommages silencieux).
