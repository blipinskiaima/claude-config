---
name: migration-platform-v15-upload-date
description: Migration trace-platform v15 (upload_date droppee) et le catch-all qui transformait la panne en page vide mensongere
metadata: 
  node_type: memory
  type: project
  originSessionId: 48047037-2961-4d87-8ce6-760c15fafa5f
  modified: 2026-09-18T12:07:50.377Z
---

Le 2026-09-17, la migration **v15** de trace-platform (`lib/platform_db.py`,
`_migrate_v14_to_v15`) a **droppé** deux colonnes de `samples` :

```
creation_date  ->  copy_start
upload_date    ->  copy_stop
```

Corrigé côté Tower le 2026-09-18. Le schéma courant est **v22** ; entre v15 et v22 toutes
les migrations n'**ajoutent** que des colonnes — v15 est la seule à supprimer (avec v11,
qui avait retiré `report_date` bien avant, et que la Tower ne référençait pas).

## Le remplaçant se lit dans trace-platform, pas dans l'intuition

Le commit `43089a3` de trace-platform s'applique à lui-même la substitution, **fallback
compris** :

```
-  COALESCE(s.upload_date, s.created_at) AS arrivee
+  COALESCE(s.copy_stop,   s.created_at) AS arrivee
```

La Tower reprend donc `COALESCE(s.copy_stop, s.created_at) as arrivee`. ⚠ **Sans le
COALESCE, 121 samples sur 373 (32 %) s'affichent vides** : `copy_stop` n'existait pas avant
v15, les échantillons antérieurs ne l'ont jamais renseigné. Le fallback n'est pas un ajout
de confort, il était déjà là avant la migration.

Vocabulaire unique de bout en bout (leçon [[migration-v34-colonnes-reads]]) : `arrivee`
en SQL, dans le JSON, dans le type `PlatformRow` et dans le libellé UI « Arrivée ».

## ⚠ Le vrai défaut n'était pas la colonne, c'était le catch-all

`PlatformService.get_samples_overview()` avait un `except Exception: return []` que **aucun
autre lecteur DuckDB du projet n'a** — `DuckDBMixin._query()` retry l'`IOException` puis
fait `raise last_error`. Chaîne complète du silence :

```
Binder Error  ──►  except Exception: return []
       ↓
GET /api/databases/platform/overview  ──►  200 []      ← pas une erreur HTTP
       ↓
TanStack : isError = false, data = []
       ↓
PlatformView : sliced.length === 0
       ↓
« Aucune analyse correspondante. »
```

⚠ **La page ne se contentait pas d'être vide : elle affirmait que le filtre n'avait rien
matché.** Une panne indiscernable d'un filtre trop restrictif — pire qu'un écran blanc.
Même famille que le `try/except: description = ""` d'[[analytics-ia-hardening]].

## ⚠ Lever l'erreur au backend ne suffit pas

`PlatformView` n'avait **aucune branche `isError`** : `const data = overview.data ?? []`
renvoyait le 500 exactement sur le même message. Corriger le service seul aurait remplacé
un mensonge par le même mensonge. Les deux moitiés vont ensemble :

- service : plus de catch-all, même forme que `_query()`
- UI : branche `isError` (`--aima-rose-500` + `String(query.error)`, pattern déjà présent
  dans `Competitors.tsx` et `Survey.tsx`)

Le même traitement a été appliqué le même jour à **`WorkflowService`** (`get_running_workflows`,
`get_completed_workflows`, `get_sync_state`) et aux trois zones correspondantes de
`Monitoring.tsx`. Effet de bord utile : `running : 0` est désormais une **information** —
sans catch-all, l'absence d'exception prouve que la requête a tourné. Retirer les trois
`logger.error` a rendu `import logging` orphelin dans `services.py`, supprimé aussi.

## ⚠ Le typecheck ne protège pas d'un renommage

`PlatformRow` est un `Record<string, unknown> & { … }` : un champ renommé à moitié passe
`tsc` sans un bruit et sort en `undefined` → « — ». La preuve d'un renommage se fait au
**runtime** (la clé `upload_date` absente du payload), jamais au typecheck.

## Ne pas chercher là

`src/callbacks.py:1316` lit encore `upload_date` : code **mort**. `app.py` / `pages.py` /
`callbacks.py` sont le trio Dash legacy, jamais importés par `backend/`. Les `report_date`
de `survey_service.py` sont une variable locale sans rapport avec la base platform.
