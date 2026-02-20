# Auto Memory Update Guide

## Quand Mettre à Jour la Mémoire

| Événement pendant la session | Sauvegarder dans |
|---|---|
| Découverte d'un pattern de code | MEMORY.md (patterns) |
| Solution à un bug difficile | Topic file debugging.md |
| Décision architecturale prise | Topic file architecture.md |
| Nouveau workflow ou commande utile | MEMORY.md (commands) |
| Gotcha ou piège non-évident | MEMORY.md (gotchas) |
| Relation entre modules découverte | Topic file architecture.md |
| Préférence utilisateur exprimée | MEMORY.md (preferences) |

## Où Sauvegarder

### Trouver le répertoire mémoire
```bash
# Le chemin dérive du git root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
# La mémoire est dans ~/.claude/projects/-{encoded-path}/memory/
ls ~/.claude/projects/*/memory/ 2>/dev/null
```

### MEMORY.md (index, chargé chaque session)

Garder sous 200 lignes. Contenu type :
- Patterns clés découverts
- Commandes et raccourcis utiles
- Gotchas critiques
- Liens vers topic files

### Topic Files (chargés à la demande)

Créer pour les sujets détaillés :
- `debugging.md` — solutions à des problèmes complexes
- `architecture.md` — relations entre modules, data flows
- `patterns.md` — conventions de code découvertes

## Comment Mettre à Jour

### 1. Lire la mémoire existante
```bash
Read: ~/.claude/projects/*/memory/MEMORY.md
```

### 2. Identifier les apprentissages de la session

Extraire du contexte de conversation :
- Quels problèmes ont été résolus ? Comment ?
- Quelles décisions ont été prises ? Pourquoi ?
- Quels patterns ont été découverts ou confirmés ?
- Quelles erreurs ont été commises et corrigées ?

### 3. Écrire de façon concise

```markdown
# Bon — actionnable et spécifique
## Debugging
- Redis connection timeout: increase `connectTimeout` to 5000ms in config
- Prisma migration fails silently: always check `npx prisma migrate status`

# Mauvais — vague et verbeux
## Notes
- We had some issues with the database connection today and after
  investigating for a while we found that the timeout was too low.
```

### 4. Vérifier la taille de MEMORY.md
```bash
wc -l ~/.claude/projects/*/memory/MEMORY.md
```

Si proche de 200 lignes → déplacer les détails dans des topic files.

## Ce qu'il NE FAUT PAS Sauvegarder

- Contexte spécifique à cette session (tâche en cours, état temporaire)
- Informations déjà dans le CLAUDE.md du projet
- Hypothèses non vérifiées
- Code complet (référencer par file:line)
- Informations éphémères ("l'utilisateur veut finir avant 18h")

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Tout mettre dans MEMORY.md | Utiliser des topic files pour les détails |
| Dépasser 200 lignes | Pruner et déplacer vers topic files |
| Dupliquer le CLAUDE.md | Référencer, ne pas copier |
| Sauvegarder du code complet | Référencer par file:line |
| Ignorer la mise à jour mémoire | Toujours sauvegarder les apprentissages |
