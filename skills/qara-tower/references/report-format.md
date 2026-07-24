# Gabarit de la synthèse QARA

La synthèse est un **texte brut** (pas de HTML) ajouté à la fin du Google Doc via
`append_gdoc.py`. Ton vulgarisé, pour un lecteur non-data-scientist (QA/RA). Concis :
une demi-page à une page. Écrire dans un fichier (ex `/tmp/qara_bloc.txt`) puis l'ajouter.

Le **titre** (option `--title`) est passé séparément et mis en gras automatiquement ; ne pas
le répéter dans le corps.

## Structure

```
Titre (via --title) :  QARA — <timestamp>  (T<n> vs T<n-1>)

1. En-tête          : période couverte (de T_{n-1} à T_n), nombre de nouveaux
                      échantillons trace-prod.
2. Métriques clés   : tableau texte seuil / sensibilité / spécificité / effectifs,
                      avant → après (Δ). Signaler ce qui NE bouge pas aussi.
3. Explication      : d'où viennent les variations, en nommant les échantillons
                      (entrants, changements de statut). Relier chaque Δ à sa cause.
4. Verdict QARA     : la performance est-elle stable ? Un écart mérite-t-il attention ?
```

## Règles de rédaction

- **Nommer les échantillons** qui expliquent un delta (c'est le cœur de la traçabilité).
- **Relier chaque variation à sa cause** : un `+2 cancers` doit être justifié (2 entrants,
  ou 1 entrant + 1 `sans_etiquette→cancer`…).
- **Signaler la stabilité** : si le seuil ou la spécificité ne bougent pas, le dire — c'est
  une information QARA en soi.
- **Ne rien inventer** : si le diff ne permet pas d'expliquer un écart, l'écrire franchement
  et proposer une vérification, plutôt que de supposer.
- **Pas de jargon** : « cohorte de calcul », « échantillons sans étiquette », plutôt que les
  noms de variables du code.

## Exemple (T1 fictif)

Titre : `QARA — 2026-08-01T09:00Z  (T1 vs T0)`

```
Période : du 24/07/2026 au 01/08/2026. 5 nouveaux échantillons enregistrés dans
trace-prod (1 471 → 1 476), dont 3 entrent dans l'analyse.

Métriques (mode Exis : mVAF v1.4, cohorte Avancés, 95 %)
  Seuil de positivité   0,0042 %   →   0,0042 %      (inchangé)
  Cohorte cancers       261        →   264           (+3)
  Cohorte sains         224        →   224           (inchangé)
  Sensibilité           82,0 %     →   82,2 % (217/264)
  Spécificité           95,1 %     →   95,1 % (213/224)   (inchangée)

Origine des variations
  +3 cancers = 2 nouveaux échantillons entrés directement en cancer
  (CGFL_Colon_71, HCL_Lung_88) + 1 échantillon déjà présent passé de
  « sans étiquette » à « cancer » (CGFL_Prostate_30, dossier clinique complété).
  Les 2 autres nouveaux échantillons trace-prod n'entrent pas dans l'analyse
  (profondeur insuffisante).

Verdict QARA : performance stable. Le seuil et la spécificité sont identiques ;
la sensibilité varie de +0,2 pt, entièrement expliquée par les 3 cancers ajoutés,
tous détectés. Aucun point d'attention.
```

## Après la rédaction

Une fois le bloc ajouté au Doc (étape 4 du workflow), **journaliser** le snapshot
(`snapshot.py --persist-file`) puis **committer** le journal. Ne jamais inverser cet ordre.
