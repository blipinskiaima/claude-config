---
name: Security setup Tower (Caddy + HTTPS + basic auth)
description: Architecture de securisation de l'app Tower en prod via reverse proxy Caddy avec TLS Let's Encrypt et basic auth bcrypt (deployee 2026-04-21)
type: project
originSessionId: dd59e579-178a-49ff-927b-0be837436a89
---
# Securisation Aima-Tower (2026-04-21)

## Architecture

```
Internet ──HTTPS:443── Caddy (aima-tower-caddy) ──HTTP:8050── Dash (aima-tower-dashboard)
                       ├─ TLS Let's Encrypt auto-renewal
                       ├─ basic_auth bcrypt cost=14
                       └─ encode gzip + HTTP/2 + HTTP/3
```

- **URL prod** : `https://tower.aima-diagnostics.com`
- **Username** : `aima`
- **Password** : stocke en **clair dans le gestionnaire de mdp AIMA** (Bitwarden/1Password). Jamais commite. Infra ne voit que le hash bcrypt.
- **Port 8050** : plus expose a Internet (`expose:` Docker, pas `ports:`)

## Fichiers cles

- `docker-compose.yml` : service `caddy` avec volumes `caddy_data`/`caddy_config` persistants (cert LE), reseau partage `tower-network`, `depends_on: mini-tower`
- `Caddyfile` : 10 lignes, `basic_auth { aima {env.TOWER_BASICAUTH_HASH} }` puis `reverse_proxy mini-tower:8050`
- `src/app.py` : `SECRET_KEY=settings.flask_secret_key` (raise si manquant), `SESSION_COOKIE_SECURE=True`
- `src/config.py` : champ `flask_secret_key: str = ""`
- `.env` : `FLASK_SECRET_KEY` + `TOWER_BASICAUTH_HASH` (hash bcrypt entre guillemets simples pour proteger les `$`)

## Gotchas d'implementation

1. **Caddy v2.x** : `basicauth` est **deprecated** → utiliser `basic_auth` (avec underscore).
2. **Hash bcrypt dans .env** : les `$` du hash doivent etre **entre guillemets simples** (`'$2a$14$...'`) pour que docker-compose ne tente pas de les interpoler.
3. **Let's Encrypt challenge** : HTTP-01 a echoue avec "No such authorization" 404 (bug ACME transitoire). Caddy a automatiquement fallback sur **TLS-ALPN-01** (port 443) qui a marche. Pas besoin d'action manuelle.
4. **Cert persistant** : volume Docker `caddy_data:/data` critique, ne pas supprimer sinon nouveau challenge LE a chaque restart (rate limit a 5/semaine par domaine).
5. **`SESSION_COOKIE_SECURE=True` fonctionne avec Caddy** meme si Flask recoit du HTTP interne : le flag est applique cote navigateur qui lui voit du HTTPS.

## Proceder au changement de mot de passe

```bash
cd /home/blipinski/Pipeline/Aima-Tower
NEW_PW=$(openssl rand -base64 24 | tr -d '/+=' | head -c 20)
NEW_HASH=$(docker run --rm caddy:2-alpine caddy hash-password --plaintext "$NEW_PW")
sed -i "s|^TOWER_BASICAUTH_HASH=.*|TOWER_BASICAUTH_HASH='$NEW_HASH'|" .env
docker compose restart caddy
echo "Nouveau password : $NEW_PW"
```

## Ajouter un user

Dans `Caddyfile` : ajouter ligne `boris {env.TOWER_BASICAUTH_HASH_BORIS}` dans le bloc `basic_auth`. Ajouter `TOWER_BASICAUTH_HASH_BORIS` dans `.env` et dans `docker-compose.yml > caddy.environment`.

## Security Group Scaleway

**Non configure en restrictif** (par defaut permissif). Decide volontairement par Boris pour eviter blast radius sur SSH. A durcir plus tard : Allow 22/80/443 + Deny all.

## Test rapide

```bash
curl -I https://tower.aima-diagnostics.com                                      # 401
curl -I -u 'aima:PASSWORD' https://tower.aima-diagnostics.com                   # 200
curl -I --max-time 5 http://51.15.250.23:8050                                   # connection refused
curl -I http://tower.aima-diagnostics.com                                       # 308 redirect HTTPS
```
