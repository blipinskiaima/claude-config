# Pattern — Preserve vs Overwrite sur erreur S3

## Le problème

`update-column` tourne sur 600-1300 samples séquentiellement. Pendant ces minutes :
- S3 Scaleway peut throttle (rate limit)
- Network peut hoqueter (timeout 10-30s)
- Le check peut échouer pour des raisons transient

**Question** : que stocker en DB si le check échoue ?

## Deux comportements possibles

### Comportement A — Overwrite à KO (générique)

Le check retourne `"KO"` explicite sur erreur. Le dispatch générique fait `UPDATE col = NULL` (car `'KO'` est traité par `_parse_status`/cas particulier).

**Avantage** : code simple, 1 ligne dans `COLUMN_CHECKERS`.
**Inconvénient** : un transient S3 réécrit la valeur correcte précédente par KO.

### Comportement B — Preserve (skip UPDATE si None)

Le check retourne `None` sur erreur. Une fonction dédiée `_update_<col>()` vérifie `is None` et **skip l'UPDATE SQL** dans ce cas.

**Avantage** : la valeur précédente est préservée, robuste aux transients.
**Inconvénient** : 3 edits au lieu d'1, pattern dédié.

## Quand utiliser preserve

Critères qui justifient le pattern preserve :
- Le check S3 est **coûteux** (≥ 1 appel API, listing récursif)
- L'erreur S3 est **statistiquement probable** sur de gros runs (600+ samples)
- La valeur précédente a une **valeur informationnelle** qu'on ne veut pas perdre

Exemples concrets dans le code :
- ✅ `bam_horaire` — listing récursif S3, preserve si erreur
- ✅ `short_read` (v7) — listing récursif sur bucket mirror, preserve
- ❌ `ancestry` — lecture d'1 petit TSV, retourne `"NA"` direct sur erreur (acceptable car NA est aussi le default)

## Quand utiliser overwrite

- Check S3 léger (1 `_s3_exists` ou `_s3_read_text` < 10 MB)
- Default `"KO"` est sémantiquement correct si fichier absent OU erreur
- Pas besoin de distinguer "fichier absent" et "erreur S3 transient"

## Implémentation preserve (code modèle)

### Étape B — `check_*()` retourne Optional

```python
def check_<col>(self, sample_dir: Path, sample: str) -> Optional[str]:
    """OK/KO selon présence. None si erreur S3 (preserve)."""
    lines = _s3_ls_recursive(...)
    if lines is None:
        return None
    # logique normale
    return "OK" if condition else "KO"
```

### Étape C — Fonction dédiée `_update_<col>()`

Le pivot est `if status is None: skipped_err += 1; continue` (pas d'UPDATE SQL).

Voir [steps/step-c-update-column.md](../steps/step-c-update-column.md) pour le template complet.

### Étape C — Entrée COLUMN_CHECKERS distinctive

```python
'<col>': ('<table>', None, '<col>', None),
```

Le 3e élément `'<col>'` (au lieu de `'checker'`) sert de discriminant dans le switch de `update_column()`.

## Anti-patterns

### ❌ Retourner None depuis un check sans fonction dédiée

```python
def check_<col>(self, sd, s) -> Optional[str]:
    return None if err else "OK"

# COLUMN_CHECKERS
'<col>': ('<table>', 'check_<col>', 'checker', None),  # ⚠ générique !
```

Le dispatch générique va `UPDATE col = NULL` → tu perds quand même la valeur. Il FAUT la fonction `_update_<col>()` pour bénéficier du preserve.

### ❌ Fonction dédiée qui ne skip pas

```python
def _update_<col>(...):
    status = checker.check_<col>(sd, s)
    db_service.conn.execute("UPDATE ...", [status, sample_id])  # ⚠ exécuté même si status is None
```

Toujours vérifier `if status is None: continue` AVANT l'UPDATE.

### ❌ Skip silencieux sans log

Toujours logger `click.echo(f"  [{i}/{N}] {s}: erreur S3, inchangé")` pour que Boris puisse re-lancer un `update-column -s sample` ciblé après coup.

## Re-tentative ciblée après preserve

Si après `tp update-column <col> liquid CGFL` certains samples sont restés inchangés (erreur S3), Boris peut re-lancer ciblé :

```bash
# Lister les samples qui n'ont pas la dernière update
tp query "SELECT s.sample_name FROM samples s JOIN <table> r ON s.id=r.sample_id WHERE s.sample_type='liquid' AND s.labo='CGFL' AND r.updated_at < '<timestamp>'"

# Re-tenter sur les samples problématiques
tp update-column <col> liquid CGFL -s sample1 -s sample2 -s sample3
```
