# Context — trace-prod — 2026-06-23T15:58:02+0000

**Branche** : main
**Dernier commit** : ac7f0f5 — feat: schema v12 — colonne bootstrap (retd_suivis)
**Status** : clean côté tracké (aucun code modifié cette session — uniquement données DB + gsheets)

## Où j'en suis
Session = remplissage ad-hoc de colonnes trace-prod (zéro code). Backfill bootstrap terminé (plateau), intégration metadata HCL (+32 nouveaux), + colonnes BAM/POD5/frag/dorado/extract pour samples HCL/CGFL ciblés. Tout exporté, rien en attente.

## Ce qui marche / ce qui foire
- ✓ Bootstrap : backfill complet CGFL 788/790, HCL 513/513 (2 KO CGFL structurels = Bladder_Urine_02_090 + Twist_10_8, props absents)
- ✓ import-metadata HCL : 422 importés (+32 = Healthy_151-182 passés de gsheet-only → base), export ONT Sample 834 lignes
- ✓ 32 Healthy_151-182 : colonnes BAM/POD5 remplies ; + frag_status_sc 37 HCL, modes_sc Colon_53 + 4 Bladder CGFL, dorado/date/pipeline/extract_full Healthy_171/176
- ✗ 11 Twist titration : stockage_pod5=SCW mais pas d'adresse/taille POD5 individuelle (POD5 partagés, structure atypique)
- ⚠ FRAG SC (frag_status_sc) ≠ Mod1/Mod2 (frag_mode*_sc) : colonnes distinctes, lancer séparément

## Prochaine étape
Rien d'engagé. Optionnel : investiguer les POD5 des 11 Twist titration (taille/complétude) ; scheduled task refresh bootstrap proposé (non retenu).
