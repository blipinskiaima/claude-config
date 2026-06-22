export const meta = {
  name: 'author-covdepth-kickoff-prompt',
  description: 'Author a grounded, best-practice dev-kickoff prompt for the covdepth QC analysis task (Step 1 R figure)',
  phases: [
    { title: 'Research', detail: 'parallel: prompt-engineering technique grounding + real codebase/QC/golden-rules context' },
    { title: 'Draft', detail: 'compose candidate prompt (FR) from research + user requirements' },
    { title: 'Verify', detail: 'adversarial critique vs prompt-creator checklist + user hard constraints, return refined final' },
  ],
}

const USER_REQ = `OBJECTIF DU DÉVELOPPEMENT (à encapsuler dans le prompt) :
- Sample test : Bladder_Urine_02_064
- Contenu du sample test (QC) : s3://aima-bam-data/processed/MRD/RetD/liquid/CGFL/Bladder_Urine_02_064/QC/
- Espace de travail : /scratch/boris/covdepth (sous-dossiers data/, result/, script/ pour sauvegarde)
- Résultats principaux (livrables accessibles à Boris) : /home/blipinski/Pipeline/Bam2Beta/dev/coverage_analysis/test
- Objectif global : valoriser l'analyse QC pour les samples ; identifier des anomalies de QC à l'échelle du sample ; identifier des anomalies de tendance à plusieurs échelles (sample, cohorte, indication, labo, multi-labo, tous samples réunis).
- Modèle de développement : Opus 4.8 1M en mode MAX thinking.
- ÉTAPE 1 (la seule définie pour l'instant) : avec le sample test, produire une figure R BASIQUE qui met en relief le rapport depth/coverage, lisible à l'œil nu et facilement intelligible par un biologiste ou un bioinformaticien. La figure doit être claire, simple et efficace. Les étapes suivantes seront définies plus tard.

PROCESS IMPOSÉ (doit figurer explicitement dans le prompt) :
- Brainstormer l'idée au maximum, PUIS récupérer un max de contexte nécessaire, en utilisant des sub-agents de recherche si nécessaire pour trouver les infos utiles au plan de développement.
- Présenter un plan de développement et n'avancer qu'APRÈS approbation explicite de Boris.
- Parallélisation des développements OU un par un : au libre choix de l'exécutant.
- Suivre IMPÉRATIVEMENT les Karpathy Guidelines (think before coding, simplicity first, surgical changes, goal-driven execution).
- S'arrêter après CHAQUE modification pour vérifier et valider chaque point avec Boris avant l'étape suivante ; poser toutes les questions nécessaires au moindre doute.
- Travailler en LOCAL dans le scratch pour ne pas surcharger le serveur.
- Copier UNIQUEMENT les résultats finaux (la figure principale) dans /home/blipinski/Pipeline/Bam2Beta/dev/coverage_analysis/test ; sauvegarder data/résultat/script dans les dossiers respectifs du scratch.
- Suivre les règles d'or (S3 : jamais de suppression/écrasement ; AWS_PROFILE=scw ; pas de secrets en clair ; conventions Nextflow).
- Documenter de façon pertinente et synthétique les étapes de développement.`

const TECH_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    recommended_scaffold: { type: 'string', description: 'Ordered section structure (XML tags or headings) optimal for an Opus dev-kickoff/agent prompt with brainstorm->context->plan->approval gate' },
    techniques: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { name: { type: 'string' }, why: { type: 'string' } }, required: ['name', 'why'] } },
    pitfalls_to_avoid: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['recommended_scaffold', 'techniques', 'pitfalls_to_avoid'],
}

