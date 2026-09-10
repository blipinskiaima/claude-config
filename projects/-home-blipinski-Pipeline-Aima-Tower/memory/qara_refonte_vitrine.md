---
name: qara-refonte-vitrine
description: "Refonte du rendu de /qara pour un lecteur externe : vue d'ensemble, bandeaux, toggle EN/FR, numéros et sources masqués — et la vérification complète contre le Google Doc."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-10T13:54:29.362Z
  originSessionId: 8caa8c85-cc3c-48c2-b136-83f5dc4b6a95
---

# `/qara` — refonte du rendu, v5.5.0 (2026-09-10)

Demande Boris : « plus lisible, plus vendeur, plus intuitif », **périmètre et valeurs
strictement inchangés**. Audience retenue : **externe — investisseur / partenaire**.
`qara-data.ts` n'a pas été touché de la session (prouvé par `git diff`).

## Le fil conducteur : la vitrine ne doit pas devenir un chiffre trompeur

Règle tenue partout, et c'est elle qui a piloté les arbitrages :
**un chiffre phare ne s'affiche jamais sans son dénominateur ni son périmètre.**

Conséquence non négociable sur **CUP** : le bandeau affiche `90.4%` + `top-1 accuracy` +
`stratum (iii) · high confidence · 1 of 3 strata`, et **aucune fraction**. Le document donne
`n = 95` dans ses tableaux §4/§5 et `n = 94` dans sa phrase de conclusion et sa figure —
en afficher un trancherait une divergence que la page a précisément pour consigne de montrer.
Les deux autres tiers de la cohorte sont à 36,8 % et 47,4 % : sortir 90,4 % seul se retourne
contre nous dès que quelqu'un lit le tableau juste en dessous.

⚠ Même piège sur **Themelio §8.1 Stage III = 100 % sur n = 3** : jamais en chiffre phare.

## Ce qui a été ajouté

- **Vue d'ensemble** (onglet par défaut) : 3 cartes cliquables, ordre **Themelio · Exis · CUP**.
  L'ordre vient du tableau `PRODUCTS` de `qara-ui.ts` → cartes ET barre d'onglets suivent
  ensemble, par construction.
- **`ProductBanner`** en tête de chaque onglet produit, même gabarit pour les trois. Avant,
  seul Exis avait des chiffres phares ; Themelio et CUP n'avaient rien à retenir.
- **Toggle EN/FR** (`qara-ui.ts`, défaut `en`, `localStorage` `qara-lang`). ⚠ **Portée
  strictement limitée à l'habillage que nous écrivons.** Intitulés de section, notes, libellés
  de colonne et valeurs restent **en anglais mot pour mot dans les deux langues** — c'est ce
  qui rend la page opposable.

⚠ **`qara-ui.ts` ne contient aucun littéral numérique.** Tous ses chiffres sont *lus* dans
`qara-data.ts` (`SPECIFICITY.n`, `THEMELIO_OVERALL.global.hits`, `CUP_CLASSES.length`…). Les
retaper aurait créé une deuxième copie qui divergerait à la prochaine version du document.
Contrôle : grep de littéraux dans le fichier — seuls restent des identifiants (`Exis 1.1`,
`s1`, `Top-1`, `5-fold`, `(iii)`) et des index de tableau.

## Ce qui a été retiré — décisions explicites de Boris, ne pas revenir dessus seul

| Retiré | Où | Note |
|---|---|---|
| Numéros de section (« 2.1. ») | les 3 onglets | **affichage seulement** — `SectionTitle` retire le préfixe au rendu, `qara-data.ts` garde la chaîne exacte, le survol du titre la redonne |
| Référence au document (`SD-02 · issued … · not recomputed`) | cartes **et** bandeaux | ⚠ plus **aucun** endroit ne relie un chiffre à sa version de document |
| `n = 284` et `n = 95` | schéma de gating CUP | ils étaient **écrits en dur dans le composant** — deuxième copie, et 95 est l'effectif contesté |

⚠ La numérotation avait été **conservée délibérément en août** pour la traçabilité d'audit.
La masquer est un revirement assumé, cohérent avec l'audience externe — d'où le compromis du
survol plutôt qu'une suppression sèche.

## Le bug corrigé : le schéma de gating CUP se contredisait

```
AVANT   max_p ≥ 0.826  →  ┌ (ii)  medium confidence   max_p < 0.826
                          └ (iii) high confidence     max_p ≥ 0.826
        ↑ le libellé de groupe répétait la condition de (iii), donc contredisait (ii)

APRÈS   les 3 strates au même niveau, chacune portant sa propre condition
```

## La vérification finale contre le document

Faite en relisant `Aima_QARA` **en API REST (GET, jamais batchUpdate)**, pattern
[[google_docs_api_read_access]] — 12 onglets lus, comparaison onglet par onglet :

```
Exis · SD-02        60 valeurs / 60 retrouvées
Themelio · SD-04    64 / 64
CUP · SD-03         19 / 19
matrices            3/3 reproduisent exactement accuracy ET balanced accuracy publiées
                    (36,8/30,0 · 47,4/42,5 · 90,4/72,9)
```

⚠ **Une exception subsiste, assumée** : les matrices en mode « row % » (le **défaut**)
affichent **47 pourcentages calculés** par la page (compte ÷ total de ligne). Le document ne
publie que les comptes. Ces comptes sont validés — ils redonnent les exactitudes publiées au
dixième — mais les pourcentages eux-mêmes ne figurent nulle part dans le texte du document.

⚠ **Piège de méthode rencontré** : un premier contrôle « nombre affiché ∈ qara-data.ts » n'a
signalé que **4** valeurs manquantes (25, 26, 56, 59). C'était trompeur — les 43 autres
pourcentages calculés tombent par coïncidence sur des nombres présents ailleurs dans le
fichier. Le vrai décompte (47) s'obtient en comptant les cellules non nulles des matrices,
pas en cherchant les absents.

⚠ Restent **4 seuils écrits en dur** dans `CupTab.tsx` (`mVAF v1.4 > 0`, `≥ 0.32`,
`max_p < 0.826`, `≥ 0.826`). Conformes au document aujourd'hui, mais ils ne suivront pas une
mise à jour de `CUP_STRATA`. Non corrigé, signalé.

## Méthode de travail : aperçu artifact + commentaires

Les 15 itérations de mise en page sont passées par un **artifact publié**
(`claude.ai/code/artifact/97e777e5…`), **généré** — `react-dom/server` rend les vrais
composants, le CSS vient du build vite — et non réécrit à la main, donc zéro valeur ressaisie.
Script `refresh-preview.sh` dans le scratchpad de session : build → rendu SSR → assemblage.
⚠ Dans l'aperçu, les commandes React internes (tri d'Exis §2.2, bascule des matrices CUP) sont
**neutralisées** faute de runtime — le dire quand on commente une capture.

⚠ **Ne pas rebuilder le container à chaque itération** : `docker compose build` refait le
build vite *à l'intérieur de l'image*, soit ~2× le temps de cycle pour rien. Aperçu seul
pendant l'itération (~1 min), rebuild une fois à la fin.

Voir aussi : [[qara_page]] (la page d'origine et le régime de recopie),
[[google_docs_api_read_access]], [[feedback_docs_readonly_and_brevity]].
