# Context — Aima-Survey — 2026-07-22 16:12

**Branche** : main
**Dernier commit** : 7049e19 — docs: audit prod + veille concurrentielle DELFI/FirstLook
**Status** : clean (le PDF généré est gitignoré)

## Où j'en suis

Session d'**audit et de veille, sans aucune modification de code**. Après 3 mois de pause,
reprise du projet : vérification de l'état de prod, cartographie du couplage avec Aima-Tower,
puis production d'un dossier de veille concurrentielle sur DELFI/FirstLook Lung (2 markdown
+ 1 PDF combiné de 13 pages).

Point d'arrêt : **un bug de production est identifié, documenté et volontairement NON corrigé**
— il attend un arbitrage produit de Boris.

## Ce qui marche / ce qui foire

- ✓ Cron sain : 707 articles, tous scorés et classifiés, dernier run 22/07 08:00
- ✓ Rapports de veille DELFI livrés (P1 technique bioinfo + P2 marché direction), chiffres
  vérifiés contre les publications en texte intégral par un agent de fact-check adversarial
- ✗ **Bug `entrez_date`** : `lib/fetcher.py` l'omet du dict passé à `upsert_article` depuis le
  2026-04-21 → `first_seen_at` retombe sur `now()`. ⚠ Le fix naïf **casserait Aima-Tower**
  (écart médian EDAT/découverte = 28 j → ~50 % des articles sortiraient de la vue « semaine »)
- ✗ **DB sans backup** : `data/` gitignoré, 707 articles + 3 mois de scoring Haiku en un seul
  exemplaire ; fichier gonflé à 117 Mo pour 1,85 Mo de texte réel
- ✗ **Doc fausse corrigée** : le CLAUDE.md des deux projets affirmait que day/week parsent le
  markdown — faux depuis le 2026-04-22, toutes les vues de Tower lisent DuckDB
- ⚠ `poppler-utils` absent du serveur (`sudo apt-get install -y poppler-utils`) ; contourné par
  un venv jetable dans le scratchpad, qui ne survivra pas à un redémarrage

## Prochaine étape

Trancher le **backup de la DuckDB** (seul risque irréversible), puis arbitrer la sémantique
voulue pour `first_seen_at` — date de découverte (comportement actuel, bon pour la veille) ou
date d'indexation PubMed — avant de corriger `lib/fetcher.py` + `lib/db.py:167-168` **ensemble**.
