---
name: create-rapport-prod
description: Generate the AIMA platform production report (16:9 slide-style PDF, French) for the PROD Bam2Beta runs of the day, or of a given date range, from trace-platform and Aima-Tower data. Checks first that trace-platform is up to date with S3, then builds the PDF, copies it to Bam2Beta/docs and shows the preview. Use when the user says "create-rapport-prod", "rapport de prod", "rapport de production", "rapport du jour", "rapport plateforme", "rapport des runs de la semaine", or asks for the CEO production report of one or several days.
---

<objective>
Reproduire à l'identique le rapport de production construit le 2026-10-01 (6 runs IRCCS RC24) pour les runs
PROD d'une période : par défaut le jour d'exécution (UTC), ou `--du / --au` si l'utilisateur précise des jours
ou des semaines. Sortie : un PDF diaporama (page de garde, frises de parcours, exécution, QC, résultats).
Aucun calcul de métrique : tout vient de trace-platform (lecture) et de l'API indicator d'Aima-Tower.
</objective>

<workflow>

## Étape 1 : Période

- Sans précision : le jour courant (UTC, la machine est en `Etc/UTC`).
- « hier », « cette semaine », « du X au Y », « les 2 dernières semaines » → convertir en `--du AAAA-MM-JJ --au AAAA-MM-JJ`.
- Un client précis demandé → ajouter `--client <UUID>` (le retrouver dans `labs_users`).
- Annoncer en une ligne la période retenue, puis enchaîner sans attendre.

## Étape 2 : Fraîcheur de la base (lecture seule, OBLIGATOIRE)

```bash
cd ~/Pipeline/trace-platform && python3 rapports/verifier_fraicheur.py --du D --au A [--client UUID]
```

| État | Action |
|---|---|
| tout `A JOUR` | passer à l'étape 4 |
| `EN COURS` | runs pas terminés : le dire, proposer d'attendre (surveillance en arrière-plan) ou de générer sans eux |
| `ABSENT` / `EN RETARD` | **lister les samples et DEMANDER l'accord** avant l'étape 3 |
| `⚠ results/` | le signaler (livrable ancien, manquant, ou `status=FAILED_QC_*`) ; voir pièges |

## Étape 3 : Re-check ciblé (seulement après accord explicite)

```bash
python3 rapports/recheck_cible.py CLIENT/PATIENT/SAMPLE ...   # backup auto puis re-check par clé exacte
python3 check_platform.py export --gsheet
```
Relancer `verifier_fraicheur.py` : tout doit être `A JOUR` avant de continuer.

## Étape 4 : Génération

```bash
python3 rapports/rapport_plateforme.py --du D --au A [--client UUID]
```
Sortie : `rapports/sortie/rapport_plateforme_<periode>_<labs>.pdf` (le script imprime le chemin).

## Étape 5 : Vérification visuelle

Rendre les pages (`pdftoppm -r 60 -png <pdf> <prefixe>`) et les regarder. Contrôler : aucun texte qui déborde
ou chevauche, frises une par ligne, N.B. lisibles, aucun « None ». Ne jamais valider un en-tête par `pdftotext |
grep` : les en-têtes espacés lettre à lettre ne sont pas retrouvés (voir pièges).

## Étape 6 : Livraison

1. Copier dans `~/Pipeline/Bam2Beta/docs/` (même nom ; écraser seulement un rapport de ce skill), puis `cmp`.
2. Afficher le PDF dans le panneau de droite : `SendUserFile` avec `display: "render"`.
3. Résumer en 3-5 lignes : période, nb d'analyses / patients / rapports, statuts run et QC avec leur raison.

| Besoin | Référence |
|---|---|
| Rejouer pas à pas la session d'origine, cas particuliers | [references/process/etapes-session.md](references/process/etapes-session.md) |
| Contenu attendu de chaque diapositive, sources, conventions | [references/rapport/contenu.md](references/rapport/contenu.md) |
| Pièges rencontrés et parades | [references/process/pieges.md](references/process/pieges.md) |

</workflow>

<quick_reference>

| Élément | Valeur |
|---|---|
| Scripts | `~/Pipeline/trace-platform/rapports/{verifier_fraicheur,recheck_cible,rapport_plateforme}.py` |
| Sélection | case effectif `PROD`, `CAST(pipeline_start_date AS DATE)` dans la période, tests internes DEV exclus |
| Durées | API Tower `http://172.18.0.2:8050/api/indicator/data` (champs `min_*`), jamais recalculées |
| Rendu | Chromium headless Playwright, `--no-sandbox` obligatoire sur ce serveur |
| Charte | PDF « 2027 Path » (Bam2Beta) + frises `Flux.tsx` de la Tower ; Nimbus Sans, marine `25254E`, rouge `E62448` |
| Écritures | base modifiée UNIQUEMENT par `recheck_cible.py`, après accord ; S3 jamais modifié |

</quick_reference>
