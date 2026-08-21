---
name: mvaf-v1-5
description: "mVAF v1.5 = v1.4 corrigee par la couverture EPIC (raima 0.5.4) — process standard + MVAF15_RETRO, unite en millions, non-regression V1.4 prouvee"
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-21T16:57:12.520Z
  originSessionId: 3b0833c6-9419-4e70-83e7-99e89241db93
---

# mVAF v1.5 — correction par la couverture EPIC (2026-08-20)

**Commite le 2026-08-21 (`983af28`).** Le batch retro a couvert **tout le liquide** : scan S3 du
2026-08-21 -> **1 362/1 362** samples liquid (849 CGFL + 513 HCL) portent `raima_score.V1.4` ET
`V1.5`, aucun ecart de perimetre entre les deux. Les **147 solid CGFL** n'en ont ni l'un ni
l'autre — attendu, `BETA_28M` n'y tourne pas. `raima:0.5.4` reste **locale, non poussee**.

Nouveau score, **derive** de la v1.4 : `raima::transfo_mvaf_by_cov(x, nb_read_epic)`, fonction
ajoutee en **raima 0.5.4** (seul ajout vs 0.5.3). Compense l'exces de faux positifs a basse
couverture. Deux voies, validees identiques sur `Healthy_826`.

```
200 scores bootstrap ──► mean(sqrt(s))^2 x 100 ──► x = mVAF v1.4 ──┐
                                                                    ├──► transfo ──► v1.5
QC/Cramino/{ID}.merged.epic.cramino.tsv col 6 / 1e6 ───────────────┘
```

Formule : `vmin = exp(-0.55 - 0.64 * nb_read_epic * 21)` ;
`res = 0 si x <= vmin, sinon vmin * ((x/vmin)^0.28 - 1)^(1/0.28)` ; `0` si `< 1e-6`.

## ⚠ LE piege : `nb_read_epic` est en MILLIONS

La doc de Florian dit *« as reported in Trace Prod »*, et trace-prod stocke `nb_reads_epic`
**en millions** (`README.md`, fiche `nb_reads_epic` : « Format stockage : Valeur en millions » ;
`format_millions(raw)` dans `checkers_short_read.py:53`). Ses 9 exemples valent 0.1 / 0.5 / 2.

En passant la valeur **brute** (6 561), `exp(-0.64 x 6561 x 21)` fait un underflow a 0, puis
`0 x Inf = NaN`, et la ligne `if (x2 >= 1)` **plante** (`missing value where TRUE/FALSE needed`).
Verifie en R reel. -> `col6 / 1e6` **obligatoire**, dans les 2 scripts.

La correction n'agit que sur la plage **0-3 M** de reads EPIC ; au-dela elle ne fait plus rien.

## Les 2 voies

| | process | script | entree |
|---|---|---|---|
| standard | `bootstrap_model` (modifie) | `bin/bootstrap_model_v1.2.R` | 22 bgzf + cramino EPIC |
| retro | `mvaf_v1_5_retro` (nouveau) | `bin/mvaf_v1_5_from_bootstrap.R` | `BOOTSTRAP/*.bootstrap_v1.tsv` + cramino EPIC |

Les 5 lignes de calcul du script retro sont copiees **verbatim** du v1.2 -> identiques par
construction. Param `--MVAF15_RETRO`. Les 2 process sont sur **`raima:0.5.4`**, image **LOCALE
non poussee** ; `latest` (0.5.3) reste la version de production, intouchee.

## Validation (runs Nextflow reels, Healthy_826)

- V1.5 standard vs V1.5 retro : **`cmp` identiques** (`1.1e-06`)
- V1.4 du run vs V1.4 de QUALIF V2.2.0 : **`cmp` identiques** (`0.58`) — non-regression
- 200 scores bootstrap du jour vs QUALIF de juillet : **`cmp` identiques** -> bootstrap
  deterministe confirme un mois apres

