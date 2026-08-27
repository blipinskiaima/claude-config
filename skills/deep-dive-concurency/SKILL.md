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
PARTIE 2 — EXTRACTION CONCURRENT cadrage → sources → corpus → fan-out → fact-check ⛔
    │                            reconstitution vérifiée, aucune comparaison à ce stade
    ▼
PARTIE 3 — COMPARAISON           confronte le concurrent vérifié ↔ profil AIMA, axe par axe
                                 → rédaction de P1 et P2 → intégration veille
```

**Ce que ce skill produit, et ce qu'il ne produit pas.** Un dossier concurrent complet compte
**quatre volets**, mais deux seulement sont de la rédaction :

```
concurency/profils/{SLUG}-P0-MAJEURS.md      ← AUTO, cli.py competitive-profil (cron lundi 10h)
concurency/profils/{SLUG}-P1-TECHNIQUE.md    ← CE SKILL, écrit à la main, puis fact-check
concurency/profils/{SLUG}-P2-MARCHE.md       ← CE SKILL, écrit à la main, puis fact-check
concurency/profils/{SLUG}-P3-TRAJECTOIRE.md  ← AUTO, cli.py competitive-profil (cron lundi 10h)
concurency/pdf/profils/{SLUG}.pdf            ← AUTO, run_profils.sh, SI P1 existe
```

P0 et P3 sont **dérivées de la table `competitive_events`**, déterministes, régénérées chaque
semaine : ne jamais les écrire à la main, elles seraient écrasées au prochain lundi. P1 et P2
ne sont **jamais** régénérées : ce sont elles, et elles seules, que ce skill rédige.

⚠ **`concurency/profils/`, pas `concurency/rapports/`.** `rapports/` et `pdf/` (racine) tiennent
encore la génération du 22-23/07/2026, d'avant la vérification adversariale du 29/07 (117
corrections) — ils sont gelés, on n'y écrit plus. Et c'est `profils/` que la page « Deep dive
concurrent » d'Aima Tower lit : un dossier écrit ailleurs n'apparaîtra jamais dans l'onglet.

Sortie de bout en bout : P1 + P2 rédigés et vérifiés, une proposition de mise à jour du
référentiel de veille (§ Partie 3, phase 6) — et, si de nouvelles données AIMA sont apparues,
une mise à jour du profil (Partie 1).

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

**Sortie de la Partie 2** : un corpus vérifié, structuré **sur les mêmes axes que le profil
AIMA** (pour un diff 1:1 en Partie 3), chaque chiffre portant son marqueur de preuve et son
verdict de fact-check. Les phases 0-4 le construisent ; la phase 4 le fige.

Il n'y a **pas de fiche intermédiaire sur disque**. Une fiche `competitors/{NOM}-PROFIL.md` a
existé pour Natera en juillet 2026, puis les six analyses suivantes s'en sont passées : elle
recopiait ce que P1 et P2 disent déjà, et se périmait dès la première correction. Le matériau
vérifié reste dans la session et va directement en Partie 3.

### Phase 0 — Cadrage et prérequis

1. Charger le **profil AIMA** (Partie 1) et déterminer **à quelle ligne** (MRD via mVAF v1.4, ou
   MCED via THEMELIO) le concurrent s'oppose — ou aucune.
2. Identifier la cible (société, produit, URL ou fichier fourni).
3. **Fixer le SLUG**, qui nomme tous les fichiers du dossier. Règle appliquée par le code
   (`cli.py` et `lib/competitive/profil.py::_slug`) : `nom.upper().replace(" ", "-")`.
   ⚠ C'est le **nom de la société**, jamais celui du produit : `GUARDANT-HEALTH` et non
   `GUARDANT-SHIELD`, `DELFI-DIAGNOSTICS` et non `DELFI-FIRSTLOOK` (les deux formes en
   `rapports/` datent d'avant la convention). Le slug est un contrat avec Aima Tower, qui le
   valide contre `^[A-Z0-9-]{2,40}$` et affiche `slug.replace("-"," ").title()` : un slug produit
   afficherait une société qui n'existe pas. Il doit être **identique** au champ `name` de
   `competitors.json`, sinon `competitive-profil` écrira P0/P3 sous un autre slug et le dossier
   se dédoublera dans l'onglet.
4. Vérifier les prérequis outils (`poppler-utils`, venv PDF).
5. Lire la fiche existante dans `~/Pipeline/Aima-Survey/data/competitors.json` et ce que la
   veille a déjà capté (DuckDB en read-only). Société absente du fichier → elle n'a **aucun**
   évènement collecté : P0 et P3 sortiront vides tant que le bloc `watch` n'existe pas
   (phase 6).

   ⚠ **« Ce que la veille a capté » veut dire le TEXTE, pas le décompte.** La colonne
   `competitive_events.raw_text` porte le corps des documents, pas seulement leur titre :
   sections `[litiges]` et `[concurrence]` des 10-K et 10-Q, et depuis le 27/08/2026 les
   communiqués de résultats déposés en EX-99.1. **Ouvrir ces textes fait partie de la phase 0**,
   au même titre que lire la plaquette.

   ```bash
   cd ~/Pipeline/Aima-Survey && python3 -c "
   import duckdb
   c = duckdb.connect('data/aima_survey.duckdb', read_only=True)
   for r in c.execute('''select source, event_date, substr(title,1,60), length(coalesce(raw_text,\'\'))
     from competitive_events where competitor ilike ? and coalesce(raw_text,\'\') <> \'\'
     order by event_date desc''', ['%{NOM}%']).fetchall(): print(r)"
   ```

   Compté le 26/08/2026 sur Biodesix : **112 ko de prose réglementaire signée de la société
   étaient en base le jour de la rédaction et n'ont pas été ouverts** — un 10-K et trois 10-Q.
   Le dossier est parti sur les seuls nombres de l'API XBRL et s'est retrouvé avec 29
   `[NON CONFIRMÉ]` contre 12 `[SOURCÉ]`, seul cas où le non-confirmé l'emporte sur les huit
   dossiers. C'est la cause racine de sa refonte intégrale. **Une société cotée dit dans ses
   dépôts ce qu'elle ne dira jamais dans un communiqué** : ses litiges, ses dépendances
   fournisseur, et la liste de ceux qu'elle considère elle-même comme ses concurrents.

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

**Sortie** : le corpus consolidé et figé, chaque chiffre portant son marqueur de preuve **et**
son verdict de fact-check. C'est ce matériau vérifié, et non des notes éparses, qui entre en
Partie 3.

Voir [references/extraction/phase4-factcheck.md](references/extraction/phase4-factcheck.md) et la
grille [references/quality/grille-pieges.md](references/quality/grille-pieges.md).

</partie_2_extraction_concurrent>

<partie_3_comparaison>

## PARTIE 3 — Comparaison

Confronter le concurrent (Partie 2, vérifié) au profil AIMA (Partie 1), axe par axe, puis rédiger.

### Phase 5 — Comparaison & rédaction

La comparaison est un **diff axe par axe** entre le corpus vérifié (Partie 2) et le profil AIMA
(Partie 1), structurés sur les mêmes axes. La grille de cross-check des verrous AIMA (profil §7)
devient la section « Verrous AIMA » du P1.

Les deux rapports **dérivent** de ce diff, pour deux publics :
`concurency/profils/{SLUG}-P1-TECHNIQUE.md` (bioinfo) et `{SLUG}-P2-MARCHE.md` (direction).
Chaque chiffre garde son marqueur de preuve et son verdict. Section « positionnement vs AIMA »
obligatoire dans les deux.

⛔ **Lire les faits majeurs AVANT d'écrire**, et les traiter dans le corps des deux rapports :

```bash
cd ~/Pipeline/Aima-Survey && python3 cli.py competitive-majeurs "{NOM}"
```

Un rapport ordonné par récence enterre les faits lourds : c'est ce qui a relégué l'inclusion
ACS de SimpleScreen en page 3 du dossier Freenome.

⚠ **Ne plus coller cette sortie en `## 0. Faits majeurs`** dans P1 et P2 — c'était la règle
jusqu'au 30/07/2026. Elle vit maintenant dans son propre volet, `{SLUG}-P0-MAJEURS.md`,
régénéré chaque lundi depuis `competitive_events` par la même fonction `faits_majeurs()` : une
copie collée dans P1/P2 se périmerait sans que personne ne s'en aperçoive. La commande reste le
moyen de **savoir ce que P0 dira**, et la règle de fond ne change pas : un fait majeur qui
n'apparaît qu'en sous-section du corps est un rapport raté.

