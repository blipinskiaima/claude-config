# Anthropic Best Practices (Claude Sonnet 4.6 / Opus 4.7)

Techniques et recommandations spécifiques aux modèles Claude actuels (mai 2026).

Source primaire : [docs.anthropic.com — Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

## Modèles actuels (mai 2026)

| Modèle | API ID | Cas d'usage |
|---|---|---|
| Claude Opus 4.7 | `claude-opus-4-7` | Coding et agentic — raisonnement complexe |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Speed + intelligence (équilibre) |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Vitesse maximale |

Legacy disponibles mais en dépréciation : Opus 4.6, Sonnet 4.5, Opus 4.5, Opus 4.1. Sonnet 4 et Opus 4 sont **deprecated** (retraite 2026-06-15).

## Adaptive Thinking (remplace Extended Thinking)

`thinking.type: "enabled"` avec `budget_tokens` est **déprécié** sur Opus 4.6 / Sonnet 4.6 et **supprimé** sur Opus 4.7 (retourne erreur 400).

```python
# Déprécié
thinking={"type": "enabled", "budget_tokens": 32000}

# Actuel
thinking={"type": "adaptive"}
output_config={"effort": "high"}
```

Valeurs `effort` (officielles) :

| Valeur | Comportement | Disponibilité |
|---|---|---|
| `max` | Pas de contrainte sur la profondeur | Sonnet 4.6, Opus 4.6, Opus 4.7 |
| `xhigh` | Exploration étendue | **Opus 4.7 uniquement** |
| `high` (défaut) | Raisonnement profond sur tâches complexes | Tous |
| `medium` | Pensée modérée, skip sur queries simples | Tous |
| `low` | Pensée minimale, priorité vitesse | Tous |

## XML Tags First-Class

Claude excelle avec les prompts XML-structurés. Tags recommandés :

```xml
<context>...</context>
<task>...</task>
<rules>...</rules>
<examples>...</examples>
<output_format>...</output_format>
<thinking>...</thinking>
<answer>...</answer>
```

**Bénéfice documenté** : queries placées en fin de prompt = jusqu'à **+30% sur tâches complexes multi-documents** (citation officielle docs.anthropic.com).

## Context Motivation

Expliquer le POURQUOI d'une règle fonctionne mieux que la règle seule.

```
# Pas optimal
Ne jamais utiliser d'ellipses.

# Optimal
Ne jamais utiliser d'ellipses car la sortie sera lue par un moteur TTS
qui ne sait pas les prononcer.
```

## Plus de prefilled responses (Claude 4.6+)

Sur Claude 4.6+, le prefill du dernier message assistant retourne **erreur 400** : `"Prefilling assistant messages is not supported for this model."`

Alternatives :
- Instructions directes : "Respond directly without preamble."
- Structured Outputs pour le format
- Tool calling pour la sortie contrainte

## Opus 4.7 — Literalisme strict

Opus 4.7 interprète les prompts **plus littéralement** qu'Opus 4.6, surtout à `effort` bas. Le modèle ne généralise pas silencieusement.

```
# Ambigu sur Opus 4.7
Use this formatting style.

# Explicite (recommandé Opus 4.7)
Apply this formatting to every section, not just the first one.
```

Citation officielle : *"It will not silently generalize an instruction from one item to another, and it will not infer requests you didn't make."*

## Anti-laziness — Softening obligatoire

Claude 4.6+ est déjà proactif. Les instructions agressives causent **overtriggering**.

```
# Anti-pattern Claude 4.6+
CRITICAL: You MUST use the search tool every time...
Be thorough and use all available tools aggressively.

# Pattern correct
Use the search tool when it would enhance understanding.
```

Citation officielle : *"Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'"*

## Parallel Tool Calling

Claude 4.x excelle en parallel tool calling natif. Snippet officiel pour booster à ~100% :

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel.
Maximize use of parallel tool calls where possible to increase speed and efficiency.
Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

## Subagent Spawning Policy

Contrôler quand le modèle doit spawner des sous-agents. La syntaxe n'est pas un tag XML standardisé, c'est du texte libre dans le system prompt :

```
Spawn multiple subagents in the same turn when fanning out across independent items or reading multiple files.

Do NOT spawn a subagent for work you can complete directly in a single response (e.g., refactoring a function you can already see).
```

Source officielle : section "Controlling subagent spawning" des docs.

## Output Formatting

- Dire CE QU'IL FAUT FAIRE plutôt que ce qu'il NE FAUT PAS FAIRE (positif > négatif)
- Utiliser des indicateurs XML pour les sections de sortie
- Faire matcher le style du prompt avec celui de la sortie

## Vision

Donner un outil de crop/zoom pour l'analyse d'images — uplift mesuré et constant sur les évaluations d'images (recommandation officielle).
