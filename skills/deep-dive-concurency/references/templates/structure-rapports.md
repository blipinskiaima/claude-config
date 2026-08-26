# Plan type des deux rapports rédigés

Ce sont les plans **réellement suivis** par 6 des 7 dossiers en place au 26/08/2026 (Guardant
Health, Natera, DELFI Diagnostics, Singlera Genomics, ClearNote Health, Geneseeq). Freenome, le
plus ancien, garde un plan différent — c'est l'exception, pas le modèle. S'aligner sur les six :
un lecteur qui passe d'un dossier à l'autre doit retrouver le même numéro pour la même question.

**Cible : 6-8 pages PDF par partie.**

---

## Les faits majeurs ne sont plus une section — ils sont le volet P0

**Avant d'écrire quoi que ce soit d'autre**, lire :

```bash
cd ~/Pipeline/Aima-Survey && python3 cli.py competitive-majeurs "{CIBLE}"
```

⚠ **Ne pas coller cette sortie en `## 0. Faits majeurs`.** C'était la règle jusqu'au 30/07/2026 ;
depuis, ces faits vivent dans `{SLUG}-P0-MAJEURS.md`, régénéré chaque lundi depuis
`competitive_events` par la même fonction `faits_majeurs()`. Une copie figée dans P1/P2 se
périmerait sans que personne ne le voie. La commande sert à **savoir ce que P0 dira**.

**La règle de fond, elle, ne change pas** : chaque fait majeur doit être **traité dans le corps**
des deux rapports. Un rapport dont un fait majeur n'apparaît qu'en sous-section est un rapport
raté, même si l'information y est. Cas mesuré le 2026-07-30 : l'inclusion de SimpleScreen CRC
dans la guideline ACS (2026-05-27) était en §2.4 du P2 Freenome — page 3 — pendant que
l'approbation FDA du 2026-07-27, plus **récente**, ouvrait le document. Deux mois d'écart
suffisaient à enterrer un fait aussi lourd.

**Majeur = ce qui change leur droit de vendre, ou qui paie.** Autorisation réglementaire,
recommandation professionnelle (ACS, NCCN, USPSTF), décision de remboursement. Ni la date ni
le volume n'entrent en compte.

Si la commande ne rend rien : l'écrire, et vérifier que les bons canaux du concurrent sont
surveillés (bloc `watch`, phase 6) avant d'en conclure qu'il ne se passe rien.

Un `## 0.` reste légitime pour **cadrer** — « pourquoi ce concurrent, et pourquoi maintenant »
(ClearNote), « ce qui est dans notre sujet et ce qui ne l'est pas » (Natera, dont l'essentiel de
l'activité est hors périmètre). C'est une section de périmètre, pas une liste de faits.

---

## P1 — `concurency/profils/{SLUG}-P1-TECHNIQUE.md`

En-tête : public visé, date, sources, renvoi vers P2, rappel compact des marqueurs.

**1. Ligne visée & maturité** — à laquelle de nos deux lignes ils s'opposent (MRD via mVAF v1.4,
MCED via THEMELIO, ou aucune), ce que fait le test en une phrase, puis ce qu'il **ne** mesure
**pas** — souvent le plus informatif (« ni méthylation, ni mutations, ni bisulfite ») — et où ils
en sont sur l'échelle LDT → marquage → approbation.

**2. Wet lab** — tableau : tube, délai, traitement, extraction, kit de librairie, séquenceur,
couverture, organisation en lots, insu. Marquer `[NON VÉRIFIÉ]` ce qui manque.

**3. Dry lab & signaux mesurés** — schéma ASCII du pipeline avec les **versions exactes** des
outils, puis un tableau des features avec leurs paramètres. Signaler les paramètres hérités d'un
papier antérieur. Inclure le fondement biologique : pourquoi le signal existe. Court, mais
indispensable pour juger de la transposabilité.

