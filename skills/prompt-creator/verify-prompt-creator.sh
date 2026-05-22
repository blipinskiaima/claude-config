#!/usr/bin/env bash
# verify-prompt-creator.sh — Tests RED pour le skill /prompt-creator
# Lance des vérifications grep et reporte PASS/FAIL.
# Usage : ./verify-prompt-creator.sh
# Exit code 0 = tous PASS, 1 = au moins un FAIL.

set -u
cd "$(dirname "$0")"

PASS=0
FAIL=0

check() {
    local desc="$1"
    local condition="$2"
    if eval "$condition" >/dev/null 2>&1; then
        echo "  PASS — $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL — $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== TEST 1 — Versions modèles à jour ==="
check "Opus 4.7 présent"        "grep -rq 'Opus 4.7' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Sonnet 4.6 présent"      "grep -rq 'Sonnet 4.6' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "GPT-5.5 présent"         "grep -rq 'GPT-5.5' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Gemini 3.x présent"      "grep -rq 'Gemini 3.x' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Pas de 'Claude 4.6)' sans 4.7"  "! grep -rq 'Claude 4.6)' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Pas de 'GPT-5.2)' isolé"        "! grep -rq 'GPT-5.2)' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Pas de 'Gemini 3)' isolé"       "! grep -rq 'Gemini 3)' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"

echo ""
echo "=== TEST 2 — Paramètres API actuels ==="
check "'adaptive' présent"      "grep -rqi 'adaptive' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "'effort' présent"        "grep -rq 'effort' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "'verbosity' présent"     "grep -rq 'verbosity' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "'developer message' présent"  "grep -rqi 'developer message' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "'budget_tokens' uniquement en déprécié"  "! grep -rq 'budget_tokens' --include='*.md' --exclude-dir='specs' --exclude-dir='plans' || grep -rA3 'budget_tokens' --include='*.md' --exclude-dir='specs' --exclude-dir='plans' | grep -qiE 'déprécié|deprecated'"

echo ""
echo "=== TEST 3 — Anti-patterns confirmés présents ==="
check "string matching downstream"  "grep -rqi 'string matching' references/anti-patterns.md"
check "expert in X (PRISM)"     "grep -rqi 'expert in X' references/anti-patterns.md"
check "MUST use (en softening)"  "grep -rq 'MUST use' references/anti-patterns.md"
check "Sur-emphasis CAPS"       "grep -rqiE 'sur-emphasis|overtrigger' references/anti-patterns.md"

echo ""
echo "=== TEST 4 — Zéro claim infirmé ==="
check "Pas de '+15-20%'"        "! grep -rqE '15-20%|\\+15' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Pas de 'PTCF'"            "! grep -rq 'PTCF' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Pas de '×17 / 17x / 17.2'"  "! grep -rqE '×17|17x|17\\.2' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"
check "Pas de '76%' (claim infirmé)"  "! grep -rq '76%' --include='*.md' --exclude-dir='specs' --exclude-dir='plans'"

echo ""
echo "=== BILAN ==="
TOTAL=$((PASS + FAIL))
echo "  PASS: $PASS / $TOTAL"
echo "  FAIL: $FAIL / $TOTAL"

if [ "$FAIL" -eq 0 ]; then
    echo ""
    echo "  OK — Tous les tests passent. Skill /prompt-creator vérifié."
    exit 0
else
    echo ""
    echo "  KO — Échecs détectés. Investiguer les FAIL ci-dessus."
    exit 1
fi
