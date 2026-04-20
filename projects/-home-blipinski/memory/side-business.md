---
name: Side business Boris
description: Projet de side business bioinformatique complémentaire à l'activité AIMA — 4 pistes identifiées, périmètre en 7 dimensions, cadrage juridique, plan d'action step-by-step
type: project
originSessionId: 025f674b-99c5-4993-ae7e-6dbe89b8f3b2
---
# Side business Boris — Services bioinfo non-cliniques

## Objectif

Créer un complément de revenu rentable (500 € à 3 000 € nets/mois) valorisant l'expertise bioinformatique, compatible avec le CDI AIMA en cours (signé 25/08/2025), sans conflit juridique ni risque d'épuisement.

## Vision en 1 phrase — à finaliser

**Version Boris (en arbitrage)** :
> Services, conseil, développement, et formation et des produits et analyses pour la bioinformatique, à destination de laboratoires académiques et de PME biotech hors oncologie et hors diagnostic médical, en dehors de mes heures de travail AIMA.

**Version affinée proposée (pas encore validée)** :
> Services, conseil, développement, formation, produits logiciels et analyses en bioinformatique — incluant Nextflow, Python, R, Docker et outils open source — à destination de laboratoires académiques et de PME biotech, à usage de recherche fondamentale et appliquée, hors oncologie, hors diagnostic médical, et hors contexte clinique, en dehors de mes heures de travail AIMA.

Différences : +"produits logiciels" (précision), +ancre technique explicite (Nextflow, Python, R, Docker), +"hors contexte clinique" (sécurité juridique renforcée par rapport au simple "hors diagnostic médical").

## Contraintes contractuelles AIMA à respecter

- **Art. 10 — Exclusivité** : toute activité parallèle nécessite accord écrit préalable de l'employeur. Lettre formelle à envoyer à Michael (CTO) **avant tout démarrage commercial**.
- **Art. 11 — Confidentialité 5 ans** : interdiction de publier retex AIMA, code source, métadonnées internes, identifiants samples, procédures QC. Marketing public en contenus anonymisés ou génériques uniquement.
- **Art. 12 — PI** : cession automatique à AIMA de tout ce qui relève des "fonctions". Le side business doit être strictement hors périmètre fonctionnel AIMA.
- **Art. 13 — Non-concurrence post-contrat** : 12 mois, France entière, activités similaires/concurrentes (interprétation stricte : diagnostic cancer méthylation / ctDNA / ONT IVD).

## Périmètre en 7 dimensions

### 1. Activités
- ✅ Conseil et audit d'infrastructures bioinformatiques
- ✅ Développement et migration de pipelines Nextflow
- ✅ Formation professionnelle (individuelle et groupe)
- ✅ Conception et vente de templates/librairies logiciels sous licence
- ✅ Rédaction technique et pédagogique rémunérée
- ✅ Analyses de données bioinformatiques à la demande (avec restrictions — voir dim. 5)
- ❌ Prestations d'analyse sur données patients humains
- ❌ Conseil sur diagnostic médical
- ❌ Activités réglementées (IVDR, ISO 15189, LDT)
- ❌ Dashboards de traçabilité clinique
- ❌ Expertise judiciaire bioinformatique

### 2. Secteurs / Domaines scientifiques
- ✅ **Zone verte** : plant genomics, microbiome environnemental, microbiome animal/sol, métagénomique shotgun, single-cell recherche, RNA-seq recherche, protéomique, phylogénie, écologie moléculaire, agriculture, élevage, aquaculture, cosmétique microbiome, biocontrole, agronomie
- ❌ **Zone rouge absolue** : oncologie humaine, diagnostic cancer, liquid biopsy, ctDNA, méthylation ADN clinique, Oxford Nanopore IVD, biopsie solide tumorale, thérapies ciblées cancer, médecine de précision, tests génétiques cliniques

