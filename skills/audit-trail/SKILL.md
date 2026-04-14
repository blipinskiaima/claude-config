---
name: audit-trail
description: "Génère un rapport de traçabilité ISO 15189 pour une version/modification du pipeline AIMA. Collecte changelog formaté, diff avant/après, hashes containers, résultats de non-régression. Use when the user says \"audit-trail\", \"tracabilité\", \"iso 15189\", \"montee en version\", \"qualification trail\", \"rapport qualité\"."
argument-hint: "[--version VX.Y.Z] [--project Bam2Beta|Pod2Bam] [--sample Healthy_826]"
allowed-tools: Bash(git*), Bash(docker*), Bash(cat*), Bash(grep*), Bash(sha256sum*), Bash(md5sum*), Bash(ls*), Bash(diff*), Bash(aws*), Read, Glob, Grep
---

# audit-trail

Génère un rapport de traçabilité conforme ISO 15189 pour une version/modification du pipeline AIMA Diagnostics.

## Contexte

- Norme **ISO 15189** : obligation de traçabilité pour les laboratoires de biologie médicale
- Exigences clés : qui a fait quoi, quand, sur quoi, avec quels outils, avec quels résultats
- Pipelines soumis : Bam2Beta (prioritaire), Pod2Bam (à venir), trace-prod
- Structure attendue : changelog + diff + hashes + non-régression

## Procédure

### Etape 1 — Identifier le périmètre

Si `--version` et `--project` fournis, utiliser directement.

Sinon :
- Détecter le projet via `pwd` (Bam2Beta, Pod2Bam, trace-prod)
- Lister les tags git récents : `git tag --sort=-v:refname | head -5`
- Demander à l'utilisateur : version courante vs version précédente à comparer

### Etape 2 — Changelog (git)

```bash
# Commits depuis la version précédente
git log --pretty=format:"%h | %ad | %an | %s" --date=short <PREV_TAG>..<CUR_TAG>

# Fichiers modifiés
git diff --name-status <PREV_TAG>..<CUR_TAG>
```

Filtrer et classer par type (feat, fix, docs, refactor, chore) selon le préfixe du commit.

### Etape 3 — Diff fonctionnel

Pour chaque fichier de code/config modifié (main.nf, *.nf, *.R, *.py, *.config, CHANGELOG.md) :

```bash
git diff <PREV_TAG>..<CUR_TAG> -- path/to/file.nf
```

Résumer en 1-2 phrases l'intention du changement (ex: "Ajout du module ichorCNA", "Fix du bug d'allocation mémoire BAM_Subsampling").

Ignorer les changements cosmétiques (whitespace, commentaires purs).

### Etape 4 — Hashes des containers Docker

Identifier les containers du projet (via `nextflow.config` ou `Dockerfile`). Pour chacun :

```bash
docker inspect --format='{{.Id}} | {{.RepoDigests}}' <image>
docker inspect --format='{{.Created}}' <image>
```

Produire un tableau :

| Container | Digest | Created |
|-----------|--------|---------|
| blipinskiaima/bam2beta:latest | sha256:... | 2026-04-01 |
| blipinskiaima/raima:latest | sha256:... | 2026-03-27 |

### Etape 5 — Hash des dépendances critiques

```bash
# BED files, références, modèles raima
sha256sum /scratch/dependencies/bed/epic850K*.bed
sha256sum /scratch/dependencies/raima-model/*.tsv.gz
sha256sum /scratch/dependencies/genomes/hg38/hg38.fa.fai
```

### Etape 6 — Tests de non-régression

Chercher les rapports de qualification récents :

```bash
ls -lt ~/Run*/QUALIF/V*/ 2>/dev/null | head -5
ls -lt /mnt/aima-bam-data/processed/MRD/QUALIF/V*/ 2>/dev/null | head -5
```

Pour le sample test (par défaut Healthy_826) :

```bash
# Rechercher le rapport de conformité
find /mnt/aima-bam-data/processed/MRD/DEV/V<VERSION>/ -name "*check-conformity*" -o -name "*.rapport.pdf"
```

Résumer les résultats : RUN CONFORME / QUALIFICATION CONFORME / écarts détectés.

### Etape 7 — Rapport final

Produire un rapport structuré au format Markdown :

```markdown
# Audit Trail — {Project} {CUR_VERSION}
**Date** : {YYYY-MM-DD}
**Version précédente** : {PREV_VERSION}
**Auteur** : {git user.name}

## 1. Changelog
{N commits depuis {PREV_VERSION}}

### Features (feat:)
- {hash} — {message}

### Fixes (fix:)
- {hash} — {message}

### Other
- {hash} — {message}

## 2. Fichiers modifiés
| Fichier | Statut | Impact |
|---------|--------|--------|
| main.nf | M | Ajout param X |
| conf/prod.config | M | Activation module Y |

## 3. Containers Docker
| Image | Digest | Build date |
|-------|--------|-----------|

## 4. Dépendances critiques
| Fichier | SHA256 |
|---------|--------|

## 5. Tests de non-régression
- Sample : {Healthy_826}
- Run DEV : {path}
- Conformité : {✓ CONFORME / ✗ ECART}
- Conformité vs QUALIF précédent : {✓ / ✗}
- Écarts détectés : {liste ou "aucun"}

## 6. Validation
- [ ] Code review effectuée
- [ ] Test fonctionnel passé
- [ ] Non-régression validée
- [ ] Documentation mise à jour
- [ ] Tag git poussé
- [ ] Release GitHub créée
```

Sauvegarder le rapport dans `~/Pipeline/{project}/audit/audit_{version}_{date}.md` si le dossier existe, sinon proposer le chemin à l'utilisateur.

## Notes

- Ne jamais modifier les fichiers sans confirmation
- Les hashes doivent être reproduits exactement pour la traçabilité
- Si le container `latest` est utilisé, avertir : préférer des tags immuables
- Le skill ne remplace pas `/maj-bam2beta` qui fait la montée en version complète — il génère juste le document de traçabilité
