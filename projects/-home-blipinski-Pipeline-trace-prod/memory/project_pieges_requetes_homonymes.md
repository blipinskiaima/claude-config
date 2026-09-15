---
name: project-pieges-requetes-homonymes
description: Pièges de requêtage trace-prod — homonymes entre labos, dates de run manquantes, et séparation structurelle sains/tumoraux par run
metadata:
  type: project
---

Rencontrés le 2026-09-15 en constituant une cohorte sains vs tumoraux depuis la base.

**1. Homonymes entre labos — le piège le plus coûteux.** `sample_name` n'est **pas unique** : le même nom existe en CGFL et en HCL, avec des dates, des runs et des mVAF totalement différents.

```
Colon_1   25/03/2025   run 14c189c8   mvaf 28.6   ← CGFL
Colon_1   01/12/2025   run c95dbd44   mvaf  0.0   ← autre labo
```

Vérifié aussi sur `Colon_2`, `Colon_5`, `Colon_30`, `Lung_4`, `Lung_5`. **Toujours filtrer sur `s.labo` ET `s.sample_type`** dans les jointures sur `samples`, y compris — et surtout — dans les requêtes annexes de métadonnées. Le symptôme quand on oublie : un dictionnaire Python construit par `dict[name] = ...` garde silencieusement la **dernière** occurrence, donc les mauvaises dates, sans aucune erreur.

**2. `date_of_run` manquante sur certains échantillons.** Les 4 `Lung_Alc_*` de la sélection n'avaient pas de date en base. Prévoir le cas `NULL` plutôt que de supposer la colonne remplie.

**3. Sains et tumoraux ne partagent JAMAIS un run.** Vérifié sur toute la base : **zéro run** contient les deux groupes. Conséquence méthodologique importante — l'effet batch est structurellement confondu avec le groupe, donc aucun design d'évaluation de biomarqueur ne pourra les séparer proprement sur les données historiques. La seule mitigation est d'étaler sur beaucoup de runs distincts, ou de choisir des tumoraux dans la fenêtre temporelle des sains.

**4. Les sains changent de labo dans le temps.** Les sains CGFL s'arrêtent en **juin 2025** ; tous les sains postérieurs (182 échantillons, jusqu'en juin 2026) sont **HCL**. Une cohorte de sains « récents » sera donc forcément HCL, ce qui introduit un effet labo mesuré à ~1 pt sur les métriques de composition.

**Why** : ces quatre points ont chacun fait dérailler une analyse avant d'être identifiés — les homonymes ont donné un panneau temporel entièrement faux avant correction.

**How to apply** : gabarit de requête cohorte sûr —

```sql
SELECT s.sample_name, m.date_of_run, b.run_id, qm.mvaf_v1, q.reads_primary_mapped
FROM samples s
JOIN qc q             ON q.sample_id = s.id
LEFT JOIN qc_metrics qm  ON qm.sample_id = s.id
LEFT JOIN metadata m     ON m.sample_id = s.id
LEFT JOIN bam_metadata b ON b.sample_id = s.id
WHERE s.labo = 'CGFL' AND s.sample_type = 'liquid' AND s.prod_status = 'OK'
  AND s.sample_name NOT LIKE '%rebasecalled%'
```

Penser aussi à exclure les urines (`%Urine%`) quand on veut du plasma pur — leur biologie de fragmentation est très différente — et à traiter les réplicats techniques (`Breast_18`/`bis`/`ter`/`quater` = un seul patient) comme une seule observation dans les statistiques.

**Accès** : pas de CLI `duckdb` sur le serveur, mais le module python fonctionne. Ouvrir en `read_only=True` sur la base de prod. Un verrou résiduel peut subsister quelques secondes après une requête précédente.
