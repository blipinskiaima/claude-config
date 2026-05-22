# Spec — Résolution contradiction `feedback-claude-usage.md`

**Date** : 2026-05-22
**Auteur** : Boris (via brainstorming session)
**Statut** : En cours de validation

---

## Contexte

`feedback-claude-usage.md` (38 jours, créé le 2026-04-13) contient 4 sections dont :
- 1 contredit directement `CLAUDE.md` (Session Start : "toujours DEEP" vs routing intent quick/deep)
- 2 sont quasi-redondantes (Communication, Sécurité données)
- 1 est partiellement utile (Délégation par projet)

La contradiction Session Start est active depuis l'évolution de CLAUDE.md (routing intent ajouté en 2026-05-22). Le fichier ne suit pas le format strict Anthropic auto memory (Règle / Why incident / How to apply).

## Décision

**Approche B retenue** : réécrire le fichier comme un vrai journal de feedback aligné sur la doc Anthropic, et migrer les préférences comportementales générales vers `CLAUDE.md`.

## Conception

### A — Nouveau `feedback-claude-usage.md`

**Frontmatter** :

```yaml
---
name: feedback-claude-usage
description: Journal des feedbacks et incidents Boris qui informent comment Claude doit travailler avec lui — règles validées par retour terrain
type: feedback
last_review: 2026-05-22
---
```

**Organisation** : chronologique inverse (plus récent en haut), append-only.

**Format strict par entrée** :

```markdown
## YYYY-MM-DD — Titre court de la règle

**Règle :** [phrase impérative concise, ce qu'il faut faire ou éviter]

**Why :** [incident précis ou décision stratégique qui a généré la règle, daté et sourcé si possible]

**How to apply :** [quand cette règle s'active, périmètre, exceptions, liens [[autre-memoire]]]
```

**Marquage obsolescence** :
- Garder le titre de niveau h2 standard : `## YYYY-MM-DD — Titre`
- En **première ligne du corps**, écrire : `> [OBSOLETE depuis YYYY-MM-DD — voir [[nom-de-la-règle-actuelle]]]`
- La règle d'origine reste lisible, le marquage est explicite, le markdown reste parseable
- Ne **jamais** supprimer (traçabilité décisions)

### B — Inventaire initial (6 entrées)

| # | Date | Règle synthétique | Source |
|---|---|---|---|
| 1 | 2026-05-22 | Routing Session Start : quick par défaut, deep pour feature/refactor | CLAUDE.md actuel + audit 2026-05-22 (remplace ancienne règle "toujours deep") |
| 2 | 2026-04-21 | Vérifier `.env` dans `.gitignore` avant tout commit initial | `security_setup.md`, todo-optim 2026-04-21 |
| 3 | 2026-04 | ComBat-Met rejeté en production : correction stats non auditable ISO 15189 | `aima-value-analysis.md` + `batch-effect-investigation.md` |
| 4 | 2026-03-XX | Ne jamais lancer 2 jobs GPU Dorado simultanément (batch size auto-réduit → résultats tronqués) | `rules/troubleshooting.md` Pod2Bam |
| 5 | 2026-XX | `aws s3 sync` skip silencieux 3-5/23-90 fichiers : retry boucle obligatoire | `rules/s3-safety.md` règle 5 |
| 6 | 2026-XX | `((COMPLETED++))` crash avec `set -e` (bash : `0++` = false) | `rules/troubleshooting.md` Pod2Bam |

Dates avec `XX` à préciser au moment de l'écriture en cherchant dans git log / boris_notes_extract.txt.

### C — Amendements `CLAUDE.md`

**Ajout dans §Communication** (1 bullet en fin de liste) :

```markdown
- Pas de résumé en fin de réponse — Boris lit le diff
```

**Nouvelle section après §Communication** :

```markdown
## Préférences opérationnelles par projet

### Pipelines cliniques (Bam2Beta, Pod2Bam)
- Demander **item par item** sur les modifications structurelles — refuser le batch implicite
- Ne **jamais paralléliser** les jobs GPU (basecall) — résultats tronqués observés
- Boris garde la main, Claude propose et explique

### Aima-Tower & outils internes
- Full autonomie Claude acceptée
- Pas d'audit ISO requis

### Jobs longs (basecall, rebasecalling, sync S3 massif)
- Lancer dans `tmux` par défaut (jamais en foreground bloquant)
- Si retry boucle nécessaire (`aws s3 sync`), encapsuler dans le tmux
```

