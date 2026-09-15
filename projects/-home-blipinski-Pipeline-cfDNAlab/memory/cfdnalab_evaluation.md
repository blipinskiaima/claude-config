---
name: cfdnalab-evaluation
description: Verdict par commande après évaluation de cfdnalab sur données AIMA réelles (cohorte 28 échantillons)
metadata: 
  node_type: memory
  type: project
  originSessionId: 5a11d752-d0d0-4ab8-bb8f-f2373e6b1257
  modified: 2026-09-15T15:50:20.119Z
---

Évaluation menée le 2026-09-15 sur données de production CGFL/HCL. **Conclusion générale : cfdnalab est bien construit et rapide (~45 s/échantillon), mais sur les données AIMA aucune de ses commandes ne bat ce qui existe déjà dans Bam2Beta.**

**Verdict par commande de feature**

| Commande | Verdict |
|---|---|
| `fcoverage` | Reproduit la CNV existante. Validation croisée réussie (depth 0,501 vs 0,53 en base ; couverture 37,1 % vs 37,42 %). À 10 kb, les « événements focaux » détectés sont des artefacts de mappabilité : **27/27 négatifs, 0 positif**, et 56 % présents aussi chez un sain. Le gain théorique de 2,2× en sensibilité CNV n'est jamais atteint car le bruit dominant à 10 kb est systématique, donc ne s'atténue pas en √n |
| `ends` | Seule famille de features absente de Bam2Beta. Signal réel (AUC 0,993 après normalisation par labo) mais **bruit de réplicat 2,24 pt ≈ signal 2,69 pt**. Reste corrélé au biais GC résiduel (r = +0,52, n=15) malgré `--gc-file` |
| `midpoints` | Architecture nucléosomale parfaite (NDR au TSS, pics +1/+2/+3, périodicité mesurée **172 bp**). Mais **76 % de l'écart sain/tumoral est un artefact de longueur de fragment** : en restreignant à 160-180 bp, l'écart passe de 10,0 à 2,4 pt |
| `lengths` | **Meilleur rapport signal/bruit de toutes les métriques testées : 4,0** (contre 1,2 pour les end-motifs). AUC 0,917 sans aucune normalisation. Mais duplique exactement le module FRAG existant |

**Pattern récurrent — à retenir avant de s'enthousiasmer sur un résultat de cet outil** : trois fois de suite, un signal net s'est effondré une fois le contrôle approprié appliqué (blacklist pour fcoverage, réplicats techniques pour ends, stratification par longueur pour midpoints).

**Commandes jamais lancées** : `ref-kmers`, `coverage-weights`, `fragment-count-weights`, `bam-to-frag`, `frag-to-bam`.

**`bam-to-bam` — testé, sans intérêt pour la mVAF.** En mode défaut il ne filtre que **0,36 %** des reads primaires au-delà du nettoyage secondary/supplementary que modkit fait déjà. Les poids GC écrits en tags AUX (`GC`, `cw`, `nw`) sont **ignorés par modkit**. Seul apport résiduel : le tag `fl` donne une longueur de fragment en span aligné, qui trancherait l'ambiguïté avec le `length(seq)` moins softclips de FRAG. Les tags MM/ML de méthylation **survivent** au passage (vérifié).

**Why** : Boris voulait savoir ce que cfdnalab pouvait apporter à Bam2Beta. Réponse mesurée plutôt que supposée.

**How to apply** : ne pas relancer une évaluation de `fcoverage`/`ends`/`midpoints` sans un plan de contrôle explicite du confondant attendu. Si une piste cfdnalab est rouverte, commencer par `lengths` fenêtré (`--by-size`, profils DELFI) — c'est le seul angle non exploré sur la métrique au meilleur rapport signal/bruit. Voir [[cfdnalab-install]] pour l'installation et le gotcha `--reads-are-fragments`.

**Obstacle structurel qui limitera toute évaluation future de biomarqueur chez AIMA** : sains et tumoraux ne partagent **jamais** un run de séquençage (vérifié sur toute la base trace-prod). L'effet batch est donc confondu avec le groupe par construction. Mesuré : effet labo CGFL/HCL de 1,14 pt sur les end-motifs, et +2,07 pt en sens inverse sur la fraction de fragments courts — donc c'est une propriété du prélèvement/séquençage, pas d'une métrique particulière.

**Environnement de travail** : `/scratch/boris/cfDNAlab/` — scripts d'analyse (`plot_*.py`, `run_cohort*.sh`), 2bit GRCh38 no_alt fabriqué localement, blacklist ENCODE, table de référence GC. Réutilisables tels quels.
