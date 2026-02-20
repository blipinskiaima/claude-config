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
| Anti-laziness on Claude 4.6 | Model is already proactive, causes runaway execution | Remove "be thorough" / "do not be lazy" prompts |
| Forcing tool use with aggressive language | Over-triggers on newer models | Use "when it would be helpful" instead of "you MUST use" |
| Compound multi-task sentences | Later tasks get ignored or partially executed | One instruction per sentence, numbered if sequential |
| Copy-pasting from older model guides | Techniques that helped GPT-3.5 may hurt GPT-5.2 / Claude 4.6 | Use model-specific best practices for current generation |
| Excessive examples (>5) | Causes overfitting, model mimics examples too literally | Use 2-3 varied examples covering different cases |
| Bribes ("I'll tip you $100") | No proven improvement, wastes tokens | Clear instructions produce better results than incentives |
| Repeating the same instruction 3 times | Wastes context, doesn't improve adherence | State once clearly, optionally remind at end of long prompts |