### D — Mise à jour `MEMORY.md`

Remplacer la ligne actuelle :
```
- [Feedback Claude Code](feedback-claude-usage.md) — Retours d'expérience, ce qui fonctionne/ne fonctionne pas
```

Par :
```
- [Journal feedbacks & incidents](feedback-claude-usage.md) — Règles validées par retour terrain (incidents, décisions stratégiques, évolutions)
```

### E — Process de maintenance

```
┌──────────────────────────────────────────────────────────────┐
│  AJOUT D'UNE ENTRÉE                                          │
│  Trigger A : Boris dit "ajoute ça au feedback"               │
│  Trigger B : Claude détecte incident (bug, rollback, refus)  │
│              → propose l'entrée à valider AVANT d'écrire     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  OBSOLESCENCE                                                │
│  Préfixer [OBSOLETE - YYYY-MM-DD]                            │
│  Ajouter "Remplacée par : [[autre-règle]]"                   │
│  Ne jamais supprimer (traçabilité)                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  REVUE                                                        │
│  Check `last_review` frontmatter                              │
│  Si > 60j : Claude propose une revue                         │
│  À intégrer dans /audit-config                                │
└──────────────────────────────────────────────────────────────┘
```

## Architecture des changements

```
AVANT                          APRÈS
─────                          ─────
feedback-claude-usage.md       feedback-claude-usage.md
  4 sections                     6 entrées datées (incidents)
  1 contradiction active         format strict Anthropic
  90% redondant                  réseau de [[liens]]
                                 last_review trackée

CLAUDE.md                      CLAUDE.md
  §Communication                 §Communication +1 bullet
  §Délégation                    §Délégation (inchangé)
  §Session Start                 §Session Start (inchangé)
                                 + §Préférences opérationnelles (nouvelle)

MEMORY.md                      MEMORY.md
  "Feedback Claude Code"         "Journal feedbacks & incidents"
                                 (description plus précise)
```

## Files affectés

| Fichier | Action | Taille estimée après |
|---|---|---|
| `~/.claude/projects/-home-blipinski/memory/feedback-claude-usage.md` | Réécrire intégralement | ~100 lignes (vs 41 actuel) |
| `~/.claude/CLAUDE.md` | Édition ciblée (§Communication + nouvelle section) | +12 lignes |
| `~/.claude/projects/-home-blipinski/memory/MEMORY.md` | 1 ligne modifiée | inchangé |

## Risques et contre-mesures

| Risque | Contre-mesure |
|---|---|
| Dates `XX` non résolues dans les entrées 4-6 | Validation Boris à l'étape implémentation (chercher git log + boris_notes_extract.txt + troubleshooting.md historique) — à défaut, mettre "Avant 2026-04" |
| Hooks auto-push commit avant validation Boris | Workflow normal : édition → revue Boris en session → commit fin de session |
| Conflit avec `last_review` lors d'imports MEMORY.md (200 lignes max) | Le frontmatter est dans le fichier individuel, pas dans MEMORY.md → pas d'impact |
| Ajout d'une nouvelle §Préférences opérationnelles dans CLAUDE.md peut le faire dépasser le seuil de chargement | CLAUDE.md actuel ~110 lignes, +12 = 122 → marge confortable |

## Critères de validation

1. **Plus de contradiction** : la règle Session Start de `feedback-claude-usage.md` reflète le routing intent de CLAUDE.md
2. **Format conforme** : chaque entrée a Règle / Why / How to apply
3. **Pas de perte d'info utile** : les 4 préférences comportementales sont dans CLAUDE.md
4. **MEMORY.md pointeur à jour** : description plus précise
5. **last_review à jour** : 2026-05-22

## Out of scope

- Recherche exhaustive d'autres incidents historiques (post-MVP, à faire lors de revues mensuelles)
- Création d'un skill `/add-feedback` (pourrait venir plus tard si volume justifie)
- Intégration `last_review` check dans `/audit-config` (à ajouter en évolution future)

## Étape suivante

Après validation de ce spec par Boris : invoquer `writing-plans` pour produire un plan d'implémentation détaillé.
