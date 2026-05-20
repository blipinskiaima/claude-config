---
name: audit-config
description: Audit complet de la configuration Claude Code de Boris — identifie les skills/agents/MCP/rules/hooks utilisés vs dormants sur les 30 derniers jours, propose un plan de cleanup en 3 commits. Use when the user says "audit-config", "audit claude config", "tri configuration claude", "cleanup claude", "fais le tri dans ma config", or wants to optimize/cleanup his ~/.claude/ setup.
---

# Skill : Audit Config Claude

Produit un audit fresh de `~/.claude/` (skills/agents/MCP/rules/hooks/plugins) en croisant l'état du repo `claude-config` avec l'activité réelle sur les 30 derniers jours.

## Sources à charger (obligatoire, dans cet ordre)

1. **Audit précédent** : dernier fichier `~/.claude/projects/-home-blipinski/memory/audit-claude-code-*.md`
2. **Inventaire** : `~/.claude/projects/-home-blipinski/memory/inventaire-claude-code.md`
3. **Feedback** : `~/.claude/projects/-home-blipinski/memory/feedback-claude-usage.md`
4. **Todo** : `~/.claude/projects/-home-blipinski/memory/todo-optimisation.md`
5. **Transcripts récents** :
   ```bash
   touch -d "$(stat -c %y ~/.claude/projects/-home-blipinski/memory/audit-claude-code-*.md | sort | tail -1 | cut -d' ' -f1)" /tmp/marker-prev-audit
   find ~/.claude/projects -name '*.jsonl' -newer /tmp/marker-prev-audit
   ```
6. **Structure actuelle** :
   ```bash
   ls ~/.claude/skills/
   ls ~/.claude/agents/
   claude mcp list
   cat ~/.claude/settings.json | python3 -c "import json,sys; s=json.load(sys.stdin); print('hooks:', list(s.get('hooks',{}).keys()))"
   ```

## Méthodologie (5 phases)

### Phase 1 — Charger l'existant
- Réutiliser le précédent audit, **NE PAS** le re-générer
- Établir l'état de référence (compteurs d'invocation par skill/agent/MCP)
- Identifier ce qui a déjà été traité (todo `Complété` + `git log` de `~/.claude/`)

### Phase 2 — Delta depuis le précédent audit
- Analyser uniquement la fenêtre temporelle depuis le précédent audit
- Pour chaque transcript nouveau, extraire (via `jq` / Python) :
  - Skills invoquées (`tool_use` avec `name: Skill`)
  - Subagents invoqués (`subagent_type`)
  - MCP tools appelés (`name: mcp__*`)
  - Bash commands fréquentes (top 20)
  - Frictions verbatim Boris (`non`, `stop`, `pas ça`)
- Comparer aux compteurs précédents

### Phase 3 — Catégoriser
Pour chaque artefact, assigner une catégorie :

| Catégorie | Critère | Action |
|---|---|---|
| **GARDER** | Invoqué ≥ 1× sur la fenêtre ET frontmatter correct | Rien |
| **MODIFIER** | Invoqué mais description/nom/scope mal calibré | Edit |
| **OPTIMISER** | Invoqué mais structure améliorable | Refactor |
| **SUPPRIMER** | 0 invoc sur la fenêtre + pas d'usage métier stratégique | `git rm` |
| **GARDER (alerte)** | 0 invoc mais métier ISO 15189 / golden rule | Garder + flag |
| **CRÉER** | Pattern ≥ 5× sans skill ou friction ≥ 2× | Nouveau skill |

### Phase 4 — Nouveaux skills
Maximum **5** propositions, chacune justifiée par :
- Pattern observé ≥ 5× dans transcripts
- OU friction verbatim Boris ≥ 2×
- OU besoin métier explicite (ISO 15189, batch effect, méthylation, Tower)

### Phase 5 — Plan d'action
**3 commits séquentiels** (pas de PR — auto-push hook):
1. **Cleanup** : `git rm` des SUPPRIMER + retrait MCP redondants
2. **Optimisations** : Edit descriptions, path-scope rules, extend hooks
3. **Nouveaux skills** : `mkdir + SKILL.md` pour chaque CRÉER

Chaque commit doit fournir :
- Commande shell exacte (copy-paste)
- Validation post-commit (`ls`, `git log`, test)

## Règles non négociables

- **NE JAMAIS** exécuter directement — produire le plan, faire la revue itérative avec Boris d'abord
- **NE JAMAIS** supprimer les golden rules (`s3-safety`, `secrets`, `nextflow`, `duckdb`)
- **NE JAMAIS** supprimer les skills sans validation explicite Boris si frontmatter cassé (peut être réparable)
- Citer file:line ou URL pour chaque claim factuelle
- Limiter à 5 nouveaux skills max
- Plafonner à 3 commits (pas de scope creep)

## Output

Rapport markdown en 6 sections :
1. **Synthèse exécutive** (10 lignes max)
2. **État des lieux post-delta** (tableau par artefact)
3. **Commit 1 — Cleanup**
4. **Commit 2 — Optimisations**
5. **Commit 3 — Nouveaux skills**
6. **Hors scope** (items du précédent audit non traités + raison)

## Workflow après production du rapport

1. Présenter chaque skill/agent un par un à Boris pour validation (Garder/Modifier/Supprimer)
2. Exécuter les 3 commits en séquence après validation complète
3. Mettre à jour `inventaire-claude-code.md` + créer le nouveau `audit-claude-code-YYYY-MM-DD.md`

## Référence

- Audit type : `~/.claude/projects/-home-blipinski/memory/audit-claude-code-2026-05-09.md`
- Skill `/prompt-creator` peut produire un system prompt complet pour cet audit si besoin
- Skill `/meta-skills-creator` pour optimiser les skills identifiés à améliorer
