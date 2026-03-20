# Memory — Boris Blipinski (Home)

## Profil professionnel

Boris = Bioinformaticien chez AIMA Diagnostics (diagnostic cancer, méthylation ADN, ONT + Illumina). Auteur unique de 13 projets dans `~/Pipeline/`. Seul membre opérant simultanément sur R&D, Production et Plateforme Client.

## Analyse de valeur (session mars 2026)

Analyse complète réalisée le 04/03/2026 à partir de :
- 75 entrées daily standup (sept 2025 – mars 2026)
- Notes réunions d'équipe 2025 + 2026
- 13 projets Pipeline (code, README, configs)

### Réalisations clés identifiées
- Pipeline Bam2Beta from scratch (34 processus NF, V1.0.1, 700+ samples, corrélation 98.4% Katsman)
- Migration AWS→Scaleway complète (déc 2025, 15TB nettoyés, 3 semaines)
- Système traçabilité complet : trace-prod + trace-platform + trace-workflow + Aima-Tower
- Setup terrain HCL (upload P24, cron+log+alerte)
- Pod2Bam GPU multi-version (V4.2.0→V5.2.0, reproductibilité confirmée)
- Benchmark short-read 4 pipelines (5base, Watchmaker x3)
- 700+ samples traités (188 HCL + 519 CGFL)

### Positionnement équipe
- Boris = nœud central connectant tous les pôles (Florian/R&D, Fred/Platform, Romain-Léa/PROD, Michael/CTO)
- Bloquant pour tous : Florian attend bedMethyl, Fred attend JSON, Romain attend traitement
- Bus factor = 1 sur tout le stack bioinformatique

### Fichier détaillé
Voir [aima-value-analysis.md](aima-value-analysis.md) pour le document complet.

## Patterns de travail avec Boris

- Préfère le français pour les conversations
- Apprécie les analyses factuelles avec preuves (dates, versions, métriques)
- Travaille souvent le weekend (lancements basecalling vendredi soir→lundi matin)
- Promoteur d'outils IA (Claude Code > Cursor)
- Approche : autonomie d'exécution + alignement stratégique régulier
