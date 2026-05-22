---
name: schema-v8-short-read-metrics
description: Schema v8 — nouvelle table short_read_metrics (28 colonnes) + commande CLI check-short-read pour tracker les métriques quantitatives du subsampling 75-200 bp en process indépendant
metadata: 
  node_type: memory
  type: project
  originSessionId: 00451d78-9b15-470b-a881-d5517e6e9b6a
---

# Schema v8 — table `short_read_metrics` (mai 2026)

Nouvelle table DuckDB (28 colonnes) qui stocke les valeurs quantitatives produites par le pipeline short read (subsampling 75-200 bp). Complète [[schema-v7-short-read]] qui ne traçait que le flag OK/KO de complétude.

**Why:** Boris voulait pouvoir comparer les scores produits par le pipeline short read avec ceux du pipeline initial (mVAF v1/v2/v1.2, ichorcna, depth, coverage, probs v1). Process séparé pour ne pas alourdir `check` standard et permettre des cycles d'extraction indépendants à mesure que les calculs short read progressent.

**How to apply:**
- Schéma : `sample_id INTEGER PK FK REFERENCES samples(id)` + 10 colonnes DECIMAL (nb_reads_total/aligned/epic en millions, ratio_percent, depth, coverage_percent, mvaf_v1/v2/v12, ichorcna) + 16 VARCHAR probs v1 epic + updated_at. **Suffixe `_short_read` sur toutes les colonnes** (choix explicite de Boris malgré la redondance avec le nom de table, pour éviter toute ambiguïté en JOIN multi-tables).
- Source S3 : `s3://aima-bam-data/processed/MRD/RetD/liquid/{LABO}_short_read/{sample}/` (pattern fichier `{sample}.minLen75_maxLen200.*`)
- CLI : `check-short-read {liquid} {CGFL|HCL} [-s sample] [-j jobs]` — n'affecte aucune autre table. Source samples : `SELECT FROM samples WHERE sample_type='liquid' AND labo=?`. UPSERT idempotent : sample partiel → NULL par colonne, complété à mesure des reruns.
- Pas d'export gsheet, pas de flag OK/KO (déjà couvert par `retd_suivis.short_read` v7).
- Liquid uniquement (le pipeline short read n'existe pas pour solid).

**Architecture du code — pattern d'héritage strict :**
- Classe dédiée `ShortReadChecker(BaseChecker)` dans `lib/checkers_short_read.py`
- **Hérite directement** : `get_nb_reads_total` (path identique), `get_mvaf(raima_file)` (path en argument), `check_ichorcna` (path identique)
- **Override 4 méthodes seulement** (paths contenant `"merged"` substitué par `self._PREFIX = "minLen75_maxLen200"`) : `get_cramino_reads`, `get_epic_reads`, `get_depth`, `get_coverage`. Code copié 1:1 de `BaseChecker`, seul le préfixe change.
- Si bug fixé un jour dans `BaseChecker.check_ichorcna`, le fix bénéficie automatiquement à `ShortReadChecker`. Aucune duplication parasite.

**PathConfig étendu :** ajout property `short_read_dir = _BASE_PROCESSED / sample_type / f"{labo}_short_read"`.

**Sync delete + compact :** `delete_sample()` et `compact()` mis à jour pour inclure la nouvelle table (sinon perte de données au prochain `clean-database`).

**Gotcha précision ichorcna :** DECIMAL(10,4) tronque les valeurs à 4 décimales (ex: `0.008966 → 0.0090`). Acceptable pour la majorité des tumor fractions, mais si Boris veut préserver les très faibles signaux, bumper en DECIMAL(10,6) via `ALTER TABLE short_read_metrics ALTER COLUMN ichorcna_short_read SET DATA TYPE DECIMAL(10,6)`.

**Coverage initiale (mai 2026, après backfill complet) :**
- CGFL liquid : 426/728 samples avec mvaf_v1 extraite (58% — 302 NULL pipeline pas tourné), 276/426 signal détecté (>0), médiane 1.22, max 75.34
- HCL liquid : 384/471 samples (82% — 87 NULL), 210/384 signal, médiane 0.34, max 19.78
- HCL plus avancé côté pipeline (82% vs 58%), CGFL avec valeurs plus élevées (cohorte chargée Lung-DI/AlCapone)

Liens : [[schema-v7-short-read]] (flag de complétude, table parente), [[columns-index]] (synthèse cross-schemas).
