# Format du snapshot et du journal

## Journal `qara/qara_snapshots.jsonl`

- Un fichier JSON Lines dans le repo Aima-Tower, **versionné git** (historique QARA immuable).
- **Une ligne = un point temporel** (T0, T1, …), ajouté par `snapshot.py --persist` /
  `--persist-file`. On n'édite jamais les lignes existantes.
- Le dernier point du fichier est le T_{n-1} auquel `compare.py` compare.

## Schéma d'un snapshot

```json
{
  "timestamp": "2026-07-24T11:11:20Z",         // UTC, date de la mesure
  "reglages": { "score": "mvaf_v14", "cohorte": "advanced",
                "specificite_cible": 0.95, "dorado": ["v5.0.0","v5.2.0"],
                "min_depth": 0.25 },
  "trace_prod": { "total": 1471, "par_type": {"liquid": 1324, "solid": 147} },
  "avances": {
    "seuil": 0.0042,
    "n_cancer": 261, "n_healthy": 224,
    "sensibilite": "82% (214/261)", "specificite": "95.1% (213/224)",
    "mut_high": "100% (107/107)", "mut_low": "78.7% (37/47)",
    "active_no_mut": "65.4% (70/107)",
    "par_indication": {"Lung": "90.6% (77/85)", "Colon": "78.6% (55/70)", ...}
  },
  "precoce": { "n_cancer": 27, "sensibilite": "40.7% (11/27)" },
  "cascade": [ {"name": "trace-prod brut", "n": 1324, "delta": 0}, ... ],   // 14 étapes
  "samples": { "CGFL_Lung_10": "cancer", "HCL_Healthy_5": "sain", ... }      // unique_id → statut
}
```

Les statuts de `samples` sont définis dans
[metrics-baseline.md](metrics-baseline.md) (`cancer` / `sain` / `sans_etiquette` / `precoce`).

## Sortie de `compare.py`

### Cas baseline (journal vide)
```json
{ "de": null, "a": "…", "est_baseline": true,
  "note": "T0 — point de référence initial, aucune comparaison.",
  "baseline": { "trace_prod_total": 1471, "n_cancer": 261, "n_healthy": 224,
                "seuil": 0.0042, "sensibilite": "…", "specificite": "…" } }
```

### Cas comparaison (T_n vs T_{n-1})
```json
{
  "de": "2026-07-24T…", "a": "2026-08-01T…", "est_baseline": false,
  "trace_prod":      { "avant": 1471, "apres": 1476, "delta": 5 },
  "cohorte_cancer":  { "avant": 261,  "apres": 264,  "delta": 3 },
  "cohorte_healthy": { "avant": 224,  "apres": 224,  "delta": 0 },
  "seuil":       { "avant": 0.0042, "apres": 0.0042, "identique": true },
  "sensibilite": { "avant": "82% (214/261)", "apres": "82.2% (217/264)" },
  "specificite": { "avant": "95.1% (213/224)", "apres": "95.1% (213/224)" },
  "par_indication": { "Lung": {"avant": "90.6% (77/85)", "apres": "90.8% (79/87)"} },
  "samples": {
    "n_entrants": 3, "n_sortants": 0, "n_changements": 1,
    "entrants": { "CGFL_Colon_71": "cancer", "HCL_Lung_88": "sans_etiquette", ... },
    "sortants": { },
    "changements_statut": { "CGFL_Prostate_30": {"avant": "sans_etiquette", "apres": "cancer"} }
  }
}
```

## Interprétation pour la synthèse

- **`entrants`** = nouveaux `unique_id` depuis T_{n-1} (nouveaux échantillons séquencés) et
  leur point de chute (cancer / sain / sans-étiquette / précoce).
- **`sortants`** = `unique_id` disparus (rare : renommage, retrait, changement de version
  dorado qui les fait sortir des filtres).
- **`changements_statut`** = échantillons déjà présents dont le statut a bougé, typiquement
  `sans_etiquette → cancer` quand un dossier clinique est complété (cas Prostate_21).

Ces trois listes **expliquent** les deltas agrégés : un `+3` sur `cohorte_cancer` se lit
comme « 2 entrants cancer + 1 changement sans_etiquette→cancer », par exemple.
