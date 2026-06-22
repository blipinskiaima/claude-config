---
name: covdepth-qc-valorization
description: Chantier R&D covdepth — valorisation analyse QC depth/coverage par sample + détection anomalies multi-échelle (roadmap) ; Étape 1 LIVRÉE (Fig.1 cumulative + Fig.2 positionnelle multi-échelle, 4 samples)
metadata: 
  node_type: memory
  type: project
  originSessionId: baa0c749-9109-466e-8649-b1ef4f18abb5
---

Chantier démarré le 2026-06-22 (dev Opus 4.8 1M). Workspace local `/scratch/boris/covdepth/{data,result,script}` ; figures finales copiées dans `dev/coverage_analysis/test/` (gitignoré). S'appuie sur l'outil existant [[coverage-analysis-cgfl-hcl]] (binning per-base mosdepth via `bin_one.sh`, helper `save_png()`, exclusion chrX/Y + `total` + alt/random) — ne pas le réinventer.

**Code versionné (décision Boris, option B, 2026-06-22)** : scripts `dev/coverage_analysis/fig1_depth_coverage.R` + `fig2_positional_multiscale.R` (le code, pas les PNG régénérables ; `test/` gitignoré). Limitation : chemins `/scratch` hardcodés dans les scripts (cleanup futur si réutilisation hors machine Boris).

**ROADMAP (prévu, PAS spéculatif maintenant)** : valoriser QC par sample → détecter anomalies sample → détecter tendances multi-échelle (sample → cohorte → indication → labo → multi-labo → tous).

## Étape 1 — LIVRÉE (2026-06-22)

**Fig.1 — cumulative depth-vs-breadth, comparative merged vs epic** (`fig1_depth_coverage.R`). Source = `*.mosdepth.global.dist.txt` (per-base exact, seuils ENTIERS ; pas les bins lissés). Agrégat autosomal pondéré par `length` (summary.txt). Axe X dynamique ~0–6x (sample ~1x), ligne 1x + annotation breadth@1x. **Finding sémantique clé** : mosdepth epic rapporte la proportion à la **longueur du chromosome entier**, PAS à l'empreinte EPIC → même dénominateur que merged, superposition légitime ; epic apparaît basse (~8% @1x vs 58% merged) car l'empreinte = petite fraction du génome.

**Fig.2 — positionnelle multi-échelles** (`fig2_positional_multiscale.R`, args `<sample> <merged|epic>`). Binning de base 100kb (`bin_one.sh`, réutilisé sans modif) agrégé en R par moyenne pondérée vers plusieurs fenêtres (merged 100k/500k/1M ; **epic 500k/1M/5M** car bruit Poisson à ~0.1x — le 100kb epic est un mur illisible, seul le 5Mb est net). Facettes empilées, norm /médiane, pics plafonnés à 2x (sur-couverture = peu utile). **Bandes rouges = déplétion systématique** (fenêtres 1Mb < 0.6× médiane, reportées sur tous les panneaux) — capte les zones non couvertes ; un vrai creux persiste à toutes les échelles, le bruit se lisse.

**Extension (4 samples)** : Fig.2 merged+epic sur 064, 073, 067 + 831 merged. Healthy CGFL liquid (642, 831) n'ont PAS de per-base epic.

**Finding QC majeur — Bladder_Urine_02_067 pathologique** : profondeur ~0.003x (autosomes tous 0.00x). trace-prod `qc_metrics` (DB `trace-prod/database/samples_status.duckdb`, join `qc_metrics.sample_id = samples.id`) : depth=0, coverage_percent=0, MAIS **34.45M reads alignés** (loi d'échelle des autres ~13M reads/x → aurait dû donner ~2.3x). → reads présents mais inexploitables (ultra-courts / dup / QC-fail exclus par mosdepth). **Concordance parfaite mosdepth ↔ trace-prod** sur depth (064:0.99, 073:9.39, 067:0.00, 831:0.71) → validation croisée de la mesure. La comparaison reads-vs-depth est le bon révélateur d'anomalie (un depth=0 seul cache les 34M reads derrière).

Profondeurs samples : 064~1.0x (57% cov), 073~9.5x (excellent, 94% cov), 067~0x (échec), 831~0.7x (46% cov).

Process : Karpathy + gates par phase, validation après chaque modif. Étapes suivantes (cohorte/labo/multi-échelle/détection auto) non encore définies.
