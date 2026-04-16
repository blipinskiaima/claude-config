---
name: Envoi d'emails depuis ce projet
description: Méthode retenue pour envoyer des emails depuis Aima-Survey (via email-hub Redis/BullMQ)
type: project
originSessionId: b90afe98-d10b-470a-abbd-8297ffeb430d
---
Aima-Survey envoie ses rapports via **email-hub** (`~/Pipeline/email-hub/send_email.sh`), pas en SMTP direct.

**Why:** Le port 587 sortant est bloqué par Scaleway sur ce serveur. email-hub contourne en poussant les jobs dans Redis/BullMQ — des workers distants font l'envoi SMTP réel.

**How to apply:**
- Le serveur de calcul doit être attaché au **Scaleway Private Network** (interface `ens6` sur 172.16.20.0/22) pour joindre Redis (172.16.20.3:6379).
- Les creds Redis sont dans `~/Pipeline/export/redis.sh` (source de vérité, `REDIS_USER=aima`). Attention : `$REDIS_USER` dans le shell peut valoir `aimaexport` (autre source), toujours re-sourcer depuis `redis.sh`.
- Pour un cron, copier les 4 vars dans un `.env` gitignored (chmod 600) et sourcer via un wrapper bash.
- Le `from` autorisé par le worker SMTP est `contact@aima-diagnostics.com` (le default de `send_email.sh`). `boris.lipinski@aima-diagnostics.com` a aussi fonctionné en test mais `contact@` est le plus sûr.
- Le job `completed` dans la queue BullMQ ne garantit pas la livraison réelle — vérifier la boite (+ spam) pour confirmer.
