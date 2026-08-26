# Context — short-read — 2026-08-26T16:41+00:00

**Branche** : main
**Dernier commit** : 6fe8706 — add mVAF v1.4/v1.5 protocol for short-read (rastair per-read → bootstrap)
**Status** : clean (seul `dl.sh` untracked, préexistant, non lié)

## Où j'en suis
Production des **mVAF v1.4 et v1.5** sur les pipelines short-read, qui n'avaient que la v1.
Le protocole est **écrit, validé et versionné** dans [mvaf14_short_read/](mvaf14_short_read/),
mais le **pilote ne couvre que 2 samples sur 1 des 3 couloirs** (NF_Watchmaker_Methylseq,
variante Standard). Périmètre validé avec Boris : BP_5base + BP_Watchmaker + NF_Methylseq,
soit ~104 runs. NF_Watchmaker_Aima mis de côté. Objectif final : fusionner les résultats
dans l'onglet `Short read` de la gsheet Trace PROD — **rien n'y a encore été écrit**, et
Boris exige de regarder et sauvegarder l'existant avant toute écriture.

## Ce qui marche / ce qui foire
- ✓ **Voie trouvée** : `rastair per-read` (v0.8.2) rend le read-level directement depuis le
  BAM. Ni tags MM/ML, ni modkit, ni réalignement. `bootstrap_model_v1()` tourne inchangé.
- ✓ **Gate validé** : ré-agréger notre `extract_full` redonne le `rastair_call` d'origine —
  couverture 97,4 %, `n_meth` 98,2 %, corrélation β **+0,997**. C'est lui qui a fait échouer
  mes 3 premières versions du repliage.
- ✓ **Pilote cohérent** : Colon_3 v1 18,03 → v1.4 **42,81** (ratio 2,37 ; médiane ONT 2,26
  sur 1 509 samples trace-prod). Healthy_634 v1 0,00 → v1.4 **0,01** (négatifs ONT : 0,00).
  Bootstrap stable, sd 0,62 sur 200 tirages.
- ✓ `rastair per-read` **tourne sur les 3 types de BAM**, y compris 5base.
- ✗ **Le gate n'existe que contre un `rastair_call`.** Il bloque BP_5base et BP_Watchmaker,
  dont la v1 vient du `CX_report` DRAGEN. C'est la seule pièce de code manquante.
- ✗ **5base non tranché** : rastair est un outil TAPS, la chimie 5-base ne l'est pas. Corrélé
  à DRAGEN une seule fois (r = +0,97, 1 sample, chr1:1-1,4 Mb, BAM tronqué). Alternative si
  ça ne passe pas : parser le tag `XM:Z` du BAM DRAGEN (présent sur 89,5 % des reads utiles).
- ✗ **`TRIM=0`** décidé pour les couloirs DRAGEN mais jamais exécuté.
- ✗ **BQ30/BQ40 irréproductibles** : `per-read` n'a pas `--min-baseq`. Les 9 variantes
  methylseq tombent à 3 (Standard, QC20, QC30).
- ✗ `add_mmml_taps.py` (section IGV) est **perdu** — jamais commité, `/scratch/short-read/`
  nettoyé. Signalé dans CLAUDE.md et dans la mémoire.

## Prochaine étape
Écrire la **version `CX_report` de `04_gate.py`** : elle ferme deux questions d'un coup —
elle débloque les 2 couloirs DRAGEN et elle valide `rastair per-read` sur le 5base.
Puis lancer BP_Watchmaker avec `TRIM=0` sur 2 samples pilotes avant de passer aux ~104 runs.

Données de travail (23 Go de BAM et de per-read) : `/scratch/boris/short_read_mvaf14/`.
