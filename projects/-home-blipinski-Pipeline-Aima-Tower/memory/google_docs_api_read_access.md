---
name: google-docs-api-read-access
description: "Comment lire (GET, jamais écrire) un Google Doc du repo Aima-Tower, y compris ses onglets internes — via l'API Docs REST + credentials OAuth gspread existants, pas de browser automation."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0e4d3284-268d-48ce-a44a-c347ecc2ad51
  modified: 2026-08-21T16:48:23.286Z
---

Pour lire le contenu d'un Google Doc (lecture seule, sans risque d'édition), réutiliser
le pattern d'authentification déjà en place pour le skill [[qara_tower_skill]], **pas**
claude-in-chrome — plus fiable (pas de clic accidentel dans un doc ouvert en mode Édition)
et ne dépend pas d'un Chrome connecté au bon compte.

## Credentials

`~/.config/gspread/authorized_user.json` — OAuth user token (refresh_token, client_id/secret,
scopes `spreadsheets` + `drive`). Le scope `drive` suffit pour l'API Docs (Docs est un type
de fichier Drive). Pattern d'obtention du Bearer token, copié de
`Aima-Tower/.claude/skills/qara-tower/scripts/append_gdoc.py::_token()` :

```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

creds = Credentials.from_authorized_user_file(str(GSPREAD_CREDS))
if not creds.valid:
    creds.refresh(Request())
tok = creds.token
```

## Lecture (GET, jamais batchUpdate)

```
GET https://docs.googleapis.com/v1/documents/{doc_id}?includeTabsContent=true
Authorization: Bearer {tok}
```

Sans `includeTabsContent=true`, seul le contenu du premier onglet (`document.body`) est
retourné. Un doc à onglets multiples (comme `Aima_QARA`, ID `1MBMc_q6NXQcKlFZWPk3sngqcyO3NJVDokm6Epyv-dAY`)
expose sa structure réelle dans `document.tabs[]` (récursif via `childTabs`).

⚠ **Piège vérifié** : `tabProperties.tabId` renvoyé par l'API porte déjà le préfixe `t.`
(ex. `t.rl2p0d594m89`) — c'est la même valeur que celle dans l'URL `?tab=t.xxx` du navigateur,
**ne pas la stripper** avant comparaison (erreur faite une première fois, corrigée).

Texte d'un onglet : `tab["documentTab"]["body"]["content"]`, parcourir
`paragraph.elements[].textRun.content` (+ `table.tableRows[].tableCells[]` pour les tableaux).

Script réutilisable : `read_gdoc_tab.py` dans le scratchpad de session — à recopier si besoin
(pas commité, écrit à la volée le 2026-08-21).

## Why

Boris a explicitement redirigé une tentative de lecture via claude-in-chrome (navigate +
screenshot dans un Google Doc ouvert en mode Édition — risque réel de clic accidentel malgré
prudence) vers ce pattern existant. Le doc visé était `1MBMc_q6NXQcKlFZWPk3sngqcyO3NJVDokm6Epyv-dAY`
("Aima_QARA"), onglet `SD-02: Exis 1.1` — la description technique complète du score Exis v1.1
(seuil 0,0042, formule bootstrap 200 réplicats, règles d'affichage TF longitudinal).

## How to apply

Avant tout accès à un Google Doc/Sheet dans ce repo, vérifier d'abord s'il existe déjà un
script du skill `/qara-tower` (ou un autre skill AIMA) qui parle à l'API — c'est le cas pour
QARA (`append_gdoc.py`) et pour Survey (gsheet fixe mentionnée dans `feature_sample_detail.md`).
Étendre ces scripts en lecture plutôt que d'ouvrir Chrome. Voir aussi [[feedback_check_existing_access_patterns]].
