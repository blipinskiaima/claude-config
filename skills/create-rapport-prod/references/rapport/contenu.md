# Contenu attendu du rapport

Référence visuelle : `~/Pipeline/Bam2Beta/docs/rapport_plateforme_2026-10-01_IRCCS.pdf` (v11, validée par Boris).
Toute évolution de forme passe par `rapport_plateforme.py` ; vérifier ensuite la non-régression :
`pdftotext -layout` du rapport du 2026-10-01 doit rester identique à la version de référence (v12 : colonne « Lectures (M) » = Nb molécule).

## Diapositives

| # | Rubrique (rouge) | Titre | Contenu |
|---|---|---|---|
| 1 | `Bioinformatique : Lipinski Boris` (`AUTEUR`) | « Rapport de production du 1er octobre » (ou « du X au Y mois ») | 4 chiffres : analyses, patients, rapports livrés, min par analyse. Tableau : client, produit, mode d'upload, Dorado version, temps de séquençage, pipeline. Tableau des versions : Éxís, Éxís CUP, Themelio, Raima. Message à droite : fenêtre d'exécution UTC, statut run, statut QC |
| 2..n | Opérationnel | Parcours de chaque échantillon | Une frise par sample (style Tower) : nom, barcode, bout en bout à gauche ; chiffre en coin = min–max bout en bout |
| suite | Opérationnel | Exécution du pipeline | Démarrage, fin, pipeline, attente file, bout en bout, statut ; N.B. statut du run |
| suite | Biologique | Contrôle qualité | « Lectures (M) » = Nb molécule (`nb_reads_filtered`, mapping de la gsheet), lectures EPIC, profondeur, couverture, QC Éxís, QC Themelio ; N.B. statut QC |
| suite | Biologique | Résultats | mVAF + seuil Éxís, score + classe Themelio, TOO prédit + décision ; seuils + N.B. réserve QC |

Pas de N.B. sur la page 1 ni sur les frises (retirés à la demande de Boris).

## Conventions validées

| Sujet | Règle |
|---|---|
| Ordre des lignes | chronologique d'exécution (`pipeline_start_date`) sur TOUTES les diapositives |
| Heures | UTC ; date ajoutée à l'heure si la période couvre plusieurs jours |
| Éxís / Éxís CUP | `version_mvaf` / `version_too` (le seuil CUP `too_CupMaxProba_threshold` appartient au module TOO, `Bam2Beta/workflow/rapport.nf:144`) — correspondance déduite, à confirmer si Boris la conteste |
| Temps de séquençage | `sequencing_time` (QC/Samtools) : propre au run ONT ; valeur unique + « même run ONT » si un seul `run_id` |
| Seuils | Éxís 0,0042 / 0,11 / 0,32 % ; Themelio Detection > 0,921, Negative ≤ 0,725 (portés par Bam2Beta, pas en base) |
| Décision TOO | traduite : « non rendue : seuil non atteint » / « non rendue : classe incertaine » |
| N.B. statuts | dire si la raison est la même pour tous ; sinon une raison par groupe avec son compte ; rappeler que WARNING run (fichiers déposés, ex. `.bai` manquant) ≠ WARNING QC (biologie) |
| Marque | « Éxís » toujours accentué |
| Frises | sample alone : SESSION → FICHIER REÇU, → CLÔTURE, ATTENTE PIPELINE, PIPELINE ; bulk : variante à 7 segments de `Flux.tsx` |
| Pas d'interprétation clinique | les résultats sont restitués, jamais commentés |
| Figures fragmentomique / CNV | non intégrées (décision de Boris, « on verra plus tard ») |
