---
name: feedback-check-existing-access-patterns
description: "Avant d'utiliser claude-in-chrome pour accéder à un service authentifié (Google Docs/Sheets...), vérifier d'abord si un skill du repo a déjà un pattern d'accès API + credentials."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0e4d3284-268d-48ce-a44a-c347ecc2ad51
  modified: 2026-08-21T16:48:32.694Z
---

Boris a interrompu une tentative de lecture d'un Google Doc via claude-in-chrome (navigate +
screenshot) pour demander de regarder comment le skill `/qara-tower` accède déjà aux docs.
Réponse : `scripts/append_gdoc.py` a un pattern OAuth complet (`~/.config/gspread/authorized_user.json`
+ API REST `docs.googleapis.com`). Voir [[google_docs_api_read_access]] pour le détail technique.

**Why:** le browser automation sur un Google Doc ouvert en mode Édition comporte un risque réel
de clic accidentel qui modifie le contenu, même en faisant attention (le curseur peut déjà être
positionné dans le texte au chargement). Un GET API est intrinsèquement sans risque d'écriture,
plus rapide, et ne dépend pas d'avoir Chrome connecté au bon compte Google. Plusieurs projets
AIMA ont déjà des credentials Google (gspread) configurés pour d'autres usages (Sheets Survey,
Doc QARA) — ce sont des ressources à chercher en premier.

**How to apply:** avant de lancer claude-in-chrome pour lire/interagir avec un service
authentifié (Google Docs, Sheets, Drive...), grep le repo courant (et les skills globaux
`~/.claude/skills/`) pour un script existant qui parle déjà à ce service via API. N'utiliser
le navigateur qu'en dernier recours, quand aucun pattern API n'existe.
