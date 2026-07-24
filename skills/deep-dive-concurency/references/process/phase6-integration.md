# Phase 6 — Intégration à la veille

## 1. Générer le PDF combiné

```bash
python3 ~/.claude/skills/deep-dive-concurency/scripts/md2pdf.py \
    {CIBLE}.pdf {CIBLE}-P1-TECHNIQUE.md {CIBLE}-P2-MARCHE.md
```

Prérequis : venv avec `weasyprint` + `markdown` (phase 0).

**Contrôler le résultat** — sans `poppler-utils`, la relecture visuelle est impossible, donc
vérifier par extraction :

```python
from pypdf import PdfReader
r = PdfReader(PDF); full = "\n".join(p.extract_text() or "" for p in r.pages)
# sections presentes ? glyphes speciaux rendus ? liens cliquables ?
for a in (page.get("/Annots") or []): print((a.get_object().get("/A") or {}).get("/URI"))
```

⚠ La police DejaVu ne contient pas tous les emojis. ⭐ disparaît silencieusement — utiliser ★
(U+2605), ⚠ et → passent correctement.

`*.pdf` est gitignoré dans Aima-Survey : le PDF est regénérable, ne pas le versionner.

## 2. Proposer un diff pour `competitors.json`

⛔ **Ne jamais écrire sans validation de Boris.** Afficher le diff proposé et attendre.

Champs à mettre à jour : `tech`, `product`, `stage`, `threat`, `threat_reason`, `aliases`
(important : les alias alimentent la requête PubMed `competitive_affiliations`), `url`,
`include_in_query_b`.

Si la société est absente, proposer une entrée complète avec son tier (1 = concurrent direct,
2 = adjacent, 3 = émergent).

Après édition validée, rappeler à Boris que `scripts/reclassify_competitors.py` doit être rejoué.

## 3. Écrire la mémoire

Un topic file dans
`~/.claude/projects/-home-blipinski-Pipeline-Aima-Survey/memory/{societe}.md`, type `reference`.

Y mettre **ce qui ne se redéduit pas** du rapport : les vrais chiffres avec leur piège, ce qui
est vérifié ou non, et l'implication pour AIMA. Lier avec `[[competitive_landscape]]` et
`[[aima_positioning]]`.

Ajouter la ligne correspondante dans `MEMORY.md`.

## 4. Mettre à jour la fiche AIMA si nécessaire

Si l'analyse révèle un manque dans `docs/AIMA-POSITIONING.md` (champ `[À PRÉCISER]` qu'on peut
désormais remplir, ou barre de performance de marché à inscrire), le proposer à Boris.

## 5. Référencer dans la documentation projet

Ajouter les deux rapports dans la section « Veille concurrentielle » du `CLAUDE.md`
d'Aima-Survey et dans l'arborescence du `README.md`.

## Sortie de phase

- PDF généré et contrôlé
- Diff `competitors.json` proposé (non appliqué sans accord)
- Mémoire écrite
- Documentation projet à jour
