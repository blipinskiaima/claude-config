---
name: Approche pragmatique de la securisation
description: Boris prefere scope discipline et iteration sur la securite (une couche a la fois, eviter le blast radius) plutot qu'un durcissement complet en une fois
type: feedback
originSessionId: dd59e579-178a-49ff-927b-0be837436a89
---
# Approche pragmatique de la securisation

Quand Boris demande une securisation, privilegier **l'iteration par couches** plutot que le durcissement complet en une passe.

**Why** : Confirme le 2026-04-21 lors de la mise en place HTTPS + basic auth. Boris a valide explicitement "on fait Caddy d'abord, Security Group plus tard". Raisons :
- Scope discipline (une chose a la fois)
- Blast radius : un Security Group mal configure peut bloquer SSH sur une VM Scaleway
- Caddy resout 95% du risque immediat (HTTPS + auth + port ferme cote Docker)
- Les couches defensives additionnelles peuvent s'ajouter sans refactor

**How to apply** :
- Pour une task de securisation, proposer **un plan a plusieurs niveaux** avec la couche critique en premier
- Signaler les ameliorations restantes comme optionnelles ("a faire plus tard" explicitement)
- Eviter de modifier le firewall/network en meme temps qu'on touche a l'auth — risque de cumul de pannes
- Toujours presenter les tradeoffs "rapide vs robuste" et laisser Boris choisir le curseur

**Exemple applique** :
- Niveau 1 : Caddy HTTPS + basic auth + port 8050 ferme ← priorite immediate
- Niveau 2 : Security Group Scaleway restrictif ← optionnel, plus tard
- Niveau 3 : MFA / OIDC ← quand besoin grandit
