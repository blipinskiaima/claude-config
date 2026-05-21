# Spec — Mise à jour du skill /prompt-creator (mai 2026)

**Date** : 2026-05-21
**Auteur** : Boris Blipinski (validation) + Claude Opus 4.7 (rédaction)
**Statut** : En attente review utilisateur

---

## Contexte

Le skill `/prompt-creator` est utilisé par Boris pour générer des prompts dans plusieurs contextes : system prompts d'agents Claude Code, prompts ad-hoc en session, prompts pour skills, prompts pour outils externes (Cursor, Anthropic Console, API Python/Nextflow).

Le développement des LLM avance rapidement. Audit demandé pour vérifier si les bonnes pratiques documentées dans le skill sont toujours d'actualité.

## Méthode d'audit

1. **Lecture exhaustive** du skill actuel (1 SKILL.md + 11 références)
2. **Recherche rigoureuse** via agent dédié, sources primaires uniquement
   (docs.anthropic.com, platform.openai.com, ai.google.dev, arxiv)
3. **Verdict par claim** : ✅ confirmé / ⚠️ partiel / ❌ infirmé
4. **Application des Karpathy Guidelines** (simplicité, modifs surgicales, critères de succès)
5. **Skills superpowers** invoqués : `writing-skills` + `brainstorming`

## Findings

### Claims CONFIRMÉS officiellement (à intégrer)

| Domaine | Claim | Source |
|---|---|---|
| Claude | Adaptive Thinking remplace `budget_tokens`, paramètre `effort` (max/xhigh/high/medium/low) | docs.anthropic.com — Adaptive thinking |
| Claude | Prefill assistant supprimé sur 4.6+ (erreur 400) | docs.anthropic.com — Prompting best practices |
| Claude | Opus 4.7 plus littéral, spécifier portée explicitement | docs.anthropic.com — Prompting best practices |
| Claude | Anti-laziness ("MUST use", "be thorough") cause overtriggering | docs.anthropic.com — Tune anti-laziness |
| Claude | Snippet `<use_parallel_tool_calls>` officiel | docs.anthropic.com — Optimize parallel tool calling |
| Claude | Tool use language softening | docs.anthropic.com — Prompting best practices |
| OpenAI | GPT-5.5 Instant sorti mai 2026, GPT-5.5/5.4/5.2 dans API | openai.com — GPT-5.5 Instant |
| OpenAI | `verbosity` distinct de `reasoning_effort` | OpenAI Cookbook |
| OpenAI | `developer message` pour o-series (pas `system`) | platform.openai.com — Reasoning |
| OpenAI | Pas de "think step by step" sur o-series | OpenAI — Reasoning best practices |
| OpenAI | `store: true` pour reasoning items dans Responses API | OpenAI — Reasoning models |
| OpenAI | Zero-shot first sur reasoning models | OpenAI — Reasoning best practices |
| Académique | Karpathy "context engineering" (X/Twitter, 25 juin 2025) | x.com/karpathy/status/1937902205765607626 |
| Académique | PRISM 2026 — expert personas dégradent accuracy | arxiv 2603.18507 |

### Claims INFIRMÉS (à retirer ou ne pas ajouter)

| Claim | Verdict | Raison |
|---|---|---|
| "XML tags +15-20% perf sur Claude" | ❌ | Chiffre absent docs primaires. Ce qui est officiel : "queries en fin = +30% complex multi-doc" |
| "PTCF framework officiel Google" | ❌ | L'acronyme n'existe pas dans docs ai.google.dev |
| "Temperature 1.0 défaut Gemini 3" | ❌ | Aucune mention officielle |
| "Multi-agent erreurs ×17" | ⚠️ | Chiffre douteux, source primaire Google DeepMind non vérifiable |
| "Prompts engineerés réduisent coûts 76%" | ❌ | Aucune source primaire |

## Plan retenu : MODERATE (7 modifs, ~40 min)

