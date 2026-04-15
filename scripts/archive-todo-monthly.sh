#!/usr/bin/env bash
# Cron mensuel : archive les entrees Partie 2 > 30 jours + commit + push.
# Lance par cron le 1er de chaque mois a 09h00.
#
# Crontab :
#   0 9 1 * * $HOME/.claude/scripts/archive-todo-monthly.sh

set -u
cd "$HOME/.claude" || exit 0

# Lance l'archivage (archive-todo.sh ecrit les fichiers mais ne commit pas)
bash "$HOME/.claude/scripts/archive-todo.sh" > /tmp/archive-todo.log 2>&1 || exit 0

# Commit + push si quelque chose a ete modifie
if git status --porcelain projects/-home-blipinski/memory/ | grep -q '.'; then
    git add projects/-home-blipinski/memory/todo-optimisation*.md
    TS=$(date +"%Y-%m")
    git commit -m "archive: rotate todo entries for $TS" --quiet 2>/dev/null || exit 0
    timeout 15 git push origin HEAD --quiet 2>/dev/null || true
fi

exit 0
