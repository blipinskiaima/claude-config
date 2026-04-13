---
name: debug-nf
description: Diagnostiquer un run Nextflow echoue. Lit les logs, identifie le processus en erreur, propose un fix. Use when the user says "debug", "nextflow error", "run failed", "pourquoi ça plante", or mentions a Nextflow error.
argument-hint: "[path/to/.nextflow.log] [--last]"
allowed-tools: Bash(cat*), Bash(grep*), Bash(ls*), Bash(find*), Bash(head*), Bash(tail*), Read, Glob, Grep
---

# debug-nf

Diagnostique automatiquement un run Nextflow echoue dans l'environnement AIMA.

## Contexte

- Pipelines : Bam2Beta (`~/Pipeline/Bam2Beta/`), Pod2Bam (`~/Pipeline/Pod2Bam/`)
- Runs lances depuis `~/Run` ou `~/Run2`
- Logs : `.nextflow.log` dans le repertoire de lancement
- Containers : `blipinskiaima/bam2beta:latest`, `pod2bam:0.9.6`, `pod2bam:1.4.0`
- Erreurs frequentes : OOM, S3 timeout, container pull failed, publishDir error

## Procedure

### Etape 1 — Localiser le log Nextflow

Si l'utilisateur fournit un chemin, l'utiliser directement.

Sinon, chercher le `.nextflow.log` le plus recent :

```bash
find ~/Run ~/Run2 -maxdepth 2 -name ".nextflow.log" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -5
```

Si `--last` est passe, prendre le plus recent sans demander.

Sinon, presenter les logs trouves et demander a l'utilisateur lequel analyser.

### Etape 2 — Identifier les erreurs

Chercher dans le `.nextflow.log` :

```bash
grep -n -E "ERROR|caused by:|Process .* terminated|exit status [1-9]|WARN.*fail|Cannot|Exception" .nextflow.log | tail -50
```

Chercher aussi le resume des processus :

```bash
grep -A2 "process >" .nextflow.log | tail -30
```

### Etape 3 — Identifier le processus echoue

Extraire :
- Le nom du processus (ex: `BINARIZE_CPG`)
- Le task hash (ex: `a1/b2c3d4`)
- L'exit code

```bash
grep -E "Task .* failed|exit status|Error executing process" .nextflow.log | tail -10
```

Localiser le repertoire de travail du task :

```bash
grep -B5 "exit status" .nextflow.log | grep "work/" | tail -1
```

### Etape 4 — Lire les logs du task echoue

Dans le repertoire `work/{hash}/` :

```bash
cat work/{hash}/.command.err
cat work/{hash}/.command.log
cat work/{hash}/.command.sh
cat work/{hash}/.command.run
```

Lire aussi `.exitcode` pour confirmer le code de sortie.

### Etape 5 — Diagnostiquer

Appliquer ces regles de diagnostic :

| Symptome | Diagnostic | Fix |
|----------|-----------|-----|
| `exit status 137`, `Killed`, `oom-kill` | OOM - memoire insuffisante | Augmenter `memory` dans le process ou ajouter `errorStrategy 'retry'` + `maxRetries 3` avec `memory { 8.GB * task.attempt }` |
| `exit status 1` + erreur Python/R | Bug dans le script | Lire `.command.err` pour l'erreur exacte, proposer correction |
| `S3 error`, `timeout`, `NoSuchKey` | Probleme S3 | Verifier `aws s3 ls` sur le chemin, verifier les credentials |
| `pull access denied`, `manifest unknown` | Container introuvable | Verifier le tag du container avec `docker images`, corriger dans `nextflow.config` |
| `publishDir` error | Erreur de publication | Verifier que le dossier de destination existe et a les permissions |
| `No such file`, `FileNotFoundException` | Fichier d'entree manquant | Verifier le samplesheet/input, verifier que le fichier existe |
| `exit status 143` | Task annule (timeout ou kill) | Augmenter `time` dans le process |
| `exit status 255` + SSH/network | Erreur reseau | Verifier la connexion, relancer avec `-resume` |

### Etape 6 — Rapport

Produire le rapport au format suivant :

```
## Diagnostic run Nextflow

### Erreur
- Process : {NOM_PROCESS} (task {hash})
- Exit code : {code}
- Cause : {diagnostic}

### Logs
{extraits pertinents du .command.err, max 30 lignes}

### Fix propose
{solution concrete avec commande ou modification de code}

### Commande pour relancer
nextflow run {pipeline} -resume {autres options du run original}
```

Pour reconstituer la commande de relance, lire le `.nextflow.log` :

```bash
grep "Command line" .nextflow.log | head -1
```

## Notes

- Toujours proposer `-resume` pour ne pas recalculer les taches deja terminees
- Si plusieurs processus ont echoue, les lister tous puis diagnostiquer chacun
- Si le log est tres volumineux, se concentrer sur les 500 dernieres lignes pour les erreurs
- Ne jamais modifier de fichier sans confirmation de l'utilisateur
