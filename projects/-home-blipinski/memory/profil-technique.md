---
name: Profil technique Boris
description: Stack, compétences, workflow quotidien, préférences de développement — guide pour adapter les réponses Claude
type: user
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
## Compétences par niveau

| Niveau | Domaines |
|---|---|
| Expert | Nextflow DSL2 |
| Avancé | R, Bash, Docker, Plotly |
| Intermédiaire | Python, Git, Infrastructure |
| Débutant | ML/IA, Statistiques, Dash |

## Workflow quotidien

- 4-10h/jour avec Claude Code, 1-5 sessions parallèles
- 1 session = 1 projet dans ~/Pipeline/, terminal SSH dans Cursor IDE
- Exploration systématique du projet au démarrage de chaque session
- Parfois exploration cross-projet pour contexte (ex: lire trace-prod pour implémenter une feature dans Bam2Beta)

## Philosophie de délégation

Gradient basé sur la criticité réglementaire :
- **Pipelines cliniques (Bam2Beta, Pod2Bam)** : Boris garde le coeur, Claude optimise. ISO 15189 visé → maîtrise personnelle maximale.
- **Outils de traçabilité (trace-prod, trace-platform)** : base créée par Boris, features par Claude.
- **Outils internes (Aima-Tower)** : full Claude, pas de norme qualité.

Principe : "Claude optimise, ne remplace pas mon expertise."

## Préférences techniques

- Code en anglais, communication en français
- Comprendre AVANT d'implémenter — explications schématiques (flèches, diagrammes ASCII)
- Pas de théorie abstraite — concret et synthétique
- Proactivité attendue sur : veille sécurité, axes d'amélioration, ponts inter-projets
- Pas de proactivité sur l'exécution en production

## Frustrations identifiées (avril 2026)

1. Perte de contexte inter-sessions — re-exploration systématique
2. Sous-exploitation de l'IA pour le coeur de métier (détection ctDNA)
3. Pas de ponts inter-projets — les projets sont des silos pour Claude