const CTX_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    existing_tool: { type: 'string', description: 'Summary of dev/coverage_analysis existing scripts/structure + test/ subdir, so new work builds on it and avoids duplication' },
    qc_structure: { type: 'string', description: 'Actual QC dir contents for this CGFL liquid sample (Cramino, Mosdepth files) — from S3 ls if reachable, else known structure' },
    depth_coverage_figure_canonical: { type: 'string', description: 'The canonical mosdepth depth-vs-coverage figure + exact input file(s) (e.g. *.mosdepth.global.dist.txt cumulative curve, *.mosdepth.summary.txt)' },
    golden_rules: { type: 'array', items: { type: 'string' }, description: 'One-line each, the golden rules relevant to this task' },
    scratch_conventions: { type: 'string' },
    anchors: { type: 'array', items: { type: 'string' }, description: 'Concrete exact paths/filenames/facts to embed verbatim in the prompt' },
  },
  required: ['existing_tool', 'qc_structure', 'depth_coverage_figure_canonical', 'golden_rules', 'anchors'],
}

phase('Research')
const [tech, ctx] = await parallel([
  () => agent(
    `Tu ancres les CHOIX DE TECHNIQUE DE PROMPTING pour un prompt que nous allons rédiger.\n\n` +
    `Lis ces fichiers de référence du skill prompt-creator (priorise system-prompt-patterns, anthropic-best-practices, prompt-templates, xml-structure, reasoning-techniques, clarity-principles, anti-patterns ; survole les autres) :\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/clarity-principles.md\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/xml-structure.md\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/reasoning-techniques.md\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/system-prompt-patterns.md\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/prompt-templates.md\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/anthropic-best-practices.md\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/anti-patterns.md\n` +
    `/home/blipinski/.claude/skills/prompt-creator/references/context-management.md\n\n` +
    `Le prompt à rédiger est un PROMPT DE LANCEMENT DE DÉVELOPPEMENT (agent kickoff) destiné à Claude Opus 4.8 (1M, MAX thinking), qui doit : piloter une tâche d'analyse bioinfo/R itérative ; front-loader un brainstorm + recherche de contexte (sub-agents) + plan, avec GATE D'APPROBATION explicite avant toute implémentation ; imposer un arrêt/validation après CHAQUE étape ; appliquer les Karpathy Guidelines (simplicité, changements chirurgicaux) ; respecter des règles d'or (S3 jamais de delete) ; travailler en scratch et ne copier que les livrables finaux ; documenter de façon synthétique.\n\n` +
    `Recommande le SCAFFOLD optimal (ordre des sections + balises) et les techniques précises à appliquer (avec le pourquoi), plus les anti-patterns à éviter pour CE type de prompt. Renvoie structuré.`,
    { label: 'tech-grounding', phase: 'Research', schema: TECH_SCHEMA, agentType: 'Explore' }
  ),
  () => agent(
    `Tu ancres le CONTEXTE RÉEL à embarquer dans un prompt de développement. Tout en LECTURE SEULE — n'exécute JAMAIS de rm, ni cp/écriture qui écrase un fichier existant.\n\n` +
    `1) Outil existant : explore /home/blipinski/Pipeline/Bam2Beta/dev/coverage_analysis/ (scripts : bin_one.sh, run_healthy.sh, 01_bin_perbase.sh, 02_plot_coverage.R, 03_plot_healthy_compare.R, + sous-dossier test/). Résume ce qui EXISTE DÉJÀ (binning per-base mosdepth en bins 100kb, figures cumulative + positionnelle) pour que le nouveau travail s'appuie dessus et NE DUPLIQUE PAS. Note conventions (PNG car VSCode ne lit pas les PDF, outputs gitignorés).\n` +
    `2) Structure QC du sample : essaie (best-effort, ne bloque pas si ça échoue) : AWS_PROFILE=scw aws s3 ls s3://aima-bam-data/processed/MRD/RetD/liquid/CGFL/Bladder_Urine_02_064/QC/ --recursive --endpoint-url https://s3.fr-par.scw.cloud . Confirme les fichiers réels (sous-dossiers Cramino/, Mosdepth/ ; fichiers mosdepth : *.mosdepth.global.dist.txt, *.mosdepth.summary.txt, *.regions.bed.gz et/ou *.per-base.bed.gz). Si l'accès S3 échoue, indique-le et donne la structure connue.\n` +
    `3) Figure depth-vs-coverage canonique : identifie LE fichier d'entrée et la figure de référence — la courbe cumulative de couverture issue de *.mosdepth.global.dist.txt (x = seuil de profondeur, y = fraction du génome couverte >= ce seuil), + le mean depth de *.mosdepth.summary.txt. Explique pourquoi c'est la figure la plus simple et intelligible pour biologiste/bioinformaticien, et donne le format exact des colonnes du global.dist.txt (chrom, depth_threshold, proportion).\n` +
    `4) Règles d'or : lis ~/.claude/rules/s3-safety.md, ~/.claude/rules/nextflow.md, ~/.claude/rules/secrets.md et /home/blipinski/Pipeline/Bam2Beta/.claude/rules/*.md . Résume en one-liners ce qui s'applique.\n` +
    `5) Scratch : confirme /scratch/boris/covdepth et l'existence (ou non) des sous-dossiers data/ result/ script/ (ls). Confirme aussi /home/blipinski/Pipeline/Bam2Beta/dev/coverage_analysis/test (ls, ou note s'il faut le créer).\n\n` +
    `Renvoie des ANCHORS concrets (chemins exacts, noms de fichiers, commandes types, one-liners de règles) prêts à coller dans le prompt. Structuré.`,
    { label: 'context-grounding', phase: 'Research', schema: CTX_SCHEMA, agentType: 'Explore' }
  ),
])

