---
name: aima-poumon-perfs-par-stade
description: "Les DEUX chiffres poumon d'AIMA, leur ventilation par stade, et le mur de spécificité qui rend toute comparaison concurrente fausse"
metadata: 
  node_type: memory
  type: project
  originSessionId: fdd4f2ac-8635-4303-a86c-70045baa73f3
  modified: 2026-07-28T13:54:37.142Z
---

Établi le 2026-07-28 : PDF Exis 1.1 lu directement + moteur `/exploration` ré-exécuté en
lecture seule sur `trace-prod/database/samples_status.duckdb`. Aucun drift vs le snapshot
QARA du 2026-07-24.

## Deux chiffres, jamais interchangeables

```
POUMON AVANCÉ    90,6 % (77/85)  @ 95,1 % (213/224)   IC95 [82,3;95,8]
   └─ ⚠ 88,2 % de la cohorte est en STADE IV (75/85). C'est une performance de
      maladie métastatique. Stades I et II : n=1 chacun. Ne jamais l'opposer
      à un chiffre de détection précoce.

POUMON Lung-DI   40,7 % (11/27)  @ 95,1 %             IC95 [22,4;61,2]
   ├─ stade I     13,3 % (2/15)  IC95 [1,7;40,5]  ← seul point de contact avec
   ├─ stade II    66,7 % (4/6)                       une revendication "stade I"
   ├─ stade III   66,7 % (2/3)                       concurrente
   └─ stade NR   100 %   (3/3)  ← absent du PDF, produit par le moteur seul
```

⚠ **« Lung-DI précoce » n'est PAS du dépistage.** Exis §2.2 verbatim : *« the lung and bladder
cohorts were assembled in a diagnostic setting, before or during the diagnostic work-up »* —
patients déjà adressés pour suspicion. Le mot « dépistage » figurait à tort dans
`~/.claude/skills/qara-tower/references/metrics-baseline.md:47`, corrigé le 2026-07-28.

## Le mur de spécificité — la vraie raison pour laquelle le tableau comparatif ment

Freenome et DELFI publient **toutes** leurs perfs poumon à **~50 % de spécificité** ; aucune à
≥90 % n'existe. AIMA est à 95,1 %. Freenome stade I = 76,6 % @ 50 %, AIMA stade I = 13,3 % @
95,1 % : **points de fonctionnement différents, pas des performances comparables.**
La question préalable est une décision de positionnement, pas un calcul : à quelle spécificité
AIMA veut-il se comparer ? Reste `[À PRÉCISER]` dans le profil §8.

## Trois blocages que des échantillons supplémentaires ne règlent pas

1. **Biais d'âge de 26 ans** : témoins sains médian 48 ans (37 % ont ≥55 ans), cancers poumon
   médian 74 ans. Notre 95,1 % est mesuré hors de la tranche cible du dépistage (50-74).
2. **Reproductibilité (Exis §2.5)** : CV du mVAF v1.4 de 0 % à **173,1 %**, concordance d'appel
   à **33 %** sur Colon_21. Insoutenable pour des strates de n=3 à 15.
3. **L'organe vient d'une regex** sur le nom d'échantillon (`_RE_INDICATION`,
   `exploratory_compute.py:42`) : sur les 85 « Lung », `metadata.class` dit `Lymphoma` pour 1 et
   `Oropharynx` pour 1.

## Comment les régénérer

```python
sys.path.insert(0, "/home/blipinski/Pipeline/Aima-Tower/src")
from exploratory_compute import ExploratoryAnalysisService
svc = ExploratoryAnalysisService("/home/blipinski/Pipeline/trace-prod/database/samples_status.duckdb")
EXIS = dict(target_specificity=0.95, score_source="mvaf_v14",
            dorado_version=frozenset({"v5.0.0","v5.2.0"}), min_depth=0.25)
svc.compute(**EXIS, cohort_mode="advanced", indications=frozenset({"Lung"}))  # + by_stage_global
svc.compute(**EXIS, cohort_mode="early")
```

⚠ **Jamais en SQL brut** : la cascade Exis compte 14 étapes (dédup, réplicats
`rep|moche|bis|ter|quater`, exclusion `CGFL_26BM01841`, carve-out d'indications). Un `WHERE`
simplifié donne 88 au lieu de 85 et 244 sains au lieu de 224.

Voir [[aima-positioning-profil]], [[delfi_firstlook]], [[freenome-poumon]].
