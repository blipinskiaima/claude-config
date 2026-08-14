---
name: feedback_gdoc_no_overwrite
description: "Ne JAMAIS reecrire une section entiere d'un Google Doc partage — remplacements de chaines exactes uniquement"
metadata: 
  node_type: memory
  type: feedback
  modified: 2026-08-14T14:34:09.632Z
  originSessionId: c23b78b9-f616-423e-90dd-4fb111a4cd59
---

Ne **jamais** supprimer puis reecrire une section entiere d'un Google Doc partage.
Uniquement des remplacements de **chaines exactes** (`replaceAllText`), qui echouent
proprement si le texte a bouge au lieu de l'ecraser.

**Why:** le 2026-08-14, j'ai lance un `deleteContentRange` sur toute la partie 6 de l'onglet
« Nb reads mapped » pour la reecrire. Boris venait de la reecrire lui-meme. Son travail a ete
**detruit et n'a pas pu etre recupere** : l'API Drive `revisions` ne conservait qu'une revision
de 12:55, ses modifications dataient de 12:56-13:00. Seul l'historique de l'UI Google Docs les
contenait encore.

Le signal etait **dans ma propre sortie** : `ancienne Partie 6 : 5152 caracteres a remplacer`
alors que j'avais ecrit 6118. Cet ecart de ~1000 caracteres etait son intervention. Je ne l'ai
pas relevé et j'ai supprime. Mon garde-fou verifiait que la partie etait bien le dernier titre
de niveau 2 — il ne verifiait pas que **le contenu n'avait pas change depuis**.

**How to apply:**
- **Texte** : `replaceAllText` avec `containsText` = la phrase entiere attendue. Si elle n'est
  plus la, l'operation renvoie 0 occurrence et ne casse rien. Ne jamais faire de remplacement
  mot a mot (faux positifs), toujours des phrases longues et uniques.
- **Image** : `deleteContentRange` sur les **2 index de l'image seule**, apres avoir verifie le
  contexte (titre qui precede ET titre qui suit). Le script s'arrete si le contexte differe.
- **Ajout** : append pur en fin d'onglet, jamais d'insertion au milieu.
- **Avant toute ecriture** : comparer la taille actuelle de la section a celle attendue. Tout
  ecart = quelqu'un est passe -> **s'arreter et demander**, ne pas ecraser.
- Un document partage peut etre edite **pendant** la session : une lecture faite il y a deux
  minutes n'est pas une garantie.

Corollaire verifie au passage : les **commentaires Google Docs survivent** a une suppression de
texte (23/23 intacts, 0 orphelin) — ce n'est pas ce qui est en jeu, c'est le texte redige.

Voir [[gdoc-qc-ratio-n50]] pour l'outillage d'acces au document.