phase('Draft')
const draft = await agent(
  `Tu es un expert en prompt engineering (techniques Anthropic/Claude). Rédige LE PROMPT FINAL, EN FRANÇAIS (tokens techniques, chemins, commandes restent littéraux/anglais), prêt à coller, destiné à Claude Opus 4.8 (1M, MAX thinking).\n\n` +
  `Ce prompt sera donné à un agent (même classe de modèle) pour DÉMARRER le développement d'un outil d'analyse QC depth/coverage dans Bam2Beta. Il doit produire un comportement : (1) brainstorm approfondi de l'idée, (2) collecte de contexte via sub-agents de recherche, (3) proposition d'un plan de développement, (4) GATE — attendre l'approbation explicite de Boris avant toute implémentation, (5) puis exécuter UNIQUEMENT l'Étape 1, en s'arrêtant pour validation après chaque modification.\n\n` +
  `=== EXIGENCES VERBATIM DE BORIS ===\n${USER_REQ}\n\n` +
  `=== SCAFFOLD & TECHNIQUES RECOMMANDÉS (à appliquer) ===\n${JSON.stringify(tech, null, 2)}\n\n` +
  `=== CONTEXTE RÉEL ANCRÉ (chemins/fichiers/règles à embarquer) ===\n${JSON.stringify(ctx, null, 2)}\n\n` +
  `RÈGLES DE RÉDACTION :\n` +
  `- Utilise des balises XML claires (ex: <role>, <contexte>, <objectif>, <perimetre_etape_1>, <process_obligatoire>, <regles_dor>, <environnement_travail>, <criteres_de_succes>, <premiere_action>) — adapte au scaffold recommandé.\n` +
  `- Sois explicite et spécifique ; embarque les chemins/fichiers EXACTS issus du contexte ancré (sample, QC S3, scratch, dossier livrable, outil coverage_analysis existant, fichier mosdepth global.dist).\n` +
  `- Spécifie l'Étape 1 de façon précise MAIS sans sur-spécifier l'implémentation (laisse l'agent brainstormer le \"comment\" de la figure) — Karpathy: simplicité, pas de features non demandées.\n` +
  `- Mentionne explicitement : gate d'approbation AVANT implémentation, arrêt/validation après chaque modif, autorisation de paralléliser ou non, usage de sub-agents de recherche, travail en scratch + copie des livrables finaux uniquement, documentation synthétique, règles d'or S3 (lecture seule, AWS_PROFILE=scw, jamais de delete/overwrite).\n` +
  `- Définis des CRITÈRES DE SUCCÈS pour l'Étape 1 (figure claire/simple/efficace, lisible biologiste+bioinfo, relation depth/coverage mise en relief, sauvegarde scratch + copie livrable).\n` +
  `- Termine par une PREMIÈRE ACTION concrète (commencer par le brainstorm + collecte de contexte, présenter le plan, et NE PAS coder avant approbation).\n` +
  `- Pas de bla-bla méta. Le prompt doit être directement utilisable.\n\n` +
  `Renvoie UNIQUEMENT le texte du prompt final (pas de commentaire autour).`,
  { label: 'draft-prompt', phase: 'Draft', effort: 'high' }
)

