# Plan type des deux rapports

Éprouvé sur l'analyse DELFI/FirstLook (juillet 2026). Adapter, ne pas suivre servilement.
**Cible : 6-8 pages PDF par partie.**

---

## §0 — Faits majeurs ⛔ OBLIGATOIRE, EN TÊTE DES DEUX RAPPORTS

**Avant d'écrire quoi que ce soit d'autre**, produire le bloc :

```bash
cd ~/Pipeline/Aima-Survey && python3 cli.py competitive-majeurs "{CIBLE}"
```

Coller la sortie telle quelle en `## 0. Faits majeurs`, juste après l'en-tête, dans **P1 ET
P2**. Chaque fait majeur doit ensuite être **traité dans le corps** du rapport — le §0 annonce,
il ne remplace pas l'analyse.

Un rapport dont un fait majeur n'apparaît qu'en sous-section est un rapport raté, même si
l'information y est. Cas mesuré le 2026-07-30 : l'inclusion de SimpleScreen CRC dans la
guideline ACS (2026-05-27) était en §2.4 du P2 Freenome — page 3 — pendant que l'approbation
FDA du 2026-07-27, plus **récente**, ouvrait le document. Deux mois d'écart suffisaient à
enterrer un fait aussi lourd. Le même évènement, chez Guardant, était en §1 : rien dans cette
procédure ne l'imposait, c'était l'initiative d'un rédacteur.

**Majeur = ce qui change leur droit de vendre, ou qui paie.** Autorisation réglementaire,
recommandation professionnelle (ACS, NCCN, USPSTF), décision de remboursement. Ni la date ni
le volume n'entrent en compte.

Si la commande ne rend rien : l'écrire, et vérifier que les bons canaux du concurrent sont
surveillés avant d'en conclure qu'il ne se passe rien.

---

## P1 — `{CIBLE}-P1-TECHNIQUE.md`

En-tête : public visé, date, sources, renvoi vers P2, rappel compact des marqueurs.

**0. Faits majeurs** — cf. ci-dessus. Obligatoire.

**1. Le principe** — une phrase sur ce que fait le test, puis ce qu'il **ne** mesure **pas**
(c'est souvent le plus informatif : « ni méthylation, ni mutations, ni bisulfite »).

**2. Wet lab** — tableau : tube, délai, traitement, extraction, kit de librairie, séquenceur,
couverture, organisation en lots, insu. Marquer `[NON VÉRIFIÉ]` ce qui manque.

**3. Dry lab** — schéma ASCII du pipeline avec les **versions exactes** des outils, puis un
tableau des features avec leurs paramètres. Signaler les paramètres hérités d'un papier
antérieur. Décrire le modèle et son seuil.

**4. Fondement biologique** — pourquoi le signal existe. Court, mais indispensable pour juger
de la transposabilité.

**5. Performances — les trois niveaux** ⚠ section critique. Sous-sections séparées : valeurs
observées, validation croisée (avec avertissement de ne pas les citer), estimation repondérée,
chiffres marketing. Puis lecture critique et réserves méthodologiques.

**6. Comparaison technique avec AIMA** — tableau axe par axe, puis l'argument scientifique
central en quelques lignes avec un schéma à flèches.

**7. Perspectives** — ce que la littérature démontre, le repère de performance à battre, les
verrous techniques numérotés, un programme de travail en étapes, et ce qui reste à trancher
en interne.

**8. Corpus** — tableaux par rôle avec PMID cliquables, en signalant les chiffres trompeurs
directement dans la colonne « rôle ».

**9. Incertitudes à lever** — liste numérotée.

---

## P2 — `{CIBLE}-P2-MARCHE.md`

En-tête identique, renvoi vers P1.

**0. Faits majeurs** — cf. ci-dessus. Obligatoire, avant « En bref ».

**1. En bref** — 4 points maximum, chacun en 2 lignes. C'est la seule partie que certains
lecteurs liront. **Les faits majeurs du §0 doivent y être repris et analysés**, pas seulement
listés : le §0 dit ce qui s'est passé, le §1 dit ce que ça change.

**2. Statut commercial** — tableau, avec les `[NON VÉRIFIÉ]` assumés (prix, volumes). Ajouter
une ligne « lecture » : ce que le silence sur certains chiffres signifie.

**3. Réglementaire** — statut réel, et distinguer désignation d'approbation. Frise ASCII si le
contexte a bougé. Terminer par « ce que ça change pour nous ».

**4. Remboursement** — souvent le point faible, et l'enseignement le plus utile pour notre
propre calendrier.

**5. Financement et gouvernance** — levées, dirigeants, effectifs, signaux faibles clairement
étiquetés comme tels.

**6. Essais cliniques** — tableau, en identifiant **l'échéance à surveiller**.

**7. Feuille de route.**

**8. Fragilité scientifique** — la controverse, et notre lecture : l'angle d'attaque, mais aussi
la question qui nous sera posée à nous.

**9. Paysage concurrentiel** — tableau des acteurs, puis les constats stratégiques marqués ⚠
(espace déjà occupé) et ✔ (espace libre).

**10. Le marché** — tableau international, puis une sous-section sur la fenêtre française
(IMPULSION, adhésion réelle au dépistage).

**11. Implications pour AIMA** — trois blocs : ce qu'il faut retenir de leur modèle, ce qui doit
nous alerter, notre angle défendable.

**12. À surveiller** — liste numérotée et priorisée.

---

## Éléments de forme qui fonctionnent

- **Schémas ASCII à flèches** pour les pipelines et les enchaînements réglementaires
- **Tableaux** pour tout ce qui est énumérable ; prose pour l'analyse
- **Citations en bloc** (`>`) pour les avertissements méthodologiques
- **⚠ et ✔** pour marquer les constats stratégiques dans les tableaux
- **★** pour signaler le papier à lire en priorité ET tout fait majeur (jamais ⭐, absent de
  la police PDF). Le ★ doit rester réservé à ces deux usages : s'il marque tout, il ne marque
  plus rien.
