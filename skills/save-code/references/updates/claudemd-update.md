# CLAUDE.md Update Guide

## Quand Mettre à Jour le CLAUDE.md

| Type de changement | Mettre à jour | Ce qu'il faut ajouter |
|---|---|---|
| Nouvelle convention de code | Oui | Règle dans Code Style |
| Nouvelle commande (build, test, etc.) | Oui | Commande dans Commands |
| Changement d'architecture | Oui | Mise à jour Architecture |
| Nouveau pattern adopté | Oui | Pattern dans Conventions |
| Nouveau gotcha découvert | Oui | Note dans Important Notes |
| Nouvelle dépendance majeure | Oui | Mise à jour Tech Stack |
| Simple bug fix | Non | — |
| Changement dans un seul fichier | Non | — |
| Refactoring sans changement de pattern | Non | — |

## Comment Mettre à Jour

### 1. Lire le CLAUDE.md existant
```bash
Read: ./CLAUDE.md OR ./.claude/CLAUDE.md
```

### 2. Identifier ce que les changements apportent de NOUVEAU

Questions à se poser :
- Est-ce qu'une nouvelle convention a été introduite ?
- Est-ce qu'une commande a changé ou a été ajoutée ?
- Est-ce qu'un nouveau module/composant a été créé ?
- Est-ce qu'un gotcha non-évident a été découvert ?
- Est-ce qu'un pattern existant a été modifié ?

### 3. Appliquer les modifications

**Principes :**
- Ajouter dans la section appropriée (pas en vrac à la fin)
- Rester concis — chaque ligne coûte des tokens à chaque session
- Être spécifique — "Use Zod for validation" pas "Validate inputs"
- Expliquer le WHY si non-évident
- Ne pas dupliquer ce qui est déjà dans .claude/rules/

### 4. Vérifier la taille

```bash
wc -l ./CLAUDE.md
```

Si le CLAUDE.md dépasse 100 lignes, envisager :
- Déplacer des sections vers .claude/rules/ (avec path targeting)
- Utiliser des imports (@path/to/file) pour le contenu détaillé
- Supprimer les instructions obsolètes

## Exemple de Mise à Jour

```markdown
## Avant la session
# Commands
- Dev: `pnpm dev`
- Test: `pnpm test`

## Après la session (ajout endpoint health)
# Commands
- Dev: `pnpm dev`
- Test: `pnpm test`
- Health check: `curl http://localhost:3000/api/health`

# Architecture
- ...
- `src/routes/health.ts` — health check endpoint (monitoring)
```

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Ajouter des infos que Claude peut déduire du code | Documenter uniquement ce qui n'est pas évident |
| Écrire des paragraphes de prose | Bullet points concis |
| Dupliquer le README | Référencer le README si besoin |
| Laisser des infos obsolètes | Supprimer les conventions abandonnées |
| Dépasser 100 lignes | Déplacer vers .claude/rules/ |
