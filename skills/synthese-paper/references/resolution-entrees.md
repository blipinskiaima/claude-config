# Résolution des entrées

Le script accepte quatre formes. La détection est automatique (`detect_kind`).

| Entrée | Détection | Traitement |
|---|---|---|
| **PMID** | 6 à 9 chiffres | `efetch` PubMed direct |
| **DOI** | commence par `10.` ou contient `doi.org/` | `esearch` `{doi}[DOI]` → PMID → `efetch` |
| **URL PubMed** | contient `pubmed.ncbi.nlm.nih.gov/{id}` | extraction du PMID par regex |
| **Autre URL** | commence par `http` | tentative d'extraction d'un DOI, sinon échec explicite |
| **PDF** | chemin de fichier existant | extraction locale via `pypdf` |

## Chemin PubMed (préféré)

C'est le cas fidèle : les métadonnées sont complètes et identiques à celles de la veille
(titre, résumé multi-sections avec labels, auteurs formatés `Nom Prénom` limités à 3 + « et al. »,
journal, date).

Utiliser `NCBI_API_KEY` s'il est présent dans l'environnement (limite de débit plus haute) :

```bash
set -a; . ~/Pipeline/Aima-Survey/.env; set +a
```

## Chemin PDF (dégradé)

Un PDF n'a pas de métadonnées structurées. Le script fait au mieux :

- **titre** : ligne la plus longue parmi les 15 premières de la page 1 — heuristique, souvent
  correcte, parfois non
- **résumé** : bloc suivant le mot « abstract », borné à l'introduction ou aux mots-clés
- **auteurs / journal / date** : `non précisé` — le prompt sait gérer ce cas
- **DOI** : extrait par regex s'il est présent, sert d'identifiant à la place du PMID

⚠ **Si un DOI est trouvé dans le PDF, préférer relancer avec ce DOI** : on récupère alors les
vraies métadonnées PubMed et la synthèse est bien meilleure.

PDF scanné sans couche texte → le script s'arrête et invite à fournir le DOI.

## Enrichissement par la veille

Après résolution, le script interroge `~/Pipeline/Aima-Survey/data/aima_survey.duckdb`
(**en lecture seule** — le cron écrit à 8h00) pour récupérer les vraies `priority` et
`queries_matched` de l'article.

- Article **déjà dans la veille** → priorité et rubriques réelles, exactement comme Tower
- Article **inconnu** → `priorité = non classé`, `rubriques = hors veille`

Le score IA est affiché en information s'il existe.

C'est ce qui rend la synthèse cohérente avec ce qu'afficherait Tower pour un article déjà suivi.

## Dépendances

`requests`, `duckdb` (présents dans l'environnement Aima-Survey), et `pypdf` pour le cas PDF
uniquement. Si `pypdf` manque, créer un venv jetable :

```bash
python3 -m venv /tmp/.venv-pdf && /tmp/.venv-pdf/bin/pip install -q pypdf
```

`pip install` direct est bloqué par PEP 668 sur ce serveur.
