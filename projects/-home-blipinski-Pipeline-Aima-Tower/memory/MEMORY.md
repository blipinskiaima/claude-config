# Aima Tower — Auto Memory

> Index. Une entrée = un titre, le piège qui évite une erreur, et le lien vers le détail.
> La narration vit dans les topic files, jamais ici — sinon l'index dépasse la limite de
> chargement (~24 Ko) et ses dernières entrées cessent d'être lues.

## `/qara` — comparaison au point figé (2026-09-11, v5.7.0)
Toggle → seconde rangée mesurée sur trace-prod. Alignement **structurel** : la carte dynamique réutilise le composant `Kpi` et itère sur `p.kpis`. ⚠ **Seul Exis est comparable.** Themelio ET CUP scorent avec un **modèle déployé** là où le doc publie de l'**out-of-fold** — CUP sort 3 classes à 100 % exactement, et son **top-1 masque la fuite** (−1,3 pt) pendant que la balanced monte de 8,4. ⚠ `sample_name` n'est pas unique (1531/1456) : joindre par `unique_id`. [qara_comparaison_dynamique.md](qara_comparaison_dynamique.md)

## `/qara` — refonte du rendu pour un lecteur externe (2026-09-10)
Vue d'ensemble, bandeaux, toggle EN/FR **limité à l'habillage** (les libellés du document restent en anglais dans les deux langues). ⚠ **`qara-ui.ts` ne contient aucun littéral numérique.** ⚠ Un chiffre phare ne s'affiche jamais sans dénominateur ni périmètre → CUP sans fraction. Numéros de section et références au document **masqués sur demande**. [qara_refonte_vitrine.md](qara_refonte_vitrine.md)

## Charte graphique du site appliquée à la Tour (2026-09-10, v5.6.0)
Couche de tokens + **alias** : les 193 classes Tailwind suivent sans éditer les composants. ⚠ **Un alias ne porte pas le sens de la couleur remplacée** — violet → magenta a fait passer deux bonnes valeurs pour des alertes. ⚠ Plotly ne lit ni les custom properties ni `color-mix()` → `lib/tokens.ts`. [charte_site_tokens.md](charte_site_tokens.md)

## Migration trace-prod v34 — colonnes reads (2026-09-10)
`nb_reads_total` → **`nb_lignes_total`**, `nb_reads_aligned` → **`nb_molecule`** (⚠ ne pas confondre). Deux propagations **silencieuses** : `SELECT q.*` de `get_sample_detail()` et le `continue` de `_apply_dynamic_filters`. À re-vérifier à chaque migration. [migration_v34_colonnes_reads.md](migration_v34_colonnes_reads.md)

## 5 endpoints /api/exploration cassés — préexistants (2026-09-10)
`scores`, `bladder`, `qc-data`, `mvaf-dotplot`, `filtered-dataset` en 500 **avant** la migration v34. Méthode de preuve réutilisable : reconstituer l'état d'avant sur une copie de base. ⚠ Comparer les lignes **positionnellement**, pas par `sample_name`. [endpoints_exploration_casses_preexistants.md](endpoints_exploration_casses_preexistants.md)

## `/analytics` — règle run-level dans les prompts (2026-09-08)
329 flowcells au lieu de 291 : solid inclus, rebasecallés inclus, et `bam_metadata` a **une ligne par sample**. ⚠ **Aucune requête en dur** n'agrège ces colonnes — la règle ne vit que dans les deux system prompts, `TestRunLevelRule` est sa seule protection. ⚠ **3 listes d'imports à aligner**. [analytics_prompt_run_level.md](analytics_prompt_run_level.md)

## `/reproductibilite` — mVAF v1.5, seuils tracés, filtre QC (2026-08-27)
v1.5 **reporte** le seuil 0,0042 de v1.4, il n'est pas recalibré. ⚠ Deux pièges Plotly en log : le **range est retenu** d'un rendu à l'autre (`autorange` ne suffit pas) et les `shapes` prennent la **valeur brute**. Le filtre « Conformes uniquement » **recalcule** et retrouve les 11 aliquots de QARA §2.5. [reproductibilite_v15_graphe_qc.md](reproductibilite_v15_graphe_qc.md)

