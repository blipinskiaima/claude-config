---
name: feedback-bash-pipefail-sigpipe
description: "Pattern bash à éviter — $(samtools view | head -1000 || true) avec set -o pipefail = bug intermittent, utiliser fichier temp"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37da32d5-7cbd-4dc3-8643-5111d2fb4e16
---

**Règle** : ne JAMAIS faire `VAR=$(cmd1 | head -N || true)` dans un script bash avec `set -o pipefail`. Préférer un fichier temp.

**Why:** Quand `head` ferme stdin après N lignes, `cmd1` reçoit SIGPIPE → exit 141. Avec `set -o pipefail`, l'exit code de la pipe entière devient 141. Le `|| true` est censé l'avaler, mais en command substitution `$(...)` le swallow n'est pas fiable : selon le timing, VAR peut être vide alors que la commande a bien produit du contenu. Bug reproduit le 2026-05-22 dans `scripts/generate_dilution.sh` — le check MM/ML failait par intermittence avec "MM:Z absent" alors que les tags étaient bien présents (167 MM:Z dans les 1000 premiers reads, vérifié manuellement).

**How to apply:**
- Pattern KO :
  ```bash
  HEAD_OUT=$(samtools view "$BAM" 2>/dev/null | head -1000 || true)
  echo "$HEAD_OUT" | grep -q "MM:Z:" || exit 1
  ```
- Pattern OK :
  ```bash
  TMP=$(mktemp)
  samtools view "$BAM" 2>/dev/null | head -1000 > "$TMP" 2>/dev/null || true
  grep -q "MM:Z:" "$TMP" || { rm -f "$TMP"; exit 1; }
  rm -f "$TMP"
  ```
- S'applique à TOUT script bash avec `set -o pipefail` qui utilise `head -N` pour capturer un sous-ensemble en variable.
- Alternative équivalente : `set +o pipefail` autour du bloc, mais le fichier temp est plus lisible.

Liens : [[project-phase1-state]] [[reference-bam2beta-integration]]
