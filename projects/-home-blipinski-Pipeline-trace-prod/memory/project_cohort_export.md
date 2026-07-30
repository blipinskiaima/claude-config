---
name: cohort-export
description: "export-cohort — audit d'inclusion cohorte Sens/Spé (onglet 'Cohort', 1324 lignes liquid, 485 inclus). Le script importe les prédicats d'Aima-Tower au lieu de les réimplémenter ; motifs évalués indépendamment (≠ cascade) donc le PREMIER motif = palier de chute"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4c0cc1e-b20b-4f48-bb7a-87640e0b5b07
  modified: 2026-07-30T21:19:14.361Z
---

# Export Cohort (juillet 2026)

Commande `export-cohort` : rend traçable, sample par sample, pourquoi on passe des 1324
liquides de trace-prod aux **485** retenus dans le calcul de sensibilité/spécificité de la
Tower (mVAF v1.4 / Exis 1.1). Onglet `'Cohort'` de la gsheet trace-prod. **Aucune table
créée** — extraction dérivée, rien de persisté en DB.

**Why:** Boris voulait auditer l'arbre de décision d'inclusion et savoir quelle métadonnée
est responsable de chaque exclusion, avec la valeur de chaque métadonnée déterminante.

## La décision d'architecture qui compte

Trois options se présentaient : réimplémenter l'arbre en SQL dans trace-prod, ajouter une
fonction dans la Tower, ou faire un script trace-prod qui **importe** la Tower. Boris a
tranché pour la 3ᵉ.

Raison : le skill `qara-tower` impose « aucun recalcul maison ». Réimplémenter les ~11
prédicats aurait dupliqué `_prepare_base_dataset`, `_filter_by_version`, `_apply_user_filters`,
`_add_flags`, `_RE_FILTER_CANCER`, `_EXCLUDED_UNIQUE_IDS` — ~200 lignes de règles ISO qui
divergent au premier changement côté Tower. `dev/cohort_extraction.py` les **importe** ;
l'import est lazy dans la commande CLI, donc trace-prod ne casse pas si la Tower est absente.

## Le piège conceptuel : cascade vs multi-motifs

La Tower filtre en **cascade** (un sample écarté au palier N n'est plus évalué ensuite).
Boris voulait TOUS les motifs d'un sample → les prédicats sont évalués **indépendamment**
sur les 1324.

Conséquence à ne pas oublier : **la somme des motifs ne redonne pas les deltas de la
cascade** (un sample en porte souvent 3 ou 4). C'est le **premier motif** d'une ligne qui
indique son palier de chute — les motifs sont listés dans l'ordre des paliers exprès pour ça.
Vérifié : premier-motif → 242/254/25/30/134/63/91, exactement les deltas du Doc QARA.

Un palier n'est pas évaluable sample par sample : le **dédup `unique_id`** (on est écarté
parce qu'un autre run est préféré) → motif relationnel `doublon de {labo}_{nom}`.

## Preuves de fidélité (à refaire si le code Tower bouge)

- Correspondance **nominative** avec `svc.compute_cohort_samples()` : 485 communs, 0 manquant,
  0 en trop, 0 label divergent. C'est LE test — l'égalité des totaux ne prouve rien.
- Les 7 deltas de la cascade reproduits exactement via le premier motif.
- Audit adversarial (12 agents, 7 lots de prédicats) → **0 divergence confirmée**.
- Contrôle élégant trouvé par l'audit : neutraliser `_EXCLUDED_UNIQUE_IDS` fait passer la
  cohorte de 485 à 486, delta = exactement `['CGFL_26BM01841']`.

## Gotchas

- **1324 ≠ toute la base.** `_DUCKDB_QUERY` de la Tower contient déjà
  `WHERE sample_type='liquid'` : les 147 solides ne sont JAMAIS chargés. Le « 1471 » du Doc
  QARA est un comptage externe, pas une étape de la cascade.
- **`get_indications()` ne retourne pas `Lung_Alc`** (les Alcapone sont filtrés en amont, et
  la fonction passe par `_get_prepared_for_graphics` en version `ge5`). Les 229 Alcapone
  reçoivent donc « indication hors-cible (Lung_Alc) » en plus de « cohorte Alcapone » :
  fidèle à la Tower, mais redondant à la lecture. Laissé tel quel.
- **mVAF ~1e-7 écrasés en `0`** : un `f"{v:.6f}"` naïf détruit 6 valeurs réelles
  (`Lung_89` = 4,9e-8). Même philosophie que `format_mvaf4` — jamais de notation
  scientifique, chiffres significatifs pour les très petites valeurs.
- **`cancer_truth` a un 3ᵉ terme** que `metrics-baseline.md` omet : `mutated OR active_cancer
  OR indication ∈ {TNE, Nuclear, Bladder_*}` (`_add_flags`). Se caler sur le code, pas la doc.
- La `vaf` est propagée par `ffill/bfill` par `unique_id` **avant** le dédup — elle peut donc
  venir d'un autre run du même patient et changer `mutated_flag`.
- `sample_centre` = `{sample_name}_{labo}` : clé unique de la feuille (les homonymes
  inter-labos existent, ex `Colon_1` CGFL exclu v4.3.0 / HCL inclus cancer).

Liens : [[project_schema_v20_mito]] (session précédente), [[feedback_status_columns]].
Doc QARA : Google Doc `1dOYIB-NDehUZYsuJi6hKalyG3YpvseSgNCDUqhdtZvs`.
