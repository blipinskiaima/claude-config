---
name: project-schema-v30-v31-sequencing-time
description: "Schema v30/v31 — retd_suivis.sequencing_time (durée du run, XhYm) + multi_run (yes/no/NA), liquid only, depuis QC/Samtools/{s}.read_start_time.tsv. Le fichier n'est PAS trié chronologiquement ET le max n'est pas échantillonnable → scan complet obligatoire (3,44 To, 9h33 de backfill). Les 2 colonnes sortent d'UN seul balayage."
metadata: 
  node_type: memory
  type: project
  originSessionId: 70b8e736-da80-4f70-928e-6bae789746ce
  modified: 2026-09-03T05:58:16.724Z
---

# Schema v30 + v31 — sequencing_time & multi_run (septembre 2026)

Deux colonnes VARCHAR DEFAULT 'KO' dans `retd_suivis`, **liquid uniquement** (0/10 samples solid
sondés ont le fichier source). Hors `STATUS_COLUMNS` et `NUMERIC_COLUMNS` — `XhYm` et `yes`/`no`
sont du texte, `_parse_status` les écraserait en KO (cf [[feedback_status_columns]]).

| Colonne | Valeurs | Header gsheet |
|---|---|---|
| `sequencing_time` | `22h18m` · `KO` | `Temps Séquençage` (col 27) |
| `multi_run` | `yes` · `no` · `NA` · `KO` | `Multi Run` (col 28) |

Source : `{sample}/QC/Samtools/{sample}.read_start_time.tsv` — **pas de header, 2 colonnes**
(read_id UUID 36 car. + timestamp), 22 à 109 M de lignes, **2,53 Go en moyenne, 3,44 To au total**.

## ⚠ Le piège central : ni la 1ʳᵉ/dernière ligne, ni un échantillon ne suffisent

**Le fichier suit l'ordre du BAM (coordonnées génomiques), pas le temps.** Première et dernière
ligne donnent une durée **négative** (mesuré : 5 samples sur 5, de −1h08 à −31h36). La demande
initiale « lire seulement la première et la dernière ligne » est donc irréalisable — vérifié
avant de coder, ce qui a évité une colonne entièrement fausse.

**Plus subtil : le max n'est pas échantillonnable non plus.** Un préfixe de 500 Mo semblait
suffire (3 exacts / 5, 2 à −2 s) — c'était un artefact du petit échantillon. Confronté aux
485 références de Boris, ce préfixe sous-estimait de 1 min à **3h54** (`HCL/Healthy_41` :
66h41 au lieu de 70h35).

Diagnostic par tranches de 10 % : le **min** est capté par *toutes* les tranches, le **max**
par *aucune* (8 tranches sur 10 plafonnent 7 h trop tôt). Cause : le début d'un run produit
des millions de reads, la fin quelques milliers (2,1 M reads/h → 21 k reads/h). **Une queue de
distribution ne s'échantillonne pas.** À rejouer pour toute future colonne de type « max ».

## Coût : plancher physique, ni contournable ni parallélisable

- Lecture **par blocs de 16 Mo** + `min()`/`max()` natifs : **186 Mo/s**, contre 112 Mo/s en
  itérant ligne à ligne. Seul gain d'implémentation réel.
- **Le parallélisme n'apporte rien** : 152 Mo/s agrégé à P=4, contre 130-190 en séquentiel.
  Le lien S3 sature. Inutile de chercher à threader `update-column`.
- **s3fs (`/mnt`), `aws s3api get-object --range` et `aws s3 cp` donnent le même débit**
  (mesuré en alternance sur samples froids : un premier test montrait s3api 40 % devant, la
  contre-épreuve l'a annulé — c'était de la variance réseau). On garde le mount : `open()`
  natif, sans subprocess. ⚠ `_s3_read_text` est **inutilisable** ici (téléchargerait 2,5 Go).
- Backfill réel des 1362 samples : **9 h 33** (CGFL 4h16 + HCL 5h17), 0 erreur.

## Les 2 colonnes sortent d'UN seul balayage

