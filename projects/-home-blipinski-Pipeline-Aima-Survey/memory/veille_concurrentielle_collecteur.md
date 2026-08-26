---
name: veille-concurrentielle-collecteur
description: "Procédure de veille concurrentielle Aima-Survey → Aima-Tower : décliner à un concurrent = 4 lignes de config, et les pièges d'API à ne pas réapprendre"
metadata: 
  node_type: memory
  type: project
  originSessionId: fdd4f2ac-8635-4303-a86c-70045baa73f3
  modified: 2026-07-28T14:44:41.817Z
---

Livré le 2026-07-28, preuve de concept Freenome, de la collecte à la page Tower.

```
data/competitors.json  ─►  cli.py competitive  ─►  competitive_events  ─►  /api/competitive/events  ─►  page /competitive
   bloc `watch`            4 sources, 0 LLM        table SÉPARÉE            read-only + retry lock         « Signaux »
```

**Décliner à un nouveau concurrent = un bloc `watch`, aucun code :**

```json
"watch": { "clinicaltrials_sponsor": "...", "sec_cik": "...",
           "newsroom_sitemap": "https://www...", "fda_applicant": "..." }
```

Une source sans identifiant est ignorée pour ce concurrent ; une source qui échoue n'interrompt
pas les autres. `upsert_event()` renvoie `new` / `changed` / `unchanged` — le `content_hash`
détecte la **modification silencieuse**, pas seulement l'apparition.

⚠ **`competitive-probe` propose, il ne valide pas — regarder ce que le sitemap contient avant
de le coller.** Mesuré sur Biodesix le 2026-08-26 : la commande retenait
`biodesix.com/sitemap.xml`, qui n'est pas un fil de communiqués mais le **plan de navigation**
du site — 30 pages `/careers`, `/privacy-policy-hipaa`, `/terms-conditions`, toutes au même
`lastmod`. Le coller aurait ingéré « Terms & Conditions » comme évènement de veille, exactement
le mode de panne Singlera. Le vrai canal était `/newsroom/press-releases`, une page d'index vers
GlobeNewswire, donc la clé **`newsroom_page`** (`PressLinksSource`) et non `newsroom_sitemap`.
Le contrôle qui tranche, à faire à blanc avant d'écrire dans `competitors.json` :

```python
from lib.competitive.press_links import _RE_FILS, _canoniser, _est_un_article
# ou NewsroomSource().collect(url, since=date(...)) pour un sitemap
```

Un sitemap dont les entrées sont des **pages de site** ou des **titres d'articles scientifiques**
n'est pas un fil de communiqués.

## Pourquoi les évènements avant les chiffres

