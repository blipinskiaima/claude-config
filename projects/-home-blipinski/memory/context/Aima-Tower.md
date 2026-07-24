# Context — Aima-Tower — 2026-07-24 (clôture session)

**Branche** : main (poussé, origin/main = 960ee8e)
**Dernier commit** : 960ee8e — docs: README v5.1.0 + CLAUDE.md (alignement Exis + skill QARA)
**Status** : clean (hors untracked .claude/worktrees/ et "Exis 1.1.pdf", hors scope)

## Où j'en suis
Session close via /end-session. Deux livrables majeurs, tous deux déployés/poussés :
(1) page /exploration alignée sur le rapport réglementaire Exis 1.1 (mVAF v1.4),
(2) skill /qara-tower de traçabilité QARA temporelle avec baseline T0 posée.

## Ce qui marche / ce qui foire
- ✓ /exploration reproduit le PDF Exis 1.1 **au chiffre près** : seuil quantile type 1
  (0,0042), exclusion CGFL_26BM01841, sélecteur Cohorte Avancés/Précoce (§2.2/§2.3),
  cohort_mode threadé partout. Prod rebuild + validée live.
- ✓ Skill /qara-tower opérationnel, **double** (local + ~/.claude, même journal), T0
  écrit dans le Google Doc (append non destructif) + qara/qara_snapshots.jsonl (versionné).
- ✓ 5 commits poussés, tests 10 passed/4 skipped, typecheck front OK.
- ✗ Rupture **assumée** de l'équivalence cell-by-cell vs pipeline R *main* (type 1 vs
  type 6) → TestRegressionVsR désactivé (skip). Choix Boris.
- ℹ Seul écart accepté Tower↔PDF = Prostate_21 (donnée passée cancer le 23/07, après le PDF).
- ℹ Copie globale du skill ~/.claude/skills/qara-tower/ pas encore commitée dans claude-config.

## Prochaine étape
Rien en cours. Au prochain point temporel (semaines/mois, après ajout de samples dans
trace-prod) : lancer /qara-tower pour enregistrer T1 vs T0. Optionnel : corriger 2 libellés
obsolètes de la cascade (« trace-prod brut liquid+solid » affiche 1324 liquid seuls ;
« Score mVAF v1 disponible » alors qu'en mode v1.4 c'est v1.4 qui est testé).
