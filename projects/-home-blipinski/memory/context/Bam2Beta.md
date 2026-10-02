# Context — Bam2Beta — 2026-10-02T13:13

**Branche** : main
**Dernier commit** : 9b13bb6 — docs: add Pod2Bam operational cost deck for CEO
**Status** : 6 fichiers modifiés/non suivis hors session (dilution_lung.sh, PDF rapports, note.txt, pair_current.tsv), volontairement non commités

## Où j'en suis
V2.3.3 (Check_Input bloque FAILED_QC_METHYLATION / FAILED_QC_BASECALL_MODEL en mode PROD, JSON dégradé 35 champs,
lanceur grep FAILED_QC_ + timeout 4h, socketTimeout 10 min) et V2.3.4 (sample de qualification Healthy_826 → Healthy_64
HCL hac@v5.0.0, 3 valeurs figées re-figées) sont releasées et QUALIF OK (V2.3.3 54/54, V2.3.4 51/51).
Déclencheur : IRCCS RC24 (BAM réalignés minimap2 sans -y → pas de MM/ML ni @RG).

## Ce qui marche / ce qui foire
- ✓ Check_Input : 22/22 cas testés (dont RC24, AIMA_020, pt100 réels) ; TEST et QUALIF OK
- ✓ Healthy_64 reproductible bit à bit sur 3 runs ; QUALIF/V2.3.4 = référence (54 contrôles dès V2.3.5)
- ✗ Lanceur V2.3.4 PAS encore copié sur la machine plateforme → la prod tourne encore en V2.3.2
- ✗ Le pipeline peut démarrer avant la fin de la copie des BAM (.dl-complete posé en premier au re-dispatch) :
  AIMA_002 (29/09) et AIMA_004 (28/09) livrés sur données partielles — non corrigé
- ✗ Cause des uploads S3 figés (AIMA_013, AIMA_004) non prouvée (logs perdus) ; socketTimeout 10 min = pari
- ✗ Token Seqera en clair dans nextflow.config:59

## Prochaine étape
Copier dev/PLT/Bam2Beta_SCW_plateforme.sh (VERSION=V2.3.4) sur la machine plateforme, puis vérifier le 1er run prod.
