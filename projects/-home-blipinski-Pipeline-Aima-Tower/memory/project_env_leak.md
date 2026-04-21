---
name: .env tracked dans git (incident securite)
description: Le fichier .env du projet Aima-Tower a ete tracked dans git jusqu'au 2026-04-21, exposant des secrets API dans l'historique de github.com/aima-dx/Aima-Tower
type: project
originSessionId: dd59e579-178a-49ff-927b-0be837436a89
---
# Incident : .env tracked dans git

Decouvert le **2026-04-21** lors de la mise en place HTTPS + basic auth.

Le fichier `.env` du projet Aima-Tower etait **tracked dans git** (present dans les commits `e1d74dd`, `e798561`, `751d962`), exposant les secrets suivants dans l'historique pushe sur `github.com/aima-dx/Aima-Tower` :

- `ANTHROPIC_API_KEY=sk-ant-api03-A4cUfVwc...` (API Claude)
- `accessToken=eyJ0aWQi...` (Seqera Platform token)

**Why** : Probablement commite par erreur dans les premiers commits, .gitignore ajoute apres. Les commits suivants ont continue a suivre le fichier.

**How to apply** (si Boris mentionne le projet Aima-Tower ou demande un setup similaire) :
1. **Verifier si `.env` est tracked** avant d'ajouter de nouveaux secrets : `git ls-files --error-unmatch .env`
2. **Si tracked** : `git rm --cached .env` + confirmer que `.gitignore` le protege
3. **Rotation des secrets exposes** : Anthropic (console.anthropic.com > API Keys) + Seqera (cloud.seqera.io > Tokens)
4. **Purge historique optionnelle** : `git filter-repo --path .env --invert-paths` + force push (destructif, a valider avec l'equipe)

**Pattern pour nouveaux projets** : ajouter `.env` au `.gitignore` **avant** le premier commit, utiliser `.env.example` comme template committe.

Etat au 2026-04-21 :
- Repo `aima-dx/Aima-Tower` est **prive** et Boris est **seul developpeur** → exposition externe quasi nulle
- Niveau 1 execute (`.env` retire du tracking, ajoute a `.env.example` + `.gitignore`)
- **Niveau 2 (rotation secrets) reporte** — pas urgent vu repo prive + dev unique
- Niveau 3 (purge historique) non decide

**Si Boris demande plus tard la rotation** : guider revocation Anthropic + Seqera puis mise a jour `.env` local.
