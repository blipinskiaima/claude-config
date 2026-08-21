# Context — trace-prod — 2026-08-21T17:00:04+00:00

**Branche** : main
**Dernier commit** : 63418c0 — feat: schema v27 — renommage short_read → small_fragments
**Status** : propre (untracked inchangés : backups .duckdb, CSV dev/, rapports HTML, metadata_HCL.tsv)

## Où j'en suis
Schema v27 terminé et pushé : renommage `short_read` → `small_fragments` partout, déclenché par
un vrai bug (le bucket S3 avait été renommé, le checker listait un préfixe inexistant → la colonne
serait passée KO à 100 % au prochain check). Le reste de la session était de l'exploitation :
MAJ ciblées de colonnes + exports, sur demande item par item.

## Ce qui marche / ce qui foire
- ✓ v27 : migration en PRÉ-migration (avant les CREATE), PK/FK préservées, testée sur copie
  puis idempotence 3 ouvertures. 1199 lignes + 1507 valeurs conservées
- ✓ Les 38 Bladder_Urine_02_1xx ex-PROD KO sont repassés OK : il ne manquait que le MITO,
  les relances l'ont produit, le check de conformité a posé le .done
- ✓ 38 `idxstats.tsv` générés hors Nextflow (`samtools idxstats`, 5 s/sample, 3 min en tmux
  parallèle) → les 4 colonnes Mapped/Primary/Unmapped/Hors chr1-22 sont enfin remplies
- ✓ N50 et mVAF v1.3 retirés de l'export, colonnes gardées en base (statut de n75)
- ✓ Fallback `Indication` étendu (Bladder_Urine, Colon) plutôt que créer 84 lignes metadata vides
- ✗ `Thémélio` sur Lung_Alc_88_av : résolu en fin de session (0,901998) après un THEMELIO_RETRO
- ✗ 12 barcodes Colon_*_rep restent NULL : ni dans le nom de fichier ni dans le RG.
  Récupérables seulement via les logs Pod2Bam + UPDATE SQL manuel — non fait
- ✗ 15 samples (12 Twist + 3 Ma_SAB) : Taille/Complétude POD5 vides car `pod5_adresse` est NULL

## Prochaine étape
Rien de bloquant. Trois fils ouverts :
1. Barcodes des 12 `Colon_*_rep*_OK` / `Colon_2x_rep1` via les logs Pod2Bam (UPDATE SQL manuel)
2. Retrouver l'adresse POD5 des 12 Twist + 3 Ma_SAB pour débloquer Taille/Complétude
3. `28M %` / `CpG %` : QCChecker les code en dur à None — câblage réel quand Bam2Beta
   publiera nativement ces comptages
