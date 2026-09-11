---
name: database-scission-pages
description: "Scission de /database en deux pages autonomes (R&D et Plateforme) et affichage de l'ID sample dans Monitoring."
metadata:
  node_type: memory
  type: project
  modified: 2026-06-24T00:00:00.000Z
---

# Scission `/database` + ID sample Monitoring (2026-06-24)

La page `/database` à onglets est **scindée en deux pages autonomes** :

- **R&D** — `/database`, ex-onglet R&D, `Database.tsx` nettoyé de ses onglets
- **Plateforme** — `/database-platform`, nouveau `DatabasePlatform.tsx` qui wrappe `PlatformView`

Deux entrées de sidebar dans le groupe monitoring, libellés **« R&D »** (FlaskConical) et
**« Plateforme »** (Building2), **sans le mot « Database »**. Les titres `h1` des pages, eux,
gardent « Database R&D » / « Database Plateforme » : seuls les libellés de sidebar sont
raccourcis.

**Zéro backend** : `SamplesView` et `PlatformView` étaient déjà des composants autonomes, et
les endpoints `/api/databases/*` (R&D) et `/api/databases/platform/*` étaient déjà séparés.
La scission est donc un simple wrapping. Route ajoutée dans `App.tsx` (branche `path="*"`,
max-w 1280). Pas de redirection de l'ancienne URL.

## Monitoring › Récents — ID sample

L'**ID sample est affiché à droite** de `CompletedRow`. Source : **`--patient_id` parsé dans
`wf.command_line`** (regex `--patient_id[=\s]+(\S+)`, `—` si absent).

⚠ Choix Boris : la **command line Nextflow**, et **pas** `params_json`. Conséquence assumée :
3 vieux workflows sans `command_line` affichent `—`.
