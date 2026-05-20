---
paths:
  - "**/*.tex"
  - "**/*.typ"
  - "**/rapport*/**"
  - "**/report*/**"
  - "**/Aima-Tower/**"
---

# Charte graphique AIMA — Éxís ctDNA

Palette hybride : structure AIMA corporate + accent produit Éxís.

## Couleurs

### AIMA corporate (structure)

| Rôle | HEX | Usage |
|---|---|---|
| Aubergine logo | `#2D1B4E` | Couleur principale du logo aima, headers dark |
| Sidebar top | `#3D1B5C` | Gradient sidebar haut |
| Sidebar bottom | `#5B1F3F` | Gradient sidebar bas |
| Coral signature | `#E85D5D` | Accent corporate, point/barre du logo, status pills (Partnerships) |

### Éxís produit (accent ctDNA)

| Rôle | HEX | Usage |
|---|---|---|
| Violet Éxís | `#5B5BD6` | Accent produit, donut TF, status badges, KPI |
| Violet deep | `#1E1E5E` | Wordmark Éxís, accent dark variant |
| Violet light | `#EEF2FF` | Background subtle pour cards Éxís |

### Neutres

| Rôle | HEX | Usage |
|---|---|---|
| slate-900 | `#0F172A` | Texte principal |
| slate-700 | `#334155` | Texte body |
| slate-500 | `#64748B` | Texte muted, labels |
| slate-300 | `#CBD5E1` | Texte tres muted, separateurs |
| slate-200 | `#E2E8F0` | Borders subtle |
| slate-100 | `#F1F5F9` | Background cards subtle |
| slate-50 | `#F8FAFC` | Background page |
| white | `#FFFFFF` | Background cards |

### Status semantique

| Rôle | HEX | Usage |
|---|---|---|
| Success green | `#10B981` | NEGATIVE result, QC OK, ✓ |
| Success light | `#D1FAE5` | Background success badge |
| Warning amber | `#F59E0B` | QC borderline |
| Warning light | `#FEF3C7` | Background warning badge |
| Danger red | `#EF4444` | POSITIVE result, QC failed, ⚠ |
| Danger light | `#FEE2E2` | Background danger badge |

## Typographie

- **Famille principale** : IBM Plex Sans (corps + display)
- **Famille mono** : IBM Plex Mono (chiffres tabulaires, codes échantillon)
- **Hierarchie suggérée** :
  - Display : 32-48pt SemiBold (résultat clé, chiffre TF)
  - H1 / Section : 14-16pt SemiBold
  - Body : 9-10pt Regular
  - Label / Small caps : 7.5-8pt Regular avec letter-spacing

## Logos

| Asset | Path | Usage |
|---|---|---|
| Logo Éxís couleur | `bin/logo/exis-color.png` | Fond clair, sur cards |
| Logo Éxís blanc | `bin/logo/exis-white.png` (à fournir) | Fond foncé, bandeau dark |
| Logo AIMA couleur | `bin/logo/aima-color.png` (à fournir) | Footer co-branding, mention corporate |
| Logo AIMA blanc | `bin/logo/aima-white.png` (à fournir) | Bandeau dark, fond foncé |

## Direction graphique

- **Light over dark** par défaut (background slate-50, cards blanc)
- **Cards rounded corners** subtiles, border `slate-200` 0.6pt
- **Pastels** pour status pills (success-light, warn-light, danger-light)
- **Coral signature AIMA** réservé aux éléments corporate (footer, mention AIMA, partnerships)
- **Violet Éxís** pour les éléments produit (TF donut, NEGATIVE/POSITIVE badge, KPI cards)
- **Dashboard moderne** style Stripe / Linear, pas Foundation Medicine traditional

## Tone of voice

- Anglais clinique RUO (Research Use Only)
- "Éxís" toujours avec accents (É et í)
- "AIMA" en majuscules (corporate name)
- "Aíma SAS" pour la mention légale RUO

## Outil cible recommandé

**Typst 0.14+** pour les rapports. Avantages :
- Pas de math mode buggé
- Unicode natif (Éxís, ≥, >, etc.)
- Layout grid moderne
- Compilation < 1 seconde
- Container léger (~80MB)

Fallback : XeLaTeX si contraintes legacy (container `blipinskiaima/rapportv3:latest`).
