---
name: feedback-claude-usage
description: Journal des feedbacks et incidents Boris qui informent comment Claude doit travailler avec lui — règles validées par retour terrain
metadata: 
  node_type: memory
  type: feedback
  last_review: 2026-05-22
  originSessionId: 7d9cb6a0-df59-414e-ac5a-c61c6bcfd944
---

# Feedback & incidents — Boris Blipinski

> Journal append-only des règles validées par retour terrain. Chaque entrée = règle, **Why** (incident ou décision stratégique), **How to apply** (quand/où).
> Ordre chronologique inverse (plus récent en haut).
> Entrées obsolètes : ne **jamais** supprimer (traçabilité décisions). Marquer en première ligne du corps `> [OBSOLETE depuis YYYY-MM-DD — voir [[autre-règle]]]`.

## 2026-05-22 — Routing Session Start par intent (quick par défaut)

**Règle :** Au Session Start, lancer `agent-explore-quick` (Haiku, ~30s) en background pour tout intent exploration/question/debug/status. Lancer `agent-explore` (Sonnet, deep) **uniquement** pour les intents implémentation/refactor, en parallèle du quick (jamais seul).

**Why :** L'audit 2026-05-22 a montré que sur 250 invocations Pipeline sur 114j, ~80 % sont des questions où la doc chargée (CLAUDE.md, MEMORY.md, rules) suffit. La règle historique « toujours deep » (feedback 2026-04-13) coûtait Sonnet (5-15 min, ~50-100k tokens) pour des tâches Haiku-suffisantes. Économie ~85 % sur l'exploration auto. Remplace explicitement l'ancienne règle.

**How to apply :** Voir routing détaillé dans `~/.claude/CLAUDE.md` §Session Start. Le skill `/explore-projet` est le raccourci manuel pour relancer le quick à tout moment.

## 2026-04-21 — `.env` Aima-Tower tracked dans git

**Règle :** Avant tout `git init` ou `git add` initial sur un nouveau projet, vérifier que `.env`, `*.env*`, `*credentials*`, `*token*` sont dans `.gitignore`. Si un secret a déjà été commité (même dans un repo privé), le révoquer et le régénérer — la suppression du fichier ne suffit pas (historique git le conserve).

**Why :** Le `.env` d'Aima-Tower contenant `ANTHROPIC_API_KEY` + `accessToken` Seqera a été tracked dans git jusqu'au 2026-04-21 (poussé sur `aima-dx/Aima-Tower`, repo privé). Détection a posteriori via audit Boris. Pattern qui peut se reproduire sur tout nouveau projet AIMA.

**How to apply :** À l'init de tout nouveau projet Pipeline. Voir aussi [[s3-safety]] et `~/.claude/rules/secrets.md`. Rotation des secrets et contexte complet : `~/.claude/projects/-home-blipinski-Pipeline-Aima-Tower/memory/project_env_leak.md`.

## 2026-04 — ComBat-Met rejeté en production (ISO 15189)

**Règle :** Pour les corrections statistiques appliquées aux features cliniques de Bam2Beta (notamment correction batch effect), privilégier les méthodes auditables et explicables. Refuser les corrections opaques même si elles améliorent les métriques.

**Why :** ComBat-Met (variante ComBat pour méthylation) a été investiguée à fond en mars-avril 2026 : 4 variantes testées, projet dédié créé, conclusion documentée. Rejetée pour la production car non auditable au sens ISO 15189 — impossible d'expliquer le détail de la transformation à un évaluateur. Documenté dans `batch-effect-investigation.md`.

**How to apply :** Sur tout projet `Bam2Beta` ou pipeline R&D destiné à passer en production clinique. Préférer features brutes + modèle interprétable (SHAP, importance). Vaut aussi pour la future correction batch CGFL vs HCL — explorer ComBat seulement en R&D exploratoire, pas en production.

## Avant 2026-04 — Pas de 2 jobs GPU Dorado simultanés

**Règle :** Ne **jamais** lancer 2 jobs Dorado basecall en parallèle sur le même GPU (ni sur 2 GPUs de la même machine si shared memory). Le batch size auto-réduit silencieusement, les reads sont tronqués.

**Why :** Incident historique Pod2Bam : 2 basecalls lancés en parallèle ont produit des résultats tronqués (reads coupés ~90 bases plus courts qu'attendu). Documenté dans `~/.claude/rules/troubleshooting.md` section Pod2Bam.

**How to apply :** Sur tout job Dorado dans `~/Pipeline/Pod2Bam/` ou wrapper basecall. Exécution **séquentielle obligatoire**. Pour multiplex GPU, utiliser 2 instances physiques distinctes (cf. campagne re-basecalling CGFL 114/114 mars 2026).

## Avant 2026-04 — `aws s3 sync` skip silencieux

**Règle :** Après tout `aws s3 sync` avec le profil `scw`, vérifier `local_count == s3_count` et **retry en boucle** jusqu'à égalité. Le sync skip silencieusement 3-5 fichiers sur 23-90 de manière aléatoire (bug Scaleway S3).

**Why :** Pattern observé répétitivement en production AIMA : sync incomplet sans aucune erreur en sortie, détecté uniquement par comptage explicite. Documenté dans `~/.claude/rules/s3-safety.md` règle 5 et `~/.claude/rules/troubleshooting.md`.

**How to apply :** Wrapper systématique pour tout sync S3 ↔ Scaleway. Encapsuler dans `tmux` si run long (voir `~/.claude/CLAUDE.md` §Préférences opérationnelles). Ne jamais considérer un sync comme terminé sans vérification de comptage.

## Avant 2026-04 — Bash `((COMPLETED++))` crash avec `set -e`

**Règle :** Dans tout script Bash avec `set -e`, ne **jamais** utiliser `((COMPLETED++))` quand la variable peut valoir 0. Préférer `COMPLETED=$((COMPLETED + 1))`.

**Why :** En Bash, `((0++))` évalue à `false` (renvoie l'ancienne valeur 0), ce qui déclenche un exit immédiat sous `set -e`. Bug subtil découvert dans Pod2Bam — le script s'arrêtait silencieusement au premier incrément depuis 0.

**How to apply :** Dans tous les scripts shell de Pipeline (Pod2Bam, Bam2Beta, SampleSheetChecker, etc.). Documenté dans `~/.claude/rules/troubleshooting.md` section Pod2Bam.
