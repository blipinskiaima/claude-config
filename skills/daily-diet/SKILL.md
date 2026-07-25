---
name: daily-diet
description: Use when Boris asks what to eat today/tonight, wants his daily diet table (journée type ZTH), his calorie/macro targets, the resto-day protocol, or wants to update the diet plan after a weekly bilan (new weight, phase change, refeed, rice option). Triggers - "je mange quoi", "tableau du jour", "mes calories", "journée type", "daily diet", "bilan dominical".
---

<objective>
Ressortir instantanément la journée alimentaire type de Boris (programme ZTH Protocole 3) : tableau détaillé aliment par aliment avec quantités et kcal, sous-totaux par repas, total journée, macros vs cibles de la phase en cours. Gérer aussi les variantes (jour resto, aliments déjà mangés) et la mise à jour du plan aux bilans.
</objective>

<source-of-truth>
TOUJOURS lire [references/plan-actuel.md](references/plan-actuel.md) ET [references/journal.md](references/journal.md) AVANT de répondre — ne jamais répondre de mémoire : le plan change aux bilans, et le journal contient ce que Boris a déjà mangé aujourd'hui.

Pour tout recalcul (nouveau poids, changement de phase, rééquilibrage d'un repas) : [references/formules-zth.md](references/formules-zth.md).
</source-of-truth>

<workflow>

## 1. Identifier le contexte de la demande

| Demande | Action |
|---|---|
| "Je mange quoi ?" (matin, journal vide) | Rendu standard du jour complet (§2) |
| "Je mange quoi ce soir ?" (journal a déjà le midi) | Règle du bloc : afficher le soir ajusté (§3) |
| "J'ai mangé X" (déclaration) | Logger dans journal.md avec kcal, confirmer le reste du jour |
| "C'est jour resto" / "je sors ce soir" | Protocole resto (dans plan-actuel.md) + logger |
| "Bilan : je fais X kg" / changement de phase / option riz | Mode mise à jour (§4) + compresser la semaine dans journal.md |
| "Mes calories ?" / "mes macros ?" | Cibles de la phase en cours + rappel timeline |

## 2. Rendu standard — format exact

Tableau markdown à 4 colonnes : `Repas | Aliment | Quantité | Kcal`.
- Une ligne par aliment, groupées par repas (Midi puis Soir)
- Ligne **Sous-total** par repas, ligne **TOTAL JOURNÉE** en gras
- Sous le tableau : macros du jour vs cibles de la phase (P/L/G)
- Terminer par les pesées critiques et le rappel du jour (pesée matinale, 10 000 pas, dernier repas 20h)

## 3. Règle du bloc (aliment déjà mangé)

La journée est un BLOC : un aliment du template mangé plus tôt dans la journée est RETIRÉ du repas du soir, jamais doublé. Recalculer le soir en soustrayant ce qui figure au journal du jour, afficher le tableau ajusté et vérifier que le total journée retombe sur la cible (±15 kcal).

Principe ZTH inter-jours : **la veille n'influence JAMAIS aujourd'hui** — pas de compensation, pas de report de calories, pas de punition post-écart. Chaque jour est un bloc neuf à la cible de la phase. Seule trace de la veille : lendemain de resto = jour normal strict (et pesée non interprétée pendant 2 jours).

## 4. Mode mise à jour (bilans dominicaux et changements)

1. Lire les deux references
2. Recalculer les cibles avec les formules (nouveau poids/âge/BF → BMR → maintenance → phases)
3. Rééquilibrer les repas selon la méthode du verrou lipides (formules-zth.md §Méthode)
4. Éditer plan-actuel.md : cibles, quantités, timeline, et ajouter une ligne datée au Journal des changements en bas du fichier
5. Ne JAMAIS modifier le plan en dehors d'une demande explicite de Boris — entre deux bilans, rien ne change (règle du programme)

</workflow>

<rules>
- Chiffres kcal/quantités : toujours ceux de plan-actuel.md, jamais approximés de mémoire
- Les protéines et lipides sont VERROUILLÉS ; seuls les glucides varient entre phases (−100 kcal = −25 g G)
- Réponses courtes : le tableau, les macros, les rappels — pas de théorie
- Si la date suggère un changement de phase imminent (voir timeline dans plan-actuel.md), le signaler à Boris
</rules>
