# Phase 6 — Intégration à la veille

Inscrire le concurrent dans le dispositif permanent. C'est ici que se joue la différence entre
« on a écrit un dossier » et « on le surveille ».

⚠ **Deux fichiers, pas un.** La veille tourne sur deux chaînes indépendantes, sans aucun lien de
code entre elles. Ne remplir que la première est l'erreur par défaut : le concurrent apparaît
dans l'onglet, ses communiqués remontent, et ses **publications scientifiques ne remontent
jamais**.

```
data/competitors.json ──▶ run_competitive.sh   08h00 quotidien ──▶ competitive_events
   bloc `watch`            run_profils.sh      lundi 10h00     ──▶ P0 + P3 + PDF
                                                               ──▶ onglet Deep dive concurrent

queries.json ──▶ run_veille.sh   08h00 quotidien + 08h05 lundi ──▶ table articles
   competitive_affiliations                                    ──▶ onglet Concurrence de /survey
```

État constaté le 26/08/2026 : `competitors.json` déclare 22 sociétés en `include_in_query_b:
true`, `queries.json` n'en interroge que 19 — ClearNote Health, Geneseeq et IMBdx sont déclarés
et jamais cherchés dans PubMed. La désynchronisation est le mode de panne normal de cette phase.

---

## 1. `data/competitors.json` — l'entrée et le bloc `watch`

⛔ **Ne jamais écrire sans validation de Boris.** Afficher le diff proposé et attendre.

**a) L'entrée.** Si la société est absente, proposer une entrée complète avec son tier
(1 = concurrent direct, 2 = adjacent, 3 = émergent). Champs : `name`, `aliases`, `hq`,
`founded`, `tech`, `product`, `stage`, `cancers`, `threat`, `threat_reason`, `url`,
`include_in_query_b`.

- `name` doit être **exactement** le nom dont dérive le SLUG (phase 0) — c'est la clé de la
  colonne `competitor` de `competitive_events` et le nom de fichier des profils.
- `aliases` alimente `scripts/reclassify_competitors.py` **et** doit être reporté à la main dans
  `queries.json` (§2). Un alias oublié = des publications non attribuées.
- `stage` : distinguer une désignation d'une approbation, comme dans le corps du rapport.

**b) Le bloc `watch`** — c'est lui, et lui seul, qui déclenche la collecte. Sans `watch` :
aucun `competitive_events`, donc P0 et P3 vides, donc pas de dossier vivant. Le découvrir :

```bash
cd ~/Pipeline/Aima-Survey && python3 cli.py competitive-probe "{NOM}" --domain {domaine}.com
```

La commande n'écrit rien : elle imprime un bloc JSON à coller. Clés reconnues :
`clinicaltrials_sponsor`, `sec_cik`, `newsroom_sitemap`, `newsroom_page`, `presslinks`,
`fda_applicant`. Chacune accepte une **chaîne ou une liste**.

⚠ **Vérifier ce que contient chaque sitemap avant de le coller.** Le collecteur applique aux
sources propriétaires (`newsroom`, `presslinks`) une règle de crédibilité
(`lib/competitive/collector.py::_source_credible`) : dès 3 évènements, si aucun titre ne
contient le premier mot du nom de la société, **toute la source est rejetée sans rien écrire**.
La règle vise les domaines abandonnés puis rachetés (cas Singlera, juillet 2026). Elle se
retourne contre un `publication-sitemap.xml`, dont les titres sont académiques et ne nomment
jamais la société — et comme les valeurs d'une même clé sont fusionnées avant le test, un
sitemap de publications suffit à faire tomber le sitemap de communiqués qui l'accompagne.
Un sitemap de publications se surveille par PubMed (§2), pas par la newsroom.

**c) Après validation** : rejouer `python3 cli.py competitive-reclassify` pour que les articles
déjà en base soient réattribués au nouveau concurrent et à ses alias.

## 2. `queries.json` — la veille bibliographique PubMed

Ajouter `"{NOM}"[Affiliation]` (et les alias qui correspondent à une affiliation réelle) dans la
requête `competitive_affiliations`. **Aucune synchronisation automatique n'existe** : c'est une
chaîne écrite à la main, chargée par `lib/fetcher.py`.