Sortie vide → l'écrire, et vérifier que les bons canaux sont surveillés (bloc `watch`, phase 6)
avant d'en conclure qu'il ne se passe rien.

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
| Prérequis, SLUG, ligne produit visée, entrée `competitors.json` | [extraction/phase0-cadrage.md](references/extraction/phase0-cadrage.md) |
| Extraire une plaquette PDF, analyser les absences | [extraction/phase1-sources-primaires.md](references/extraction/phase1-sources-primaires.md) |
| Retrouver les vraies publications derrière un produit | [extraction/phase2-corpus-scientifique.md](references/extraction/phase2-corpus-scientifique.md) |
| Prompts des 3 agents de recherche | [extraction/phase3-fanout.md](references/extraction/phase3-fanout.md) |
| Protocole de vérification adversariale | [extraction/phase4-factcheck.md](references/extraction/phase4-factcheck.md) |
| Rédiger P1 et P2 | [comparaison/phase5-redaction.md](references/comparaison/phase5-redaction.md) |
| Inscrire le concurrent dans la veille (2 fichiers, pas 1) | [comparaison/phase6-integration.md](references/comparaison/phase6-integration.md) |
| **Pièges chiffrés récurrents** (à lire absolument) | [quality/grille-pieges.md](references/quality/grille-pieges.md) |
| Convention des marqueurs de preuve | [quality/niveaux-preuve.md](references/quality/niveaux-preuve.md) |
| Plan type des rapports P1 et P2 | [templates/structure-rapports.md](references/templates/structure-rapports.md) |

