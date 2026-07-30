---
name: freenome-poumon
description: "Freenome a bien un programme poumon (SimpleScreen Lung), ses perfs sont toutes à 50 % de spécificité, et competitors.json est périmé sur son statut FDA"
metadata: 
  node_type: memory
  type: reference
  originSessionId: fdd4f2ac-8635-4303-a86c-70045baa73f3
  modified: 2026-07-28T13:54:56.319Z
---

Établi le 2026-07-28 par reconnaissance vérifiée (SEC 424B4, ClinicalTrials.gov v2, openFDA,
newsroom). ⚠ `data/competitors.json` dit encore **« NON approuvé FDA au 07/2026 »** — périmé,
non corrigé faute de validation Boris (règle : pas d'écriture factuelle sans son accord).

## Ce qui est établi

- **SimpleScreen Lung** (« Lung v1 ») est leur **2ᵉ produit commercial**, pas un projet de
  recherche. Techno : **méthylation cfDNA base-resolution + immunodosages protéiques**
  (SEC 424B4 p.233). LDT sous CLIA annoncé au **2ᵉ semestre 2026**, PMA sans date.
- **Aucun statut FDA sur le poumon** : ni PMA, ni 510(k), ni De Novo, ni Breakthrough
  (0 occurrence de « Breakthrough » dans le 424B4 complet).
- **SimpleScreen CRC approuvé par la FDA le 2026-07-27**, Abbott commercialise, jalon 100 M$.
- **Coté au Nasdaq (FRNM), CIK 0002017526.** ⚠ Piège d'identité : ce CIK s'appelait
  *Perceptive Capital Solutions Corp* (SPAC) jusqu'au **2026-07-15** ; `tickers = ["PCSC","FRNM"]`.
- Essai pivot **PROACT LUNG NCT06122077** : ~8 000 inclus / 20 000 cibles, adossé au LDCT.
  **`RECRUITING`, complétion primaire au 2026-06-15 dépassée, dernière mise à jour 2025-08-05.**
- Une seule publication peer-review poumon, et elle porte sur EarlyCDT-Lung, pas sur leur test.
- Ils **ont** des features fragmentomiques et de l'IP 5hmC au niveau plateforme (424B4 p.236),
  mais ne les revendiquent pas dans le produit poumon. Seul le CNV est réellement absent.

## Le point qui décide de toute comparaison

**Toutes leurs perfs poumon sont à ~50 % de spécificité. Aucune à ≥90 % n'existe.**

| | valeur | nature |
|---|---|---|
| sensibilité brute | **88,8 %** @ 50 % spéc. | seule valeur OBSERVÉE |
| sensibilité pondérée IUP | 85,7 % @ 50 % | repondérée |
| stade I | 76,6 % @ 50 % | repondérée, IC ~21 pts |

Cohorte n=636, répartition cas/témoins **non divulguée**. Les 90,7 %/80,4 % du communiqué de
mars 2026 sont des chiffres de **développement** (n=673), repondérés.
→ À 50 % de spécificité ce n'est pas un test de dépistage autonome, au mieux un enrichissement
amont du LDCT (~7 M de faux positifs par cycle sur 14-15 M d'éligibles US).

Voir [[aima-poumon-perfs-par-stade]] pour le mur de spécificité côté AIMA,
[[veille-concurrentielle-collecteur]] pour la procédure qui suit ce concurrent.
