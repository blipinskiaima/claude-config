---
name: probs-loyfer-manquantes-d-calage-temporel-d-extraction-pas-un-bug
description: "Loyfer NULL alors qu'epic OK sur des samples rebasecalled → le fichier props_loyfer a été généré APRÈS la dernière passe `probs --probs_loyfer`. upsert_probs préserve loyfer quand on relance en mode v1 seul. Fix = relancer `probs -P`."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 25758bab-c866-4ef4-af5c-beceff3452f8
---

# Probs loyfer manquantes sur rebasecalled (diagnostic juin 2026)

**Symptôme** : N samples (ex: 9 HCL rebasecalled V6.0.0) ont epic v1 OK mais loyfer NULL en DB.

## Cause racine — décalage temporel, PAS un bug

```
Fichier loyfer S3 : EXTRACT_FULL_28M/{sample}.merged.all.props_loyfer.tsv
  - généré APRÈS la dernière passe `probs --probs_loyfer` (ou -P)
  - epic, lui, a été recalculé plus tard (passe v1 seule) → epic OK / loyfer NULL
```

Le témoin : un sample du même lot dont le fichier loyfer existait AU MOMENT de la passe loyfer (Healthy_11, fichier daté plus tôt) a son loyfer ; les autres non.

## Ce que ce n'est PAS (vérifié)

- ❌ Fichier absent → les fichiers loyfer existent bien sur S3 (~820 octets, 2 lignes × 31 col)
- ❌ Parsing cassé → contenu identique au sample témoin qui passe
- ❌ Un recalc epic mode v1 (`props_v1.3`) qui aurait écrasé loyfer → **non** : `upsert_probs` (lib/duckdb.py:956) ne remplit `data` avec les 31 colonnes loyfer **que si `loyfer_values` est fourni**. `_upsert_table` fait un `ON CONFLICT DO UPDATE SET` **ciblé sur les seules colonnes présentes** → mode v1 seul préserve loyfer (et inversement).

## Fix

Relancer l'extraction loyfer (ou concat pour rafraîchir epic v1.3 en même temps) :
```bash
python3 database/check_samples.py probs liquid HCL -P -s {sample}_rebasecalled_V6.0.0
```
puis `export liquid HCL --probs --gsheet`.

## Gotchas commande `probs`

- `-s/--sample` est **mono-sample** (PAS `multiple=True`, contrairement à `update-column`). Pour plusieurs samples → **boucler** (séquentiel, single writer lock DuckDB).
- Modes : `--probs`/`-p` = v1 seul (16 epic, lit `BETA/{s}.merged.epic.props_v1.3.tsv`), `--probs_loyfer` = loyfer seul (31, lit `EXTRACT_FULL_28M/{s}.merged.all.props_loyfer.tsv`), `-P`/`--probs_concat` = les deux.
- Vérif source epic = v1.3 : valeur DB `blood_0` == colonne 1 ligne 2 du `props_v1.3.tsv`.
