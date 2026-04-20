# Synthèse valeur ajoutée — Boris Blipinski (AIMA Diagnostics)

Dernière mise à jour : 20/04/2026. Couvre la période sept 2025 – avril 2026.

## Bullet points de valeur

### Infrastructure & Pipeline cœur (sept 2025 – jan 2026)

- **Architecte et opérateur unique de l'intégralité du stack bioinformatique AIMA** : 16 projets conçus, codés, déployés et maintenus seul, du pipeline Nextflow au dashboard Dash en passant par les bases DuckDB et le pipeline ML.

- **Constructeur du pipeline cœur de métier Bam2Beta** (34 processus, V1.0.2) qui transforme les données brutes ONT en scores diagnostiques cancer avec 98.4% de corrélation clinique — produit technique sur lequel repose toute la proposition de valeur d'AIMA.

- **Pilote de la migration AWS→Scaleway** réalisée en 3 semaines (déc 2025), débloquant un goulot de calcul critique, nettoyant 15 TB, maintenant 100% de continuité opérationnelle.

- **Homme de terrain autant que de code** : déplacements physiques au HCL pour installer l'infra d'upload (script cron+log+alerte), résoudre une coupure de courant, et former les biologistes.

### Traçabilité & Monitoring (jan – mars 2026)

- **Créateur d'un écosystème de traçabilité complet** (trace-prod, trace-platform, trace-workflow + Aima-Tower) remplaçant un tableur artisanal par un système industriel à 13+ tables, daemon de sync et dashboard 5 pages temps réel.

- **Industrialisation de la traçabilité** : 7 commits en 2 semaines sur trace-prod (mars 2026) ajoutant complétude POD5/BAM, volumétrie, vérification croisée HCL, tolérance ghost S3, métadonnées ONT (freq, vaf, noms runs) — transformation en système d'audit qualité des données.

- **Détection et investigation des discordances de données** : identification automatique de barcodes BAM vs barcodes ONT incohérents, métadonnées manquantes (18 samples NANO15_26), POD5 absents — rigueur de vérification qui protège l'intégrité des résultats cliniques.

### R&D & Innovation (fév – mars 2026)

- **Concepteur du pipeline IA de détection ctDNA** : pipeline ML end-to-end (data→features→modèle→inférence) atteignant AUC=1.0 sur tumeurs solides et évalué sur 438 biopsies liquides réelles (79% sensibilité VAF>5% CGFL), posant les bases du score diagnostique automatisé d'AIMA.

- **Campagne de re-basecalling CGFL menée à terme** : 114/114 échantillons convertis de V4.3.0 vers V5.0.0 via Pod2Bam GPU (mars 2026), avec optimisation multiplex sur 2 instances GPU parallèles + 49/49 HCL V4.3.0 — harmonisation complète de la cohorte pour éliminer le batch effect.

- **Intégrateur du pipeline ichorCNA** (estimation fraction tumorale par CNV) : implémentation du workflow hmmcopy_utils→ichorCNA→score TF, objectif calcul rétrospectif sur 1000 échantillons — élargissement de l'arsenal diagnostique au-delà de la méthylation.

- **Concepteur du benchmark short-read** comparant 4 pipelines Illumina (5base Dragen, Watchmaker Dragen/nf-core/nf-Aima) avec comparaison IGV des calls de méthylation ONT vs Illumina — positionnement AIMA sur la double technologie.

- **Création d'une fonction de conversion BAM Illumina→ONT** : pont technique entre les deux technologies de séquençage, permettant la comparaison directe des calls de méthylation.

### Production & Opérations (sept 2025 – mars 2026)

- **Responsable du traitement de 700+ échantillons patients** (188 HCL + 519 CGFL) — chaque résultat clinique, chaque dossier investisseur, chaque contrat partenaire s'appuie sur ces données.

- **Libération de 38 To de stockage S3** (mars 2026) par nettoyage systématique (BAM horaires, doublons, POD5 legacy) — création de procédures de clean reproductibles, maîtrise des coûts cloud.

