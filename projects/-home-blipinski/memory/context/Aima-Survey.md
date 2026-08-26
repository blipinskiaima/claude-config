# Context — Aima-Survey — 2026-08-26 (clôture session)

**Branche** : main (poussé, origin/main = 3d9effa)
**Dernier commit** : 3d9effa — feat(concurrence): Biodesix en 8e concurrent + crédibilité
des sources jugée valeur par valeur
**Status** : clean

## Où j'en suis
Session terminée, feuille de route en 6 étapes menée au bout. Biodesix est le 8e concurrent
surveillé : dossier complet en 4 volets dans `concurency/profils/`, visible dans l'onglet
Deep dive concurrent de la Tower, PDF de 19 pages généré. Et le garde-fou `_source_credible`
du collecteur a été corrigé — c'est le vrai apport technique de la session.

## Ce qui marche / ce qui foire
- ✓ Collecte Biodesix : 44 évènements, 3 sources actives, **0 source en échec**. Les 44 ont
  été marqués notifiés sans envoi (demande de Boris) — la file est vide, seuls les vrais
  deltas partiront désormais.
- ✓ ClearNote réparé : la crédibilité se juge valeur par valeur, `publication-sitemap` retiré.
  Simulation du cron quotidien sur les 8 concurrents → **0 source en échec**.
- ✓ 255 tests passent (+3 dont un test de non-régression sur le jugement par valeur).
- ✓ Skill `/deep-dive-concurency` réaligné sur la pratique — 7 dérives corrigées, dont les
  chemins (`profils/` et non `rapports/`), les 4 volets, et les marqueurs de preuve.
- ⚠ Profondeur du canal Biodesix limitée à ~20 communiqués (~10 mois) : leur newsroom ne
  pagine pas. Le début d'une fenêtre à 12 mois n'est couvert que par la SEC.
- ⚠ Le cron tourne à 8h00 Paris alors que ClinicalTrials.gov reconstruit son snapshot vers
  09:00 UTC → on lit J-1 sur cette source. Assumé par défaut, jamais tranché.
- ⚠ Aucune alerte d'échec de cron dans l'écosystème : un job mort reste invisible.

## Prochaine étape
Rien de bloquant. Deux candidats si on reprend ce sujet : trancher l'horaire du cron
concurrentiel (8h00 Paris vs snapshot CT.gov à 09:00 UTC), ou porter une alerte d'échec de
cron — c'est le trou le plus large du dispositif, identifié dès le 28/07 et jamais comblé.
