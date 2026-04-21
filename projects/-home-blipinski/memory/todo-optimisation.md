---
name: Todo optimisation Claude Code & projets
description: Liste des tâches en cours (par priorité) et historique des tâches complétées (par jour).
type: project
originSessionId: 129fb3f7-7613-4550-adf0-9392306d8a85
---
# Todo — Optimisation Claude Code & Projets

**Dernière mise à jour : 2026-04-15 (ajout tâches post-Batches A-F + planification HCL)**

---

# Partie 1 — À faire (par priorité)

## Pour demain (2026-04-16)

- [ ] **Nouveau client** — suivre la prise en charge (relance / réponse au premier mail).
- [ ] **Seqera AI** — finir la prise en main du CLI et de l'API.

## Haute priorité

- [ ] **Sécurité secrets — étape 1** : migrer `~/Pipeline/export/` vers des fichiers `.env` avec `chmod 600`. Documenter le pattern pour les autres projets (tokens Tower dans nextflow.config).

## Moyenne priorité

- [ ] **Rotation secrets Aima-Tower compromis** — `.env` était tracked dans git jusqu'au 2026-04-21 (historique pushé sur `aima-dx/Aima-Tower`, repo privé). Révoquer `ANTHROPIC_API_KEY` (console.anthropic.com > API Keys) + `accessToken` Seqera (cloud.seqera.io > Tokens), regénérer les 2 et mettre à jour `.env` local + `docker compose restart`. Voir `~/.claude/projects/-home-blipinski-Pipeline-Aima-Tower/memory/project_env_leak.md`.
- [ ] **Clean dossier `raw HCL` dans le bucket BAM** — nettoyage ciblé des fichiers obsolètes. ⚠️ Rappel golden rule S3 : aucune suppression sans confirmation explicite + lister les fichiers avant + vérifier qu'ils ne sont pas référencés dans trace-prod/trace-platform.

### Skills bioinformatiques
- [ ] **Améliorer skills v1 avec /meta-skills-creator** — sample, debug-nf, check-consistency sont fonctionnels mais créés sans le processus rigoureux. Raffiner après usage.

### Projets bioinformatiques
- [ ] **Aima-Tower — évolutions post-Batches A-F** (socle livré 04-14) :
  - [ ] **Remplacer "Distribution scores Healthy par kit" par scatter TF mVAF v1 vs TF panel génétique** (dans `/analytics` Avancé). X = VAF panel génétique (gene1_vaf, %), Y = mVAF v1 (score méthylation). Trace la corrélation TF_meth ↔ TF_gen. Couleur par indication ou centre, ligne y=x en référence, R² ou Spearman affiché.
  - [ ] **Comprendre et améliorer le Calibration plot** (`/analytics` Avancé). Actuel : qcut en déciles de score + fraction cancer_truth observée + diagonale "calibration parfaite si score = probabilité". Questions à creuser : (1) la diagonale est-elle la bonne référence alors que mVAF v1 n'est pas une probabilité brute mais un score continu ? (2) ajouter un reliability diagram avec CI Wilson par bin, (3) calculer Brier score ou ECE (Expected Calibration Error), (4) envisager isotonic regression ou Platt scaling pour calibrer le score, (5) doc explicative dans le modal `?`.
  - [ ] **Ajouter un backlog dans `/qualite`** — liste persistante d'items à suivre côté surveillance qualité (incidents, anomalies détectées, actions correctives, audits à faire). Champs : date, titre, description, statut (open/in_progress/closed), priorité, lien snapshot/permalien associé. Stockage JSON simple dans `/app/data/qualite_backlog.json` (comme pour les snapshots). UI : tableau CRUD dans une nouvelle carte de la page `/qualite`.
  - [ ] **Enrichir les agents IA (/analytics IA)** avec accès aux métriques exploratory-analysis et aux filtres (actuellement l'agent n'a pas ce contexte).
  - [ ] **Intégrer IGV.js via dash-bio** (visualisation bedMethyl) — reporté, prérequis : réduire la charge de la page /exploration.
  - [ ] **Précompute client-side (point 10)** — reporté : architectural refactor vs ROI limité au vu des temps actuels <200ms. À réactiver si cohorte dépasse 5000 samples.
  - [ ] **Cron alertes dérive (/qualite)** — actuellement les snapshots sont manuels. Ajouter un cron hebdo qui appelle `check_drift()` et envoie email/Slack si alerte (prerequis : SMTP ou webhook configuré).
  - [ ] **Pytest en CI** — les 11 tests tournent en local, les intégrer à un workflow GitHub Actions ou hook pre-commit.
  - [ ] **Feedback itératif** sur usage réel : layout Confrontation, ergonomie des 4 filtres avancés, pertinence des bins VAF, lisibilité ISO 15189 report.
