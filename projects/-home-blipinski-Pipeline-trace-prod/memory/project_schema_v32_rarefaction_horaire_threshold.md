---
name: project-schema-v32-rarefaction-horaire-threshold
description: "Schema v32 — table rarefaction_horaire_threshold (63 col, autonome, PK composite dès le DDL), pseudo-samples {base}_{5M|10M|15M|20M}, calque de rarefaction_horaire sans mvaf_v1/v2. Export vers une 2e gsheet dédiée (onglets mVAF 16 col / Prop 51 col)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8030cb14-c61f-41aa-83fa-95f5f9072b12
  modified: 2026-09-03T07:43:06.155Z
---

# Schema v32 — `rarefaction_horaire_threshold` (septembre 2026)

Table **autonome** de 63 colonnes, pseudo-samples `{base}_{5M|10M|15M|20M}` (4 paliers en millions
de reads), aucune FK vers `samples`. Calque de [[project_schema_v28_rarefaction_horaire]] : mêmes
fichiers sources, même checker, même helper d'export.

**Why:** Boris veut comparer les métriques d'un BAM raréfié à 5/10/15/20 M reads aux valeurs
initiales du sample parent — l'équivalent de l'expérience horaire (12h/24h/48h), mais sur l'axe
profondeur au lieu de l'axe temps.

## Ce que le calque a bien fait gagner

Zéro règle métier réécrite. Le checker **importe** `_bootstrap_means` de
`checkers_rarefaction_horaire` et `_read_props` de `checkers_dilution` ; les deux exports
réutilisent `_export_rarefaction_horaire` **tel quel** (il est déjà paramétré par
`config_key`/`ws_default`/`headers`/`text_cols`). 5 fichiers modifiés + 1 créé.

Le garde-fou anti-création de ligne d'`update-column-rarefaction-horaire` a été repris : filtre
`existing` (SELECT des sample_name du labo) **avant** l'UPSERT. Vérifié des deux côtés — un
`-s <inexistant>` affiche `Ignorés (absents…)` et laisse le compte de lignes intact.

## Les deux différences avec la v28, et pourquoi

- **`read_threshold`** au lieu de `time_point`, regex `^(.*)_(\d+M)$` (celle de `rarefaction` v16).
- **63 colonnes = 65 − 2** : `mvaf_v1` et `mvaf_v2` **retirés**. Leur source est
  `BETA/{s}.merged.epic.raima_score.V2.tsv`, qui n'existe dans **aucun** de ces dossiers —
  vérifié sur l'intégralité des 14 858 clés S3, `BETA/` ne contient que `V1.4` et `V1.5`.
  Les garder aurait fabriqué deux colonnes NULL à vie. 6 sous-dossiers seulement
  (`BAM, BETA, BETA_28M, BOOTSTRAP, EXTRACT_FULL_28M, QC`), pas de `CNV`.

## PK composite : 28 collisions, constatées AVANT de coder

7 bases (`Colon_25/27/28/29/31/32/34`) existent en CGFL **et** en HCL → 28 pseudo-samples
homonymes. Avec une PK mono-colonne, le check HCL aurait écrasé 28 lignes CGFL — le bug v17,
qui avait coûté 90 lignes. **Un `cut | sort | uniq -d` sur le listing S3 tranche en 10 secondes
et doit précéder l'écriture du DDL**, pas la suivre.

## ⚠ Loyfer non bootstrapable — la limite est physique, pas un choix

Revérifiée sur fichier réel avant d'écrire une ligne :

```
BOOTSTRAP/{s}.merged.all.bootstrap_v1.props.tsv    201 lignes × 16 col  → epic seul, 200 réplicats
EXTRACT_FULL_28M/{s}.merged.all.props_loyfer.tsv     2 lignes × 31 col  → Loyfer, valeur UNIQUE
```

Aucun fichier bootstrap Loyfer n'existe. Une demande de « proportions Loyfer et epic
bootstrapées » n'est donc réalisable **qu'à moitié** : epic = moyenne des 200 réplicats,
Loyfer = la valeur unique. Le dire explicitement plutôt que de livrer en silence.

