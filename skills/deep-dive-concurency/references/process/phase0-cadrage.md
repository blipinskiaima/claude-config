# Phase 0 — Cadrage et prérequis

## 1. Charger le référentiel AIMA — non négociable

```bash
cat ~/Pipeline/Aima-Survey/docs/AIMA-POSITIONING.md
```

Sans cette fiche, la comparaison sera approximative et différente d'une analyse à l'autre.
Si elle manque ou paraît obsolète, le signaler à Boris **avant** de continuer.

## 2. Déterminer la ligne de produit concernée

AIMA a **deux lignes**, avec des concurrents disjoints :

| Ligne AIMA | Score | Concurrents directs |
|---|---|---|
| **MRD** | mVAF v1.4 | Natera Signatera, Guardant Reveal, DELFI-TF |
| **MCED** | THEMELIO 1.0.0 | GRAIL Galleri, Exact Cancerguard, Guardant Shield MCD |

⚠ Beaucoup de sociétés ne s'opposent frontalement à **aucune** des deux. DELFI/FirstLook fait
du **triage mono-cancer vers l'imagerie** : c'est un repère technologique sur la fragmentomique,
pas un concurrent direct du MCED. Le dire explicitement dans le rapport évite une comparaison
faussée dès le départ.

Si la ligne est ambiguë, demander à Boris plutôt que de deviner.

## 3. Vérifier les prérequis outils

```bash
command -v pdftotext pdftoppm || echo "poppler-utils ABSENT"
```

`poppler-utils` n'est **pas installé** sur le serveur (état connu au 2026-07-22). Sans lui :
- l'outil de lecture PDF natif ne peut pas rendre les pages,
- `pdftotext` est indisponible.

Contournement éprouvé — venv jetable (`pip install` direct est bloqué par PEP 668) :

```bash
python3 -m venv /tmp/.venv-pdf && /tmp/.venv-pdf/bin/pip install -q pypdf weasyprint markdown
```

Recommander à Boris `sudo apt-get install -y poppler-utils` s'il n'a jamais été installé.

## 4. Lire la fiche concurrent existante

```bash
python3 -c "
import json; d=json.load(open('/home/blipinski/Pipeline/Aima-Survey/data/competitors.json'))
for tier,items in d.items():
    if isinstance(items,list):
        for c in items:
            if 'NOM_CIBLE'.lower() in json.dumps(c).lower(): print(tier, json.dumps(c, indent=2, ensure_ascii=False))
"
```

Champs de la fiche : `name`, `aliases`, `hq`, `founded`, `tech`, `product`, `stage`, `cancers`,
`threat`, `threat_reason`, `url`, `include_in_query_b`.

Si la société est absente, ce sera une création en phase 6.

## 5. Vérifier ce que la veille a déjà capté

```bash
cd ~/Pipeline/Aima-Survey && python3 -c "
import duckdb
con=duckdb.connect('data/aima_survey.duckdb', read_only=True)
print(con.execute('''SELECT external_id, pub_date, score, org_name, substr(title,1,70)
  FROM articles WHERE lower(COALESCE(affiliations,'')||COALESCE(org_name,'')||COALESCE(title,''))
  LIKE '%NOM_CIBLE%' ORDER BY pub_date DESC''').fetchall())
"
```

⚠ Ouvrir la DB en **read-only** (le cron de 8h00 écrit dedans).

## Sortie de phase

Un court cadrage écrit : cible, produit, ligne AIMA opposée (ou aucune), inputs disponibles,
présence dans `competitors.json`, nombre d'articles déjà en base.
