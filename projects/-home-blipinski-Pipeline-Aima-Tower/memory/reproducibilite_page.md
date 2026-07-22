---
name: reproducibilite-page
description: "Page /reproductibilite : 2 expériences (réplicats purs vs kits d'extraction), sémantique des suffixes de nommage trace-prod, métriques CV/accord, intégration themelio."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1ac897e3-ecbe-4991-b748-6a6308a81fb3
  modified: 2026-07-22T16:14:20.835Z
---

# Page `/reproductibilite` (2026-07-22)

Dispersion de plusieurs mesures d'un **même prélèvement**. Service autonome
`src/reproducibility_service.py`, lecture read-only de trace-prod.

## Sémantique des suffixes trace-prod — établi par archéologie

C'est le cœur de la session : ces conventions ne sont **documentées nulle part**
côté trace-prod, elles ont été reconstruites en croisant code, mémoires et données.

| Suffixe | Ce que c'est | Confiance |
|---|---|---|
| `_rep1`, `_rep2` | Runs de séquençage indépendants (run_id distincts) | certain |
| `_moche`, `_moche_1/2` | Runs indépendants dont les **POD5 étaient rangés hors des chemins standards sur S3** | probable (source : mémoire Pod2Bam `batch-colon.md`) |
| `_rep1_OK`, `_rep2_OK` | **Sous-ensemble du même run** : même `run_id`, barcode perdu, 5-6× moins de reads, créés 3 mois après, aucune ligne `metadata` | déduit des données |
| `bis`/`ter`/`quater` | **Kits d'extraction** : Promega / Macherey-Nagel / Qiagen (base = Apostle) | certain (`metadata.extraction_protocol`) |
| `_rebasecalled_V5.0.0_trimmed` | Même run POD5 retraité avec un dorado plus récent | certain |

**« Moche » ne veut PAS dire mauvaise qualité.** Les chiffres le contredisent :
`Colon_17_moche` est à 2.28× / 82 % de couverture, mieux que `Colon_17_rep1`
(1.56×). C'était mon hypothèse initiale, elle était fausse — ne pas la refaire.
Personne n'a documenté qui a choisi ce mot.

## Les deux expériences sont séparées par le `run_id`

```
Colon_17  PURE          4 run_id distincts, tous Apostle, même barcode19
                        → seul le run varie = reproductibilité analytique

Colon_62  EXTRACTION    1 SEUL run_id, 4 barcodes, 4 kits
                        → la variable "run" est neutralisée = effet du kit
```

Détection de la cohorte extraction : `patient_id` ayant >1 `extraction_protocol`
(critère sémantique, plus robuste qu'un parsing des suffixes). 9 patients,
28 points — dont 4 familles Apostle/Promega **uniquement en v4.3.0**, invisibles
tant qu'on ne coche pas cette version dans le sélecteur dorado.

## Ne pas réutiliser le pipeline /exploration

`_get_prepared` élimine les réplicats à **trois** niveaux : `unique_id` construit
sans le suffixe technique (`exploratory_compute.py:246`), `drop_duplicates("unique_id")`
(l.289), puis `df[~name.contains(_RE_FILTER_CANCER)]` (l.296). C'est délibéré —
`/exploration` mesure la performance clinique, compter deux fois le même patient
serait une faute. D'où un service **séparé**, pas un flag threadé dans les caches.

## themelio n'est pas un modèle concurrent des mVAF

**mVAF v1.4 est l'une des 10 features d'entrée de themelio**
(`screening_top10_xgb/README.md:182-198`). Comparer les deux ne compare donc pas
deux mesures indépendantes : themelio hérite d'une partie de l'instabilité de
v1.4. Interdit de conclure « themelio est plus reproductible » sans précaution.

Seuils cliniques repris du bundle (`releases/themelio_1_0/MANIFEST.md`) :
s1 = 0.9210 (spé 99.55 %), s2 = 0.7250 (98.21 %), calibrés sur 224 sains.
trace-prod ne stocke que le score brut — la catégorie est calculée côté Tower.

## Métriques : méthodologie copiée du R

`_pairwise_agreement` reproduit `pairwise_agreement_rate` de
`exploratory-analysis-CGFL-HCL/bootstrap/R/replicate_utils.R:247` (moyenne sur
les C(n,2) paires). But : que Tower et le R ne divergent pas sur la métrique.
Le R fait déjà cette analyse dans `bootstrap/05_replicate_concordance_98pct.R`.

**Divergence assumée** : le R inclut les `_OK` dans `REPLICATE_SUFFIXES`, Tower
les exclut des stats (ils partagent le run_id → effet de profondeur, pas de
variabilité analytique). Si un jour on veut aligner, c'est le R qu'il faut trancher.

Ordres de grandeur observés : pure CV médian 1.2 % / accord 44/48 ;
extraction CV médian 26.2 % / accord 19/30. **Le kit d'extraction pèse
beaucoup plus lourd que le run.**

## Gotcha test : lock DuckDB

`tests/test_reproducibility.py` a une fixture `svc` qui bascule sur une **copie**
de la base quand un `check_samples.py update-column` tient le lock en écriture.
Sans ça, 22 tests tombent en `IOException` dès qu'un import trace-prod tourne —
ce qui arrive souvent. Le code de prod n'est pas touché.

Voir aussi : [[exploration_score_source_toggle]] (même parsing virgule FR),
[[combined_suspect_tab]] (même archi reader-only).
