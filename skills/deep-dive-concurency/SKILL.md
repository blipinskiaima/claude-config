---
name: deep-dive-concurency
description: Analyse concurrentielle approfondie d'une société de diagnostic, à partir d'une plaquette commerciale, d'un article scientifique, ou du seul nom de la société. Architecture en 3 parties — (1) le profil AIMA vivant qui sert de base de comparaison, (2) l'extraction vérifiée des informations du concurrent, (3) la comparaison. Fact-check adversarial obligatoire de chaque chiffre. Use when the user says "deep-dive-concurency", "analyse concurrent", "veille sur {société}", "que fait {concurrent}", "décortique cette plaquette", "analyse ce produit concurrent", "mets à jour le profil aima", or gives a competitor brochure/URL/paper to analyze.
---

<objective>
Produire une analyse concurrentielle **vérifiée** d'une société de diagnostic, cadrée par le
positionnement AIMA, en trois parties bien séparées.

**Architecture** :

```
PARTIE 1 — PROFIL AIMA          référentiel vivant, base de comparaison, maintenu à part
    │                            concurency/AIMA-POSITIONING.md  (source : rapport Exis 1.1)
    ▼
PARTIE 2 — EXTRACTION CONCURRENT procédure d'extraction vérifiée → fiche {NOM}-PROFIL.md
    │                            cadrage → sources → corpus → fan-out → fact-check ⛔
    │                            sortie = fiche structurée, miroir des axes du profil AIMA
    ▼
PARTIE 3 — COMPARAISON           confronte {NOM}-PROFIL.md ↔ profil AIMA, axe par axe
                                 → rapports P1/P2 dérivés → intégration veille
```

Sortie : 2 markdown (P1 technique, P2 marché) + 1 PDF combiné + une proposition de mise à jour
du référentiel de veille — et, si de nouvelles données AIMA sont apparues, une mise à jour du
profil (Partie 1).

**Principe fondateur** : une plaquette commerciale ne dit jamais comment le produit marche, et
ses chiffres ne sont presque jamais ceux des publications. Le travail consiste à reconstituer la
mécanique réelle depuis la littérature, puis à confronter chaque affirmation à sa source **et au
profil AIMA**.
</objective>

<partie_1_profil_aima>

## PARTIE 1 — Le profil AIMA

Le profil AIMA est la **base de comparaison** de tout deep-dive, découplée de l'analyse
concurrente et maintenue dans le temps.

- **Fichier canonique** : `~/Pipeline/Aima-Survey/concurency/AIMA-POSITIONING.md`.
- **Source de vérité des chiffres** : rapport **Exis 1.1 (SD-02)**, reproduit par la page
  `/exploration` d'Aima Tower ; code `~/Pipeline/` pour les specs techniques.
- Le charger au début de chaque analyse. S'il paraît obsolète, le mettre à jour **avant**.
- On le met à jour **au fil de l'eau** dès que de nouvelles données autoritaires arrivent
  (nouveau rapport Exis, nouvel eval, décision réglementaire) — indépendamment d'un deep-dive.

Procédure de chargement et de mise à jour : [references/aima/profil.md](references/aima/profil.md).

Déclencheur direct : « mets à jour le profil AIMA » → aller directement en Partie 1 sans lancer
d'analyse concurrente.

</partie_1_profil_aima>

<partie_2_extraction_concurrent>

## PARTIE 2 — Extraction des informations du concurrent

Procédure d'extraction **vérifiée** de la cible, indépendante d'AIMA. Aucune comparaison ici :
on reconstitue et on vérifie.

**Sortie de la Partie 2** : une **fiche concurrent structurée**,
`~/Pipeline/Aima-Survey/concurency/competitors/{NOM}-PROFIL.md`, aux **mêmes axes que le profil AIMA**
(pour un diff 1:1 en Partie 3). C'est le miroir concurrent du profil AIMA : fiche vivante,
remise à jour à chaque analyse. Template et discipline de marquage :
[references/templates/profil-concurrent.md](references/templates/profil-concurrent.md). Les
phases 0-4 remplissent cette fiche ; la phase 4 la fige avec les verdicts de fact-check.

### Phase 0 — Cadrage et prérequis

1. Charger le **profil AIMA** (Partie 1) et déterminer **à quelle ligne** (MRD via mVAF v1.4, ou
   MCED via THEMELIO) le concurrent s'oppose — ou aucune.
2. Identifier la cible (société, produit, URL ou fichier fourni).
3. Vérifier les prérequis outils (`poppler-utils`, venv PDF).
4. Lire la fiche existante dans `~/Pipeline/Aima-Survey/data/competitors.json` et ce que la
   veille a déjà capté (DuckDB en read-only).

Voir [references/extraction/phase0-cadrage.md](references/extraction/phase0-cadrage.md).

### Phase 1 — Sources primaires

Extraire intégralement ce qui est fourni (plaquette, article, page produit).
⚠ **Recenser ce qui est ABSENT autant que ce qui est présent.**

Voir [references/extraction/phase1-sources-primaires.md](references/extraction/phase1-sources-primaires.md).

### Phase 2 — Reconstitution du corpus scientifique

Remonter au laboratoire d'origine et **chercher par auteurs**, pas seulement par nom de société.

