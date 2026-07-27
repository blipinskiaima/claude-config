# Context — Bam2Beta — 2026-07-27T17:21:00+0200

**Branche** : main
**Dernier commit** : fa3d554 — feat(MITO): QC mitochondrien mosdepth+BAM (liquid, mode rétro)
**Status** : poussé (HEAD = fa3d554) ; hors commit possible : note.txt, prompt_generator.pdf, mods dev/SCW

## Où j'en suis
Module **MITO QC** livré et poussé (`fa3d554`) : liquid only, rétro si `!BETA`, TSV 11 cols sous `MITO/`, **pas** de champs `metadata.json`. NUMT différé. Feature stable pour usage rétro.

## Ce qui marche / ce qui foire
- ✓ MITO câblé (from-scratch si BETA ; rétro BAM+mosdepth sous `params.output`)
- ✓ Smoke H826 (câblage) + Colon_1 (signal réel)
- ✓ Étape 4 vérif partielle — OK pour usage rétro
- ✗ NUMT reporté (hors scope)
- ✗ Bug `themelio_absent.csv` hors scope, toujours présent

## Prochaine étape
Usage rétro MITO en batch S3 si besoin ; sinon reprise NUMT ou fix `themelio_absent.csv` quand priorisé.
