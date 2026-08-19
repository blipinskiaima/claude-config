# Context — Bam2Beta — 2026-08-19T17:18:00+00:00

**Branche** : main
**Dernier commit** : b2d5401 — docs(QC): manuel d'utilisation du duo ratio N50/N75 x masse > 1 kb
**Status** : 8 fichiers non commités — tous PRÉEXISTANTS (dev/SCW/*.sh modifiés + 6 non trackés),
aucun n'est de ces sessions

## Où j'en suis

**Deux chantiers du QC palier 1 menés en parallèle, aucun code pipeline modifié.**

**(A) Comptage `Preprocess_28M`** — la population, jusque-là absente de toute sortie, est
désormais **reconstituable à ±0,002 %** depuis `EXTRACT_FULL_28M` (`uniq(read_id) + skipped` du
log modkit). Backfill des 1 506 samples terminé, 100 % OK. La partie 3 du Google Doc (onglet
`Nb read mapped`), placeholder depuis l'origine, est remplie et publiée.

**(B) Fano (indice de dispersion)** comme critère QC, dans le prolongement de
`docs/QC-seuils-biopsie-liquide.md`. Run cohorte **terminé** : 1 344/1 346 liquides mesurés sur
le périmètre EPIC. Matériel dans `/scratch/boris/depth_fano/`, findings dans
[[fano-couverture-qc]].

## Ce qui marche / ce qui foire

**(A) Comptage 28M**
- ✓ Méthode validée sur 2 samples contre `samtools` (Healthy_826 +5, Lung_9 −649 sur 29,3 M)
- ✓ `uniq` sans tri suffit (22/22 chromosomes) → backfill en streaming, `bgzip -@4` −31 %
- ✓ `nb_reads_28M.tsv` : 1 506 samples, 100 % OK, dans `/scratch/boris/nb_read_28M/`
- ✓ Partie 3 publiée : texte + tableau 7×8 + 2 figures, onglet 16 986 → 20 991 car.
- ✗ `Preprocess_28M` ne publie toujours rien dans le pipeline — la reconstitution est un
  contournement, pas un correctif

**(B) Fano**
- ✓ **1re métrique du palier 1 à passer le critère de succès** : 48 outliers Tukey (seuil 1,320)
  sur le périmètre EPIC, dont **47 invisibles** aux seuils 5 M reads / 0,25× — 35 plasmas, 13 urines
- ✓ Confondants **écartés** : CNV (r = −0,020, outliers à `score_cnv` médian 0,00 contre 4,28),
  longueur/N50 (+0,050), reads (+0,065)
- ✓ Reproductibilité vérifiée : `Breast_8` et `Breast_8_rebasecalled_V5` à 0,008 près
- ✗ **Fano génomique brut inutilisable** — les satellites à 23 130× écrasent la variance, il
  classe `Lung_9` (propre) pire que l'urine aberrante
- ✗ `corr(EPIC, génomique) = +0,811` : le proxy gratuit dit presque la même chose →
  **l'apport réel du run EPIC n'est pas démontré**
- ✗ `corr(EPIC, depth) = +0,445` subsiste → travailler sur un résidu, pas la valeur brute
- ✗ `--use-median` écarté (7 valeurs distinctes à 2×) · 2 samples manquants
  (`HCL__Colon_14`, `CGFL__Lung_Alc_74_av`, per-base absents sur S3)

**Transverse — 3 items du palier 1 restent ouverts**
- ✗ Les 4 plasmas HCL (mécanisme non établi, impacte la `depth` publiée donc le seuil 0,25×)
- ✗ Le seuil 4 M du contributif « à creuser »
- ✗ Le renommage `nb_reads_aligned` → `nb_reads_primary` (breaking change trace-platform / Tower)

## Prochaine étape

**Priorité** : les **4 plasmas HCL** — seul point ouvert capable d'invalider un rendu existant.

Sinon, au choix :
- **(A)** publier le comptage dans `Preprocess_28M` (`samtools idxstats` sur le BAM déjà indexé
  + `collectFile()`, addition pure mais re-run complet du 28M en qualification) ;
- **(B)** comparer les **listes d'outliers** Fano EPIC et génomique : si elles se recouvrent
  entièrement, garder le proxy génomique (gratuit, déjà calculé) et clore la piste. Piste
  secondaire : les outliers sont **×2,1 enrichis en `score_cnv` = 0** (55,9 % contre 26,9 %) —
  tester si les samples à CNV nul ont un Fano supérieur à profondeur comparable, le sens de la
  flèche n'étant pas établi.
