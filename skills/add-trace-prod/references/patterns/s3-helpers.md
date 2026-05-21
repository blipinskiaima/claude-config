# Pattern — Helpers S3 dans extractors.py

## Les 4 helpers existants

Tous dans `lib/extractors.py` (~ligne 23-77). Conventions communes :
- Retournent `None` sur échec (timeout, OSError, returncode != 0)
- Utilisent profil `scw` (variable `_S3_PROFILE`)
- Bucket `aima-bam-data` (variable `_S3_BUCKET`)
- Convertissent `/mnt/aima-bam-data/...` → `s3://aima-bam-data/...`

### `_s3_read_text(filepath: Path) -> Optional[str]`

```python
content = _s3_read_text(sample_dir / "BETA" / f"{sample}.raima.tsv")
if content is None and tsv.exists():
    content = tsv.read_text(encoding="utf-8")  # fallback NFS
```

- Cmd : `aws s3 cp s3://... -` (stdout)
- Timeout : 10s
- **Usage** : lecture d'1 petit fichier TSV/log (< 10 MB recommandé)
- ⚠ Ne pas utiliser pour les BAM (gros), POD5, bedMethyl > 10 MB

### `_s3_exists(filepath: Path) -> Optional[bool]`

```python
if _s3_exists(sample_dir / "QC" / f"{sample}.tsv"):
    return "OK"
```

- Cmd : `aws s3api head-object`
- Timeout : 5s
- **Usage** : vérifier la présence d'1 fichier sans le lire (fichiers volumineux : read_start_time.tsv ~3-4 GB)

### `_s3_ls_lines(dir_path: Path, prefix: str = "") -> Optional[list]`

```python
lines = _s3_ls_lines(sample_dir / "BETA")
if lines:
    files = [l.split()[-1] for l in lines]  # extract filename column
```

- Cmd : `aws s3 ls s3://.../` (listing 1 niveau, exclut marqueurs `/`)
- Timeout : 10s
- **Usage** : lister un dossier sans descendre dans les sous-dossiers
- Sortie : lignes `YYYY-MM-DD HH:MM:SS  SIZE  filename`

### `_s3_ls_recursive(dir_path: Path) -> Optional[list]`

```python
lines = _s3_ls_recursive(short_sd)
for line in lines:
    parts = line.split(maxsplit=3)
    key = parts[3]  # ⚠ clé S3 COMPLÈTE
```

- Cmd : `aws s3 ls --recursive s3://.../`
- Timeout : 30s (plus long car gros listings)
- **Usage** : compter/lister tous les fichiers d'un sample (sous-dossiers inclus)
- ⚠ La 4e colonne contient la clé S3 **complète depuis le bucket root**, pas relative au dossier listé. Toujours stripper via un `sample_prefix` connu.

## Arbre de décision

```
Que veux-tu faire ?
│
├─ Lire le contenu d'1 fichier
│   ├─ Petit (< 10 MB) → _s3_read_text
│   └─ Gros → NE PAS LIRE, juste check présence → _s3_exists
│
├─ Vérifier la présence d'1 fichier → _s3_exists
│
├─ Compter/lister fichiers d'un dossier
│   ├─ 1 niveau seulement → _s3_ls_lines
│   └─ Récursif (sous-dossiers) → _s3_ls_recursive
│
└─ Aucun ne convient → ajouter un nouveau helper dans extractors.py
```

## Pattern S3-first systématique

Toujours essayer S3 d'abord, fallback NFS uniquement si S3 retourne None ET si on a besoin du contenu :

```python
content = _s3_read_text(tsv)
if content is None and tsv.exists():
    try:
        content = tsv.read_text(encoding="utf-8")
    except IOError:
        return "NA"
if not content:
    return "NA"
```

## Anti-patterns

### ❌ Lire un gros fichier (>10 MB) avec _s3_read_text

```python
# MAUVAIS — read_start_time.tsv fait 3-4 GB
content = _s3_read_text(sample_dir / "QC/Samtools" / f"{sample}.read_start_time.tsv")

# BON — juste vérifier l'existence
return self._ok_ko(self._exists(sample_dir / "QC/Samtools" / f"{sample}.read_start_time.tsv"))
```

### ❌ `Path.iterdir()` sur `/mnt/aima-bam-data/`

Le mount s3fs peut hanger sur des dossiers à 700+ entrées. Toujours utiliser `_s3_ls_lines` ou `_s3_ls_recursive` à la place.

### ❌ Profil aws au lieu de scw

Tous les helpers utilisent `_S3_PROFILE = "scw"`. Ne pas ajouter de helper avec profil aws sauf bucket différent justifié.

## Quand ajouter un nouveau helper

Critères :
- Aucun helper existant ne convient
- Le pattern sera réutilisé (≥ 2 colonnes)
- L'opération est différente sémantiquement (pas juste un paramètre en plus)

Sinon : utiliser un helper existant + parsing inline dans `check_*()`.
