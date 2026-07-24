---
name: synthese-paper
description: Produit la synthèse structurée d'un article scientifique, strictement identique à celle générée par la page /survey d'Aima-Tower (question de recherche, méthode, résultats clés, limitations, implications AIMA, recommandation). Accepte un PMID, un DOI, une URL ou un PDF. Use when the user says "synthese-paper", "synthétise ce papier", "résume cet article", "fiche de lecture", "que dit ce papier", gives a PMID/DOI/PubMed URL/PDF of a scientific article, or asks for the Tower-style synthesis of a publication.
---

<objective>
Sortir la synthèse d'un article scientifique **exactement comme Aima-Tower la produit** sur sa
page `/survey`, mais depuis n'importe quelle entrée : PMID, DOI, URL ou PDF — y compris pour un
article qui n'est pas dans la veille.

La fidélité est garantie **par construction** : le prompt système et le wrapper d'appel sont
importés depuis `~/Pipeline/Aima-Tower/src/`, jamais recopiés.
</objective>

<workflow>

## Étape 1 — Lancer le script

```bash
set -a; . ~/Pipeline/Aima-Survey/.env; set +a     # NCBI_API_KEY + CLAUDE_CODE_OAUTH_TOKEN
python3 ~/.claude/skills/synthese-paper/scripts/synthese_paper.py <entrée>
```

`<entrée>` : PMID, DOI, URL PubMed ou chemin vers un PDF — détection automatique.

Options :
- `--out fiche.md` — écrire la synthèse dans un fichier
- `--fulltext` — PDF uniquement, injecte le texte intégral. ⚠ **écart assumé** avec Tower, dont
  le prompt impose de se baser sur le seul résumé. À n'utiliser que si demandé explicitement.

## Étape 2 — Vérifier ce qui a été résolu

Le script affiche sur stderr l'identifiant, le titre, la priorité et les rubriques retenues.

- Si l'article est **dans la veille**, ses vraies priorité et rubriques sont utilisées → la
  synthèse est identique à celle qu'afficherait Tower.
- Sinon : `priorité = non classé`, `rubriques = hors veille`. C'est normal et attendu.

⚠ Si l'entrée était un PDF et qu'un **DOI a été détecté**, proposer de relancer avec ce DOI :
les métadonnées PubMed sont bien plus riches qu'une extraction heuristique de PDF.

## Étape 3 — Restituer

Afficher la synthèse telle quelle. Elle suit toujours cette structure :

1. Question de recherche · 2. Méthode · 3. Résultats clés · 4. Limitations ·
5. Implications AIMA · puis **Recommandation AIMA** en une phrase actionnable.

Ne pas la reformuler, ne pas la résumer, ne pas y ajouter de commentaire — c'est la sortie
produit. Si l'utilisateur veut une analyse complémentaire, la donner **après**, séparément.

</workflow>

<navigation>

| Besoin | Fichier |
|---|---|
| Ce qui garantit l'identité avec Tower, et ce qui la romprait | [references/contrat-fidelite.md](references/contrat-fidelite.md) |
| Formes d'entrée acceptées, cas PDF, enrichissement par la veille | [references/resolution-entrees.md](references/resolution-entrees.md) |

</navigation>

<hard_rules>

1. **Ne jamais recopier le prompt** de Tower dans ce skill — il doit rester importé, sinon il
   dérive dès que Boris modifie Tower.
2. **Ne jamais changer de modèle.** Tower utilise `claude-sonnet-4-6`, pas Haiku.
3. **Si Aima-Tower est introuvable, s'arrêter** plutôt que produire une synthèse approximative.
   Le script le fait déjà.
4. **Lire la DuckDB en read-only** — le cron d'Aima-Survey y écrit à 8h00.
5. **Ne pas retoucher la sortie du modèle.** C'est le livrable.

</hard_rules>

<notes>

La synthèse de Tower vit en **cache RAM** et n'est jamais persistée en base (les colonnes
`synthesis*` de DuckDB ne sont écrites par personne). Ce skill ne persiste rien non plus, sauf
si `--out` est passé.

Le `pipeline_context` injecté par Tower concatène tous les `~/Pipeline/*/CLAUDE.md` : c'est ce
qui permet à la section « Implications AIMA » d'être pertinente. Il est chargé automatiquement
par l'import.

</notes>
