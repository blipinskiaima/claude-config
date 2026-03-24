# Memory — Boris Blipinski (Home)

## Profil professionnel

Boris = Bioinformaticien chez AIMA Diagnostics (diagnostic cancer, méthylation ADN, ONT + Illumina). Auteur unique de 16 projets dans `~/Pipeline/`. Seul membre opérant simultanément sur R&D, Production et Plateforme Client.

## Analyse de valeur (mise à jour 20/03/2026)

Analyses réalisées le 04/03/2026 puis mise à jour 20/03/2026 à partir de :
- 75 entrées daily standup (sept 2025 – mars 2026)
- Notes réunions d'équipe 2025 + 2026 (3 fichiers)
- 16 projets Pipeline (code, README, configs, git logs)
- Mémoires projets Claude (IA, Pod2Bam, trace-prod, Bam2Beta, short-read)

### Réalisations clés identifiées
- Pipeline Bam2Beta from scratch (34 processus NF, V1.0.2, 700+ samples, corrélation 98.4% Katsman)
- Pipeline IA ctDNA Detection (ML end-to-end, AUC=1.0 solide, 438 cfDNA évalués, 79% sens VAF>5%)
- Migration AWS→Scaleway complète (déc 2025, 15TB nettoyés, 3 semaines)
- Système traçabilité complet : trace-prod + trace-platform + trace-workflow + Aima-Tower
- Setup terrain HCL (upload P24, cron+log+alerte)
- Pod2Bam GPU multi-version : 114/114 CGFL + 49/49 HCL convertis (batch effect éliminé)
- Benchmark short-read 4 pipelines (5base, Watchmaker x3) + comparaison IGV ONT/Illumina
- ichorCNA pipeline en cours d'intégration (0/1000, mars 2026)
- 38 To libérés par nettoyage S3 systématique (mars 2026)
- IA for IA avec Fred : phases 1+2 terminées (mars 2026)
- 700+ samples traités (188 HCL + 519 CGFL)

### Positionnement équipe
- Boris = nœud central connectant tous les pôles (Florian/R&D, Fred/Platform, Romain-Léa/PROD, Michael/CTO)
- Bloquant pour tous : Florian attend bedMethyl, Fred attend JSON, Romain attend traitement
- Bus factor = 1 sur tout le stack bioinformatique

### Fichier détaillé
Voir [aima-value-analysis.md](aima-value-analysis.md) pour les bullet points complets (21 points).

## Patterns de travail avec Boris

- Préfère le français pour les conversations
- Apprécie les analyses factuelles avec preuves (dates, versions, métriques)
- Travaille souvent le weekend (lancements basecalling vendredi soir→lundi matin)
- Promoteur d'outils IA (Claude Code > Cursor)
- Approche : autonomie d'exécution + alignement stratégique régulier
- Sensible à la sécurité des données (alerte "Claude ne doit pas supprimer/modifier des données")
