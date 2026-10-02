# Methylseq — mémoire projet

- [Version du pipeline nf-core](version-pipeline-nf-core.md) — clone v4.2.0, dépôt aligné sur master le 18/09/2026, sauvegarde sous tag `v4.2.0-aima` ; les 3 écarts AIMA à préserver.
- [Run 5base Healthy_767](run-5base-healthy767.md) — methylseq --taps valide sur 5base (C 20,6 %, 98 % mappés) ; nOT/nOB mesurés ≠ Watchmaker, à relire par sample.
- [Export QC methylseq](qc-export-methylseq.md) — methylseq_qc.py → gsheet ; Nb reads vs Nb molécules (paires, ÷2) validés ; depth mosdepth ≠ DRAGEN.
- [Token Seqera exposé](secret-token-tower-expose.md) — accessToken en clair et commité dans nextflow.config : révoquer avant tout le reste.