</navigation>

<tools>

| Script | Usage |
|---|---|
| `scripts/md2pdf.py` | `python3 md2pdf.py sortie.pdf P0.md P1.md P2.md P3.md` — PDF combiné, charte AIMA, liens cliquables. Nécessite un venv avec `weasyprint` + `markdown` (voir phase 0). En routine c'est `run_profils.sh` qui l'appelle, pas nous. |

Côté Aima-Survey, cinq sous-commandes `cli.py` servent ce skill — toutes en lecture, aucune
n'écrit dans `competitors.json` :

| Commande | Rôle | Quand |
|---|---|---|
| `competitive-probe "{NOM}" --domain x.com` | Découvre les identifiants `watch` (sitemap, CIK, sponsor ClinicalTrials) et **imprime** le bloc JSON à coller | une fois par concurrent, phase 6 |
| `competitive-majeurs "{NOM}"` | Imprime les faits majeurs — aperçu de ce que P0 contiendra | avant de rédiger, phase 5 |
| `competitive-profil --competitor "{NOM}"` | **Écrit** P0 et P3 depuis `competitive_events` | cron du lundi ; à la main pour vérifier un nouveau concurrent |
| `competitive-pending` | Évènements collectés pas encore notifiés par mail | diagnostic |
| `competitive-reclassify` | Rejoue la classification Haiku des articles PubMed après ajout d'un concurrent ou d'un alias | après édition de `competitors.json` |

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
