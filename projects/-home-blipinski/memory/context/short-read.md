# Context — short-read — 2026-06-12T16:12+00:00

**Branche** : main
**Dernier commit** : ff753d3 — docs: add IGV TAPS section to README and project CLAUDE.md
**Status** : clean (seul `dl.sh` untracked, préexistant, non lié)

## Où j'en suis
Développé un script standalone pour calculer les **proportions Loyfer** (déconvolution cellulaire) sur les samples short-read du pipeline NF_Watchmaker_Methylseq. Script écrit + **validé** (test de fidélité vs `raima::prop_loyfer` → `max|diff|=0`). Run des 144 combinaisons **interrompu par Boris** (~3/144) → CSV pas encore produit. **En pause jusqu'à lundi 15/06.**

## Ce qui marche / ce qui foire
- ✓ Script : `/scratch/boris/loyfer_short_read/loyfer_methylseq.sh` — flux : `rastair_call.txt → bedmethyl_rastair() → bedMethyl 4col → prop_loyfer (modèle préchargé 1×) → CSV`
- ✓ Déconvolution = copie fidèle de `raima::prop_loyfer` (raima INTACT), `max|diff|=0` sur Colon_25/call
- ✓ Offset calibré = **1** (= défaut ; 86% régions appariées vs 47-48% pour 0/-1)
- ✓ Sources sur mount : `…/Methylseq/rastair/{call,call_20,call_30,call_bq30,call_bq40,call_20_bq30,call_20_bq40,call_30_bq30,call_30_bq40}/{ID}.rastair_call.txt` (16 samples × 9 variantes)
- ✓ Modèle `/mnt/temp/florian/model_loyfer_data.tsv.gz` (133s/chargement → préchargé 1× sinon ~5h) ; image `raima:latest` (prop_loyfer 0.5.0) ; RAM ~8-10G
- ✗ Run 144 interrompu à `Breast_18/call_30` → pas de `prop_loyfer_methylseq.csv`

## Prochaine étape
**Lundi 2026-06-15** : relancer `bash /scratch/boris/loyfer_short_read/loyfer_methylseq.sh` en tmux (~40 min) → sortie `prop_loyfer_methylseq.csv` (144 lignes : `Sample, Variant, <31 types cellulaires>`).
