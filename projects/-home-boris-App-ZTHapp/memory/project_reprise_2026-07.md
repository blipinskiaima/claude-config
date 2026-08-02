---
name: reprise-2026-07
description: "Plan de reprise ZTH validé fin juillet 2026 — paramètres, phases, rampe sport, système de suivi hebdo"
metadata: 
  node_type: memory
  type: project
  originSessionId: aba2a68a-e855-4413-8037-928eb06c9aae
  modified: 2026-08-02T09:30:21.103Z
---

# Reprise ZTH — 25 juillet 2026

## Contexte pause
- Pause de 4 semaines (fin juin → fin juillet 2026), PAS 2.5 mois
- Pendant la pause : 1-2 séances/sem à charges légères (poids de la S3 appliqué à toutes les séries), ~7500 pas/j, alimentation libre 2200-2600 kcal 9j/10
- Poids : 64.0 → 64.5 kg (+0.5 kg seulement) → maintenance réelle validée ~2300-2400
- Motivation principale : gras abdominal + arrière des bras ("ailes de chauve-souris"), pas la performance
- Avant la pause : offset glucides −200 actif (template Riz Œuf réduit à 909 kcal, journée ~1805)

## Paramètres recalculés (calculateur ZTH officiel, formules Excel vérifiées)
- **30 ans** (anniversaire passé, confirmé 25/07) · 1.67 m · 64.5 kg · BF ~20 % (photo à refaire)
- Maintenance 2301 kcal · P 100 g / L 62 g verrouillés
- Maintien : G 336 · Déficit P3 (−300) : 2001 kcal, G 261 · Étape 1 si stagnation : 1801, G 211

