---
name: qc-filtre-80-1kb
description: "QC apres filtre fragmentomique 80 < L < 1 kb sur le BAM merged (1378 liquides, 2026-09-10/11) — methode une passe streaming, conventions validees bit a bit sur Lung_9, resultats de cohorte et bascules de statut QC"
metadata:
  node_type: memory
  type: project
---

# QC post-filtre 80 pb - 1 kb (2026-09-11)

Etude R&D : que deviennent depth, coverage, nb de lignes et nb de molecules si on ne garde que
les reads de longueur **strictement** entre 80 et 1000 pb ? **Le filtre n existe pas dans le
pipeline**, il a ete pose pour l occasion. 1378 liquides (865 CGFL + 513 HCL), 20,96 To relus.
Colonnes en base : voir `project_schema_v35_qc_80_1000` cote trace-prod.

## Ce que l existant ne permettait PAS (la question de depart)

`Fragmentomics/filtered_softclipped/{ID}.read_lengths.csv` porte toutes les longueurs read par
read, mais **une seule colonne** : aucune position -> ni depth ni coverage. Et il est produit en
`-F 3840 -L chr1_22`, donc **sans la strate A** (non alignees), qui compte dans A+D. mosdepth et
cramino agregent : on ne peut pas retrancher a posteriori les reads hors bornes.
-> relecture complete des BAM obligatoire, mais **une seule passe suffit pour les 4 metriques**.

⚠ La borne haute seule etait deja publiee : `QC/Samtools/{ID}.n50_ratio.tsv` colonne
`n_reads_filtered` = reads L <= 1000 ([frag.nf:86]). Il ne manquait que la borne basse.

## Methode — `/scratch/boris/qc_stat/` (metrics.awk + run.sh)

```
aws s3 cp BAM - | samtools view -@1 -h - | mawk -v MIN=80 -v MAX=1000 -f metrics.awk
   molecules A+D   flag & 0x900 == 0                     (convention cramino num_reads)
   depth/coverage  flag & 1796  == 0                     (convention mosdepth -F 1796)
   bases           CIGAR M/=/X SEULS                     (mosdepth n inclut PAS les deletions)
   coverage        union des intervalles en streaming    (BAM trie -> memoire constante)
```

Streaming pur, **zero ecriture disque**, idempotent (1 fichier resultat par sample, skip si present).
Le **nb de lignes** (A+B+C+D) n est pas sorti par l awk mais se derive : `reads_total - skipped`,
`skipped` etant compte avant tout test de flag. Verifie sur Lung_9.

### Validation bit a bit (Lung_9 HCL, sans filtre vs valeurs publiees)

| metrique | awk | pipeline | ecart |
|---|---|---|---|
| molecules A+D | 37 692 469 | cramino `num_reads` | **0** |
| bases | 6 995 591 241 | mosdepth | **0** |
| depth | 2.2568 -> 2.26 | 2.26 | **0** |
| coverage | 0.8295 -> 83 % | 83 % | conforme |

- ⚠ Sommer `M/D/N/=/X` donne **+0,58 %** : mosdepth ne compte pas les deletions. `M/=/X` seuls.
- ⚠ Denominateur = **3 099 721 093**, pas la somme des LN du header (3 099 922 541) : mosdepth
  ecarte `chrEBV` + `chrUn_KI270396v1` + `chrUn_KI270752v1` (tous a 0 read). Ecart 0,0065 %.
  **Le header est identique sur 1378/1378** -> la constante est legitime.
- En filter expression samtools, la longueur fragmentomique s ecrit **`qlen - sclen`** (`qlen`
  inclut les softclips). Non utilise ici, mais exact.

### Performance — 3 idees fausses, mesurees

- **Telecharger le BAM d abord est PLUS LENT** : `cp` multipart = 151 Mo/s contre 41 en streaming,
  mais le calcul local (395 s) ne gagne que 24 s sur le streaming (419 s) -> total 509 s vs 419 s.
- **mawk ne gagne que 16 %** sur gawk (339 s contre 395), valeurs identiques. Pas de `and()` en
  mawk (tests de bits en arithmetique) et **`%.0f` obligatoire**, `%d` deborde a 2^31.
- **`samtools coverage` n est pas la solution** : 234 s pour depth+coverage, mais il faut une 2e
  passe pour les molecules -> ~400 s, plus lent que l awk qui fait tout d un coup.
