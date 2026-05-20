---
name: Audit cleanup Claude Code 2026-05-20
description: Audit + cleanup exécuté sur 41j (2026-04-09 → 2026-05-20). Suppression de 14 skills + 1 MCP, optim de 6 artefacts, création de 3 nouveaux skills. 3 commits sur main du repo claude-config.
type: project
originSessionId: prompt-creator-audit-2026-05-20
---

# Audit & Cleanup Claude Code — 2026-05-20

> Fenêtre : 2026-04-09 → 2026-05-20 (41j).
> S'appuie sur l'audit du 2026-05-09 (100 sessions, 8839 tool calls, 25 actions priorisées).
> Delta analysé : 67 transcripts modifiés depuis le 2026-05-09.

---

## Résultat — 3 commits exécutés sur main

| Commit | Hash | Contenu | Diff |
|---|---|---|---|
| 1 — Cleanup | `60fd732` | 14 skills supprimés + MCP `memory` retiré | -2400 lignes, -15 fichiers |
| 2 — Optimisations | `1363051` | 3 skills (desc) + 1 agent (desc) + 1 rule path-scopée + hook étendu | +28 -5 lignes, 6 fichiers |
| 3 — Nouveaux skills | `521dbdc` | 3 nouveaux skills (`docker-restart`, `audit-config`, `seqera-status`) | +233 lignes, 3 fichiers |

---

## État avant/après

| Artefact | Avant | Après | Delta |
|---|---|---|---|
| Skills | 39 | **28** | -14 +3 |
| Agents | 4 | 4 | inchangé (Boris a gardé agent-explore-quick override) |
| MCP listés | 8 | 7 | -1 (memory retiré) |
| Rules | 11 (1 path-scopée existante) | 11 (2 path-scopées) | aima-brand.md path-scopé |
| Hooks PreToolUse Bash | 8 règles | **9 règles** | +nextflow run hors ~/Run |
| Plugins activés | 5 | 5 | inchangé (superpowers + frontend-design déjà ajoutés depuis 2026-05-09) |

---

## Skills — détail des décisions

### Supprimés (14)

| Skill | Raison |
|---|---|
| utils-oneshot | 0 invoc 41j, frontmatter cassé (`name: oneshot`) |
| utils-fix-grammar | 0 invoc 41j, frontmatter cassé (`name: fix-grammar`) |
| python-refactor | 0 invoc 41j, YAML manquant (bloc inline) |
| git-commit | 0 invoc 41j, `name: commit`, Boris fait git en Bash (92×/11j) |
| git-create-pr | 0 invoc 41j, `name: create-pr`, workflow PR pas adopté |
| git-fix-pr-comments | 0 invoc 41j, `name: fix-pr-comments`, pas de reviewer humain |
| git-merge | 0 invoc 41j, `name: merge`, merge en Bash direct |
| graphify | Décision Boris (knowledge graph peu utilisé) |
| qc-report | Décision Boris (workflow QC ailleurs) |
| audit-trail | Décision Boris (traçabilité ISO 15189 traitée autrement) |
| batch-effect | Décision Boris (analyse stats ailleurs) |
| compare-batches | Décision Boris (idem) |
| correlation | Décision Boris (idem) |
| check-consistency | Redondant avec `tp check` |

### Modifiés (3 skills + 1 agent)

| Artefact | Modification |
|---|---|
| `claude-memory` (SKILL.md) | Description précise auto memory officielle + syntaxe `@import` + `paths:` rules |
| `workflow-apex` (SKILL.md) | `name: apex` → `name: workflow-apex` (matche dossier) |
| `react-best-practices` (SKILL.md) | Desc inclusive Tower V3 + extensible aux futurs projets React |
| `agent-docs` (.md) | Desc précise : SEULEMENT doc versionnée Context7, redirect vers websearch/pubmed sinon |

### Path-scoped (1 rule)

| Rule | Avant | Après |
|---|---|---|
| `aima-brand.md` | Global | `paths: ["**/*.tex", "**/*.typ", "**/rapport*/**", "**/report*/**", "**/Aima-Tower/**"]` |
| `template-claude-md.md` | déjà path-scopé (sans changement) | idem |

### Hook étendu

`scripts/pretool-bash-guard.sh` ajoute règle 9 : bloque `nextflow run` quand `cwd` est `~/Pipeline/...`. Couverture passe de 8/9 à **9/9 golden rules Bash testées**.

