---
name: DCATrack theme system (light + dark)
description: Comment fonctionne le toggle de thème, persistance, et bonnes pratiques pour ajouter de nouveaux composants
type: reference
---

**Thème** : light + dark via Tailwind v4 dark variant + classe `.dark` sur `<html>`.

**Configuration** dans `app/globals.css` :
```css
@variant dark (&:where(.dark, .dark *));
```

**Bootstrap anti-flash** : un script inline dans `<head>` (`app/layout.tsx`) lit `localStorage.getItem('dcatrack-theme')` ou `prefers-color-scheme` et applique `.dark` AVANT le rendu.

**Toggle** : `app/components/ThemeToggle.tsx` (Client Component) gère :
- État `theme: "light" | "dark"`
- `getInitialTheme()` lit localStorage puis fallback sur `prefers-color-scheme`
- `useEffect` synchronise la classe `.dark` sur `documentElement` + persiste dans localStorage
- SSR-safe : retourne un placeholder pendant `!mounted` pour éviter le mismatch d'hydration

**Variables CSS** pour les composants qui ne peuvent pas utiliser `dark:` (ex: Recharts) :
- `--chart-tooltip-bg`, `--chart-tooltip-border`, `--chart-tooltip-text`, `--chart-tooltip-label`
- Définies dans `:root` (light) et redéfinies dans `html.dark`

**Convention pour ajouter un nouveau composant** :
1. **Background** : `bg-white/70 dark:bg-zinc-900/40` ou `bg-zinc-100 dark:bg-zinc-900/60`
2. **Border** : `border-zinc-200 dark:border-zinc-800`
3. **Text principal** : `text-zinc-900 dark:text-zinc-100`
4. **Text secondaire** : `text-zinc-700 dark:text-zinc-400`
5. **Text muted** : `text-zinc-500` (même valeur dans les 2 modes — déjà neutre)
6. **Accent positif** : `text-emerald-600 dark:text-emerald-400`
7. **Accent négatif** : `text-rose-600 dark:text-rose-400`
8. **Accent warning** : `text-amber-600 dark:text-amber-400`

`verdictMeta` dans `app/lib/score.ts` retourne déjà des classes light+dark prêtes à l'emploi pour les verdicts 🟢🟡🔴.

**Couleurs des cards par ETF** (`colorFor` dans `app/lib/colors.ts`) — ces couleurs sont des hex utilisés par Recharts en `stroke`/`fill`. Elles sont volontairement vives pour rester lisibles en light comme en dark. Ne pas les changer selon le thème.

**Gotcha SVG icons** : utiliser `currentColor` pour `stroke`/`fill` dans les icônes inline → la couleur s'adapte automatiquement via la classe `text-*` du parent.
