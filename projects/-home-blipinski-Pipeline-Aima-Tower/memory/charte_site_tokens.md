---
name: charte-site-tokens
description: "Charte graphique du site officiel Aíma appliquée à la Tour (v5.6.0) : tokens canoniques, alias, sémantique d'état, logos, Plotly, et les pièges rencontrés (navy en texte, logo à fond blanc, color-mix illisible par Plotly)."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-10T15:18:04.292Z
  originSessionId: 13ad22ec-cb9d-4028-8529-0bd5dfcde22f
---

# Charte du site officiel appliquée à la Tour (2026-09-10, v5.6.0)

Demande Boris : réaligner la Tour sur https://preview.aima-diagnostics.com/en, comportement
strictement intact, par une couche de thème centralisée. Quatre checkpoints validés
(accès et outils → charte extraite en tokens → rendu QARA côte à côte → plan de déclinaison),
puis exécution en trois phases. Tag de retour intégral : `pre-charte-site` (= `0379bf9`).

## Ce que le site est, mesuré (Playwright, styles calculés, 5 pages)

- Build Lovable, shadcn + Tailwind v3 ; les noms de couleurs du `tailwind.config` sont lisibles
  dans le bundle CSS (`aima-ink`, `aima-navy`, `aima-magenta`, `aima-cyan`, `aima-blue`,
  `aima-green`, `aima-amber`, `aima-line`, `aima-surface`, `aima-muted`, `aima-faint`…).
- ink `#0A1330` (héros, nav), deep `#101A3D`, abyss `#06091C` (footer), navy `#202A58`
  (= la couleur du **texte**, 101 occurrences), magenta `#E61E45` (CTA, soulignements, verdict
  « high confidence »), magenta-ink `#D91840` (en texte), cyan `#4DD0E1` (eyebrows sur sombre),
  bleu Exís `#3B3BE8`, vert Themélio `#007F41`, ambre `#C79009` / ambre-ink `#8A6400`,
  line `#E7E3EE`, surface `#F7F8FA`, sky `#E9F3FA`, dot `#D3D7E0`, muted `#6E6880`, faint `#736C86`.
- Montserrat (titres : 300 accueil, 700-800 produit), Inter (texte), IBM Plex Mono (labels
  capitales espacées, chiffres). Rayons 9999 boutons/pastilles, 12 tableaux, 16 cartes,
  24 cartes produit. Une seule ombre `0 10px 26px -14px rgb(32 42 88 / .55)`. Transitions 150 ms.
- Verdicts = couleurs : vert sous les seuils, ambre intermédiaire, magenta signal de cancer.
  Figures de la page Technology : plasma sain **navy**, tissu tumoral **magenta**.
- Style : titres en casse de phrase avec point final, eyebrows mono « 01 · Why » / « § The science »,
  point médian séparateur, flèches → ↓ ↗, marques accentuées (Aíma, Themélio, Exís), pastille
  « Research use only » à côté de chaque produit.
- Logos : `aima-logo.png` (couleur, **fond blanc opaque** — navy `#24294F` + rouge `#C93F4E`),
  `aima-logo-blanc.png`, wordmarks `themelio.png` (navy `#001B58` + vert) et `exis.png`
  (navy + bleu `#212CE8`), passés en blanc par `brightness(0) invert(1)` sur fond sombre.
  Pas de logo CUP (le site dit « Exís-ToO »). Trois navys de logo ≠ navy d'interface : ne pas unifier.

## Comment c'est transposé (frontend/src/index.css)

Tokens canoniques + sémantiques + **couche d'alias** : les anciens noms (`--aima-violet-*` →
magenta, `-emerald-*` → vert, `-rose-*`/`-coral-*` → magenta, `-amber-*`, `-indigo-*` → navy,
`-neutral-*` → neutres du site) et les familles Tailwind nommées (`@theme --color-emerald-*`…)
sont dérivés par `color-mix` depuis la couleur pivot. Résultat : les 193 classes Tailwind et les
composants non retouchés suivent la charte sans édition. Décisions Boris : accent magenta partout
où la v4 utilisait son violet ; CUP en cyan sans logo ; sombre conservé = bandeaux ink du site ;
Montserrat via fontsource ; serif supprimé (→ Montserrat 600) ; barres hautes des cartes de
section en **navy** ; grille d'état navy total · bleu en cours · ambre attente · vert succès ·
magenta échec · muted archivé ; orange → ambre, purple/sky → bleu.

## Pièges rencontrés — à ne pas refaire

- ⚠ **Le navy en texte disparaît en sombre** (KPI Plateforme, icônes Tableau de bord invisibles).
  Texte = `--aima-fg-strong` ; navy réservé aux fonds, barres et traces.
- ⚠ **Le logo couleur a un fond blanc opaque** : `brightness-0 invert` en fait un rectangle blanc.
  Sur sombre, passer au fichier blanc (`Logo variant="white"`), jamais un filtre.
- ⚠ **Plotly ne lit ni les custom properties ni `color-mix()`** (calculé en oklab). D'où
  `lib/tokens.ts` (`tokenColor` résout par un élément sonde, `useDarkMode` force le re-rendu) et
  des **hex** pour les accents éclaircis du mode sombre. Côté serveur `exploration_graphs.py`
  porte les mêmes hex.
- ⚠ `lib/theme.ts` existait (gestion dark/light) : je l'ai écrasé avant de le restaurer depuis
  git. Regarder la cible avant tout `write`.
- ⚠ `pkill -f "vite preview"` tue le shell qui contient ce texte : servir en tâche de fond
  séparée et tuer par pid. La preview `vite` avec `/api` proxifié vers le conteneur
  (`172.18.0.2:8050`) permet l'audit de toutes les pages avec données sans rebuild Docker.
- ⚠ L'audit a révélé la panne **trace-prod v34** (`nb_reads_total` renommée) : 5 pages sans
  données, indépendante de la charte, traitée par une session parallèle (worktree `clever-bose`,
  commit `34cbeb2`) qui touchait aussi `ReproChart.tsx`, `SampleDetail.tsx` et
  `exploration_graphs.py`. **Mergée sans conflit** dans `main` (`c3d22e3`) : un seul rebuild a
  déployé correctif et charte ensemble. ⚠ Un chantier de thème qui touche des fichiers de
  données est à séquencer avec les correctifs en cours, pas à déployer en parallèle.
- ⚠ **Un alias ne porte pas le sens de la couleur qu'il remplace.** Vu seulement en ligne, avec
  données : la tuile « Spécificité AI » et le palier 60-80 % de l'échelle d'`/exploration`
  ressortaient en **magenta** (via `--aima-violet-600`), donc en alerte, pour des valeurs
  parfaitement bonnes. Corrigé en `df7159a` (échelle vert · bleu · ambre · magenta comme QARA,
  spécificité et N healthy en `fg-strong`). La couche d'alias fait gagner les 193 classes d'un
  coup, mais **chaque endroit où l'ancienne couleur codait un état demande une relecture**.

Voir aussi : [[qara_refonte_vitrine]] (page pilote), [[reproductibilite_v15_graphe_qc]]
(pièges Plotly de l'échelle log).
