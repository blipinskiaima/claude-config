---
name: rarefaction-cascade
description: "Feature rarefaction (workflow/rarefaction.nf) - cascade nestee 20M->10M->5M->2M->1M via samtools -s, 2 temps facon small_fragment. GOTCHA majeur : samtools view -s utilise un hash ABSOLU du read-name sur [0,1) ; meme seed en cascade = seuils composes en MIN -> comptes faux (frac x N_merged au lieu de frac x fichier_courant). Fix : seed INCREMENTE par niveau. Valide bit-a-bit (comptes +/-0.13%, nesting 0 orphelin)."
metadata: 
  node_type: memory
  type: project
  originSessionId: a50bef91-57d2-4179-a3ce-1e0492eeca76
---

# Rarefaction cascade (workflow/rarefaction.nf, 2026-07-07)

Feature R&D (non qualifiee) : produit des BAM rarifies **nestes** a plusieurs profondeurs (`DEPTH` = 20M,10M,5M,2M,1M) pour etudier score/QC vs profondeur de sequencage. Meme logique 2-temps que [[small-fragment-flow]] : Temps 1 genere les BAM rarifies (masquerade `.merged.bam`), Temps 2 relance bam2beta dessus.

## Design retenu (valide avec Boris)

- **1 seul process `Rarefaction_Cascade`** fait toute la cascade (boucle bash sequentielle sur `params.rarefaction` trie decroissant, merged exclu). Input = `BAM_FILE` (tuple ID,BAM,BAI = merged via branche retro). `optional:true` (si merged < plus petit niveau -> rien).
- **Cascade** : chaque niveau tire du **fichier precedent** (20M depuis merged, 10M depuis le 20M, ...) -> nesting physique garanti (1M subset 2M subset 5M subset 10M subset 20M).
- **Denominateur recalcule** a chaque niveau (`samtools view -c`), pas nominal -> l'erreur ne se propage pas.
- **Skip-niveau** : si `COUNT <= TARGET`, on saute (decision Boris), la source reste le dernier BAM valide.
- **Approximatif** assume : `samtools -s` a une dispersion stochastique ~sqrt(reads) (+/-3000 a 20M, +/-700 a 1M), negligeable ; `%.6f` sur la fraction (au lieu de `%.4f` de BAM_Subsampling) pour tuer le biais systematique de rounding.
- Ressources : `withName: Rarefaction_Cascade` dans conf/base.config = cpus 8, mem 4GB, time 2h (calque sur Small_Fragment_Filter).
- publishDir route via `saveAs` chaque `${ID}_${DEPTH}.merged.bam` vers `${output_base}/${ID}_${DEPTH}/BAM/`. **Chaque niveau = nouvel ID unique `${ID}_${DEPTH}`** (Temps 2 derive l'ID du dossier). Boris a mis le base a `${params.output}_rarefaction`.
- Tag rollback : `pre-rarefaction` (sur HEAD a32c09b/0d8e65d).

## GOTCHA MAJEUR — samtools -s + meme seed casse la cascade

`samtools view -s SEED.FRAC` garde un read si `hash(SEED, read_name) < FRAC`. **FRAC est un seuil ABSOLU sur [0,1)**, et avec le **meme SEED le hash est deterministe**. Donc re-subsampler un BAM deja reduit avec le meme seed ne prend PAS "FRAC% du fichier courant" : il **re-seuille le meme hash**, et les seuils se composent en **MIN**, pas en produit.

Consequence en cascade seed=42 partout : niveau k = `frac_k x N_merged` (pas `frac_k x count_precedent`). Ex merged 30M : 10M demande -> 0.5x30M = **15M** obtenu. Le 1er niveau (20M) est correct (pas de cascade) ; tout ce qui suit est faux et **trop haut**. Motif observe en prod : 20M ok, 10M/5M/2M/1M gonfles.

**Fix** : seed **incremente** par niveau produit (`SEED=42` puis `SEED=$((SEED+1))`), `-s ${SEED}.${FRACTION}`. Hash independant a chaque etage -> FRAC s'applique bien au fichier courant. Nesting preserve (sous-ensemble physique). Reproductible (seeds 42,43,44... deterministes).

## Validation (2026-07-07, sur Bladder_Urine_02_117 merged reduit a 30M)

- **Comptes corriges** : 20M->20 004 602, 10M->10 005 059, 5M->5 003 751, 2M->2 001 234, 1M->998 676. Tous a **+/-0.13%** de la cible.
- **Buggy reproduit** (seed 42 fige, meme donnee) : 10M->14 999 399, 5M->10 003 255, 2M->5 998 585, 1M->5 003 204 = exactement `frac x 30M` et le motif prod de Boris. Diagnostic prouve empiriquement.
- **Nesting** : `comm -23` des read-names entre paliers consecutifs = **0 orphelin** partout -> 1M subset 2M subset 5M subset 10M subset 20M confirme.
- Artefacts de test : `/scratch/boris/rare_test/` (scripts + BAM fixed_*, Boris les garde).

## État opérationnel — RESTE À FAIRE (relevé du snapshot de contexte du 2026-07-07)

Le bug est corrigé et commité (`b2648b5`), mais **les conséquences sur les données ne sont pas traitées** :

- ⚠ **Les sorties S3 de production sont FAUSSES** — `processed/MRD/RetD/{liquid,solid}/{CGFL,HCL}_rarefaction/`
  ont été produites AVANT le fix (seed identique en cascade → comptes faux, trop hauts :
  `frac_k × N_merged` au lieu de `frac_k × count_précédent`). **Elles n'ont jamais été re-générées.**
  Quiconque les consomme aujourd'hui travaille sur des comptes erronés.
  → Re-lancer le Temps 1 (code corrigé) sur les 10 samples, puis le Temps 2.
  → Décider au préalable : écraser sur S3 (interdit sans accord explicite de Boris,
    cf. [[feedback_s3_no_delete]]) ou écrire dans un nouveau dossier.

- ⚠ **3 échecs du Temps 2 jamais investigués** : `KO=0` sur **Lung_121**, **Prostate_45**, **Lung_13**
  (crashs séparés, sans rapport avec le bug de seed). Cause inconnue.

Rappels d'usage : toggle `--RAREFACTIONS` (au **pluriel**), profondeurs via
`--rarefaction '20M,10M,5M,2M,1M'`. Artefacts de test conservés dans `/scratch/boris/rare_test/`.
