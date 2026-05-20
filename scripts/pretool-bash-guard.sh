#!/usr/bin/env bash
# PreToolUse(Bash) hook — protections renforcées golden rules AIMA
#
# Bloque les commandes Bash qui violent les golden rules (~/.claude/rules/).
# Exit 2 = blocage avec message stderr renvoyé a Claude.
# Exit 0 = autorisation.
#
# Couvre :
#  1. S3 destructive (aws s3 rm/rb, sync --delete)
#  2. cd vers repertoire protege + rm dans la meme commande
#  3. Python interprete destructif (shutil.rmtree, os.unlink, os.remove, Path.unlink)
#  4. find -delete et find -exec rm
#  5. dd vers /dev/* (overwrite disque)
#  6. xargs rm sur paths proteges
#  7. Redirection > vers .pod5
#  8. shred/truncate/mkfs sur paths absolus protégés
#  9. nextflow run depuis ~/Pipeline/ (doit être lancé depuis ~/Run ou ~/Run2)

set -euo pipefail

input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // ""')
cwd=$(echo "$input" | jq -r '.cwd // ""')

# Pour debug : decommenter pour logger toutes les cmd verifiees
# echo "[guard] $(date -Is) $cmd" >> ~/.claude/pretool-guard.log

# 1. S3 destructive (golden rule s3-safety)
if echo "$cmd" | grep -qE '(aws s3 rm|aws s3 rb|aws s3 sync.*--delete)'; then
    echo 'BLOCKED: operation de suppression S3 detectee — golden rule s3-safety violation' >&2
    exit 2
fi

# 2. cd vers repertoire protege + rm dans la meme commande
if echo "$cmd" | grep -qE 'cd[[:space:]]+[^&|;]*(\$HOME/Pipeline|~/Pipeline|/home/blipinski/Pipeline|\$HOME/Run|~/Run|/home/blipinski/Run|/scratch/basecall)[^&|;]*(&&|\||;)[[:space:]]*[^&|;]*\brm\b'; then
    echo 'BLOCKED: cd vers repertoire protege suivi de rm — risque de bypass des deny rules' >&2
    exit 2
fi

# 3. Python interprete destructif
if echo "$cmd" | grep -qE 'python[23]?[[:space:]]+(-c|<<)[[:space:]]*.*(shutil\.rmtree|os\.unlink|os\.remove|Path\([^)]*\)\.unlink|os\.removedirs|pathlib\.[A-Z][a-z]+Path\([^)]*\)\.unlink)'; then
    echo 'BLOCKED: python -c avec appel destructif (rmtree/unlink/remove) — utiliser un script revue' >&2
    exit 2
fi

# 4. find -delete et find -exec rm
if echo "$cmd" | grep -qE 'find[[:space:]].*(-delete|-exec[[:space:]]+rm)'; then
    echo 'BLOCKED: find avec -delete ou -exec rm — utiliser rm explicit pour passer par les deny rules' >&2
    exit 2
fi

# 5. dd vers /dev/* (overwrite disque)
if echo "$cmd" | grep -qE 'dd[[:space:]].*\bof=/dev/'; then
    echo 'BLOCKED: dd vers device /dev/* — risque catastrophique de destruction disque' >&2
    exit 2
fi

# 6. xargs rm avec paths proteges
if echo "$cmd" | grep -qE 'xargs[[:space:]]+(-[^[:space:]]+[[:space:]]+)*rm[[:space:]]'; then
    if echo "$cmd" | grep -qE '(~/Pipeline|/home/blipinski/Pipeline|~/Run|/scratch/basecall|\.pod5)'; then
        echo 'BLOCKED: xargs rm cible un repertoire ou pattern protege' >&2
        exit 2
    fi
fi

# 7. Redirection > vers fichier .pod5 (overwrite POD5)
if echo "$cmd" | grep -qE '>[[:space:]]*[^[:space:]]+\.pod5(\b|$)'; then
    echo 'BLOCKED: redirection ecriture vers fichier .pod5 — POD5 source de verite (golden rule s3-safety)' >&2
    exit 2
fi

# 8. Truncate / shred / mkfs sur paths absolus
if echo "$cmd" | grep -qE '\b(shred|truncate|mkfs|mkfs\.[a-z0-9]+)\b'; then
    if echo "$cmd" | grep -qE '(/scratch|~/Pipeline|/home/blipinski/Pipeline|~/Run|/dev/)'; then
        echo 'BLOCKED: shred/truncate/mkfs sur chemin protege' >&2
        exit 2
    fi
fi

# 9. nextflow run depuis ~/Pipeline/ (golden rule nextflow.md)
#    Lancer Nextflow depuis ~/Pipeline/<projet>/ crée un workdir interne au repo
#    qui pollue le code et empêche les runs parallèles. Toujours utiliser ~/Run
#    ou ~/Run2 comme cwd.
if echo "$cmd" | grep -qE '\bnextflow[[:space:]]+(-[a-zA-Z][^[:space:]]*[[:space:]]+)*run\b'; then
    if echo "$cwd" | grep -qE '^/home/blipinski/Pipeline/'; then
        echo 'BLOCKED: nextflow run depuis ~/Pipeline/ — golden rule nextflow.md : lancer depuis ~/Run ou ~/Run2 (cd ~/Run && nextflow run ~/Pipeline/<projet>/main.nf)' >&2
        exit 2
    fi
fi

exit 0
