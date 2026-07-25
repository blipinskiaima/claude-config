---
name: weekly-muscu
description: Use when Boris asks about his ZTH training sessions - what to do today/Monday, exercise details (loads, series, reps, rest, warm-up), progression decisions after reporting a performance, or weekly training review. Triggers - "séance", "je fais quoi lundi/mercredi/vendredi", "combien à l'incliné/squat/bench", "j'ai fait X reps", "programme muscu", "échauffement", "progression", "stagnation".
---

<objective>
Ressortir instantanément le programme muscu ZTH de Boris (3 séances/semaine, 5 exercices chacune) : charges, séries × reps, repos, échauffements, techniques d'intensification — selon la semaine en cours (rampe S1, test S2, progression S3+). Enregistrer les performances déclarées et rendre les verdicts de progression selon les règles du PDF.
</objective>

<source-of-truth>
TOUJOURS lire [references/programme-actuel.md](references/programme-actuel.md) ET [references/carnet.md](references/carnet.md) AVANT de répondre — les standards évoluent avec les perfs déclarées, jamais de réponse de mémoire.

Pour les décisions (monter la charge, stagnation, alternatives, déficit) : [references/regles-progression.md](references/regles-progression.md).
</source-of-truth>

<workflow>

## 1. Identifier la demande

| Demande | Action |
|---|---|
| "Je fais quoi lundi ?" / "séance A ?" / "séance du jour ?" | Rendu de la séance (§2) selon la semaine en cours |
| "Combien à l'incliné ?" / détail d'un exercice | Fiche exercice : charges actuelles + schéma + repos + technique |
| "C'est quoi l'échauffement ?" | Gammes montantes du 1er poly de la séance concernée |
| "J'ai fait 70×6 / 65×8 / 60×10" (déclaration de perf) | Logger dans carnet.md + verdict progression (§3) |
| "Bilan de la semaine" | Synthèse du carnet + verdicts + mise à jour des standards |
| "Je stagne sur X" | Règle des 2 semaines + alternative officielle de l'exercice |

Vocabulaire : « séance A » / « séance 1 » / « lundi » = Upper A · « séance jambes » / « séance 2 » / « mercredi » = Lower · « séance B » / « séance 3 » / « vendredi » = Upper B.

## 2. Rendu d'une séance — format

Tableau : `# | Exercice | S1 | S2 | S3 | Repos`, précédé de l'échauffement du 1er poly (gammes montantes chiffrées) et suivi des rappels : arrêt 1 rep avant l'échec technique sur les polys, échec autorisé sur isolations, saisie dans l'app série par série.

Vérifier la date vs la timeline de programme-actuel.md : si on est en semaine 1 → tables rampe ; semaine 2 → standards (test) ; ensuite → standards évolutifs.

## 3. Déclaration de performance — verdict

1. Logger la perf datée dans carnet.md (séance, exercice, séries réalisées)
2. Appliquer les règles de regles-progression.md : haut de fourchette atteint sur une série → +1 incrément sur CETTE série la prochaine fois (progression par série indépendante)
3. Si progression validée → mettre à jour le tableau des standards dans programme-actuel.md + logger le changement
4. Si échec sous la fourchette → rester à la charge, noter ; 2 séances consécutives ratées sur un exercice clé → proposer l'alternative officielle
5. Rappeler le contrat déficit : MAINTENIR = gagné, progresser = bonus

## 4. Règles

- Chiffres : toujours ceux de programme-actuel.md (standards évolutifs), jamais les valeurs historiques de mémoire
- Paliers matériel : barre 2.5 kg · haltères 2 kg (10/12/14, JAMAIS 12.5/15) · machine 5 kg · lest tractions 2.5 kg
- Ne JAMAIS modifier les standards sans une perf déclarée qui le justifie
- Réponses courtes : le tableau, le verdict, le rappel — pas de théorie
- L'app ZTHapp reste le carnet officiel de saisie ; carnet.md est le miroir conversationnel

</workflow>
