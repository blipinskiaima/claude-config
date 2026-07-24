---
name: deep-dive-concurency
description: Analyse concurrentielle approfondie d'une société de diagnostic, à partir d'une plaquette commerciale, d'un article scientifique, ou du seul nom de la société. Produit 2 rapports (technique bioinfo + marché direction) comparés au positionnement AIMA, avec fact-check adversarial obligatoire de chaque chiffre. Use when the user says "deep-dive-concurency", "analyse concurrent", "veille sur {société}", "que fait {concurrent}", "décortique cette plaquette", "analyse ce produit concurrent", or gives a competitor brochure/URL/paper to analyze.
---

<objective>
Produire une analyse concurrentielle **vérifiée** d'une société de diagnostic, cadrée par notre
propre positionnement, en 6 phases dont une de vérification bloquante.

Sortie : 2 markdown (P1 technique, P2 marché) + 1 PDF combiné + une proposition de mise à jour
du référentiel de veille.

**Principe fondateur** : une plaquette commerciale ne dit jamais comment le produit marche, et
ses chiffres ne sont presque jamais ceux des publications. Le travail consiste à reconstituer la
mécanique réelle depuis la littérature, puis à confronter chaque affirmation à sa source.
</objective>

<workflow>

## Phase 0 — Cadrage et prérequis

1. Identifier la cible (société, produit, URL ou fichier fourni s'il y en a un).
2. **Charger le référentiel AIMA** : `~/Pipeline/Aima-Survey/docs/AIMA-POSITIONING.md`.
   Sans lui, aucune comparaison n'est fiable. Déterminer **à quelle ligne de produit**
   (MRD via mVAF v1.4, ou MCED via THEMELIO) le concurrent s'oppose — ou aucune.
3. Vérifier les prérequis outils (`poppler-utils`, venv PDF).
4. Lire la fiche existante dans `~/Pipeline/Aima-Survey/data/competitors.json` si la société y est.

Voir [references/process/phase0-cadrage.md](references/process/phase0-cadrage.md).

## Phase 1 — Sources primaires

Extraire intégralement ce qui est fourni (plaquette, article, page produit).

⚠ **Recenser ce qui est ABSENT autant que ce qui est présent.** L'absence des termes techniques
et des métriques de performance dans une plaquette est une donnée exploitable.

Voir [references/process/phase1-sources-primaires.md](references/process/phase1-sources-primaires.md).

## Phase 2 — Reconstitution du corpus scientifique

Les plaquettes ne citent jamais la vraie science. Remonter au laboratoire d'origine et
**chercher par auteurs**, pas seulement par nom de société : les spin-off publient sous
affiliation académique.

Voir [references/process/phase2-corpus-scientifique.md](references/process/phase2-corpus-scientifique.md).

## Phase 3 — Fan-out parallèle (3 agents)

Trois axes lancés en parallèle : mécanique technique, marché et réglementaire, état de l'art de
notre différenciateur appliqué à leur technologie.

Voir [references/process/phase3-fanout.md](references/process/phase3-fanout.md).

## Phase 4 — Fact-check adversarial ⛔ BLOQUANT

**Ne jamais rédiger avant cette phase.** Un agent indépendant challenge chaque affirmation
chiffrée : CONFIRMÉ / INEXACT / TROMPEUR / NON VÉRIFIABLE.

Inclut les affirmations sur **nos propres outils**, à vérifier aussi sévèrement.

Voir [references/process/phase4-factcheck.md](references/process/phase4-factcheck.md) et la
grille [references/quality/grille-pieges.md](references/quality/grille-pieges.md).

## Phase 5 — Rédaction

Deux documents, publics distincts, chaque chiffre porteur d'un marqueur de niveau de preuve.
Section « positionnement vs AIMA » obligatoire dans les deux.

Voir [references/process/phase5-redaction.md](references/process/phase5-redaction.md),
[references/templates/structure-rapports.md](references/templates/structure-rapports.md) et
[references/quality/niveaux-preuve.md](references/quality/niveaux-preuve.md).

## Phase 6 — Intégration à la veille

Proposer un diff pour `competitors.json`, écrire la mémoire, générer le PDF.
**Attendre validation avant d'écrire dans le référentiel.**

Voir [references/process/phase6-integration.md](references/process/phase6-integration.md).

</workflow>

<navigation>

| Besoin | Fichier |
|---|---|
| Prérequis, référentiel AIMA, choix de la ligne produit | [process/phase0-cadrage.md](references/process/phase0-cadrage.md) |
| Extraire une plaquette PDF, analyser les absences | [process/phase1-sources-primaires.md](references/process/phase1-sources-primaires.md) |
| Retrouver les vraies publications derrière un produit | [process/phase2-corpus-scientifique.md](references/process/phase2-corpus-scientifique.md) |
| Prompts des 3 agents de recherche | [process/phase3-fanout.md](references/process/phase3-fanout.md) |
| Protocole de vérification adversariale | [process/phase4-factcheck.md](references/process/phase4-factcheck.md) |
| Rédiger les 2 rapports | [process/phase5-redaction.md](references/process/phase5-redaction.md) |
| Mettre à jour competitors.json et la mémoire | [process/phase6-integration.md](references/process/phase6-integration.md) |
| **Pièges chiffrés récurrents** (à lire absolument) | [quality/grille-pieges.md](references/quality/grille-pieges.md) |
| Convention des marqueurs de preuve | [quality/niveaux-preuve.md](references/quality/niveaux-preuve.md) |
| Plan type des rapports P1 et P2 | [templates/structure-rapports.md](references/templates/structure-rapports.md) |

</navigation>

<tools>

| Script | Usage |
|---|---|
| `scripts/md2pdf.py` | `python3 md2pdf.py sortie.pdf P1.md P2.md` — PDF combiné, charte AIMA, liens cliquables. Nécessite un venv avec `weasyprint` + `markdown` (voir phase 0). |

</tools>

<hard_rules>

1. **Jamais de rédaction avant la phase 4.** L'ordre inverse a coûté une réécriture complète
   lors de l'analyse DELFI de juillet 2026.
2. **Une sensibilité sans sa spécificité et son effectif n'est pas une donnée.** Refuser toute
   comparaison entre deux performances mesurées à des spécificités différentes.
3. **Ne jamais citer un chiffre de validation croisée** comme performance d'un test.
4. **Distinguer systématiquement** valeur observée, estimation repondérée et chiffre marketing.
5. **Vérifier nos propres affirmations** sur nos outils avec la même sévérité que celles du
   concurrent.
6. **Ne pas écrire dans `competitors.json`** sans validation explicite de Boris.

</hard_rules>