### 3. Clients
- ✅ Labos académiques publics hors oncologie (INRAE, CEA, CNRS, Inria)
- ✅ Universités et UMR hors oncologie
- ✅ PME biotech non-IVD (microbiome, agritech, etc.)
- ✅ Agences environnementales (OFB, ADEME)
- ✅ Grands groupes agroalimentaires / cosmétiques
- ⚠️ Instituts de recherche type Pasteur, Curie, ICM : cas par cas
- ❌ CRO (la plupart touchent à l'oncologie)
- ❌ Biotechs IVD / diagnostic médical
- ❌ Concurrents directs AIMA
- ❌ Clients actuels ou prospects AIMA
- ❌ Hôpitaux (CHU, CHG, cliniques)

### 4. Technologies mobilisables
- ✅ Nextflow DSL2, nf-core, Seqera Platform, Docker/Singularity, Git/GitHub Actions, Python (pandas, Click, Pydantic), R (tidyverse, Bioconductor), DuckDB (usage générique), Plotly/Dash, Bash/awk, AWS/Scaleway S3, outils bioinfo publics (samtools, modkit, bwa…)
- ❌ Code source AIMA, pipelines Bam2Beta/Pod2Bam, scripts raima, architecture Aima-Tower, données AIMA, benchmarks internes, conventions de nommage, procédures QC, identifiants samples, documentation interne

### 5. Formats d'intervention
- ✅ Mission forfait (projet clé-en-main), TJM facturé, formation 1-3 jours (week-end ou RTT/CP), formation individuelle en ligne, licence logicielle annuelle, conseil ponctuel
- ⚠️ Abonnement/retainer mensuel : prudence, engagement disponibilité à cadrer
- ❌ Directeur technique fractionnel, administrateur startup concurrente, création de société concurrente

### 6. Volumétrie et horaires
- Maximum **1 jour/semaine en moyenne annuelle**
- Soir (après 19h) et week-end uniquement (sauf RTT/CP posés)
- Priorité absolue au CDI AIMA en cas de conflit horaire
- Pas d'usage du matériel AIMA, pas d'usage des locaux AIMA

### 7. Géographie
- ✅ France, UE, UK, Suisse, Amérique du Nord, reste du monde — aucune restriction géographique dans le contrat AIMA.

## Les 4 pistes retenues

### Piste 1 — Consulting Nextflow académique
- **Cible** : INRAE, CEA, CNRS, Inria, Génoscope, Pasteur (hors onco), CIRAD, IFREMER, universités
- **Offre** : migration Snakemake/bash → Nextflow DSL2 + setup Seqera Platform + formation
- **Tarif** : 550-750 €/jour × 8-12 jours = 5-9 k€/mission
- **Cadence cible** : 1/trimestre à M6, 1/mois à M18

### Piste 2 — BaaS PME biotech non-IVD
- **Cible FR** : Nahibu, Enterome (hors onco), Ÿnsect, Gourmey, NextProtein, Biomemory, Amoéba, Microphyt, Algama, Vitasense
- **Cible UE** : NovaBiome, AgroLiquid, PlantUp, Alga Biosciences
- **Offre** : pipeline production clé-en-main (Nextflow + Docker + CI + doc + handoff)
- **Tarif** : 8-15 k€ forfait ou TJM 600 €/jour sur 15-25 jours
- **Cadence cible** : 3-4 projets/an à M12

### Piste 4 — Pipeline Library Premium (produit scalable)
- **Templates roadmap 18 mois** :
  1. RNA-seq production avec QC Plotly intégré
  2. Métagénomique shotgun + reporting DuckDB
  3. Single-cell multimodal (RNA + ATAC)
  4. Variant calling germline recherche
  5. Benchmark pipeline runner (multi-tools)
- **Modèle** : MIT open-core + Commercial Edition premium
- **Tarifs** : 499 €/an solo | 1 200 €/an équipe ≤10 | 2 500 €/an entreprise illimité
- **Effort** : 80-120h par template (réutilise code missions 1/2)
- **Cadence cible** : 3 templates × 15 licences × 800 € moyen = 36 k€/an passif à M24

### Piste 6 — Formation Nextflow B2B en entreprise
- **Cible** : mêmes PME/CRO que piste 2 + grandes structures (Biotrial, Eurofins, Charles River FR hors onco)
- **Format** : 2-3 jours sur site ou distanciel, 6-12 apprenants
- **Contenu** : DSL2 patterns production, nf-core, Seqera Platform, CI/CD bioinfo, debug
- **Tarif** : 2 000-2 500 €/jour × 2-3 jours = 5-7,5 k€/session
- **Conversion** : chaque mission 1/2 réussie → proposition formation = 50-70 % de conversion attendue
- **Cadence cible** : 6-8 sessions/an à M12

## Positionnement commercial

> **Boris Lipinski — Expert Nextflow production pour la bioinformatique de recherche non-clinique.**
> *"Je transforme vos scripts fragiles en pipelines Nextflow production-grade, documentés, reproductibles."*

## Architecture cascade des 4 pistes

```
Acquisition (LinkedIn + nf-core + blog)
         │
         ▼
   Audit gratuit 30 min (lead qualification)
         │
  ┌──────┼──────┐
  ▼      ▼      ▼
Piste1 Piste2 Piste6
(acad)  (PME) (formation)
  │      │      │
  └──────┼──────┘
         │ extraction patterns récurrents
         ▼
     Piste 4 (templates premium)
         │
         ▼
  Revenu récurrent semi-passif
```

## Prévisionnel financier 24 mois

| Poste | M3 | M6 | M12 | M18 | M24 |
|---|---|---|---|---|---|
| Piste 1 (cumulé €) | 0 | 7 k | 14 k | 21 k | 28 k |
| Piste 2 (cumulé €) | 0 | 0 | 10 k | 25 k | 35 k |
| Piste 6 (cumulé €) | 0 | 5 k | 10 k | 24 k | 40 k |
| Piste 4 (cumulé €) | 0 | 0 | 5 k | 15 k | 30 k |
| **Total cumulé** | 0 | 12 k | 39 k | 85 k | 133 k |
| CA mensuel moyen | 0 | 2,0 k | 3,2 k | 4,7 k | 5,5 k |
| Heures/semaine | 10-12 | 12-15 | 15 | 15 | 15 |

## Statut juridique prévu

- **M0-M12** : micro-entreprise BNC (plafond 77 700 €/an) — largement sous plafond
- **M12-M24** : bascule SASU dès CA mensuel régulier > 5 k€ (meilleure protection sociale + optimisation IS/dividendes)

## Plan d'action step-by-step

### J+7
- Rédiger courrier Art. 10 AIMA (périmètre précis : secteurs + formats + plafond 1 j/semaine)
- RDV Michael CTO pour exposer le projet
- Ouvrir blog technique (Hashnode ou dev.to, domaine perso)
- Sélectionner 1 pipeline nf-core à contribuer
- Landing page simple (1 page, offre 1/2)

### J+30
- Accord écrit AIMA reçu (idéalement "activités de formation et conseil en bioinformatique hors périmètre AIMA")
- Micro-entreprise créée (urssaf.fr, 15 min)
- Compte pro Qonto ou Shine
- 3 articles techniques publiés
- 1 PR nf-core soumise
- Profil LinkedIn en mode "expert Nextflow"

### M+3
- Premier lead entrant via LinkedIn ou nf-core
- Proposition commerciale modèle rédigée (1 page)
- CGV + contrats types prestataire
- Première mission 1 ou 2 signée (5-10 k€)

### M+6
- 1 mission livrée + étude de cas anonymisée publique
- 2e mission en cours
- Formation entreprise upsell en négociation
- Premier template open source publié (teaser piste 4)

### M+12
- CA cumulé : 35-45 k€
- 4-5 clients avec références
- Premier template premium commercialisé (3-5 licences pilotes)
- Formation B2B catalogue formalisé
- Décision bascule SASU si CA > 5 k€/mois

### M+24
- CA année 2 : 90-130 k€
- Templates premium 3 en production, 30-50 licences actives
- 8-12 missions dans l'année
- SASU active

## Canal d'acquisition

1. **LinkedIn pro** (60 % des leads) — 2 posts/semaine, connexions ciblées (directeurs plateformes bioinfo, bioinformaticiens labos, CTO biotech PME). Objectif M6 : 2 000 connexions qualifiées.
2. **Contributions nf-core** (30 %) — 1-2 pipelines à améliorer, devenir mainteneur, 4-6h/semaine sur 3-6 mois.
3. **Conférences & événements FR** (10 %) — JOBIM 2026, Nextflow Summit Barcelona, Seqera Summit Europe.

## 3 challenges à résoudre avant J+7

1. **Piste 6 impose des jours ouvrés** — solutions : formations vendredi+samedi consécutifs, ou négocier 4/5 temps AIMA, ou reporter piste 6 à M7+ avec temps partiel.
2. **Confidentialité 5 ans (Art. 11)** limite le marketing — compensation : contributions nf-core pour crédibilité publique alternative.
3. **Missions CRO risquées** — filtre strict : ne jamais travailler pour un CRO qui touche à l'oncologie, même sur projet déconnecté.

## État d'avancement

- [x] Analyse contrat de travail AIMA et contraintes juridiques
- [x] Benchmark salaire et package (voir `remuneration-package.md`)
- [x] Identification des 4 pistes
- [x] Périmètre en 7 dimensions
- [ ] **Validation synthèse 1 phrase** (arbitrage en cours)
- [ ] Nom commercial + identité visuelle
- [ ] Offres détaillées (fiche produit/service par piste)
- [ ] Grille tarifaire argumentée
- [ ] Plan canal d'acquisition détaillé
- [ ] Choix statut juridique initial
- [ ] Lettre Art. 10 à Michael (texte complet)
- [ ] Templates livrables (proposal, CGV, facture)
- [ ] Lancement (M+1)

## Prochaines étapes (ordre suggéré)

| # | Sujet | Durée estimée |
|---|---|---|
| 1 | Périmètre | ✅ fait |
| 2 | Nom commercial + identité | 30 min |
| 3 | Offres détaillées | 45 min |
| 4 | Tarification | 30 min |
| 5 | Canal d'acquisition | 30 min |
| 6 | Statut juridique | 30 min |
| 7 | Lettre Art. 10 AIMA | 20 min |
| 8 | Premiers livrables | 45 min |
