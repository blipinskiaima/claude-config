# Planning Workflow

## Etape 2a : Creer le Prompt de Planification

Utiliser le skill `/prompt-creator` pour generer un prompt de planification structure.

### Contenu du prompt a generer

Le prompt doit inclure :

1. **Objectif clair** — description de la feature avec criteres d'acceptation
2. **Contexte d'exploration** — architecture, fichiers, patterns (synthese de l'etape 1)
3. **Contraintes** :
   - Karpathy Guidelines (surgical changes, simplicity first)
   - Style et conventions du projet (depuis CLAUDE.md ou exploration)
   - Limitations techniques identifiees
4. **Output attendu** — format du plan demande :

```
Pour chaque modification :
1. Fichier : [path]
2. Action : [creer/modifier/supprimer]
3. Changement : [description precise]
4. Verification : [comment verifier que c'est correct]
```

### Exemple de prompt genere

```xml
<context>
Projet : [nom] | Stack : [tech stack]
Architecture : [resume]
Feature : [description]
Criteres d'acceptation : [liste]
</context>

<constraints>
- Suivre les Karpathy Guidelines : surgical changes, simplicity first
- Matcher le style existant : [conventions du projet]
- Ne pas toucher au code en dehors du scope de la feature
</constraints>

<task>
Planifier l'implementation de cette feature. Pour chaque modification :
1. Fichier et action (creer/modifier)
2. Description precise du changement
3. Verification pour confirmer la correction
4. Ordre d'implementation (dependances entre fichiers)
</task>
```

## Etape 2b : Executer en Mode Plan

Appeler `EnterPlanMode` puis :

1. **Explorer les fichiers impactes** — lire chaque fichier identifie, comprendre le code existant
2. **Designer l'approche** — definir les changements precis, ligne par ligne si necessaire
3. **Definir l'ordre** — quels fichiers modifier en premier (dependances, tests d'abord si TDD)
4. **Lister les verifications** — pour chaque etape du plan, definir comment verifier

### Format du plan

```markdown
## Plan d'Implementation : [Feature]

### Pre-requis
- [ ] [Dependance a installer, config a modifier, etc.]

### Etapes

#### 1. [Titre] — `path/to/file`
- **Action** : [creer/modifier]
- **Changement** : [description precise]
- **Verification** : [test, build, check]

#### 2. [Titre] — `path/to/file`
- **Action** : [creer/modifier]
- **Changement** : [description precise]
- **Verification** : [test, build, check]

### Post-implementation
- [ ] Tests passent
- [ ] Build reussit
- [ ] Pas de regression
```

Appeler `ExitPlanMode` pour soumettre a l'utilisateur.
