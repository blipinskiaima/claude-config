---
name: Paysage concurrentiel AIMA (source de vérité)
description: Liste des concurrents AIMA sur le marché cfDNA methylation cancer — source de vérité versionnée + veille active via queries.json
type: reference
originSessionId: 2436002f-1dc1-46c9-9d7b-0cb1a41488d6
---
## Source de vérité

**Fichier structuré** : `~/Pipeline/Aima-Survey/data/competitors.json` (22 entreprises, 3 tiers, aliases PubMed-ready)
**Rendu humain** : `~/Pipeline/Aima-Survey/docs/COMPETITORS.md` (tableaux markdown + synthèse stratégique)
**Audit date** : 2026-04-21

## Structure JSON

```
{
  "tier_1": [...] // 7 concurrents directs (méthylation cfDNA + MCED/MRD)
  "tier_2": [...] // 8 adjacents (liquid biopsy similar use case)
  "tier_3": [...] // 7 émergents / plateformes / early stage
}
```

Chaque entrée : `name`, `aliases` (pour match PubMed `[Affiliation]`), `hq`, `founded`, `tech`, `product`, `stage`, `cancers`, `threat`, `threat_reason`, `url`, `include_in_query_b` (bool).

## Intégrations (à vérifier avant de recommander ces fichiers)

1. **`queries.json` d'Aima-Survey** : rubrique `competitive_affiliations` construite à partir des entrées avec `include_in_query_b=true` — fetch PubMed quotidien ciblant les affiliations des concurrents
2. **Rubrique "Concurrence" Aima-Tower** : onglet qui liste tous les articles dont `queries_matched` contient `competitive_affiliations` — **doublon UI assumé** avec les rubriques techniques (1 article peut apparaître dans plusieurs onglets)
3. **Page `/competitors` Aima-Tower** : tableau statique lu directement depuis `competitors.json`

## Top 3 menaces identifiées (2026-04-21)

1. **Volition (VolitionRx)** — remboursement France Q4 2026 sur cancer du poumon → attaque marché AIMA territorial
2. **biomodal** (ex-Cambridge Epigenetix) — même combo 5mC+5hmC, intégré Element AVITI que AIMA teste → convergence technologique UK leader
3. **Freenome + Exact Sciences** — deal $885M, FDA CRC 2026 + lung 2026 → barrière entrée USA

## Opportunités de différenciation AIMA

1. **Pipeline ONT low-coverage (~1x) UNIQUE cliniquement** — aucun Tier 1 n'utilise ONT
2. **Multi-modalité un seul run** : méthylation (5mC+5hmC) + fragmentomics + CNV — AIMA seul à verticalement intégrer les 3

## Usage pour sessions futures

Face à une question du type :
- "Qui sont les concurrents d'AIMA ?" → lire `competitors.json` (toujours la version la plus à jour)
- "On doit réagir à quel move stratégique ?" → section "Synthèse stratégique" dans `COMPETITORS.md`
- "Comment ajouter un nouveau concurrent ?" → éditer `competitors.json` (+ aliases PubMed si `include_in_query_b=true`) puis régénérer MD

**Ne pas citer de mémoire** le tableau : le fichier JSON peut avoir été mis à jour depuis. Toujours lire le fichier courant avant de répondre.
