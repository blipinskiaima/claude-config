---
name: qara-tower
description: Traçabilité QARA (Quality Assurance / Regulatory Affairs) de l'évolution temporelle d'Aima Tower au fil des ajouts d'échantillons dans trace-prod. À chaque exécution, mesure l'état courant (T_n), le compare au dernier point enregistré (T_{n-1}), calcule les deltas d'effectifs / seuil / sensibilité / spécificité en réutilisant les fonctions de la Tower (aucun recalcul maison), justifie les variations par diff nominatif des échantillons, et ajoute une synthèse vulgarisée horodatée à la fin du Google Doc de suivi. Use when the user says "QARA-Tower", "traçabilité QARA", "point QARA", "checkpoint QARA", "suivi temporel de la tour", "T_n vs T_{n-1}", or wants to record a QARA point of Aima Tower after new samples were added to trace-prod.
---

# QARA-Tower

<objective>
Assurer la traçabilité réglementaire (ISO 15189) de l'évolution d'Aima Tower au fil des
ajouts d'échantillons dans trace-prod. Chaque exécution enregistre un point temporel T_n,
le compare au précédent, explique les écarts (effectifs, seuil, sensibilité, spécificité),
et consigne une synthèse vulgarisée horodatée dans le Google Doc officiel de suivi.

Le point T0 (baseline validée le 24/07/2026) est déjà aligné sur le rapport Exis 1.1 ;
les exécutions futures se comparent au dernier point du journal, jamais au PDF.
</objective>

## Réglages figés (mode Exis) — non modifiables

Toutes les métriques sont mesurées avec les réglages de référence : **mVAF v1.4 · cohorte
Avancés · spécificité 95 % · dorado v5.0.0+v5.2.0 · profondeur ≥ 0,25×**. Les changer
casserait la comparabilité temporelle. Détails et sources dans
[references/metrics-baseline.md](references/metrics-baseline.md).

## Prérequis

- Aima Tower dans `~/Pipeline/Aima-Tower`, trace-prod dans `~/Pipeline/trace-prod`.
- Credentials Google `~/.config/gspread/authorized_user.json` (scope drive/docs actif).
- Google Doc de suivi : **`1dOYIB-NDehUZYsuJi6hKalyG3YpvseSgNCDUqhdtZvs`** (le même que le user guide).

Les scripts utilisent des chemins absolus : le skill fonctionne à l'identique qu'il soit
invoqué depuis la copie locale (`Aima-Tower/.claude/skills/`) ou globale (`~/.claude/skills/`).

## Workflow

Exécuter dans cet ordre. Les scripts sont dans `scripts/` sous ce skill.

1. **Mesurer T_n** une seule fois (ce point servira à comparer, synthétiser ET journaliser) :
   ```bash
   python3 scripts/snapshot.py --out /tmp/qara_tn.json
   ```

2. **Comparer** au dernier point du journal :
   ```bash
   python3 scripts/compare.py --current /tmp/qara_tn.json
   ```
   Journal vide → `est_baseline: true` (c'est T0, pas de comparaison). Sinon → deltas
   agrégés + `entrants` / `sortants` / `changements_statut` nommés.

3. **Rédiger la synthèse** vulgarisée à partir du diff, en suivant
   [references/report-format.md](references/report-format.md). L'écrire dans un fichier,
   ex `/tmp/qara_bloc.txt`.

4. **Ajouter au Google Doc** (append à la fin, sans toucher l'existant) :
   ```bash
   python3 scripts/append_gdoc.py 1dOYIB-NDehUZYsuJi6hKalyG3YpvseSgNCDUqhdtZvs \
       --text-file /tmp/qara_bloc.txt --title "QARA — <timestamp du snapshot>"
   ```

5. **Journaliser le snapshot** — le MÊME que celui comparé (pas de re-mesure) :
   ```bash
   python3 scripts/snapshot.py --persist-file /tmp/qara_tn.json
   ```

6. **Committer le journal** (traçabilité immuable) :
   ```bash
   git -C ~/Pipeline/Aima-Tower add qara/qara_snapshots.jsonl
   git -C ~/Pipeline/Aima-Tower commit -m "qara: point <timestamp>"
   ```

## Navigation

| Fichier | Quand le lire |
|---|---|
| [references/metrics-baseline.md](references/metrics-baseline.md) | réglages Exis, baseline T0, définitions sourcées (seuil type 1, cancer_truth, cohorte Avancés/Précoce) |
| [references/snapshot-format.md](references/snapshot-format.md) | schéma du snapshot et du journal JSONL, statuts des échantillons, sortie de compare.py |
| [references/report-format.md](references/report-format.md) | gabarit de la synthèse vulgarisée à ajouter au Doc, avec exemple |

## Règles impératives

- **Aucun recalcul maison** : les scripts appellent `ExploratoryAnalysisService.compute()` /
  `compute_cohort_cascade()`. Ne jamais réimplémenter une métrique ailleurs.
- **T0 ne se compare à rien** ; chaque T_n se compare au dernier point du journal.
- **Ordre critique** : append au Doc (étape 4) AVANT la journalisation (étape 5). Sinon T_n
  devient sa propre référence et le prochain diff sera vide.
- Le journal `qara/qara_snapshots.jsonl` est **immuable** : on ajoute une ligne, on ne
  réécrit jamais les précédentes.
- **Ne jamais** modifier les réglages Exis figés sans décision explicite de Boris (rupture
  de comparabilité réglementaire).
