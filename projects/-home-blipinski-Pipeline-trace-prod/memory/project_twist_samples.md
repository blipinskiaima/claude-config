---
name: ""
metadata: 
  node_type: memory
  originSessionId: c981991f-4725-46fb-89ec-2c8c8270a5f5
---

« twist » n'est **ni un sample_type, ni une cohorte, ni une commande** dans trace-prod (zéro occurrence dans le code). Ce sont des samples `Twist_*` stockés comme `liquid` / `CGFL`, une série de titration pour la validation de la chimie d'enrichissement **Twist** (concurrent de Watchmaker).

**Écart données S3 ↔ base** (juin 2026) : S3 `processed` a 14 dossiers Twist, `data` (raw) en a 13 ; la DB n'en tracke pas tous (un sample n'est checké que s'il est en base, sauf `--new_samples`). État DB : 12 samples après ajout manuel de `Twist_10_7` (`check liquid CGFL -s Twist_10_7` → upsert insère le nouveau). **`Twist_10_5` existe en data (processed+raw) mais reste hors DB** (non ajouté à la demande de Boris). Dossier **`Twist_0%/`** parasite dans processed uniquement (nom malformé, `Twist_0pct` existe déjà proprement) — ne pas y toucher (règle S3).

Samples DB : `Twist_0pct`, `Twist_0_1pct`, `Twist_0_25pct`, `Twist_0_5pct`, `Twist_1pct`, `Twist_10_1/2/3/4/6/7`, `Twist_Diluant_RB`. Profils mVAF ~0 = blanc `Twist_Diluant_RB` **et** `Twist_10_7` (contrôle/négatif attendu).

**Workflow "check twist + export"** :
```bash
python3 database/check_samples.py check liquid CGFL -s Twist_0pct -s Twist_0_1pct -s Twist_0_25pct -s Twist_0_5pct -s Twist_1pct -s Twist_10_1 -s Twist_10_2 -s Twist_10_3 -s Twist_10_4 -s Twist_10_6 -s Twist_Diluant_RB -j 4
python3 database/check_samples.py export liquid CGFL --gsheet
```
Liste à jour : `query "SELECT sample_name FROM samples WHERE LOWER(sample_name) LIKE '%twist%' ORDER BY sample_name"`.

L'export `liquid CGFL --gsheet` pousse **toute** la table liquide CGFL (763 samples), les Twist inclus — il n'est pas filtrable par sample. Voir [[project_columns_index]].
