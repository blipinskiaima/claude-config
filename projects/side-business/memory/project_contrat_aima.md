---
name: contrat-aima-clauses-side
description: Analyse du contrat de travail AIMA de Boris (signé août 2025) — 4 clauses bloquantes pour side business (exclusivité Art.10, confidentialité Art.11, IP Art.12, non-concurrence Art.13). Lancement side conditionné à accord écrit Arnaud SANDRIN.
metadata:
  type: project
---

## Contrat de travail AIMA — analyse des clauses bloquantes pour side business

**Source** : `/home/boris/Téléchargements/LIPINSKI Boris - AIMA Contrat de travail (1).pdf` (15 pages, signé 25 août 2025)

**Rémunération de référence** : 47 100€ brut annuel + bonus annuel potentiel 2 000€ brut, soit 3 925€ brut/mois × 12. Statut Cadre, Position 2.2, coefficient 130, convention collective SYNTEC.

**Forfait jours** : 219 jours/an, 38h30/sem, "réalisation de missions", grande autonomie horaire.

**Lieu** : domicile principal + Grenoble (locaux AIMA Meylan). Télétravail formalisé Article 5.

**Supérieur hiérarchique** : Michaël BLUM (CTO).

---

## 🚨 Article 10 — CONFLITS D'INTÉRÊTS ET OBLIGATION D'EXCLUSIVITÉ (page 8)

**Citation critique** :

> *« Les responsabilités et fonctions du Salarié nécessiteront qu'il consacre à la Société tout le temps nécessaire au bon accomplissement de ses fonctions. Reconnaissant cette nécessité, il réservera l'exclusivité de son activité professionnelle à la Société sauf accord exprès et écrit préalable de cette dernière. »*

**Implication** : Toute activité professionnelle rémunérée parallèle nécessite **accord écrit préalable** d'Arnaud SANDRIN (Président AIMA). Pas de tolérance tacite. Pas d'activité "sous le radar".

**Sévérité** : 🚨 CRITIQUE — c'est LE blocage du side business. Sans levée écrite, Boris s'expose à faute grave.

---

## Article 11 — CLAUSE DE DISCRÉTION ET DE CONFIDENTIALITÉ (page 8)

**Citation** :

> *« Le Salarié s'interdit formellement de divulguer... [les] Informations tant pendant la durée du présent contrat qu'après l'expiration de celui-ci et ce pour une durée de 5 ans à compter de la fin de la mission. »*

**Périmètre très large** : technologies, conceptions, procédés, programmes, **logiciels-sources**, développements de progiciels, architectures de classes, **algorithmes**, conceptions d'interfaces utilisateur, modèles, architectures, bibliothèques de classes, objets, recherches, découvertes, inventions, savoir-faire, dessins, marchés, plans marketing, conditions de rémunération, produits, plans de développement, secrets commerciaux, listes de clients, informations financières.

**Implication** :
- 5 skills bioinfo créés à AIMA (audit-trail, qc-report, batch-effect, debug-nf, check-consistency, etc.) → **propriété AIMA, non redéployables**
- Aima-Survey v2 → **propriété AIMA, non externalisable**
- Architecture Aima-Tower / trace-prod / trace-platform → **savoir-faire confidentiel**
- Méthodes d'industrialisation Nextflow apprises chez AIMA → **savoir-faire à manier prudemment**

---

## Article 12 — PROPRIÉTÉ INTELLECTUELLE (pages 9-13)

### 12.1.3 — Créations dans le cadre du contrat
> *« La Société... sera seule titulaire de l'intégralité des droits de propriété intellectuelle relatifs à toute Création quelle qu'en soit le support, réalisée par le Salarié sous quelque forme que ce soit, dans le cadre du présent contrat, que ce soit en exécution de ses fonctions ou pour des travaux qui lui sont expressément confiés. »*

→ Tout ce que Boris a créé à AIMA depuis août 2025 appartient à AIMA, point.

### 12.2.1 — Inventions hors missions ATTRIBUABLES
> *« La Société... pourra se faire attribuer gratuitement... la propriété ou la jouissance de toute invention qui pourrait être réalisée par le Salarié hors du strict cadre du présent contrat mais néanmoins :*
> - *dans le cours de l'exécution de ses fonctions, ou*
> - *dans le domaine des activités du Groupe ou*
> - *par la connaissance ou l'utilisation des techniques ou des moyens spécifiques au Groupe ou de données procurées par ledit Groupe. »*

🚨 **Implication critique** : Toute création **bioinfo / IA appliquée santé / pipeline / dashboard** que Boris ferait en side TOMBE potentiellement sous cet article. **AIMA peut s'attribuer ses créations side même hors temps de travail** si elles touchent le "domaine d'activités du Groupe".

### 12.2.2 — Inventions hors missions NON ATTRIBUABLES (la zone safe)
> *« Il s'agit des inventions réalisées par le Salarié en dehors de son temps de travail et en l'absence de toute mission inventive permanente ou occasionnelle expressément confiée par la Société. La Société ne pourra faire valoir aucun droit sur l'invention et en conséquence, elle appartiendra de plein droit au Salarié qui pourra en jouir ou en disposer à son gré. »*

→ Pour qu'une création soit "non attribuable" : (1) hors temps de travail, (2) hors mission confiée, (3) **hors domaine d'activité du Groupe**. Les 3 conditions cumulatives.

### 12.3 — Interdiction de dépôt (18 mois post-contrat)
Pendant le contrat ET 18 mois après résiliation, Boris ne peut pas déposer marques/brevets/dessins/modèles pour les créations Article 12 (sauf inventions hors missions non attribuables) sans accord écrit AIMA.

---

## Article 13 — CLAUSE DE NON-CONCURRENCE (pages 13-14)

