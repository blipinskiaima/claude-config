---
name: rarefaction-horaire
description: "Les 2 modules de rarefaction TEMPORELLE — RAREFACTION_HORAIRE (12/24/48 h) et RAREFACTION_HORAIRE_THRESHOLD (5/10/15/20 M molecules, seuil 30 M). Gotcha mktime vs ordre lexicographique du st:Z:, validation Breast_11, confondant taille de BAM a palier egal"
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-03T06:14:35.003Z
  originSessionId: 063256a2-6991-468b-9ba9-5931323894e8
---

# Rarefaction temporelle — les 2 modules (2026-09-02)

Meme critere (`st:Z:`, le start time ONT de chaque read), meme origine (le **premier read du BAM**,
pas une heure declaree dans les metadonnees du run), meme nesting par cascade. Deux decoupes :

```
                    BAM merged, reads primaires (-F 0x900), horodates st:Z:
                                        |
        +-------------------------------+-------------------------------+
  RAREFACTION_HORAIRE                              RAREFACTION_HORAIRE_THRESHOLD
  coupe par DUREE : 12 h / 24 h / 48 h             coupe par VOLUME : 5/10/15/20 M molecules
  ecarte un point si duree reelle <= ce point      ne produit RIEN si le sample < 30 M molecules
  workflow/BAM/rarefaction_horaire.nf              workflow/BAM/rarefaction_horaire_threshold.nf
```

Les deux publient dans `{LABO}_rarefaction_horaire[_threshold]/{ID}_{PALIER}/BAM/` via un unique
`publishDir` + `saveAs` qui reconstruit le sous-dossier depuis le nom de fichier. Sortie declaree
par **glob + `optional: true`** : quand rien n'est produit, le process reussit et n'emet rien.
Le warning est un `echo ... | tee -a $LOG >&2` en bash, pas un `log.warn` Nextflow.

## ⚠ LE gotcha : l'ordre lexicographique du st:Z: est faux sur un changement d'heure

`RAREFACTION_HORAIRE` compare des **chaines** et contourne le probleme en reexprimant son seuil
dans chaque offset present (`bounds.txt` / `thr.txt` + `date -d`) — corrige apres 1 h d'erreur
constatee sur `Prostate_31`. `RAREFACTION_HORAIRE_THRESHOLD` a besoin d'un **ordre total**, donc
il convertit en instant absolu directement dans l'awk :

```awk
o  = substr($2, length($2)-5)                       # "+01:00"
ts = substr($2, 1, 19) ; gsub(/[-T:]/," ",ts)
off = (substr(o,1,1)=="-"?-1:1)*(substr(o,2,2)*3600+substr(o,5,2)*60)
print mktime(ts) - off, $1                          # TZ=UTC force
```

**Teste** (2026-09-02, 3 reads sur le passage a l'heure d'hiver, offsets `+02:00` et `+01:00`) :

| read | st:Z: | UTC reel | epoch |
|---|---|---|---|
| A | `2024-10-27T02:59:00+02:00` | 00:59 | 1729990740 |
| B | `2024-10-27T02:01:00+01:00` | 01:01 | 1729990860 |
| C | `2024-10-27T02:30:00+02:00` | 00:30 | 1729989000 |

ordre `mktime` = **C A B** (correct) · ordre lexicographique = **B C A** (place le dernier en
premier). Le bug est donc corrige a la racine, pas contourne.

⚠ Angle mort **commun aux deux modules** : `substr(s, length(s)-5)` suppose un offset `+HH:MM`.
Un timestamp finissant par `Z` casserait le calcul, silencieusement. Jamais rencontre.

## Outillage confirme dans bam2beta:latest (verifie par docker run)

**GNU Awk 5.1.0 avec `mktime` fonctionnel** — donc conversion epoch en une passe, zero fork.
`date -f -` (conversion en batch depuis stdin) marche aussi, en repli. samtools 1.22.1,
GNU sort 8.32. Le container par defaut suffit, aucun `withName` de container n'est necessaire —
seule l'entree de **ressources** l'est (`conf/base.config`, 8 cpu / 8 GB / 2 h).

## Le double comptage, gratuit

Le meme awk qui extrait les `st:Z:` compte les lignes lues (`n`), donc une seule passe donne :

- `TOTAL` = molecules primaires **A+D** (≡ `samtools view -c -F 0x900`, la definition
  « molecules generees » de [[qc-deux-niveaux]]) → **c'est lui qui porte le seuil des 30 M**
- lignes de `st.tsv` = molecules **horodatees**, les seules ordonnables dans le temps