- [ ] **Explorer MethylBERT** — Transformer read-level (Nat Comm 2025) pour améliorer sensibilité basse VAF (<5%). Nécessite GPU. ~2-3 jours.

## Basse priorité

- [ ] **Sécurité secrets — étape 2** : installer `gitleaks` en pre-commit hook sur les projets gittés.
- [ ] **Sécurité secrets — étape 3** : évaluer un gestionnaire de secrets (sops, age, vault).
- [ ] **Skill save-code pour trace-prod** — automatiser la sauvegarde de session.
- [ ] **Aima-Survey — évaluer remplacement MCPs inexistants** — seul point restant du chantier "automatisation complète" : statuer si les MCPs DuckDB/S3/Ensembl/NCBI sont utiles ou si les scripts Python directs (PubMed E-utilities + SQLite) suffisent. Scoring IA + dashboard + email quotidien = faits le 04-16.
- [ ] **Skills Pod2Bam** — créer test/qualif/maj analogues à Bam2Beta. Pas urgent tant que Pod2Bam n'est pas soumis à audit qualité.

---

# Partie 2 — En cours

- [ ] **Import metadata HCL depuis gsheet** — 282 samples importés le 15/04, 32 Healthy (111-142) absents de la table `samples` (pas encore intégrés). Cron one-shot auto-destructif planifié 16/04 12h Paris pour re-lancer `import-metadata liquid HCL` après intégration des nouveaux samples.
- [ ] **Prise en charge nouveau client** — premier mail envoyé, en attente de retour.

---

# Partie 3 — Complété (par jour)

## 2026-04-21 — Aima-Tower sécurisation + HCL runs + backup S3 + check Healthy

- [x] **Sécurisation Aima-Tower HTTPS + basic auth** — Caddy reverse proxy + cert Let's Encrypt auto (TLS-ALPN-01) + `basic_auth` bcrypt cost=14 (user `aima`), port 8050 fermé à Internet (`expose:` au lieu de `ports:`), `SECRET_KEY` Flask depuis `.env` + `SESSION_COOKIE_SECURE=True`. `.env` retiré du tracking git (était pushé sur `aima-dx/Aima-Tower` — incident détecté et documenté). Rotation secrets Anthropic/Seqera reportée (repo privé, Boris seul dev). Commits `a2321e1` (Aima-Tower) + `bee7b2e` (claude-config). URL prod : `https://tower.aima-diagnostics.com`. Détails mémoire : `security_setup.md`, `project_env_leak.md`.
- [x] **32 samples HCL Bam2Beta** — lancés en PROD, nouveaux samples intégrés dans la cohorte exploratory.
- [x] **Sauvegarde HCL sur S3** — BAM + POD5 des 32 samples uploadés, counts vérifiés.
- [x] **Check prod Healthy** — état de production des samples Healthy vérifié.

## 2026-04-20 — Aima-Survey refonte v6 + Aima-Tower /survey + /exploration

### Aima-Survey — refonte v6 (8 commits)

- [x] **Aima-Survey v6 — DuckDB single-table multi-source** — `lib/db.py` + table `articles` avec colonnes `external_id`, `source`, `score`, `score_why`, `first_seen_at` (commits `636f83b`, `a65a4e7`, `af1341b`, `fa13c65`, `30b6587`, `939a0bd`).
- [x] **Aima-Survey v6 — CLI Click complet** — `cli.py` : `add`/`remove`/`list`/`query`/`stats`/`export`/`backfill`. `veille.py` refactoré pour lire la DB + nouveau `lib/render.py` dédié markdown.
- [x] **Aima-Survey — fusion rubriques + +5 rubriques** — fusion ctDNA+cancer, fusion outils, suppression high_impact_journals (`4fec01a`) ; ajout MRD, MCED, tissue-origin, ML classifiers, EPIC/Illumina (`73ff597`). Total 12 rubriques.

