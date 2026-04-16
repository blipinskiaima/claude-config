---
name: veille
description: Analyser les derniers rapports de veille scientifique PubMed. Lit les rapports generés par le cron, resume les publications pertinentes pour AIMA, et priorise par impact. Use when the user says "veille", "publications", "quoi de neuf", "new papers", or wants a scientific literature update.
argument-hint: "[--days N] [--query nom_requete]"
allowed-tools: Read, Glob, Bash(python3*), Bash(cd*), Bash(ls*), Bash(cat*), WebFetch
---

# Veille Scientifique — Analyse Claude

Lis et analyse les rapports de veille PubMed generes automatiquement par le cron.

## Workflow

1. **Lire les derniers rapports** :
   ```bash
   ls -lt ~/Pipeline/Aima-Survey/reports/ | head -5
   ```
   Lis le rapport le plus recent (ou celui des N derniers jours si --days specifie).

2. **Analyser chaque publication** :
   Pour chaque publication trouvee, evalue :
   - **Pertinence AIMA** (haute/moyenne/basse) : impact direct sur le pipeline ctDNA, batch effect, scoring, ou outils
   - **Action suggeree** : a lire, a tester, a integrer, informatif seulement
   - **Lien avec les projets** : quel projet Pipeline est concerne (Bam2Beta, IA-for-IA, exploratory-analysis, etc.)

3. **Resume structure** en francais :
   ```
   ## Veille du {date}

   ### Publications haute pertinence
   - {titre} — {pourquoi c'est pertinent pour AIMA} — Action: {action}

   ### Publications moyenne pertinence
   - ...

   ### Rien de nouveau sur
   - {requetes sans resultats}
   ```

4. **Si aucun rapport recent** : lancer manuellement la veille
   ```bash
   cd ~/Pipeline/Aima-Survey && python3 veille.py --days 7 --report
   ```

## Options

- `--days N` : analyser les rapports des N derniers jours (defaut: 7)
- `--query nom` : filtrer sur une requete specifique (ex: ctDNA_methylation_ONT)

## Contexte scientifique AIMA

Pour evaluer la pertinence, garder en tete :
- Pipeline : POD5 → Pod2Bam → BAM → Bam2Beta → bedMethyl → raima → trace-prod
- Probleme principal : batch effect CGFL vs HCL, sensibilite basse VAF
- Modele : combined_binom nometh, 97.4% sens VAF>5%, 53.8% VAF 0-5%
- Technologies : Oxford Nanopore basse couverture, TAPS+ Illumina, Dorado basecalling
- Outils : modkit, samtools, raima (R), ichorCNA, DuckDB
