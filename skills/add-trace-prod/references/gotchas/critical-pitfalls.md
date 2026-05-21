# Pièges critiques à éviter

Tous ces gotchas viennent d'expériences réelles dans le projet trace-prod. Les ignorer = bugs en prod.

## 1. `aws s3 ls --recursive` retourne les clés COMPLÈTES

### Le piège

`aws s3 ls --recursive s3://bucket/path/to/sample/` retourne dans la 4e colonne :
```
processed/MRD/RetD/liquid/CGFL/sample/BAM/file.bam   # ← clé S3 complète depuis le bucket root
```

PAS la clé relative au dossier listé (`BAM/file.bam`).

Donc faire `key.split("/", 1)[0]` donne `"processed"`, jamais `"BAM"`.

### Le fix

Toujours stripper avec un `sample_prefix` connu :
```python
sample_prefix = f"processed/MRD/RetD/{self.config.sample_type}/{self.config.labo}/{sample}/"
for line in lines:
    parts = line.split(maxsplit=3)
    key = parts[3]
    if not key.startswith(sample_prefix):
        continue
    relative = key[len(sample_prefix):]
    folder = relative.split("/", 1)[0]  # ← maintenant correct
```

### Vu en vrai sur

Schema v7 — `check_short_read` premier draft retournait KO sur 100% des samples car `parts[3].split("/", 1)[0] == "processed"`. Fix : ajout du `sample_prefix` strip.

---

## 2. DuckDB single writer lock

### Le piège

DuckDB n'accepte qu'**un seul écrivain à la fois**. Si tu lances 2 `update-column` en parallèle, le second hang ou crash avec `database is locked`.

### Le fix

**Séquentialiser** :
```bash
# ❌ MAUVAIS
tp update-column <col> liquid CGFL &
tp update-column <col> liquid HCL &

# ✅ BON
tp update-column <col> liquid CGFL
tp update-column <col> liquid HCL
```

Si la DB est lockée par une autre session :
```bash
fuser ~/Pipeline/trace-prod/database/samples_status.duckdb
```

---

## 3. STATUS_COLUMNS rigide

### Le piège

Ajouter une colonne dans `STATUS_COLUMNS` (`lib/duckdb.py` ligne 412-428) force le parsing strict via `_parse_status` qui rejette TOUTE valeur autre que `OK`, `KO`, `WARNING`.

Si plus tard tu veux y mettre `"OK partial 4/6"` ou un nombre, tu es coincé : valeur transformée en NULL silencieusement.

### Le fix

**Préférer VARCHAR libre** (ne pas ajouter à STATUS_COLUMNS). Le default `'KO'` reste possible, le parsing est juste plus laxe.

Si tu as besoin de la rigueur OK/KO/WARNING à 100%, ajoute à STATUS_COLUMNS. Sinon, garde VARCHAR libre — c'est ce qu'ont fait `ichorcna_score`, `ancestry`, `frag_mode1`, `read_start_time`, `short_read`.

---

## 4. CREATE TABLE AS SELECT perd les PRIMARY KEY/FK

### Le piège

DuckDB ne préserve PAS les contraintes lors de `CREATE TABLE new AS SELECT * FROM old`. Si tu tentes une migration brute, tu casses les FK silencieusement.

### Le fix

Toujours utiliser le DDL original + `INSERT INTO ... SELECT` pour les migrations de tables. Voir `DuckDBService.compact()` (`lib/duckdb.py` ~ligne 489) comme modèle.

Pour les **ajouts de colonnes** (cas standard de ce skill), `ALTER TABLE ... ADD COLUMN` est OK — pas de problème de FK.

---

## 5. Collision mapping TSV_TO_DB

### Le piège

Plusieurs `tsv_col` peuvent légitimement pointer vers le même `db_col` (variantes casse/long/court entre labos) :
```python
"SpeedVac": "speedvac",
"SpeedVAc": "speedvac",       # ← HCL a une casse différente
"Stage": "stage",
"Stage (I, II, III and IV or code ADICAP if available)": "stage",  # ← long format
```

Sans précaution, la 2e itération écrase la 1re par `None` (colonne absente dans le labo courant).

### Le fix

Code existant dans `_prepare_data` (`lib/duckdb.py` ~ligne 599-611) :
```python
for tsv_col, db_col in mapping.items():
    if tsv_col not in raw_data:
        continue
    val = raw_data[tsv_col]
    ...
    # ✅ Préserve la 1re valeur non-None
    if new is not None or db_col not in data:
        data[db_col] = new
```

Ne pas casser cette logique. Si tu rajoutes une variante, vérifier que la règle `or db_col not in data` est respectée.

