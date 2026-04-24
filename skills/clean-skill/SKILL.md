---
name: clean-skill
description: Nettoie le code d'un projet Pipeline (Python/Nextflow/R/Bash) de Boris. Refactorisation, simplification, suppression du code mort et inutile. Commence par un checkpoint git (commit + tag) pour rollback garanti. Comportement du code strictement intact, aucune régression fonctionnelle. Use when the user says "clean-skill", "nettoie le code", "clean code", "nettoyer le projet", "supprimer code mort", "dead code", "refactor code", "simplifier code", or asks to clean up a project in ~/Pipeline/.
---

<role>
Tu aides Boris à nettoyer un projet de son dossier `~/Pipeline/` : refactoriser,
simplifier, supprimer le code mort et inutile — **sans jamais changer le
comportement observable**.
</role>

<contexte-utilisateur>
Boris = bioinformaticien AIMA, bus factor = 1 sur tout le stack Pipeline.
Langages : Python (intermédiaire), Nextflow/Groovy (expert), R/Bash (avancé).
Il maintient seul tous les projets → privilégier la **lisibilité linéaire** sur
l'élégance. Si un pattern n'est pas déjà utilisé dans le projet (décorateurs
custom, Protocol/ABC, metaprogramming, type hints complexes, closures Groovy
imbriquées), **ne l'introduis pas**.
</contexte-utilisateur>

<regles-absolues>
1. **Comportement intact** — aucune modif d'API publique, signature exposée,
   route Dash, process Nextflow, paramètre CLI, ou format de sortie
2. **Checkpoint d'abord** — Step 0 obligatoire, jamais de clean sans tag de rollback
3. **Dry-run** — tu proposes un rapport, Boris valide par catégorie, tu appliques
   ensuite. Jamais l'inverse
4. **Preuve obligatoire** — chaque suppression s'appuie sur un grep qui confirme
   l'absence d'usage dans ce repo ET les autres projets Pipeline qui en dépendent
   (cf. CLAUDE.md du projet pour identifier les dépendances)
5. **Edits chirurgicaux** — `Edit` tool uniquement, jamais `Write` sur fichier
   existant ; aucun refactor "bonus" non listé
6. **Karpathy Guidelines** (`~/.claude/CLAUDE.md`) — simplicity, surgical,
   no speculative abstractions
7. **Golden Rules** (`~/.claude/rules/`) — s3-safety, duckdb, nextflow, secrets
   sont non-négociables (zéro exception)
</regles-absolues>

<workflow>

## 0. Checkpoint (obligatoire, AVANT tout scan)

Point de rollback garanti. Jamais de clean sans checkpoint.

```bash
# 1. État du repo
git status --porcelain

# 2. Si dirty → vérifier qu'aucun secret n'est dans les changements
if [ -n "$(git status --porcelain)" ]; then
  # Scan préventif secrets avant add -A
  if git diff --name-only && git ls-files --others --exclude-standard | \
     xargs grep -l -iE "(password|token|api[_-]?key|secret)[=:]" 2>/dev/null; then
    echo "⚠️  Fichiers sensibles détectés. Stop — Boris doit gitignore d'abord."
    exit 1
  fi
  git add -A
  git commit -m "chore(clean-skill): checkpoint avant nettoyage $(date +%F)"
fi

# 3. Tag de retour (toujours, même si clean)
TAG="clean-skill-checkpoint-$(date +%Y%m%d-%H%M)"
git tag "$TAG"

# 4. Annoncer
echo "🏁 Checkpoint : $TAG ($(git rev-parse --short HEAD))"
echo "   Rollback    : git reset --hard $TAG"
```

Garder le tag en tête du rapport final.

## 1. Scan — détecter le type de projet

```bash
ls                                       # structure racine
cat CLAUDE.md 2>/dev/null                # conventions + deps inter-projets
ls src/ 2>/dev/null                      # projet Python
ls main.nf nextflow.config 2>/dev/null   # projet Nextflow
ls *.R 2>/dev/null                       # projet R
```

Identifier : langage primaire, entry points, dépendances cross-projet citées
dans CLAUDE.md.

## 2. Detection — 4 catégories universelles

**A. Code mort (🟢 sûr)**
- Python : `ruff check --select F401,F841 src/` (imports/variables inutilisés)
- Nextflow : processes jamais `include`/appelés, params de `nextflow.config`
  jamais référencés (`grep -rn "params.foo"`)
- R/Bash : fonctions jamais sourcées/appelées (grep manuel)
- Tous : branches inatteignables (`if False:`, code après `return`/`exit`/`raise`)

**B. Duplication sémantique (🟡 à valider)**
- Même logique 2-3 fois → factorisation **simple** (fonction, pas classe/module
  nouveau)
- Chaînes/constantes répétées → constante locale au module
- Nextflow : 2 processes quasi-identiques → un seul paramétré (seulement si la
  différence est un vrai paramètre, pas un workaround)

**C. Over-engineering (🟡 à valider)**
- Classe à usage unique sans état → fonction
- Paramètre `default` jamais overridé → signature simplifiée (interne uniquement)
- `try/except` sur erreurs impossibles
- Config fields jamais lus (Python, `nextflow.config`, R options)
- Wrapper qui ne fait qu'appeler une autre fonction à l'identique

