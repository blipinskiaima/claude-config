# Context — trace-prod — 2026-09-03T06:07:44+00:00

**Branche** : main
**Dernier commit** : 388f777 — feat: schemas v30 + v31 — sequencing_time + multi_run
**Status** : propre (untracked inchangés : backups .duckdb, CSV dev/, rapports HTML, metadata_HCL.tsv)

## Où j'en suis
Schemas v30 + v31 terminés et poussés : `sequencing_time` (durée du run, `XhYm`) et
`multi_run` (`yes`/`no`/`NA`) dans `retd_suivis`, liquid only, extraits de
`QC/Samtools/{sample}.read_start_time.tsv`. Backfill des 1362 samples fait dans la nuit
(9h33), gsheet exportée, doc et mémoire à jour. Les 4 étapes de la feuille de route sont
bouclées, rien en attente.

## Ce qui marche / ce qui foire
- ✓ 1362/1362 samples renseignés, 0 KO — validé **485/485 sans écart** contre le calcul
  awk indépendant de Boris (`/scratch/rarefaction_horaire/result.csv`, 26/08)
- ✓ Contrôle de vraisemblance : les 993 `multi_run=no` ne dépassent jamais 71 h, la limite
  d'un run ONT — un faux négatif se verrait comme un `no` à 100 h, il n'y en a aucun
- ✓ Gsheet CGFL 849×57 et HCL 513×57, colonnes 27-28, 0 cellule vide ; solid intact (40 col)
- ✗ **Le préfixe de 500 Mo était faux** : il passait 5 tests sur 5 et sous-estimait de 3h54
  sur `HCL/Healthy_41`. C'est la confrontation aux 485 valeurs de Boris qui l'a révélé —
  un max ne s'échantillonne pas, la fin d'un run ne produit que quelques milliers de reads
- ✗ 62 samples à `NA` (format `…SSZ` sans fraction de seconde, cohorte `Lung_Alc`), dont
  12 dépassent 72 h : probablement multi-run, indémontrable depuis le fichier
- ✗ Les `*_rebasecalled_*` ressortent massivement `multi_run=yes` — plausible, **non vérifié**

## Prochaine étape
Rien de bloquant. Deux fils ouverts : vérifier l'hypothèse `rebasecalled → multi_run=yes`
(comparer les fractions de seconde d'un rebasecalled et de son sample d'origine), et
contrôler dans la gsheet les formats de cellule à droite de la colonne 28, décalés d'un
cran par l'ajout des deux colonnes (`clear()` n'efface pas les formats).
