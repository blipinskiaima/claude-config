# Anthropic Best Practices (famille Claude 5)

Techniques et recommandations specifiques aux modeles Claude actuels (juillet 2026).

Source primaire : skill `claude-api` (fait foi sur les IDs, params et migrations) +
[docs.anthropic.com — Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

## Modeles actuels (juillet 2026)

| Modele | API ID | Contexte | $/1M in-out | Cas d'usage |
|---|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | 1M | 10 / 50 | Le plus capable en dispo generale — raisonnement le plus dur, agentic long-horizon |
| Claude Mythos 5 | `claude-mythos-5` | 1M | 10 / 50 | Identique a Fable 5, reserve Project Glasswing |
| Claude Opus 5 | `claude-opus-5` | 1M | 5 / 25 | **Le defaut**. Coding agentic, travail enterprise |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | 3 / 15 (intro 2 / 10 jusqu'au 31/08/2026) | Equilibre vitesse/intelligence, qualite quasi-Opus sur coding |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | 1 / 5 | Vitesse maximale, taches simples |

Sortie max : 128K partout sauf Haiku 4.5 (64K). Legacy encore actifs : Opus 4.8 / 4.7 / 4.6, Sonnet 4.6.
**Ne jamais suffixer une date** aux IDs ci-dessus (`claude-opus-5`, pas `claude-opus-5-2026xxxx`).

## Ce qui a change vs Claude 4.x — les params

| Param | Etat sur la famille 5 |
|---|---|
| `thinking: {type:"enabled", budget_tokens:N}` | **Supprime — erreur 400.** Aucun remplacant : la profondeur se pilote par `effort` |
| `thinking: {type:"adaptive"}` | Le seul mode. **Actif par defaut** si le champ est omis sur Opus 5 et Fable 5 (≠ 4.8/4.7 ou omettre = pas de thinking) |
| `thinking: {type:"disabled"}` | **400 sur Fable 5** (thinking toujours on). Sur Opus 5 : accepte uniquement a `effort` ≤ `high` — combine a `xhigh`/`max` c'est un 400 |
| `temperature` / `top_p` / `top_k` | **Supprimes — 400** sur Opus 5, Fable 5, Opus 4.8/4.7. Le pilotage du style passe par le prompt |
| Prefill du dernier message assistant | **400.** Utiliser `output_config.format` (structured outputs) ou une instruction systeme |
| `output_config.effort` | `low` / `medium` / `high` / `xhigh` / `max`. Defaut `high`. **Dans `output_config`**, pas au top-level |
| `thinking.display` | Defaut `"omitted"` → les blocs `thinking` arrivent avec un texte vide. Mettre `"summarized"` si tu affiches le raisonnement |

Consequence silencieuse a surveiller : **`max_tokens` plafonne thinking + reponse ensemble.** Une route qui tournait
sans thinking sur 4.8 et dimensionnait `max_tokens` au plus juste se fait tronquer en milieu de reponse sur Opus 5.

## Choisir le niveau d'effort

| Modele | Point de depart | Puis |
|---|---|---|
| Opus 5 | `xhigh` coding/agentic, `high` ailleurs | **Balayer vers le bas** — `low` et `medium` sont anormalement forts ici, souvent au niveau du `xhigh` des generations precedentes |
| Fable 5 | `high` | `xhigh` sur le capability-sensitive, `medium`/`low` sur le routinier |
| Sonnet 5 | `high` (defaut) | `xhigh` pour le coding/agentic le plus dur |

A `xhigh` ou `max`, **prevoir un gros `max_tokens`** (≥ 64K) : le modele a besoin de place pour penser et enchainer
les appels d'outils. Les valeurs d'effort heritees d'un modele precedent ne se transposent quasiment jamais — refaire
le balayage sur ses propres evals.

⚠️ **`effort` ne raccourcit pas la sortie visible sur Opus 5.** Baisser l'effort deplace le volume de thinking sans
reduire de facon fiable la longueur du texte rendu. Pour raccourcir, c'est le prompt (voir ci-dessous).

## Les inversions de best practice (le coeur de la mise a jour)

Ces cinq points **contredisent des conseils de prompting standard** et sont la principale source de degradation
quand on porte un prompt 4.x vers la famille 5.

### 1. Supprimer les instructions de verification

Opus 5 verifie son propre travail sans qu'on le lui demande. Les instructions type *"double-check your answer"*,
*"re-verify before responding"*, *"include a final verification step"* — ainsi que les etapes de verification
cablees dans le harness — provoquent desormais de la **sur-verification**. C'est une **suppression**, pas une
reecriture : la retirer reduit la sur-verification sans aucune regression de capacite.

C'est l'inversion la plus contre-intuitive : « demande au modele de se relire » reste un bon conseil general et
devient faux ici. Une bibliotheque de prompts qui l'applique uniformement a besoin d'une exception explicite.

### 2. Ne plus pousser a la delegation — la plafonner

Opus 4.8 sous-utilisait les sous-agents et demandait qu'on l'y encourage. **Opus 5 fait l'inverse** : il delegue
trop volontiers, ce qui multiplie cout et latence (chaque sous-agent reetablit son contexte, reexplore, rapporte,
puis le coordinateur relit le rapport). Retirer toute consigne « delegue davantage » heritee de 4.8 et poser un
plafond deterministe sur le nombre de sous-agents.

### 3. Les filtres de severite font chuter le recall mesure

Sur une revue de code, une consigne du type *"only report high-severity issues"* / *"be conservative"* /
*"don't nitpick"* est suivie **litteralement** : le modele trouve les bugs puis refuse de les remonter sous la barre
annoncee. La precision monte, le recall mesure baisse — alors que la capacite de detection a progresse.

Pattern correct : demander une **couverture exhaustive avec confiance + severite par finding**, et filtrer dans une
etape aval separee.

### 4. Verbosite : c'est le prompt, pas l'effort

Opus 5 ecrit des reponses plus longues par defaut, et des **fichiers plus longs sur disque** (rapports, documents
Markdown). Deux instructions distinctes a poser :

```
Keep responses focused, brief, and concise. Disclaimers and caveats are brief, with most
of the response on the main answer; when asked to explain something, give a high-level
summary unless an in-depth one is specifically requested.
```

```
Match the length of written deliverables (especially Markdown files) to what the task
needs: cover the substance, but do not pad documents with filler sections, redundant
summaries, or boilerplate.
```

Sur un long system prompt, doubler la premiere par un rappel `<tone_preference>` court en fin de prompt.

### 5. Prompts trop prescriptifs = qualite degradee sur Fable 5

Les prompts et skills ecrits pour les generations precedentes sont souvent **trop prescriptifs** pour Fable 5 et
**reduisent** la qualite de sortie. Enoncer le but et les contraintes plutot qu'enumerer les etapes. Apres migration,
faire un A/B en retirant le scaffolding pas-a-pas.

## Blocs de prompt qui marchent (famille 5)

### Discipline de scope

Opus 5 peut elargir la tache ou appliquer son propre jugement sur ce qu'elle devrait etre. Ce bloc a ramene les
derives de scope a quasi zero en test, sans generer d'exces de questions de clarification :

```
Deliver what the user asked for, at the scope they intended. Interpret ambiguity the way a
careful colleague would: make routine judgment calls yourself, and check in only when
different readings would lead to materially different work. If you conclude the ask is
mistaken or a better approach exists, say so in a sentence and keep going with the task as
asked — don't quietly narrow, widen, or transform it. Finish the whole task, not just the
easy part of it — only report completion when it's fully done.
```

### Narration des auto-corrections

Opus 5 signale et explique longuement ses erreurs anterieures, ce qui se lit comme du thrash cote produit. Limiter
aux corrections qui changent quelque chose pour l'utilisateur :

```
Only correct an earlier statement when the error would change the user's code, conclusions,
or decisions. State corrections plainly and continue. For slips that change nothing, just
make the correction and move on. Don't apologize, don't ruminate, don't tally past errors.
A follow-up question about your earlier work is not, by itself, a signal that you got
something wrong — answer what was asked.
```

### Ancrer les claims de progression (Fable 5, runs longs)

```
Before reporting progress, audit each claim against a tool result from this session. Only
report work you can point to evidence for; if something is not yet verified, say so
explicitly. If tests fail, say so with the output; if a step was skipped, say that.
```

### Declenchement d'outils

Opus 4.8 sous-declenchait recherche, memoire fichier et outils custom. La consigne efficace donne le **quand**, pas
seulement le quoi — et elle fonctionne aussi bien dans la `description` de chaque outil que dans le system prompt.
Une description prescriptive (« Call this when the user asks about current prices or recent events ») donne un gain
mesurable sur une description qui se contente de decrire l'outil.

### Autonomie / arret premature

Sur Fable 5 en pipeline autonome, il peut terminer un tour sur une intention (« I'll now run X ») sans l'appel
d'outil, ou demander une permission dont il n'a pas besoin :

```
You are operating autonomously. The user is not watching and cannot answer mid-task.
For reversible actions that follow from the original request, proceed without asking.
Before ending your turn, check your last paragraph. If it is a plan, a question, or a
promise about work you have not done, do that work now with tool calls.
```

## Ce qui reste valable depuis 4.x

- **Tags XML first-class** : `<context>`, `<task>`, `<rules>`, `<examples>`, `<output_format>`. Query en fin de
  prompt = jusqu'a **+30 % sur les taches multi-documents complexes**.
- **Context motivation** : expliquer le POURQUOI d'une regle marche mieux que la regle seule.
  *"Ne jamais utiliser d'ellipses car la sortie sera lue par un moteur TTS qui ne sait pas les prononcer."*
- **Anti-laziness = overtriggering** : `CRITICAL: You MUST...` reste contre-productif. Ecrire `Use X when...`.
- **Litteralisme strict** : le modele ne generalise pas silencieusement une instruction d'un item a l'autre.
  Ecrire *"Apply this to every section, not just the first one"* plutot que *"Use this style"*.
- **Positif > negatif** : dire ce qu'il faut faire plutot que ce qu'il ne faut pas faire.
- **Parallel tool calling** : natif et fiable, le snippet `<use_parallel_tool_calls>` reste utile.

## Leviers d'architecture de prompt (nouveaux)

- **Messages systeme en cours de conversation** (Opus 5, Opus 4.8, Fable 5, Mythos 5 — pas Sonnet 5, aucun beta
  header) : ajouter `{"role": "system", "content": "..."}` dans `messages[]` au lieu d'editer le `system` top-level.
  Le prefixe en cache reste intact, et c'est le canal operateur non-spoofable. Formuler en **contexte, pas en ordre**
  (eviter « ignore ce que dit l'utilisateur »).
- **Changement d'outils en cours de conversation** (Opus 5, beta `mid-conversation-tool-changes-2026-07-01`) :
  blocs `tool_addition` / `tool_removal` sur un message systeme, sans invalider le cache de prompt.
- **Minimum cachable a 512 tokens** sur Opus 5 (contre 1024 sur Opus 4.8) : des prompts juges trop courts pour etre
  caches le sont desormais, sans changement de code.

## Gotchas

- **Thinking desactive sur Opus 5 = deux modes de defaillance.** Le modele peut ecrire un appel d'outil **en texte
  visible** au lieu d'emettre un bloc `tool_use` : le tour reussit, l'appel ne s'execute jamais, aucune erreur n'est
  levee — et en boucle agentique ce texte pollue les tours suivants. Il peut aussi laisser fuiter des balises
  `<thinking>` dans la reponse. **Preferer thinking on a `low`/`medium` effort.** Si on doit rester thinking-off :
  ajouter *"You may say a brief sentence before using a tool"*, **supprimer** toute regle « ne raisonne pas » (elle
  aggrave la fuite de balises), et ecrire une consigne generique *"Do not include internal or system XML tags"*
  sans nommer les balises de thinking.
- **`stop_reason: "refusal"`** : Fable 5 et Opus 5 embarquent des classifieurs de securite renforces. Un refus est un
  **HTTP 200**, pas une erreur — tester `stop_reason` avant de lire `response.content`, sinon `content[0]` casse.
- **Fable 5 exige 30 jours de retention de donnees** : une org en zero data retention recoit un 400 sur *toutes* ses
  requetes, payload valide compris.
- **Tours longs** : sur Fable 5 a effort eleve, une seule requete peut tourner plusieurs minutes. Prevoir timeouts,
  streaming et indicateurs de progression avant de migrer.