Arbitrage de Boris, et il tient : les 6 rapports de reconnaissance de la session ont **tous** été
jugés `PARTIELLEMENT_INEXACT` par leur vérificateur adversarial (URL 404 marquée « vérifié »,
effectif d'inclusion pris pour un dénominateur, « early-stage » lu comme « stade I »). Une date
d'approbation FDA ne s'interprète pas ; une sensibilité si. L'extraction des KPI viendra au temps 2,
avec `metric_kind` en enum, `source_quote` obligatoire et `is_complete=false` sans spécificité ni effectif.

## Le garde-fou `_source_credible` se juge VALEUR PAR VALEUR (corrigé le 2026-08-26)

Une clé `watch` accepte une liste. La règle anti-domaine-détourné — dès 3 évènements, au moins
un titre doit nommer la société — s'appliquait à la liste **fusionnée** de toutes les valeurs.
Conséquence mesurée sur ClearNote Health, domaine parfaitement vivant :

```
post-sitemap.xml         78 évènements · 26 nomment « ClearNote »   sain
publication-sitemap.xml  21 évènements ·  0 nomme  « ClearNote »    titres d'articles
                         ────────────────────────────────────────
sur 7 jours, seul le second a du récent → la fusion ne contient que ses 5 titres académiques
                                        → 0 hit → TOUT le bloc newsroom rejeté,
                                          y compris le sitemap sain
```

Le message « domaine probablement abandonné ou détourné… RIEN N'A ÉTÉ ÉCRIT » était donc un
**faux positif**, et il accusait le mauvais flux. `run_collect` juge maintenant chaque valeur
séparément — ce qui rend aussi le garde-fou **plus** protecteur : un domaine réellement détourné
parmi trois sitemaps sains se cachait jusque-là derrière ses voisins. Deux dédoublonnages : par
valeur avant le test, puis inter-valeurs après.

⚠ **Ne pas court-circuiter sur une liste d'évènements vide** : la ligne `✓ source : 0
évènements` est ce qui distingue une source **qui a tourné sans rien trouver** d'une source
absente ou en échec. Je l'ai supprimée par inadvertance en corrigeant, puis remise.

⚠ Un **flux de publications scientifiques** échouera toujours cette règle : les titres d'articles
ne nomment jamais la société qui les cosigne. Ce n'est pas un cas à contourner — c'est le canal
PubMed (`queries.json`, `[Affiliation]`) qui doit le porter, et il le fait mieux : il apporte le
résumé, le score IA et la classification. C'est pourquoi le `publication-sitemap` de ClearNote a
été retiré de son `watch` plutôt que « réparé ».

## Pièges d'API mesurés — ne pas les réapprendre

- **SEC EDGAR est la source la plus rapide** : le 8-K du 2026-07-27 portait l'approbation FDA le
  jour même. openFDA ne l'avait toujours pas (dernier enregistrement 2026-07-17). SEC alerte,
  openFDA confirme.
- **openFDA renvoie HTTP 404 pour « zéro résultat »**, pas pour une erreur. Un `raise_for_status()`
  naïf fait tomber le cron tous les jours calmes.
- **SEC exige un `User-Agent` nominatif** (403 sinon). CIK zero-paddé sur `/submissions/`, **non
  paddé** sur `/Archives/` (301 sinon).
- **Le `lastmod` d'un sitemap est une date de RÉÉDITION.** Sur 18 communiqués Freenome, 8
  divergent de `datePublished`, jusqu'à 133 jours. Lire le JSON-LD de chaque page.
- **ClinicalTrials.gov émet `nextPageToken` dès que la page est pleine**, même s'il ne reste rien.
- **CT.gov reconstruit son snapshot vers 09:00 UTC** → un cron à 8h00 Paris lit celui de la veille.
- Interdits par ToS : LinkedIn (contractuel), Crunchbase, Google Patents `/xhr/`. Aucune voie
  brevets à la fois licite et non authentifiée sans clé USPTO ODP.

## Contraintes structurelles à respecter

- **Table séparée d'`articles`, non négociable** : Aima-Tower lit `articles` sans filtre de source,
  `scorer.py` y applique un prompt de pertinence *publication*, `classifier.py` y cherche une
  affiliation. Ajouter une table est sans risque ; **renommer une des 17 colonnes qu'il lit
  positionnellement provoque un HTTP 500 non rattrapé.**
- Côté Tower, `include_router` doit rester **avant** le catch-all SPA de `main.py` (sinon 404 muet),
  et `docker compose restart` ne déploie rien — le code est `COPY` dans l'image.
- `AgGrid.tsx` existe mais **n'a jamais tourné** (0 import, conflit thème v35 / CSS legacy).

## Indications suivies

`indication` ∈ `lung` | `crc` | `pancreas` | `autre`, un onglet Tower chacun. Priorité en cas
de double mention : **poumon > CRC > pancréas** (le poumon est l'axe principal).
⚠ Le sigle « crc » n'est pas cherché en sous-chaîne — il matcherait n'importe quel identifiant.
`cli.py competitive-reclassify` recalcule tout sans une seule requête HTTP.

**Invariant à ne pas casser** : le `content_hash` tranche *une seule* question — la source
a-t-elle bougé ? `title`, `summary`, `evidence_url` et `indication` sont **notre rendu**, donc
resynchronisés à chaque passage sur la branche `unchanged`, sans toucher `last_changed_at`.
Sans ça, changer le code de rendu laisse l'ancien texte figé en base indéfiniment — c'est ce
qui a rétrogradé les 15 PMA Shield de `crc` à `autre` le 2026-07-28.
Corollaire : **tout champ dont dépend la classification doit être persisté**, pas seulement
consommé au vol (cas de `generic_name` côté openFDA).

## L'automatisation demandée le 2026-07-28 est en place (constaté le 2026-08-26)

⚠ Cette section disait « aujourd'hui la collecte est **manuelle** ». C'est **faux** depuis que
les crons sont câblés — corrigé plutôt que laissé, une mémoire périmée coûte plus qu'une absente.

```
0 8  * * *   run_competitive.sh --days 7 --email     collecte quotidienne → competitive_events
0 10 * * 1   run_profils.sh                          lundi : P0 + P3 + PDF des 8 dossiers
0 8  * * *   run_veille.sh --days 7 --report --email veille bibliographique PubMed
5 8  * * 1   run_veille.sh --days 7 --report --email résumé hebdomadaire
```

Les trois scripts partagent le **même `flock`** sur `data/.aima-survey-db.lock` : même base
DuckDB, écritures sérialisées, plus de « Could not set lock on file » silencieux. Le point
`RotatingFileHandler` est réglé (`data/competitive.log`, 10 Mo × 5). Reste ouvert : **aucune
alerte d'échec de cron** dans l'écosystème — un job mort y est toujours invisible.

⚠ Le point horaire n'a **pas** été tranché : le cron tourne à 8h00 Paris alors que
ClinicalTrials.gov reconstruit son snapshot vers 09:00 UTC. On lit donc J-1 sur cette source,
et c'est assumé par défaut plus que par décision.

Voir [[freenome-poumon]], [[competitive_landscape]], [[tower_survey_coupling]],
[[dossiers_concurrent_p1p2p3]], [[biodesix]].
