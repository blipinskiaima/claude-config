# Phase 1 — Sources primaires

## Cas A — Une plaquette PDF est fournie

Les plaquettes marketing sont souvent des exports Illustrator : le texte n'est pas extractible
par un simple fetch web. Utiliser `pypdf` dans le venv de la phase 0.

```python
from pypdf import PdfReader
r = PdfReader(PDF)
for i, p in enumerate(r.pages, 1):
    print(f"--- page {i} ---")
    print(p.extract_text())
```

Si `WebFetch` sur l'URL du PDF renvoie une analyse pauvre (« contenu structurel »), c'est ce
cas — le fichier binaire est mis en cache localement par WebFetch, récupérer ce chemin.

## Cas B — Un article scientifique est fourni

Passer par les outils MCP PubMed :

```
ToolSearch: "select:mcp__pubmed__search_pubmed,mcp__pubmed__fetch_summary,mcp__pubmed__get_fulltext"
```

`get_fulltext` déborde souvent la limite de tokens et écrit dans un fichier. Ce fichier a des
**lignes très longues** : ne pas le lire par plages de lignes, utiliser un script Python de
recherche par mots-clés avec extraction de contexte.

⚠ Si plusieurs papiers sont récupérés d'un coup, ils sont **concaténés dans le même fichier**.
Toujours vérifier à quel papier appartient chaque détail méthodologique (piège avéré).

## Cas C — Rien n'est fourni

Partir du nom de la société : site officiel, page produit, mentions réglementaires.
Passer directement en phase 2 pour la mécanique.

## ⚠ Le point clé : recenser les ABSENCES

Une plaquette se lit autant par ce qu'elle **tait**. Tester systématiquement la présence des
termes techniques et des métriques :

```python
low = texte.lower()
for t in ["fragmentom","methylation","machine learning","genome","sequencing","algorithm",
          "sensitivity","specificity","ppv","positive predictive","npv","auc","accuracy"]:
    print(f"{t:24s} {'PRESENT' if t in low else 'ABSENT'} (x{low.count(t)})")
```

**Exemple réel (DELFI FirstLook, août 2025)** : les mots *fragmentomics*, *machine learning*,
*genome*, *methylation*, *sensitivity*, *specificity* et *positive predictive value* sont tous
absents. La seule description technique tient en une phrase. C'est un résultat d'analyse en soi.

## ⚠ Tracer l'origine de chaque chiffre de performance

Repérer les appels de note des métriques mises en avant et **remonter à la référence**.

**Exemple réel** : les trois chiffres de la plaquette FirstLook (VPN 99,8 %, NNS 79, RR 5,2)
portent tous l'appel 9, qui renvoie à « Unpublished data on file » — aucune vérification
possible, et deux de ces valeurs diffèrent de celles publiées (76 et 5,5).

Extraire aussi la bibliographie complète et **classer les références par nature** :
épidémiologie, modélisation, recherche sur les services de santé, biologie moléculaire.
Une plaquette de diagnostic qui ne cite aucun papier de sa propre technologie est un signal.

## Sortie de phase

- Texte intégral extrait
- Tableau des termes présents/absents
- Origine tracée de chaque métrique affichée
- Bibliographie classée par nature