## Plan validé (audit de conformité PDF fait — session 25/07)
- **Protocole P3 confirmé** (pas P2 — masse musculaire intacte : bench 80, tractions +15, squat 80×10)
- **Restart officiel : lundi 2026-07-27 en DÉFICIT DIRECT 2001 kcal** — Boris a explicitement assumé de zapper les 2 sem de maintien (écart à la lettre du PDF, choix éclairé le 25/07 : son mois de pause à ~2300-2400 poids stable = calibration de facto). Pas de collation (mécanisme du maintien, supprimé). Refeed 2 sem à 2301 après 2 mois de déficit ≈ fin septembre 2026.
- **Repas verrouillés par choix de Boris (setup mono-template)** : midi Raptor Club 896 (pain 156 · poulet 150 · Leerdammer 50 · mayo 15 · 2 tomates · mâche 45) + soir Riz Œuf ajusté 1104 (4 œufs · pomme 250 · 3 tomates · huile 5 g · riz cru 170 g) + collation 16h en maintien seulement (banane 120 · pomme 250 · miel 20 = 303). Pas de rotation.
- **Diagnostic échecs passés (validé avec Boris)** : ~80 % excès sociaux (≥1 resto/sem) + pas à 7500, ~20 % absence de tracking poids/taille dans l'app, 0 % le concept 2 repas. Excès = social.
- **Protocole resto 1×/sem intégré** (PDF p.71-73) : ce jour-là midi = Club Raptor recette 654 kcal, pas de collation, resto le soir sans tracking précis (choix cadrés : viande + pdt/frites, plat+dessert OU entrée+plat, jamais les 3), reprise normale J+1 sans compensation, pas de pesée les 2 jours suivants
- Ajustements templates calculés (L journée = 62 verrouillé) : Riz Œuf pomme 100→250/riz 110→170/huile 15→5 · Pat Œuf pdt 800/h7 · Riz Stk riz 160/h18 · Riz Thon riz 150/h23 · Pat Stk h20 · Pâtes Stk h17 · Spaghettor hors rotation (seul Riz Œuf actif pour l'instant)
- **Gap app découvert : aucun historique de poids ni tour de taille** (profile.weight scalaire) → à implémenter en priorité phase app (le PDF pilote tout sur le poids bas hebdo)
- Refeed : 2 sem à maintien après 2 mois de déficit (≈ S11) — compteur 60j existe dans l'app
- Sport : S1 rampe (pyramides un cran sous les standards : incliné 65/60/55 · tractions +12.5/+10/+7.5 · squat 75×3×10 · OHP 45/40/35 · bench 72.5/65/57.5 ; isolations + techniques d'intensification directes aux standards), S2 = standards de mai complets (test), S3+ progression ZTH normale. En déficit : objectif = MAINTENIR les charges, progresser = bonus.
- 10 000 pas/j dès J1 (écart principal de la pause) · 16/8 (12h→20h) · pesée quotidienne (réf = plus bas hebdo)
- Mensurations hebdo : taille + pectoraux + bras + épaules + jambes (feuille 3 Excel)
- RDL : marge de progression vers 20-30 kg/haltère (PDF p.152), monter 16→18→20 par paliers 2 kg

## Système d'accompagnement (demande explicite de Boris — "être accompagné, un peu perdu")
- Quotidien : saisie app (poids, repas templates, séance, pas)
- **Hebdo (dimanche) : bilan avec Claude Code** — lire les données, appliquer l'arbre de décision PDF (poids bas hebdo, tour de taille, perfs → rien changer / ajuster glucides / refeed)
- Mensuel : photos mêmes conditions + réestimation BF
- Objectif réaliste communiqué : 20 % → ~15 % BF sur le cycle de 12 sem, arrière de bras dessiné vers ~12 % au cycle suivant. Pas de spot reduction (expliqué et accepté).

## Actions app décidées
- Restaurer template riz-oeuf ~1100 kcal (pomme 250 g, riz cru 140 g) — code
- Boris via UI /parametres : poids 64.5, offset glucides → 0
- Chips spawnées : fix context-builder coach (phase_events→phase_history, supplements→taken, skipped flag) + export backup incomplet
- Chantier en cours non committé : scripts/build-knowledge.mjs + 5 docs zth-*.md (base de connaissance Coach IA)

## État au 2026-08-02 — semaine 1 bouclée

**Nutrition — adhérence parfaite.** Raptor Club + Riz Œuf tous les jours du 27 au 31/07, zéro resto, zéro écart. Réel : 2015 kcal/j (P 107 · L 60 · G 263), déficit 286 kcal/j → ~0.26 kg de gras sur la semaine. C'est la première semaine tenue intégralement, alors que le diagnostic du 25/07 attribuait 80 % des échecs passés aux excès sociaux.

**Sport — rampe S1 passée sur les 3 séances** (Upper A 27/07 · Lower 30/07 · Upper B 31/07). 6 standards montés : curl 12→14, RDL 16→18, oiseau 6→8, latérales Raptor S3 14→16, upright row Upper B 10/12/14→12/14/16. Détail et verdicts dans le skill `weekly-muscu`.

**Décisions actées par Boris :**
- Vocabulaire **« palier »** imposé — voir [[vocabulaire-palier]]
- **Quantités figées : riz 170 g / huile 5 g** (a explicitement refusé la version optimisée 160/7). Ne pas reproposer.
- Extensions mollets **remplacées par des dips** en Lower (3 × 10-15, repos 1'30-2') — jamais faites, et les dips servent l'objectif « arrière des bras »
- Riz de référence = étiquette **Curti 349 kcal/100 g, L 0** ≠ générique `app/lib/foods.ts` (340 / L 1.2) → correction applicative en attente

**Absence 03 → 09/08** (déplacement) : aucune séance possible, repas documentés par Boris, calories INCHANGÉES à 2001, aucune compensation au retour (règle PDF p.71).

**Prochaine décision de palier : dimanche 09/08** (J14 du palier 1) — glisse au **23/08** si les données du déplacement sont inexploitables. Le passage au palier 2 n'est PAS automatique : il suppose une stagnation du poids bas ET du tour de taille, avec adhérence vérifiée.
