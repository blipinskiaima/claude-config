# Projet : Home Boris Blipinski

## Contexte utilisateur

Boris Blipinski est **Bioinformaticien** chez **AIMA Diagnostics**, startup de diagnostic cancer par analyse de méthylation ADN (séquençage Nanopore ONT + Illumina).

- **Supérieur direct** : Michael (CTO)
- **Équipe core** : Florian (Data Science/ML), Fred (DevOps/Full-Stack), Arnaud (Fondateur/Business), Romain (PROD CGFL), Léa (PROD HCL)

## Structure des données

### Notes personnelles
- `~/boris_notes_extract.txt` — 2590 lignes, ~75 entrées daily standup (sept 2025 – mars 2026). Format : `# JJ mois. AAAA` puis listes `[x]`/`[ ]`/`~~strikethrough~~`.
- `~/Notes_Team_Meetings.txt` — Réunions d'équipe 2026
- `~/Notes_Team_Meetings (1).txt` — Réunions d'équipe 2025

### Projets Pipeline
14 projets dans `~/Pipeline/`, tous avec Boris comme auteur unique :

| Projet | Type | État | Complexité |
|--------|------|------|------------|
| Bam2Beta | Pipeline Nextflow méthylation ONT | Production V1.0.1 | Très élevée (34 processus) |
| Pod2Bam | Pipeline re-basecalling GPU | Production V0.1.0 | Moyenne |
| Aima-Tower | Dashboard monitoring Dash/Plotly | Production V2.2.0 | Élevée |
| trace-prod | CLI tracking R&D (DuckDB) | Production | Élevée |
| trace-platform | CLI tracking clients (DuckDB) | Production V0.1.0 | Moyenne-haute |
| trace-workflow | Cache daemon Seqera (DuckDB) | Production | Moyenne-haute |
| Watchmaker | Pipeline TAPS+ Illumina | Dev V1.0.0 | Moyenne |
| Methylseq | Fork nf-core bisulfite | Dev/Recherche | Très élevée |
| short-read | Benchmark 4 pipelines | Recherche | Moyenne |
| batch_effect | Analyse effets de lot | Recherche | Basse |
| SampleSheetChecker | Validation TSV + sync S3 | Production | Moyenne |
| basecall | Re-basecalling standalone | Legacy | Moyenne |
| Fastq2Bam | Pipeline alignement short-read | Dev V0.0.0 | Moyenne-haute |

## Conventions

- Boris prend ses notes en français, les README/code sont souvent en anglais
- Daily notes : `[x]` ou `~~strikethrough~~` = tâche complétée, `[ ]` = en cours/todo
- Stack principal : Nextflow DSL2, Python (Click, DuckDB, Dash), R (raima), Docker, AWS S3/Scaleway S3
- Langue de conversation préférée : français
