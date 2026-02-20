# Verification Checklist

## 1. Verification Technique

### Tests
```bash
# Lancer les tests du projet
npm test / pytest / cargo test / etc.
```
- Tous les tests existants passent (pas de regression)
- Nouveaux tests pour la feature (si applicable)

### Build
```bash
# Verifier la compilation
npm run build / cargo build / etc.
```
- Pas d'erreur de compilation
- Pas de warning nouveau

### Diagnostics IDE
```
mcp__ide__getDiagnostics
```
- Pas de nouvelle erreur TypeScript/ESLint/etc.
- Warnings acceptables documentes

### Lint
```bash
# Si le projet a un linter configure
npm run lint / flake8 / clippy / etc.
```

## 2. Recap des Modifications

Presenter a l'utilisateur un recapitulatif clair :

```markdown
## Recap : [Feature]

### Fichiers Modifies
| Fichier | Action | Changement |
|---------|--------|------------|
| `path/file.ts` | Modifie | [description courte] |
| `path/new.ts` | Cree | [description courte] |

### Resume Fonctionnel
[2-3 phrases expliquant ce qui a ete implemente]

### Tests
- [x] Tests existants : passent
- [x] Nouveaux tests : [nombre] ajoutes
- [x] Build : OK
- [x] Lint : OK

### Erreurs Rencontrees
- [erreur] → [resolution]
(ou "Aucune erreur rencontree")
```

## 3. Sauvegarde Memoire

Si l'utilisateur valide le recap, invoquer `/claude-memory` avec le contexte :

**Quoi sauvegarder :**
- Patterns architecturaux decouverts ou confirmes
- Decisions d'implementation et leur justification
- Gotchas rencontres et solutions
- Conventions de code confirmees
- Dependances ajoutees et pourquoi

**Quoi NE PAS sauvegarder :**
- Details specifiques a cette feature (trop ephemere)
- Code snippets (deja dans le repo)
- Informations deja dans CLAUDE.md