**D. Surface publique (🔴 risqué — signaler, pas toucher)**
- Python : fonction/classe publique (pas de `_`) apparemment orpheline
- Nextflow : process publié dans un module `include`-able
- Dash : callbacks référencés par string ID (grep `id="..."` avant tout)
- CLI : sous-commandes `argparse`/`click` → chercher dans scripts shell
- **Vérifier usage cross-projet** : `grep -rn "from <projet>" ~/Pipeline/*/`

## 3. Rapport (obligatoire avant toute modif)

```
## clean-report — <projet> — <date>
🏁 Checkpoint : clean-skill-checkpoint-<timestamp>
   Rollback   : git reset --hard clean-skill-checkpoint-<timestamp>

### 🟢 SÛR (N)
- `src/foo.py:42` — import `os` inutilisé (0 usage vérifié dans le fichier)
- `modules/bar.nf:10-30` — process `legacy_qc` jamais `include` (grep Pipeline/)

### 🟡 À VALIDER (N)
- `src/services.py:210-250` — `_old_helper()` 0 appel (grep src/ + tests/). Supprimer ?
- `main.nf:80-110` — canal `ch_tmp` dupliqué avec `main.nf:180-210`. Factoriser ?

### 🔴 RISQUÉ (N)
- `src/api.py:15` — `public_func()` sans usage interne ni cross-projet visible. Décision ?
- `workflows/run.nf:40` — process exporté `RUN_QC`. Utilisé par un autre pipeline ?
```

Chaque entrée : **chemin:ligne + nature + preuve (commande grep) + action proposée**.

## 4. Validation (attendre Boris)

"applique le vert" / "vert + jaune" / "applique tout" / validation item par item.
Ne rien toucher avant son feu vert.

## 5. Apply

- Un `Edit` par changement, groupé par fichier
- Strictement ce qui est dans le rapport validé
- Aucun refactor "bonus"

## 6. Verify (adapté au langage, après chaque apply)

**Python** :
```bash
python3 -m py_compile $(find . -name "*.py" -not -path "*/\.*")
python3 -c "import <module_principal>"  # adapter selon projet
pytest --collect-only -q 2>/dev/null || true
```

**Nextflow** :
```bash
nextflow run main.nf --help 2>&1 | head -20  # parse OK
nextflow run main.nf -profile test -preview 2>&1 | tail -10  # si profil test
```

**R** :
```bash
Rscript -e 'source("main.R"); cat("OK\n")'
```

**Bash** :
```bash
bash -n script.sh                # syntax check
shellcheck script.sh 2>/dev/null || true
```

Si échec → stop, signaler à Boris, proposer la commande de rollback pré-remplie :
`git reset --hard <TAG>`.

</workflow>

<exemples>

<exemple niveau="🟢 SÛR — Python">
Trouvé : `from typing import Optional` dans `src/foo.py:3`
Vérif : `grep -c "Optional" src/foo.py` → 1 (uniquement l'import)
Rapport : 🟢 `src/foo.py:3` — import `Optional` inutilisé
</exemple>

<exemple niveau="🟢 SÛR — Nextflow">
Trouvé : `params.old_threshold = 0.5` dans `nextflow.config:45`
Vérif : `grep -rn "params.old_threshold" .` → 1 (uniquement la définition)
Rapport : 🟢 `nextflow.config:45` — `params.old_threshold` jamais lu
</exemple>

<exemple niveau="🟡 À VALIDER">
Trouvé : `_normalize_path()` dans `src/services.py:45-60`
Vérif : `grep -rn "_normalize_path" ~/Pipeline/` → uniquement la définition
Rapport : 🟡 `src/services.py:45-60` — `_normalize_path()` jamais appelée (repo + cross-projet). Supprimer ?
</exemple>

<exemple niveau="🔴 RISQUÉ — ne pas toucher">
Trouvé : process `CALL_VARIANTS` dans `modules/call.nf` sans usage visible
Vérif cross-projet : `grep -rn "CALL_VARIANTS" ~/Pipeline/*/` → résultats dans autres repos
Rapport : 🔴 `modules/call.nf` — process utilisé par d'autres pipelines. Ne pas toucher.
</exemple>

</exemples>

<anti-patterns>
NE JAMAIS :
- Introduire un décorateur/closure custom pour "factoriser" 2-3 usages
- Remplacer une boucle claire par une comprehension/chain imbriquée
- Ajouter des type hints complexes si le projet n'en a pas
- "Moderniser" la syntax si la version cible ne le supporte pas
- Supprimer des commentaires, même paraissant évidents
- Renommer des variables (hors `_unused_*`)
- Toucher aux retries/backoff DuckDB (`~/.claude/rules/duckdb.md`)
- Toucher aux opérations S3 (`~/.claude/rules/s3-safety.md`)
- Lancer Nextflow depuis le répertoire du pipeline (`~/.claude/rules/nextflow.md`)
- Logger/afficher secrets, tokens, credentials (`~/.claude/rules/secrets.md`)
- Skip le Step 0 checkpoint, même "juste pour voir"
</anti-patterns>

<format-reponse>
- **Step 0** : afficher le tag de checkpoint + commande de rollback
- **Avant apply** : rapport markdown structuré + rappel du tag en en-tête + question "quelle catégorie j'applique ?"
- **Pendant apply** : une ligne par fichier modifié (`src/foo.py: 3 lignes supprimées`)
- **Après apply** : résultat des vérifs + `git diff --stat` + rappel rollback
- **En cas d'échec** : stop, message court, rollback pré-rempli :
  `git reset --hard clean-skill-checkpoint-<timestamp>`
</format-reponse>
