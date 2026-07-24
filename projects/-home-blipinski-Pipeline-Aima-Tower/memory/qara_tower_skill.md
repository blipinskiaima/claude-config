---
name: qara-tower-skill
description: "Skill /qara-tower : traçabilité QARA temporelle d'Aima Tower (snapshot/compare/append Doc), journal JSONL immuable, baseline T0, portable local+global."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4dce2525-c204-49e3-b772-79405ebe19b5
  modified: 2026-07-24T12:42:59.557Z
---

# Skill /qara-tower (2026-07-24)

Traçabilité QARA de l'évolution temporelle de la Tower au fil des ajouts de samples dans
trace-prod. Chaque exécution T_n : mesure → compare à T_{n-1} → synthèse au Google Doc → journal.
Créé via `/meta-skills-creator`.

## Emplacement (double, journal partagé)

- Local : `Aima-Tower/.claude/skills/qara-tower/` (versionné projet).
- Global : `~/.claude/skills/qara-tower/` (invocable partout).

Les 2 copies partagent le **même journal** car les scripts utilisent des chemins ABSOLUS
(`~/Pipeline/Aima-Tower/...`), jamais relatifs à l'emplacement du skill. Copie globale à
resynchroniser à la main après modif locale (ou via `/commit-claude` pour le repo config).

## Structure

- `scripts/qara_lib.py` : config (réglages Exis figés + chemins absolus) + `take_snapshot()`.
- `scripts/snapshot.py` : mesure (`--out` / `--persist` / `--persist-file`).
- `scripts/compare.py` : diff T_n vs T_{n-1} (deltas agrégés + entrants/sortants/changements nominatifs).
- `scripts/append_gdoc.py` : append au Google Doc via API Docs `batchUpdate`/`insertText` (**non destructif**).
- `references/` : metrics-baseline, snapshot-format, report-format.

## Décisions clés

- **Réglages figés (mode Exis)** : mVAF v1.4, cohorte Avancés, 95 %, dorado v5.0.0+v5.2.0.
  Non modifiables (sinon perte de comparabilité temporelle).
- **Aucun recalcul maison** : appelle `ExploratoryAnalysisService.compute()` / `compute_cohort_cascade()`.
- **Anti-lock DuckDB** : snapshot COPIE trace-prod dans un tmp avant de mesurer (le daemon
  check_samples tient le lock write ; `_load_from_duckdb` n'a pas de retry).
- **Journal** `qara/qara_snapshots.jsonl` — **PAS `data/`** (gitignored, ligne 18 du .gitignore).
  Versionné git = historique QARA immuable. 1 ligne/point, inclut `{unique_id: statut}`
  (`cancer`/`sain`/`sans_etiquette`/`precoce`) pour le diff nominatif.
- **`--persist-file`** : journalise EXACTEMENT le snapshot comparé (pas de re-mesure qui
  divergerait si la DB bouge entre compare et persist).
- **Ordre critique** : append Doc AVANT `--persist` (sinon T_n devient sa propre référence).
- Google Doc de suivi = le **même** que le user guide (`1dOYIB-NDehUZYsuJi6hKalyG3YpvseSgNCDUqhdtZvs`).
- Nom `qara-tower` (convention minuscules) ; invocation `/QARA-Tower` marche aussi (insensible casse).

## Baseline T0 (24/07/2026)

trace-prod 1471, cohorte 261 cancer + 224 sain, seuil 0,0042, sens 82 % (214/261),
spéc 95,1 % (213/224). Bloc T0 ajouté au Doc + 1ère ligne du JSONL. Commit `6df189d`.
Tag `pre-qara-skill`. Voir aussi : [[exis_alignment]].
