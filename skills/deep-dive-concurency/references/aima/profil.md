# Partie 1 — Le profil AIMA (référentiel de comparaison)

Le profil AIMA est la **base de comparaison** de tout deep-dive. Il est **découplé** de
l'analyse concurrente : maintenu dans le temps, indépendamment de chaque cible, et chargé au
début de chaque analyse comme référence figée.

## Où il vit

**Fichier canonique : `~/Pipeline/Aima-Survey/concurency/AIMA-POSITIONING.md`.**

C'est l'équivalent, pour AIMA, des rapports P1/P2 qu'on produit pour un concurrent — mais sous
forme d'un **document unique vivant** plutôt que d'un livrable figé. Il porte les mêmes axes de
comparaison que ceux d'un rapport concurrent (plateforme, couverture, signaux, modèle,
performances, réglementaire, marché), pour que la confrontation en Partie 3 soit axe par axe.

## Charger le profil — début de chaque deep-dive

```bash
cat ~/Pipeline/Aima-Survey/concurency/AIMA-POSITIONING.md
```

Sans lui, la comparaison est approximative et diffère d'une analyse à l'autre. S'il paraît
obsolète (journal de MAJ ancien, chiffres divergents de ce qu'on sait), **le signaler à Boris
avant de continuer** — et éventuellement déclencher une mise à jour (ci-dessous) avant l'analyse.

## Source de vérité des chiffres

| Type d'info | Source canonique |
|---|---|
| **Performances mVAF v1.4** | rapport **Exis 1.1 (doc SD-02)**, reproduit par la page `/exploration` d'Aima Tower |
| Performances combo THEMELIO | `~/Pipeline/Feature/result/speedvac_no/eval_kpis.csv` |
| Spécifications techniques (wet/dry lab, scores) | code des projets `~/Pipeline/` (Bam2Beta, Pod2Bam, Feature…) |
| Effectifs de cohorte, seuils | rapport Exis 1.1 / trace-prod |

⚠ Le profil peut se périmer en silence si l'eval est rejouée ou si un nouveau rapport Exis
paraît. Vérifier la cohérence entre le journal de MAJ de la fiche et la date du dernier rapport
Exis / du dernier `eval_kpis.csv`.

## Mettre à jour le profil

Quand de nouvelles données autoritaires arrivent (nouveau rapport Exis, nouvel eval, nouveau
score, décision réglementaire) :

1. **Identifier le référentiel** de la donnée (Exis SD-0x ? eval interne ? code ?) et son
   marqueur (`[EXIS]`, `[MESURÉ]`, `[CODE]`).
2. **Ne jamais écraser** un référentiel par un autre : mVAF v1.4 seul et combo THEMELIO sont des
   scores distincts, sur des cohortes distinctes — ils coexistent (cf. §5.A / §5.B de la fiche).
3. **Marquer chaque chiffre** de son niveau de preuve et de sa cohorte (n, spécificité). Un
   chiffre sans effectif ni spécificité n'entre pas dans le profil.
4. **Ajouter une ligne au journal** de mise à jour en fin de fiche (date, ce qui a changé,
   source).
5. Si la MAJ comble un champ `[À PRÉCISER]` ou en ouvre un nouveau, le refléter dans les
   sections « À compléter » / « Positionnement marché ».
6. **Attendre validation de Boris** avant d'inscrire un chiffre marqué `[VALIDÉ]`.

## Ce que le profil doit toujours contenir pour servir la comparaison

- Les **deux lignes produit** (MRD / MCED) et leurs concurrents directs, pour router la cible.
- Le **différenciateur réel** formulé correctement (genome-wide, par base, 5hmC natif, CNV) —
  pas la version périmée « trois signaux sur la même molécule » (Guardant le fait aussi).
- Les **verrous connus**, sous forme de grille de cross-check à remplir pour chaque concurrent.
- Le **chiffre de référence** citable de chaque ligne, avec sa cohorte et sa spécificité.
- La **règle de comparaison** (jamais de sensibilité sans spécificité + effectif).
