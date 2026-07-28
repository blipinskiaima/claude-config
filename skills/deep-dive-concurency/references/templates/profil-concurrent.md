# Template — Profil concurrent structuré

Fiche produite par la **Partie 2** du deep-dive. C'est le **miroir du profil AIMA**
(`concurency/AIMA-POSITIONING.md`) : mêmes axes, même ordre → la Partie 3 compare axe par axe.

- **Emplacement** : `~/Pipeline/Aima-Survey/concurency/competitors/{NOM}-PROFIL.md`
- **Statut** : fiche vivante, remise à jour à chaque nouvelle analyse de la cible (comme le
  profil AIMA). Les rapports `{NOM}-P1-TECHNIQUE.md` / `{NOM}-P2-MARCHE.md` en **dérivent** en
  Partie 3 (rendu narratif pour deux publics) ; le `competitors.json` en reçoit le résumé.
- **Discipline** : chaque chiffre porte **deux marqueurs** — le niveau de preuve
  ([../quality/niveaux-preuve.md](../quality/niveaux-preuve.md)) **et** le verdict de fact-check
  de la phase 4. Un chiffre sans les deux n'entre pas dans la fiche.

Copier le squelette ci-dessous, remplacer les `{...}`, retirer les axes sans objet en les
marquant `[NON VÉRIFIÉ]` plutôt qu'en les supprimant.

---

```markdown
# Profil concurrent — {NOM} / {PRODUIT}

> Fiche structurée (Partie 2 du /deep-dive-concurency), miroir du profil AIMA.
> Rapports narratifs dérivés : {NOM}-P1-TECHNIQUE.md · {NOM}-P2-MARCHE.md.
> Dernière MAJ : {YYYY-MM-DD} · Sources principales : {rapport / PMID / plaquette}.
>
> Double marquage de chaque chiffre :
> preuve — [MESURÉ] observé · [PONDÉRÉ] repondéré · [MARKETING] sans publi · [PRÉPRINT] · [NON VÉRIFIÉ]
> fact-check (phase 4) — ✅ CONFIRMÉ · ❌ INEXACT · ⚠ TROMPEUR · ❔ NON VÉRIFIABLE

## 0. Cadrage
- **Ligne AIMA opposée** : MRD (vs mVAF v1.4) / MCED (vs THEMELIO) / triage / **aucune** (repère techno)
- **Tier** competitors.json : 1 direct · 2 adjacent · 3 émergent
- **Fiche competitors.json** : présente ? champs à mettre à jour
- **Déjà en veille** : PMID captés dans aima_survey.duckdb / angles morts

## 1. Ligne visée & maturité
- Indication réelle du produit (dépistage / MRD / triage / TOO)
- **Maturité réglementaire** : R&D · LDT-CLIA · Breakthrough (≠ approbation) · PMA · CE-IVD · IVDR
- ⚠ Comparer au **stade équivalent** de trajectoire AIMA, pas au produit commercial si AIMA est en R&D

## 2. Plateforme & wet lab
| Axe | Valeur |
|---|---|
| Tube / stabilité / délai prélèvement→traitement | |
| Extraction / input cfDNA | |
| Kit de librairie · conversion (bisulfite / enzymatique / affinité / **native**) | |
| Séquenceur · chimie · amplification | |
| Couverture / profondeur | |
| Lots · insu (blinding) du protocole d'éval | |
| Turnaround time tube→résultat | |

## 3. Signaux mesurés
| Modalité | Présent ? | Détail (résolution, empreinte génomique) |
|---|---|---|
| Méthylation (5mC / 5hmC) | | par base / scalaire · genome-wide / ciblé (Mb) · conversion ? |
| Fragmentomique | | genome-wide / limitée à la cible |
| CNV / fraction tumorale | | |
| Mutations | | |
→ **Combien de signaux, sur la même molécule ?** (le vrai axe vs AIMA : genome-wide, par base, 5hmC, CNV)

## 4. Score / modèle & seuil
- Famille de modèle · features en entrée · **combiné avec clinique/imagerie ?** (piège n°3)
- **Seuil de décision** et sur quoi il est fixé
- Sortie : binaire (Elevated/Not) vs catégories vs TOO

## 5. Performances — les trois niveaux
⚠ Ne jamais confondre. Toujours : n, sensibilité, **spécificité**, IC.

### 5.A Observé `[MESURÉ]`
| Unité | n | Sensi | Spéc | IC | fact-check |
|---|---|---|---|---|---|
| Global | | | | | |
| Par stade | | | | | ⚠ effectifs < 30 : ne pas comparer |

### 5.B Repondéré `[PONDÉRÉ]` — sur quelle population de référence ?
### 5.C Validation croisée — ⚠ **ne jamais citer comme performance**
### 5.D Marketing `[MARKETING]` — écart avec le publié ?

## 6. Verrous AIMA — grille de cross-check
Pour chaque verrou du profil AIMA §7 : le concurrent le **subit / contourne / résout** ?
| Verrou AIMA | subit / contourne / résout | preuve |
|---|---|---|
| Méthylation genome-wide à faible profondeur | | |
| Bornes fragments transposables ONT | | |
| Classifieur verrouillé | | |
| 5hmC natif sans conversion | | |

## 7. Marché & réglementaire
- **Commercial** : disponibilité, géographies, prix, volumes, partenariats
- **Réglementaire** : statut réel — distinguer désignation (Breakthrough) d'approbation (PMA)
- **Remboursement** : Medicare, CPT/PLA, MolDX, couverture
- **Financement / gouvernance** : levées (montant, date), dirigeants, effectifs, signaux de tension
- **Essais cliniques** : ClinicalTrials.gov — statut, taille, échéance à surveiller
- **Controverse** : lettres critiques, éditoriaux, position des sociétés savantes

## 8. Incertitudes / non vérifié
Liste numérotée des `[NON VÉRIFIÉ]` assumés — à afficher, pas à combler.

## 9. Corpus
| Rôle | PMID | Journal / année | Cohorte | Note |
|---|---|---|---|---|
| ★ Validation clinique (= le produit) | | | | |
| Fondateur | | | | |
| Application | | | | |

## Journal de mise à jour
- **{YYYY-MM-DD}** : {ce qui a changé, source}
```
