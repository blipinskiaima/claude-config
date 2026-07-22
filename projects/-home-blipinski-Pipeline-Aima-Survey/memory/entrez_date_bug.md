---
name: bug-entrez-date-et-pi-ge-du-fix-na-f
description: "entrez_date jamais écrite depuis 2026-04-21 (fetcher l'omet) — et pourquoi le corriger naïvement casserait les vues d'Aima-Tower"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2cf74f69-f6e5-4e35-926d-561f28925c84
  modified: 2026-07-22T16:10:14.256Z
---

Identifié le 2026-07-22, **non corrigé**.

## Le bug

`lib/fetcher.py` (~ligne 112-126) reconstruit le dict passé à `db.upsert_article()` clé par
clé et **omet `entrez_date`**. Le parser `lib/sources/pubmed.py` la produit correctement
(vérifié en live sur PMIDs réels), l'UPSERT de `lib/db.py` sait l'écrire — le fetcher la jette
au passage.

Résultat : **100 % des articles insérés depuis le 2026-04-21 ont `entrez_date` NULL** (268 sur
707 au moment du diagnostic). Les 439 valeurs non nulles viennent du script one-shot
`backfill_entrez_date.py`, supprimé au clean-skill v6.2.

## Le piège — ne PAS corriger naïvement

`lib/db.py` (~ligne 167-168) cale `first_seen_at` sur `entrez_date` si disponible, sinon
`now()`. Comme elle est toujours NULL, `first_seen_at` vaut la **date du cron**.

Or **Aima-Tower filtre et trie TOUTES ses vues sur `first_seen_at`** (cf.
[[tower_survey_coupling]]).

La recherche PubMed utilise `datetype=pdat` (date de **publication**), pas l'EDAT. Un article
paru cette semaine peut avoir été indexé des mois plus tôt s'il était en *ahead of print* —
c'est le cas courant. Mesure sur 40 articles récents re-fetchés : écart médian **28 jours**,
moyen 41 j, max 161 j, **aucun à zéro**.

Donc recaler `first_seen_at` sur `entrez_date` ferait **sortir ~50 % des articles de la vue
« semaine » et ~48 % de la vue « mois »** de Tower — des articles pourtant découverts il y a
quelques jours, invisibles parce que PubMed les avait indexés en avril.

**Why :** le comportement actuel, bien qu'accidentel, est le bon pour un outil de veille
(« qu'est-ce qui est nouveau *pour moi* »). L'intention documentée en v6.1 (caler sur l'EDAT)
était le mauvais choix produit.

**How to apply :** propager `entrez_date` comme colonne **informative uniquement**, ET retirer
le calage de `first_seen_at` sur elle dans `lib/db.py`. Faire l'un sans l'autre casse la veille.
Aucun test ne couvre ce chemin — la fixture de `tests/test_backfill.py` omet elle aussi
`entrez_date`, donc les 69 tests passent en reproduisant le bug. Ajouter un test sur le mapping
champ par champ de `run_fetch` → `upsert_article`.
