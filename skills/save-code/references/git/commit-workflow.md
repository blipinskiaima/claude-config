# Git Commit & Push Workflow

## Workflow Sécurisé

### 1. Vérifier l'état avant commit
```bash
git status                    # Voir tous les changements
git diff --stat               # Résumé des modifications
git diff                      # Détail des modifications
```

### 2. Staging sélectif

**Toujours ajouter les fichiers spécifiquement — jamais `git add .` ou `git add -A`.**

```bash
# Bon — fichiers spécifiques
git add src/routes/health.ts
git add src/tests/health.test.ts
git add README.md

# Mauvais — trop large
git add .
git add -A
```

**Fichiers à NE JAMAIS commit :**
- `.env`, `.env.*` (secrets)
- `credentials.json`, `*.key`, `*.pem` (clés)
- `node_modules/`, `__pycache__/` (dépendances)
- Fichiers générés (build/, dist/, .next/)

### 3. Message de Commit

**Format conventionnel :**
```
type(scope): description concise

Corps optionnel pour expliquer le WHY.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Types :**

| Type | Usage |
|---|---|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation uniquement |
| `refactor` | Restructuration sans changement fonctionnel |
| `test` | Ajout ou modification de tests |
| `chore` | Maintenance, config, dépendances |
| `perf` | Amélioration de performance |
| `style` | Formatage, lint (pas de changement logique) |

**Exemples :**
```bash
# Feature
git commit -m "feat(api): add health check endpoint for monitoring"

# Bug fix
git commit -m "fix(auth): handle expired token refresh correctly"

# Documentation
git commit -m "docs: update README with new API endpoints"

# Multiple changes
git commit -m "$(cat <<'EOF'
feat(api): add health check endpoint

- GET /api/health returns server status
- Includes DB connection check
- Updates README with endpoint documentation

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### 4. Commit

```bash
git commit -m "message"
```

Vérifier le succès :
```bash
git log --oneline -1    # Voir le commit créé
git status              # Vérifier qu'il ne reste rien
```

### 5. Push

**Toujours demander confirmation avant de push.**

```bash
# Vérifier la branche
git branch --show-current

# Push
git push

# Si première fois sur cette branche
git push -u origin $(git branch --show-current)
```

## Règles de Sécurité

- **JAMAIS** `git push --force` sans confirmation explicite
- **JAMAIS** `git reset --hard` sans confirmation explicite
- **JAMAIS** commit de fichiers contenant des secrets
- **JAMAIS** push vers main/master sans confirmation
- **TOUJOURS** vérifier la branche avant de push
- **TOUJOURS** vérifier git status après le commit
- **TOUJOURS** utiliser le staging sélectif (pas `git add .`)

## Si le Commit Échoue (pre-commit hooks)

1. Le commit N'A PAS été créé
2. Lire l'erreur du hook
3. Corriger le problème (lint, format, tests)
4. Re-stager les fichiers
5. Créer un **NOUVEAU** commit (ne PAS utiliser `--amend`)

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| `git add .` | Ajouter les fichiers un par un |
| `git commit --no-verify` | Corriger les erreurs de hook |
| `git push --force` | `git push` normal ou demander |
| `git commit --amend` après hook fail | Nouveau commit |
| Commit message vague ("fix stuff") | Message descriptif avec type et scope |
| Push sans vérifier la branche | Toujours vérifier avec `git branch` |
