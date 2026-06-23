# Context — Bam2Beta — 2026-06-23T14:12:06+0000

**Branche** : main
**Dernier commit** : 918ddb0 — docs: update CHANGELOG and README for V1.3.3
**Status** : clean (seul dev/SCW/bacasable.sh untracked, sandbox ignoré)

## Où j'en suis
Session terminée : feature **Check_Input** (QC des fichiers d'entrée en amont du merge)
implémentée + **retrait du rapport PDF**, version **V1.3.3 publiée ET qualifiée en
production** (QUALIF OK 3/3). Aucune tâche en cours.

## Ce qui marche / ce qui foire
- ✓ Check_Input : input KO → run SUCCESS + REPORT/metadata.json (status=FAILED_QC_INPUT + reason), seul Check_Input ; input OK → pipeline normal ; autre erreur → crash standard
- ✓ Retrait PDF : génération rmarkdown désactivée, conformité (2 scripts) + doc nettoyées ; Raima_report → JSON uniquement
- ✓ Gotcha NF documenté : channel vide → emit de sous-workflow qui plante (No such property DataflowBroadcast) → fix = retrait emits inutilisés (Beta_epic/Frag/IV). Voir [[check-input-qc]]
- ✓ V1.3.3 : /test_bam2beta TEST OK 3/3 + /qualif-bam2beta QUALIF OK 3/3 (bit-à-bit vs V1.3.2), tag + release GitHub publiés
- ✓ Score mVAF prod = raima:latest **0.5.0** (vérifié : 0.5.2 = bootstrap R&D `--bootstrap` uniquement, inactif en prod/qualif)
- ⏳ Cas "input absent" (dossier inexistant) : pas de json possible dans NF (checkIfExists plante à l'init) ; dossier vide existant → json OK. Garde-fou amont (bash) si besoin, non implémenté

## Prochaine étape
Rien de bloqué. Optionnel si le cas se présente en prod : garde-fou bash (input absent → json
d'échec) dans launch_SCW.sh. Sinon, prochaine feature.
