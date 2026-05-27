---
name: livrables-actuels-du-projet-feature
description: "Référence des dossiers features/combined_v*/ produits, leurs combos NEW vs OLD, leurs KPIs et la décision recommandée. Remplace tableau-final-kpi.md (figé au 7 mai 2026) comme source de vérité actuelle."
metadata: 
  node_type: memory
  type: project
  originSessionId: 21c62b1e-354b-4299-9aec-44b2a439b513
---

# Livrables actuels — projet Feature/

Mis à jour : **2026-05-26**.

Chaque livrable suit la rule 07-feature-structure.md : `compute/ + model/ + eval/ + README + config.yaml`. Tous comparent un combo NEW (avec les nouvelles features testées) vs un combo OLD (baseline immédiatement antérieure) sur la **même cohorte** quand possible.

## Tableau récapitulatif

| Livrable | Date | Nouveauté testée | n NEW vs OLD | KPI cible (Sens@95% Active_NoMut) | Décision |
|---|---|---|---|---|---|
| **combined_v2_probs** | 22/05 | + `probs_epic` (16) + `probs_loyfer` (31) | 480 vs 480 | **71.8% vs 57.3%** (**+14.5 pp**) | ✅ Adopté au pool |
| combined_v3_short_read | 22/05 | + `mvaf_v1_short_read` (couverture 76%) | 365 vs 480 | 74.5% vs 71.8% (biaisé cohortes ≠) | Exploratoire — superseded par v4 |
| **combined_v4_short_read** | 26/05 | + `mvaf_v1_short_read` + `ichor_short_read_x100` (couverture 99.6%) | 478 vs 480 | **76.4% vs 71.8%** (**+4.6 pp**) | ✅ Recommandé adoption pool prod |

## Combos gagnants à retenir

### combined_v2_probs (best post-tri du 19/05)
```
mvaf + frag_diff + frag_mode1 + probs_epic + probs_loyfer       (5 features logiques, 50 cols XGBoost)
AUC ALL = 0.9408 | Sens@95% Active_NoMut = 71.8%
```

### combined_v4_short_read (best avec short_read)
```
mvaf + frag_mode1 + frag_mode2 + ichor_short_read_x100
     + mvaf_v1_short_read + probs_epic + probs_loyfer            (7 features logiques, 52 cols XGBoost)
AUC ALL = 0.9489 | Sens@95% Active_NoMut = 76.4%
```

## Observations clés

- **Probes (v2)** : les blocs probs_epic (16) + probs_loyfer (31) apportent +14.5 pp sur le KPI clé. Ils sont **systématiquement présents** dans tous les top combos. Adoption inconditionnelle.
- **Short_read (v4)** : malgré une corrélation 0.978 (mvaf) et 0.995 (ichor) avec les homologues ONT, l'ajout des 2 features short_read apporte +4.6 pp sur le KPI clé. XGBoost trouve une complémentarité dans les 2-5% de variance Illumina vs ONT.
- **Le combo v4 garde `mvaf` ONT + `mvaf_v1_short_read` ensemble** (= les 2 mVAF en parallèle), mais **remplace** `ichor_x100` ONT par `ichor_short_read_x100`. Subtilité à comprendre.

## Pool actuel (post-26/05)

11 features candidates :
- mvaf [REQUIRED]
- mvaf_v2, ichor_x100, frag_mode1, frag_mode2, frag_diff, loyfer_non_wbc (6 simples ONT)
- probs_epic (bloc 16 EPIC), probs_loyfer (bloc 31 Loyfer)
- mvaf_v1_short_read, ichor_short_read_x100 (2 features short_read)

## Workflow pour nouveau test

Préférer la commande slash :
```
/run-new-feature <nom_feature_1> [<nom_feature_2> ...]
```

Le skill orchestre les 9 briques (refresh_cohort + pool.yaml + snapshot + grid + best combo + livrable + comparison). Cf. `~/.claude/skills/run-new-feature/SKILL.md`.

## Cohortes utilisées

- Toutes les comparaisons des livrables actuels utilisent le **même snapshot du 26/05** (couverture 99.6% short_read) ou le 22/05 pour combined_v2_probs.
- Cohorte effective n=480 (sans features short_read) ou n=478 (avec short_read).
- Filtres analytiques : rep/moche/bis/ter/quater + TNE/Nuclear/Bladder_Blood + depth≥0.25 + dedup unique_id.

## Pour aller plus loin

- Le `tableau-final-kpi.md` du 7 mai 2026 (memory) contient l'historique des tests pré-tri (avec score_cnv, mvaf_v1_20m etc., maintenant retirés du pool). Référence historique seulement.
- La base `experiments/feature_runs.duckdb` contient TOUS les runs (1392 au 26/05) — requêter avec filtre par `n_samples` pour homogénéité.
