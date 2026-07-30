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

## Pourquoi les évènements avant les chiffres

Arbitrage de Boris, et il tient : les 6 rapports de reconnaissance de la session ont **tous** été
jugés `PARTIELLEMENT_INEXACT` par leur vérificateur adversarial (URL 404 marquée « vérifié »,
effectif d'inclusion pris pour un dénominateur, « early-stage » lu comme « stade I »). Une date
d'approbation FDA ne s'interprète pas ; une sensibilité si. L'extraction des KPI viendra au temps 2,
avec `metric_kind` en enum, `source_quote` obligatoire et `is_complete=false` sans spécificité ni effectif.

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

## Reste à faire — demandé explicitement par Boris le 2026-07-28

**Automatiser de bout en bout, tous les jours** : aller chercher les nouveaux évènements des
concurrents retenus sur les trois indications, alimenter `competitive_events`, et que la mise
à jour se propage seule dans Aima-Tower. Aujourd'hui la collecte est **manuelle**.

Points à trancher avant de câbler le cron :
- **Horaire** : ClinicalTrials.gov reconstruit son snapshot vers 09:00 UTC — un cron à 8h00
  Paris lirait celui de la veille. Placer après 11h Paris, ou assumer J-1.
- **Aucune alerte d'échec de cron n'existe dans tout l'écosystème** : un job mort y est
  invisible. Porter le `RotatingFileHandler` de `check_workflow.py` + une alerte email.
- `run_veille.sh` n'a ni `flock` ni PID file, et le daily 8h00 croise déjà potentiellement le
  weekly du lundi 8h05 → module et cron **séparés** pour la veille concurrentielle.

Voir [[freenome-poumon]], [[competitive_landscape]], [[tower_survey_coupling]].
