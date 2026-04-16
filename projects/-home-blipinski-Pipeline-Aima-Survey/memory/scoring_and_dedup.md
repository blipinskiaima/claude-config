---
name: Scoring IA et dédup cross-jours
description: Mécanisme de scoring Claude Haiku + cache SQLite + dédup qui empêche le spam email dans Aima-Survey
type: project
originSessionId: b90afe98-d10b-470a-abbd-8297ffeb430d
---
Aima-Survey embarque 2 caches SQLite dans `data/scoring_cache.db` :

**Table `scores`** — cache des scores IA par PMID (pour ne pas re-scorer un article vu 2 fois).
Colonnes : `pmid, score, why, tags, model, scored_at`.

**Table `sent_articles`** — liste des PMIDs déjà envoyés par email.
Colonnes : `pmid, first_sent_at`.

**Why:** Le cron daily tourne en `--days 7` (fenêtre glissante) pour rattraper les papiers indexés en retard par PubMed (`pdat` parfois mois-seul ou futur). Sans dédup, chaque article apparaitrait 7 jours d'affilée dans les emails. La dédup `sent_articles` garantit qu'un PMID n'est envoyé qu'une fois.

**How to apply:**
- Le filtre dédup ne s'applique QUE si `--email` est passé. Un run manuel `--report` sans `--email` montre tout.
- Les PMIDs sont marqués comme envoyés SEULEMENT si `send_email_via_hub` retourne True (pas de marquage si l'envoi échoue).
- Pour "reset" la dédup (ex: reforce un renvoi) : `DELETE FROM sent_articles WHERE pmid IN (...)`.
- Le scoring cache est orthogonal : il reste peuplé même si on reset le dédup (évite le coût API).
- Claude Haiku enveloppe parfois sa réponse en ```json ... ```. `scorer.py` strip le fence avant `json.loads`.
- Tri final des articles : priorité asc > score desc (None en dernier) > date desc.