**Resultat inedit : les deux sont EGAUX.** `Breast_11_rebasecalled_V5.0.0_trimmed` 48 578 468 /
48 578 468 · `Colon_1` HCL 68 714 795 / 68 714 795. **100 % des reads primaires portent un
`st:Z:`** — aucun read n'est perdu par l'ordonnancement temporel. Premier chiffre du projet sur
ce point ; l'exclusion silencieuse des reads sans tag dans `RAREFACTION_HORAIRE` est donc, en
pratique, sans effet.

## Validation reelle — Breast_11_rebasecalled_V5.0.0_trimmed (2026-09-02)

48 578 468 molecules ≥ 30 M → les 4 paliers produits. Verification sur les BAM **publies** :

| palier | primaires | horodatees | fenetre |
|---|---:|---:|---:|
| 5M | **5 000 000** | 5 000 000 | 0 → 2 h |
| 10M | **10 000 000** | 10 000 000 | 0 → 5 h |
| 15M | **15 000 000** | 15 000 000 | 0 → 9 h |
| 20M | **20 000 000** | 20 000 000 | 0 → 12 h |

- comptes **exacts au read pres**, pas « environ »
- `MIN_EPOCH` **identique sur les 4** (1750073635) → meme origine
- `MAX_EPOCH` strictement croissant → ce sont des prefixes temporels
- nesting : **0 orphelin** sur 5M⊂10M, 10M⊂15M, 15M⊂20M
- test exact : le BAM 5M est **rigoureusement** l'ensemble des 5 M reads les plus anciens du 20M

**Le debit decroit fortement** : 5 M en 2 h, puis 5 M de plus en 3 h, 4 h, 3 h. Consequence :
sur ce sample le palier **20M tombe a ~12 h**, donc quasi superposable au point `12h` de
`RAREFACTION_HORAIRE`. A savoir en croisant les deux series.

## ⚠ Confondant : a palier egal, les BAM ne pesent pas pareil

| BAM a **20 M molecules** | taille |
|---|---:|
| `Colon_1` HCL | **8,1 Gio** |
| `Breast_15_rebasecalled_V5.0.0_trimmed` | 6,7 Gio |
| `Breast_11_rebasecalled_V5.0.0_trimmed` | 5,9 Gio |

**36 % d'ecart a nombre de molecules identique.** Deux causes : reads plus longs chez HCL
(0,40 Gio/M contre 0,29), et `samtools view -N` selectionnant **par nom**, il ramene aussi les
secondaires et supplementaires — dont la proportion varie par sample (cf. [[read-counting-cascade]]).
« 20 M molecules » ≠ « meme quantite d'ADN sequence ». La comparaison palier vs **run complet du
meme sample** n'est pas affectee ; la comparaison **entre samples a palier egal** l'est.

## Cout : proportionnel au sample, pas au palier

Seul le palier 20M lit le BAM source ; 15M part du 20M, 10M du 15M, 5M du 10M. Le BAM complet est
malgre tout traverse **deux fois** (une pour les `st:Z:`, une pour le palier 20M) — incompressible.
Sur `Colon_1` : 54 Gio traverses contre 24 pour `Breast_15`. Les paliers 5/10/15 coutent en revanche
a peu pres pareil d'un sample a l'autre.

## Tri deterministe obligatoire

`LC_ALL=C sort -k1,1n -k2,2` — la cle secondaire (read_id) n'est pas cosmetique : sans elle,
beaucoup de reads partagent la meme seconde et `head -n` couperait un sous-ensemble **different a
chaque run**. Meme lecon que le tri pre-bootstrap de [[bootstrap-model-v1]] (V2.0.1).

## Etat et suites

- Lanceur `dev/SCW/rarefaction_horaire_threshold.sh` — ecrit et corrige **par Boris**. Le temoin
  d'idempotence doit viser `${ID}_20M` (le palier produit), pas `${ID}_12h`.
- **Le Temps 2 n'existe pas** : le module produit les BAM, pas les scores. Le cahier des charges
  demande un recapitulatif **mVAF v1.4 + v1.5 par palier** → relancer `--EXIS true --MERGE false`
  sur chaque `{ID}_5M`… (`Raima_score_mVAF` sort les deux), puis agreger. Non ecrit.
- Contexte metier : **experience de concordance** des classifications +/- et des scores continus
  vs run complet, sur les samples ≥ 30 M molecules.
- ⚠ Gotcha de debug rencontre : **`docker run` sans `-i` ne connecte pas stdin** → un
  `bash -s <<'EOF'` recoit un script vide et sort en **exit 0 sans rien faire**. Faux positif
  silencieux.

Voir [[rarefaction-cascade]] pour la rarefaction ALEATOIRE (`--RAREFACTIONS`, seed incremente,
probleme tout autre), [[small-fragment-flow]] pour le patron 2-temps, [[read-counting-cascade]]
pour les strates A/B/C/D.