## `/profil-aima` — plus aucune comparaison chiffrée (2026-08-26)
Colonnes Eux/Nous/Comparabilité, écarts et verdicts retirés de l'affichage : nos cohortes ne sont pas les leurs. ⚠ **Ne pas réintroduire** sans demande (3ᵉ itération). ⚠ Backend inchangé, le retrait est **front pur**. ⚠ `/profil-aima` ≠ `/profils`. [profil_aima_sans_comparaison.md](profil_aima_sans_comparaison.md)

## Couche IA morte (E2BIG) + durcissement /analytics (2026-08-26)
`PIPELINE_CONTEXT` (164 Ko) passé en **un argument** dépassait `MAX_ARG_STRLEN` → toute la couche IA HS sans qu'aucun code ait changé. Fix : `--system-prompt-file`. Durcissement : sous-processus tuable, boucle d'auto-réparation, Opus 5 là où le modèle écrit du code. [analytics_ia_hardening.md](analytics_ia_hardening.md)

## Page `/qara` — Exis / Themelio / CUP (2026-08-21)
Première page **100 % statique**, valeurs recopiées du Google Doc. ⚠ **Ne jamais y dériver une valeur.** ⚠ Pas d'`uppercase` CSS sur les en-têtes. ⚠ Divergence CUP rendue **verbatim + encart** — sa cause est désormais connue (un `max_p` exactement au seuil). [qara_page.md](qara_page.md)

## Bloc « Performance des produits » — Tableau de bord (2026-08-12)
Aucun recalcul : même endpoint et même `pct()` que le Profil AIMA. ⚠ La ligne Exis **globale** exclut vessie/TNE/Nuclear → 82,0 % contre 76,2 % sur `/exploration`. ⚠ La spécificité est **globale**, elle se répète sur les 4 lignes. [dashboard_bloc_produits.md](dashboard_bloc_produits.md)

## Seuil Exis 0,0042 sur /reproductibilite (2026-08-12)
`_category()` est le point **unique** de décision et alimente aussi `_pairwise_agreement` : déplacer le seuil déplace le taux d'accord. ⚠ Le seuil vaut pour v1.4 et v1.5 (même échelle), **pas pour v1.0**. [reproductibilite_seuil_exis.md](reproductibilite_seuil_exis.md)

## Alignement Exis 1.1 — /exploration (2026-07-24)
Seuil en **quantile type 1** (et non type 6), exclusion nommée `CGFL_26BM01841`, sélecteur Cohorte Avancés/Précoce. ⚠ **Rompt** l'équivalence cell-by-cell vs R main. Seul écart accepté au PDF : `Prostate_21`. [exis_alignment.md](exis_alignment.md)

## Skill `/qara-tower` (2026-07-24)
Traçabilité temporelle : mesure T_n → compare → append au Doc → journal. ⚠ **Aucun recalcul maison**, réglages Exis figés. ⚠ Journal dans `qara/`, **pas `data/`** (gitignored). ⚠ Ordre : append Doc **avant** persist. [qara_tower_skill.md](qara_tower_skill.md)

## Page `/reproductibilite` (2026-07-22)
2 onglets = 2 protocoles séparés par le `run_id`. ⚠ Sémantique des suffixes : `_moche` ≠ mauvaise qualité, `_OK` = sous-ensemble du même run. ⚠ **Ne pas réutiliser `_get_prepared`** (triple dédup). ⚠ mVAF v1.4 est une feature d'entrée de themelio. [reproducibilite_page.md](reproducibilite_page.md)

## `/exploration` — toggle Score mVAF v1 / v1.4 (2026-07-03)
Une seule colonne `score` pilote toute la page ; le swap se fait dans `_prepare_base_dataset` **avant** le filtre `notna`. `score_source` threadé dans les caches et 11 méthodes. [exploration_score_source_toggle.md](exploration_score_source_toggle.md)

## Page `/combined` — onglet Suspects (2026-06-25)
25 imageries **sans vérité-terrain** → ⚠ ni sensibilité ni spécificité, seulement N au-dessus du seuil. ⚠ Le garde `float(label)` empêche les lignes sans vérité d'entrer dans la calibration. Jitter **déterministe**, pas `Math.random`. [combined_suspect_tab.md](combined_suspect_tab.md)

## Page `/combined` — refonte + onglet Dilution (2026-06-22)
Archi **α** : le pipeline Feature score les Twist, Tower reste **reader**. Source unique `scores.csv`, lookup colonne = `features.replace(",","+")`. ⚠ `FEATURE_NAMES` est une liste figée **à synchroniser à la main**. [combined_dilution_tab.md](combined_dilution_tab.md)