### Aima-Tower /survey — intégration DuckDB v6 (13 commits)

- [x] **Tower /survey — lit `aima_survey.duckdb`** — `SurveyService._articles_from_duckdb` pour vues mois/all (READ_ONLY + retry backoff), fallback markdown si DB KO. Config paths + mount Docker Aima-Survey (commits `93958bd`, `2183bc3`).
- [x] **Tower /survey — 5 vues temporelles** — jour / semaine (défaut) / mois / all / **Favoris** (5e mode, `4d5cd27`). Semaine par défaut à chaque ouverture (`7a10c12`), suppression DatePickerRange + slider Score IA min (`702f520`), suppression onglet "Top articles" vue Semaine (`19f1197`).
- [x] **Tower /survey — fixes parser + onglets** — un article ne peut être que dans un seul onglet rubrique (`de66540`), vue Mois filtre strictement `pub_date` (retire OR first_seen_at, `cb75f4f`), `get_article_by_pmid` lit aussi la DuckDB (`acfce9e`), catégories obsolètes → "Autres", traduction vieilles descriptions markdown, filtre catégories obsolètes parser + maj labels.
- [x] **Tower /survey — UX polish** — spinner `dots` pendant génération synthèse IA, header "Vue Jour" harmonisé, script one-shot maj descriptions favoris post-fusion. Pagination 50 par onglet testée puis revert.

### Aima-Tower /exploration — refresh + UX filtres + slider VAF

- [x] **Aima-Tower /exploration — bouton Refresh** — bouton dans le header qui appelle `exploratory_service.reload()` + invalide le cache LRU + toast de confirmation. Évite le `docker compose restart` quand de nouveaux samples arrivent dans trace-prod.
- [x] **Aima-Tower /exploration — défaut Dorado = ge5** — filtre version Dorado par défaut passé de `v5.0.0` strict à `Toutes (≥ 5.0)` (option en première position). Reset filters aligné. Couvre v5.0.0 + v5.2.0 d'office (~270 healthy au lieu de 148).
- [x] **Aima-Tower /exploration — filtres avancés en collapse** — selects (indications, cancer actif, dorado, kit, rebasecalled) déplacés dans un `dbc.Collapse` togglé par bouton "Filtres avancés ▾". Bouton aligné avec Seuils/Cohorte/Reset/Export sur une seule barre du bas.
- [x] **Aima-Tower /exploration — slider VAF_LIMIT** — `VAF_LIMIT` (seuil high/low VAF du tableau stratifié) exposé en slider 0.5–5.0 (défaut 2.0) à côté de Spec/Profondeur. Câblé dans `compute()`, `_compute_stratified()`, callbacks tab/thresholds/reset/permalink/restore_url/download.
- [x] **Aima-Tower /exploration — headers dynamiques tableau stratifié** — colonnes `VAF > X%` / `0 < VAF <= X%` du tableau Sensibilité Stratifiée suivent le slider VAF en temps réel (format `:g`, ex. 2.0 → "2"). `vaf_limit` threadé via `_build_one_side` → `_build_tables_content`.

## 2026-04-16 — Aima-Survey + Aima-Tower : email quotidien + page Survey intégrée