**4. Score, modèle & seuil** — la nature du modèle, ce qu'il sort, comment le seuil est fixé et
sur quelle population il est calibré.

**5. Performances — les trois niveaux** ⚠ section critique. Sous-sections séparées : valeurs
observées, validation croisée (avec avertissement de ne pas les citer), estimation repondérée,
chiffres marketing. Puis lecture critique et réserves méthodologiques.

**6. Comparaison technique avec AIMA** — tableau axe par axe, puis l'argument scientifique
central en quelques lignes avec un schéma à flèches.

**7. Verrous AIMA — grille de cross-check** — reprendre les verrous du §7 du profil AIMA un par
un et dire, pour chacun, si ce concurrent le franchit, le contourne ou s'y heurte. C'est la
section qui transforme un dossier en décision : elle dit ce qui reste défendable chez nous.

**Corpus** — tableaux par rôle avec PMID cliquables, en signalant les chiffres trompeurs
directement dans la colonne « rôle ».

**Incertitudes à lever** — liste numérotée.

**Journal de mise à jour** — une ligne datée par révision, ce qui a changé et pourquoi. Présent
dans les 14 rapports en place : c'est ce qui permet de relire un dossier six mois plus tard sans
se demander ce qui est encore vrai.

---

## P2 — `concurency/profils/{SLUG}-P2-MARCHE.md`

En-tête identique, renvoi vers P1.

**1. En bref** — 4 points maximum, chacun en 2 lignes. C'est la seule partie que certains
lecteurs liront. **Les faits majeurs de P0 doivent y être repris et analysés**, pas seulement
listés : P0 dit ce qui s'est passé, le §1 dit ce que ça change.

**2. Où ils en sont commercialement** — tableau, avec les `[NON VÉRIFIÉ]` assumés (prix,
volumes). Ajouter une ligne « lecture » : ce que le silence sur certains chiffres signifie.
Y loger la feuille de route produit quand elle existe.

**3. Réglementaire** — statut réel, et distinguer désignation d'approbation. Frise ASCII si le
contexte a bougé. Terminer par « ce que ça change pour nous ».

**4. Remboursement** — souvent le point faible, et l'enseignement le plus utile pour notre
propre calendrier. Chez Guardant et Natera c'est au contraire leur vraie avance : le titre de
section peut le dire (« Remboursement — leur douve la plus profonde »).

**5. Solidité financière** — levées, dirigeants, effectifs, trésorerie et horizon de cash,
signaux faibles clairement étiquetés comme tels.

**6. Paysage concurrentiel & marché** — tableau des acteurs et tableau international, les
constats stratégiques marqués ⚠ (espace déjà occupé) et ✔ (espace libre), puis une sous-section
sur la fenêtre française (IMPULSION, adhésion réelle au dépistage). Y intégrer les essais
cliniques en identifiant **l'échéance à surveiller**, et la fragilité scientifique s'il y a
controverse : l'angle d'attaque, mais aussi la question qui nous sera posée à nous.

**7. Implications pour AIMA** — trois blocs : ce qu'il faut retenir de leur modèle, ce qui doit
nous alerter, notre angle défendable.

**8. À surveiller** — liste numérotée et priorisée.

**Corpus**, **Incertitudes à lever**, **Journal de mise à jour** — comme en P1.

---

## Éléments de forme qui fonctionnent

- **Schémas ASCII à flèches** pour les pipelines et les enchaînements réglementaires
- **Tableaux** pour tout ce qui est énumérable ; prose pour l'analyse
- **Citations en bloc** (`>`) pour les avertissements méthodologiques
- **⚠ et ✔** pour marquer les constats stratégiques dans les tableaux
- **★** pour signaler le papier à lire en priorité ET tout fait majeur (jamais ⭐, absent de
  la police PDF). Le ★ doit rester réservé à ces deux usages : s'il marque tout, il ne marque
  plus rien.
