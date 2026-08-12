---
name: dashboard-bloc-produits
description: "Bloc « Performance des produits » du Tableau de bord : source unique avec le Profil AIMA, et le piège de la ligne Exis globale qui diverge de /exploration."
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ec5d89-9e21-4626-81f9-57f4f990b853
  modified: 2026-08-12T15:30:01.163Z
---

# Bloc « Performance des produits » — Tableau de bord (2026-08-12)

Cinq lignes intercalées entre les cartes système et le bento Disques/API de `Home.tsx` :
Exis global, Exis CRC / Lung / Pancreas, THEMELIO. Composant `SyntheseProduits`.

## Aucun recalcul — c'est le principe de la page

Tout vient de `/api/competitive/comparaison`, le **même endpoint** que le Profil AIMA.
Le helper de formatage `pct()` a été **sorti** de `AimaComparaison.tsx` vers
`lib/comparaison.ts` et est importé des deux côtés : deux copies auraient divergé.

Une seule chose manquait au payload : le total trace-prod. D'où `_n_trace_prod()` dans
`comparaison_service.py`, qui appelle `database_service.get_stats()["total"]` — la requête
exacte du skill qara-tower (`SELECT COUNT(*) FROM samples`), mais via le service pour
hériter du retry backoff. Un verrou DuckDB masque le compteur, il ne casse pas la Home.

⚠ Le champ est à la **racine** du payload, pas dans `aima` : `_perfs_exis` est mis en cache
par `(cible, cohorte)` et l'y ranger l'aurait figé au premier appel.

## Le piège : une ligne diverge de /exploration, trois non

```
                        Tableau de bord     /exploration (mêmes réglages)
Exis (global)           82,0 % (214/261)    76,2 % (301/395)   ← DIVERGE
Exis CRC                78,6 % (55/70)      78,6 % (55/70)     ✓
Exis Lung               90,6 % (77/85)      90,6 % (77/85)     ✓
Exis Pancreas           60,0 % (9/15)       60,0 % (9/15)      ✓
```

La ligne globale est recomposée par `_perfs_exis` en excluant `indications_exclues`
du référentiel (Bladder_Blood 56, Bladder_Urine 53, Nuclear 15, TNE 10 = 134 cancers,
87 détectés). 395 − 134 = 261 ; 301 − 87 = 214. Les lignes par indication, elles, sont
lues telles quelles dans `by_indication_global`.

Conséquence : quelqu'un qui compare la Home à `/exploration` trouvera trois lignes
identiques et une quatrième qui ne l'est pas. C'est correct, ce n'est pas un bug.

## La spécificité est globale, et c'est pour ça qu'elle se répète

95,1 % (213/224) apparaît sur les quatre lignes Exis. Le seuil est **unique** et calibré
sur les mêmes 224 sains quelle que soit l'indication : il n'y a pas de sains « du côlon »
dans la cohorte, donc **une spécificité du CRC n'existe pas**. Ne pas « corriger » cette
répétition en la calculant par indication — il n'y a rien à calculer.

## Coût

Premier appel après redémarrage du container : **~5,5 s** (chargement DuckDB +
préparation du dataframe). Ensuite ~0,1 s. La Home affiche un skeleton et le reste de
la page rend immédiatement — TanStack Query ne bloque pas.

⚠ Mesure piégeuse : vider `compute.cache_clear()` ne suffit PAS à simuler un démarrage à
froid, le cache de dataframes préparés survit. Seul un container neuf donne le vrai chiffre.

## Décompte affiché

`485 / 1471` = cohorte Exis (261 cancers + 224 sains) sur le total trace-prod. Le sens
n'est plus écrit à l'écran (choix Boris, 2026-08-10) mais reste en infobulle.
THEMELIO ne porte **pas** de décompte : sa cohorte vient du pipeline `Feature/`, pas de
trace-prod, et un total commun laisserait croire à une population unique.

Voir aussi : [[exis_alignment]], [[qara_tower_skill]], [[reproductibilite_seuil_exis]].
