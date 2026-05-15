---
name: Compte ZTHapp Supabase
description: Email du compte Boris pour ZTHapp (Supabase auth) — différent de l'email global Claude Code
type: user
originSessionId: 1475a4a7-d56a-4373-bc32-2df4b2f927e5
---
**Email Supabase pour ZTHapp** : `boris.lipinski83@gmail.com`

Ne PAS confondre avec l'email global Claude Code (boris.lipinski@aima-diagnostics.com) — ce dernier ne s'applique pas à ce projet.

À utiliser systématiquement dans :
- SQL filtrant par `auth.users.email` pour ce projet (ex: récup user_id pour insert workouts/entries/etc.)
- Toute config / instruction qui demande "ton email" dans le contexte ZTHapp
- Coach IA / context-builder si jamais on filtre user

L'email de connexion est aussi celui qui apparaît dans la sidebar / BottomNav après login.