⚠ **`Healthy_826` sature la correction** : 6 561 reads EPIC seulement -> `0.58` devient
`1.1e-06`. L'egalite est prouvee, mais en **regime extreme**. La chaine n'a **jamais ete testee
en regime normal** (2-5 M reads EPIC). Les 9 valeurs de reference de Florian, elles, sont bien
reproduites par le conteneur.

## Les gotchas

- ⚠ **Le V1.4 devait rester bit-a-bit inchangé.** Le premier jet du script (ecrit par Boris)
  faisait `data.frame(name, mvaf1.4 = c(x,x2), model = c("v1.4","v1.5"))` -> la colonne du
  **V1.4** devenait `mvaf1.4`. Or `rapport.nf:77`, `too.nf:49` et `themelio.nf:51` cherchent
  `mvaf` **par nom** ; `c` serait reste non initialise et `$c` aurait rendu la ligne entiere.
  Fix : **deux `data.frame` separes**, colonne `mvaf` dans les deux.
- ⚠ **Les 200 scores sont ecrits a 7 chiffres significatifs** (`write()` de R, `options(digits)`).
  Le standard part des doubles, le retro des valeurs tronquees -> ecart relatif **5e-07**,
  invisible apres `signif(., 2)`. Structurel, non corrigeable sans changer le format d'un
  fichier publie depuis V2.0.0. Boris a tranche : **non significatif**.
- ⚠ **Ancien nommage du cramino EPIC** : `{ID}.epic.cramino.tsv` sans le `.merged` sur les runs
  anciens (verifie sur `Colon_2` CGFL). Repli en dur dans `main.nf`, meme convention que
  trace-prod. **Ne pas confondre** avec les `{ID}.<N>M.epic.cramino.tsv`, qui sont des
  rarefactions. Le **fichier de sortie** garde toujours le nommage `.merged.epic.`.
- ⚠ **Le cramino EPIC vient de `Beta_epic`**, pas de `Beta_28M` -> nouvel emit
  `qc_cramino_epic` dans `beta.nf`, et **`BETA_28M` exige desormais `BETA`** (garde `error`
  explicite dans `main.nf`). Les 3 profils prod/liquid/solid ont deja les deux.
- ⚠ **Le cramino passe dans le MEME tuple que les bgzf** (`tuple val(ID), path(BGZF_FILES),
  path(CRAMINO_EPIC)`) : un 3e argument de process aurait casse l'appel retro existant
  `bootstrap_model(BGZF_RETRO, RAIMA_V1_WL)` de `--bootstrap`.
- ⚠ **`--bootstrap` (R&D) produit desormais le V1.5 lui aussi**, et il **ecrase** deja
  `BOOTSTRAP/` + `BETA/V1.4` — comportement preexistant, distinct de `MVAF15_RETRO`.

## Anti-ecrasement (exigence explicite de Boris)

Triple garde sur `MVAF15_RETRO` : le script R n'ecrit qu'un fichier · filtre amont
`!V1.5.exists()` + `log.warn` · `publishDir ... overwrite: false`. Teste : au 2e passage,
`WARN: MVAF15_RETRO: Healthy_826 ignore (V1.5 deja present, aucun ecrasement)`.

## Le fix qui debloque les batchs

`main.nf` construisait `BAM_FILE` avec `checkIfExists: true` quand `MERGE=false` -> **un seul
sample sans BAM merged tuait tout un run `--input ".../*"`** (plante sur
`Bladder_Urine_02_109`). Passe en `.filter { exists } + log.warn`, meme patron que
[[check-input-qc]] et TOO_RETRO/THEMELIO_RETRO. ⚠ Effet de bord : en mono-sample, un BAM
absent ne leve plus d'erreur, seulement un warning.

⚠ **Le mode retro exige quand meme le BAM merged** dans `params.output` alors qu'aucun process
ne le lit — `BAM_FILE` est construit inconditionnellement. Contrainte preexistante, partagee
avec TOO_RETRO / THEMELIO_RETRO.

Voir [[bootstrap-model-v1]] pour la v1.4 et le bootstrap, [[read-counting-cascade]] pour le
comptage EPIC (`num_reads` = strate D seule sur le BAM EPIC).
