---
name: feedback-bash-pipefail-sigpipe
description: "Pattern bash à éviter — toute pipe `cmd | head -N` ou `cmd | grep -q ...` avec set -o pipefail est buggy quand le consommateur de droite ferme stdin avant que la commande de gauche ait fini d'écrire"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 37da32d5-7cbd-4dc3-8643-5111d2fb4e16
---

**Règle** : ne JAMAIS utiliser `cmd1 | head -N` ou `cmd1 | grep -q PATTERN` dans un script bash avec `set -o pipefail` quand `cmd1` produit beaucoup d'output. Préférer une capture en variable + test pur bash, ou un fichier temp.

**Why:** Quand `head -N` ou `grep -q` ferme stdin (N lignes atteintes ou première match trouvée), `cmd1` reçoit SIGPIPE → exit 141. Avec `set -o pipefail`, l'exit code de la pipe entière devient 141. Le `|| true` est censé l'avaler en commande standalone, mais en command substitution `$(...)` le swallow n'est pas fiable : selon le timing, VAR peut être vide alors que la commande a bien produit du contenu. Bug reproduit le 2026-05-22 et 2026-05-25 dans `~/Pipeline/Dilution/scripts/generate_dilution.sh` sur **deux variantes du même pattern** :

1. **Check MM/ML** (commit `30ff946`) — `samtools view "$BAM" | head -1000` failait par intermittence avec "MM:Z absent" alors que les tags étaient présents (167 MM:Z dans les 1000 premiers reads vérifiés manuellement).
2. **Check @SQ header** (commit `e3c38cb`) — `samtools view -H "$BAM" | grep -q "^@SQ"` failait sur les 3 jobs `Breast_34 + Healthy_807` (les 3 BAMs étaient valides, count + MM/ML déjà passés au-dessus).

Avec hg38 (~25 @SQ lines), `grep -q` match immédiatement et ferme stdin → samtools fail systématiquement. Avec head -1000 sur un BAM de 12.5M reads, c'est aussi systématique mais paraît "intermittent" car samtools peut buffer différemment selon la load CPU.

**How to apply:**

Pattern KO #1 (head dans command substitution) :
```bash
HEAD_OUT=$(samtools view "$BAM" 2>/dev/null | head -1000 || true)
echo "$HEAD_OUT" | grep -q "MM:Z:" || exit 1
```

Pattern KO #2 (grep -q en pipe direct) :
```bash
samtools view -H "$BAM" | grep -q "^@SQ" || exit 1
```

Pattern OK #1 — fichier temp (pour head) :
```bash
TMP=$(mktemp)
samtools view "$BAM" 2>/dev/null | head -1000 > "$TMP" 2>/dev/null || true
grep -q "MM:Z:" "$TMP" || { rm -f "$TMP"; exit 1; }
rm -f "$TMP"
```

Pattern OK #2 — capture en variable + test pur bash (pour grep -q) :
```bash
HEADER=$(samtools view -H "$BAM" 2>/dev/null || true)
[[ "$HEADER" == *"@SQ"* ]] || { echo "FAIL"; exit 1; }
```

S'applique à TOUT script bash avec `set -o pipefail` qui pipe un producteur (BAM, gros fichier) vers un consommateur qui peut "early exit" (head, grep -q, awk avec exit, sed avec q). Alternative équivalente : `set +o pipefail` autour du bloc, mais les patterns OK ci-dessus sont plus lisibles.

Liens : [[project-phase1-state]] [[reference-bam2beta-integration]] [[feedback-manual-finish-pattern]]
