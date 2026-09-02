# Context — Bam2Beta — 2026-09-02T17:05

**Branche** : main
**Dernier commit** : 3c84353 — chore(launchers): lanceurs prod sur la release V2.3.0
**Status** : clean, main = origin/main

## Où j'en suis

**V2.3.0 livrée de bout en bout** : restructuration EXIS (fusion QC+BETA+BETA_28M),
raima 0.5.6 = latest (poussé sur Docker Hub), nouvelle métrique amplitude_fragmento_qc
(from-scratch + rétro --RETRO_FRAG_AMPLITUDE), coupe des scores EPIC + CNV raima.
Tag + release GitHub publiés, QUALIF/V2.3.0 écrite (QUALIF OK, marqueurs .done posés),
lanceurs prod bumpés V2.3.0, doc/CHANGELOG/mémoire à jour, worktree restructuration
supprimé. Détail complet : memory/restructuration-v2.3.0.md.

## Ce qui marche / ce qui foire

- ✓ Non-régression prouvée à chaque étage (Run_test_2→9 + final + test + qualif) ;
  concordance metadata.json ↔ fichiers natifs 22/22
- ✓ Amplitudes de référence : Healthy_826 = 236.0128, Lung_9 = 225.7892, Lung_4 = 216.6840
- ✗ trace-prod lit des sorties coupées (checkers.py:91,507 → raima_score.V2.tsv ;
  colonne score_cnv) → colonnes KO sur les futurs samples V2.3.0, à adapter AVANT
  les premiers runs RetD
- ✗ Casse héritée V2.2.0 toujours ouverte : trace-platform/check_platform.py
- ✗ Process rétro RETRO_FRAG_AMPLITUDE jamais exercé en vrai run Nextflow
  (validé via la commande R exacte en docker manuel sur Lung_4)

## Prochaine étape

Backfill amplitude des ~1 500 samples RetD via --RETRO_FRAG_AMPLITUDE (batch glob,
profil scw,docker — d'abord 2-3 samples pour exercer le process NF), et session
trace-prod pour adapter les checkers aux sorties coupées.
