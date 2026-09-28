---
name: eacr-google-doc
description: "Google Doc EACR (ID, structure en sous-onglets) et comment y écrire — script gdoc_write.py + collage d'images via Chrome"
metadata:
  node_type: memory
  type: project
  originSessionId: fbaa2509-de79-4f95-9ddf-dec04915f149
  modified: 2026-09-28T14:02:10.494Z
---

Google Doc « EACR » = destination de la synthèse du congrès EACR Liquid Biopsies 2026 : ID `1-LLRuhheBikbs8kg2nM0cJHbIdiaViYBzPMKmiUMVqo`. Onglet parent « EACR » (t.0) = sommaire avec liens vers chaque onglet, groupés par session (source `_contexte/sommaire.md`) → 13 sous-onglets : Synthèse générale, 11 talks (titres sans heure, ex. « Lee — cfVista »), Posters. Rempli le 2026-09-28 avec 51 figures (48 dans les talks et les posters, 3 dans la synthèse générale).

Écriture : `python3 /home/blipinski/Pipeline/EACR/_contexte/gdoc_write.py` (token gspread `~/.config/gspread/authorized_user.json`, API Docs). Règle de permission dédiée dans `EACR/.claude/settings.local.json` (le mode auto bloque sinon l'usage du credential). Commandes : tabs, add-tab, append-md (onglet vide seulement), delete-tab (titre confirmé), check-figs, diff-text, clean-placeholders, code-font, fix-alerts.

L'API Docs n'insère une image que depuis une URL publique → refusé par Boris. Méthode retenue : repères `[[FIG:x:n]]` écrits par l'API, puis collage depuis le Chrome de Boris (champ fichier injecté + file_upload, focus éditeur, Ctrl+F, remplissage JS du champ « Rechercher dans le document », Escape, ClipboardEvent paste), vérification par check-figs/diff-text. Pièges vus : premier collage juste après chargement perdu dans un autre onglet ; toujours envoyer le fichier dans le même lot que le collage. Quand l'onglet Chrome est en arrière-plan (Boris utilise son navigateur), les touches réelles n'arrivent plus : méthode fiable = tout en JS dans la page (Ctrl+F simulé sur l'éditeur AVANT chaque recherche, valeur + Enter simulés dans le champ « Rechercher dans le document », Escape simulé, ClipboardEvent paste), puis contrôle API check-figs après chaque lot.

Onglet Posters (refait le 2026-09-28 à la demande de Boris) : une fiche par poster, sans vue d'ensemble ni croisement — titre, auteurs, photo du poster entier, « Idée principale » + « Pour AIMA » (2 phrases). Source : `poster/posters_fiches.md`. Mise en page « 1 page = 1 poster » : `gdoc_write.py compact-layout` (corps 9, H1 16, H2 12 avec saut de page, légende 8) + images collées en HTML avec width/height imposés (Docs respecte la taille, garde la pleine résolution) : hauteur max 520 pt (450 pour le poster 1), page A4 zone utile 451 × 698 pt. L'API ne sait pas redimensionner une image existante → recréer l'onglet.

Voir [[syntheses-science-seule]].