Tests passants (validés avant commit) :
- `ls` depuis `~/Run` → autorisé (exit 0)
- `nextflow run main.nf` depuis `~/Pipeline/Bam2Beta` → BLOQUÉ (exit 2)
- `nextflow run /home/blipinski/Pipeline/Bam2Beta/main.nf` depuis `~/Run` → autorisé (exit 0)

### Créés (3 nouveaux skills)

| Skill | Pattern source | Trigger |
|---|---|---|
| `/docker-restart` | `docker compose down && build && up -d && logs -f` 10× verbatim Aima-Tower | "restart tower", "redémarre aima-tower", "rebuild and restart" |
| `/audit-config` | Encapsule ce workflow pour relance régulière 1-3 mois | "audit-config", "tri configuration claude", "cleanup claude" |
| `/seqera-status` | Todo prioritaire "Seqera AI prise en main" + MCP auth pending | "seqera-status", "tower status", "où en sont mes runs" |

---

## MCP — état actualisé

| MCP | État | Usage 11j | Décision |
|---|---|---|---|
| `Claude_in_Chrome` | ✓ (via plugin) | 13× | Gardé (le plus utilisé) |
| `pubmed` | ✓ connected | 0 | Gardé (workflow veille) |
| `seqera` | ! auth pending | 0 | À réauthentifier (couvert par `/seqera-status`) |
| `context7` | ✓ via plugin | 1× | Gardé (plugin officiel) |
| `claude_ai_Gmail/Drive/Calendar` | ! auth pending | 0 | Gardés (low priority Aima-Survey futur) |
| `memory` | ~~✓ connected~~ | ~~0~~ | **SUPPRIMÉ** (redondant auto memory) |
| `browser-tools` | (n'était pas dans user config) | 0 | Pas dans repo, rien à faire |
| `playwright` | (absent) | 0 | Pas dans repo, rien à faire |

---

## Items audit 2026-05-09 — état au 2026-05-20

### ✅ Faits

| # | Action | Statut |
|---|---|---|
| #4 (B5/C6) | `permissions.deny` ajoutées (20 deny rules) | ✓ commit `2992e3f` (avant 2026-05-20) |
| #15 (A8) | `agent-docs` description précisée | ✓ commit 2 (2026-05-20) |
| (B6) | Hook `if:` étendu (via script bash, pas via `if:` natif) | ✓ commit 2 |
| (B30) | Path-scope rules | ✓ partiel (aima-brand fait, template déjà) |
| Skills cleanup massif | 14 supprimés | ✓ commit 1 |
| Skill `/docker-restart` | Créé | ✓ commit 3 |
| Skill `audit-config` | Créé | ✓ commit 3 |

### ⏳ Hors scope (manuels Boris ou non urgents)

| Item | Pourquoi |
|---|---|
| #1 `/fewer-permission-prompts` | Action manuelle Boris (à lancer dans une session active) |
| B1 Remote Control + push mobile | Action manuelle (install app, `claude remote-control`, `/config`) |
| B13 MCP DuckDB read-only | Effort S mais bénéfice futur non urgent |
| B14 MCP S3 Scaleway read-only | Effort M, profil scw direct fonctionne |
| B27 StatusLine enrichie | Gain ergonomique faible vs charge |
| B26 Output style `aima-clinical` | Superpowers couvre partie du besoin |
| B7 PreCompact hook | Pas de friction observée |
| A11 `/init` 5 projets sans CLAUDE.md | Par projet, hors scope claude-config |

---

## Validation finale

| Check | OK |
|---|---|
| 3 commits sur main | ✓ (`60fd732`, `1363051`, `521dbdc`) |
| Skills résultats : 28 (39 - 14 + 3) | ✓ |
| Golden rules préservées (s3-safety, secrets, nextflow, duckdb) | ✓ |
| Hook PreToolUse étendu et testé | ✓ |
| Pas de modif orphelines staged dans les commits | ✓ (sessions et trace-prod memory restent hors commits) |
| Auto-push hook actif | ✓ (push GitHub à la fin de session) |

---

## Référence

- Audit précédent : `audit-claude-code-2026-05-09.md`
- Inventaire à mettre à jour : `inventaire-claude-code.md`
- Pour relancer cet audit dans 1-3 mois : `/audit-config`
