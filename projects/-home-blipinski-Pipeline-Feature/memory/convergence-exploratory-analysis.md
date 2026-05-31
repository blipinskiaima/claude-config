---
name: convergence-exploratory-analysis
description: "exploratory-analysis-CGFL-HCL (branche main, 17 scripts) recoupe la mission de Feature/ sur le score combiné et la fragmentomique"
metadata: 
  node_type: memory
  type: project
  originSessionId: c2f7cad8-b1a9-4dd5-93ee-f14009c1102c
---

`~/Pipeline/exploratory-analysis-CGFL-HCL` branche `main` = 17 scripts numérotés (état 28/05/2026, origin/main). Ce n'est pas un pipeline linéaire : un socle `01` (produit `rds/all_res_v5_{all,cgfl,hcl}.rds` depuis **GSheet** via `raima::compile_vaf_data()`, PAS DuckDB) + familles d'analyses qui se branchent. Pivots de dépendance : `01→rds`, `09→combined_score_xgboost_5fold.csv` (lu par 10/15), `14→fragment_length_histograms_75_500_5bp.csv` (lu par 16/17).

Familles : A=éval mVAF base (02-07), B=score combiné XGBoost (08-10,15), C=cliniques ciblées (11-13), D=fragmentomique avancée (14,16,17).

**Deux ponts directs avec Feature/ :**
1. **Score combiné (08-10,15)** : `09_sensitivity_specificity_combined_vs_mvaf.R` fait un XGBoost binaire CV 5-fold OOF sur 4 features `mvaf+frag_mode1+frag_mode2+ichorcna`, labels healthy=0/muté-ou-actif-sans-mut=1, suspects scorés par inférence — **exactement la mission de Feature/ mais en R/GSheet** vs Python/DuckDB. Risque de divergence de résultats entre les deux sources de données.
2. **FragDirection (14,16,17)** : feature de delta directionnel du profil de longueur de fragments, construite depuis les BAM. Recoupe les features `short_read` du pool Feature/ (cf. [[livrables-actuels]]).

**Why:** éviter de réinventer/diverger ; clarifier qui porte le score combiné. **How to apply:** quand on touche au combiné ou à la fragmentomique dans Feature/, comparer d'abord avec `09` et `17` d'exploratory-analysis (s'aligner sur leur logique ou justifier l'écart). Le protocole d'éval socle de Feature/ vient de 01-07 (cf. [[trace-prod-schema]] pour la source DuckDB côté Feature).