- ⚠⚠ **16 flux paralleles = optimum, 32 s effondre** : les 32 `aws s3 cp` remplissent leurs
  tampons d un coup (pic reseau 1137 Mo/s, **96 Go de RAM, 2 Go libres**), puis le debit tombe a
  **61 Mo/s**. A 16 : ~400 Mo/s stables, 0 KO sur 1378. Ne pas reinstruire.
- Duree reelle : 1378 samples / 20,96 To en **~15 h** a 16 flux, machine partagee avec les runs
  de dilution de Boris.

## Resultats de cohorte

| metrique | avant | apres | conserve (med) | n |
|---|---|---|---|---|
| Nb de lignes | 41 897 912 | 38 011 096 | **92,7 %** | 1356 |
| Nb de molecules A+D | 34 895 625 | 32 428 307 | **92,6 %** | 1356 |
| Depth | 1,96x | 1,88x | **96,8 %** | 1376 |
| Coverage | 79,00 % | 77,84 % | **99,0 %** | 1373 |

(les 22 `Twist_*` n ont **aucun `reads_primary` en base** -> exclus des 2 comptages ; notre calcul
leur en donne un)

**Le filtre coupe du court, pas du long** : les reads ecartes font **78,5 pb** de moyenne contre
177,2 pb pour les conserves (median sur 1211 samples). D ou l ordre des impacts : comptages
-7,4 % > depth -3,2 % > coverage -0,96 %. Un comptage traite chaque read a egalite, la profondeur
ne perd que la masse, et la couverture presque rien (a 1,9x, une base perdue est souvent couverte
par un autre read).

### La traine du depth = detecteur d ADN long

| depth conserve | n | masse > 1 kb (med) |
|---|---:|---:|
| < 50 % | 21 | **57,3 %** |
| 50-80 % | 44 | 28,7 % |
| 80-95 % | 273 | 5,7 % |
| >= 95 % | 1005 | **1,9 %** |

Facteur 30, strictement monotone. Cas extreme `TNE_2` : 0,66x -> 0,13x, et c est l echantillon a
81 % de masse > 1 kb ([[n50-ratio-qc]]). **Le filtre est incidemment un revelateur de gDNA.**

### Bascules de statut QC ([[qc-status-exis-themelio]])

| bascule | Exis | Themelio | cause |
|---|---:|---:|---|
| SUCCESS -> WARNING | 36 | 36 | molecules sous **20 M** |
| WARNING -> FAILED | 14 | 10 | molecules sous **5 M** |
| amelioration | 0 | 0 | |

**Seul le comptage de molecules fait basculer** — jamais la profondeur ni le coverage (les 3
samples dont le depth passe sous 0,25x etaient deja FAILED sur les molecules). Arbre reconstruit
en SQL : **99,6 % d accord** (1361/1366) avec `exis_qc_status` en base, donc chiffres fiables.

⚠ **Themelio bascule MOINS qu Exis** (46 vs 50) parce qu il est plus severe en amont : les 4
urines d ecart (`Bladder_Urine_02_016/_134/_138/_170`, amplitude 8,6 a 34,9) sont deja FAILED chez
lui avant tout filtre (amplitude < 80 = FAILED chez Themelio, WARNING chez Exis). Le produit le
plus severe est celui que le filtre deplace le moins.

## Finding de bord — `qc_metrics.coverage_percent` n a qu 1 point de precision

**Entier rond sur 1378/1378.** Il est lu dans la `global.dist` de mosdepth, qui ne publie que
2 decimales de **proportion** (0.83 -> 83 %), alors que la colonne est typee `DECIMAL(5,2)`.
Tout seuil bati dessus herite de cette granularite. C est ce qui explique les 143 samples ou
`coverage_80_1000 > coverage_percent` : ecart max **0,49 pt**, soit sous la demi-granularite.

## Restitution

Google Doc QC, onglet **`Deep Dive > Filtre read entre 80 et 1000Kb`** (`t.vhotayve8x7`, le titre
dit 1000Kb mais la borne est 1 kb). 6 parties imposees par Boris. Insertion par append pur dans un
onglet vide, `tabId` dans chaque requete ([[gdoc-qc-ratio-n50]]). Boris a condense la partie 1
apres coup ([[feedback_doc_concision]] : il coupe, il ne fait pas re-expliquer).

Voir [[read-counting-cascade]] (strates A/B/C/D), [[softclip-fragmentomics-length]] (la convention
de longueur), et cote trace-prod `project_schema_v35_qc_80_1000`.