- [x] **Aima-Tower — page Survey intégrée** — nouvelle route `/survey` consommant les rapports markdown Aima-Survey. Vue Jour/Semaine avec onglets rubriques, filtres combinables (recherche + priorité + rubrique + journal + date + état lu/non-lu), synthèse IA par article à la demande (claude-sonnet-4-6), marquage vu/non-vu avec badge navbar, favoris avec notes inline. Bug `TOP_N=10` fixé côté `veille.py` (tous les articles exportés). Commit `91c545d`.
- [x] **Aima-Survey — envoi email quotidien** — `veille.py` refactoré : envoi via email-hub (Redis/BullMQ), contourne le port 587 bloqué Scaleway. Badges date/priorité HTML, dédup par PMID + tri priorité > date. `run_veille.sh` wrapper + `.env` chmod 600 gitignoré. Cron daily 8h00 opérationnel (email envoyé uniquement si ≥1 publication).
- [x] **Aima-Survey — requêtes PubMed enrichies** — 10 requêtes (vs 6) avec filtres `humans[mesh]` sur axes cliniques + `NOT review[Publication Type]` partout + 3 nouveaux axes (fragmentomics, modkit/dorado, 5hmC) + filet haut-impact (Nature/Genome Biology/NAR...).
- [x] **Prendre en main automate veille scientifique** — projet exploré en profondeur (agent-explore), flux cron → PubMed E-utilities → markdown compris, évolutions majeures apportées dans la foulée (cf. entrées ci-dessus).
- [x] **Aima-Tower — page Survey polish & perf** — filtres redesignés (InputGroup avec icônes, persistence session, compact `size="sm"`), lazy-render des onglets (payload Day 170→15 KB soit -91%, Week 278→104 KB soit -62%), `dbc.Collapse` par card remplacé par `html.Div` + toggle `style.display` (mount React plus rapide), UI note retirée (backend préservé). Commit `d1d8486`.
- [x] **Agent de veille enrichi** — `scorer.py` Claude Haiku 4.5 : score 0-10 + why + tags par article dans Aima-Survey, cache SQLite `scoring_cache.db`, rendu via span `score-badge` + bullet `**IA**` dans le markdown. Commit Aima-Survey `85036d0`.
- [x] **Aima-Tower — scoring IA intégré dans /survey** — parser étendu (`score`, `why`), badge `IA X/10` coloré (vert ≥7 / jaune 4-6 / gris <4), ligne justification en italique, slider "Score min" 0-10, tri multi-critères `(priorité, score desc, None en fin, date desc)`, rétrocompatible rapports pré-scoring.
- [x] **Aima-Survey — dédup cross-jours + fenêtre 7j + docs** — table SQLite `sent_articles` qui filtre les PMIDs déjà envoyés (évite le spam quand cron passe à `--days 7`). Cron daily 1j → 7j : rattrape les papiers avec `pdat` indexé en retard (ex: fRagmentomics PMID 41886314 loupé en `--days 1`). README.md créé, CLAUDE.md réécrit (stack + conventions + historique v1→v5), 2 mémoires Claude : `email_sending.md`, `scoring_and_dedup.md`. Commit Aima-Survey `08328ae`.

## 2026-04-15 — Housekeeping projets

- [x] **Renommage projet `veille-scientifique` → `Aima-Survey`** : dossier renommé, 2 lignes crontab mises à jour, skill `/veille` migré (2 refs), CLAUDE.md du projet corrigé.
- [x] **Git push Aima-Survey sur GitHub** : branche renommée `master` → `main`, remote `origin` configuré sur https://github.com/aima-dx/Aima-Survey.git, 2 commits poussés. Aucun secret dans les fichiers trackés (clé NCBI via `NCBI_API_KEY` env var).
- [x] **Todo list restructurée** : ajout d'une Partie 2 "En cours" (entre À faire et Complété). Routing par section sauvé en mémoire Aima-Tower (`feedback_todo_sections.md`).
- [x] **trace-workflow multi-workspace** — ajout workspace `aima-diagnostics` en plus du perso via filtre `ALLOWED_ORGS`. Migration DB idempotente (`workspace_id`), 15 957 workflows existants préservés.
- [x] **Prise en main CLI Seqera** — `seqera ai --headless` (via skill `/seqera`) pour les questions NL, et API REST directe (`/user-info`, `/workflow?workspaceId=`) utilisée par `trace-workflow`.
- [x] **Traduction user manual plateforme** — terminée.

## 2026-04-14 — Aima-Tower : Batches A-F + refonte navigation

Session de développement intensif post-Batches de base. Aima-Tower passe d'un dashboard d'exploration à un **outil ISO 15189 opérationnel**.

### Refonte navigation
- [x] **Navbar recomposée** : `Database | Monitoring | Analytics | Exploration | Qualité | Overview`. Suppression de `/compute` (contenu fondu dans `/monitoring`). Nouvelle page `/qualite` dédiée à la surveillance longitudinale ISO 15189.
- [x] **Ressources système (CPU + Mémoire)** déplacées de `/compute` vers `/monitoring` en carte compacte sous le tableau "Workflows terminés". Front adapté (labels inline, plus de headers de cartes séparées).

### /analytics refondu (Batch A)
- [x] **Suppression "Reads par Tissu"** + ses filtres (sample-type, labo, tissue) et callbacks associés.
- [x] **Tabs IA | Avancé** :
  - **IA** : regroupe "Draw with Aima Analyser" + "Ask to Aima Analyser" (inchangés).
  - **Avancé** : sidebar filtres indépendante (target, depth, dorado, indications, active, rebase) + 4 analyses.