Le mapping y est le nom tel qu'il apparaît dans le champ Affiliation des papiers, qui n'est pas
toujours le `name` de `competitors.json` — vérifier sur un papier connu de la société avant
d'écrire.

⚠ `queries.json` est relu **au démarrage** de la veille et le mapping `queries_matched` →
rubriques est chargé au module load côté Aima-Tower : après édition, `docker compose restart`
sur Tower pour que les nouvelles rubriques apparaissent.

## 3. `concurency/COMPETITORS.md` — le tableau de doc

Ajouter la ligne. Le fichier annonce `data/competitors.json` comme source structurée mais
**aucun script ne les synchronise** : la doc dérive silencieusement si on l'oublie.

Au passage, deux pointeurs morts connus dans le bloc `_meta` de `competitors.json` : il annonce
être lu par `lib/fetcher.py` (faux — `fetcher.py` ne lit que `queries.json`) et renvoie à
`docs/COMPETITORS.md` (le fichier est en `concurency/COMPETITORS.md`). Ne pas s'y fier.

## 4. Vérifier que le dossier se constitue

P0, P3 et le PDF arrivent seuls au cron du lundi 10h00. Pour ne pas attendre une semaine avant
de savoir si le `watch` fonctionne, forcer une collecte et une génération :

```bash
cd ~/Pipeline/Aima-Survey
./run_competitive.sh --days 30            # collecte (respecte le flock partagé)
python3 cli.py competitive-profil --competitor "{NOM}"   # écrit P0 et P3
```

Puis contrôler que les quatre volets sont bien là et que le slug est le bon :

```bash
ls concurency/profils/{SLUG}-P*.md
curl -s localhost:8050/api/competitive/profils | python3 -m json.tool | grep -A2 '{SLUG}'
```

Le PDF, lui, n'est pas produit à la demande — `weasyprint` vit dans `.venv-pdf` côté Aima-Survey
et `run_profils.sh` l'appelle. Pour le forcer, lancer `./run_profils.sh`. Contrôler ensuite par
extraction, la relecture visuelle étant impossible sans `poppler-utils` :

```python
from pypdf import PdfReader
r = PdfReader(PDF); full = "\n".join(p.extract_text() or "" for p in r.pages)
# sections presentes ? glyphes speciaux rendus ? liens cliquables ?
for a in (page.get("/Annots") or []): print((a.get_object().get("/A") or {}).get("/URI"))
```

⚠ La police DejaVu ne contient pas tous les emojis. ⭐ disparaît silencieusement — utiliser ★
(U+2605), ⚠ et → passent correctement.

`*.pdf` est gitignoré dans Aima-Survey : le PDF est regénérable, ne pas le versionner.

## 5. Écrire la mémoire

Un topic file dans
`~/.claude/projects/-home-blipinski-Pipeline-Aima-Survey/memory/{societe}.md`, type `reference`.

Y mettre **ce qui ne se redéduit pas** du rapport : les vrais chiffres avec leur piège, ce qui
est vérifié ou non, et l'implication pour AIMA. Lier avec `[[competitive_landscape]]` et
`[[aima_positioning]]`.

Ajouter la ligne correspondante dans `MEMORY.md`.

## 6. Mettre à jour la fiche AIMA si nécessaire

Si l'analyse révèle un manque dans `concurency/AIMA-POSITIONING.md` (champ `[À PRÉCISER]` qu'on
peut désormais remplir, ou barre de performance de marché à inscrire), le proposer à Boris.

## 7. Référencer dans la documentation projet

Ajouter les deux rapports dans la section « Veille concurrentielle » du `CLAUDE.md`
d'Aima-Survey et dans l'arborescence du `README.md`.

## Sortie de phase

- Entrée + bloc `watch` proposés pour `competitors.json` (non appliqués sans accord)
- Ligne ajoutée à `queries.json` — **la moitié qu'on oublie**
- `COMPETITORS.md` à jour
- Collecte forcée, quatre volets présents, dossier visible dans l'onglet
- Mémoire écrite, documentation projet à jour
