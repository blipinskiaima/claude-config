# Aima Tower — Auto Memory

## Page `/exploration` — toggle Score mVAF v1 / v1.4 (2026-07-03)
Sélecteur **Score** (sidebar) pilotant toute la page (tables Sens/Spé + graphes) via param `score_source` (`mvaf_v1` défaut = `qc_metrics` float / `mvaf_v14` = `retd_suivis` VARCHAR virgule FR, `KO` exclu de la cohorte). Swap dans `_prepare_base_dataset` AVANT filtre `score.notna`, threadé comme `dorado_version` (caches + 11 méthodes + `ExplorationFilters`). **Bug pré-existant corrigé** : 4 endpoints graphes (qc-data/mvaf-dotplot/methylation-vaf/bladder) plantaient (mauvais passage d'args) → refonctionnels. Validé live : v1 78.5%/88.4%, v1.4 81.7%/85.3%. Détails : [exploration_score_source_toggle.md](exploration_score_source_toggle.md)

## Page `/combined` — onglet Suspects (2026-06-25)
4ᵉ onglet Résultat : dotplot des **25 imageries suspectes** (`scores.csv` unité `suspect`) scorées par le combo sélectionné + ligne de seuil + compteur N au-dessus. **Sans vérité-terrain** (`label` NULL) → **ni sensibilité ni spécificité**, seulement `n_above/n_total`. Seuil = `quantile_type1` healthy train, avec garde `float(label)` pour que les lignes sans vérité n'entrent pas dans la calibration. Backend `dilution_service.get_suspect_scores` + `/api/combined/suspect` ; front `useCombinedSuspect` (lazy) + `SuspectChart` (jitter Weyl déterministe, **pas** `Math.random`). 4 tests verts. Détails : [combined_suspect_tab.md](combined_suspect_tab.md)

## Scission `/database` + ID sample Monitoring (2026-06-24)
Page `/database` à onglets **scindée en 2 pages autonomes** : **R&D** (`/database`, ex-onglet R&D, `Database.tsx` nettoyé des onglets) + **Plateforme** (`/database-platform`, nouveau `DatabasePlatform.tsx` qui wrappe `PlatformView`). 2 entrées sidebar (groupe monitoring) labels **"R&D"** (FlaskConical) / **"Plateforme"** (Building2), sans le mot "Database". `SamplesView`/`PlatformView` étaient déjà des composants autonomes → simple wrapping, **0 backend** (endpoints `/api/databases/*` R&D et `/api/databases/platform/*` déjà séparés). Route ajoutée dans `App.tsx` (branche `path="*"`, max-w 1280). Pas de redirection. — Monitoring › Récents : **ID sample affiché à droite** de `CompletedRow`, source = **`--patient_id` parsé dans `wf.command_line`** (regex `--patient_id[=\s]+(\S+)`, `—` si absent) — choix Boris : command line Nextflow, **pas** `params_json` (3 vieux workflows sans command_line → `—`). Titres h1 de page gardent "Database R&D"/"Database Plateforme" (seuls les labels sidebar sont raccourcis).

## Page `/combined` (ex-exploration-beta) — refonte + onglet Dilution (2026-06-22)
`/exploration-beta` renommée `/combined` (fichiers/route/endpoints, commit `0fb9357`). Panneaux Cohorte retirés, défaut SpeedVac (`std_522`), Résultat en onglets (Initial/Lung-DI/**Dilution**, + Suspects ajouté le 2026-06-25), sélecteurs d'éval (Profondeur/Spécificité/Unité) regroupés à gauche. **Onglet Dilution** : courbes Twist pilotées par le combo sélectionné via **source unique** `scores.csv` (unité d'éval `dilution` générée côté pipeline Feature = archi α, Tower reste reader) ; lookup colonne = `features.replace(",","+")` ; marche mono ET multi-features XGBoost. Page `/dilution` autonome **supprimée**. Détails : [combined_dilution_tab.md](combined_dilution_tab.md)

## Page `/combined` — intégration pipeline Feature (2026-06-09, renommée depuis `/exploration-beta` le 2026-06-22)
Tower lit (read-only) les résultats du pipeline `~/Pipeline/Feature` : sélection de features → CSV sensibilité stratifiée (ligne Combined colorée vert/rouge vs baseline mVAF) + best combos. **Affichage seul** : aucune exécution depuis le conteneur (pas de R, mount `/pipeline:ro`) ; même `feature_db.py best_combo` répliqué en SQL read-only (son `connect()` ouvre la DB en write → KO sur `:ro`). Clé canonique `normalize_features` copiée du pipeline (ordre de sélection indifférent). Endpoints `/api/combined/{result,best-combos,dilution}` (cohort-info retiré, png→410). MAJ DB → pas de restart (bind-mount live). Détails : [feature_pipeline_integration.md](feature_pipeline_integration.md) + [combined_dilution_tab.md](combined_dilution_tab.md)

## Feature `/samples` + `/sample/:id` — Tower v4.2.0 (2026-05-13)
Deux nouvelles pages : liste tous les samples R&D + détail enrichi 1-sample reproduisant le mockup `aima-tower-sample-detail.html`. Backend `DatabaseService.get_sample_detail()` JOIN 5 tables. Animation `aima-rise` cascade appliquée sur toutes les pages via `key={location.pathname}`. Décisions clés : TF=mvaf_v1, NEGATIVE/POSITIVE strict (==0/>0), depth threshold 0.25×, paths trace-prod `s3://aima-bam-data/processed/MRD/RetD/{type}/{labo}/{sample}/{REPORT|LOG}/`. Détails : [feature_sample_detail.md](feature_sample_detail.md)

## Spec ciblée vs Spec réalisée
Slider `target_specificity` = ce qu'on demande. `Spec_AI` du tableau = ce qu'on obtient (= `nb_healthy_below_threshold / nb_healthy_total`). Diverge à cause de la quantification (seuil discret sur N healthy fini). Détails : [spec_ciblee_vs_realisee.md](spec_ciblee_vs_realisee.md)

## Tower v3.0.0 en prod (2026-05-07) — refonte UI complète
Stack : FastAPI + Vite + React + Tailwind v4 (remplace Dash). Un seul worktree = `~/Pipeline/Aima-Tower/` sur `main`. Parachute rollback = tag `v2.3.0` (Dash mono-stack). Plan C et Plan G nettoyés (worktrees + branches supprimés le 2026-05-11). Détails : [project_v3_cutover.md](project_v3_cutover.md)

## Todo list — routing par section
Todo list `~/.claude/projects/-home-blipinski/memory/todo-optimisation.md` a 4 parties : À faire / En cours / Complété / Stand-by. Afficher UNIQUEMENT la partie demandée, pas le fichier complet. Détails : [feedback_todo_sections.md](feedback_todo_sections.md)

## Docker compose Tower — project name figé à `aima-tower`
Le compose contient `name: aima-tower` (override). Sans ça compose dérive du dossier et taggue une image fantôme distincte des containers historiques. Permet de renommer le worktree sans casser les volumes/réseaux nommés. Détails : [feedback_compose_project_name.md](feedback_compose_project_name.md)

## DuckDB Cross-DB Join Pattern

Quand on doit joindre deux bases DuckDB read-only (ex: platform + trace-workflow), `_query()` ne peut pas ATTACH (connexion read-only). Solution : connexion in-memory avec ATTACH des deux bases :
```python
conn = duckdb.connect(":memory:")
conn.execute(f"ATTACH '{db1}' AS pl (READ_ONLY)")
conn.execute(f"ATTACH '{db2}' AS wf (READ_ONLY)")
# Utiliser pl.table et wf.table dans la requete
```
Voir `PlatformService.get_samples_overview()` pour l'implementation complete.
Details : [duckdb-patterns.md](duckdb-patterns.md)

## Liens Scaleway désactivés (2026-06-12)

Tous les liens cliquables vers la console Scaleway ont été retirés (commit `5744647`, tag rollback `pre-disable-scaleway`). Les chemins S3 restent affichés en **texte non cliquable** (`<code>`) sur `/database›Platform`, `/monitoring`, `/sample/:id` (bouton « Exporter rapport » supprimé). Helpers `s3ToScaleway` (front) et `_s3_to_scaleway` (Dash legacy `callbacks.py`) **supprimés** — ne plus s'y référer. Décision Boris : garder le chemin, retirer la navigation web Scaleway.

## Platform Detail Panel (Database > Platform)

- Layout : Donnees (lg=8) gauche, Trace (lg=4) droite
- Input/Output : liens cliquables vers console Scaleway (classe `detail-value-path`)
- Rapport : lien Click vers `{input_path}/results/`
- Log : lien Click vers `{output_path}/{sample_name}/LOG/`
- Police paths : `0.75rem` (plus petit que le reste)

## Gotcha: Python Closures in Loops

Definir les fonctions helper AVANT leur premier appel dans la boucle. UnboundLocalError si defini apres (Python voit l'assignation dans le scope et considere la variable locale).

## Docker Workflow

Rebuild rapide : `docker compose down && docker compose build && docker compose up -d`
Restart sans rebuild (si seul CSS change dans assets/) : `docker compose restart`
Note : `COPY src/` dans Dockerfile invalide le cache a chaque modif src/.

## Page Survey — patterns

Parser extensible, lazy tabs, state atomique, scoring IA découplé, persistence session. Tous les patterns réutilisables consolidés dans [survey_patterns.md](survey_patterns.md).

## Intégration DuckDB Aima-Survey (v6 — 2026-04-20)

Vues `month` et `all` lisent `~/Pipeline/Aima-Survey/data/aima_survey.duckdb` en READ_ONLY (retry backoff), fallback markdown si DB KO. Day/week inchangés. Traduction `queries_matched` (names) → `categories` (descriptions humaines) via `queries.json`. Détails : [survey_duckdb_integration.md](survey_duckdb_integration.md)

## Sécurité Tower (2026-04-21)

Tower accessible via `https://tower.aima-diagnostics.com` (Caddy reverse proxy + basic auth bcrypt + Let's Encrypt). Port 8050 non exposé à Internet. Password dans gestionnaire de mdp AIMA. Détails : [security_setup.md](security_setup.md)

## Sécurité — approche pragmatique

Boris valide le scope discipline en sécu : couches par iteration (Caddy d'abord, Security Group plus tard). Détails : [feedback_security_pragmatism.md](feedback_security_pragmatism.md)

## Incident `.env` tracked dans git

`.env` était tracked dans git jusqu'au 2026-04-21 (repo privé). Retiré via `git rm --cached`. Rotation secrets Anthropic/Seqera **reportée** (repo privé, Boris seul dev). Détails : [project_env_leak.md](project_env_leak.md)

## Backend IA via CLI `claude -p` (2026-04-22)

Tous les appels IA Tower (Survey synthese, Analytics chat, DB Q&A) passent par `src/claude_cli.py` subprocess `claude -p` + `CLAUDE_CODE_OAUTH_TOKEN` (abonnement Max au lieu credits API). `ANTHROPIC_API_KEY` **retire** du container (priorite CLI bypasse OAuth). HOME isole `/app/data/claude-home`. Contexte injecte = 14 CLAUDE.md Pipeline (~20K tokens). Détails : [ia_cli_migration.md](ia_cli_migration.md)

## Vues temporelles Survey pilotees par `first_seen_at` (2026-04-22)

Depuis backfill EDAT Aima-Survey, toutes les vues (Day/Week/Month/Year/All) filtrent sur `first_seen_at` = EDAT PubMed (stable, immuable, non-future). Plus de pub_date. Card UI affiche les 2 dates distinctes ("Indexé : ... • Publié : ..."). Vue Jour migree DuckDB avec `DATE(first_seen_at) = ?` + selecteur conditionnel. Détails : [survey_first_seen_at.md](survey_first_seen_at.md)

## Onglet Concurrence Survey étendu

`is_competitor_article(a)` matche desormais `a.org_name` OR `a.last_author_affiliation` contre `competitors.json` (23 entreprises tier_1/2/3 avec aliases). +IMBdx ajoute comme tier_2 MOYENNE. Passe de 11 a 29 articles concurrents. Reclassification Haiku ciblee en cours (script `reclassify_competitors.py` cote Aima-Survey).

## Guardant Health — stratégie Europe (2026-04-23)

Snapshot : Guardant360 CDx seul IVDR-certifié (mai 2024). Reveal MRD = LDT via labs hospitaliers (VHIO, Royal Marsden, Gemelli) — **aucun partenariat France**. Shield MCED **absent Europe**, priorité Asie 2026 (Manulife). Signatera devance Guardant sur CRC France (CIRCULATE-PRODIGE-70). Fenêtres AIMA : MCED CRC sanguin méthylation + MRD CRC France via UNICANCER/CLCC. IVDR classe C se ferme 2028. Détails : [competitors_guardant_europe.md](competitors_guardant_europe.md)

## Sens_Active redéfini = cancer_truth (2026-05-11, demande Michael)
Tableau Sensibilité stratifiée VAF colonne "Cancer actif" utilise `cancer_truth` (mutated OR active_cancer) au lieu de `active_cancer_flag` strict. Diverge volontairement du pipeline R. Détails : [project_sens_active_cancer_truth.md](project_sens_active_cancer_truth.md)

## Refonte Exploration v2.3 (2026-04-30)

Tower ≡ R main cell-by-cell validé (target=0.85+0.90, mode=ge5). 2 cohortes distinctes par sub-tab : Sens/Spé (cancer+healthy strict, R02) vs Graphique (tous samples filtrés, R04). Pattern "tout sélectionné = no-op" via `_legacy_set_or_none` / `_active_cancer_param`. Onglet Avancé reuse `build_boxplot()`. TNE/Nuclear et Healthy carve-out asymétriques (tableaux only). Détails : [exploration_v2_3_design.md](exploration_v2_3_design.md)

## Dash 4.1+ gotchas Tower

`allow_direct_input=False` requis sur sliders (sinon input numérique éditable). Persistence ID bumping (`persistence="v2-key"`) pour invalider le cache navigateur. Composants conditionnels → utiliser `dcc.Store` relais. Imports tardifs pour éviter cycles. Détails : [dash_4_gotchas.md](dash_4_gotchas.md)

## Cascade cohorte /exploration — intégrée v3.0.0 (2026-05-07)

Backend `compute_cohort_cascade()` `@lru_cache(64)` + endpoint `/api/exploration/cohort-cascade`. Frontend `useCohortCascade` TanStack Query (lazy `enabled` au premier open) + `useDebouncedValue(250ms)` pour les sliders. Détails : [feature_cohort_cascade_integration.md](feature_cohort_cascade_integration.md)

## UI Tower v3 — multi-utilisateurs (2026-05-07)

Tower n'est plus un dashboard perso : retrait des références "Boris" / "Plan G" / branche `feat/ui-refresh-g` / "Internal · v3 preview" dans Sidebar + Home + Exploration. Thème **light par défaut** (fallback `getStoredTheme` → `"light"` au lieu de `"system"`, `theme-preference` localStorage préservé pour les users qui ont déjà choisi). Toggle dark/system reste dispo dans la sidebar.
