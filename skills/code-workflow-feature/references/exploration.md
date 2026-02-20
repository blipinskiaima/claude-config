# Exploration Strategy

## Agent Selection

### Codebase Exploration

**Premiere question : le projet est-il deja documente ?**

- **Oui** (CLAUDE.md existe et contient architecture) → lancer `agent-explore-quick` (Haiku, rapide)
  - Si le resultat est insuffisant pour comprendre la zone impactee → relancer `agent-explore` (Sonnet, exhaustif)
- **Non** → lancer `agent-explore` directement

**Prompt pour l'agent :**
```
Explore ce codebase en profondeur. Je vais implementer [description feature].
J'ai besoin de comprendre :
- L'architecture des zones impactees
- Les patterns et conventions du projet
- Les fichiers cles a modifier
- Les dependances et data flow
```

### Documentation (Libraries)

Lancer `agent-docs` des qu'une library est impliquee :

- Library deja dans le projet → chercher la doc de la version installee
- Nouvelle library → chercher la doc + comparaison avec alternatives
- API tierce → chercher la doc + exemples d'integration

**Prompt pour l'agent :**
```
Cherche la documentation de [library] pour [usage specifique].
Version utilisee : [version from package.json/config].
J'ai besoin de : [API specifiques, patterns, exemples].
```

### Web Research

Lancer `agent-websearch` quand :

- La feature requiert un pattern/approche non trivial
- Besoin de best practices pour un cas specifique
- Probleme connu qui a des solutions documentees
- Comparaison de plusieurs approches possibles

**Prompt pour l'agent :**
```
Recherche [topic] pour implementer [feature].
Contexte : projet [stack] avec [contraintes].
Besoin : [best practices / patterns / exemples / comparaison].
```

## Parallelisation

Lancer les agents en parallele quand ils sont independants :

```
agent-explore (ou quick)  ─┐
agent-docs (library 1)    ─┤── en parallele
agent-docs (library 2)    ─┤
agent-websearch            ─┘
```

Utiliser `run_in_background: true` si l'exploration est longue et que l'utilisateur veut continuer a interagir.

## Synthese

Combiner les resultats en un briefing structure :

```markdown
## Contexte d'Exploration

### Architecture Impactee
- [Couche/module] : [fichiers cles] — [role]

### Fichiers a Modifier
1. `file:line` — [modification prevue]
2. `file:line` — [modification prevue]

### Fichiers a Creer
1. `path/new-file` — [role]

### APIs & Patterns
- [Pattern existant a suivre]
- [API de library a utiliser]

### Contraintes & Gotchas
- [Risque ou piege identifie]
- [Comportement non-intuitif]

### Documentation Cle
- [Library] : [resume des points pertinents]
```
