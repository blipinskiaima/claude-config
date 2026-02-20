# Execution Rules

## Karpathy Guidelines Appliquees

### 1. Think Before Coding
- Avant chaque modification, verifier que l'intention est claire
- Si un doute apparait en cours d'implementation → arreter, poser la question a l'utilisateur
- Ne jamais "deviner" un comportement attendu

### 2. Simplicity First
- Ecrire le code minimal qui fonctionne
- Pas d'abstractions pour un seul usage
- Pas de features speculatives ("au cas ou")
- Pas de flexibilite/configurabilite non demandee
- Si 200 lignes peuvent devenir 50 → reecrire

### 3. Surgical Changes
- Chaque ligne modifiee doit etre traceable au plan approuve
- Ne pas "ameliorer" le code adjacent
- Ne pas refactorer ce qui n'est pas casse
- Matcher le style existant meme si on ferait differemment
- Dead code pre-existant → mentionner, ne pas supprimer
- Imports/variables rendus orphelins par NOS changements → supprimer

### 4. Goal-Driven Execution
- Suivre l'ordre du plan approuve
- Apres chaque etape du plan : verifier selon le critere defini
- Si une verification echoue → corriger avant de continuer
- Si la correction n'est pas evidente → demander a l'utilisateur

## Workflow d'Execution

```
Pour chaque etape du plan :
  1. Lire le fichier cible
  2. Comprendre le code existant autour de la zone a modifier
  3. Appliquer la modification (Edit, pas Write sauf creation)
  4. Verifier (test, build, diagnostic)
  5. Si echec → corriger ou demander a l'utilisateur
  6. Passer a l'etape suivante
```

## Gestion des Obstacles

**Code ne compile pas :**
1. Lire l'erreur attentivement
2. Identifier si c'est lie a la modification ou pre-existant
3. Si pre-existant → informer l'utilisateur, ne pas corriger hors scope
4. Si lie → corriger et re-verifier

**Test echoue :**
1. Lire le test et comprendre ce qu'il verifie
2. Est-ce un test existant casse par la modification ? → ajuster le code
3. Est-ce un nouveau test mal ecrit ? → corriger le test
4. Doute → demander a l'utilisateur

**Dependance manquante :**
1. Verifier si elle est dans le plan
2. Si oui → installer et continuer
3. Si non → proposer a l'utilisateur avant d'installer

**Conflit avec code existant :**
1. Ne pas forcer / hack
2. Expliquer le conflit a l'utilisateur
3. Proposer des alternatives
4. Attendre la decision
