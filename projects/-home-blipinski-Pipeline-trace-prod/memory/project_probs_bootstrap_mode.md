---
name: probs-bootstrap-mode
description: "Mode probs --probs_bootstrap : remplace les 16 probs epic par la MOYENNE des 200 réplicats bootstrap (BOOTSTRAP/{s}.merged.all.bootstrap_v1.props.tsv), liquid CGFL+HCL, réversible via probs --probs"
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c45c-6098-4ead-86fb-0dfa18961e0a
---

# Mode probs --probs_bootstrap (juillet 2026)

Nouveau **mode** de la commande `probs {type} {labo}` (flag `--probs_bootstrap`) : au lieu de lire `BETA/{s}.merged.epic.props_v1.3.tsv` (1 ligne de valeurs), il calcule la **moyenne colonne par colonne des 200 réplicats bootstrap** dans `BOOTSTRAP/{s}.merged.all.bootstrap_v1.props.tsv` (201 lignes = header + 200 × 16 col epic `blood_0…testis_0`), et **écrase** les 16 colonnes epic de la table `probs`.

**Why:** Boris veut que les probs epic exportées (onglet Prop) soient la moyenne bootstrap (estimation robuste sur 200 rééchantillonnages) plutôt que la valeur `props_v1.3` unique.

**How to apply:**
- Fonction `extract_bootstrap_means(filepath) -> list` (`database/check_samples.py`, à côté de `extract_probs_from_file`) : somme puis moyenne des 200 lignes pour les 16 colonnes, format `.7f` **point** ; retourne `['NA']*16` si fichier absent/invalide.
- Flag `--probs_bootstrap` (`mode_bootstrap`) sur `probs_cmd`. Mode `'bootstrap'` → lit `BOOTSTRAP/{s}.merged.all.bootstrap_v1.props.tsv`, `v1 = extract_bootstrap_means(...)`, `upsert_probs(sample_id, v1, loyfer=None)` (**préserve loyfer**).
- **Samples sans fichier → 16 epic VIDÉES (NULL)** : `extract_bootstrap_means` renvoie `['NA']*16` → `upsert_probs` mappe `NA→NULL`. Écrasement total (moyenne OU NULL), PAS de préservation des probs v1.3 pour les absents (choix Boris).
- Scope : liquid CGFL + HCL. Export : `export --probs --gsheet` (existant, **inchangé**) pousse les moyennes dans l'onglet Prop.
- **Réversible** : re-`probs --probs` (ou `-P`) restaure les probs v1.3 depuis `props_v1.3.tsv`.
- 1 fichier modifié (`check_samples.py`), 5 edits. Aucune nouvelle table/colonne. Checkpoint : tag `checkpoint-pre-probs-bootstrap` + patch `/scratch/boris/trace-mvaf/pre-probs-bootstrap.patch`.

**Gotcha** : `probs -s` est **mono-sample** (click prend le dernier `-s`). Pour tester plusieurs samples ciblés → boucler / 1 par 1. Le backfill complet (sans `-s`) traite tous via `list_samples`.

**Vérifié** : `extract_bootstrap_means` == `awk` indépendant (n=200, 16 moyennes identiques au 10⁻⁷) ; 26BM01841 `blood_0` 0,7996383 (v1.3) → **0,8014998** (moyenne) ; sample sans fichier → NULL ; loyfer préservé. Backfill juillet 2026 : CGFL **791/804** moyennes + 13 vidés, HCL **502/513** + 11 vidés.

Le `.props.tsv` = fichier de la colonne [[schema-v14-bootstrap-props]] (16 col epic × 200 réplicats). Ne pas confondre avec `bootstrap_v1.tsv` (mono-colonne, score bootstrap).
