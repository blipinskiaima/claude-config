# OpenAI Best Practices (GPT-5.5 / o-series, mai 2026)

Techniques pour les modèles OpenAI actuels.

Sources primaires :
- [Reasoning best practices — OpenAI](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [GPT-5 Prompting Guide — Cookbook](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide)
- [Prompt caching — OpenAI](https://developers.openai.com/api/docs/guides/prompt-caching)

## Modèles actuels (mai 2026)

| Modèle | Type | Note |
|---|---|---|
| **GPT-5.5 Instant** | Standard | Modèle par défaut ChatGPT (sorti mai 2026) |
| GPT-5.5 / 5.4 / 5.2 | Standard | API |
| **o3 / o4-mini** | Reasoning | Raisonnement interne natif |

**Le prompting diffère fondamentalement** selon le type (standard vs reasoning). Lire les deux sections.

---

## Modèles standard (GPT-5.5, GPT-4o, GPT-5.x)

### CTCO Pattern

Structure éprouvée pour les prompts GPT :
- **Context** : qui est le modèle, état de fond
- **Task** : action atomique unique
- **Constraints** : limites, scope
- **Output** : format exact attendu

### Structure recommandée

```markdown
# Role and Objective
# Instructions
## Sub-categories for detail
# Reasoning Steps
# Output Format
# Examples
# Context
# Final instructions (reminder)
```

Markdown headings = délimiteur principal (vs XML pour Claude).

### Verbosity vs reasoning_effort

GPT-5.x expose **deux paramètres distincts** :

| Paramètre | Contrôle | Valeurs |
|---|---|---|
| `verbosity` | Longueur de la **réponse finale** | low / medium (défaut) / high |
| `reasoning_effort` | Profondeur du **raisonnement interne** | none / minimal / low / medium / high / xhigh |

```python
# Réponse courte mais raisonnement profond
{"verbosity": "low", "reasoning_effort": "high"}

# Réponse détaillée avec peu de raisonnement
{"verbosity": "high", "reasoning_effort": "minimal"}
```

Sur GPT-5.5 : `reasoning_effort` défaut = `none`. Sur GPT-5 original : défaut `medium`.

### Instruction Placement (long contexte)

Pour les prompts longs (> 10k tokens) : placer les instructions critiques au **DÉBUT ET FIN**. Si une seule option : début > fin.

### Prompt Caching (automatique)

Le caching est **automatique** pour les prompts ≥ 1024 tokens. Pour maximiser le cache hit :

```
[Contenu STATIQUE — début du prompt]   ← cache hit garanti
  - System prompt
  - Few-shot examples
  - Instructions générales

[Contenu VARIABLE — fin du prompt]      ← per-call
  - Données utilisateur
  - Question spécifique
```

Source officielle : *"Place static content like instructions and examples at the beginning of your prompt, and put variable content at the end."*

### Structured Outputs

`response_format` avec `strict: true` pour du JSON strict :

```python
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": "extraction",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {...},
            "required": [...]
        }
    }
}
```

Plus fiable que demander du JSON en plain text. Disponible sur GPT-4o et GPT-5.x.

---

## Modèles reasoning (o3, o4-mini)

**Règles fondamentalement différentes** des modèles standard.

### Developer message, PAS system message

```python
# Standard models (GPT-5.5, GPT-4o)
messages = [{"role": "system", "content": "..."}]

# Reasoning models (o3, o4-mini)
messages = [{"role": "developer", "content": "..."}]
```

Citation officielle : *"Developer messages are the new system messages for reasoning models."*

### Ne JAMAIS écrire "think step by step"

Les modèles reasoning raisonnent déjà en interne. L'instruction CoT manuelle est superflue et peut dégrader.

```
# Anti-pattern sur reasoning models
"Think step by step before answering..."
"Explain your reasoning..."

# Pattern correct
[Description claire et directe de la tâche]
[Format de sortie attendu]
```

Citation officielle : *"prompting them to 'think step by step' or 'explain your reasoning' is unnecessary."*

### Prompts COURTS et DIRECTS

| Standard models | Reasoning models |
|---|---|
| Instructions détaillées OK | Prompts courts |
| Few-shot utile | **Zero-shot first** |
| Explicit Chain-of-Thought | Ne PAS forcer CoT |
| Step-by-step prescriptif | Outcome-oriented |
| System message | Developer message |

### Few-shot RAREMENT utile

Recommandation officielle :
> *"Reasoning models often don't need few-shot examples. Try writing prompts WITHOUT examples first. If you have complex requirements for output format, include a few examples of inputs and desired outputs."*

### Reasoning items persistence (Responses API)

Préserver les reasoning items entre les tours pour réduire les tokens de raisonnement :

```python
response = client.responses.create(
    model="o3",
    messages=[...],
    store=True   # préserve les reasoning items
)
```

Citation officielle : *"The `store: true` parameter maintains state from turn to turn, preserving reasoning and tool context in the Responses API."*

---

## Patterns communs (standard + reasoning)

### Scope Discipline

```
No extra features, no added components, no UX embellishments beyond what was specified.
```

### Agentic Persistence

```
Keep working until the task is fully resolved.
Do not yield control until done or genuinely blocked.
```

### File Diff Format (pour les modifications de code)

GPT a été entraîné sur le format V4A diff. Utiliser : 3 lignes de contexte, opérateurs `@@`, **jamais de numéros de ligne**.
