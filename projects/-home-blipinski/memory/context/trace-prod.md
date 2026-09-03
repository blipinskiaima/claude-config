# Context — trace-prod — 2026-09-03T12:41:17+00:00

**Branche** : main
**Dernier commit** : bbd1027 — docs: gotcha metadata.kit (non fiable côté HCL)
**Status** : propre (untracked inchangés : backups .duckdb, CSV dev/, rapports HTML, metadata_HCL.tsv)

## Où j'en suis
Deux chantiers dans la session. (1) Schemas v30/v31 terminés et poussés : `sequencing_time`
(`XhYm`) + `multi_run` dans `retd_suivis`, backfill 1362/1362 en 9h33, validé 485/485 contre
le calcul awk indépendant. (2) Analyse ad-hoc des pore scans, entièrement hors repo dans
`/scratch/boris/pore-scan/` : extraction du pore scan initial de 146 rapports MinKNOW
(92 CGFL + 54 HCL) → `pore_scan_initial.tsv`, puis cinétique de séquençage et mortalité des
pores sur 4 runs. Rien n'est en cours, tout est livré.

## Ce qui marche / ce qui foire
- ✓ `pore_scan_initial.tsv` : 146 runs × 11 col (labo, flow cell, date, type, kit, nb samples,
  pores totaux/dispo, ratio, nb scans). Scripts dans `/scratch/boris/pore-scan/`
- ✓ **Aucune différence CGFL/HCL** sur les pores au lancement (médianes 2704 vs 2663, p=0,12),
  ni sur le type de flow cell : `FLO-PRO114M` + `SQK-NBD114-96` sur les 146 runs
- ✓ **La réserve de pores prédit la longévité** : r=+0,44 entre pores *totaux* au 1er scan et
  demi-vie (<6500 → 25 h ; >8500 → 41 h). Le nombre de pores *disponibles* ne prédit rien
  (plafonné par les ~2675 channels) — la bonne métrique qualité est le total
- ✓ Cinétique : jamais de plateau, décroissance continue dès h+2 pilotée par la mortalité des
  pores. 92-100 % des reads acquis à h+48 sur les 4 runs
- ✓ Pores reconstituables **sans rapport MinKNOW** via les tags `ch:i`/`mx:i` du BAM
  (validé à ±3 % contre le mux scan officiel du run test_002)
- ✗ **2 faux départs corrigés en cours de route** : mon comptage de samples comptait le bruit
  de démultiplexage (médiane 95/96 au lieu de 4) ; et ma détection de « chute brutale »
  a classé PBK07581 sur du bruit de fin de vie alors qu'il saigne dès h+0
- ✗ Cause du profil 2 non élucidée : ni paramètre de run, ni log, ni réutilisation de flow cell
  (146 IDs distincts, aucun doublon). Le préfixe explique 10 % de la variance mais est
  totalement confondu avec la date

## Prochaine étape
Rien de bloquant. Trois fils : demander aux labos s'ils lavent/réutilisent des flow cells
(seul moyen de trancher, aucune trace dans les rapports) ; investiguer les 3 runs CGFL du
27/03/2026 qui meurent à l'identique en 8 h avec une réserve saine (cause commune probable :
librairie ou lot de réactifs) ; et vérifier l'hypothèse non testée `rebasecalled → multi_run=yes`.
