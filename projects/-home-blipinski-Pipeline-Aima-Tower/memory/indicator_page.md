---
name: indicator-page
description: "Page /indicator : périmètre production de trace-platform, jointure aux tâches Seqera, flux mesuré et non supposé, et le mécanisme de déclinaison qui a remplacé la version câblée en dur."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-18T14:05:02.333Z
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

## Le seul écart assumé avec trace-platform : `_OVERRIDE_CASE_IGNORE`

Demande Boris en fin de session : **ne pas compter les échantillons de rboidot comme de
la production, dans la Tower seulement**. Constat qui la fonde — ses **deux** comptes
sont déclarés **DEV** dans `labs_users` ; ce sont les `PROD_CUTOFFS` qui forcent à PROD
les échantillons déposés après le 15/06.

```
16342fc9-…  rboidot@cgfl.fr  CGFL  case=DEV   11 forcés PROD + 12 restés DEV
060f70e8-…  rboidot@cgfl.fr  CGFL  case=DEV   16, déjà tous DEV
```

⚠ **L'override est neutralisé, pas remplacé** : `samples.case` est mis à NULL pour ces
comptes, puis la règle normale s'applique et `labs_users.case` décide. Si le TSV les
déclare PROD un jour, leurs échantillons reviennent d'eux-mêmes. Rien n'est modifié en
base — retirer les deux lignes de la constante rend la règle du projet à l'identique.

⚠ L'expression `_CASE_EFF_SQL` est **partagée par les deux requêtes** : un périmètre
différent entre les échantillons et leurs étapes ferait des nœuds de diagramme calculés
sur une autre population que les figures. Deux tests le verrouillent, et j'ai vérifié
qu'ils tombent bien quand on retire la garde (51 au lieu de 40).

Effet au 18/09 : **51 → 40 PROD**. ⚠ Imagenome Labosud pèse alors **32 sur 40**, soit
80 % du périmètre — celui-là même dont la nomenclature (`Sample4_2`…) ressemble à de la
validation, et que Boris a choisi de garder au motif que la base fait foi.

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

## Chronologie des étapes plateforme — corrigée le 2026-09-21 (commit `3d9f9d8`)

Ordre de trace-platform, confirmé sur les données : Session Start → Transfer Start →
Transfer Stop → Session Stop → Copy Start → Copy Stop → Pipeline Start → Pipeline Stop.
La page affiche 5 étapes : **Transfert → Attente copie → Copie → Attente pipeline → Pipeline**
(`PLATFORM_STEPS`). Une attente est un écart calculé, pas un horodatage.

