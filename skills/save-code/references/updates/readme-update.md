# README.md Update Guide

## Quand Mettre à Jour le README

| Type de changement | Mettre à jour | Section impactée |
|---|---|---|
| Nouvelle feature | Oui | Features, Usage |
| Nouvelle API/endpoint | Oui | API, Usage |
| Changement de setup/install | Oui | Installation, Getting Started |
| Nouvelles dépendances | Oui | Prerequisites, Installation |
| Changement de commandes | Oui | Usage, Commands |
| Changement de config | Oui | Configuration |
| Bug fix | Non (sauf si workaround documenté) | — |
| Refactoring interne | Non | — |
| Changement de style/lint | Non | — |

## Comment Mettre à Jour

### 1. Lire le README existant
```bash
Read: ./README.md
```

### 2. Identifier les sections impactées

Sections typiques d'un README :
- **Description** — le projet a-t-il changé de scope ?
- **Features** — nouvelle fonctionnalité à ajouter ?
- **Installation** — nouvelles étapes de setup ?
- **Usage** — nouvelles commandes ou API ?
- **Configuration** — nouveaux paramètres ?
- **Architecture** — changement structurel majeur ?
- **Contributing** — nouvelles conventions ?

### 3. Rédiger la mise à jour

**Principes :**
- Matcher le style existant du README (ton, format, langue)
- Ajouter au bon endroit dans la section existante (pas à la fin en vrac)
- Inclure des exemples de code si la section en contient déjà
- Ne pas réécrire les sections non impactées

### 4. Proposer les changements

Montrer à l'utilisateur un diff clair :
```
Section "Features" :
+ - **Health Check** : endpoint GET /api/health pour monitoring

Section "Usage" :
+ ```bash
+ curl http://localhost:3000/api/health
+ ```
```

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Réécrire tout le README | Modifier uniquement les sections impactées |
| Ajouter des sections vides | N'ajouter que si du contenu existe |
| Documenter des détails d'implémentation | Documenter l'usage et le comportement |
| Changer le style/format du README | Matcher le style existant |
| Mettre à jour pour un simple bug fix | Ignorer sauf si un workaround était documenté |
