---
name: check-consistency
description: Verification coherence trace-prod vs S3 vs outputs Bam2Beta. Detecte orphelins, samples manquants, outputs incomplets. Use when the user says "check", "consistency", "coherence", "verification", "orphelins", or wants to audit data integrity.
argument-hint: "<liquid|solid> <CGFL|HCL> [--deep]"
allowed-tools: Bash(python3*), Bash(cd*), Bash(aws*), Bash(duckdb*), Read
---

# Check Consistency

Verifie la coherence des donnees entre trace-prod (DuckDB), S3 (Scaleway), et les outputs Bam2Beta. Detecte les orphelins, les samples manquants, et les incompletudes.

## Regles absolues

- **JAMAIS supprimer de fichiers S3.** Read-only. On detecte et on rapporte, c'est tout.
- Combinaisons type/labo valides : `liquid`x`CGFL`, `liquid`x`HCL`, `solid`x`CGFL`.
- Si l'utilisateur demande `solid`x`HCL`, signaler que cette combinaison n'existe pas.

## Arguments

| Argument | Requis | Description |
|----------|--------|-------------|
| `type` | oui | `liquid` ou `solid` |
| `labo` | oui | `CGFL` ou `HCL` |
| `--deep` | non | Verifications supplementaires (version Dorado, taille BAM) |

## Chemins et outils

- **DuckDB** : `~/Pipeline/trace-prod/database/samples_status.duckdb`
- **CLI trace-prod** : `python3 ~/Pipeline/trace-prod/database/check_samples.py query "SQL"`
- **S3 (profil scw)** :
  - BAM merged : `s3://aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample}/BAM/`
  - bedMethyl : `s3://aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample}/BETA/`
  - POD5 : `s3://aima-pod-data/data/{labo}/{type}/{sample}/`

## Procedure

### Etape 1 — Lister les samples trace-prod

Requeter la base DuckDB pour obtenir tous les samples du type et labo demandes :

```bash
python3 ~/Pipeline/trace-prod/database/check_samples.py query \
  "SELECT sample_id, status, dorado_version FROM samples WHERE type='${TYPE}' AND labo='${LABO}' ORDER BY sample_id"
```

Stocker la liste des sample_id et leur statut.

### Etape 2 — Lister les samples sur S3

Lister les dossiers presents dans le chemin S3 BAM merged :

```bash
aws s3 ls s3://aima-bam-data/processed/MRD/RetD/${TYPE}/${LABO}/ --profile scw | grep PRE | awk '{print $2}' | sed 's/\/$//'
```

Stocker la liste des sample_id trouves sur S3.

### Etape 3 — Comparer les listes

- **Orphelins trace-prod** : samples dans la DB mais absents de S3. Probable cause : pipeline en cours, echec, ou nettoyage premature.
- **Orphelins S3** : samples sur S3 mais absents de la DB. Probable cause : sample non enregistre, migration incomplete, ou test.

### Etape 4 — Verifier la completude des outputs

Pour chaque sample commun (present dans DB ET sur S3), verifier la presence de :

```bash
# BAM
aws s3 ls s3://aima-bam-data/processed/MRD/RetD/${TYPE}/${LABO}/${SAMPLE}/BAM/ --profile scw

# bedMethyl
aws s3 ls s3://aima-bam-data/processed/MRD/RetD/${TYPE}/${LABO}/${SAMPLE}/BETA/ --profile scw
```

Outputs attendus par sample :
- `BAM/` : au moins 1 fichier `.bam` + `.bam.bai`
- `BETA/` : au moins 1 fichier bedMethyl

Signaler tout sample avec des outputs manquants.

### Etape 5 (optionnel, --deep) — Verifications approfondies

Si `--deep` est demande :

1. **Version Dorado** : comparer la version dans trace-prod avec les metadonnees du BAM header si disponible. Signaler les incoherences.
2. **Taille BAM** : verifier que les fichiers BAM ont une taille raisonnable (> 100 MB pour liquid, > 500 MB pour solid). Signaler les fichiers anormalement petits.

```bash
aws s3 ls s3://aima-bam-data/processed/MRD/RetD/${TYPE}/${LABO}/${SAMPLE}/BAM/ --profile scw --human-readable
```

## Format de sortie

```
## Verification coherence : {type} {labo}

### Resume
- trace-prod : {n} samples | S3 BAM : {m} samples | Communs : {k}

### Orphelins trace-prod (dans DB mais pas sur S3)
- {sample_id} — statut DB : {status} — {raison probable}

### Orphelins S3 (sur S3 mais pas dans DB)
- {sample_id} — action recommandee : enregistrer dans trace-prod ou investiguer

### Outputs incomplets
- {sample_id} : manque {BAM|bedMethyl}

### Tout OK
- {n} samples avec BAM present
- {n} samples avec bedMethyl present
- Aucun orphelin detecte (si applicable)
```

Si `--deep` :
```
### Verifications approfondies
- Versions Dorado : {coherent|incoherences detectees}
- Tailles BAM : {toutes raisonnables|anomalies detectees}
  - {sample_id} : {taille} (attendu > {seuil})
```

## Exemples d'utilisation

- `/check-consistency liquid CGFL` — verification standard liquid CGFL
- `/check-consistency solid CGFL --deep` — verification approfondie solid CGFL
- `/check-consistency liquid HCL` — verification standard liquid HCL
