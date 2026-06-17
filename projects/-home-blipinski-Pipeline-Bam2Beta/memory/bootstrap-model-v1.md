---
name: bootstrap-model-v1
description: "Feature bootstrap du score mVAF v1 (raima::bootstrap_model_v1) - process NF, image raima:0.5.2, mode retrospectif --bootstrap, validation bit-a-bit Breast_10 + Lung_138"
metadata: 
  node_type: memory
  type: project
  originSessionId: 93e0e13c-f268-4544-aac0-2e3c49c6277c
---

# Bootstrap model_v1 (2026-06-12)

Bootstrap du score mVAF v1 : `raima::bootstrap_model_v1` rééchantillonne les reads pour produire **200 scores** (distribution du score), au lieu d'une valeur ponctuelle. Sert à quantifier l'incertitude du mVAF.

## Image Docker raima:0.5.2 (bootstrap, parallèle à latest)

- Bootstrap tourne sur une image raima dédiée, séparée de `raima:latest` (0.5.0, prod) qui reste **intacte** (id c69bfa42ec1a).
- `docker/Dockerfile.raima` : COPY/install pointent le tarball raima courant (`raima_0.5.2.tar.gz`) + install R `future` + `withr` (Suggests de raima, donc PAS tirés par l'install raima → ajout explicite ; `bootstrap_model_v1` fait `assert_package("future"/"withr")` au runtime).
- Build : `docker build -t blipinskiaima/raima:0.5.2 -f docker/Dockerfile.raima .` (NE PAS taguer latest).
- **Historique versions image bootstrap** : `0.5.1` (1ère, validée Breast_10) → **`0.5.2`** (courante, validée Lung_138, le 2026-06-17). `bootstrap_model_v1` exporté depuis 0.5.1 (absent de 0.5.0). Pour bumper : changer le tarball dans Dockerfile + `conf/base.config` withName + rebuild avec le nouveau tag.
- Tarball gitignoré, fetché depuis `s3://aima-resources/raima-model/`. Pas pushée sur Docker Hub (build local) → OK mono-nœud SCW ; push requis si run multi-nœuds.

## Process bootstrap_model (workflow/beta_28M.nf)

- Input : `tuple(ID, [22 extract_full_table.bgzf])` (= channel `BGZF_FILE`, le même que `Raima_process_loyfer`) + `path(WHITELIST)`.
- Script `bin/bootstrap_model_v1.R` (calqué sur raima_score_v1_3.R) : `raima::bootstrap_model_v1(paths, ncores=task.cpus, tgz_model_v1_data=whitelist)` puis `write(scores, res_file, ncolumns=1)`.
- Output : `${ID}.merged.all.bootstrap_v1.tsv` (200 lignes) → publishDir `${output}/${ID}/BOOTSTRAP/`.
- `conf/base.config` : `withName: bootstrap_model { container = 'blipinskiaima/raima:0.5.2' ; cpus 10 ; mem 24GB }`.
- Câblé en **from-scratch** dans `workflow Beta_28M` (à côté de Raima_process_loyfer) ET en **rétrospectif** via main.nf.
- `bootstrap_model_v1` : `n_boot=200`, `seed=1` → reproductible. Résultat invariant au `ncores` (juste levier de perf, vérifié par le package).

## Mode rétrospectif --bootstrap (main.nf, miroir de --MVAF1_3)

- `params.bootstrap = false` (nextflow.config). `include { bootstrap_model } from beta_28M.nf`.
- Bloc `if (params.bootstrap)` : collecte `${output}/${ID}/EXTRACT_FULL_28M/${ID}.merged.all.chr{1..22}.extract_full_table.bgzf` (checkIfExists), aucun recalcul.
- Lance : `--bootstrap true --input s3://.../data/$LABO/$TYPE/$ID --output s3://.../RetD/$TYPE/$LABO -profile scw,docker,tower` (profil sans prod/liquid → seul bootstrap tourne).

## Gotcha channel : RAIMA_V1_WL en value channel

- En from-scratch, le whitelist est consommé par 2 process (`Raima_score_v1_3` + `bootstrap_model`) → un queue channel s'épuiserait. Fix : `RAIMA_V1_WL = Channel.fromPath(...).first()` dans main.nf (value channel, réutilisable N fois, n'impacte pas les consommateurs existants).

## Whitelist = params.raima_model_v1_whitelist (décision validée)

- Le défaut littéral de la fonction (`/mnt/temp/florian/model_v1_data_whitelist.tsv.gz`) n'est PAS monté dans le conteneur. On passe `params.raima_model_v1_whitelist` (`/scratch/dependencies/raima-model/model_v1_data_whitelist.tsv.gz`) stagé en input.
- **Équivalence bit-à-bit confirmée** : la dépendance déployée == celle de Florian (sinon les scores divergeraient).

## Validation (2026-06-12 → 2026-06-17)

- **Breast_10** (CGFL liquid, rétrospectif, image 0.5.1) : 200 scores **bit-à-bit identiques** à la réf Florian (`max|Δ|=0`). Valide process + script + future/withr + seed + whitelist.
- **Lung_138** (HCL liquid, rétrospectif, image **0.5.2**) : 200 scores **bit-à-bit identiques** à la réf Florian (`max|Δ|=0`). Valide l'image 0.5.2. (Gotcha lecture réf : l'affichage R démarre à `[1]` ; un copier-coller partiel peut omettre la 1ère ligne → vérifier que le nb de valeurs = 200.)
- Pattern non-régression S3 : `aws s3api list-objects-v2` (Key+Size+ETag+LastModified) avant/après prouve que seul `BOOTSTRAP/*.bootstrap_v1.tsv` est ajouté, tout le reste intact. Script `/tmp/inv_colon2.sh`.
