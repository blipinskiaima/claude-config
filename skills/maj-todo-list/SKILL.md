---
name: maj-todo-list
description: "Déplace une tâche de la Partie 1 (À faire) vers la Partie 2 (Complété) du fichier todo-optimisation.md, sous la section datée d'aujourd'hui. Reformule le bullet en version done synthétique (résultat/conclusion en 1 phrase). Use when the user says maj-todo, maj todo, marque comme fait, tâche terminée, done, maj-todo-list, or asks to move/close/complete a task in his to-do list."
allowed-tools: Read, Edit, Bash(date*)
---

# Skill : Maj Todo (move to done)

Déplace une tâche de la Partie 1 (À faire) vers la Partie 2 (Complété), sous la date du jour, en reformulant en bullet synthétique.

## Fichier cible

`~/.claude/projects/-home-blipinski/memory/todo-optimisation.md`

Structure fixe :
- **Partie 1 — À faire (par priorité)** : Haute / Moyenne (sous-sections) / Basse
- **Partie 2 — Complété (par jour)** : sections `## YYYY-MM-DD — Titre du jour`

## Format strict d'un bullet done

```
- [x] **Titre court (4-8 mots)** — 1 phrase : résultat concret ou conclusion. Référence courte (fichier, projet, PR) si pertinent.
```

Règles :
- **Max 2 phrases** (souvent 1 suffit).
- Capturer le **résultat** ou la **décision**, pas l'historique détaillé (celui-ci va en mémoire).
- Mentionner le chiffre clé s'il y en a un (ex : "17% → 3% FP").
- Pointer vers un fichier de mémoire si la tâche a généré une investigation longue.

## Invocation sans argument

Si l'utilisateur invoque le skill **sans nommer de tâche** (juste `/maj-todo-list`) :

1. **Scanner la session courante** pour détecter ce qui a été complété/résolu. Chercher les signaux :
   - réalisations concrètes : fichiers créés/modifiés, scripts qui tournent, fix validé, skill créé
   - décisions prises et actées : "on retient X", "on abandonne Y"
   - conclusions d'investigation : "le driver est X", "l'hypothèse Y est écartée"
   - bugs reproduits + fixés dans la session
2. **Lire** Partie 1 du fichier todo et **matcher** chaque réalisation contre les tâches existantes (fuzzy sur les titres + mots-clés).
3. **Proposer une liste numérotée** (max 5) des candidats à marquer comme done, avec :
   - le bullet source dans Partie 1
   - la reformulation proposée en bullet done (résultat synthétique tiré de la session)

   Exemple :
   ```
   Candidats done détectés :
   1. Todo : **Sécurité secrets — étape 1**
      → Done : **Sécurité secrets — étape 1** — `~/Pipeline/export/` migré en `.env` + `chmod 600`.
   2. Todo : **Skill /qc-report**
      → Done : **Skill /qc-report** — créé, 3 sections (mapping, methylation, CNV), testé sur Healthy_826.

   Lesquels valides-tu ? (numéros, "tous", ou "aucun")
   ```
4. **Détecter aussi les tâches faites NON présentes dans la todo** (réalisation mais pas de bullet correspondant). Les proposer comme "nouvelles entrées done" avec thème de la journée, à insérer directement en Partie 2.
5. **Attendre la confirmation** avant d'éditer le fichier.
6. Si **aucun candidat**, dire : "Rien d'évident de terminé dans la session. Dis-moi quelle tâche marquer done."

## Instructions (mode avec argument ou après confirmation)

1. **Identifier la tâche** : prendre l'entrée utilisateur (titre partiel, fuzzy), `Grep` sur le fichier pour localiser le bullet exact dans Partie 1. Si plusieurs matches, demander à l'utilisateur lequel.
2. **Obtenir la date du jour** : `date +%Y-%m-%d`.
3. **Reformuler en bullet done** :
   - Conserver le titre en gras (le raccourcir si besoin).
   - Remplacer la description "à faire" par le résultat/conclusion.
   - Si le résultat n'est pas évident, demander à l'utilisateur en 1 phrase.
4. **Insérer dans Partie 2** :
   - Si la section `## YYYY-MM-DD — ...` du jour existe : ajouter le bullet à la fin de cette section.
   - Sinon : créer une nouvelle section juste après `# Partie 2 — Complété (par jour)` avec le format `## YYYY-MM-DD — {thème court du jour}`. Demander à l'utilisateur le thème si non déduit (ex : "Setup skills", "Debug Bam2Beta").
5. **Supprimer** le bullet correspondant dans Partie 1.
6. **Confirmer** à l'utilisateur : ancien emplacement → nouveau bullet + date.

## Exemples

### Tâche simple

Utilisateur : "maj-todo: Sécurité secrets étape 1 — fait, les exports ont été migrés en .env chmod 600"

Action :
- Retire le bullet `- [ ] **Sécurité secrets — étape 1** ...` de Partie 1 / Haute priorité.
- Ajoute sous `## 2026-04-14 — ...` (crée la section si besoin) :
  ```
  - [x] **Sécurité secrets — étape 1** — `~/Pipeline/export/` migré en `.env` + `chmod 600`.
  ```

### Tâche avec investigation longue

Utilisateur : "maj-todo expérience Apostle vs Maxwell : fait, kit extraction n'est pas le driver principal, c'est le barcoding"

Action :
- Retire le bullet de Partie 1.
- Ajoute :
  ```
  - [x] **Expérience Apostle vs Maxwell** — kit extraction écarté comme driver principal, barcoding NBD114-96 vs NBD114-24 reste suspect #1. Détails dans `~/.claude/projects/-home-blipinski-Pipeline-Bam2Beta/memory/batch-effect-investigation.md`.
  ```

## Anti-patterns

- ❌ Recopier verbatim le bullet "à faire" avec juste `[x]` au lieu de `[ ]` → reformuler en **résultat**
- ❌ Dupliquer l'historique détaillé dans la todo → le détail va en mémoire, la todo garde le résumé
- ❌ Oublier de retirer le bullet de Partie 1 (doublon à faire/fait)
- ❌ Créer plusieurs sections `## YYYY-MM-DD` pour le même jour → fusionner