## Page `/combined` — intégration pipeline Feature (2026-06-09)
Tower est **reader**, pas exécuteur : pas de R dans l'image, `/pipeline` monté `:ro`. ⚠ Même `best_combo` est inlançable (son `connect()` ouvre en write). ⚠ Test de présence d'une feature : `list_contains`, jamais `LIKE '%mvaf_v1%'`. [feature_pipeline_integration.md](feature_pipeline_integration.md)

## Scission `/database` + ID sample Monitoring (2026-06-24)
`/database` scindée en **R&D** et **Plateforme** (`/database-platform`), **zéro backend** — les composants et endpoints étaient déjà séparés. ID sample de Monitoring parsé depuis **`--patient_id` de la command line**, pas `params_json`. [database_scission_pages.md](database_scission_pages.md)

## Feature `/samples` + `/sample/:id` — v4.2.0 (2026-05-13)
`get_sample_detail()` JOIN 5 tables. Décisions : TF = `mvaf_v1`, Negative/Positive strict (== 0 / > 0), seuil de profondeur **0,25×**. Helper `parseEuFloat()` pour les VARCHAR à virgule. [feature_sample_detail.md](feature_sample_detail.md)

## Spec ciblée vs Spec réalisée
Le slider dit ce qu'on **demande**, `Spec_AI` ce qu'on **obtient**. L'écart vient de la quantification du quantile sur un N healthy fini. [spec_ciblee_vs_realisee.md](spec_ciblee_vs_realisee.md)

## Tower v3.0.0 en prod (2026-05-07)
FastAPI + Vite + React + Tailwind v4 remplacent Dash. Un seul worktree, `~/Pipeline/Aima-Tower` sur `main`. Parachute de rollback = tag `v2.3.0`. [project_v3_cutover.md](project_v3_cutover.md)

## UI Tower v3 — multi-utilisateurs (2026-05-07)
Plus un dashboard perso : références personnelles retirées, **thème light par défaut**. ⚠ `theme-preference` préservé pour ceux qui ont déjà choisi. [ui_v3_multi_utilisateurs.md](ui_v3_multi_utilisateurs.md)

## Cascade cohorte /exploration — v3.0.0 (2026-05-07)
`compute_cohort_cascade()` `@lru_cache(64)` + hook lazy TanStack (`enabled` au premier open) et `useDebouncedValue(250ms)` sur les sliders. [feature_cohort_cascade_integration.md](feature_cohort_cascade_integration.md)

## Sens_Active redéfini = cancer_truth (2026-05-11, demande Michael)
La colonne « Cancer actif » utilise `cancer_truth` (mutated OR active_cancer). ⚠ Diverge **volontairement** du pipeline R — ne pas re-débattre. [project_sens_active_cancer_truth.md](project_sens_active_cancer_truth.md)

