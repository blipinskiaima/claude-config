# Context — Bam2Beta — 2026-07-17T14:38:54+00:00

**Branche** : main
**Dernier commit** : b1a966b — chore(dev): maj scripts SCW + gitignore des bacs a sable
**Status** : clean

## Où j'en suis
Chantier TOO (Tumor of Origin) **TERMINÉ** : les 7 étapes de la roadmap sont livrées.
V2.1.0 taguée, publiée sur GitHub et **qualifiée** (QUALIF/V2.1.0, 27/27 conformes).
Session close proprement — rien en cours, aucun run actif.

## Ce qui marche / ce qui foire
- ✓ **V2.1.0 qualifiée** : QUALIF/V2.1.0 écrit depuis la release GitHub (`-r V2.1.0`), 27 vérifications / 27 conformes. Devient la référence des prochains tests.
- ✓ **Module TOO actif en prod** — 5 classes, gate mVAF 0.32 + max_p 0.8257. Container `too:0.4.1`.
- ✓ **JSON V2 refondu (18 champs)** — BREAKING : `score` supprimé (doublon de `tf`), `model` → `"v1.4"`. Les 2 seuils TOO sortent du **bundle** (`run_too5.R` → CSV → `rapport.nf`), pas d'un param → le JSON ne peut pas contredire la décision qu'il publie.
- ✓ **Qualif refondue** : Lung_9 = 2e sample, 12 valeurs nommées figées, bit-à-bit abandonné (cassait à chaque ajout de champ + ne nommait pas la métrique fautive).
- ✓ Lung_9 bit-à-bit identique au 1er run S3 du 15/07 ; interprétation identique au golden (écarts ≤ 1.6e-03, graine du bootstrap mVAF v1.4).
- ✗ **Bug channel latent non corrigé** sur `RAIMA_MODEL1/2`, `ANCESTRY_MODEL`, `BED`, `FASTA`, `FAI` : queue channel à 1 item consommé en `path()` simple → 1 exécution par invocation. Inoffensif en prod (1 sample/run), casse le multi-samples. Candidat V2.1.1 : `.first()` sur les 6.
- ✗ **3 Rscript/cp pointent vers des fichiers absents** après l'archivage (`bin/archive/`) : `bootstrap_trasnfo.R`, `raima_score_v1_3.R`, `ctdna_report_template.Rmd`. Tous sur chemins morts aujourd'hui — piège si on décommente `beta_28M.nf:43-53`.
- ✗ `maj-bam2beta` utilise `git describe --tags` → attrape les checkpoints (`pre-too`) au lieu des versions. `run-test.sh` filtre correctement avec `git tag -l 'V*'`.

## Prochaine étape
Rien de bloquant sur TOO. Deux chantiers dorment, par ordre d'urgence :
1. **Raréfaction** — les sorties S3 de prod sont FAUSSES (produites avant le fix `b2648b5`) et n'ont jamais été re-générées ; 3 échecs non investigués (Lung_121 / Prostate_45 / Lung_13). Détail versé dans [rarefaction-cascade.md](../../-home-blipinski-Pipeline-Bam2Beta/memory/rarefaction-cascade.md) (section « État opérationnel »).
2. Patch V2.1.1 : `.first()` sur les 6 canaux restants (aucun changement de comportement en prod, débloque le multi-samples).
