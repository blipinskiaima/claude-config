---
name: length-distribution-figure
description: "Process Length_Distribution_Plot (frag.nf) — PNG de distribution de longueur du sample vs 3 references embarquees, seuil 1 kb ; pondere par la MASSE d'ADN"
metadata: 
  node_type: memory
  type: project
  originSessionId: ddfe1da5-81f0-495e-90f2-6e719f7dc108
  modified: 2026-08-12T12:27:49.687Z
---

# Figure de distribution de longueur des reads (2026-08-12, `e8eac18`)

Process `Length_Distribution_Plot` dans [workflow/frag.nf], appele dans `workflow Frag` juste
apres `Extract_read` dont il consomme le meme channel (`csv_file`). Produit
`Fragmentomics/filtered_softclipped/{ID}.length_distribution.png` : 4 courbes (sample courant +
3 references embarquees), ligne verticale de seuil a 1000 pb, legende en 2 categories REF/SAMPLE.

## Le point cle : masse d'ADN, pas nombre de reads

L'ordonnee est la **part de la masse d'ADN** par tranche de longueur. C'est la meme ponderation
que le `n50_ratio.tsv` deja produit par `Extract_read` — la figure en est le pendant visuel.

**La mediane est aveugle au defaut qu'on cherche.** Sur les 8 plasmas contamines identifies,
`median_length` vaut 163-176 pb (strictement normal) pendant que le `n50` monte a 1 608 et
3 647 pb. La mediane compte les fragments un par un et les longs sont peu nombreux ; le N50
pondere par la masse et les voit immediatement. Voir [[n50-ratio-qc]] et
[[qc-palier1-candidats-ecartes]].

## Les 3 references

`bin/length_distribution/reference_distributions.tsv` — 106 lignes, 4,3 Ko, colonnes
`sample / label / length_bp / pct_mass`. **Calculees avec la methode exacte d'`Extract_read`**
(`-F 3840` + BED `hg38_chr1_22.bed` + soft clips retires du CIGAR), pas avec une methode maison.

| sample | label | masse > 1 kb |
|---|---|---:|
| `Breast_28` | Plasma normal | 0,31 % |
| `Bladder_Urine_02_041` | Urine | 23,08 % |
| `Breast_6` | Contamination gDNA | 57,26 % |

⚠ **Seul `Bladder_Urine_02_041` est encore relancable** : les BAM horaires de `Breast_28` et
`Breast_6` ont ete supprimes de `data/` (campagne de nettoyage), il ne reste que les
`*_list.txt` / `*_header.txt`.

## Implementation

- **Aucun nouveau conteneur** : ggplot2 3.5.2 + scales 1.4.0 sont deja dans `bam2beta:latest`,
  container par defaut du process (verifie par `docker run`, pas suppose).
- **Binning en awk, en streaming** : 12 bins/decade, 3,8 s pour les 9,2 M de lignes de
  `read_lengths.csv`, sans montee en memoire. R ne recoit que ~45 bins.
- **Patron `${projectDir}`** pour le script R et le TSV de references — aucun channel, donc
  aucun risque du gotcha `Channel.fromPath` = queue a 1 item.

## Validations

- **Croisee, forte** : sur `Bladder_Urine_02_041`, le `pct_mass_removed` calcule par le run
  (23,08 %) est identique a la masse > 1 kb de la reference embarquee — par deux chemins
  independants (BAM re-merge depuis 144 BAM horaires vs BAM `RetD`). Valide du meme coup la
  reference, le determinisme du merge et le binning.
- Execute sur 3 samples reels : `Healthy_826`, `Lung_9`, `Bladder_Urine_02_041`.
- `check-conformity` vs QUALIF V2.2.0 : **41/41**, aucune regression.

## Gotchas

- **`cramino mean_length` n'est pas fiable en presence de chimeres** : il annonce 167 pb sur
  `Lung_Alc_79_prog` alors que 54 % de ses reads font 583 pb. Le seuil doit s'appuyer sur le
  **n50**, pas sur `mean_length`.
- **`nextflow lint` (25.10) sort 9 erreurs sur `frag.nf`** — mais le fichier en avait deja 6
  avant, soit 3 par process, toutes dues a la syntaxe `process Name() {` avec parentheses vides.
  Rejetee par le linter, acceptee par le runtime. Preexistant, pas une regression.
- **Le seuil doit etre specifique a la matrice** : plasma p95 = 212 pb, urine mediane = 247 pb —
  les distributions ne se recouvrent pas. Un seuil unique declarerait anormale la moitie des
  urines normales.
