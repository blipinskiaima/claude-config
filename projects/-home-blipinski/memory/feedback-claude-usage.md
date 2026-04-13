---
name: Feedback utilisation Claude Code
description: Retours d'expérience sur l'utilisation de Claude Code — ce qui fonctionne, ce qui ne fonctionne pas, préférences validées
type: feedback
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
## Communication

- Toujours répondre en français, code en anglais.
- Expliquer avec des schémas/diagrammes ASCII avant d'implémenter.
- Pas de résumés en fin de réponse (Boris lit le diff).

**Why:** Boris veut comprendre avant d'agir. Les explications abstraites ne l'aident pas.
**How to apply:** Chaque explication technique complexe (ML, stats, architecture) doit inclure un schéma visuel.

## Délégation

- Ne jamais remplacer l'expertise de Boris sur les pipelines cliniques — optimiser seulement.
- Pour Aima-Tower et outils internes : full autonomie Claude acceptée.

**Why:** Norme ISO 15189 — Boris doit pouvoir expliquer et défendre chaque ligne de code des pipelines cliniques.
**How to apply:** Sur Bam2Beta/Pod2Bam, proposer des changements et expliquer, ne pas implémenter directement les modifications structurelles.

## Session Start

- Toujours lancer une exploration DEEP (agent-explore) au démarrage, jamais quick.

**Why:** Boris lance souvent des sessions cross-projet et a besoin du contexte complet dès le départ.
**How to apply:** Utiliser agent-explore (pas agent-explore-quick) en background au premier message.

## Sécurité données

- Ne JAMAIS supprimer ou écraser des données S3/POD5 — voir ~/.claude/rules/s3-safety.md
- Inquiétude sécurité secrets : 6/10 — progression step by step souhaitée.

**Why:** Bus factor = 1, données irremplaçables, contexte clinique.
**How to apply:** Toujours vérifier avant toute opération sur des fichiers de données. Les golden rules S3 sont non négociables.
