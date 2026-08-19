---
name: feedback_doc_concision
description: "Dans un texte de restitution (Google Doc), une case/categorie qui ne s'explique pas en une phrase doit etre retiree, pas expliquee plus longuement"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 26ddc2c6-4453-4f2c-8844-a7dbb79c1a63
  modified: 2026-08-17T14:14:20.467Z
---

Quand une case d'interpretation ou une statistique ne se comprend pas au premier coup d'oeil
dans un texte destine a etre lu (Google Doc, rapport), **la retirer plutot que la re-expliquer**.
Ne pas empiler les clarifications (schema ASCII, reformulations successives) sur un concept que
le lecteur ne saisit pas d'emblee.

**Why:** session du 2026-08-17, recensement QC des Lung_Alc. Une case « Mixte » du tableau
(echantillons anormaux qui cumulent deux defauts sans franchir aucun des deux seuils pris
isolement) a demande 3 tentatives d'explication (texte, schema ASCII, reformulation en une
phrase) sans que Boris la comprenne — *« non c'est trop compliquer je comprend pas »*. Boris a
tranche seul, en editant le document a la main : il a **supprime toute la case et son axe**
(avec les 21 aberrants Tukey qui allaient avec), plutot que de continuer a en discuter. Le
tableau et le texte publies sont ressortis plus courts et plus clairs que ma version, malgre
la perte d'exhaustivite statistique.

**How to apply:**
- Un texte de restitution vise un lecteur qui doit comprendre **au premier passage**, pas un
  rapport d'analyse exhaustif. Voir aussi le ton deja etabli dans [[gdoc-qc-ratio-n50]] :
  phrases courtes, une idee par puce.
- Si une case/categorie exige plus de 2 lignes ou une deuxieme metrique pour se definir
  ("ni l'un ni l'autre des deux seuils, mais leur somme depasse..."), c'est un signal pour la
  retirer du livrable, pas pour mieux la formuler.
- Garder la mesure sous-jacente en memoire projet (elle reste vraie et peut resservir), mais ne
  pas la republier dans un document dont Boris a deja simplifie le contenu — verifier l'etat
  reel du document avant de reciter une ancienne version, cf. [[feedback_gdoc_no_overwrite]].
- Ne pas persister a expliquer un point deja qualifie de "trop compliqué" une seconde fois de la
  meme maniere — changer de strategie (retirer, ou proposer une alternative radicalement plus
  simple) des le premier signal d'incomprehension repete.