- [x] **Distribution des scores Healthy par kit** : histogramme overlay Apostle / Maxwell / Autre — visualise le batch effect kit (amplificateur EPIC→ONT).
- [x] **Calibration plot** : déciles de score (qcut) vs fraction cancer_truth observée + diagonale référence.
- [x] **Stats comparatives CGFL vs HCL** : Δ Sens_AI, Δ Spec_AI et Fisher exact 2×2 (scipy).
- [x] **Clustering FN/FP** : PCA 2D (sklearn) sur features score+vaf+depth+indication+kit+version — visualise les groupes d'erreurs.

### /qualite nouvelle page (Batch B + D + F)
- [x] **Création page** : navbar, route, factory, layout (filtres gauche + content droite).
- [x] **Drift temporel Sens/Spec** : bucket par fenêtre (semaine/mois/trimestre), seuil global stable, baseline horizontale pointillée, markers ∝ N par fenêtre. `m.date_of_run` ajoutée à la query DuckDB.
- [x] **Snapshots persistants** : `qualite_snapshots.py` (JSONL `/app/data/qualite_snapshots.jsonl`), bouton "Enregistrer snapshot", tableau historique (20 derniers).
- [x] **Alertes dérive** : `check_drift()` compare dernier snapshot à moyenne des 5 précédents, seuil 3 pp. Banner warning en tête de page si alerte.
- [x] **Rapport ISO 15189** : bouton "Rapport ISO 15189" → download HTML imprimable (filtres + tables + figures Plotly via CDN + SHA-256 hash + timestamp). Utilisateur imprime en PDF via Ctrl+P.

### /database nouvel onglet (Batch F)
- [x] **Onglet "Détails ML"** : tableau sample-level avec sort/filter/pagination natifs (dash_table). Colonnes Sample/Centre/Indication/Label/Score/Seuil/AI/VAF/Depth/Kit/Dorado. Code couleur vert/rouge/jaune pour TP/FN/FP.

### /exploration améliorations (Batch C)
- [x] **depth_sweep vectorisé** : une passe numpy au lieu de 38 computes pandas. **~10× plus rapide** (2-3s → 200ms).
- [x] **Correction date parsing** : `pd.to_datetime(dayfirst=True)` pour les dates FR `%d/%m/%Y`.
- [x] **Presets nommés** (essai → retrait) : créés puis supprimés à la demande (redondant avec le permalien URL). Suppression du module `bookmarks.py`, menu dropdown, modal, 4 callbacks.

### Qualité (Batch D)
- [x] **11 snapshot tests pytest** dans `tests/test_exploratory_compute.py` — **11/11 PASS**. Couvre la régression R (Phase 1b), le default v5.0.0 strict, la stabilité des filtres, le quantile seuil.
- [x] **scipy + scikit-learn** ajoutés à `requirements.txt` + Docker rebuild.

### Fix UI post-session
- [x] **Drift plot ne rendait pas** : 2 bugs — `alert_banner = None` injecté comme children + `Input("qualite-snapshot-save-feedback")` référencé depuis l'intérieur du callback Output (circular). Hoist feedback div hors de qualite-content, filtrage des None children.

### Commits (8)
- `99a86da` slider dynamique + plots (phase 1+2+3)
- `50eb016` cohort filters (indication, active, depth)
- `cac96f4` Dorado version, kit, rebasecalled filters
- `050c915` cohort counts match R + dual bars
- `4bf1c90` Batch 1-3 UX + depth sweep + VAF bin + info modal
- `828c72b` comparison mode A|B (reverté)
- `09dfd93` A|B → onglet Confrontation dédié
- `b7044cc` Batch A+B (analytics refactor + /qualite création)
- `050c915` (fix cohort counts)
- `4bf1c90` UX + depth sweep + VAF
- Batch C+D+E+F (perf, snapshots, bookmarks, exports, ML tab)
- `260ec61` remove presets + fold Compute into Monitoring + fix drift freq
- `2d5fb78` fix drift plot render (hoist feedback, strip None children)

## 2026-04-14 — Aima-Tower exploratory-analysis : UX complète + 4e onglet Confrontation

Session de livraisons successives post-phase-3, page `/exploration` refondue :

