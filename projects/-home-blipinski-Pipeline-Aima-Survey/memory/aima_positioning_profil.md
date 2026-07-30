---
name: aima-positioning-profil
description: "Profil AIMA canonique (concurency/AIMA-POSITIONING.md), perfs Exis 1.1 figées vs recalcul Tower, nuance détection vs MRD"
metadata: 
  node_type: memory
  type: reference
  originSessionId: fdd4f2ac-8635-4303-a86c-70045baa73f3
  modified: 2026-07-28T13:54:12.459Z
---

`~/Pipeline/Aima-Survey/**concurency**/AIMA-POSITIONING.md` = **profil AIMA canonique**, base de
comparaison de tout `/deep-dive-concurency`. ⚠ Chemin changé le 2026-07-28 : tout le matériel
concurrentiel a migré de `docs/` vers `concurency/`.

**Chiffre Exis figé ≠ recalcul live de Tower** — piège corrigé le 2026-07-28 après extraction
directe du PDF SD-02 (`~/Pipeline/Aima-Tower/Exis 1.1.pdf`, 7 p., gelé au 2026-07-06) :

| | Exis 1.1 figé (à citer en externe) | recalcul Tower (dérive continue) |
|---|---|---|
| global avancés | **82,3 % (214/260)** | 82,0 % (214/261) |
| Prostate | 78,0 % (32/41) | 76,2 % (32/42) |
| actif sans mutation | 66,0 % (70/106) | 65,4 % (70/107) |

Cause : un échantillon Prostate est passé « cancer » le 2026-07-23, après le gel du rapport.
Spécificité **95,1 % (213/224)**, seuil mVAF v1.4 > 0,0042 % — identiques dans les deux.
Le « 82 % » porte sur **6 indications sélectionnées** ; sans ce carve-out, 76,2 % (301/395).

Deux référentiels à **NE JAMAIS mélanger** : mVAF v1.4 seul (Exis 1.1) vs combo THEMELIO
(90,5 % @ 96,2 %, n=190/53). ⚠ THEMELIO est calculé en **cross-validation out-of-fold sans
aucun test set held-out** (`train.R`, `NFOLD <- 5L`, `combined_score_type='cv_oof'`) — donc
non présentable comme une performance.

Voir [[aima-poumon-perfs-par-stade]], [[signatera-natera]], [[competitive_landscape]],
[[delfi_firstlook]].
