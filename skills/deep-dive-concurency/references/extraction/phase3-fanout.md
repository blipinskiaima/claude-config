# Phase 3 — Fan-out parallèle (3 agents)

Trois agents lancés **en parallèle dans un seul message**, en background. Chacun a un périmètre
disjoint pour éviter la duplication.

⚠ Pendant qu'ils tournent, faire soi-même ce qu'ils ne peuvent pas faire : analyser la plaquette
locale (elle n'est ni sur le web ni sur PubMed, les agents n'y ont pas accès) et interroger notre
DuckDB.

## Agent A — Mécanique technique (`agent-explore` ou `general-purpose`)

Objectif : reconstituer la chaîne complète du tube au résultat.

À demander explicitement :
1. **Wet lab** : tube, délai, traitement, extraction, kit de librairie, séquenceur, couverture
2. **Dry lab** : outils **avec versions exactes**, génome de référence, filtres
3. **Features** : définition précise, tailles de fenêtres, normalisations, corrections
4. **Modèle** : famille, hyperparamètres, validation, **seuil de décision**
5. **Performances** : par cohorte, par stade, avec effectifs et intervalles de confiance
6. **Distinguer** ce qui vient du papier de validation de ce qui vient des papiers antérieurs

## Agent B — Marché et réglementaire (`agent-websearch`)

À demander explicitement :
1. Statut commercial : disponibilité, géographies, partenariats, prix, volumes
2. Réglementaire : LDT/CLIA, FDA (clearance, PMA, De Novo, Breakthrough Device), CE-IVD, IVDR
3. Remboursement : Medicare, code CPT/PLA, MolDX, décisions de couverture
4. Financement : levées avec montants et dates, dette, dirigeants, effectifs, signaux de tension
5. Essais cliniques : **interroger ClinicalTrials.gov**, statut, taille, dates de complétion
6. Roadmap produit
7. Controverses : critiques méthodologiques, éditoriaux, position des sociétés savantes
8. Concurrents de la cible

Exiger la distinction **faits sourcés (URL + date)** vs communiqués marketing, et la mention
explicite de ce qui n'a pas pu être vérifié.

## Agent C — État de l'art de notre différenciateur (`agent-websearch`)

C'est l'agent qui alimente la section « perspectives ». Lui donner **notre positionnement**
(depuis la fiche AIMA) et demander ce que la littérature dit de notre angle appliqué à leur
technologie.

Pour AIMA, les questions récurrentes :
1. État de l'art de la **combinaison méthylation + fragmentomique** : gain d'AUC mesuré, seul vs combiné
2. **Faisabilité nanopore** : fragmentomique ONT publiée ? méthylation native simultanée ?
   transposabilité des seuils de longueur de fragments calibrés sur Illumina ?
3. **Couverture minimale** par signal — et en particulier le verrou de la méthylation
   genome-wide résolue en régions à faible profondeur
4. Meilleurs résultats publiés de notre modalité sur l'indication visée, **par stade**
5. Acteurs académiques et industriels sur notre techno
6. Verrous réglementaires de l'indication
7. Marché, avec le volet européen et français

Exiger la séparation entre **démontré et publié** d'une part, prospectif ou marketing d'autre part.

## Piège de calibrage

Un rapport d'agent peut déclencher un avertissement du harness sur du contenu « instruction-shaped »
quand il cite des flags de CLI (par exemple `--permission-mode bypassPermissions` dans du code
d'authentification). C'est un faux positif attendu : traiter comme de la documentation, le
signaler brièvement dans la réponse à Boris.

## Sortie de phase

Trois synthèses structurées et sourcées, **non encore rédigées en rapport**.