### Filtres & interactivité (priorité 2)
- [x] **Filtres cohorte** : multi-select indications (default = toutes), select cancer actif (Tous/Actif/Non actif), slider depth (0.10–2.00, défaut 0.25). Healthy toujours conservés pour calibrage seuil. Commit `50eb016`.
- [x] **Filtres avancés** : version Dorado (défaut v5.0.0 strict, option v5.2.0, option "Toutes ≥5.0" = R), kit extraction (Apostle/Maxwell/Autre, normalisé depuis `extraction_protocol`), rebasecalled (Inclure/Exclure/Uniquement). Commit `cac96f4`.
- [x] **Dédup par version** : préparation paramétrée par `version_mode`, original préféré + rebasecallé en fallback. Cache prep keyé par `(centre, analysis_type, version_mode)`.
- [x] **Counts cohorte alignés sur R** : `_compute_cohort_counts` retire seulement rep/moche/bis/ter/quater (garde TNE/Nuclear/Bladder_Blood), 48/48 lignes identiques aux CSV R à 0.85 mode ge5. Commit `050c915`.

### Graphiques (priorité 3)
- [x] **Distribution scores** : overlay healthy vs cancer + ligne verticale seuil.
- [x] **ROC curve** : TPR vs FPR à tous seuils + marker ambre mobile au seuil courant + AUC dans le titre.
- [x] **Forest plot** : sens par indication avec CI 95% Wilson.
- [x] **Depth sweep** : courbe Sens/Spec vs depth_min (0.10–2.00).
- [x] **VAF bin plot** : Sens_AI par bin VAF (0-0.5 / 0.5-1 / 1-2 / 2-5 / 5-10 / ≥10% / Non-muté).
- [x] **Cohort bar plot dual** : barres grises background (total depth=0) + barres bleues foreground (depth filtré), label `N_filtré / N_total` au-dessus.

### UX & ergonomie (Batches 1-2)
- [x] **Sous-onglets Tableaux / Graphiques** (persistence session, pills styled) dans chaque onglet centre.
- [x] **Badges sens/spec** : dégradé HSL rouge→jaune→vert (30%→100%), saturation 80%.
- [x] **CI Wilson 95% inline** : format `81.2% [76.3–85.4] (242/298)` sur tous les badges (validation R inchangée, computed en display layer).
- [x] **Reset button** : remet tous les filtres aux défauts en un clic.
- [x] **Indicateur cohorte live** : "Cohorte ALL : 298 cancer + 140 healthy" mis à jour avec filtres. Warning "seuil instable" si healthy < 20.
- [x] **Modal info "Comment ça marche ?"** : doc détaillée pipeline R→Python (étapes 01/02/03, filtres analytiques vs cohort counts, normalisation kit, CI Wilson, validation R).
- [x] **Export CSV par table** : dropdown menu avec les 14 clés exportables (détection, par indication, stratifié, misclassified, counts). Filtres courants intégrés au nom du fichier.
- [x] **Permalien** : dcc.Clipboard copie l'URL `/exploration?target=0.90&kit=Apostle&...`. Restore depuis URL query string au chargement.
- [x] **Plotly modeBar** : réactivé au hover, export PNG 2×, logo plotly retiré.
- [x] **Slider compact** : handle plus petit, marks 0.7rem, track réduit, focus avec halo bleu.
- [x] **Colonne Depth ajoutée** aux tableaux misclassified FN/FP.

### 4e onglet Confrontation
- [x] **Mode comparaison A|B dédoublement de la carte filtres** : tentative abandonnée (surcharge UI). Remplacé par onglet dédié.
- [x] **4e onglet "Confrontation CGFL vs HCL"** : affiche CGFL (header vert) et HCL (header violet) côte à côte avec les filtres principaux partagés. UI propre, pas de doublon de contrôles. Commit en cours.

### Commits
- `99a86da` feat(exploration): slider dynamique + plots (phase 1+2+3)
- `50eb016` feat(exploration): cohort filters (indication, active, depth)
- `cac96f4` feat(exploration): Dorado version, kit, rebasecalled filters
- `050c915` fix(exploration): cohort counts match R + dual bars
- `4bf1c90` feat(exploration): Batch 1-3 UX + depth sweep + VAF bin + info modal
- `828c72b` feat(exploration): comparison mode A|B toggle (reverté ensuite)

