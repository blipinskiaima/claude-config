---
name: profil-aima-sans-comparaison
description: "Page /profil-aima : retrait de toute comparaison chiffrée nous/concurrents, et pourquoi il ne faut pas la réintroduire."
metadata:
  node_type: memory
  type: project
  modified: 2026-08-26T00:00:00.000Z
---

# `/profil-aima` — plus aucune comparaison chiffrée (2026-08-26)

## La décision

Boris : *« il ne sert pas à grand chose d'indiquer l'incomparable »*. Tout ce qui mettait un
de nos chiffres en face d'un chiffre concurrent a été **retiré de l'affichage**.

Retiré, dans `frontend/src/pages/AimaComparaison.tsx` :

| Où | Élément |
|---|---|
| Vue d'ensemble | colonnes **Eux**, **Nous**, **Comparabilité** (7 → 4 colonnes, `colSpan` 7 → 4) |
| Fiche produit | tableau **AIMA / concurrent côte à côte** → devient le concurrent seul, 2 colonnes |
| Fiche produit | ligne **Écart de sensibilité** |
| Fiche produit | **badge de comparabilité** (degré, justification, plafonnement) |
| Fiche produit | badge **point de fonctionnement** (« hors fenêtre · X pts ») |
| Fiche produit | paragraphe « recalculés à LEUR point de fonctionnement » |
| Fiche produit | encart **Différences de mesure** |
| Synthèse | **Verdict chiffré** (« nous devant / derrière », écart, badge « n faible ») |

8 composants devenus orphelins supprimés : `PointDeFonctionnement`, `Ecart`, `COMPARABILITE`,
`ecartNeutre`, `BadgeComparabilite`, `EncartMesures`, `LIBELLE_CHIFFRE`, `VerdictChiffre`.
667 → 462 lignes.

⚠ **`TEINTE_POSITION` est CONSERVÉ** : il sert le bloc « position » (menace directe /
structurelle / repère technologique), qui est un **jugement assumé** — la page l'annonce
elle-même, « notre lecture, pas une mesure ». Ce n'est pas une comparaison chiffrée.

## Ce qu'il ne faut pas faire

⚠ **Ne pas réintroduire** ces éléments sans demande explicite de Boris. Le motif n'est pas
esthétique : nos cohortes ne sont pas les leurs, et deux colonnes en regard **se lisent comme
une mesure commune qui n'existe pas**. C'est la troisième itération dans ce sens — le
2026-07-31 avait déjà sorti l'écart de sensibilité du tableau global et supprimé un badge
« Verdict » qui affichait « comparable » en vert dès que les spécificités s'alignaient.

⚠ **Le backend est inchangé** : `/api/competitive/comparaison` calcule et renvoie toujours
`ecart_sensibilite_pts`, `comparabilite`, `verdict_chiffre`, `recalcule_a_leur_point`,
`specificite_alignee`, `hors_fenetre`, `effectif_faible`. Le retrait est **front pur**, donc
un retour arrière est un revert du commit front — ne pas aller purger le référentiel ni le
service Python en croyant « finir le travail ».

## Pièges rencontrés

⚠ **`/profil-aima` ≠ `/profils`**. `/profil-aima` = cette page (sidebar « Profil AIMA »,
`AimaProfil.tsx`, coquille autour de `AimaComparaison.tsx`). `/profils` = « Deep dive
concurrent » (`CompetitiveProfiles.tsx`, les dossiers markdown P1/P2/P3). J'ai fait un smoke
test sur la mauvaise route avant de m'en apercevoir — les deux renvoient 200.

ℹ `pct()` et `lib/comparaison.ts` sont **partagés avec le bloc « Performance des produits »
du Tableau de bord** ([[dashboard_bloc_produits]]) : ne pas y toucher en nettoyant. Ce bloc
affiche nos chiffres **seuls**, ce n'est pas une comparaison — il n'était pas concerné.

ℹ Le README décrivait encore `/analytics` avec des filtres, un scatter Depth/Coverage, un bar
de distribution et une table — vestiges Dash v2, aucun n'existe en React. Corrigé au passage.

Voir aussi [[dashboard_bloc_produits]], [[analytics_ia_hardening]].
