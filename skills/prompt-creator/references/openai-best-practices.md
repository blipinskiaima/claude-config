# OpenAI Best Practices (GPT-5.x / o-series, juillet 2026)

Techniques pour les modèles OpenAI actuels.

Sources primaires (revérifiées juillet 2026) :
- [GPT-5.2 Prompting Guide — Cookbook](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide) (déc. 2025)
- [GPT-5.1 Prompting Guide — Cookbook](https://cookbook.openai.com/examples/gpt-5/gpt-5-1_prompting_guide)
- [Reasoning models — OpenAI API](https://developers.openai.com/api/docs/guides/reasoning)
- [Prompt engineering — OpenAI API](https://developers.openai.com/api/docs/guides/prompt-engineering)

## Modèles actuels

| Modèle | Type | Note |
|---|---|---|
| **GPT-5.2** | Reasoning | Guide de prompting officiel le plus récent trouvé (déc. 2025) — les valeurs chiffrées de cette page en proviennent |
| GPT-5.1 / GPT-5 | Reasoning | Guides officiels disponibles |
| **o3 / o4-mini** | Reasoning | Raisonnement interne natif |
| GPT-5.5 / 5.4 | Standard | ⚠️ Mentionnés dans une version antérieure de ce skill mais **non retrouvés dans la doc officielle** en juillet 2026. Vérifier avant de s'appuyer dessus |

**Le prompting diffère fondamentalement** selon le type (standard vs reasoning). Lire les deux sections.

---

## Modèles standard (GPT-4o et modèles sans raisonnement natif)

### CTCO Pattern

Structure couramment citée pour les prompts GPT :
- **Context** : qui est le modèle, état de fond
- **Task** : action atomique unique
- **Constraints** : limites, scope
- **Output** : format exact attendu

⚠️ **Non confirmé dans le cookbook officiel OpenAI** (vérification juillet 2026) — l'acronyme provient de sources
secondaires. Le fond (contexte + tâche + contraintes + format) est bien la recommandation officielle ; c'est
l'étiquette « CTCO » qui n'est pas sourcée. Ne pas la présenter comme un standard OpenAI.

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

Sur GPT-5.2 : `reasoning_effort` défaut = `none` (contre `minimal` sur GPT-5). Table de migration officielle :

| Départ | Cible GPT-5.2 |
|---|---|
| GPT-4o / 4.1 | `none` |
| GPT-5 | garder l'effort existant, sauf `minimal` → `none` |
| GPT-5.1 | garder, n'ajuster qu'après evals |

**`reasoning_effort` est un bouton de réglage, pas un rattrapage de qualité** — citation officielle : *"Treat
`reasoning.effort` as a tuning knob, not the primary way to recover quality"*. Un mauvais prompt ne se compense pas
en montant l'effort.

### Contraintes de longueur explicites

GPT-5.2 formalise la consigne de concision plus que les autres éditeurs — valeurs de référence officielles :
*"Default: 3–6 sentences or ≤5 bullets for typical answers"*, *"For simple yes/no questions: ≤2 sentences"*,
*"Avoid long narrative paragraphs; prefer compact bullets"*. Reprendre ces bornes chiffrées plutôt qu'un « sois
concis » subjectif.

### Extraction : null plutôt que deviner

Consigne anti-hallucination officielle à intégrer dans tout prompt d'extraction structurée :
*"If a field is not present in the source, set it to null rather than guessing"*.

### Ambiguïté

*"If the question is ambiguous, explicitly call this out and ask 1-3 precise clarifying questions"* — borner le
nombre de questions évite le ping-pong de clarification.

### Agentique : narration minimale

*"Brief updates (1-2 sentences) only when starting new major work or discovering plan changes"*,
*"Avoid narrating routine tool calls"*. Même logique que le silence-par-défaut recommandé côté Claude.

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

## Modèles reasoning (o3, o4-mini, GPT-5.x)

**Règles fondamentalement différentes** des modèles standard.

Règle-cadre officielle : *"Give the model the task, constraints, and desired output format"* **sans** prescrire
chaque étape intermédiaire. C'est l'inverse exact de la doctrine 2024 pour GPT-4, où l'énumération pas-à-pas
aidait. Sur un modèle à raisonnement, elle ajoute du bruit.

À noter aussi : le few-shot chain-of-thought *"no longer improves reasoning in newer models, with their only
remaining function being format alignment"* — garder les exemples pour cadrer le **format**, pas pour enseigner le
raisonnement.

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