`scan_read_start_time()` (BaseChecker) renvoie `{'sequencing_time', 'multi_run'}` ;
`check_sequencing_time` / `check_multi_run` ne sont que des accesseurs. Le dispatch passe par
`_update_sequencing_time()` (calque `_update_pod5_storage`, type `'sequencing_time'` dans
`COLUMN_CHECKERS` pour **les deux** clés) qui écrit les 2 colonnes en une passe.
**Un checker par colonne aurait doublé un backfill de 9 h.**

## multi_run : la fraction de seconde est la signature du run

Les timestamps valent `run_start + N secondes entières` → **la fraction de seconde est
constante sur tout un run**. Deux fractions distinctes = deux flow cells. Implémenté par
min/max sur `ts[19:26]` dans le même balayage (pas de `set()` : min/max suffit et reste
vectorisable). Validé : `HCL/Colon_4` 2 fractions (`yes`), `HCL/Colon_10` 1 (`no`).

⚠ **`NA` et non `no` quand le timestamp n'a pas de fraction** (format `…SSZ`, les `Lung_Alc`) :
62 samples, dont **12 dépassent 72 h** et sont donc très probablement multi-run — indémontrable
depuis le fichier. Un `no` aurait été un mensonge commode.

**Trois formats de timestamp coexistent** (32 / 29 / 20 caractères, offsets `+01:00` `+02:00`
`+00:00` `Z`). `datetime.fromisoformat` les gère tous en Python 3.12 (le `Z` depuis 3.11).
Le timestamp commence toujours à l'octet 37 (UUID 36 + tab), d'où le garde-fou `ln[36] == 9`
plutôt qu'une position d'offset en dur — c'est exactement ce qui casse dans
`/scratch/rarefaction_horaire/make_slices.sh` (`substr($0,64,6)`, valide pour le seul format 32).
Les extrêmes sont gardés **avec leur offset** pour que la conversion en UTC reste juste sur un
run à cheval sur un changement d'heure.

## Validation croisée — 485/485

`/scratch/rarefaction_horaire/result.csv` (485 samples, calculés par Boris le 26/08 en `awk`,
script non conservé) confronté à la base : **485 identiques, 0 écart sur la durée, 0 sur
multi_run**. Deux implémentations indépendantes. Script : `/scratch/boris/trace-seqtime/verify.py`.

**Contrôle de vraisemblance, plus parlant encore** : les **993 samples `multi_run=no` ne
dépassent jamais 71 h**, exactement la limite d'un run ONT ; les 307 `yes` montent à 148 h.
Un faux négatif de la détection apparaîtrait comme un `no` à 100 h — il n'y en a aucun.

Couverture : **1362/1362, 0 KO**. 307 `yes`, 62 `NA`.

## Gotchas

- ⚠ **`pkill -f <motif>` / `pgrep -f <motif>` matchent leur propre ligne de commande** et tuent
  le shell qui les porte (3 fois de suite ici, exit 144, dont une qui a interrompu le travail en
  cours). Utiliser une classe de caractères : `ps -eo pid,args | grep '[u]pdate-column'`.
- La branche `'checker'` de `update-column` est **séquentielle** : le `-j` est affiché mais
  jamais utilisé. Sans importance ici (le lien sature de toute façon), mais l'estimation de
  durée d'un backfill ne doit pas le supposer parallèle.
- Homonymes inter-labos : `Colon_4` vaut `66h01m`/`no` en CGFL et `58h12m`/`yes` en HCL.
  Toujours discriminer par labo avant de crier à l'écart (cf [[project-schema-v20-mito]]).
- Les `*_rebasecalled_*` ressortent massivement `multi_run=yes` — plausible (un rebasecall
  regroupe les POD5 de plusieurs runs), **non vérifié**.
- Le CSV de référence ne couvre que les samples de la raréfaction horaire : les 45 premiers
  traités (`26BM*`, `ANG-CA*`, `Bladder_Blood_*`) n'y sont pas, la confrontation ne démarre
  qu'aux `Breast_*`.

Tag de rollback `checkpoint-pre-sequencing-time` (sur `c7fb7b4`), backup
`database/samples_status.backup-pre-sequencing-time-20260902_170952.duckdb`.

Liens : [[project_schema_v6_iv_qc]] (la colonne `read_start_time` v6 trace la *présence* du même
fichier, sans le lire), [[feedback_status_columns]], [[project_columns_index]].