Voir [references/extraction/phase2-corpus-scientifique.md](references/extraction/phase2-corpus-scientifique.md).

### Phase 3 — Fan-out parallèle (3 agents)

Trois axes en parallèle : mécanique technique, marché et réglementaire, état de l'art de notre
différenciateur appliqué à leur technologie.

Voir [references/extraction/phase3-fanout.md](references/extraction/phase3-fanout.md).

### Phase 4 — Fact-check adversarial ⛔ BLOQUANT

**Ne jamais passer en Partie 3 avant cette phase.** Un agent indépendant challenge chaque
affirmation chiffrée : CONFIRMÉ / INEXACT / TROMPEUR / NON VÉRIFIABLE. Inclut les affirmations
sur **nos propres outils**, à vérifier aussi sévèrement.

**Sortie** : la fiche `{NOM}-PROFIL.md` consolidée et figée, chaque chiffre portant son marqueur
de preuve **et** son verdict de fact-check. C'est cette fiche, et non des notes éparses, qui
entre en Partie 3.

Voir [references/extraction/phase4-factcheck.md](references/extraction/phase4-factcheck.md) et la
grille [references/quality/grille-pieges.md](references/quality/grille-pieges.md).

</partie_2_extraction_concurrent>

<partie_3_comparaison>

## PARTIE 3 — Comparaison

Confronter le concurrent (Partie 2, vérifié) au profil AIMA (Partie 1), axe par axe, puis rédiger.

### Phase 5 — Comparaison & rédaction

La comparaison est un **diff axe par axe** entre `{NOM}-PROFIL.md` (Partie 2) et le profil AIMA
(Partie 1), tous deux structurés sur les mêmes axes. La grille de cross-check des verrous AIMA
(profil §7 ↔ fiche §6) est déjà remplie dans la fiche concurrent.

Les deux rapports **dérivent** de ce diff, pour deux publics : `{NOM}-P1-TECHNIQUE.md` (bioinfo)
et `{NOM}-P2-MARCHE.md` (direction). Chaque chiffre garde son marqueur de preuve et son verdict.
Section « positionnement vs AIMA » obligatoire dans les deux.

Voir [references/comparaison/phase5-redaction.md](references/comparaison/phase5-redaction.md),
[references/templates/structure-rapports.md](references/templates/structure-rapports.md) et
[references/quality/niveaux-preuve.md](references/quality/niveaux-preuve.md).

### Phase 6 — Intégration à la veille

Proposer un diff pour `competitors.json`, écrire la mémoire, générer le PDF. Si l'analyse révèle
un manque dans le profil AIMA, proposer sa mise à jour (retour Partie 1).
**Attendre validation avant d'écrire dans le référentiel.**

Voir [references/comparaison/phase6-integration.md](references/comparaison/phase6-integration.md).

</partie_3_comparaison>

<navigation>

| Besoin | Fichier |
|---|---|
| **Charger / mettre à jour le profil AIMA** | [aima/profil.md](references/aima/profil.md) |
| Le profil AIMA lui-même (contenu) | `~/Pipeline/Aima-Survey/concurency/AIMA-POSITIONING.md` |
| Prérequis, choix de la ligne produit, fiche concurrent | [extraction/phase0-cadrage.md](references/extraction/phase0-cadrage.md) |
| Extraire une plaquette PDF, analyser les absences | [extraction/phase1-sources-primaires.md](references/extraction/phase1-sources-primaires.md) |
| Retrouver les vraies publications derrière un produit | [extraction/phase2-corpus-scientifique.md](references/extraction/phase2-corpus-scientifique.md) |
| Prompts des 3 agents de recherche | [extraction/phase3-fanout.md](references/extraction/phase3-fanout.md) |
| Protocole de vérification adversariale | [extraction/phase4-factcheck.md](references/extraction/phase4-factcheck.md) |
| **Structure de la fiche profil concurrent** | [templates/profil-concurrent.md](references/templates/profil-concurrent.md) |
| Rédiger les 2 rapports | [comparaison/phase5-redaction.md](references/comparaison/phase5-redaction.md) |
| Mettre à jour competitors.json et la mémoire | [comparaison/phase6-integration.md](references/comparaison/phase6-integration.md) |
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

1. **Jamais de rédaction (Partie 3) avant le fact-check (phase 4).** L'ordre inverse a coûté une
   réécriture complète lors de l'analyse DELFI de juillet 2026.
2. **Une sensibilité sans sa spécificité et son effectif n'est pas une donnée.** Refuser toute
   comparaison entre deux performances mesurées à des spécificités différentes.
3. **Ne jamais citer un chiffre de validation croisée** comme performance d'un test.
4. **Distinguer systématiquement** valeur observée, estimation repondérée et chiffre marketing.
5. **Vérifier nos propres affirmations** sur nos outils avec la même sévérité que celles du
   concurrent.
6. **Ne pas écrire dans `competitors.json` ni dans le profil AIMA** sans validation explicite de
   Boris.
7. **Ne jamais mélanger deux référentiels AIMA** : mVAF v1.4 seul (Exis 1.1) et combo THEMELIO
   sont des scores et des cohortes distincts — jamais opposés comme un progrès.

</hard_rules>
