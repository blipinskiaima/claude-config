---
name: Bash inline dans process Nextflow
description: Boris préfère commandes bash directement dans script:"""""" des process plutôt que scripts dans bin/Module/
type: feedback
originSessionId: 613eeff2-6b1f-420e-aaf2-3c2272f88dd3
---
Pour les nouveaux modules Nextflow dans Bam2Beta, **toutes les commandes bash doivent être écrites directement dans le bloc `script: """ ... """`** du process, pas dans des scripts bash externes dans `bin/Module/`.

**Why:** Boris a explicitement corrigé ce point lors de l'implémentation Sniffles2/Severus/Decoil (2026-04-28). Le plan initial proposait `bin/Sniffles2/run_sniffles2.sh` etc. à l'image d'`ichorCNA.nf` qui appelle `bin/ichorCNA/run_readCounter.sh`. Boris a préféré le pattern de `frag.nf` où les commandes (samtools, awk, etc.) sont inline. Raison : tout exécutable dans le `.nf`, plus facile à lire d'un coup, pas besoin de naviguer entre fichiers, et un seul endroit pour modifier la logique.

**How to apply:**
- Pour TOUT nouveau process Nextflow dans ce projet : commandes bash inline dans `script: """ """`
- Inclure le logging Bash inline aussi (`LOG=...; echo ... > $LOG; cmd 2>&1 | tee -a $LOG`)
- Référence Rscript externe encore acceptable (cf. `Rscript "${projectDir}/bin/fragmentomics_score.R"` dans frag.nf) — mais pas de bash externe
- Les scripts existants dans `bin/ichorCNA/` ne sont PAS à migrer rétroactivement (legacy OK)
- Pattern source à imiter : `workflow/frag.nf` (pas `workflow/ichorCNA.nf`)