phase('Verify')
const VERIFY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    final_prompt: { type: 'string', description: 'The refined, ready-to-paste final prompt in French' },
    fixes: { type: 'array', items: { type: 'string' }, description: 'Concrete fixes applied vs the draft' },
    residual_concerns: { type: 'array', items: { type: 'string' }, description: 'Anything Boris should still decide or watch out for' },
    techniques_applied: { type: 'array', items: { type: 'string' }, description: 'Short list of prompting techniques used, for the delivery note' },
  },
  required: ['final_prompt', 'fixes', 'techniques_applied'],
}
const verdict = await agent(
  `Tu es un relecteur ADVERSARIAL de prompt (rigueur maximale). Voici un BROUILLON de prompt de lancement de développement :\n\n<<<DRAFT>>>\n${draft}\n<<<END DRAFT>>>\n\n` +
  `Critique-le puis renvoie une VERSION FINALE AMÉLIORÉE (en français, prête à coller).\n\n` +
  `Checklist prompt-creator (vérifie chaque point) :\n` +
  `1. Clarté : un agent non familier pourrait-il suivre ?\n` +
  `2. Ambiguïté : une instruction interprétable de plusieurs façons ?\n` +
  `3. Complétude : critères de succès définis ?\n` +
  `4. Concision : une section coupable sans perte de sens ?\n` +
  `5. Alignement : les exemples/contraintes couvrent-ils toutes les règles énoncées ?\n\n` +
  `Contraintes DURES de Boris à garantir présentes et non ambiguës :\n` +
  `- Brainstorm AVANT tout, puis collecte de contexte (sub-agents de recherche autorisés), puis PLAN, puis GATE d'approbation explicite AVANT toute implémentation.\n` +
  `- Arrêt + validation après CHAQUE modification ; poser toute question en cas de doute.\n` +
  `- Karpathy Guidelines explicitement référencées.\n` +
  `- Étape 1 = figure R basique depth/coverage, claire/simple/efficace, lisible biologiste+bioinfo ; étapes suivantes NON encore définies.\n` +
  `- Travail en scratch /scratch/boris/covdepth (data/result/script) ; copie des livrables finaux UNIQUEMENT dans /home/blipinski/Pipeline/Bam2Beta/dev/coverage_analysis/test.\n` +
  `- Règles d'or S3 : jamais de delete/overwrite, AWS_PROFILE=scw, lecture seule sur S3 ; pas de secrets en clair.\n` +
  `- Documentation synthétique des étapes.\n` +
  `- Chemins/fichiers EXACTS présents (sample Bladder_Urine_02_064, QC S3, outil coverage_analysis existant, fichier mosdepth global.dist comme source canonique depth/coverage).\n\n` +
  `Vérifie aussi qu'il NE SUR-SPÉCIFIE PAS l'implémentation de la figure (l'agent doit garder la liberté de brainstormer le comment). Corrige tout manquement. Renvoie le prompt final + la liste des correctifs + concerns résiduels + techniques appliquées.`,
  { label: 'verify-refine', phase: 'Verify', effort: 'high', schema: VERIFY_SCHEMA }
)

return { final_prompt: verdict.final_prompt, fixes: verdict.fixes, residual_concerns: verdict.residual_concerns || [], techniques_applied: verdict.techniques_applied, draft }
