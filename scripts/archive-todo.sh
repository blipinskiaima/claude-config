#!/usr/bin/env bash
# Archive mensuel de la todo list.
#
# Extrait de `todo-optimisation.md` toutes les entrees Partie 2 plus vieilles
# que 30 jours et les deplace dans `todo-optimisation-archive-YYYY-MM.md`.
# Le fichier principal ne garde que le mois en cours + les 30 derniers jours.
#
# Usage :
#   ~/.claude/scripts/archive-todo.sh [--dry-run]
#
# Lance-le quand le fichier principal depasse ~2000 lignes ou mensuellement
# en cron si tu veux automatiser.

set -euo pipefail

TODO_DIR="$HOME/.claude/projects/-home-blipinski/memory"
TODO_FILE="$TODO_DIR/todo-optimisation.md"
DRY_RUN=false

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

if [[ ! -f "$TODO_FILE" ]]; then
    echo "ERROR: $TODO_FILE introuvable"
    exit 1
fi

CUTOFF=$(date -d "30 days ago" +%Y-%m-%d)
echo "Cutoff : entrees anterieures a $CUTOFF seront archivees"

# Extraire les sections datees de Partie 2
python3 <<PYEOF
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

todo_file = Path("$TODO_FILE")
cutoff = datetime.now() - timedelta(days=30)
content = todo_file.read_text(encoding="utf-8")

# Split on "## YYYY-MM-DD" headers in Partie 2
lines = content.splitlines(keepends=True)
out_main = []
archived_by_month = {}  # 'YYYY-MM' -> list of lines

in_partie2 = False
current_bucket = None
current_section = []
section_header_re = re.compile(r"^## (\d{4})-(\d{2})-(\d{2})")
partie3_re = re.compile(r"^# Partie 3")

def flush_section():
    global current_section, current_bucket
    if not current_section:
        return
    if current_bucket is None:
        out_main.extend(current_section)
    else:
        archived_by_month.setdefault(current_bucket, []).extend(current_section)
    current_section = []

for line in lines:
    if line.startswith("# Partie 2"):
        in_partie2 = True
        out_main.append(line)
        continue
    if partie3_re.match(line):
        flush_section()
        in_partie2 = False
        out_main.append(line)
        continue

    if in_partie2:
        m = section_header_re.match(line)
        if m:
            flush_section()
            y, mo, d = m.groups()
            section_date = datetime(int(y), int(mo), int(d))
            if section_date < cutoff:
                current_bucket = f"{y}-{mo}"
            else:
                current_bucket = None
            current_section = [line]
        else:
            current_section.append(line)
    else:
        out_main.append(line)

flush_section()

if not archived_by_month:
    print("Rien a archiver.")
    sys.exit(0)

print(f"A archiver : {sum(len(v) for v in archived_by_month.values())} lignes dans {len(archived_by_month)} mois")
for month, content_lines in archived_by_month.items():
    archive_path = todo_file.parent / f"todo-optimisation-archive-{month}.md"
    existing = archive_path.read_text(encoding="utf-8") if archive_path.exists() else f"# Archive todo — {month}\n\n"
    new_content = existing + "".join(content_lines)
    print(f"  -> {archive_path.name} ({len(content_lines)} lignes)")
    if not $DRY_RUN:
        archive_path.write_text(new_content, encoding="utf-8")

if not $DRY_RUN:
    todo_file.write_text("".join(out_main), encoding="utf-8")
    print("Fichier principal nettoye.")
else:
    print("DRY RUN — aucun fichier modifie.")
PYEOF

if ! $DRY_RUN; then
    echo ""
    echo "N'oublie pas de commit + push pour persister :"
    echo "  cd ~/.claude && git add projects/-home-blipinski/memory/todo-optimisation*.md && git commit -m 'archive: rotate old todo entries' && git push"
fi
