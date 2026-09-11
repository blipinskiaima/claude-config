# Context — Aima-Tower — 2026-09-11 (clôture session)

**Branche** : main (poussé, origin/main = ccfdaf7)
**Dernier commit** : ccfdaf7 — feat(qara): comparaison au point fige — v5.7.0
**Status** : clean (hors untracked `Exis 1.1.pdf` et `.claude/worktrees/`,
hors scope depuis le 24/07)

## Où j'en suis
Session en deux temps. D'abord une **enquête** : peut-on recalculer les chiffres
du doc QARA depuis trace-prod ? Réponse établie produit par produit, en lisant
le document par l'API **et** les artefacts figés du pipeline. Puis
l'**implémentation** : `/qara` gagne un interrupteur qui déplie une seconde
rangée de trois box, mesurées sur trace-prod, alignées sur les box figées.
Déployé en v5.7.0, container `healthy`.

## Ce qui marche / ce qui foire
- ✓ **Exis** : aucun calcul maison, `exploratory_service.compute()` aux réglages
  figés. Un seul écart au doc : **+1 cancer prostate** (`Prostate_21`, passé
  cancer le 23/07 après l'émission du PDF). Spécificité identique au chiffre
  près, les 224 sains n'ayant pas bougé.
- ✓ **CUP** : **284/284 mVAF v1.4 identiques** au fichier figé du pipeline,
  aucun changement de strate. Et la **divergence 94/95 du document est
  résolue** : `CGFL_Bladder_Blood_02_094` a un `max_p` exactement au seuil, le
  `>` strict donne les chiffres publiés, le `>=` donne ceux des tableaux.
- ✓ **Alignement structurel** : la carte dynamique réutilise le composant `Kpi`
  et itère sur `p.kpis`. Les deux rangées ne peuvent pas se désaligner.
- ✗ **CUP balanced accuracy 72,9 → 81,3 (+8,4 pt)** : plus gros écart de la
  page, **non expliqué**. La composition par classe de la cohorte a changé, ce
  qui déplace beaucoup une moyenne de rappels.
- ✗ **Cohorte CUP 284 vs 522** : le 284 du doc est un jeu de développement figé,
  pas un filtre reproductible. Les effectifs de strates comparent donc des
  populations de tailles différentes. Documenté, pas résolu.
- ✗ Les 2 tests `test_exploratory_compute.py` restent rouges (383 vs 416),
  **inchangés depuis le 26/08**.
- ⚠ **Themelio n'est pas comparable, et ce n'est pas un défaut** :
  `clinical_config.rds` déclare calibration « 5-fold OOF » (le doc) contre
  production « transfer (full model, not OOF) » (la base) — 54,5 % vs 62,3 % sur
  les mêmes 301 échantillons, **même bundle des deux côtés**.
- ⚠ **Deux erreurs de méthode commises, corrigées** : j'ai joint par
  `sample_name` (non unique : 1531 lignes / 1456 noms) et pris le mauvais
  fichier de référence Themelio, concluant à tort à un score recalculé.
- ⚠ `MEMORY.md` fait **29,6 Ko** pour une limite de chargement de ~24,4 Ko :
  une partie n'est plus lue au démarrage. Signalé deux sessions de suite.

## Prochaine étape
Comprendre le **+8,4 pt de balanced accuracy CUP** — recalculer les rappels par
classe côté figé et côté base pour voir quelle classe bouge. Puis consolider
`MEMORY.md`, qui dépasse sa limite depuis deux sessions. Toujours en suspens
depuis le 26/08 : trancher les 2 snapshots `exploratory` (416/374 en référence,
ou comprendre les +33 samples).
