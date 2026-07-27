# Context — Aima-Survey — 2026-07-27T15:19:41+0000

**Branche** : main
**Dernier commit** : d1e4c0d — docs: profil AIMA canonique (Exis 1.1) + 1re fiche concurrent Signatera
**Status** : 10 fichiers non commités (tous PRÉ-EXISTANTS hors session : COMPETITORS.md, rapports FREENOME/GENESEEQ/GUARDANT, images, SYNTHESE)

## Où j'en suis
Refonte du skill `/deep-dive-concurency` en 3 parties (profil AIMA / extraction concurrent / comparaison), terminée et testée de bout en bout sur Natera Signatera. Profil AIMA mis à jour avec le rapport Exis 1.1. Le skill (~/.claude) sera commité par commit-claude ; le test Signatera s'est arrêté avant la Phase 6 (rapports P1/P2 + diff competitors.json non produits).

## Ce qui marche / ce qui foire
- ✓ Architecture 3 parties câblée, liens vérifiés, docs/AIMA-POSITIONING.md = profil canonique (Exis 1.1 : mVAF v1.4 82%/95,1%)
- ✓ Template fiche concurrent + 1re fiche NATERA-SIGNATERA-PROFIL.md fact-checkée (5 erreurs corrigées avant rédaction)
- ✓ Fact-check a bloqué le faux parallèle 82% détection AIMA vs 88-94% MRD-surveillance Signatera
- ✗ Profil AIMA n'a que des perfs de DÉTECTION (Exis), pas de MRD longitudinale → diff de perfs impossible face à un pur concurrent MRD (gap n°1)
- ✗ competitors.json contient le « 94/98 » Signatera non contextualisé (vessie-spécifique) — à corriger
- ✗ Volet marché AIMA (§8) encore squelette [À PRÉCISER]

## Prochaine étape
Décider de la Phase 6 du test Signatera : (a) générer les rapports P1/P2 + PDF, (b) diff competitors.json pour corriger le 94/98, ou (c) combler les gaps du profil AIMA (perfs MRD, volet marché).
