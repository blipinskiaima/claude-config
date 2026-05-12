---
name: Rebasecalled POD5 columns — ne pas propager
description: Pour les samples *_rebasecalled*, laisser taille_pod5/nb_pod5/pod5_completude à NULL après update-column stockage_pod5 — ne pas copier depuis l'original
type: feedback
originSessionId: e32b47d7-d244-48cd-b5b3-aec585cf8f89
---
Après un `update-column stockage_pod5 {type} {labo}`, les samples rebasecalled retombent à NULL sur `stockage_pod5`, `sample_type_pod5`, `taille_pod5`, `pod5_adresse`, `nb_pod5`, `pod5_completude` (la fonction `_update_pod5_storage()` ne propage pas depuis l'original).

**Comportement attendu** : les laisser à NULL. Ne pas proposer/exécuter de UPDATE SQL pour copier les valeurs depuis le sample d'origine.

**Why:** Confirmé par Boris le 2026-05-11 après update HCL liquid (471 samples, dont 81 rebasecalled retombés NULL). Les rebasecalled n'ont pas de POD5 propre — la valeur "héritée" n'apporte pas d'info utile, et NULL est plus honnête.

**How to apply:** Quand un `update-column stockage_pod5` (ou colonnes POD5 dérivées) wipe les rebasecalled, ne pas proposer de repropagation. Mentionner le compte de rebasecalled à NULL comme info, mais ne pas y toucher. Contredit l'ancienne note MEMORY.md "HCL rebasecalled POD5 columns also copied from original" — cette propagation manuelle n'est plus souhaitée.
