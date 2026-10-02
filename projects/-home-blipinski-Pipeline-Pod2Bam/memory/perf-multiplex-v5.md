---
name: perf-multiplex-v5
description: "Temps d'exécution de référence Pod2Bam multiplex V0.9.6_V5.0.0 (24 flowcells 4-plex, mars 2026) + specs machines"
metadata:
  node_type: memory
  type: project
  originSessionId: c9589956-8780-493a-8c7c-00064e5193a0
  modified: 2026-10-01T13:49:01.951Z
---

# Perf Pod2Bam multiplex V0.9.6_V5.0.0 — référence (calculé 2026-10-01)

**Périmètre** : 24 flowcells distinctes, 4-plex, run complet en une fois (trace initiale `Pod2Bam_trace.txt`, 4 process COMPLETED, 0 cached). Exclus : moche, `_OK`, `rep*`, PBE35455 (5-plex). Batchs FR + WS (10-12 mars 2026) + Colon f181e139/b4caa48f (12 mars). Pipeline `--min_qscore 9`, pré-V0.2.0 (demux --no-trim).

**Sources** : traces NF `RetD/{run}/V0.9.6_V5.0.0/log/Pod2Bam_trace.txt` (submit→complete) + logs globaux `RetD/Pod2Bam_20260310_*.log`, `Pod2Bam_colon_*.log` (PREFETCH Start/Done = download, FINALIZE Upload→Cleanup = upload).

## Moyenne par flowcell (n=24)

| Étape | Moyenne | SD | Min | Max |
|---|---:|---:|---:|---:|
| Download POD5 S3→local | 21 min | 8 | 4 | 35 |
| Basecall (GPU) | 2h06 | 56 min | 23 min | 3h35 |
| Demux+align+sort (CPU) | 1h23 | 38 min | 16 min | 2h47 |
| Nextflow total | 3h29 | 1h32 | 39 min | 6h21 |
| Upload output local→S3 | 2 min | 1 | 0.3 | 4 |
| Total | 3h52 | 1h41 | 43 min | 7h00 |

- **Boris (2026-10-01) : ne plus raisonner en Go** — unité de référence = la flowcell 4-plex (moyenne ci-dessus). Info seulement : POD5 88–807 Go.
- Download ~350 Mo/s, upload ~300 Mo/s ; output ≈ 8% taille POD5.
- ⚠ L'ancienne note "~5.5 min/Go" dans MEMORY.md était fausse.
- Biais : finalize (CPU) chevauche le basecall du run suivant → partie CPU possiblement gonflée.

## Machines (Scaleway, 2 serveurs identiques)
- `GPU-compute-1` (batch FR) et `GPU-compute-2` (batch WS + Colon)
- Instance Scaleway **H100-1-80G** (PAR 2, Block & Scratch, €2.8665/h au 2026-10-01) — confirmé par Boris
- 1× NVIDIA H100 80GB (Dorado `cuda:0` seul, batch size 3520), AMD EPYC 9334 (24 vCPU), 240 GB nominal (236 vus par NF), Ubuntu kernel 6.8
- **Décision Boris (2026-10-01)** : H100-1-80G à €2.8665/h = machine ET prix de référence pour toute estimation temps/coût Pod2Bam (seule option qui reproduit exactement l'environnement initial ; actuellement en rupture de stock PAR 2)
- **Coût de référence : €11.1 / flowcell 4-plex (3h52) = €2.78 / sample** ; ±1 SD ≈ €6.3–€16.0 ; min €2.1, max €20.1
- Image `pod2bam:0.9.6`, Nextflow executor local (cpus=24, memory_max 230 GB)

Lien : [[setup-v6-0-0]] (simplex V6.0.0 a ses propres traces, H100 PCIe).

## Deck CEO (2026-10-01)
- `~/Pipeline/Bam2Beta/docs/Pod2Bam_cout_operationnel.pdf` (10 slides, unitaire uniquement, daté 1er oct. 2026)
- Source : `docs/Pod2Bam_cout_operationnel_src/deck.html` + logos extraits de `2027 Path.pdf`
- Rendu : chrome-headless-shell de `~/.cache/ms-playwright/chromium_headless_shell-1223/` → `--print-to-pdf` (pas d'install)
- Choix Boris : pas de KPI batch, Bam2Beta hors périmètre mais visible en fin de chaîne, coût présenté comme indicatif (stand-by depuis mars 2026)
