# Phase 2 — Reconstituer le corpus scientifique

La plaquette ne dit pas comment le produit marche. La mécanique réelle est dans la littérature
du laboratoire d'origine.

## 1. Identifier le laboratoire fondateur

La plupart des sociétés de diagnostic sont des spin-off académiques. Chercher :
- « {société} founded spin-off university »
- les co-fondateurs scientifiques, souvent encore au conseil
- l'affiliation des auteurs seniors des publications produit

**Exemple** : DELFI Diagnostics est un spin-off de Johns Hopkins (Velculescu, Scharpf).

## 2. ⚠ Chercher par AUTEURS, pas seulement par société

C'est le piège le plus coûteux de cette phase.

Une requête `"{Société}"[Affiliation]` rate la production académique amont, publiée sous
affiliation universitaire des années avant la commercialisation. Les papiers fondateurs sont
signés « Johns Hopkins University », pas « DELFI Diagnostics ».

```
mcp__pubmed__search_pubmed:
  "{Auteur1}[Author] OR {Auteur2}[Author]) AND ({technologie} OR {produit})"
```

Chercher aussi par nom de technologie et par nom d'algorithme (souvent un acronyme :
DELFI, ARTEMIS, GEMINI…).

## 3. Structurer le corpus par rôle

| Rôle | Ce qu'on cherche |
|---|---|
| **Papier fondateur** | pose le principe, souvent dans Nature/Science, cohorte modeste |
| **Papier d'application** | applique à l'indication visée, cohorte intermédiaire |
| **Validation clinique** | **c'est le produit commercial** — classifieur verrouillé, cohorte de validation tenue à part |
| Extensions de plateforme | autres indications, autres signaux |
| Biologie sous-jacente | mécanisme — souvent le plus utile pour nous |
| Revues et critiques | lettres, éditoriaux, réponses des auteurs |

Le papier de **validation clinique** est celui qui décrit le produit vendu. C'est là que sont
les vrais chiffres.

## 4. Chercher activement la controverse

Systématiquement : lettres critiques, commentaires, réponses des auteurs (`-Reply` dans le titre
PubMed), éditoriaux accompagnant la publication. Les positions des sociétés savantes aussi.

**Exemple réel** : la validation de FirstLook a fait l'objet d'une lettre critique en février
2026 (biais d'âge entre cas et témoins : médianes 70 vs 64 ans), avec réponse des auteurs.
C'est l'angle d'attaque le plus solide contre eux — et une question qui sera posée à AIMA aussi.

## 5. Croiser avec notre base de veille

Vérifier lesquels de ces PMIDs sont déjà dans `aima_survey.duckdb` (requête en phase 0).
Les absents révèlent soit une antériorité normale (base récente), soit un angle mort de veille.

⚠ Ne pas conclure trop vite à un défaut de nos requêtes : **rejouer la requête** de
`queries.json` avant d'affirmer qu'elle rate quelque chose. Une accusation non vérifiée de ce
type a déjà été portée à tort.

## Sortie de phase

Un corpus structuré par rôle, avec PMID, journal, année, cohorte, et le papier de validation
clinique clairement identifié.
