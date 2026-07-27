# Anti-Patterns

Common prompting mistakes to avoid. These waste tokens, confuse models, or produce worse results.

| Anti-Pattern | Why It Fails | Do This Instead |
|---|---|---|
| ALL CAPS THREATS | Creates adversarial dynamic, rarely improves output | Use clear, calm instructions |
| "You MUST..." on every rule | Dilutes emphasis when everything is urgent | Reserve strong emphasis for truly critical rules |
| Negative examples ("don't do this") | Model may learn the wrong behavior | Show only positive examples of desired output |
| "Think step by step" on reasoning models | Redundant on o-series/Claude extended thinking, causes over-thinking | State the problem clearly, let built-in reasoning work |
| JSON for wrapping long documents | Performance degrades vs XML/markdown (OpenAI research) | Use XML tags or markdown for document context |
| Vague length constraints ("be concise") | Subjective, produces inconsistent results | Use concrete limits ("max 5 bullets, each under 15 words") |
| Over-specifying trivial decisions | Wastes context, limits flexibility | Constrain only what matters for output quality |
| Anti-laziness on Claude 4.6+ / famille 5 | Model is already proactive, causes runaway execution and overtriggering | Remove "be thorough" / "do not be lazy" / "CRITICAL" prompts. Use plain phrasing |
| "Double-check your answer" / étape de vérification sur Claude Opus 5 | Le modèle se vérifie déjà seul → sur-vérification, coût et latence en pure perte | **Supprimer** l'instruction et l'étape de harness. Inversion assumée d'une best practice standard |
| "Delegate to subagents when possible" sur Claude Opus 5 | Consigne écrite pour Opus 4.8 qui sous-déléguait ; Opus 5 sur-délègue, ×coût et ×latence | Retirer la consigne et poser un plafond explicite sur le nombre de sous-agents |
| "Only report high-severity issues" en code review (Claude 5) | Suivi littéralement : les bugs sont trouvés puis tus → recall mesuré en baisse | Demander une couverture exhaustive avec confiance + sévérité, filtrer en aval |
| Baisser `effort` pour raccourcir la réponse (Claude Opus 5) | `effort` déplace le volume de thinking, pas la longueur du texte rendu | Instruction de concision explicite dans le prompt |
| `budget_tokens` / `temperature` / `top_p` / prefill assistant sur la famille Claude 5 | Tous supprimés → erreur 400 | `effort` pour la profondeur, prompt pour le style, `output_config.format` pour le format |
| Prompts pas-à-pas très prescriptifs sur Claude Fable 5 | Dégradent activement la qualité de sortie | Énoncer le but et les contraintes, laisser le modèle choisir la démarche |
| Forcing tool use with aggressive language | Over-triggers on newer models | Use "when it would be helpful" instead of "you MUST use" |
| Compound multi-task sentences | Later tasks get ignored or partially executed | One instruction per sentence, numbered if sequential |
| Copy-pasting from older model guides | Techniques that helped GPT-3.5 may hurt GPT-5.x / Claude 4.6+ / o-series | Use model-specific best practices for current generation |
| Excessive examples (>5) | Causes overfitting, model mimics examples too literally | Use 2-3 varied examples covering different cases |
| Bribes ("I'll tip you $100") | No proven improvement, wastes tokens | Clear instructions produce better results than incentives |
| Repeating the same instruction 3 times | Wastes context, doesn't improve adherence | State once clearly, optionally remind at end of long prompts |
| String matching downstream sur format texte | Casse au moindre changement de phrasing, fragile | Utiliser Structured Outputs (JSON schema strict OpenAI, tool_use Anthropic, responseSchema Gemini) |
| Prompts prescriptifs pas-à-pas pour modèles reasoning (o3, o4-mini, Claude adaptive thinking) | Contraint le processus interne, peut dégrader le raisonnement | Décrire le résultat désiré, pas les étapes |
| "You are an expert in X" seul comme optimisation | Améliore l'alignement (tone, style) mais peut dégrader l'accuracy (paper PRISM, mars 2026) | Contexte riche + exemples > persona seule. Garder la persona pour le ton, pas pour la précision |
| Sur-emphasis CAPS / "CRITICAL" / "MUST" sur Claude 4.6+ | Overtriggering documenté officiellement (anti-laziness) | Instructions normales : "Use X when..." plutôt que "You MUST use X" |
