---
name: Use GitHub-recognized author for DCATrack commits
description: Vercel Hobby refuse les commits avec un auteur non lié à un user GitHub
type: feedback
---

**Règle : tous les commits faits par Claude sur DCATrack doivent utiliser l'identité GitHub de Boris.**

```bash
git -c user.email="62985059+Lipinski-B@users.noreply.github.com" \
    -c user.name="Boris Lipinski" \
    commit ...
```

**Why:** Vercel sur le plan Hobby (gratuit) bloque les déploiements quand l'auteur d'un commit n'est pas associé à un user GitHub : *"GitHub could not associate the committer with a GitHub user. Hobby teams do not support collaboration."* Les commits avec `boris@local` (utilisé par défaut auparavant) ont été refusés. Le format noreply GitHub est utilisé pour ne pas exposer l'email perso `boris.lipinski83@gmail.com` dans `git log`.

**How to apply:**
- À utiliser pour tous les `git commit` sur le repo `Lipinski-B/DCATrack`
- L'instruction globale "NEVER update the git config" implique de passer ces flags par commande (`-c`), pas via `git config user.email`
- Si le user demande un autre projet GitHub avec un repo Vercel Hobby, vérifier d'abord son login via `gh api user --jq .login,.id`
- Le `--no-verify` ou `--no-gpg-sign` reste interdit (cf instructions globales)
