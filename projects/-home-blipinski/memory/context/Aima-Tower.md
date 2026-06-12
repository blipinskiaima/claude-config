# Context — Aima-Tower — 2026-06-12T14:02:07+00:00

**Branche** : main (synchro origin/main)
**Dernier commit** : 5744647 — feat(scaleway): désactive les liens cliquables vers la console Scaleway
**Status** : 6 fichiers modifiés non commités (WIP exploration-beta, session précédente)

## Où j'en suis
Feature **« désactivation des liens cliquables Scaleway »** terminée, commitée (5744647), **poussée**
et déployée (container `aima-tower-dashboard` rebuildé + healthy). Les chemins S3 restent affichés en
texte mais ne sont plus cliquables. Le travail **exploration-beta** (6 fichiers, courbes Plotly /
cohortes speedvac) reste **non commité** — c'est le WIP de la session précédente, à reprendre/finir.

## Ce qui marche / ce qui foire
- ✓ `/database›Platform` + `/monitoring` : liens `<a>` → `<code>` texte non cliquable (chemin S3 brut)
- ✓ `/sample/:id` : bouton « Exporter rapport » retiré (« Trace prod » Google Sheets conservé)
- ✓ Dash legacy `callbacks.py` neutralisé par cohérence (html.A Scaleway → html.Span path S3)
- ✓ Helpers `s3ToScaleway` / `_s3_to_scaleway` supprimés ; icône « Chemins » Monitoring → `Folder`
- ✓ Build front OK + docker rebuild + redéploiement healthy ; doc CLAUDE.md/README MAJ
- ✓ Commit 5744647 ciblé (7 fichiers) **poussé sur origin/main** ; tag rollback `pre-disable-scaleway`
- ⚠ 6 fichiers exploration-beta toujours non commités (WIP, intacts)

## Prochaine étape
Reprendre le WIP exploration-beta : vérif visuelle des courbes sur quelques combos bench (pas seulement
mvaf_v1), puis commit.
