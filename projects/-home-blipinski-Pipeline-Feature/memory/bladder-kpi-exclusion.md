---
name: bladder-kpi-exclusion
description: Bladder sang exclu du KPI active/active_nomut (flag --exclude-bladder) ; effet contre-intuitif +2 à +6 pts
metadata: 
  node_type: memory
  type: project
  originSessionId: 602fe315-1a98-46cf-8c10-9268c6a7011d
---

Juillet 2026 : flag `--exclude-bladder` ajouté à `eval.R` (défaut OFF, rétro-compat ; activé dans `main.sh`). Retire le Bladder sang (`cohort=='Bladder'`, 52 samples) des unités KPI `active` et `active_nomut`. Aligné rule 04 (exploratory-analysis : sang vs urine, profils trop différents).

**Insight contre-intuitif** : on supposait que les bladder *gonflaient* le Sens_Active_NoMut. C'est l'inverse — ce sont des cas **difficiles** (mVAF faible, ~54 % détectés vs ~61 % global), donc les retirer **augmente** la sensibilité de **+2 à +6 pts** (les deux variantes speedvac). Le KPI « propre » façon exploratory-analysis est donc meilleur, pas pire.

**Portée** : les bladder restent dans le **train** (ils entraînent toujours le modèle XGBoost, 52/294 cancers) — on les retire **uniquement du calcul KPI**, pas du modèle. C'est le « cas 1 » (filtre eval.R seul, pas de retrain) ; le « cas 2 » (modèle entraîné sans bladder) = pipeline entier, question différente.

**Tower** : `eval_kpis.csv` régénéré des 2 variantes → la Tower sert la vue sans-bladder après simple **refresh** (bind mount `/home/blipinski/Pipeline:/pipeline:ro`, lecture fraîche par requête, aucun cache Python, pas de rebuild docker). Backups avec-bladder : `result/speedvac_*/eval_kpis_withbladder_*.csv`.

Voir [[label-definitions]] (canon truth), [[pipeline-3-etapes]] (archi select→train→eval).