- **Rigueur de production industrielle** : SampleSheetChecker (ajout support --type=pod5), 8+ scénarios non-conformité, Tower QC (onglet non-conformités + backlog suivi), workflow qualification (QUALIF vs DEV sur S3).

### Positionnement & Organisation

- **Seul membre de l'équipe opérant simultanément sur les 3 axes** R&D, Production et Plateforme Client — nœud central connectant Florian (modèles), Fred (web), Romain/Léa (wet lab) et Michael (stratégie).

- **Facteur bloquant pour l'ensemble de l'équipe** : Florian attend bedMethyl pour modéliser, Fred attend JSON pour la plateforme, Romain attend le traitement de ses samples, Michael s'appuie sur les résultats pour les dossiers cliniques.

- **Initiateur du projet "IA for IA"** avec Fred : prompt engineering pour automatiser les processus internes — phases 1+2 terminées (mars 2026), démontrant la capacité à combiner bioinformatique et IA générative.

- **Promoteur de l'outillage IA interne** : POC "Claude Code >>> Cursor", auto-formation, démo avec Fred, adoption poussée au sein de l'équipe + alerte sécurité données ("sécuriser que Claude ne puisse supprimer/modifier des données").

- **Profil FinOps actif** : jobs d'extinction auto, estimations coûts/temps pod5 (849 samples = 72 jours GPU), analyse setups disponibles, coordination avec Fred sur lifecycle S3 (128 To→40 To).

- **Autonomie d'exécution avec alignement stratégique** : propose des solutions puis les exécute de bout en bout, avec points mensuels Michael et plans d'attaque concertés.

- **Bus factor = 1** sur l'ensemble du stack bioinformatique : risque pour AIMA, mais preuve d'une charge technique justifiant 2-3 personnes.

### Livraisons mars-avril 2026 (ajout 2026-04-20)

- **Pivot Aima-Tower vers outil ISO 15189 opérationnel** (14/04/2026) : page `/qualite` dédiée à la qualité pipeline avec drift plot, snapshots JSONL versionnés, rapport HTML imprimable signé SHA-256, onglet ML Details, onglet Confrontation CGFL vs HCL — transformation stratégique d'un dashboard exploration en support de certification.

- **Réimplémentation Python de run_pipeline.R (ExploratoryAnalysisService)** : phases 1-3 terminées, 28/28 tests cross-validés R ↔ pandas, sortie de la dépendance R pour la consommation Dash → fiabilité et performance du dashboard.

- **Aima-Survey v2** (ex-veille-scientifique) : renommage, push GitHub, scoring Claude Haiku 4.5, dédup SQLite, cron daily + hebdo, intégration Aima-Tower — veille scientifique industrialisée.

- **Outillage IA interne étendu** : création des skills `/audit-trail`, `/compare-batches`, `/correlation`, `/qc-report`, `/batch-effect` (5 nouveaux skills bioinformatiques), industrialisation du workflow d'investigation.

- **Investigation ComBat-Met menée à son terme** : projet complet créé, 4 variantes testées, conclusion argumentée de non-rétention pour production (documenté dans `batch-effect-investigation.md`) — protection ISO 15189 contre une correction statistique qui aurait été non auditable.

- **trace-workflow multi-workspace** (15/04) : ajout du workspace `aima-diagnostics` en plus de `community`, monitoring consolidé.

- **Prise en main du CLI Seqera** : intégration au sous-agent `/seqera`, automatisation des requêtes Tower.

## Données sources

- `~/boris_notes_extract.txt` — 75 entrées daily standup (sept 2025 – mars 2026)
- `~/Notes_Team_Meetings.txt` + `~/Notes_Team_Meetings (1).txt` — Réunions équipe 2025-2026
- `~/Notes_Team_Meetings (2).txt` — Réunions équipe janv-mars 2026 (source ajoutée 20/03/2026)
- `~/Pipeline/` — 24 projets analysés (code, README, configs, git logs) — état 2026-04-20
- `~/.claude/projects/*/memory/` — Mémoires projets Pipeline (IA, Pod2Bam, trace-prod, Bam2Beta, short-read, SampleSheetChecker)
- `~/.claude/projects/-home-blipinski/memory/todo-optimisation.md` — chantiers mars-avril 2026