**Hors scope** (jugé nice-to-have pour le profil Boris — usage principalement Claude) :
- google-best-practices.md (Gemini peu utilisé)
- context-management.md prompt caching (peu d'API directe)
- few-shot-patterns.md bump 3-5 (cosmétique)
- prompt-templates.md structured outputs (nice-to-have)

## Architecture cible (inchangée)

```
prompt-creator/
├── SKILL.md                            🔧 (versions modèles)
└── references/
    ├── clarity-principles.md           ✅ Inchangé
    ├── xml-structure.md                🔧 Retrait "+15-20%"
    ├── few-shot-patterns.md            ✅ Inchangé (hors scope)
    ├── reasoning-techniques.md         🔧 Effort + cross-ref
    ├── context-management.md           ✅ Inchangé (hors scope)
    ├── system-prompt-patterns.md       🔧 + developer message
    ├── prompt-templates.md             ✅ Inchangé (hors scope)
    ├── anti-patterns.md                🔧 +4 patterns confirmés
    ├── anthropic-best-practices.md     🔥 Réécriture
    ├── openai-best-practices.md        🔥 Réécriture
    └── google-best-practices.md        ✅ Inchangé (hors scope)
```

**Pourquoi pas de nouveau fichier** : application Karpathy #2 (Simplicity First). Tous les ajouts s'intègrent naturellement dans des fichiers existants (subagents → anthropic, reasoning models → openai, developer message → system-prompt-patterns).

## Mapping détaillé par fichier

### 1. SKILL.md — MAJ versions modèles

**Ajout** : références Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5, GPT-5.5 Instant, Gemini 3.x

**Retrait** : "Claude 4.6", "GPT-5.2", "Gemini 3" (sans .x)

**Aucun changement** sur la structure du workflow Step 1-5.

### 2. anthropic-best-practices.md — RÉÉCRITURE

**Sections cibles** :
1. Adaptive Thinking (remplace section Extended)
   - Pattern `{"thinking": {"type": "adaptive"}, "output_config": {"effort": "high"}}`
   - Valeurs `effort` : max / xhigh (Opus 4.7 only) / high / medium / low
2. Prefill mort sur Claude 4.6+
   - Migration vers structured outputs, instructions système
3. Opus 4.7 literalisme
   - "Apply to every section, not just the first one"
4. Anti-laziness softening
   - "MUST use" → "Use when..."
5. Parallel tool calls (snippet officiel)
6. Subagent spawning policy (concept officiel ; syntaxe en texte libre, pas de tag XML standardisé chez Anthropic)

**Retrait** : "be thorough", "do not be lazy", langage agressif

### 3. openai-best-practices.md — RÉÉCRITURE

**Sections cibles** :
1. Modèles disponibles mai 2026 (GPT-5.5/5.4/5.2 + o3/o4-mini)
2. CTCO pattern (conservé)
3. `verbosity` distinct de `reasoning_effort`
4. **Nouvelle section : Reasoning models (o-series)**
   - `developer message` (pas system)
   - Pas de "think step by step"
   - Zero-shot first
   - `store: true` pour reasoning items
   - Prompts courts et directs
5. Prompt caching (statique en début)
6. Structured Outputs (`response_format` strict JSON)

**Retrait** : GPT-5.2 only, few-shot obligatoire sur reasoning

### 4. system-prompt-patterns.md — MAJ ciblée

**Ajout** :
- Section "Developer message vs System message" (cas o-series OpenAI)
- Note sur literalisme Opus 4.7

### 5. reasoning-techniques.md — MAJ ciblée

**Ajout** :
- Paramètre `effort` Claude (cross-ref vers anthropic-best-practices.md)
- Renforcement "pas de CoT sur o-series" (cross-ref vers openai-best-practices.md)

### 6. anti-patterns.md — MAJ ciblée

**Ajout (4 patterns confirmés)** :
| Anti-pattern | Pourquoi | Alternative |
|---|---|---|
| String matching downstream sur format de sortie | Casse au changement de phrasing | Structured Outputs |
| Prompts prescriptifs pas-à-pas pour reasoning models | Contraint le raisonnement interne | Décrire résultat, pas étapes |
| "Expert persona" seul comme optimisation | Améliore alignement, dégrade accuracy (PRISM 2026) | Contexte riche > persona seule |
| Sur-emphasis CAPS sur Claude 4.6+ | Overtriggering | Instructions normales |

### 7. xml-structure.md — Correction

**Retrait** : "+15-20% perf" (claim infirmé)

**Conservation/Ajout** : citation officielle "queries en fin = +30% complex multi-doc inputs" (docs.anthropic.com)

## Critères de succès (Tests RED)

Après application des modifs, un script bash `verify-prompt-creator.sh` à la racine du skill vérifie automatiquement :

### TEST 1 — Versions modèles à jour

```bash
grep -r "Opus 4.7" .              # PASS: ≥1 occurrence
grep -r "Sonnet 4.6" .            # PASS: ≥1 occurrence
grep -r "GPT-5.5" .               # PASS: ≥1 occurrence
grep -r "Gemini 3.x" .            # PASS: ≥1 occurrence
grep -rE "Claude 4\.6[^.]" .      # PASS: 0 occurrence (sauf en histo)
grep -r "GPT-5.2" .               # PASS: 0 occurrence
```

### TEST 2 — Paramètres API actuels

```bash
grep -rE "adaptive|effort" .      # PASS: ≥1 occurrence
grep -r "verbosity" .             # PASS: ≥1 occurrence
grep -r "developer message" .     # PASS: ≥1 occurrence
grep -r "budget_tokens" .         # PASS: contexte "déprécié" uniquement
```

### TEST 3 — Anti-patterns confirmés présents

```bash
grep -r "string matching" anti-patterns.md       # PASS: ≥1
grep -r "expert persona" anti-patterns.md         # PASS: ≥1
grep -r "think step by step" anti-patterns.md     # PASS: ≥1 (en anti)
grep -r "MUST use" anti-patterns.md               # PASS: ≥1 (en softening)
```

### TEST 4 — Zéro claim infirmé

```bash
grep -rE "15-20%|\+15" .          # PASS: 0 occurrence
grep -r "PTCF" .                  # PASS: 0 occurrence
grep -rE "×17|17x|17\.2" .        # PASS: 0 occurrence
grep -r "76%" .                   # PASS: 0 occurrence
```

**Total : 18 vérifications grep, exit code 0 = tous PASS.**

## Karpathy Compliance Check

| Guideline | Application |
|---|---|
| #1 Think Before Coding | Recherche rigoureuse + brainstorming + verdicts explicites avant écriture |
| #2 Simplicity First | 0 nouveau fichier créé, intégration dans l'existant |
| #3 Surgical Changes | 7 fichiers modifiés / 12 (5 inchangés). Chaque modif tracée à un claim vérifié |
| #4 Goal-Driven Execution | 4 tests RED automatisés avec 18 vérifs grep |

## Hors scope (volontairement exclus)

- Google/Gemini best practices (Boris utilise peu Gemini)
- Prompt caching dédié (peu d'API directe dans son workflow)
- Few-shot patterns bump 3-5 exemples (cosmétique)
- Template structured outputs (nice-to-have)
- Création de nouveaux fichiers `context-engineering.md`, `reasoning-models.md`, etc.
  (initialement proposés, jugés sur-engineering : info intégrée dans fichiers existants)

## Plan d'exécution suivant

Après approbation de ce spec :
1. Invocation du skill `superpowers:writing-plans` pour générer un plan d'implémentation détaillé
2. Le plan inclura : ordre des fichiers, gestion git, exécution des tests RED
3. Exécution séquentielle avec validation fichier par fichier (préférence Boris)

## Risques identifiés

| Risque | Mitigation |
|---|---|
| Recommandations LLM obsolètes dans 6-12 mois | Plan documenté, rejouable. Spec doc archive le contexte |
| Régression sur les prompts existants de Boris | Pas de breaking change : les vieilles techniques restent valides quand applicables, les NEW sont des ajouts |
| Hallucinations dans la recherche | Mitigé par verdict ✅/⚠️/❌ avec citation littérale obligatoire |
| Sur-engineering | Mitigé par Karpathy #2 (0 nouveau fichier, scope MODERATE retenu) |

---

**Validation utilisateur** : à fournir avant invocation de `writing-plans`.
