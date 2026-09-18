# Context — Aima-Tower — 2026-09-18 (clôture session)

**Branche** : main (poussé, origin/main = ef54b3b)
**Dernier commit** : ef54b3b — feat(indicator): page de performance du pipeline
en production — v5.8.0
**Status** : clean (hors untracked `Exis 1.1.pdf` et `.claude/worktrees/`,
hors scope depuis le 24/07)

## Où j'en suis
Page `/indicator` créée de bout en bout et déployée (container `healthy`,
v5.8.0) : indicateurs de performance du pipeline sur trace-platform ×
trace-workflow, en deux parties — 10 figures et un diagramme de flux SVG.
Deux refontes après retours de Boris en fin de session : le diagramme rendu
graphique et homogène, puis la dimension « version », qui était câblée dans cinq
figures, remplacée par un **mécanisme de déclinaison unique éteint par défaut**.

## Ce qui marche / ce qui foire
- ✓ **Le détecteur trouve du réel** : `score_cnv` passe de 100 % à 55 % puis
  **0 % à partir de Bam2Beta V2.3.0** — le pipeline a cessé d'écrire la métrique.
  Visible en une case de la grille de couverture, sans l'avoir cherché.
- ✓ **Le flux est mesuré, pas supposé** : `Merge` rang 1 sur 117 workflows, cinq
  branches à 67-100 % de chevauchement, fin de chaîne aux rangs 5-8.
- ✓ 16 tests verts. Les 2 échecs de `test_exploratory_compute` reproduits à
  l'identique sur `pre-indicator` → préexistants, pas de régression.
- ✓ Trouvé en chemin : `/database-platform` était **morte depuis le 17/09**
  (colonne `upload_date` droppée, erreur avalée). Corrigée en session séparée,
  mergée dans main (`081a03f`).
- ✗ **Boris n'a pas encore jugé la page en conditions réelles.** Les deux
  questions de l'étape 5 restent sans réponse : la section A permet-elle de
  repérer une divergence sans la chercher, le diagramme se lit-il sans
  explication.
- ⚠ **Périmètre production = 51 échantillons seulement**, dont 32 d'un compte
  (Imagenome) à la nomenclature de validation. Décision Boris : la base fait foi.
  Les vues par groupe reposent souvent sur 2 à 13 points.
- ⚠ L'endpoint coûte **3,3 s à chaque chargement**, aucun cache serveur.

## Prochaine étape
Recueillir le jugement de Boris sur la page en conditions réelles. Puis, selon sa
réponse, les deux points laissés ouverts : ajouter le **taux de succès** comme
figure déclinée (10 `FAILED` en production, écartée à tort à l'étape 2 sur une
affirmation fausse de ma part), et décider du **cache serveur** sur
`/api/indicator/data`.
