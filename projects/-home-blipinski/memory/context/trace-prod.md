# Context — trace-prod — 2026-09-15T16:00:08+00:00

**Branche** : main
**Dernier commit** : 66c028d — feat(dilution-lung): schema v36 — Mode1/Mode2/Frag Score v2 + doc de la table
**Status** : clean (untracked inchangés : backups .duckdb, CSV dev/, rapports HTML)

## Où j'en suis
Chantier `dilution_lung` terminé et clos. Le lot des 220 couples du plan
`Bam2Beta/early_lung_dilution_pairs_original.tsv` est complet, et le schema v36 a ajouté
les 3 métriques fragmentomiques softclipped. Rien n'est en cours, tout est commité, poussé
et exporté.

## Ce qui marche / ce qui foire
- ✓ **220/220 sur toutes les colonnes** : BAM, PROD, mVAF v1.4/v1.5, Mode1/Mode2/Frag Score v2,
  probs epic et Loyfer. 0 ligne sans identité, 0 fantôme. Montée en charge 33 → 220 en 8 passes
- ✓ **v36 en 39 lignes sur 4 fichiers** : `extract_metrics` appelle les `check_frag_*_sc` de
  `BaseChecker`, aucune règle réécrite. Export en fin d'onglet `mVAF` (24 col), Mode1/2 arrondis
  2 déc. via un paramètre optionnel `round2_cols` ajouté au helper partagé (4 autres appelants intacts)
- ✓ **Probs HCL rafraîchies en mode bootstrap** (518/518 epic + Loyfer, somme = 1,0000) puis
  exportées. ⚠ la base tient les **moyennes bootstrap**, pas les `props_v1.3` — un `probs -P`
  écraserait ce choix de juillet
- ✓ **Table documentée** : README section 14 (absente depuis la création en v33) + section
  v33/v36 dans CLAUDE.md avec les 4 commandes
- ✗ **Deux pièges de génération parallèle, chers** : `aws s3 ls` matche par **préfixe**, un `.bai`
  orphelin a masqué `Lung_141_Healthy_111` deux jours → utiliser `head-object`. Et la purge des
  BAM stagés balaie tout `/scratch/nxf-work`, ce qui a tué 3 paires → `-w` dédié **et** recherche
  limitée à ce `-w`
- ✗ **3 samples HCL sans probs** : les `Twist_*_rep_4`, dossiers réduits à `LOG/`, pipeline pas
  encore passé. Se rempliront seuls

## Prochaine étape
Rien de bloquant. Si le pipeline reprend sur d'autres couples, la routine est rodée :
lister S3, checker les nouveaux plus les `prod_status='KO'`, puis les deux exports. Les
`Twist_*_rep_4` méritent une passe `probs liquid HCL --probs_bootstrap` quand leur `BETA/` sera là.
