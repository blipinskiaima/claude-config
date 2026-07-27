# Context — trace-prod — 2026-07-27T09:55:00+0000

**Branche** : main
**Dernier commit** : 6b22116 — feat: schema v19 — too_predicted_class + too_final_decision
**Status** : clean (synchro origin/main)

## Où j'en suis
Session courte post-v18/v19 : investigation du stockage POD5 de 3 samples CGFL liquid (Bladder_Urine_02_117/118/119). Conclusion : leurs POD5 n'ont jamais été déposés sur Scaleway. Rien d'engagé côté code.

## Ce qui marche / ce qui foire
- ✓ Diagnostic POD5 : les 3 samples sont séquencés (BAM processed 54G/25G/24G) mais sans metadata (run_number NULL) → `update-column stockage_pod5` retourne NULL faute de mapping run.
- ✗ POD5 absents de Scaleway : run PBM55727 (run_id 1ecd4428, séquencé 29/06/2026) introuvable dans `s3://aima-pod-data/data/CGFL/liquid/` ; dernier run déposé = 23/06/2026. Dépôt POD5 manquant en amont, pas un bug trace-prod.
- ✓ /pull-claude : ~/.claude à jour (skills daily-diet/weekly-muscu + mémoires ZTHapp/DCATrack), travail local deep-dive-concurency préservé (non commité).

## Prochaine étape
Rien d'engagé sur trace-prod. Côté POD5 : si Boris veut les récupérer, il faut les redéposer sur Scaleway en amont (question infra/séquençage, pas trace-prod).
