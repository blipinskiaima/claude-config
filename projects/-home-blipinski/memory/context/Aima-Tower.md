# Context — Aima-Tower — 2026-09-28T14:25+0000

**Branche** : main
**Dernier commit** : ef18387 — docs(indicator): README à jour et version 5.9.0
**Status** : propre (3 non suivis à laisser : `frontend/.apercu/`, `.claude/worktrees/`, `Exis 1.1.pdf`)

## Où j'en suis
Chantier `/indicator` terminé et déployé : page unique, diagramme de flux en frise par mode
d'upload sur les 8 horodatages de trace-platform, détail bulk en flèches sur le temps réel,
Gantt avec barre d'outils. Revue faite élément par élément dans un aperçu commenté (artifact),
tous les fils traités sauf un. 9 commits poussés (`3ddc7d1..ef18387`).

## Ce qui marche / ce qui foire
- ✓ Frise en **moyennes sur les parcours complets** : la somme des segments redonne le temps
  affiché (bulk 4h56 sur 9 échantillons, sample alone 75 min sur 12).
- ✓ Gantt : mode / tri / sens / nombre, vérifiés en headless sur 7 cas.
- ✓ Aperçu commenté (`frontend/.apercu/`, jamais commité) : boucle de revue efficace, à réutiliser.
- ✗ **La 5.9.0 n'est pas déployée** : le conteneur tourne sur `6a97cff`, le pied de page affiche v5.8.0.
- ✗ trace-workflow n'enregistre plus rien depuis le 15/08 : `/monitoring` et le détail par module
  ignorent tout ce qui a tourné depuis.
- ✗ Un fil de commentaire reste ouvert : retirer ou non les petits compteurs sous les indicateurs clés.

## Prochaine étape
Reconstruire et redémarrer le conteneur pour déployer la 5.9.0.