## 2026-04-14 — Aima-Tower exploratory-analysis (recalcul dynamique, 5 phases)

- [x] **Phase 1a — ExploratoryAnalysisService Python** : `src/exploratory_compute.py` créé, réimplémente `run_pipeline.R` + `functions_prepare_data.R` en pandas/numpy. Charge trace-prod DuckDB, prépare datasets (filter v≥5.0, depth≥0.25, dedup unique_id), threshold via `np.quantile method='weibull'` (= R `type=6`), expose `compute(target_specificity)` avec cache LRU.
- [x] **Phase 1b — Validation croisée Python vs R** : **28/28 tests PASS** (14 tableaux × 2 targets 0.85 + 0.90). Outputs identiques aux CSV R (`figures_and_tables_085_new/` et `figures_and_tables_090_new/`). Key learning : R `type=6` = numpy `method='weibull'` (pas `'hazen'`).
- [x] **Phase 2a — UI slider** : `_threshold_slider_card()` (0.80–0.99, step 0.01, default 0.85) ajouté au-dessus des tabs dans `exploration_page()`. Persistence session.
- [x] **Phase 2b — Callback dynamique** : `update_exploration_tab` modifié pour prendre `exploration-target-slider` en Input → recalcule tab content. Nouveau callback `update_exploration_thresholds` affiche target% + seuils ALL/CGFL/HCL live. `_build_exploration_content(centre, target_spec=0.85)` utilise `exploratory_service.compute()` via mapping `_CENTRE_KEYS`.
- [x] **Phase 3 — Cleanup** : suppression `ExplorationService` CSV-based + `_CSV_MAP` + `exploration_service` dans services.py, `exploration_csv_path` dans config.py, volume `/exploratory-analysis` dans docker-compose.yml, import dans pages.py. Rebuild Docker OK, 1033 samples chargés depuis trace-prod.
- [x] **Checkpoint git** : branche `backup-pre-exploratory` (commit `8df0502`) créée pour rollback.

## 2026-04-14 — Investigation batch effect CGFL vs HCL

- [x] **Investigation systématique batch effect CGFL vs HCL** — exploration de 12 pistes via trace-prod + exploratory-analysis + lecture BAM/bedMethyl :
  - composition biologique (Cat 1/2/3/4, VAF panel)
  - kit barcoding (NBD114-96 vs NBD114-24) — confounded
  - kit extraction (Apostle vs Maxwell) — confounded, Maxwell n'a PAS plus de gDNA long (hypothèse inverse)
  - version Dorado / GPU — pas significatif en v5.0.0
  - couverture — FP stables à toutes profondeurs
  - taille des fragments — CGFL a en fait des reads plus longs (mean 260bp vs 222bp)
  - fragmentomics mode1 — artefact des rebasecallés, pas un batch effect
  - modkit auto-threshold — déjà testé, ne change rien
  - score CNV — batch effect confirmé (matrice 100% CGFL dans raima)
  - ichorCNA — OK, corrèle avec charge tumorale
  - déconvolution Loyfer — distributions proches
  - profil cfDNA FP HCL — signal tissulaire subtil (moins de blood_0)
  - Voir `~/.claude/projects/-home-blipinski-Pipeline-Bam2Beta/memory/batch-effect-investigation.md`
