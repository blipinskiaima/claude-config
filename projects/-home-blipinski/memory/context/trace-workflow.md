# Context — trace-workflow — 2026-06-24

**Branche** : main
**Dernier commit** : 5584f5a — chore: retire skills/agents locaux inutilises (.claude/)
**Status** : clean (analysis/ laissé untracked, volontairement)

## Où j'en suis
Session terminée : rattrapage des workflows 11→24 juin (152 → 1525 en base), gestion
des 4 zombies RUNNING, et implémentation du catch-up paginé du daemon. Tout est commité
et poussé (3 commits découpés). Le daemon prod (PID au moment de la session) tourne
ENCORE l'ancien code en mémoire — le catch-up auto ne s'activera qu'à son redémarrage.

## Ce qui marche / ce qui foire
- ✓ Backfill 11→24 juin : 1525 workflows (user + pipeline-prod), via pagination offset
- ✓ 4 zombies du 17 juin marqués UNKNOWN en base (cancel Tower impossible — runs non orchestrés)
- ✓ Catch-up testé : trou en tête de 250 comblé en 7,5s ; régime normal 0 en 4,4s
- ✓ Doc à jour (README, CLAUDE.md, MEMORY.md), 3 commits poussés sur main
- ✗ Daemon prod PAS redémarré → catch-up au boot inactif tant qu'il tourne l'ancien code
- ⚠ Trou profondément enclavé (>200 workflows sains au-dessus) non couvert par le catch-up auto

## Prochaine étape
Redémarrer le daemon (tmux) pour activer le catch-up au boot — quand Boris le décide
(pas urgent : prod déjà backfillée, aucun trou actuel).
