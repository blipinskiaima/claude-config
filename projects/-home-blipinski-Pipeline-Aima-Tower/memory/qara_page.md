---
name: qara-page
description: "Page /qara (3 onglets Exis/Themelio/CUP) : première page 100 % statique du projet, régime de recopie stricte, et la divergence prouvée du document CUP."
metadata: 
  node_type: memory
  type: project
  originSessionId: 0e4d3284-268d-48ce-a44a-c347ecc2ad51
  modified: 2026-08-26T08:57:41.807Z
---

# Page `/qara` — Exis 1.1, Themelio 1.0, CUP 1.0 (2026-08-21)

Restitution visuelle des sections de performance du Google Doc `Aima_QARA`
(`1MBMc_q6NXQcKlFZWPk3sngqcyO3NJVDokm6Epyv-dAY`). Entrée sidebar dans le groupe
`core`, juste sous Tableau de bord (choix Boris : mise en évidence).

## Ce qui rend cette page différente de toutes les autres

C'est la **première page de contenu 100 % statique** du projet. Vérifié à
l'exploration : toutes les autres pages routées passent par un hook `lib/*.ts`
qui tape le backend. Ici, zéro appel, zéro service, zéro router — 4 fichiers de
composants + 1 fichier de constantes, rien côté Python.

Créer `backend/routers/qara.py` aurait été cohérent avec la convention du projet
(les 13 routers passent tous par un service) mais **overkill** : les chiffres ne
recoupent aucune base et ne changent qu'à l'émission d'une nouvelle version du
document. Le seul précédent applicable était `FEATURE_NAMES` dans
`combined-data.ts` — une constante figée maintenue à la main. C'est ce régime
qui a été retenu.

## Règle non négociable : recopier, jamais dériver

Toute valeur affichée doit exister **telle quelle** dans le document. Piège
rencontré et corrigé en cours de route : j'avais reconstitué un numérateur
`hits = round(accuracy/100 * n)` pour afficher une fraction sur les barres CUP.
Doublement fautif — le §5 de CUP ne publie **que** des pourcentages, et le calcul
serait parti d'effectifs eux-mêmes erronés. `BarRow.hits` est donc optionnel et
la colonne reste vide quand le document ne donne pas de fraction.

Corollaire : pas de résumé calculé non plus. « 7/9 groupes à 100 % de
concordance » avait été proposé en maquette puis retiré — ce comptage n'est pas
dans le document.

## Anglais mot pour mot, et le piège du `uppercase`

Choix Boris : libellés en anglais strict, numérotation des sections conservée
(« 2.1. Specificity (healthy cohort) »), pour qu'un auditeur retrouve la chaîne
exacte. Conséquence non évidente : **aucune classe `uppercase` sur les en-têtes
de colonne**. La convention visuelle du projet (`TablesView.tsx`) les met en
capitales, ce qui réécrivait `CV (mVAF v1.4)` en `CV (MVAF V1.4)` et `n` en `N`.
D'où le composant `ColLabel` dédié, sans `uppercase`.

Autre conséquence : la phrase « Per-indication sensitivity is provided **below** »
doit précéder la liste qu'elle annonce, sinon elle devient fausse.

## La divergence du document CUP — démontrée, pas supposée

Les tableaux §4 et §5 donnent `n = 94` pour la strate medium et `n = 95` pour la
high. La phrase de conclusion du §5 **et** la figure donnent l'inverse.

```
                    medium    high
tableau §4            94       95      (+ libellés (ii)/(iii) inversés)
tableau §5            94       95
phrase §5             95       94
figure                95       94   ← recomptée cellule par cellule
```

Preuve arithmétique : les matrices somment à 95 / 95 / 94 (total 284), et les
pourcentages publiés ne sont reproductibles qu'avec ces effectifs —
45/95 = 47,4 % et 85/94 = 90,4 %. Avec les effectifs des tableaux, aucun
numérateur entier ne tombe juste (45/94 = 47,9 % ; 85/95 = 89,5 % ;
86/95 = 90,5 %).

**Décision Boris : verbatim + encart de constat.** Les tableaux sont rendus sans
correction, un appel de note `*` sur la colonne `n` renvoie à l'encart
(`CUP_N_DIVERGENCE`). Ne pas « réparer » ces valeurs dans `qara-data.ts` — ce
serait une correction éditoriale d'un document réglementaire.

## Matrices de confusion

Transcrites d'une image fournie par Boris (l'API Docs ne rend que le texte).
5 classes : Lung, Colon, Prostate, Bladder+Pancreas, Breast. `counts[vraie][prédite]`.
Transcription **vérifiée par script** : les 3 matrices reproduisent exactement
les accuracies *et* les balanced accuracies publiées, et les rappels par ligne
correspondent aux pourcentages de la figure. Refaire tourner ce contrôle si les
matrices sont un jour mises à jour.

## Forme visuelle : un tableau unique, pas deux systèmes

Trois itérations ont été nécessaires, chacune sur retour de Boris :
1. Waffle de 224 points + barres animées → jugé « stylé graphique inutile ».
   350 px pour dire 213/224, alors que 95 % et 100 % sont indiscernables sur un
   waffle. Supprimé, comme les barres de CV (échelle calée sur 173 %, trompeuse)
   et l'animation de croissance.
2. Grille CSS à colonnes fixes → vide entre libellé et barre, barres de 72 px.
3. **Tableau avec colonne barre** (`QaraTable` / `TdBar` / `TdDualBar` dans
   `pages/qara/shared.tsx`) — forme finale, partagée par les 3 onglets. La barre
   est la colonne `w-full` qui absorbe l'espace ; `TdLabel` porte
   `whitespace-nowrap`, sans quoi la colonne barre comprime le libellé jusqu'à le
   casser sur 4 lignes.

Barres à deux segments (`TdDualBar`) réservées à Themelio, où le document
exprime réellement `Detection + Suspicious = Global` (§6.2, §6.3, §8.1). Les
couleurs viennent de `DETECTION_COLOR` / `SUSPICIOUS_COLOR`, partagées avec la
légende — une première version colorait ces barres sur l'échelle `pctColor`, ce
qui les rendait rouges alors que la légende les annonçait violettes.

## Accès en lecture au Google Doc

Via l'API REST + credentials gspread, jamais le navigateur — voir
[[google_docs_api_read_access]] et [[feedback_docs_readonly_and_brevity]].

Voir aussi : [[exis_alignment]] (le 0,0042 vient du même rapport Exis 1.1),
[[reproductibilite_seuil_exis]], [[qara_tower_skill]] (traçabilité temporelle,
qui mesure la Tower ; cette page, elle, ne fait que refléter le document).
