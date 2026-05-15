---
name: DCATrack side menu (drawer)
description: Drawer principal accessible depuis ☰ dans le header de toutes les pages, contient nav + actions
type: reference
---

**Composant** : `app/components/SideDrawer.tsx` exporte :
- `SidePanel` : composant tout-en-un (sidebar desktop + drawer mobile + bouton ☰ flottant). Inclus une seule fois dans `app/layout.tsx`.
- `MenuButton` : alias de `SidePanel` (compat ascendante).

**Comportement responsive** :
- **Desktop (≥ 1024px)** : sidebar fixe permanente à gauche, toujours visible. Largeur `var(--sidebar-w)` = 16rem (déplié) ou 4.5rem (replié). Bouton "Replier / Déplier" en bas. Repliée → icônes seuls + tooltips hover. Le contenu pousse via `body { padding-left: var(--sidebar-w) }`.
- **Mobile / tablette (< 1024px)** : sidebar = drawer overlay. Bouton ☰ flottant en haut-gauche (`fixed top-3 left-3 lg:hidden`) déclenche l'ouverture. Backdrop + Escape ferment.

**Persistance** :
- État replié/déplié dans `localStorage` clé `dcatrack-sidebar`
- Bootstrapé dans un script inline dans `<head>` (`app/layout.tsx`) pour éviter le flash

**CSS** dans `app/globals.css` :
```css
:root { --sidebar-w: 16rem; }
@media (min-width: 1024px) {
  body {
    padding-left: var(--sidebar-w);
    transition: padding-left 200ms ease-out;
  }
}
```

**Structure du drawer** :
1. Header : brand "DCATrack" gradient + bouton fermer ✕
2. Section "Navigation" :
   - 🏠 Vue Générale → `/`
   - 📊 DCATrack → `/tracker` (indicateurs sans Profil)
   - 🥧 Profil DCA → `/profil`
3. Section "Plus" :
   - ❓ Aide → `/aide`
   - ⚙️ Paramètres → `/parametres`
   - ℹ️ À propos → `/a-propos`
4. Section "Actions" :
   - 🔄 Actualiser (Server Action `refreshETFs`)
   - 🌗 Mode sombre/clair (avec switch visuel, lit/écrit `localStorage` clé `dcatrack-theme`)
5. Footer : "Données justETF · Cache 1h · POC"

**Comportement** :
- Backdrop noir 50% opaque + blur léger ; click dehors ferme le drawer
- Escape ferme le drawer
- Body scroll lock pendant l'ouverture (évite le scroll en arrière-plan)
- Active link mis en évidence (background ambre + dot) selon `pathname`
- Click sur un lien de nav ferme le drawer automatiquement
- Theme toggle inline (logique répliquée depuis ThemeToggle.tsx, intentionnellement self-contained pour éviter une dépendance fragile)

**Vues accessibles** :
- `/` (Vue Générale) : StrategySummary + Tracker (avec badges DCA)
- `/tracker` : Tracker seul, `showStrategyBadge={false}` sur les cards, message "vue indépendante du Profil DCA"
- `/profil` : `ProfileTabs` → `ProfileList` (grille de cartes profils) + état view/edit/create via `mode` state machine
- `/etf/[isin]` : page détail ETF (gros chart + breakdown)
- `/aide`, `/parametres`, `/a-propos` : pages secondaires (Server Components, contenus statiques)

**Suppression de composants devenus inutiles** :
- `ProfileLink.tsx` : remplacé par le nav du drawer (le composant existe encore mais plus importé)
- `ThemeToggle.tsx`, `RefreshButton.tsx` : leur logique est inline dans le drawer (composants existent mais plus importés). Peuvent être supprimés en cleanup.

**Pour ajouter un nouveau lien dans le drawer** : ajouter une entrée dans `NAV` (nav principale) ou `SECONDARY_NAV` (section Plus) dans `SideDrawer.tsx`. Format `{ href, label, description, icon: ComponentRendererInline }`.
