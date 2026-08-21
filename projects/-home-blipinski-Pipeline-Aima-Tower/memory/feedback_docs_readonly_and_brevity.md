---
name: feedback-docs-readonly-and-brevity
description: "Règle absolue : ne jamais modifier un Google Doc/document externe, même par inadvertance. Réponses courtes et simples par défaut."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0e4d3284-268d-48ce-a44a-c347ecc2ad51
  modified: 2026-08-21T16:49:37.898Z
---

Deux consignes données ensemble le 2026-08-21, après lecture du doc `Aima_QARA` (onglet SD-02 Exis 1.1) :

1. **Ne jamais modifier un document externe, en aucun cas.** Lecture strictement read-only
   (GET API, jamais batchUpdate/insertText) — voir [[google_docs_api_read_access]]. S'applique
   même si une action semble mineure ou utile (corriger une coquille, etc.) : ne jamais le faire
   sans que Boris le demande explicitement pour CE document précis.
   **Why:** le doc lu était un document réglementaire QARA (SD-02) — une modification accidentelle
   aurait une conséquence de conformité, pas juste un désagrément.
2. **Réponses courtes et simples.** Renforce la consigne globale CLAUDE.md ("concret et
   synthétique"), donnée spécifiquement après une réponse jugée trop longue (synthèse détaillée
   du contenu Exis 1.1 avec sous-sections).

**How to apply:** pour toute lecture de document externe (Docs/Sheets/Drive), rester en API
GET pure. Pour toute réponse, préférer 3-5 lignes factuelles à une synthèse structurée à
sections/puces multiples, sauf si Boris demande explicitement le détail complet.
