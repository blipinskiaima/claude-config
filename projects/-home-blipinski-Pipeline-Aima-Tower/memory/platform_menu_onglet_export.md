---
name: platform-menu-onglet-export
description: "Menu déroulant de /database-platform aligné sur l'onglet Platform de la gsheet Trace PROD (47 colonnes) + frise de /indicator par échantillon (2026-09-28, commit 434036b)."
metadata:
  node_type: memory
  type: project
  originSessionId: aefba143-77f2-4888-b903-68ff8a4eb3b6
  modified: 2026-09-28T15:09:17.969Z
---

# `/database-platform` — menu déroulant = onglet Platform + frise par échantillon (2026-09-28)

**Référence d'exhaustivité** : l'onglet `Platform` de la gsheet « Trace PROD » est écrit par
**trace-platform** (`lib/gsheets.py`, pas trace-prod malgré le nom du classeur) :
`COLUMNS` (40) + `MANUAL_COLUMNS` (2) + `VERSION_COLUMNS` (5) = 47, familles dans `META_ROW`.
⚠ La feuille n'a **pas de famille « Trace »** : la « trace » de la Tower = sa famille *Timestamp*.
⚠ La liste est **recopiée à la main** dans `PlatformView.tsx` → à resynchroniser quand
trace-platform ajoute une colonne à l'export. La feuille occulte aussi 168 samples
(`data/export_hidden_samples.tsv`), la Tower les montre tous — non traité, hors demande.

Choix Boris : **option B** (les 47 dans le menu, quitte à répéter la ligne du tableau),
puis ergonomie en deux côtés (résultats pipeline / parcours), statuts colorés, timestamps
sur fond distinct. Pas d'onglets dans le menu (choix réversible, validé « parfait »).

**Trois « presque doublons » gardés à côté des colonnes de la feuille** (règle : rien retiré) :
Arrivée = `COALESCE(copy_stop, created_at)` ≠ Copy Stop (121 sans copy_stop) ;
Done pipeline = done seul ≠ Pipeline Stop = `COALESCE(done, failed)` (82 échecs) ;
`pipeline_version` ≈ `version_bam2beta` (casse différente, 2 divergences V2.0.2/v2.2.0).
⚠ `analysis_name` vaut `MRD` partout : l'« Analysis » de la feuille est `product`.

**Frise par échantillon** : aucune durée recalculée — lue dans `/api/indicator/data`
(398 lignes, clé unique `(client_uuid, patient_name, sample_name)`), même SQL que
`/indicator`. `Frise`/`MODES`/`palette` exportés de `Flux.tsx`, prop `unique`
(« Temps mesuré »), défaut inchangé pour `/indicator`. Données repérées : AIMA_010
`copy_start` > `copy_stop` (segment Copy « — ») ; `transfer_start` avant `session_start`
tronque le premier segment (même règle stricte `>` qu'Indicator).

Vérif visuelle : `playwright-core@1.47` (Node 18 ; ≥1.48 exige Node 20) installé dans le
scratchpad + `chromium_headless_shell-1223`, page servie par le container `172.18.0.2:8050`
(pas d'auth en interne), clic sur la ligne puis screenshot du `td[colspan] > div`.

Voir [[indicator_page]], [[migration_platform_v15_upload_date]], [[database_scission_pages]].
