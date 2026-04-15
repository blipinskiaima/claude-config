#!/usr/bin/env bash
# Hook Stop : commit + push automatique des memories et rules si elles ont change.
# Silencieux : n'affiche rien a l'utilisateur, s'execute en fond.
#
# Scope (whitelist explicite pour eviter de commit les cache/temp files) :
#   - projects/**/memory/*.md           (todo, profils, memoire auto)
#   - rules/*.md                        (golden rules)
#   - scripts/*.sh                      (scripts utilitaires)
#   - CLAUDE.md                         (instructions globales)

set -u
cd "$HOME/.claude" || exit 0

WHITELIST=(
    "projects/-home-blipinski/memory"
    "rules"
    "scripts"
    "CLAUDE.md"
)

# Ne rien faire si aucun changement dans la whitelist
CHANGED=0
for path in "${WHITELIST[@]}"; do
    if git status --porcelain "$path" 2>/dev/null | grep -q '.'; then
        CHANGED=1
        break
    fi
done

[[ $CHANGED -eq 0 ]] && exit 0

# Stage les fichiers whitelist uniquement
for path in "${WHITELIST[@]}"; do
    git add "$path" 2>/dev/null || true
done

# Bail out si rien d'effectivement stage (cas des fichiers gitignore)
git diff --cached --quiet && exit 0

TS=$(date +"%Y-%m-%d %H:%M")
git commit -m "auto: session end snapshot $TS" --quiet 2>/dev/null || exit 0

# Push en fond, timeout 15s pour eviter de bloquer si le reseau part
timeout 15 git push origin HEAD --quiet 2>/dev/null || true

exit 0
