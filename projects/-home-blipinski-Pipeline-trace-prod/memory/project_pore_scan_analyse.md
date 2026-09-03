---
name: project-pore-scan-analyse
description: "Analyse des pore scans MinKNOW (146 runs, /scratch/boris/pore-scan/) — le 'pores available' se lit dans les LOGS du rapport HTML, pas dans un champ. La réserve de pores (totaux) prédit la longévité du run, les pores disponibles non. Aucune différence CGFL/HCL. Reconstituable depuis les tags ch/mx du BAM quand le rapport manque."
metadata: 
  node_type: memory
  type: project
  originSessionId: 70b8e736-da80-4f70-928e-6bae789746ce
  modified: 2026-09-03T12:43:29.841Z
---

# Analyse des pore scans MinKNOW (septembre 2026)

Analyse **ad-hoc, hors repo** : scripts et données dans `/scratch/boris/pore-scan/`
(+ `/scratch/boris/plateforme-seqtime/` pour le run plateforme). Rien n'est versionné,
conformément à [[feedback_scratch_workspace]].

## Où se trouve l'information (le point à retenir)

Le nombre de pores **n'est pas un champ** du rapport HTML : il est dans les **messages de
log** MinKNOW embarqués dans le JSON de la page.

```
"Pore scan for flow cell PBK18624 has found a total of 7681 pores.
 2593 pores available for immediate sequencing"
```

- **total** = pores détectés sur les 4 mux de chaque channel
- **disponibles** = celui retenu par channel, donc plafonné par les ~2675 channels

⚠ J'avais d'abord conclu que l'information était absente, en cherchant les noms de champs de
la plateforme (`single_pore`, `mux_scan_results`, présents eux dans le `report_*.json` de
MinKNOW 6.x). **Boris a insisté, il avait raison.** Chercher dans les logs avant de conclure
à une absence.

Un run porte **46 scans** (un toutes les 1,5 h) → courbe complète d'usure de la flow cell.
Le champ `"pores_remaining"` du HTML ne donne que l'état de fin.

## Corpus

