---
name: PEA display excludes CW8
description: Toujours exclure CW8 de tout affichage/suivi du PEA - la ligne reste détenue mais Boris ne veut pas la suivre
type: feedback
originSessionId: 317926e1-4c36-4716-a022-503b5b799f6e
---
**Règle : Toute référence au PEA doit ignorer la ligne CW8 (Amundi MSCI World, LU1681043599).**

**Why:** Boris ne souhaite pas suivre cette ligne dans ses tableaux/analyses (1 part, achetée juin 2023, conservée mais non pilotée). La ligne reste physiquement dans le PEA Fortuneo, elle n'est juste pas affichée ni intégrée aux totaux suivis.

**How to apply:**
- Commandes "tableau PEA", "état du PEA", "lis mon patrimoine" (section PEA), tout récap PEA → masquer CW8
- Calculs de poids/répartition PEA → calculer hors CW8
- Quand on rafraîchit les positions via Finary API, CW8 sera toujours présent dans la réponse — il faut le filtrer côté affichage
- Toujours mentionner discrètement que le total réel du PEA inclut CW8 (transparence) si l'écart est significatif, ou afficher "Total affiché (hors CW8)" + "Total PEA réel" en note
- Ne PAS supprimer CW8 de la mémoire (`project_pea_current.md`) — la ligne reste documentée comme détenue mais non suivie
- Si Boris demande explicitement "y compris CW8" ou "tout le PEA", inclure CW8

**Exception** : le tableau récap général (commande "tableau récap") n'est pas concerné — c'est une watchlist de marché, pas un suivi de positions PEA. CW8 y reste.
