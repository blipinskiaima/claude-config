---
name: Survey page patterns
description: Patterns architecturaux cles de la page /survey — parser extensible, lazy tabs, state persistant, scoring IA
type: project
originSessionId: 6f5f6d25-70e3-4fb2-8fa2-e5e167e33164
---
# Page Survey — patterns reutilisables

## 1. Parser markdown extensible

`survey_service.py::_parse_article_block` :
- Boucle sur les lignes d'un bloc article (H3 + bullets)
- Extrait les spans HTML (priority, date, score) via regex dediees
- Branche `if label.startswith(...)` sur la boucle `BULLET_RE` pour chaque `**Label** : value`
- **Pattern pour ajouter un champ** : 1) regex pour span si applicable, 2) branche `elif` dans la boucle bullets, 3) nouveau champ `Optional[...]` sur dataclass `Article` (default = None/"")
- Retrocompat garantie par les defauts : les rapports anciens n'ont pas le champ, parsing renvoie `None` / `""`

## 2. Tri multi-criteres avec None en fin

`SurveyService.sort_for_display` :
```python
sorted(articles, key=lambda a: (
    prio_rank.get(a.priority, 3),
    a.score is None,              # True trie apres False
    -(a.score if a.score is not None else 0),
    tuple(-int(p) for p in a.date.split("-")) if a.date else (0, 0, 0),
))
```
Idiome cle : `a.score is None` comme 2e composante trie les None-scores en fin de bloc priorite, tout en gardant le tri par score desc parmi les scorés.

## 3. Lazy-render des onglets (payload -91% Day / -62% Week)

Probleme : `dbc.Tabs` envoie tous les enfants au browser, meme non-actifs → payload massif avec 40+ cards × multiples onglets.

Solution :
- `render_survey_content` construit `dbc.Tabs` avec LABELS seulement (pas de content dans chaque Tab)
- Contenu de l'onglet actif dans un Div separe `survey-active-tab-content`
- Callback `switch_survey_tab` avec `Input("survey-tabs", "active_tab")` → rend le contenu a la demande
- `prevent_initial_call=True` evite le double-render au mode change

## 4. Patterns pour UI reactivite

- **Filtres persistents** : `persistence=True, persistence_type="session"` sur tous les inputs → etat preserve au re-render
- **Clientside callback** pour toggle visibilite containers (instant, sans roundtrip serveur) → cf. date/date-range containers
- **Remplacer `dbc.Collapse` par `html.Div` + toggle `style.display`** : plus leger cote React (pas de state/transitions internes), ~30% mount/unmount plus rapide
- **Pattern-matching dict ids** avec `slot` en plus de `pmid` : necessaire quand un meme article apparait dans plusieurs onglets (sinon conflit d'ids)

## 5. State persistant atomique

Pattern `survey_state.py` / `survey_bookmarks.py` :
```python
def _write(data):
    tmp = STATE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, STATE_FILE)  # atomic rename
```
Evite les corruptions sous acces concurrent Flask multi-thread.

**Volume Docker critique** : `./data:/app/data` dans `docker-compose.yml` — sinon les JSON persistants sont perdus au `docker compose down`. Ce volume sert aussi a `qualite_snapshots.py` (ISO 15189).

## 6. Scoring IA decouple

Scoring produit par un projet EXTERNE (`Aima-Survey/scorer.py` via Claude Haiku 4.5), ecrit dans le markdown comme source de verite. Aima-Tower ne fait que consommer — pas d'appel API pour le scoring, pas de dependance au cache SQLite du projet amont.

**Avantage** : separation des responsabilites, cache cote producteur, Aima-Tower reste un simple lecteur.