---

## 6. Fallback dict oublié dans check_sample()

### Le piège

`LiquidChecker.check_sample()` et `SolidChecker.check_sample()` ont un bloc `if not self.sample_exists(sample):` qui retourne un dict pré-rempli pour TOUTES les colonnes.

Si on oublie d'y ajouter la nouvelle colonne :
- Le sample non-présent sur filesystem → KeyError quand l'export tente `sample.get("<Header>")`
- Ou silencieusement `"NA"` au lieu du default voulu (selon où le fallback s'applique)

### Le fix

Toujours ajouter dans le fallback dict (`lib/checkers.py` ~ligne 480-518 liquid) :
```python
"<Header Gsheet>": "<default>",  # ex: "KO" ou "NA"
```

Idem pour SolidChecker (~ligne 596-700) si scope inclut solid.

---

## 7. Path.iterdir() sur /mnt/aima-bam-data/

### Le piège

Le mount s3fs FUSE peut bloquer (wchan=`request_wait_answer`) sur `Path.iterdir()` quand le dossier contient 700+ entrées. C'est arrivé sur `/mnt/aima-bam-data/data/CGFL/liquid/` (samples).

### Le fix

Pour lister les samples : **query la DB DuckDB**, pas le filesystem.
```python
# ✅ BON (rapide, robuste)
rows = db_service.conn.execute("""
    SELECT sample_name FROM samples WHERE sample_type = ? AND labo = ?
""", [sample_type, labo]).fetchall()

# ❌ MAUVAIS (peut hanger)
samples = [p.name for p in config.origin_dir.iterdir() if p.is_dir()]
```

Pour les listings S3 directs : utiliser `_s3_ls_lines` ou `_s3_ls_recursive` (subprocess `aws s3 ls`, bypasse le FUSE).

---

## 8. S3 sync skip silencieusement

### Le piège

`aws s3 sync` Scaleway skip silencieusement 3-5 fichiers sur 23-90, de manière aléatoire. Pas d'erreur, juste des fichiers manquants.

### Le fix

Ce skill ne fait pas de sync, mais si tu écris du code qui télécharge des outputs : **retry en boucle** jusqu'à `local_count == s3_count`. Voir `~/.claude/rules/s3-safety.md`.

---

## 9. Métadonnée rebasecalled : propagation forcée

### Le piège

Les samples `*_rebasecalled*` doivent toujours hériter de la metadata de leur sample original. Si tu ajoutes une colonne metadata, il faut que `import-metadata` la propage aussi aux rebasecalled.

### Le fix

`import-metadata` re-propage déjà toutes les colonnes via la logique `_propagate_rebasecalled()` dans le code existant. Tant que tu passes par `TSV_TO_DB_METADATA` standard, ça marche automatiquement.

⚠ Pour POD5 storage (cas particulier) : NE PAS propager (voir [[feedback-rebasecalled-pod5]] dans la mémoire trace-prod).

---

## 10. Date format DD-MM-YYYY → YYYY-MM-DD

### Le piège

DuckDB DATE attend `YYYY-MM-DD`. Si ton checker retourne `DD-MM-YYYY` (format français), l'INSERT/UPDATE échoue silencieusement (colonne NULL).

### Le fix

La conversion existe déjà dans `update_column()` (`check_samples.py` ~ligne 478-480) :
```python
elif column == 'date_done' and isinstance(new_value, str) and len(new_value.split('-')) == 3:
    parts = new_value.split('-')
    db_value = f"{parts[2]}-{parts[1]}-{parts[0]}"
```

Si ta nouvelle colonne est de type DATE, dupliquer la logique avec ton nom de colonne, OU normaliser en YYYY-MM-DD dans le checker.

---

## Checklist anti-régression

Avant de marquer une étape comme `completed`, vérifier :

- [ ] **Étape A** : `tp columns <table>` montre la colonne avec le bon default
- [ ] **Étape A** : `tp query "SELECT MAX(version) FROM _schema_version"` retourne N+1
- [ ] **Étape B** : test direct du `check_*()` retourne OK + KO sur 2 samples réels
- [ ] **Étape B** : fallback dict du checker pour sample absent contient la colonne
- [ ] **Étape C** : `tp update-column -s sample` persiste en DB (query check)
- [ ] **Étape D** : `head -1 export.tsv | tr '\t' '\n' | grep -n "<Header>"` à la bonne position
- [ ] **Étape D** : valeur d'un sample testé apparaît dans l'export
- [ ] Aucun warning/error pendant les vérifications
- [ ] Mémoire mise à jour (fichier topique + MEMORY.md)
