# Étape C — Dispatch update-column (database/check_samples.py)

## Fichier impacté
`~/Pipeline/trace-prod/database/check_samples.py`

## Arbre de décision : pattern simple vs preserve

```
                       Q7 — Comportement erreur S3 ?
                                  │
                ┌─────────────────┴──────────────────┐
                │                                    │
        KO strict (échec → KO)              Preserve (échec → skip UPDATE)
                │                                    │
        Pattern SIMPLE                       Pattern PRESERVE
        (1 edit dans COLUMN_CHECKERS)        (3 edits : decl + dispatch + fn)
                │                                    │
        check_*() retourne "KO"             check_*() retourne None sur erreur
                │                                    │
        ex: ancestry, mvaf_v12              ex: bam_horaire, short_read
```

## Pattern SIMPLE — 1 seul edit

Dans le dict `COLUMN_CHECKERS` (~ligne 337-388), ajouter UNE entrée alphabétiquement ou thématiquement :

```python
'<col>': ('<table>', 'check_<col>', 'checker', None),
```

Le 4e élément (`None`) peut être un paramètre extra si la méthode `check_*()` accepte un 3e argument (cf threshold_20m / `check_beta_depth(sd, sample, '20M')`).

**Suffit dans 80% des cas.** Le dispatch générique gère :
- str `"KO"`/`"NA"` → UPDATE à NULL
- date `DD-MM-YYYY` → conversion `YYYY-MM-DD`
- str avec virgule + col NUMERIC → conversion `,`→`.`
- autres → UPDATE direct

⚠ Limite : si `check_*()` retourne `None`, le générique fait quand même UPDATE à NULL → écrase la valeur existante. **Si tu veux preserve, utilise le pattern preserve.**

## Pattern PRESERVE — 3 edits

### Edit 1 — Déclaration dans COLUMN_CHECKERS

```python
'<col>': ('<table>', None, '<col>', None),
```

Note : le 2e élément est `None` (pas de méthode), le 3e est le `col_type` (le nom de la colonne sert de discriminant).

### Edit 2 — Dispatch dans update_column()

Dans `update_column()` (~ligne 391-498), ajouter un nouveau bloc juste après `if col_type == 'bam_horaire'` (~ligne 422-424) :

```python
if col_type == '<col>':
    _update_<col>(db_service, config, sample_type, labo, sample_filter=sample or None)
    return
```

### Edit 3 — Nouvelle fonction `_update_<col>()`

À placer juste après `_update_bam_horaire()` (~ligne 698-733), AVANT `_list_s3_objects` :

```python
def _update_<col>(db_service, config, sample_type: str, labo: str, sample_filter=None):
    """UPDATE chirurgical de la SEULE colonne <col>.
    Skip l'UPDATE si check_<col> retourne None (erreur S3 transient)."""
    checker = get_checker(sample_type, config, extract_bam=False)
    if sample_filter:
        samples = list(sample_filter)
    else:
        rows = db_service.conn.execute("""
            SELECT sample_name FROM samples WHERE sample_type = ? AND labo = ?
            ORDER BY sample_name
        """, [sample_type, labo]).fetchall()
        samples = [r[0] for r in rows]

    updated = skipped_err = missing = 0
    for i, s in enumerate(samples, 1):
        row = db_service.conn.execute("""
            SELECT id FROM samples WHERE sample_name = ? AND sample_type = ? AND labo = ?
        """, [s, sample_type, labo]).fetchone()
        if not row:
            missing += 1
            click.echo(f"  [{i}/{len(samples)}] {s}: pas en DB, skip")
            continue
        sample_dir = checker.sample_dir(s)
        status = checker.check_<col>(sample_dir, s)
        if status is None:
            skipped_err += 1
            click.echo(f"  [{i}/{len(samples)}] {s}: erreur S3, inchangé")
            continue
        db_service.conn.execute(
            "UPDATE <table> SET <col> = ? WHERE sample_id = ?",
            [status, row[0]],
        )
        updated += 1
        click.echo(f"  [{i}/{len(samples)}] {s}: {status}")
    click.echo(f"  {updated} mis à jour, {skipped_err} erreur S3, {missing} samples non DB")
```

## Cas particulier — bam_metadata join

Si `<table>` = `bam_metadata`, la requête JOIN est légèrement différente. Voir `_update_bam_horaire` comme modèle (utilise `bam_metadata b JOIN samples sa ON sa.id = b.sample_id`).

## Vérification

```bash
# Sur 2 samples (1 OK + 1 KO)
python3 database/check_samples.py update-column <col> liquid CGFL -s <sample_ok> -s <sample_ko>

# Vérifier en DB
python3 database/check_samples.py query "
  SELECT s.sample_name, r.<col>
  FROM samples s JOIN <table> r ON s.id = r.sample_id
  WHERE s.sample_name IN ('<sample_ok>', '<sample_ko>')
"
```

Résultats attendus :
- Output update-column : `<sample_ok>: OK`, `<sample_ko>: KO`, `2 mis à jour, 0 erreur S3`
- Query DB : 2 lignes avec les bonnes valeurs

## STOP — Validation Boris

```
✅ Étape C — update-column validée
- Pattern utilisé : SIMPLE | PRESERVE
- Entry COLUMN_CHECKERS ajoutée
- [Si preserve] Fonction _update_<col>() créée, skip None implémenté
- Test : <sample_ok>=OK, <sample_ko>=KO persistés en DB
- Multi-sample (-s s1 -s s2) supporté

OK pour Étape D (export gsheet) ?
```
