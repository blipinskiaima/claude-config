---
name: Refonte rapport PDF ctDNA — Typst V2
description: Décision de pivoter de R Markdown / XeLaTeX vers Typst pour le rapport ctDNA. Direction GRAIL Galleri retenue. Source dans test/V2final/.
type: project
originSessionId: 957bf81d-a6c4-4701-a8df-8dc9a5b82a22
---
# Refonte rapport PDF ctDNA → Typst V2

**Date :** 2026-05-07
**État :** R&D, intégration pipeline prévue lundi 2026-05-11

## Contexte

Le rapport `bin/ctdna_report_template.Rmd` actuel (pdflatex via container `blipinskiaima/rapportv2:latest`) est fonctionnel mais minimaliste visuellement. Boris voulait un rendu "magnifique, moderne, à la pointe, effet wow".

## Décisions clés

### Pivot LaTeX → Typst

Tentative initiale avec XeLaTeX (`Dockerfile.rapportv3` + `bin/ctdna_report_template.v3.Rmd`) — abandonnée après 8 bugs cumulés (Unicode dans `cat()`, KPI cards cassés, math mode buggé `$>$`, fontspec capricieux, fontawesome name conflicts, `tabular` fragile, `~5M` perdu, etc.).

**Pivot vers Typst 0.14.2** (binaire Rust 40MB, compilation <1s) :
- Pas de math mode buggé
- Unicode natif (`Éxís`, `≥`, `>` sans échappement)
- Layout `grid` + `stack` modernes
- Compilation en 1 try sans bug

### Direction tonale : GRAIL Galleri

4 directions explorées en parallèle (tous dans `test/typst/`) :
- `report-stripe.typ` — dark hero monochrome
- `report-foundation.typ` — clinical numéroté 01-06 + bandes colorées
- `report-apple.typ` — minimaliste, énorme `0%` central
- `report-grail.typ` — light + Result en grande card colorée centrale

**GRAIL Galleri retenu** : Result instantanément visible, accessible patient + clinicien.

### V2 raffinée

Voir `test/V2final/report-grail-v2.typ`. Composants :
- Bandeau coral signature AIMA (4pt) en haut
- Header avec kicker `AIMA DIAGNOSTICS · ÉXÍS CTDNA` + titre `ctDNA Report` + logo Éxís 2.7cm
- Patient/Sample/Date 14pt bold (gauche/centre/droite)
- Hero card colorée (vert NEGATIVE / rouge POSITIVE) avec donut TF + ✓/✗ vectoriel cetz
- QC barres alignées (75% si OK, scaling fixe)
- Interpretation avec `*This report is not a clinical diagnostic report*` en bold
- Page 2 : sections homogènes (label small caps + texte) + 3 KPI cards 99%/100%/71% + logo AIMA 3.8cm sous RUO
- Texte 100% aligné sur l'original (`Healthy_826.merged.epic.rapport.pdf`)

## Stack technique

- **Compilateur** : Typst 0.14.2 (binaire Linux musl)
- **Package** : `@preview/cetz:0.4.2` (donut + check/cross vectoriels)
- **Fonts** : IBM Plex Sans + IBM Plex Mono (32 OTF dans `test/typst/fonts/`)
- **Container futur** : `blipinskiaima/rapportv4:latest` (Typst + cetz + IBM Plex)

## Fichiers

- **Template final** : `test/V2final/report-grail-v2.typ`
- **PDFs de test** : `test/V2final/test{1-4}_*.pdf` (NEG clean, POS clean, NEG warning, POS warning)
- **Alternatives** : `test/typst/report-{stripe,foundation,apple,grail-v1,grail-v2-stylized}.typ`
- **Backup R Markdown** : `bin/ctdna_report_template.v1.Rmd` (l'original)
- **Tentative LaTeX V3** : `bin/ctdna_report_template.v3.Rmd` (abandonné mais conservé)
- **Dockerfile LaTeX V3** : `docker/Dockerfile.rapportv3` (abandonné)
- **References** : `references/` (Foundation Medicine, Tempus, Stripe, GRAIL Galleri, Guardant360, screenshot charte AIMA)
- **Charte** : `.claude/rules/aima-brand.md` (palette AIMA + Éxís hybride)

## Intégration pipeline (à faire)

Tâche dans la todo list haute priorité, **lundi 2026-05-11** :
1. Créer `Dockerfile.rapportv4` (Typst binaire + cetz packages + fonts IBM Plex)
2. Remplacer `rmarkdown::render` dans `workflow/beta.nf:309` (process `Raima_report`) par `typst compile` avec params `--input`
3. Modifier `conf/base.config:141` + `conf/prod.config:127` → `blipinskiaima/rapportv4:latest`
4. Test final via `/test_bam2beta` sur Healthy_826