Les deux sortent du **même `.bgzf` 28M** — `Modkit_extract_full_28M` alimente `Raima_score_mVAF`
(→ BOOTSTRAP + raima V1.4/V1.5) *et* `Raima_process_loyfer` (→ props_loyfer),
cf. `Bam2Beta/workflow/beta_28M.nf:30-42`. D'où le préfixe `.merged.all.` commun.
⚠ **`rarefaction` (v16) lit ses epic ailleurs** : `BETA/{s}.merged.epic.props_v1.tsv` (panel EPIC,
valeur unique, version périmée — le `probs` standard est passé à `props_v1.3.tsv`). Seules les
**deux tables horaires** ont des epic bootstrapées.

## Gotchas

- ⚠ **`bam_status_threshold` vaut `OK` sur 308/308** → ne discrimine rien. Tous les BAM sont
  produits, seule une fraction passe dans le pipeline. Le discriminant est `prod_status_threshold`
  (120/308). Même situation que `bam_status_horaire` en v28. La colonne a été demandée
  explicitement, elle est gratuite (même listing), mais ne jamais trier dessus.
- ⚠ **`LOG/`** dans les deux dossiers → filtre `split_threshold(s)[1]`, sinon ligne fantôme.
- ⚠ **Le lot grossit pendant qu'on travaille** : 300 pseudo-samples à 06:15 le 03/09, **308** à
  06:30. Annoncer un décompte comme définitif est faux ; le `check` est idempotent, une relance
  rattrape sans `DELETE`.
- ⚠ **L'onglet cible s'appelle `Prop`** (majuscule), pas `prop`. Les deux onglets existaient mais
  étaient **vides** (grille pré-dimensionnée en 16/51 par duplication de la gsheet v28).
- L'écart **123 vs 120** entre métriques QC et mVAF n'est pas un bug : 3 pseudo-samples ont déjà
  `QC/` et `EXTRACT_FULL_28M/` mais pas encore `BETA/` ni `BOOTSTRAP/` (vague de production).

## Vérifications

- 4 samples croisés base ↔ fichiers sources : mVAF v1.4/v1.5 relues dans le TSV **et moyenne
  bootstrap recalculée indépendamment** depuis les 200 réplicats → 0 écart.
- Relecture des 2 onglets vs TSV local → **0 écart sur 4 944 + 15 759 cellules**.
- Somme des 16 epic = 1,0000 et des 31 Loyfer = 1,0000 sur les 120 lignes renseignées.
- Les 77 parents existent tous dans `samples` (y compris 15 `*_rebasecalled_V5.0.0_trimmed`) et
  ont tous `nb_reads_total ≥ 30 M` → la condition amont du pipeline est confirmée, et l'onglet
  `mVAF` n'a **aucun `NA` côté valeurs initiales**.

## Corrections apportées à la doc v28 au passage (vérifiées par exécution)

- Les onglets horaires font **16 et 51 colonnes**, pas 15 et 50 (le README et la mémoire
  oubliaient la colonne `ID complet` = le row name concaténé `{base}_{labo}_{palier}`).
- `update-column-rarefaction-horaire -s <inexistant>` **ne crée plus de ligne** : le garde-fou
  existe dans le code. Le gotcha noté en v28 est périmé.

## État (03/09/2026)

**308 lignes** = 176 CGFL (44 bases) + 132 HCL (33 bases), 77 bases × 4 paliers, 77 par palier.
BAM 308/308 · PROD 120 · métriques QC + Loyfer 123 · mVAF + epic 120.
Backup `samples_status.backup-pre-rarefaction-horaire-threshold-*.duckdb`,
checkpoint `checkpoint-pre-rarefaction-horaire-threshold` (sur `388f777`).

Liens : [[project_schema_v28_rarefaction_horaire]] (le calque), [[project_schema_v16_rarefaction]]
(PK composite v17), [[project_probs_bootstrap_mode]] (même moyenne des 200 réplicats).
