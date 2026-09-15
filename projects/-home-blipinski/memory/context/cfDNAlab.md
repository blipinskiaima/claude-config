# Context — cfDNAlab — 2026-09-15T15:51

**Branche** : main
**Dernier commit** : a9acaed — Removes `--normalize-by-length off` case from equivalent CLI string
**Status** : clean (clone upstream BesenbacherLab/cfdnalab, rien à y committer)

## Où j'en suis
Évaluation de cfdnalab terminée sur données AIMA réelles. Les 4 commandes de features
ont été testées jusqu'au bout, cohorte de 28 échantillons (15 sains CGFL+HCL, 13 tumoraux
dont 4 réplicats). Conclusion posée : rien dans cfdnalab ne bat ce qui existe déjà dans
Bam2Beta. Aucune décision d'intégration prise — la session s'arrête sur ce constat.

## Ce qui marche / ce qui foire
- ✓ cfdna v0.9.0 installé et opérationnel (`~/.cargo/bin/cfdna`, env conda `cfdnalab`)
- ✓ Environnement complet réutilisable dans `/scratch/boris/cfDNAlab/` : 2bit GRCh38 no_alt,
  blacklist ENCODE, table de référence GC, 9 scripts d'analyse
- ✓ `lengths` = meilleur rapport signal/bruit (4,0) — mais duplique le module FRAG existant
- ✗ `fcoverage` à 10 kb ne remonte que des artefacts de mappabilité (27/27 négatifs)
- ✗ `ends` : bruit de réplicat (2,24 pt) ≈ signal (2,69 pt), et reste corrélé au biais GC
  résiduel (r=+0,52) malgré `--gc-file`
- ✗ `midpoints` : 76 % de l'écart sain/tumoral est un artefact de longueur de fragment
- ✗ Obstacle structurel : sains et tumoraux ne partagent jamais un run → effet batch
  confondu avec le groupe par construction

## Prochaine étape
Rien d'engagé sur cfdnalab. Si la piste est rouverte, le seul angle non exploré est
`lengths --by-size 5000000` (profils DELFI spatiaux) sur la métrique au meilleur ratio —
les BAM de la cohorte ayant été supprimés, compter ~2 h de retéléchargement.
Sinon, le résultat actionnable de la session est ailleurs : `Small_Fragment` dégrade la
mVAF (mémorisé côté Bam2Beta), à trancher avec Boris.
