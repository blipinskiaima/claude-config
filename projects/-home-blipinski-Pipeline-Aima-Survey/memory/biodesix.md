---
name: biodesix
description: "Biodesix (BDSX), 8e concurrent surveillé : protéomique poumon, aucune épigénétique, et le chiffre que leurs communiqués ne donnent jamais"
metadata:
  node_type: memory
  type: reference
  modified: 2026-08-26T00:00:00.000Z
---

Ajoutée à la veille le 2026-08-26. `tier_3`, menace **BASSE**. Dossier complet :
`concurency/profils/BIODESIX-P{0,1,2,3}-*.md`.

## Le verdict technique, en une ligne

**Ni méthylation, ni fragmentomique, ni CNV genome-wide.** Nulle part : ni en produit, ni dans
le pipeline AACR 2026, ni en brevet. Trois piliers orthogonaux au nôtre — protéomique
(MALDI-TOF sérum, MRM-MS plasma), auto-anticorps ELISA, ddPCR/NGS mutationnel. La seule
intersection est le CNV du module NGS, sur 12 gènes ciblés.

Placée en `tier_3` aux côtés de `20/20 Gene Systems` (« multi-biomarqueurs protéiques ») : dans
ce référentiel, le tier mesure la **proximité à notre modalité**, pas la taille de la société —
Oxford Nanopore y est aussi, et Biodesix fait 88,5 M$ de chiffre d'affaires.

## Ce qui ne se redéduit pas du dossier

**VeriStrat mesure l'inflammation de l'hôte, pas la tumeur.** Ses 8 features spectrales sont des
protéoformes de SAA1, SAA2, SAA4, CRP et β2-microglobuline — protéines de la phase aiguë
(PMID 38074293). Aucune sensibilité de détection n'existe ni ne peut exister pour ce test :
toute source qui en présente une est à écarter.

**Le chiffre absent de tous leurs communiqués.** Le communiqué du 20/03/2026 titre « la plus
grande étude de validation de biomarqueur de nodule jamais publiée » et ne publie que la
spécificité. Le résumé PubMed (PMID 41703731, n=1164, prévalence 35 %) donne la sensibilité :
**16 % au seuil Moderate, 9 % au seuil High**, pour 91 % et 96 % de spécificité. C'est une
analyse **groupée rétrospective**, pas un essai prospectif. Piège type : aller lire la source.

**Deux tests délibérément opposés** : Nodify XL2 est un *rule-out* (97 % / 44 %, n=178, PANOPTIC
PMID 29496499), Nodify CDT un *rule-in* (16 % / 90 %, n=447, PMID 40296864). Ne jamais les citer
comme s'ils mesuraient la même chose.

**ORACLE porte un signal de sécurité que le communiqué tait** : −74 % de procédures invasives
(PMID 37432960), mais les nodules **malins** envoyés en surveillance passent de 3,5 % à 7,5 %
(p = 0,075). C'est la question qui nous sera posée à nous le jour où un score AIMA servira à
**ne pas** faire un geste.

## Deux divergences de registre, constatées et non corrigées

- **PANOPTIC est sponsorisé par Integrated Diagnostics**, pas Biodesix (registre NCT01752114) :
  la validation princeps de leur produit phare est **antérieure au rachat** de 2018. Le registre
  dit n=684, la publication n=685.
- **ALTITUDE (NCT04171492)** s'intitule « A Multicenter, **Randomized Controlled Trial** … »
  mais est enregistré `studyType: OBSERVATIONAL`, `observationalModel: COHORT`. Lecture attendue
  **fin 2026** : c'est l'essai d'utilité clinique, et un observationnel ne démontre pas ce qu'un
  randomisé démontre. Constater, ne pas trancher à leur place.

## L'angle défendable pour AIMA — et sa réserve

Nodify CDT publie à **90-96 % de spécificité**, c'est-à-dire dans le régime de nos 95,1 % — ce
qui est rare, DELFI et Freenome publiant tout à ~50 %. À point de fonctionnement comparable, un
test qui lit la **réponse de l'hôte** plafonne sous 20 % de sensibilité ; un test qui lit le
**signal tumoral** n'a pas ce plafond structurel. L'argument vaut contre la **modalité**, pas
contre l'entreprise.

⚠ Ne pas en conclure que nous serions neuf fois meilleurs : leurs négatifs sont des nodules
bénins chez des patients déjà suspects, les nôtres des sujets sains. **Leur question est plus
difficile.** Le jour où nous produirons des chiffres sur une cohorte de nodules, c'est le
**97 % / 44 %** de Nodify XL2 qu'il faudra battre, pas les 9 %.

## Ce que ce dossier a appris sur NOS verrous

- **Verrou n°1 partiellement franchi par d'autres** : `SPOT-MAS` (eLife 2023, PMID 37819044)
  profile méthylation + fragmentomique + CNV + end motifs dans **un seul workflow à ~0,55×**,
  738 cancers / 1550 sains, **72,4 % @ 97,0 %**. « Aucun classifieur publié à ce niveau » ne tient
  plus. Reste vierge : la **résolution par base** et le **5mC + 5hmC natifs simultanés**.
- **Verrou n°2 confirmé empiriquement** : `NanoRCS` mesure **R² = 0,34** entre distributions de
  tailles Illumina et nanopore ; l'équipe qui a tenté la fragmentomique ONT a re-calibré ses
  propres bornes plutôt que de reprendre DELFI. Notre prudence est désormais sourcée.
- ⚠ **À ne jamais citer** : le « 97 % / 93 %, AUC 0,951 » présenté comme un classifieur nanopore
  vient de **mélanges synthétiques in silico** (Genome Medicine 2023, PMID 37138315), sur 20-23
  patients **colorectaux**, à **200 millions de reads**.

## Surveillance

`watch` = `sec_cik: 0001439725` + `clinicaltrials_sponsor: Biodesix` + **`newsroom_page`**
(`/newsroom/press-releases`, index vers GlobeNewswire). Pas `newsroom_sitemap` : voir le piège
documenté dans [[veille_concurrentielle_collecteur]]. Profondeur du canal limitée à ~20
communiqués, soit ~10 mois — le début d'une fenêtre à 12 mois n'est couvert que par la SEC.

À surveiller : **ALTITUDE fin 2026**, et tout signe que leur **pipeline MRD pan-cancer** (ddPCR,
avec Memorial Sloan Kettering) sort — il les ferait entrer sur notre ligne MRD.

Voir [[dossiers_concurrent_p1p2p3]], [[veille_concurrentielle_collecteur]],
[[competitive_landscape]], [[aima_positioning_profil]].
