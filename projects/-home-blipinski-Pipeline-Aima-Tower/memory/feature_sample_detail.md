---
name: feature-sample-detail
description: Tower v4.2.0 — pages /samples + /sample/:id (liste + detail enrichi). Decisions de design et conventions trace-prod intégrées au front.
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c624d9b-b50c-4a91-8e32-49096a3ef4d5
---

Tower v4.2.0 ajoute deux pages : `/samples` (liste AG Grid-like des ~1100 samples R&D) et `/sample/:id` (détail enrichi, reproduit le mockup `aima-tower-sample-detail.html` avec les KPI trace-prod).

**Why:** Boris voulait industrialiser le mockup HTML standalone en pages React intégrées à Tower, exposant l'intégralité des champs metadata + qc_metrics + retd_suivis + bam_metadata d'un sample en un seul endroit.

**How to apply:**
- Backend : `DatabaseService.get_sample_detail(sample_name)` fait un JOIN 5 tables avec alias `m.dorado_version as metadata_dorado_version` pour éviter collision avec `b.dorado_model_version`
- Frontend type `SampleDetail` dans `frontend/src/lib/samples.ts` — attention aux duplicates si on ajoute des champs déjà retournés par `b.*`/`q.*`
- Helpers VARCHAR-with-comma → number : `parseEuFloat()` pour `ichorcna_score`, `mvaf_v12`, `frag_mode1/2`

## Décisions UI (Boris)

- **Tumor Fraction** affiche `mvaf_v1` directement (PAS `ichorcna_score`) — `parseEuFloat(ichorcna)` retiré
- **Badge Negative/Positive** strict : `mvaf_v1 == 0` → Negative vert | `mvaf_v1 > 0` → Positive rouge | null → N/A
- **Depth threshold = 0.25×** (pas 30× ni 15×) — `≥ 0.25 = OK`, sinon KO. Appliqué dans KPI card et QC checklist
- **Pas de Footer custom** dans SampleDetail.tsx — le `<Footer />` global de App.tsx suffit (sinon doublon "aíma Diagnostics · RUO")
- **Layout bento 12-col** unique (gap-4) au lieu de Cards stacked avec space-y-7 — moins long visuellement
- **Couleurs pastel hex direct** (`#D1FAE5`, `#FEE2E2`, `#FEF3C7`) car Tower n'a que `--aima-emerald-500/700` (pas de `-100`)
- **Badge & pills sans border** — fond pastel suffit visuellement (mockup ne met pas de border)

## Conventions paths S3 trace-prod

```
Base : s3://aima-bam-data/processed/MRD/RetD/{sample_type}/{labo}/{sample_name}/
Rapport : {base}/REPORT/   (dossier — Scaleway liste les PDF)
Log     : {base}/LOG/      (non utilisé en V1, bouton remplacé par Trace prod)
```

- Bouton **Trace prod** pointe vers la gsheet Google Sheets fixe (`docs.google.com/spreadsheets/d/1gm_vB7vTzAq38dgkJFNpgA3Cy_XRlUqunMgoBvKnh6M`) en violet primary `var(--aima-violet-600)` (≈ bouton primary mockup)
- Bouton **Exporter rapport** pointe vers le dossier `REPORT/` (Boris a refusé le PDF direct car le pattern de nom variait)

## Animation aima-rise cascade

Pour reproduire l'effet du mockup HTML (`@keyframes rise` translateY 8px → 0, 0.5s ease-out cubic, délais 0.02s → 0.30s) :
- Tower a déjà la classe `.aima-rise` avec `animation-delay: calc(var(--idx, 0) * 0.04s)`
- Sur SampleDetail.tsx : wrap chaque bloc avec `<div className="aima-rise" style={{ "--idx": N } as React.CSSProperties}>` (idx 1→8)
- Pour rejouer l'animation à chaque navigation : `key={location.pathname}` sur le wrapper qui contient `<Routes>` dans App.tsx — force démontent + remont. Active sur toutes les pages.

Voir aussi : [[feature-cohort-cascade-integration]] pour autre feature qui utilise un layout dense.