**146 runs** = 92 CGFL + 54 HCL, soit **la moitié** des 291 runs en base (185 CGFL, 106 HCL) —
les autres n'ont pas de rapport conservé. Rapports CGFL sur `s3://aima-pod-data/data/CGFL/liquid/{run}/`
(95, profil scw) ; HCL déjà en local dans `~/Pipeline/trace-prod/rapport/` (55, dont `flag.html`
qui n'est pas un rapport). `pore_scan_initial.tsv` : 146 lignes × 11 colonnes.

## Résultats

**Aucune différence entre labos**, sur aucune métrique : pores disponibles (médianes 2704 vs
2663, Mann-Whitney p=0,12), pores totaux (7521 vs 7379, p=0,43), ratio dispo/total (35,9 % vs
36,3 %, p=0,64). Configuration identique sur les 146 runs : `FLO-PRO114M` + `SQK-NBD114-96`,
72 h de limite, pore scan à 1,5 h, reserved pores On.

**La bonne métrique de qualité est le TOTAL, pas le disponible.** Corrélation pores totaux ↔
demi-vie du run : **r = +0,44** (t=5,5, n=131). Le disponible ne prédit presque rien car il est
plafonné par les channels — d'où l'illusion que toutes les flow cells se valent.

| pores totaux au départ | demi-vie médiane |
|---|---|
| < 6500 | 25 h |
| 6500-7500 | 32 h |
| 7500-8500 | 33 h |
| > 8500 | 41 h |

Mécanique : MinKNOW n'utilise qu'un pore par channel et bascule sur un autre mux quand il meurt.
**Les pores totaux sont le stock de remplaçants.**

**Deux profils de run raté** (24/146, 16 %), répartis de façon asymétrique :
- **Profil 1** — flow cell pauvre à la réception (pic < 1500) : **9 runs, dont 8 HCL**
- **Profil 2** — départ normal mais demi-vie < 20 h : **15 runs, dont 13 CGFL** (14 % des runs
  CGFL contre 4 % des HCL)

C'est le **seul écart net entre labos** de toute l'analyse.

**Cause du profil 2 : non élucidée.** Écarté par les données : paramètres de run (aucun ne
discrimine), messages de log (aucun surreprésenté), réutilisation de flow cell (146 IDs
distincts, aucun doublon, aucun log de `wash`), distribution unimodale des pores totaux (pas de
2ᵉ population). Le préfixe d'ID (`PBA`→`PAY`→`PBE`→`PBI`→`PBK`→`PBM`) explique 10 % de la
variance mais est **totalement confondu avec la date** — la réserve passe de 5200 à 8200 pores
en 18 mois, ce qui ressemble à des générations successives de consommables.

Piste ouverte : **3 runs CGFL du 27/03/2026** (`PBK07581`, `PBK03918`, `PBK04038`, lancés à
09:25-09:46) partent sains (2700-2750 pores, 7800-8400 totaux) et meurent tous en 8-11 h.
Cause commune probable côté librairie ou lot de réactifs.

## Cinétique de séquençage

**Jamais de plateau** : décroissance continue dès h+2, qui suit exactement la courbe des pores.
Sur 4 runs (HCL `PBK18624`, CGFL `PBE96775` et `PBM55710`, plateforme `PBG32970`), **92 à 100 %
des reads sont acquis à h+48**. Le prolongement au-delà ne rapporte que 0,2 à 8 %.

## Reconstituer les pores sans rapport MinKNOW

Les tags **`ch:i` (channel) et `mx:i` (mux)** du BAM permettent de compter les couples distincts
= pores ayant produit. **Validé contre la référence** sur le run `test_002` de la plateforme
(seul à avoir `report_*.json` + BAM) : 334 mesurés à 30 min contre **344** au mux scan officiel,
soit −2,9 %.

⚠ Ce n'est **pas la même grandeur** que le « pores available » : on mesure les pores *actifs*
(ayant produit dans la fenêtre), pas les pores *disponibles* testés activement. Borne inférieure,
comparable en tendance mais pas en valeur absolue — normaliser en % avant toute comparaison.

## Gotchas

- ⚠ **Compter les barcodes ayant des reads ≠ compter les samples.** Le démultiplexage assigne
  1 à 205 reads à des barcodes non utilisés, contre des millions pour un vrai sample. Mon
  premier comptage donnait une médiane de **95 samples** au lieu de **4**. Seuil retenu :
  **0,1 % des reads du run** (~1000× au-dessus du bruit). Conséquence : la question
  simplex/multiplex est **intestable** ici — 133 des 146 runs chargent exactement 4 samples.
- ⚠ **Une « chute brutale » en fin de vie est du bruit.** Ma détection (perte > 40 % entre deux
  scans, garde `> 200 pores`) a classé `PBK07581` comme chute tardive à h+52 : il ne restait que
  203 pores sur 2754, et il perdait en réalité 12-21 % à *chaque* scan depuis h+0. Filtrer sur
  un seuil relatif au pic, pas absolu.
- ⚠ **`nb samples` du pore scan rate les samples faibles** : `Healthy_826` (0,08 % du run) passe
  sous le seuil de 0,1 % → son run est compté à 3 samples au lieu de 4.
- ⚠ Le type de flow cell **n'est ni dans le BAM ni en base** — uniquement dans le rapport. Le
  `@RG DS` ne porte que `runid`, `basecall_model`, `modbase_models`. Impossible d'étendre
  l'analyse aux 145 runs sans rapport.
- ⚠ `flow_cell_life_condition` vaut `false` sur les 146 : **aucun historique du consommable**
  n'est tracé (pas de compteur d'utilisations, pas de date de mise en service). L'hypothèse
  « flow cell lavée puis réutilisée » n'est donc ni vérifiable ni réfutable depuis ces fichiers.

Voir aussi [[project-schema-v30-v31-sequencing-time]] (la durée de run vient du même besoin),
[[project_frag_softclip_trim]] (cohorte Lung_Alc / AlCapone).
