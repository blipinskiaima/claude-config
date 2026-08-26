---
name: dossiers-concurrent-p1p2p3
description: "Architecture des dossiers concurrent P0/P1/P2/P3, les deux régimes d'écriture, et les pièges qui ont coûté cher"
metadata: 
  node_type: memory
  type: project
  originSessionId: fdd4f2ac-8635-4303-a86c-70045baa73f3
  modified: 2026-07-30T06:44:09.189Z
---

`concurency/profils/{SLUG}-P{0,1,2,3}-*.md` — **8 concurrents × 4 parties** (Biodesix ajoutée le
2026-08-26). `SLUG` = nom canonique en majuscules, espaces → tirets. Servis par Aima-Tower sur
`/profils`, onglet « Deep dive concurrent », un dossier par concurrent, PDF téléchargeable.

⚠ **Le slug est un contrat avec la Tower**, pas un choix libre : validée contre
`^[A-Z0-9-]{2,40}$`, elle affiche `slug.replace("-"," ").title()`. C'est le nom de la **société**
(`GUARDANT-HEALTH`), jamais du produit (`GUARDANT-SHIELD`, forme des rapports gelés de juillet),
et il doit égaler le champ `name` de `competitors.json` sinon le dossier se dédouble dans l'onglet.

**Deux régimes d'écriture qu'il ne faut jamais confondre :**

⚠ **Les QUATRE parties sont écrites par Claude.** La distinction n'est pas « humain contre
machine », c'est le **rythme** — erreur que la doc portait jusqu'au 2026-07-30.

| | écrit par | rythme |
|---|---|---|
| P1 technique, P2 marché | skill `deep-dive-concurency`, puis vérifiés | sur décision, jamais auto |
| P0 faits majeurs, P3 trajectoire | `cli.py competitive-profil`, dérivées de `competitive_events` | cron lundi 10h00 |

⚠ **Un P0 vide n'est pas une panne.** « Majeur » = ce qui change leur droit de vendre ou qui
paie : autorisation, recommandation professionnelle, remboursement. Une société qui vend en LDT
sans jamais déposer de dossier n'en produit aucun — vérifié sur Biodesix, **zéro fait majeur sur
60 mois** pour 44 évènements collectés, et c'est le portrait fidèle de l'entreprise. Même cas
chez Geneseeq. Guardant, qui dépose, a un P0 fourni.

⚠ **Le PDF n'est produit que si un `P1-TECHNIQUE.md` existe** (`run_profils.sh` boucle dessus).
Un concurrent dont seuls P0 et P3 sont générés n'aura jamais de PDF, et la Tower affichera
« PDF non généré » — c'est voulu, pas un incident.

Un texte qui se réécrit tout seul finit par contenir une erreur que personne ne voit passer —
d'où P1/P2 gelés. Le lien se fait par la §4 de la P3, qui **signale** sans réécrire.

**Trois pièges mesurés, chacun a failli passer :**

1. **Borner la P3 par indication est faux.** `autre` veut dire « aucun de nos trois organes
   nommé », jamais « hors sujet ». Sur Natera, couper là-dessus supprimait l'approbation PMA du
   CDx Signatera, la recommandation NCCN vessie et le jugement de royalties. Le bon axe est la
   **ligne de produit** (`hors_perimetre` dans `data/competitors.json`), avec une **garde
   oncologique** : un titre qui nomme un cancer n'est jamais écarté, même s'il dit « kidney ».
2. **`concurency/pdf/*.pdf` (racine) est une ARCHIVE du 2026-07-23**, bâtie avant la
   vérification adversariale. Les PDF courants vivent dans `pdf/profils/`. Servir les premiers
   livrerait la version sans les 117 corrections.
3. **Les marqueurs de preuve doivent être accentués** — `[SOURCÉ]`, pas `[SOURCE]`. Le
   rédacteur Freenome en avait écrit 236 sans accent : tout filtre sur la forme accentuée les
   aurait ignorés en silence. Même famille que le bug `_RE_FILS`.
4. **La légende n'a pas de forme unique.** Selon le dossier c'est une citation de 2, 3 ou 4
   lignes — ou un **tableau** (les deux Freenome). Un motif ancré ligne par ligne n'en
   attrapait que 8 sur 14 : les 6 autres auraient gardé l'ancienne légende au-dessus de
   marqueurs convertis, en silence. Repérer l'ÉTENDUE du bloc, jamais sa mise en page.

**Taxonomie ramenée de 4 à 3 niveaux le 2026-07-29** (878 `SOURCÉ` · 175 `CALCULÉ` ·
587 `NON CONFIRMÉ`) :

| avant | après | pourquoi |
|---|---|---|
| `MESURÉ` | `SOURCÉ` | « mesuré » laissait croire que NOUS avions mesuré, alors qu'il voulait dire « lu dans une source fiable » — c'est cette confusion qui a produit les 28 fautes critiques |
| `ESTIMÉ` | `CALCULÉ` | c'est notre calcul, il est dit |
| `NON VÉRIFIÉ` + `À PRÉCISER` | `NON CONFIRMÉ` | 565 de leurs 574 emplois étaient **nus** : la nuance « cherché sans trouver » vs « jamais publié » n'était jamais lisible. Quand elle compte, elle est dans la phrase |

Le rendu Tower (`MarkdownContent.tsx`) reconnaît **encore les anciens libellés**, pour qu'un
document non converti ne retombe pas en rose indifférencié.

**Vérification adversariale du 2026-07-29** : 7/7 `PARTIELLEMENT_INEXACT`, 117 corrections dont
28 critiques, presque toutes de la même forme — **un `[MESURÉ]` posé sur un chiffre absent de la
source citée**. Un marqueur sur six reste `[NON VÉRIFIÉ]` : non opposable en externe sans lui.

Voir [[signatera_natera]] (deux chiffres corrigés là), [[competitive_landscape]],
[[veille_concurrentielle_collecteur]], [[tower_survey_coupling]].
