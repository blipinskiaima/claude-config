---
name: qc-status-exis-themelio
description: "Statut QC par produit (exis/themelio _qc_status + _qc_reason) dans metadata.json — arbre de decision de l onglet Synthese, process QC_status, module retro RETRO_REPORT, gotcha du glob S3 CGFL, cablage trace-prod v34"
metadata: 
  node_type: memory
  type: project
  originSessionId: 91db610d-3471-4bee-af3e-ed164ac490eb
  modified: 2026-09-08T17:40:18.789Z
---

# Statut QC Exis / Thémélio (2026-09-08)

Source des regles : Google Doc QC, onglet `Synthèse` (`t.bw3qo6n8aizg`), **2 images PNG** (arbres), pas du
texte. Arbres identiques sauf le noeud amplitude. Ordre, seuils et libelles valides par Boris :

| # | critere | defaut si | raison (`QC reason`, anglais) | Exis | Thémélio |
|---|---|---|---|---|---|
| 1 | molecules A+D (cramino `num_reads` col 6) | `< 5 M` | Insufficient number of molecules | FAILED | FAILED |
| 1' | idem, **branche parallele** | `5 M <= x < 20 M` (20 M pile = OK) | Limited number of molecules | WARNING | WARNING |
| 2 | profondeur (mosdepth `total` col 4) | `< 0,25` | Insufficient depth | FAILED | FAILED |
| 3 | `amplitude_fragmento_qc` | `< 80` | Non-plasma-like sample | **WARNING** | **FAILED** |
| 4 | `ratio_n50_n75_filtered > 1,5` OU `pct_mass_removed > 30` | | Genomic DNA contamination | WARNING | WARNING |
| 5 | non alignes `idxstats '*' / (A+D) > 30 %` | | Non-human DNA contamination | WARNING | WARNING |

- Chemin principal = **premier critere en defaut puis stop** ; la branche 5-20 M s ajoute. **Le pire statut
  gagne ; raisons triees par gravite (FAILED avant WARNING) puis ordre de l arbre**, separateur `; `.
  Ex : 8 M + profondeur 0,1 -> `Insufficient depth; Limited number of molecules` ; 8 M + amp 70 (Exis) ->
  `Limited number of molecules; Non-plasma-like sample`.
- Metrique absente/non numerique quand l arbre l atteint -> statut `NA`, raison `Missing metric: <x>` ;
  un FAILED trouve avant reste FAILED. Bornes strictes comme ecrites (0,25 / 80 / 1,5 / 30 pile = OK).
- Les colonnes ratio/masse sont celles que lit trace-prod (`_filtered`), l onglet ayant ete chiffre dessus.
- Seuils gDNA de l arbre (1,5 / 30 %) != anciens 1,26-1,43 / 22 % de [[n50-ratio-qc]] : l arbre fait foi.

## Implementation (option B validee : process dedie, l arbre n existe qu une fois)

`workflow/rapport.nf` : process **`QC_status`** (un awk, ~45 l.) -> `QC/{ID}.qc_status.tsv` (header +
1 ligne : name / exis_qc_status / exis_qc_reason / themelio_qc_status / themelio_qc_reason, raison vide si
conforme). `Raima_report` le relit par nom de colonne (`qstr`) -> 4 champs JSON, **29 -> 33 champs**,
`exis_qc_*` apres `exis_quantification_threshold`, `themelio_qc_*` apres `themelio_OutlierPattern_threshold`.
Cablage : `frag.nf` emit `qc` (n50 + amplitude avec ID), `qc.nf` `BAM_Idxstats` en tuple + emit
`QC_merged.idxstats`, `exis.nf` le remonte, `main.nf` `Rapport(..., Exis.out.idxstats, Frag.out.qc)`,
`base.config` withName QC_status. Valide : 19 cas fabriques, Lung_9 SUCCESS, Healthy_826 FAILED,
JSON QUALIF V2.3.0 inchange sur ses 29 champs. Tag rollback `pre-qc-status` (62d9bf9).

## Retro `--RETRO_REPORT` (workflow/retro_report.nf, temporaire)

Reutilise `QC_status` + `Raima_report` sur les 10 fichiers publies sous `${output}/{ID}/` (< 10 Ko chacun,
aucun recalcul) ; cramino ancien nom `{ID}.cramino.tsv` en repli (14 samples) ; `raima_version.txt` jamais
publie -> fichier **vide** -> `version_raima: null` (le garde-fou `"Non disponible"` de Raima_report ne
peut pas matcher : l awk retire les espaces AVANT de comparer, quirk preexistant). `version_bam2beta` =
manifest du run retro, `patient_name` = `params.patient_id` (DEV) — accepte tel quel.
Idempotent : skip si le JSON porte deja `exis_qc_status`. Les 157 anciens JSON (majoritairement schema
10 champs de juin) sont sauvegardes en `REPORT/metadata.json.pre_qc_status` avant ecrasement.
Couverture : **1366 / 1379** liquides (854 CGFL + 512 HCL) ; 13 skips = 12 sans aucune sortie + 1 sans
THEMELIO ; `LOG/` a la racine du labo est attrape par le glob et skippe.

## ⚠ Gotcha : le glob `RetD/liquid/CGFL/*` casse cote S3

`Channel.fromPath(".../CGFL/*", type:'dir')` meurt **4/4** apres ~40 s : `Failed to parse XML document
... ListBucketHandler` dans le `PathVisitor` (listObjects de `readAttributes`), meme bride
(`aws.client.maxConnections 8`, `maxForks 4`) et meme par sous-lots (`CGFL/B*`), alors que
`RetD/liquid/HCL/*` (514 dossiers) passe et qu un `--input` sur **un seul dossier** passe toujours.
Suspect non confirme : le dossier residuel `CGFL/Twist_0%` (6 cles de lanceur prod, pas un sample) — un
`--input .../Twist_0%` seul ne reproduit pas. Sortie : HCL par glob, **CGFL lance par Boris** (enumeration
via `data/CGFL/liquid/*`, 872 dossiers dont les 854 eligibles, proposee et verifiee cote couverture).
Les runs de ce jour ont tourne sous Nextflow **25.04.8** (tmux) et 25.10.2 (shell interactif).

## Resultat cohorte (2026-09-08)

CGFL 854 : 449 S/S, 223 W/W, **105 W/F** (amplitude < 80, urines), 77 F/F. HCL 512 : 475 / 31 / 6.
`Non-human DNA contamination` **ne sort jamais** : les 28 samples > 30 % non alignes sont tous arretes
avant (14 molecules, 8 profondeur, 6 amplitude) — dernier critere inatteignable par construction.
`Genomic DNA contamination` 6 fois, toujours couple a « molecules limite ».

Voir [[metadata-json]] (contrat), [[n50-ratio-qc]], [[read-counting-cascade]] (strates A/D), et cote
trace-prod `project_schema_v34_qc_status` (4 colonnes retd_suivis lues dans le JSON, pattern preserve).
