# Degrees of Freedom

Calibrate how prescriptive the skill is. Wrong calibration → either a rigid skill that fails edge cases, or a vague skill where Claude wanders.

## The Three Levels

| Level | Form | Use when |
|---|---|---|
| **High** | Text heuristics, principles | Multiple valid approaches, decisions depend on context |
| **Medium** | Pseudocode, parameterized scripts | Preferred pattern with acceptable variation |
| **Low** | Specific scripts, narrow params, exact steps | Fragile ops, consistency critical, regulatory constraint |

## Mental Model

Claude navigates a path:
- **Open field** (high freedom) → many valid routes, pick by judgment
- **Marked trail** (medium freedom) → preferred route, alternatives allowed
- **Narrow bridge with cliffs** (low freedom) → one route, guardrails both sides

The narrower the bridge, the more specific the guidance.

## Examples by Level

### High freedom — `code-review` skill

```markdown
Review the diff. Focus on:
- Correctness
- Maintainability
- Security

Adapt depth and order to the changes' nature.
```

Why high: every diff is different. Heuristics > prescription.

### Medium freedom — `commit-message` skill

```markdown
Use Conventional Commits format:
  type(scope): summary

Common types: feat, fix, refactor, docs, test, chore.
Adjust scope based on affected area.
```

Why medium: format is fixed, content is contextual.

### Low freedom — `pod5-basecalling` skill

```bash
# Run exactly this. Order and flags matter.
dorado basecaller \
  --kit-name SQK-NBD114-24 \
  --trim all \
  dna_r10.4.1 input.pod5 > out.bam
```

Why low: deviation breaks output (see `~/.claude/rules/troubleshooting.md` Pod2Bam section).

## When to Increase Freedom

- Task has multiple valid solutions
- Claude has strong general knowledge to apply
- Output format is contextual
- Speed > strict consistency

## When to Decrease Freedom

- Operation is fragile (data loss, silent failures)
- Compliance constraint (ISO 15189, GDPR, audit trail)
- Output must match an exact format (API contract, DB schema)
- Past failures show Claude diverges from desired behavior

## Calibration Heuristic

| Phrase in your skill | Implied level |
|---|---|
| "Use your best judgment for X" | High |
| "Prefer X but Y is acceptable" | Medium |
| "You MUST do X" | Low |
| "Run exactly this script" | Low |

If unclear, **start medium**, then tighten or loosen based on observed behavior during real usage.

## Anti-Patterns

| Don't | Why |
|---|---|
| Over-specify trivial tasks | Wastes tokens, Claude already knows this |
| Under-specify fragile tasks | Silent failures (wrong output, lost data) |
| Mix levels within one section | Confusing — split into two clearly labeled sections |
| Set "low" everywhere by reflex | Makes the skill brittle on edge cases |
| Set "high" to avoid writing detail | Skill provides no real value over zero-skill |

## Connection to Skill Structure

- **High freedom skills** → fewer reference files, more principles in SKILL.md
- **Medium freedom skills** → templates and patterns in references
- **Low freedom skills** → scripts in `scripts/`, exact commands in SKILL.md
