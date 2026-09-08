---
name: analytics-prompt-run-level
description: "Les deux cartes IA comptaient 329 flowcells au lieu de 291 : règle run-level absente des prompts. Et la panne « Import interdit: time », même cause — une règle que le modèle ne pouvait pas deviner."
metadata:
  node_type: memory
  type: project
  modified: 2026-09-08T00:00:00.000Z
---

# `/analytics` — ce que le prompt ne dit pas, le modèle ne peut pas l'inventer (2026-09-08)

Deux pannes de la même famille, corrigées le même jour. **Aucune ligne de service métier
touchée** : les deux vivent dans les system prompts.

## 1. Comptage des runs — 329 au lieu de 291

Référence de vérité : l'export **gsheet « Trace RUN »**
(`1rGasqTmeGXi69k0jbeZibX0F-yrYTXhMp_HfgCXilq8`), 291 runs liquid.

**Trois causes cumulées**, aucune dans les données :

```
  aucun filtre                 329   ← ce que faisait le SQL généré
  hors solid                   294   (−35, hors périmètre liquid : vrai mais hors scope)
  hors rebasecallés            326   (−3  : faux, à retirer)
  hors solid ET rebasecallés   291   = la gsheet
```

⚠ **Prouvé par égalité ensembliste des `run_id`**, pas seulement par le compte : 0 run en base
absent de la gsheet, 0 dans l'autre sens. Un compte identique ne prouve rien tout seul.

⚠ Les rebasecallés ne pèsent que **+3** parce qu'ils **réutilisent le `run_id` de l'original**
(208 samples rebasecallés, 3 `run_id` qui leur sont propres). Ne pas déduire de leur faible
poids qu'ils sont inoffensifs — ils dupliquent des runs déjà comptés.

**Troisième cause, non listée au départ** : `bam_metadata` a **une ligne par sample**, et
`reads_per_flowcell` est **constant à l'intérieur d'un `run_id`** (vérifié : 0 run avec deux
valeurs). Un histogramme sur les lignes compte donc chaque flowcell **4,6 fois en moyenne,
jusqu'à 21** — les gros runs écrasent la distribution.

**La règle vit uniquement dans les prompts.** Grep exhaustif sur `src/`, `backend/`,
`frontend/src/` : **aucune requête en dur** n'agrège `reads_per_flowcell` ni ne compte de
`run_id`. Ces chiffres sortent tous du SQL écrit par le modèle → bloc `<run_level_metrics>`
dans `analytics_assistant.py` + règle équivalente dans `database_qa.py`, et un test
(`TestRunLevelRule`) qui exige les trois termes dans chacun, faute de quoi rien ne protégerait
une correction faite de texte.

ℹ Faux soupçons levés en route : `filters_view.py:24` range `reads_per_flowcell` sous
`qc_metrics`, mais `_ADV_RELOCATE` est un **regroupement d'affichage**, pas un mapping SQL ;
`/reproductibilite` et `/exploration` filtrent déjà `sample_type = 'liquid'` en dur.

## 2. « Import interdit: time » — même schéma

Le Contract du prompt n'énonçait **nulle part** l'allowlist des modules importables. Le modèle
la découvrait dans le message d'erreur de sa **reprise unique** (`_AI_MAX_REPAIRS = 1`), qu'il
gaspillait à corriger un import qu'il ignorait interdit. Intermittent : 4 rejeux du même prompt
passaient sans erreur.

`time` ajouté à l'allowlist — stdlib comme `datetime`/`math`/`re` déjà présents, et le risque
`time.sleep` est **déjà couvert** par le sous-processus tuable à 60 s.
⚠ Il y a maintenant **trois** listes à garder alignées : `requirements.txt` ↔
`_AI_CODE_ALLOWED_TOP_MODULES` ↔ le Contract du prompt. Le test
`test_prompt_declares_the_same_allowlist` parse la ligne du Contract et la compare au set.

## Le piège de méthode : la base bouge sous la mesure

Un `update-column reads_per_flowcell` a tourné **pendant** la session : les valeurs renseignées
sont passées de 1514 à 1310 lignes, et les moyennes que j'avais annoncées (203,29) sont devenues
fausses (149,45) — alors que **les comptages de runs, eux, tenaient**, ne dépendant pas de cette
colonne. ⚠ Toujours mesurer effectifs et valeurs **dans la même copie**, et rapprocher deux
chiffres seulement s'ils viennent du même instantané.

État vérifié en fin de session : 291 runs des deux côtés et **les 291 valeurs
`reads_per_flowcell` identiques à la gsheet** (0 écart, tolérance 0,005 M) ; moyenne 149,45,
médiane 152,50 — moyenne **sous** la médiane, tirée par 10 runs à moins de 20 M.

Voir aussi : [[analytics_ia_hardening]] (même page, la panne E2BIG et le durcissement),
[[reproducibilite_page]] (sémantique des suffixes, dont `_rebasecalled`).