**S'applique APRÈS la fin du contrat** (pas pendant) :

> *« A la fin du présent contrat, quel que soit le motif de départ et quelle que soit la partie qui en prenne l'initiative Monsieur Boris LIPINSKI s'interdit en outre :*
> - *d'occuper, directement, indirectement, ou par personne interposée et sous quelque statut que ce soit, de fonctions similaires ou concurrentes de celles exercées au sein de la Société*
> - *de s'intéresser directement ou indirectement à toute fabrication et à tout commerce pouvant concurrencer les produits de la Société*
> - *d'engager des membres du personnel de la Société...*
> - *de tenter de détourner, de façon directe ou indirecte, les clients avec lesquels il aura été en contact*

**Durée** : 12 mois après cessation
**Zone** : France entière
**Indemnité versée par AIMA** : **33% du dernier salaire mensuel brut de base** (≈ 1 295€/mois × 12 = ~15 500€)
**Renonciation possible** : AIMA peut renoncer à la clause par lettre recommandée avec AR dans les 30 jours suivant la notification de rupture → libère Boris ET dispense AIMA du versement
**Pénalité en cas de violation** : 12 mois de salaire dus à AIMA + dommages-intérêts

---

## Synthèse impact sur l'offre "DSL2-to-Dashboard"

**Verdict** : L'offre actuelle est **structurellement bloquée** sans accord écrit d'AIMA car :

| Aspect de l'offre | Article concerné | Blocage |
|---|---|---|
| Activité rémunérée parallèle | Art. 10 | Exclusivité non levée |
| Création de skills Claude Code bioinfo | Art. 12.2.1 | "Domaine d'activités du Groupe" |
| Réutilisation des skills déjà créés à AIMA | Art. 11 + 12.1.3 | Confidentialité + IP AIMA |
| Dashboards de production type Aima-Tower | Art. 12.2.1 | "Connaissance/techniques du Groupe" |
| Vente à des labos cliniques | Art. 13 (post-contrat) | Risque clients concurrents |
| Consulting Nextflow industriel | Art. 12.2.1 | "Domaine d'activités du Groupe" si bioinfo santé |

**Activités envisageables sans accord (zone Art. 12.2.2)** :
- Activités strictement hors bioinfo / hors santé (ex : webdev classique, fintech sans liens santé, formations généralistes IA non bioinfo)
- Activités non rémunérées (open source neutre, blog grand public, contribution communautaire) — sous réserve confidentialité Art. 11
- Création artistique / créative sans rapport AIMA

**Activités à risque MAJEUR sans accord** :
- Toute offre B2B bioinfo / pipeline / dashboard de production / IA pour santé
- Consulting Nextflow pour labos / biotechs
- SaaS veille scientifique
- Marketplace skills bioinfo Claude Code
- Audit ISO 15189 bioinfo

---

## Recadrage RDV mi-juin 2026 — 4 ÉTAGES

Le RDV avec Arnaud SANDRIN et Michaël BLUM devient à 4 dimensions :

### Étage 1 — Cap table BSPCE (existant)
- Total shares AIMA, % détenu par Boris
- Calendrier de vesting confirmé
- Clauses bad/good leaver
- Anti-dilution / pre-emption rights
- Acceleration on change of control

### Étage 2 — Négociation nouvelle tranche BSPCE (existant)
- Demande de tranche supplémentaire au strike 64€ avant clôture levée
- Argument bus factor 1, valeur démontrée, fidélisation

### Étage 3 — Renégociation salaire post-cliff (existant)
- Cible : +10 à +15k€ brut/an minimum
- Argument : bus factor 1 + cliff franchi = engagement démontré

### Étage 4 — 🆕 Accord écrit pour activité side business (NOUVEAU)
- Demande de levée partielle ou aménagée de la clause d'exclusivité Article 10
- Définition d'un périmètre acceptable par AIMA
- Validation des "zones safe" (clients, types d'activités, secteurs)
- Engagement écrit pour éviter conflit Article 12.2.1 (IP)

## Options à anticiper pour Étage 4

| Option | Probabilité | Impact |
|---|---|---|
| **(a)** AIMA accepte side dans périmètre strictement hors bioinfo santé | Très probable | Force pivot offre |
| **(b)** AIMA accepte bioinfo avec liste blanche de clients non-concurrents | Possible | Compatible offre actuelle si liste large |
| **(c)** AIMA accepte side sans restriction sectorielle | Peu probable | Idéal mais demande beaucoup |
| **(d)** AIMA refuse toute activité side | Possible si tendu | Choix : rester salarié pur ou partir |
| **(e)** AIMA propose hausse salaire / equity en échange du maintien exclusivité | Possible | Trade-off à évaluer (calcul ROI) |

**Stratégie de négociation** : ouvrir avec **(c)**, accepter **(b)** comme repli, garder **(e)** comme alternative économique si refus.

---

## Actions immédiates pour Boris

| Action | Délai | Statut |
|---|---|---|
| **NE PAS LANCER d'activité side rémunérée** avant accord écrit AIMA | Permanent | À respecter |
| **Préparer le RDV mi-juin** avec dossier complet 4 étages | Avant 15 juin | En cours (S2) |
| **Activités non-rémunérées OK** (open source neutre, blog général) sous réserve confidentialité Art. 11 | Permanent | Ouvert |
| **Lire à nouveau ce fichier avant le RDV** | Avant 15 juin | À programmer |

---

## Liens

Voir [[project_overview]] pour la stratégie globale side business.
Voir [[project_offre_consulting]] pour l'offre "DSL2-to-Dashboard" maintenant conditionnée à l'accord AIMA.
Voir [[project_bspce_negociation]] pour les étages 1-3 du RDV mi-juin.