⚠ **En `sample alone`, la copie n'existe pas** : trace-platform écrit `copy_* = transfer_*`
(`check_platform.py:279-283`, « le transfert EST l'écriture dans data/ »). Avant le correctif,
la page comptait le transfert deux fois (Copie = Transfert, 26/26). Désormais `min_copie`
n'est calculée qu'en bulk et `min_attente_copie` vaut NULL d'elle-même (copy_start = transfer_start).
Sample alone = bulk sans la copie : un seul temps mort, fin du transfert → début du pipeline.

⚠ **Bulk ne repose que sur 9 échantillons, une seule session (14/09)** : `bulk/` n'est conservé
sur S3 que depuis cette date (commit trace-platform `43089a3`). Le mode est fiable en PROD :
vérifié sur S3, les 31 sample alone n'ont pas de `bulkSessionId`, les 9 bulk en ont un.
Médianes bulk : transfert 14 min · attente copie 110 min · copie 1 min · attente pipeline 105 min.

- Le Gantt empile les durées : avec les 5 segments le cumul retombe sur les vrais horodatages.
  Son filtre « parcours complet » dépend du mode (copie et attente copie exigées en bulk seulement).
- Diagramme : `COLS = 5`, trait vers le détail du pipeline accroché au dernier nœud (`xDernier`).
- `DUREES` de `Croisements.tsx` est une copie séparée de la liste : à tenir alignée à la main.
- ⚠ Aperçu : le `chrome` complet de ms-playwright **reste bloqué** en `--headless=new` (même avec
  `--timeout`) ; utiliser `chromium_headless_shell-1223/chrome-headless-shell-linux64/chrome-headless-shell`.
- ⚠ `docker compose build` a consommé ~2,7 Go : disque à 99 % → builder AVANT `down`, pour que la
  Tour reste en ligne si le build échoue.

## Diagramme de flux par mode d'upload — 2026-09-21 (commit `1499c05`)

Demande Boris : une rangée plateforme **par mode**, pas une seule rangée mêlée. Bulk =
5 étapes ; sample alone = Transfert → Attente pipeline → Pipeline (« la copie est juste
immédiate », donc ni attente copie ni copie affichées). Chaque étape garde sa colonne de la
chronologie bulk (flèche longue en sample alone) ; les deux rangées partagent la même échelle.
Règle dans `Flux.tsx` : `MODES` + `BULK_SEULEMENT` ; une rangée sans échantillon disparaît.
Durées ≥ 90 min affichées « 1h50 » (`fmtMin`), plus « 1.8 h » — Boris lisait mal l'heure décimale.

## Frise des 8 horodatages + détail bulk — 2026-09-21 (commits `0436f57`, `67f86c4`)

⚠ **Remplace la section « par mode d'upload » ci-dessus** : la plateforme n'est plus en nœuds
d'étape mais en **frise** — un point par horodatage (Session Start … Pipeline Stop), une frise par
mode, l'écart médian entre deux points ; trait plein = étape active, pointillé = temps mort,
espacement régulier. Sample alone saute les 2 points Copy. Écarts calculés en SQL
(`min_session_transfert`, `min_transfert_session`, `min_session_copie`, `min_session_pipeline`).
Bulk : 41 min · 14 min · **1h50 (avant la clôture de session)** · 6.8 min · 1.3 min · 1h45 · 25 min.

⚠ **Les attentes médianes du bulk sont des files d'attente**, pas des temps morts : transferts en
série, session fermée par `system_timeout` 30 min après le dernier transfert (lu dans le
`.dl-complete.txt` de session sur S3 — **pas en base**), pipelines un par un. D'où le menu
déroulant « Pourquoi l'attente est longue en bulk » (`SessionBulk.tsx`) : dernière session bulk,
un échantillon par ligne dans l'ordre d'arrivée, axe en heure réelle (UTC), calcul à l'ouverture.

- ⚠ trace-workflow n'enregistre plus rien depuis le **15/08** (dernière soumission en base) :
  le détail par module du diagramme et `/monitoring` ignorent tout ce qui a tourné depuis.
- Capture d'un état ouvert (menu `<details>`) : protocole DevTools via `websocket-client` installé
  en `--target` dans le scratchpad, `suppress_origin=True` sinon Chrome refuse (403).

## Revue en aperçu commenté + page unique — 2026-09-21 (commit `e97c0b7`, déployé)

Page revue élément par élément dans un artifact commenté (aperçu Vite hors serveur, fetch
intercepté par un instantané pseudonymisé, `frontend/.apercu/`, **jamais commité**). Résultat
décrit dans CLAUDE.md : plus d'onglets ; frise = sections nommées une fois + pointillés
verticaux au milieu des points (pas d'encadré, pas de dégradé — refusés) ; détail bulk en
flèches sur le temps réel ; Gantt avec menus mode / tri / ordre / nombre.

⚠ **Les pastilles de la frise ne s'additionnent pas au « Temps médian »** — question de Boris :
1. une médiane n'est pas additive : chaque échantillon est exact (ses segments somment à son
   total, écart 0), mais le segment lent change d'un échantillon à l'autre. Bulk : 5h04 de
   pastilles contre 4h57 ; sample alone, sur ses 12 chaînes complètes : 59 min contre 1h27.
2. en sample alone, pas les mêmes échantillons derrière chaque chiffre : 13/31 PROD sans
   `session_start` (donc sans total), et des segments NULL par la comparaison stricte `>` :
   `transfer_start` tronqué à la seconde, 57 ms **avant** `session_start` (×3) ;
   `transfer_start = transfer_stop` (×2, l'échantillon à ~99 h en fait partie) ; pas de transfert (×1).
Seule la **moyenne sur un même ensemble** s'additionne (bulk 4h56, sample alone 1h15 sur les
chaînes complètes). **Boris a choisi les moyennes** (2026-09-21) : `mesure()` de `Flux.tsx`
sur les seuls parcours complets du mode ; le bandeau du haut reste en médianes.
