# Synthèse valeur ajoutée — Boris Blipinski (AIMA Diagnostics)

Session du 04/03/2026. Points clés extraits de l'analyse complète.

## Bullet points de valeur

- **Architecte et opérateur unique de l'intégralité du stack bioinformatique AIMA** : 13 projets conçus, codés, déployés et maintenus seul, du pipeline Nextflow au dashboard Dash en passant par les bases DuckDB.

- **Constructeur du pipeline cœur de métier Bam2Beta** (34 processus, V1.0.1) qui transforme les données brutes ONT en scores diagnostiques cancer avec 98.4% de corrélation clinique.

- **Seul membre de l'équipe opérant simultanément sur les 3 axes** R&D, Production et Plateforme Client — nœud central connectant Florian (modèles), Fred (web), Romain/Léa (wet lab) et Michael (stratégie).

- **Responsable du traitement de 700+ échantillons patients** (188 HCL + 519 CGFL) — chaque résultat clinique, chaque dossier investisseur, chaque contrat partenaire s'appuie sur ces données.

- **Pilote de la migration AWS→Scaleway** réalisée en 3 semaines (déc 2025), débloquant un goulot de calcul critique, nettoyant 15 TB, maintenant 100% de continuité opérationnelle.

- **Créateur d'un écosystème de traçabilité complet** (trace-prod, trace-platform, trace-workflow + Aima-Tower) remplaçant un tableur artisanal par un système industriel à 13 tables, daemon de sync et dashboard 5 pages temps réel.

- **Homme de terrain autant que de code** : déplacements physiques au HCL pour installer l'infra d'upload, résoudre une coupure de courant, et former les biologistes.

- **Initiateur et exécutant de la résolution du batch effect** : identification du problème, conception de Pod2Bam GPU multi-version (V4.2.0→V5.2.0), validation reproductibilité, lancement campagne 849 samples.

- **Concepteur du benchmark short-read** comparant 4 pipelines Illumina — positionnement AIMA sur la double technologie ONT + Illumina.

- **Facteur bloquant pour l'ensemble de l'équipe** : Florian attend bedMethyl, Fred attend JSON, Romain attend traitement, Michael s'appuie sur les résultats pour les dossiers cliniques.

- **Promoteur de l'outillage IA interne** : POC "Claude Code >>> Cursor", auto-formation, démo avec Fred, adoption poussée au sein de l'équipe.

- **Profil FinOps actif** : jobs d'extinction auto, estimations coûts/temps pod5, analyse setups GPU — conscience permanente de l'impact financier.

- **Rigueur de production industrielle** : SampleSheetChecker, 8 scénarios non-conformité, workflow qualification (QUALIF vs DEV sur S3), vérification 100% dossiers migrés.

- **Autonomie d'exécution avec alignement stratégique** : propose des solutions puis les exécute de bout en bout, avec points mensuels Michael et plans concertés.

- **Bus factor = 1** sur l'ensemble du stack bioinformatique : risque pour AIMA, mais preuve d'une charge technique justifiant 2-3 personnes.

## Données sources

- `~/boris_notes_extract.txt` — 75 entrées daily standup (sept 2025 – mars 2026)
- `~/Notes_Team_Meetings.txt` + `~/Notes_Team_Meetings (1).txt` — Réunions équipe 2025-2026
- `~/Pipeline/` — 13 projets analysés (code, README, configs)