- [x] **Création projet `~/Pipeline/ComBat-Met/`** — CLAUDE.md, .claude/rules, Docker (R 4.4 + ComBatMet 0.99.3), 9 scripts R/bash pour extraction, correction, scoring parallèle.
- [x] **Test ComBat-met** — 4 variantes testées (group=H/C, rebalancé, ref.batch=CGFL, Healthy only). **Aucune ne fonctionne**. Finding inattendu : la simplification du bedMethyl seule réduit 17% → 3% FP HCL sans ComBat-met.
- [x] **Identification des 2 batch effects racines** :
  1. **EPIC → ONT** (majeur) : raima V1 entraîné sur 19 EPIC bisulfite microarrays, appliqué à ONT → biais technologique jamais corrigé
  2. **Apostle vs Maxwell** (amplificateur) : kits d'extraction ADN cfDNA avec chimies différentes (Apostle = nanoparticules propriétaires, Maxwell = billes magnétiques Promega) → biais de capture CpG différent ; Apostle produit des profils ONT plus proches des refs EPIC **par hasard** → explique les 2% FP CGFL vs 17% HCL
  - Les 2 effets sont liés : le kit crée une composante de biais ONT qui interagit avec le biais EPIC. Confounded avec centre (pas de Maxwell CGFL, pas d'Apostle HCL).
- [x] **Conclusion ComBat-met** : **non retenu pour la production**. Documenté dans `~/Pipeline/ComBat-Met/README.md`. Dépendance batch-spécifique incompatible ISO 15189 + simplification technique suffit pour 80% du problème.
- [x] **Mise à jour mémoire Claude** : `batch-effect-investigation.md` + pointeur dans MEMORY.md Bam2Beta.
- [x] **Restructuration todo list** : séparation tâches à faire (par priorité) / tâches complétées (par jour).
- [x] **Skill `/audit-trail`** — créé, traçabilité ISO 15189 (changelog + diff + hashes containers + non-régression) pour les versions Bam2Beta/Pod2Bam.
- [x] **Skills analyse scientifique** — `/compare-batches` (Wilcoxon/Fisher + confounders), `/qc-report` (rapport standardisé avec seuils), `/correlation` (Spearman + paradoxe de Simpson) créés et pushés sur claude-config.
- [x] **Centralisation doc effet batch** — tout regroupé dans `~/Pipeline/batch_effect/` : README central (12 pistes + 2 batch effects racines + ComBat-met), CLAUDE.md workflow de reprise, `ComBat-Met/` déplacé en sous-dossier, mémoire Claude `batch-effect-investigation.md` mise à jour.

## 2026-04-13 — Rétrospective et setup Claude Code

- [x] **Nettoyage config Claude** — skills, plugins, agents dupliqués supprimés.
- [x] **Golden rules globales** — s3-safety, duckdb, nextflow, secrets dans `~/.claude/rules/`.
- [x] **CLAUDE.md global** — profil Boris (bioinfo AIMA, bus factor 1) réécrit.
- [x] **MCP installés** — pubmed, duckdb, memory, ensembl, ncbi, s3.
- [x] **Hooks** — protection S3, notification.
- [x] **Veille scientifique automatisée** — cron + skill `/veille`.
- [x] **Skill `/export-gsheet`** pour trace-prod.
- [x] **Profil utilisateur complet** — technique + scientifique dans `~/.claude/projects/-home-blipinski/memory/`.
- [x] **Skills bioinformatiques v1** — `/sample`, `/debug-nf`, `/check-consistency`, `/batch-effect`.
- [x] **Références techniques** — bedMethyl, troubleshooting, stats-guide, dorado-reference.md.
- [x] **Contexte pipeline AIMA** dans 7 CLAUDE.md projets.
- [x] **Instructions compaction intelligente** — garder fichiers modifiés, commandes testées, décisions, état runs NF, bugs.
- [x] **Aliases et template CLAUDE.md** standardisés.
- [x] **Agent explore bioinfo** avec détection automatique Phase 6.

---

# Partie 4 — En stand-by

Tâches identifiées mais bloquées (dépendance externe, info manquante, décision en attente). Ne pas mélanger avec "basse priorité" — ici c'est **bloqué**, pas juste **pas prioritaire**.

Format : `- [ ] **Titre** — raison du blocage. **Débloquer quand :** condition concrète.`

---

**Why:** Issue de la rétrospective complète Claude Code du 13/04/2026 + investigation batch effect du 14/04/2026. Format 4-parties : à faire (Partie 1) / en cours (Partie 2) / complété (Partie 3) / en stand-by (Partie 4).
**How to apply:** Consulter la Partie 1 en début de session. Déplacer une tâche en Partie 2 quand elle démarre activement. Ajouter en tête de Partie 3 à chaque fin de session avec la date. Utiliser Partie 4 pour les tâches bloquées qu'on ne veut pas perdre mais qu'on ne peut pas avancer.

**Routing des requêtes utilisateur :**
- "qu'est-ce qui est à faire" / "todo" / "à faire" → Partie 1
- "qu'est-ce qui est en cours" / "en cours" → Partie 2
- "qu'est-ce qui est fait" / "complété" / "historique" → Partie 3
- "qu'est-ce qui est en stand-by" / "bloqué" → Partie 4
- "montre la todo list" (sans précision) → Partie 1 + 2 (actif uniquement)
