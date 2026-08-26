---
name: mvaf-v1-4-v1-5-sur-short-read-via-rastair-per-read
description: "Le read-level nécessaire à la v1.4 se récupère avec rastair per-read, pas depuis les CX_report/rastair_call archivés. 3 décisions de reformatage, validées par un gate."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4dc96509-78a0-4f58-b441-f96dfacda724
  modified: 2026-08-26T16:40:21.450Z
---

La mVAF v1.4 exige le détail **par read** (`raima::bootstrap_model_v1` rééchantillonne des reads entiers 200×). Les `CX_report`, `rastair_call` et `.bed.gz` archivés sur S3 sont agrégés par position : l'information est détruite et l'agrégation est irréversible. Il faut repartir du BAM.

**La voie : `rastair per-read`** (sous-commande de rastair 0.8.2, distincte de `rastair call`). Testée et fonctionnelle sur les 3 types de BAM short-read — Methylseq/BWA-mem2, Watchmaker/DRAGEN, 5base/DRAGEN. Pas besoin de tags MM/ML ni de modkit. Protocole complet : `~/Pipeline/short-read/mvaf14_short_read/`.

**Why:** Sans ça on aurait cru devoir écrire un convertisseur MM/ML et brasser 1,5 To de BAM avec `modkit extract full`. `rastair per-read` rend le même read-level directement.

**How to apply:**

Trois décisions de reformatage, chacune trouvée parce que le gate échouait — ne pas les redécouvrir :

1. **Repliage des brins sur la base du génome**, pas sur l'orientation du read. Mesuré : pour les deux orientations, les positions brutes tombent à 48 % sur un CpG brin `+` et 48 % sur un `−`. Règle : `ref[q]=='C'` → garder `q` ; `ref[q]=='G'` → `q−1`.
2. **Dédupliquer les mates.** Fragments cfDNA ~167 bp contre 2×110 bp de reads → 24-28 % des CpG vus deux fois. raima agrège `by (chrom,pos,read_id)` en **sommant** (conçu pour les 2 lignes m/h de modkit), donc un CpG discordant serait appelé méthylé. Une observation par `(read_id, position)`, discordances écartées.
3. **Reproduire le trim m-bias `nOT`/`nOB`** quand la v1 de référence vient de `rastair call` (+32 % d'observations sinon). `TRIM=0` pour les couloirs DRAGEN, dont la v1 vient du `CX_report`.

**Le gate est non négociable** : ré-agréger l'`extract_full` par position doit redonner le `rastair_call` d'origine. Cible atteinte : couverture identique 97,4 %, `n_meth` 98,2 %, corrélation β +0,997.

**v1.4 n'est pas sur la même échelle que v1** — ne pas lire un écart comme un bug. v1 applique la spline `model_v1_to_vaf.rds` ; v1.4 applique `mean(√s)²×100` sur les 200 scores bootstrap, avec la whitelist et `radii=1:100` (contre `1:50`). Rapport v1.4/v1 : **médiane 2,26 sur 1 509 samples ONT** de trace-prod. Pilote Colon_3 : v1 = 18,03 → v1.4 = 42,81, soit 2,37.

**v1.5 = v1.4 au-dessus de ~2 M reads EPIC**, ce n'est pas un bug. `transfo_mvaf_by_cov` est une pénalité de faible couverture : `vmin = exp(−0,55 − 0,64 × nb_read_epic × 21)`. À 4,66 M, `vmin ≈ 4e−28`, la correction s'annule. Le short-read est plus couvert que l'ONT (médiane 1,96 M) donc jamais pénalisé. `nb_read_epic` n'existe pas en short-read : calculé par `samtools view -c -q 20 -F 3844 -L epic850K.extended.100.clean.bed`, divisé par 1e6.

**Limite connue** : `rastair per-read` n'a pas `--min-baseq` (contrairement à `call`), donc les variantes BQ30/BQ40 ne sont pas reproductibles — les 9 variantes methylseq tombent à 3. `--min-mapq` existe, donc QC20/QC30 passent.

Voir [[project_taps_igv_inversion]] pour la question voisine des tags MM/ML.
