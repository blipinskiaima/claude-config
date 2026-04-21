---
name: Aima-Survey v6.1 — classification sector/org + abonnement Pro
description: Refonte 2026-04-21 : ajout traçabilité origine institutionnelle (privé/public + nom labo/boîte) pour chaque article + migration complète du scoring et de la classification sur l'abonnement Claude Pro/Max
type: project
originSessionId: 2436002f-1dc1-46c9-9d7b-0cb1a41488d6
---
## Déclencheur

Boris voulait pouvoir distinguer dans Aima-Tower les articles provenant de labos publics vs entreprises privées, avec le nom de l'organisation, pour analyser rapidement qui travaille sur tel sujet de veille. En cours de route : crédit API Anthropic épuisé → décision de basculer sur l'abonnement Pro/Max (pattern déjà utilisé dans Aima-Tower).

## Ce qui a été ajouté en DB (`data/aima_survey.duckdb`)

8 nouvelles colonnes sur `articles`, toutes via `ALTER TABLE ADD COLUMN IF NOT EXISTS` (idempotent) :

- **Parsing PubMed** : `affiliations` (TEXT concat ` | `), `last_author_affiliation` (signal principal)
- **Classification Haiku** : `sector`, `org_type`, `org_name`, `classification_why`, `classification_model`, `classified_at`

## Taxonomie (enums fixes)

- `sector` ∈ `{public, private, mixed, unknown}`
- `org_type` ∈ `{academic, hospital, company, startup, consortium, government, unknown}`
- `org_name` : texte libre (ex: "Broad Institute", "Guardant Health")

**Why :** public/private/mixed permet un filtrage macro ; org_type permet de distinguer labo académique vs hôpital vs biotech ; org_name donne la granularité maximale pour recherche textuelle.

**How to apply :** Ne pas modifier ces enums sans adapter le prompt de `lib/classifier.py` + les labels FR dans `Aima-Tower/src/survey_render.py::_ORG_TYPE_LABELS_FR`.

## Optimisation coût : short-circuit 0 token

`lib/classifier.py::classify_one` ne fait **PAS** d'appel Haiku si `last_author_affiliation` ET `affiliations` sont tous deux NULL → retourne directement `sector=unknown`. Sur 338 articles, 247 short-circuits + 91 vrais appels Haiku = ~0.05 € total.

## Intégration Aima-Tower (UI /survey)

- Dropdown `survey-filter-sector` multi-select avec 2 sections séparées (──Secteur── + ──Organisations──), options dynamiques via `SurveyService.list_sectors_and_orgs()`
- Valeurs préfixées : `sector:public` / `org:Broad Institute` pour dispatch dans `filter_articles`
- Badge dans chaque card avec couleur selon sector (vert=public, orange=privé, bleu=mixte, gris=unknown) + label FR org_type + org_name
- Barre de recherche texte étendue à `org_name` (taper "Guardant" trouve les articles de Guardant)

## Why (motivation stratégique)

**Why :** traçabilité industrie/académie critique pour Boris — permet de repérer rapidement les annonces produit biotech (GRAIL, Guardant, Volition) vs avancées académiques fondamentales. Contexte AIMA : compétition directe avec GRAIL/Guardant sur la détection précoce par méthylation cfDNA.

**How to apply :** Si un futur projet AIMA veut classifier l'origine des publications/brevets/etc., cette taxonomie + le pattern classifier Haiku + short-circuit sont réutilisables tels quels.
