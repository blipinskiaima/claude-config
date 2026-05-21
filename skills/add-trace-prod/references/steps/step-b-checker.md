# Étape B — Méthode `check_*()` (lib/checkers.py)

## Fichiers impactés
- `lib/extractors.py` (UNIQUEMENT si nouveau helper S3 nécessaire)
- `lib/checkers.py` (4 edits)

## Décision préalable — Quel helper S3 ?

Voir [patterns/s3-helpers.md](../patterns/s3-helpers.md). Résumé :

| Besoin | Helper |
|---|---|
| Lire 1 fichier TSV/log (< 10 MB) | `_s3_read_text(path)` |
| Vérifier présence d'1 fichier | `_s3_exists(path)` |
| Lister 1 dossier (non récursif) | `_s3_ls_lines(dir)` |
| Lister récursivement (sous-dossiers) | `_s3_ls_recursive(dir)` |

Si aucun ne convient, ajouter un helper minimal dans `extractors.py` à la suite de ceux existants (~ligne 65-78).

## Edit 1 (optionnel) — Helper S3 dans extractors.py

Template d'un nouveau helper (après les helpers existants) :
```python
def _s3_<verb>(<args>) -> Optional[<type>]:
    """<docstring>."""
    s = str(<path>)
    if not s.startswith(_NFS_PREFIX):
        return None
    key = s[len(_NFS_PREFIX):]<.rstrip('/')+'/' si listing>
    try:
        result = subprocess.run(
            ["aws", "s3", "<cmd>", "...", f"s3://{_S3_BUCKET}/{key}", "--profile", _S3_PROFILE],
            capture_output=True, text=True, timeout=<10|30>,
        )
        return ... if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, OSError):
        return None
```

⚠ Timeout : 10s pour lecture/exists, 30s pour listing récursif.

## Edit 2 — Import dans checkers.py

Ligne 10, ajouter le helper si nouveau :
```python
from .extractors import (..., _s3_exists, _s3_ls_count, _s3_ls_lines, _s3_ls_recursive, _s3_read_text)
```

## Edit 3 — Méthode `check_<col>` dans BaseChecker

Position : à la suite des autres `check_*()` (~ligne 213-260). Insérer juste après une méthode de la même famille (check_read_start_time, check_ancestry, etc.).

### Signature standard

```python
def check_<col>(self, sample_dir: Path, sample: str) -> str:
    """<docstring 1 ligne>."""
    # logique
    return "OK" | "KO" | "NA" | "<valeur>"
```

### Signature avec preserve (Q7 = preserve)

```python
def check_<col>(self, sample_dir: Path, sample: str) -> Optional[str]:
    """<docstring>. None si erreur S3 (preserve la valeur en DB)."""
    result = _s3_<helper>(...)
    if result is None:
        return None  # signal preserve
    # logique
    return "OK" | "KO"
```

### Templates par source (Q4)

**Source = fichier S3 (lecture)** :
```python
def check_<col>(self, sample_dir: Path, sample: str) -> str:
    tsv = sample_dir / "<subfolder>" / f"{sample}.<suffix>.tsv"
    content = _s3_read_text(tsv)
    if content is None and tsv.exists():
        try:
            content = tsv.read_text(encoding="utf-8")
        except IOError:
            return "NA"
    if not content:
        return "NA"
    # parse content...
    return result
```

**Source = présence S3 (1 fichier)** :
```python
def check_<col>(self, sample_dir: Path, sample: str) -> str:
    return self._ok_ko(
        self._exists(sample_dir / "<subfolder>" / f"{sample}.<suffix>")
    )
```

**Source = listing S3 récursif (plusieurs dossiers)** :
```python
def check_<col>(self, sample_dir: Path, sample: str) -> Optional[str]:
    target_sd = Path(str(sample_dir).replace("/<base>/", "/<other>/"))  # si bucket différent
    lines = _s3_ls_recursive(target_sd)
    if lines is None:
        return None
    sample_prefix = f"processed/MRD/RetD/{self.config.sample_type}/{self.config.labo}/{sample}/"
    seen = set()
    for line in lines:
        parts = line.split(maxsplit=3)
        if len(parts) < 4:
            continue
        try:
            size = int(parts[2])
        except ValueError:
            continue
        if size == 0:
            continue
        key = parts[3]
        if not key.startswith(sample_prefix):
            continue
        relative = key[len(sample_prefix):]
        if "/" not in relative:
            continue
        seen.add(relative.split("/", 1)[0])
    required = {<set des dossiers attendus>}
    return "OK" if required.issubset(seen) else "KO"
```

⚠ **Gotcha** : `aws s3 ls --recursive` retourne les clés S3 COMPLÈTES, pas relatives. Toujours stripper via `sample_prefix`. Voir [gotchas/critical-pitfalls.md](../gotchas/critical-pitfalls.md).

## Edit 4 — Câblage dans check_sample()

### LiquidChecker (Q5 = liquid ou both)

Dans `LiquidChecker.check_sample()` (~ligne 464-586), ajouter une entrée dans le dict `result.data` :

```python
"<Header Gsheet>": self.check_<col>(sd, sample),
```

Position recommandée : juste après une méthode de la même famille thématique.

### SolidChecker (Q5 = solid ou both)

Dans `SolidChecker.check_sample()` (~ligne 596-700), même chose.

### Fallback dict (sample n'existe pas)

⚠ **Critique** : si on oublie, KeyError au runtime quand un sample est en DB mais pas sur le filesystem.

Dans le bloc `if not self.sample_exists(sample):` (~ligne 480-518 liquid, équivalent solid), ajouter :

```python
"<Header Gsheet>": "<default>",   # ex: "KO" pour status, "NA" pour info
```

## Vérification (test direct, sans toucher la DB)

```python
# Choisir 2 samples connus : 1 OK + 1 KO
python3 -c "
from lib.utils import get_config
from lib.checkers import LiquidChecker
cfg = get_config('liquid', 'CGFL')
ck = LiquidChecker(cfg)
print('OK expected:', ck.check_<col>(cfg.base_dir / '<sample_ok>', '<sample_ok>'))
print('KO expected:', ck.check_<col>(cfg.base_dir / '<sample_ko>', '<sample_ko>'))
"
```

Résultats attendus : `OK` et `KO` (ou les valeurs définies en Q6).

## STOP — Validation Boris

```
✅ Étape B — check_<col>() validée
- Helper S3 utilisé : <_s3_helper>
- Méthode ajoutée dans BaseChecker
- Câblée dans LiquidChecker.check_sample() [+ SolidChecker]
- Fallback dict mis à jour
- Test 2 samples : <sample_ok>=OK, <sample_ko>=KO

OK pour Étape C (update-column) ?
```
