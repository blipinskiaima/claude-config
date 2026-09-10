---
name: schema-v35-qc-80-1000
description: "Schema v35 — reads_primary_80_1000 / depth_80_1000 / coverage_80_1000 dans qc (liquid) : QC apres filtre fragmentomique 80 < L < 1000 sur le BAM merged, calcule hors pipeline, import one-shot sans checker"
metadata:
  type: project
---

# Schema v35 — QC post-filtre fragmentomique 80 < L < 1000 (2026-09-10)

3 colonnes dans `qc`, **liquid uniquement** : `reads_primary_80_1000` INTEGER (molecules A+D),
`depth_80_1000` DECIMAL(10,2), `coverage_80_1000` DECIMAL(5,2) (**en %**, convention
`qc_metrics.coverage_percent`). `NULL` = sample jamais calcule.

**Why:** mesurer l effet du filtre de longueur fragmentomique sur les 3 QC de rendu, sans relancer
Bam2Beta. Le filtre **n existe pas dans le pipeline** — il a fallu le poser pour l occasion.

## La seule vraie question etait : que peut-on tirer de l existant ?

**Rien pour ces 3 metriques.** `Fragmentomics/filtered_softclipped/{ID}.read_lengths.csv` porte bien
toutes les longueurs read par read, mais **une seule colonne** (`read_length`) : aucune position, donc
ni depth ni coverage. Et il est produit avec `-F 3840 -L chr1_22`, donc **la strate A (reads non
alignees) en est absente** alors qu elle compte dans A+D. mosdepth/cramino, eux, agregent : on ne peut
pas retrancher a posteriori la contribution des reads hors 80-1000.

-> **relecture complete des BAM merged obligatoire** (20,96 To, 1378 samples), mais une seule passe
suffit pour les 3. Le pipeline n est pas relance.

## Conventions — validees bit a bit contre le pipeline sur Lung_9

| metrique | filtre | reference | ecart |
|---|---|---|---|
| molecules A+D | `flag & 0x900 == 0` | cramino `num_reads` 37 692 469 | **0** |
| bases | `flag & 1796 == 0`, CIGAR **M/=/X seuls** | mosdepth 6 995 591 241 | **0** |
| depth | bases / 3 099 721 093 | 2.2568 -> 2.26 | **0** |
| coverage | union des intervalles / idem | 0.8295 -> 83 % | conforme |

- ⚠ **mosdepth ne compte PAS les deletions** : sommer `M/D/N/=/X` donne +0,58 %. Seules `M/=/X`.
- ⚠ **Le denominateur n est pas la somme des LN du header** (3 099 922 541) mais **3 099 721 093** :
  mosdepth ecarte 3 contigs (`chrEBV`, `chrUn_KI270396v1`, `chrUn_KI270752v1`, tous a 0 read).
  Ecart 0,0065 %, mais autant prendre la valeur du pipeline.
- Longueur = `length(SEQ) - softclips`, convention `Extract_read` de frag.nf. En filter expression
  samtools c est **`qlen - sclen`** (`qlen` inclut les softclips) — non utilise ici, mais exact.

## Import : one-shot, aucun checker (ecart assume au pattern du projet)

`dev/import_qc_80_1000.py --tsv <fichier>` lit le TSV produit par `/scratch/boris/qc_stat/run.sh`,
resout `sample_id` sur (`sample_name`, `labo`, `liquid`) et appelle `upsert_qc` avec **les 3 clefs
seules** -> les 25 autres colonnes de `qc` sont preservees (`upsert_qc` n ecrit que les clefs fournies).
Idempotent. Aucun `check_*()`, aucun `update-column` : **rien n est publie sur S3**, il n y a donc rien
a lire pour un sample futur, qui restera a NULL jusqu a un nouveau calcul + import manuel.

⚠ La colonne `sample_id` du TSV porte le **nom** du sample, pas l id de la base.

Export : 3 libelles en fin de `_QC_READ_HEADERS` (`Nb molécule 80-1kb`, `Depth 80-1kb`,
`Coverage 80-1kb`). `get_qc_unified()` les remonte **sans edit**, son SELECT etant construit depuis
`QC_COLUMNS` — seul l ajout a cette liste (etape A) est necessaire.

## Le calcul cote Bam2Beta (pour memoire)

`/scratch/boris/qc_stat/` : `metrics.awk` (une passe, union d intervalles en memoire constante) +
`run.sh` (streaming `aws s3 cp - | samtools view -h | mawk`, zero ecriture disque, idempotent).

- **Ne pas telecharger le BAM d abord** : `cp` multipart = 151 Mo/s contre 41 en streaming, mais le
  calcul local (395 s) ne gagne que 24 s sur le streaming (419 s) -> le total est **plus lent**.
- `mawk` vs `gawk` : **+16 % seulement** (339 s contre 395), valeurs identiques. Pas `and()` en mawk
  (tests de bits en arithmetique) et `%.0f` obligatoire, `%d` deborde a 2^31.
- ⚠ **16 flux paralleles est l optimum, 32 s effondre** : les 32 `aws s3 cp` remplissent leurs tampons
  d un coup (pic reseau a 1137 Mo/s, **96 Go de RAM**, idle 0 %), puis le debit tombe a 61 Mo/s.
  A 16 : ~400 Mo/s stables. Ne pas reinstruire.

Voir [[schema-v34-qc-status]] pour la migration precedente, et cote Bam2Beta `read-counting-cascade`
(strates A/B/C/D) et `n50-ratio-qc` (le `read_lengths.csv` et ses limites).
