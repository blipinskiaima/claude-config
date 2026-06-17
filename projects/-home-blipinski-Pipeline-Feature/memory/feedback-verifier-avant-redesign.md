---
name: feedback-verifier-avant-redesign
description: "Quand Boris décrit le comportement attendu d'un script, vérifier d'abord si le code y répond DÉJÀ avant de proposer des refontes ou des questions multi-options"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f66bf4f6-be8c-4d91-95f6-baf2e045de16
---

Quand Boris décrit la **spec attendue** d'un script (« no = sans X, yes = tout le monde »), commencer par **vérifier si le code actuel produit déjà ça** — test direct et décisif (ex. égalité/sous-ensemble des `sample_id`, pas juste les effectifs) — AVANT de proposer des designs alternatifs ou un `AskUserQuestion` multi-options.

**Why:** 2026-06-14, debug cohorte speedvac de `select_cohort_train.py`. Une anomalie (8 HCL healthy au lieu de 40) venait d'un champ `cohort=NULL` en DB que Boris a corrigé par backfill trace-prod — pas du code. Au lieu de tester `no ⊂ yes`, j'ai déroulé un comparatif de 3 sémantiques et posé une question de design. Le code était déjà correct (`yes = no + speedvac`, au sample_id près). Boris s'est agacé : il voulait une vérification, pas une refonte.

**How to apply:** sur un « ça inclut/exclut mal X », d'abord reproduire et **prouver** ce que le code fait réellement (subset, diff de sets, counts croisés), confronter à la spec, et seulement si écart réel → proposer un fix. Ne pas dégainer `AskUserQuestion` tant que l'écart code↔spec n'est pas établi. Vérifier aussi l'état **live** de trace-prod (la DB bouge en cours de session). Voir [[feedback-feature-pipeline-design]], [[pipeline-3-etapes]].
