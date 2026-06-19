---
name: feature-dilution-page
description: "Page /dilution Tower V1 — séries de dilution Twist (trace-prod) en 2 panneaux mVAF v1 + seuil spécificité speedvac. Archi, parsing, gotchas."
metadata: 
  node_type: memory
  type: project
  originSessionId: 525c30ac-f630-40f2-9338-9ebeeaa37b3d
---

# Page `/dilution` — Tower V1 (2026-06-19)

Nouvelle page Tower qui visualise **jusqu'à quelle dilution le signal mVAF v1 reste
au-dessus du seuil de spécificité clinique**, pour les samples **Twist** de trace-prod.
**Affichage seul**, lecture read-only de 2 sources. Spec : [docs/superpowers/specs/2026-06-19-dilution-page-design.md], plan : [docs/superpowers/plans/2026-06-19-dilution-page.md]. Commits `7d7069c`→`23855f5` sur main.

## 2 sources read-only
- **Signal Y** = `qc_metrics.mvaf_v1` (float propre) des samples `sample_name ILIKE 'Twist%'` (trace-prod).
- **Seuil** = `quantile_type1(healthy mVAF v1 train, spec)` sur `~/Pipeline/Feature/result/speedvac_yes/scores.csv` (cohorte std_522). @98%=0.9916, @95%=0.6906, @99%=1.2300.

## Parsing nom de sample (parsable, pas de colonne dédiée)
```
^Twist_10_([1-8])(_rep_2)?$   → dilution dN, série main/rep2
^Twist_Diluant_RB(_rep_2)?$   → Diluant (position finale)
reste (Twist_0_1pct, *pct…)   → ignoré
```
Axe X = **intersection** des points présents dans les 2 séries = `d1..d8 + Diluant` (9 pts).
`Twist_0_1pct` **exclu** (pas de rep_2). `Twist_10_8` (principale) est **prod_status KO** →
`mvaf_v1=null` → trou (`connectgaps:false`) ; rep_2 d8 OK (1.412). Diluant : main RB=0.0, rep2 RB_rep_2=1.28.

## Décisions Boris actées
- **Sélecteur stat mVAF (mvaf_v1) / mVAF v1.3 (mvaf_v13)** ajouté (commits `7246423` back + `964b379` front, 2026-06-19). `mvaf_v1` = qc_metrics (float) ; `mvaf_v13` = retd_suivis (**texte à virgule** → parse). Whitelist `_STATS` dans dilution_service, param `?stat=`. Clé du point renommée `mvaf_v1`→`value`.
- **Le seuil suit la stat affichée** : `mvaf_threshold(speedvac, spec, stat)` lit la colonne correspondante du `scores.csv` Feature (qui contient mvaf_v1 ET mvaf_v13). v1@98=0.9916, v1.3@98=0.9904. Axe X inchangé (présence sample, pas la valeur).
- Layout = **2 panneaux côte à côte**. Toggle spécificité **95/98/99 %**, défaut 98, cohorte seuil **speedvac=yes figée**.
- Hors scope : score combiné (absent trace-prod), séries % de TF (Twist_0pct/0_25pct/0_5pct/1pct), toggle speedvac, réintégration d8 KO.

## Archi (pattern exploration-beta)
- Back : `src/dilution_service.py` (`parse_twist_name`, `DilutionService.get_series`, `mvaf_threshold`), `backend/routers/dilution.py` (`GET /api/dilution/series?spec=`), enregistré dans `backend/main.py`.
- Front : `lib/dilution.ts` (hook `useDilutionSeries`), `components/DilutionChart.tsx` (1 panneau réutilisé ×2), `pages/Dilution.tsx`, route pleine largeur `App.tsx`, item Sidebar `Droplets` (groupe biologie).

## Gotchas
- **`mvaf_threshold` placé dans `dilution_service.py`** (pas `feature_service.py`) car ce dernier était un WIP exploration-beta non commité — éviter de l'emporter dans le commit. Importe `quantile_type1` (stable, HEAD) de `feature_curves`.
- `mvaf_v12`/`ichorcna_score` de trace-prod sont en **texte à virgule** → écartés ; seul `mvaf_v1` (float) utilisé.
- La table `dilution` de trace-prod ne contient PAS les Twist (dilutions in-silico `*_target_*`) ; `probs` = déconvolution tissulaire, pas un score combiné.
- Tests `test_exploratory_compute` : 7 échecs de **dérive de snapshot** (N_Cancer 298→371) pré-existants, sans lien.
