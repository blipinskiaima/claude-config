---
name: Design system ZTH (Editorial Sport)
description: Tokens, fonts, composants signatures et patterns de la refonte Phase 6. Réutiliser pour toute nouvelle UI.
type: project
originSessionId: 1475a4a7-d56a-4373-bc32-2df4b2f927e5
---
Refonte UI complète effectuée Phase 6.1 + 6.2 (commits 5452d1a, 13fe7d8, ff6daf2) — Direction "Editorial Sport" : **light éditorial premium + dark ardoise coach**, inspirée du PDF Zero To Hero.

**Why:** Boris jugeait l'app trop ressemblante à DCATrack (palette ambre, glassmorphism, Geist, donut multicolore). Il voulait une identité ZTH explicite — teal pétrole, Anton condensed, photos lifestyle, tableaux noirs sport.

**How to apply:** Toute nouvelle vue/composant doit réutiliser les tokens et composants ci-dessous. Ne jamais réintroduire amber/emerald/zinc/Geist/backdrop-blur/rounded-2xl.

## Tokens (définis dans app/globals.css)
- `--zth-bg` (#FAFAF7 / #0E1316) — fond global, classe `bg-bg`
- `--zth-surface` (#FFFFFF / #161D21) — cards, classe `bg-surface`
- `--zth-surface-2` (#EAF1F3 / #1E272C) — surfaces secondaires (bleu poudré PDF), classe `bg-surface-2`
- `--zth-border` (#D8DDE0 / #2A343A) — séparateurs, classe `border-border`
- `--zth-fg` (#1A1F24 / #ECEFF1) — texte principal, classe `text-fg`
- `--zth-fg-muted` (#5A6168 / #9AA3A9) — texte secondaire, classe `text-fg-muted`
- `--zth-primary` (#2F6770 / #4FA0AB) — teal signature ZTH, classe `text-primary` `bg-primary` `border-primary`
- `--zth-accent` (#C9A96A / #D6BE8E) — doré champagne, UNIQUEMENT sous-titres et accents (jamais CTA), classe `text-accent`
- `--zth-ink-strong` (#0A0A0A) — fond noir des "tableaux ardoise coach" (header séance), classe `bg-ink-strong`
- `--zth-on-primary` (#FFFFFF / #0A0A0A) — texte sur fond teal, classe `text-on-primary`
- `--zth-on-ink` (#FFFFFF) — texte sur fond noir, classe `text-on-ink`

## Fonts (chargées dans layout.tsx)
- **Anton** (Google Fonts, weight 400 single) — display condensed uppercase. CSS var `--font-anton`. Classe utility `zth-display` (caps + line-height 0.92 + tracking 0.01em).
- **Inter** (weights 400/500/600/700) — corps, labels, sous-titres. CSS var `--font-inter`. Classe `font-sans` par défaut.
- Tabular nums via classe `zth-num` (font-variant-numeric: tabular-nums).
- Sub-display uppercase tracking large via classe `zth-eyebrow` (Inter 700 + uppercase + tracking 0.18em + 0.7rem). Parfait pour labels et titres de section.

## Composants signatures (app/components/ui/)
Réutiliser ces composants au lieu de réinventer :
- `<TealPill variant="outline|solid|ghost" size="sm|md|lg">` — label rectangulaire teal caps tracking large. Pour labels meta, CTAs secondaires, titres en pilule.
- `<KcalBadge kcal={123} size="sm|md|lg" />` — cercle teal 64px en overlay sur photos.
- `<DishCard title kcal macros imageSrc>` — card recette avec photo + KcalBadge + macros bleu poudré. Usage `<Link href>` ou clic.
- `<SessionTable>` + `<SessionRow>` + `<SessionCell>` — tableau noir headers teal (look "ardoise coach" PDF). Pour catalog statique d'exercices.
- `<PageHero eyebrow title subtitle trailing>` — titre Anton géant + sous-titre doré tracking large. À utiliser EN HAUT de chaque route.
- `<SynthBlock label>{children}</SynthBlock>` — section avec titre Anton + trait horizontal (style "SYNTHÈSE" PDF).
- `<TealFooterBand>` — bandeau pleine largeur teal en pied de page. Termine chaque route majeure.
- `<StatBigNumber value unit label helper emphasis>` — chiffre Anton XL + label caps tracking large. Pour KPIs.
- `<BottomSheet open onOpenChange title description>` — wrapper vaul Drawer. **Préférer pour modals mobile** plutôt que centré (UX mobile bien meilleure).

## Charts (Recharts mappé palette ZTH)
- Tooltip via vars CSS `--chart-tooltip-bg/border/text/label`
- Donut macros : 3 nuances de teal `var(--pie-prot/gluc/lipi)` (jamais multicolore)
- Lines / bars : `stroke="var(--zth-primary)"`, fill `var(--zth-primary-soft)` pour les valeurs en dessous de cible
- Reference lines : `stroke="var(--zth-accent)"` (doré pour seuils/cibles)

## Anti-patterns à fuir (codes DCA proscrits)
- `amber-*`, `emerald-*`, `violet-*`, `rose-*`, `sky-*` en CSS — jamais. Tout passe par tokens.
- `bg-white/70 backdrop-blur` (glassmorphism) — aplats opaques uniquement.
- `rounded-2xl`, `rounded-xl` — utiliser `rounded-md` ou `rounded-sm`, voire pas de radius (`rounded-none`).
- `bg-gradient-to-*` ambre/orange — aplats only.
- `font-mono` (Geist Mono) — utiliser `zth-num` (Inter tabular-nums) à la place.
- Donut multicolore P/G/L — 3 nuances de teal seulement.
- Couleurs sémantiques (emerald=ok, rose=erreur) — utiliser primary (positif) + accent (warning/négatif). ZTH n'a pas de palette feedback color.
- `text-2xl font-bold tracking-tight` pour titres de page — utiliser `<PageHero>`.

## Méthode de refonte validée
Side-by-side : design system d'abord (Phase A : tokens + fonts + composants atomiques + dashboard pilote pour validation utilisateur), puis migration des routes une par une (Phase B). Préserve la logique métier (lib/) intacte — refonte purement UI/CSS.

Pattern `npm run build` + commit + push Vercel à chaque checkpoint validé (jamais `npm run dev` sur cette machine — voir feedback_no_local_dev_server.md).
