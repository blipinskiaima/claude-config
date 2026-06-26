# Context — Bam2Beta — 2026-06-26T14:55:40+0000

**Branche** : main
**Dernier commit** : f99812e — feat(mvaf): arrondi sortie mVAF v1.4 en % (round/signif) + fix flags launch_SCW
**Status** : clean (seul dev/SCW/bacasable.sh untracked, sandbox perso)

## Où j'en suis
Feature **mVAF v1.4** (R&D, non qualifié) : formatage de la sortie `mvaf` finalisé.
La valeur est désormais exprimée en **% (×100)** puis arrondie. Bloc de transfo identique
dans les 2 scripts (`bootstrap_trasnfo.R` rétrospectif + `bootstrap_model_v1.1.R` from-scratch).
En parallèle, flux **small_fragment** : Temps 2 toujours en attente (cf. snapshot précédent).

## Ce qui marche / ce qui foire
- ✓ Arrondi sortie V1.4 : `x=mvaf*100` → `x>=1 → round(x,2)` / `x<1 → signif(x,2)`, committé (f99812e)
- ✓ Les 2 scripts (model_v1.1 + trasnfo) cohérents bit-à-bit sur le bloc transfo
- ✓ launch_SCW.sh corrigé : `~/Run2`→`~/Run12`, `--cpu`→`--cpus_max`
- ✗ Validation bit-à-bit SORTIE 1 (`rowSums(props)` vs ancien appel direct) toujours non faite — gate lors d'un vrai run `--bootstrap`
- ✗ Temps 2 small_fragment (Bladder_Blood_01_001) pas encore lancé (load serveur)

## Prochaine étape
Lors du prochain run `--bootstrap` réel : valider bit-à-bit la SORTIE 1 de bootstrap_model_v1.1.R
(rowSums des props vs ancien appel direct) ET vérifier le nouveau formatage % des sorties V1.4.
Puis débloquer le Temps 2 small_fragment quand le load serveur retombe.
