---
name: sequencing-time-fastpath
description: "sequencing_time / multi_run — Bam2Beta publie le TSV, trace-prod le lit au lieu de balayer 2,5 Go. Piege de l ecrasement a l upsert (omettre la clef, pas renvoyer KO), clefs en libelles FR, bug DST mesure comme non-declenchant"
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-08T15:29:29.919Z
  originSessionId: a9370b32-1b9e-4964-847d-075c41b1c8aa
---

# sequencing_time — le calcul passe de trace-prod a Bam2Beta (2026-09-08)

Avant : `sequencing_time` et `multi_run` sortaient d un balayage complet de
`QC/Samtools/{ID}.read_start_time.tsv` (2,5 Go/sample, ~9h30 sur la cohorte), lance **a la
main** par `update-column`. Consequence : chaque nouveau sample arrivait avec la colonne
vide, le check de routine ne la remplissait jamais.

```
Bam2Beta  workflow/qc.nf : Read_Start_Time
     samtools view -F 0x900 | awk  ──┬──►  {ID}.read_start_time.tsv   (inchange, ~2,5 Go)
                                     └──►  {ID}.sequencing_time.tsv   (2 lignes, ~58 o)
                                            name / sequencing_time / multi_run
                                     le BAM est deja traverse -> 4 scalaires en plus, gratuit
                          │
trace-prod  lib/checkers.py : scan_read_start_time(sample_dir, sample, allow_scan=True)
                          │
     1. lit {ID}.sequencing_time.tsv (_s3_read_text puis repli local)  ──► retour immediat
     2. allow_scan=False  ──► {'KO','KO'}, on ne lit rien
     3. sinon, balayage complet de read_start_time.tsv (INCHANGE, retro)

     check de routine   -> allow_scan=False   (jamais 2,5 Go, et il tourne a jobs=4)
     update-column      -> allow_scan=True    (defaut, rattrapage des samples anterieurs)
```

## ⚠ LE piege : une clef a 'KO' EFFACE la valeur existante

`_upsert_table` (lib/duckdb.py) construit `ON CONFLICT DO UPDATE SET c = EXCLUDED.c` pour
**toutes** les colonnes presentes dans le dict. **Il n y a aucun skip sur les `None`.**

| ce que rend `check_sample()` | effet sur un sample deja backfille |
|---|---|
| `'KO'` | ecrit `'KO'` -> la vraie duree est **perdue** |
| `None` | ecrit `NULL` -> **perdue** aussi |
| **clef absente du dict** | `_prepare_data` fait `continue` -> colonne hors du `SET` -> **preservee** |

Le « pattern preserve » du projet, c est **omettre la clef**, pas renvoyer une sentinelle.
Le premier jet (renvoyer `'KO'`) aurait efface les 1 362 valeurs du backfill au premier
`check` de routine. D ou le `if rst["sequencing_time"] != "KO":` dans
`LiquidChecker.check_sample()`.

Verifie en reel : `check` sur `Prostate_31` (qui a `60h53m` et pas de TSV) -> valeur intacte.

## ⚠ Les clefs du dict sont les LIBELLES FR

`_prepare_data` itere `TSV_TO_DB_RETD` et cherche ses **membres gauches** dans le dict :
`"Temps Séquençage"` et `"Multi Run"`, PAS `sequencing_time` / `multi_run` (qui sont les
noms de colonnes DB). Une clef en snake_case -> `continue` silencieux, colonne jamais
alimentee, **aucune erreur**.

## Le bug DST : reel en theorie, MESURE comme non-declenchant

`scan_read_start_time` prend `min()`/`max()` sur les **octets bruts** du timestamp, donc en
ordre **lexicographique**, alors qu un run a cheval sur un changement d heure porte deux
offsets. Mesure sur la cohorte (2026-09-08) :

- **0 duree negative** sur les 1 362 valeurs
- **28 runs** traversent une transition : **12 en mars** (avance de l heure, pas d heure
  repetee -> l ordre lexicographique EST l ordre chronologique, immunes par construction) et
  **16 en octobre**
- `Prostate_31` (octobre, 33 317 296 reads, 2,33 Go, offsets `+01:00` ET `+02:00` presents) :
  lexicographique et mktime choisissent **exactement les memes extremes** -> `60h53m`

Le prefixe de date domine la comparaison, donc les extremes sont bien selectionnes. L erreur
n apparait que si le premier ou le dernier read tombe dans le 02:00-03:00 **repete** d octobre.
**Ne pas reinstruire ce sujet** : le nouveau code de `qc.nf` utilise `mktime` (correct par
construction), et les valeurs deja en base sont bonnes -> **aucun backfill n est necessaire**.

Voir [[rarefaction-horaire]] pour le meme `mktime`, ou l enjeu est tout autre (il faut un
**ordre total** sur les reads, pas seulement les 2 extremes).

## multi_run

La fraction de seconde est **constante sur une flow cell** (les timestamps valent
`run_start + N secondes entieres`), elle en est la signature. Deux fractions distinctes = deux
flow cells -> la duree mesuree devient une fenetre calendaire, pas un temps machine.
Timestamp sans fraction (format `...SSZ`, cohorte Lung_Alc) -> `NA`, on ne peut pas trancher.

## Validation de bout en bout (2026-09-08)

`Twist_10_6_rep_3` : DB a `KO` -> depot du TSV sur S3 -> `check` (avec `allow_scan=False`,
donc le balayage est **impossible**) -> `69h07m`/`no`, identique a ce qu un balayage
independant des 681 Mo produit. La boucle pipeline -> trace-prod est prouvee.

Cote perimetre : **liquid uniquement** (decision Boris), `SolidChecker` non cable.
`"Multi Run"` est absent de `_LIQUID_QC` (lib/utils.py) -> il ne sort **pas** dans l export
par sample ; l onglet agrege `run` (`export-run`) porte bien les deux, lus en SQL direct.
Cet onglet agrege par `LIST_DISTINCT` : un run partiellement rempli affiche `"69h07m, KO"`.

Voir [[read-counting-cascade]] pour le `-F 0x900` de `Read_Start_Time` (molecules primaires
A+D), et [[debugging-gotchas]] pour le risque `git add` sur les backups duckdb de trace-prod.
