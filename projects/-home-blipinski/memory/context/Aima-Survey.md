# Context — Aima-Survey — 2026-07-30T21:20:36+00:00

**Branche** : main
**Dernier commit** : a144944 — merge: dossiers concurrent en 4 volets, pondération par importance, taxonomie à 3 niveaux
**Status** : clean (1 fichier non suivi : SYNTHESE-42285091-fragmentia-ai.md)

## Où j'en suis
Veille concurrentielle complète et déployée : 7 dossiers en 4 volets (P0 faits
majeurs, P1 technique, P2 marché, P3 trajectoire), onglet AIMA de comparaison
chiffrée, pondération des évènements par importance. Tout est poussé sur main
dans les 3 dépôts. Dernière tâche de la session : synthèse QC sur les seuils
Bam2Beta (5M reads / 0,25×), livrée en analyse — aucun code modifié.

## Ce qui marche / ce qui foire
- ✓ Cron lundi 10h00 (`run_profils.sh`) : P0 + P3 + 7 PDF, testé de bout en bout,
  flock partagé avec les 2 crons quotidiens de 8h00
- ✓ Onglet AIMA : chiffres recalculés à la spécificité DE CHAQUE concurrent
  (fenêtre 80–99 %), 5/7 comparables. Conforme au rapport Exis au sample près
  (214/261 @ 95,1 %, seuil 0,0042)
- ✓ Pondération : ACS + FDA sortent en tête chez Freenome ET Guardant. 206 tests
- ✓ Seuils QC Bam2Beta instruits : Katsman 2022 (PMID 35841107) publie la même
  règle en ONT natif à 2,5M/0,2× — nous sommes 2× plus stricts. Longueur alignée
  médiane mesurée à 172 pb sur 1 469 échantillons
- ✗ CLEARNOTE-HEALTH-P1 non vérifié par la 2e passe (erreur serveur) — seul
  fichier sur 12 à ne pas avoir été relu
- ✗ 3 concurrents (DELFI, Singlera, Geneseeq) sortent 0 fait majeur : signal de
  couverture de collecte, leurs canaux réels ne sont pas surveillés
- ✗ Le cron hebdo n'envoie AUCUN email : il peut signaler des tensions et des
  évènements non versés sans que personne ne le sache

## Prochaine étape
Câbler l'email du lundi dans `run_profils.sh` (faits majeurs nouveaux, tensions
§4.2, dette §4.1 par dossier, + email d'échec) — sur le modèle de `competitive.py`.
Sinon : reprendre la vérification de CLEARNOTE-HEALTH-P1.
