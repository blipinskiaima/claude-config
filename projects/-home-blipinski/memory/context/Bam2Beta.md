# Context — Bam2Beta — 2026-09-28T14:41

**Branche** : main
**Dernier commit** : 777aa9b — fix(prod): plafonner un run plateforme a 6h pour ne plus geler la file
**Status** : clean (2 non suivis : docs/pair_current.tsv, qualifStatus.txt)

## Où j'en suis
Incident prod du 25/09 réglé : AIMA_013 figé 7 h (morceau 7/20 de l'envoi du merged.bam jamais
arrivé sur S3, socketTimeout 1 h × 20 retries), file plateforme bloquée. Relancé depuis zéro le
26/09 (conforme en 11 min, mVAF 0,98 / Thémélio 0,966574 identiques). Correctif commité et poussé :
lanceur plateforme sous `timeout --kill-after=5m 6h` → code 124/137 → branche else (.failed + email,
code de sortie dans le log), sans livraison du metadata.json (choix ISO de Boris).
En parallèle, R&D end motifs 5' cfDNA dans /scratch/boris/end_motif/ (scripts + figures).

## Ce qui marche / ce qui foire
- ✓ End motifs ONT : 5' sans clip à 91-93 % (le 3' clippé à 61 %), CCCA en 1re position chez les sains
- ✓ Cohorte HCL séquencée le même jour (8 H / 20 L) : pas de biais GC ; effet dose MDS ρ=+0,62, CCCA ρ=−0,61 avec la mVAF
- ✗ Signal invisible sous ~30 % de TF (variabilité entre individus 10 fois le signal à 2 %) → pas de gain en détection
- ✗ Cohorte CGFL 5/5 inexploitable : groupe confondu avec le run (Lung le même jour, 6× plus d'ADN chargé) + biais GC
- ✗ FLARE : code inutilisable (pas de licence, top 20 seulement, module méthylation faux) → réimplémenté
- ⚠ Timeout 6 h testé en simulation seulement, pas sur un vrai run Nextflow
- ⚠ socketTimeout 1 h (nextflow.config:79) non modifié : passer à 10 min = V2.3.3 + test + qualif
- ⚠ AIMA_016 : aucun BAM reçu, le client doit renvoyer ; client bdcb0133 absent de labs_users

## Prochaine étape
`git pull` sur la VM plateforme pour activer le timeout 6 h, puis décider du socketTimeout (V2.3.3).
