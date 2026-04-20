---
name: Architecture multi-sources
description: Extensibilité lib/sources/, convention search/fetch, ajout d'une nouvelle source sans refactor
type: project
originSessionId: 39895026-ccd6-4902-95d9-095b93ed61ed
---
## Pattern de la refonte v6

Aima-Survey peut consommer plusieurs sources d'articles scientifiques. La PK composite `(source, external_id)` de la table `articles` autorise plusieurs sources dans une même DB sans conflit.

### Convention d'une source

Pas d'abstract class, pas de Protocol (Karpathy). Une convention suffit. Chaque source expose :

```python
class MySource:
    name = "mysource"     # doit matcher l'entrée du registre

    def search(self, query: str, *, days=None, since=None, until=None,
               max_results=50) -> list[str]:
        """Retourne une liste d'external_id correspondant à la requête."""

    def fetch(self, external_ids: list[str]) -> list[dict]:
        """Retourne une liste de dicts avec au minimum :
        external_id, title, abstract, authors, journal, pub_date, doi, url.
        """
```

### Registre

`lib/sources/__init__.py` :

```python
def build_sources(api_keys=None):
    keys = api_keys or {}
    return {
        "pubmed": PubMedSource(api_key=keys.get("pubmed") or os.environ.get("NCBI_API_KEY")),
        # demain : "biorxiv": BioRxivSource(), "medrxiv": MedRxivSource(), …
    }
```

### Ajouter une nouvelle source — 3 étapes

1. **Créer `lib/sources/<name>.py`** avec la classe respectant la convention.
2. **L'ajouter à `build_sources`** dans `lib/sources/__init__.py`.
3. **Taguer les requêtes dans `queries.json`** avec `"source": "<name>"`.

Aucun autre code à modifier. La CLI `fetch` itère automatiquement les sources en fonction du champ `source` des requêtes. La DB accueille les nouveaux articles via la même `upsert_article`.

**Why :** éviter un refactor à chaque nouvelle source. Boris a anticipé ça dès la V6 pour que l'ajout de bioRxiv/medRxiv/EuropePMC coûte ~80 lignes, pas une journée.

### Dédup cross-source

- PK `(source, external_id)` → le même article en preprint et publié coexiste naturellement (2 lignes distinctes).
- Index sur `doi` → dédup opportuniste à faire à la demande via SQL (à voir plus tard si besoin : merger `biorxiv:10.1101/...` et `pubmed:XXXX` qui pointent vers le même DOI).

**How to apply :** si un jour on veut merger, écrire une commande CLI `consolidate-by-doi` qui prend les 2 lignes, garde la plus riche, et fait une mise à jour. Pas implémenté tant qu'on n'a qu'une source.

### Traduction description → name (legacy migration)

Les bookmarks Aima-Tower antérieurs stockaient la description humaine ("Detection cancer par methylation cfDNA") au lieu du name machine ("cancer_detection_cfDNA"). `lib/migrate._description_to_name_map()` retraduit via `queries.json` pour garder `queries_matched` propre après migration.

**How to apply :** si on renomme un `name` dans `queries.json`, les bookmarks déjà migrés garderont l'ancien name. Pas de rollback automatique — c'est un choix assumé (traçabilité historique).