## Refonte Exploration v2.3 (2026-04-30)
Tower ≡ R main cell-by-cell (avant l'alignement Exis). ⚠ **2 cohortes distinctes** par sub-tab : Tableaux = R02, Graphiques = R04 — ne jamais unifier les deux chiffres. Pattern « tout coché = no-op » pour préserver les NULL. [exploration_v2_3_design.md](exploration_v2_3_design.md)

## Dash 4.1+ gotchas Tower
`allow_direct_input=False` sur les sliders, bump de la clé `persistence` pour invalider le cache navigateur, `dcc.Store` relais pour les composants conditionnels. [dash_4_gotchas.md](dash_4_gotchas.md)

## Docs externes read-only + réponses courtes (2026-08-21)
⚠ **Ne jamais modifier un Google Doc ou document externe**, même mineur, sans demande explicite pour ce doc précis. Réponses courtes par défaut. [feedback_docs_readonly_and_brevity.md](feedback_docs_readonly_and_brevity.md)

## Lecture Google Docs — API, pas navigateur (2026-08-21)
GET `docs.googleapis.com` + credentials gspread, jamais claude-in-chrome. ⚠ `includeTabsContent=true`, et le `tabId` garde son préfixe `t.`. ⚠ Chercher d'abord un script d'accès existant dans le repo. [google_docs_api_read_access.md](google_docs_api_read_access.md) · [feedback_check_existing_access_patterns.md](feedback_check_existing_access_patterns.md)

## Todo list — routing par section
4 parties : À faire / En cours / Complété / Stand-by. ⚠ Afficher **uniquement** la partie demandée. [feedback_todo_sections.md](feedback_todo_sections.md)

## Docker compose Tower — project name figé
Le compose contient `name: aima-tower`. ⚠ Sans cet override, compose taggue une **image fantôme** et le container tourne avec l'ancien code. [feedback_compose_project_name.md](feedback_compose_project_name.md)

## DuckDB Cross-DB Join Pattern
Une connexion read-only ne peut pas `ATTACH` : passer par une connexion `:memory:` qui attache les deux bases en READ_ONLY. Reproduire le retry backoff. [duckdb-patterns.md](duckdb-patterns.md)

## Liens Scaleway désactivés (2026-06-12)
Navigation web Scaleway retirée, chemins S3 gardés en **texte non cliquable**. ⚠ Helpers `s3ToScaleway` et `_s3_to_scaleway` **supprimés** — ne plus s'y référer. [scaleway_links_disabled.md](scaleway_links_disabled.md)

## Backend IA via CLI `claude -p` (2026-04-22)
Abonnement Max au lieu des crédits API. ⚠ **`ANTHROPIC_API_KEY` interdit** dans le container (le CLI le priorise et bypasse l'abonnement). ⚠ HOME isolé `/app/data/claude-home`. [ia_cli_migration.md](ia_cli_migration.md)

## Page Survey — patterns
Parser markdown extensible, lazy-render des onglets, écriture d'état atomique (tmp + rename), scoring IA découplé côté Aima-Survey. [survey_patterns.md](survey_patterns.md)

## Intégration DuckDB Aima-Survey (v6 — 2026-04-20)
`month` et `all` lisent `aima_survey.duckdb` en READ_ONLY avec retry, fallback markdown. Traduction `queries_matched` → descriptions humaines via `queries.json`, chargée au module load (restart requis si le fichier change). [survey_duckdb_integration.md](survey_duckdb_integration.md)

## Vues temporelles Survey pilotées par `first_seen_at` (2026-04-22)
Pivot = EDAT PubMed : **immuable, jamais dans le futur**, contrairement à `pub_date` qui produisait des dates futures et ratait les indexations tardives. [survey_first_seen_at.md](survey_first_seen_at.md)

## Onglet Concurrence Survey étendu
Le match se fait sur `org_name` **OR** `last_author_affiliation` : 11 → 29 articles. [survey_competitors_tab.md](survey_competitors_tab.md)

## Sécurité Tower (2026-04-21)
`https://tower.aima-diagnostics.com` via Caddy + basic auth bcrypt + Let's Encrypt. Port 8050 non exposé. ⚠ Caddy v2 : `basic_auth`, pas `basicauth`. ⚠ Hash bcrypt entre guillemets simples dans `.env`. [security_setup.md](security_setup.md)

## Sécurité — approche pragmatique
Boris valide l'itération **par couches** plutôt que le durcissement complet en une passe (blast radius). [feedback_security_pragmatism.md](feedback_security_pragmatism.md)

## Incident `.env` tracked dans git
`.env` tracked jusqu'au 2026-04-21, retiré via `git rm --cached`. ⚠ **Rotation des secrets reportée** (repo privé, dev unique). [project_env_leak.md](project_env_leak.md)

## Guardant Health — stratégie Europe (2026-04-23)
Snapshot à revalider trimestriellement : Guardant a **délégué l'Europe** aux labs locaux, aucun partenariat France sur le MRD. Fenêtres AIMA identifiées. [competitors_guardant_europe.md](competitors_guardant_europe.md)

## Platform Detail Panel (Database > Platform)
Layout Données (lg=8) à gauche, Trace (lg=4) à droite. Police des chemins `0.75rem`, plus petite que le reste.

## Docker Workflow
Rebuild : `docker compose down && docker compose build && docker compose up -d`. Restart simple si seul `assets/` change. ⚠ `COPY src/` invalide le cache à chaque modif de `src/`.

## Gotcha: Python Closures in Loops
Définir les fonctions helper **avant** leur premier appel dans la boucle — sinon `UnboundLocalError`, Python voyant l'assignation plus bas dans le scope.
