---
name: MFP API
description: Endpoints MFP, auth, Rails vs v2, workflow création repas, IDs aliments connus
type: reference
---

# MFP API — Endpoints & Tools

## Projet
- **Path** : `/home/boris/App/Myfitnesspal/`
- **Fichier principal** : `tools.py`
- **MCP Server** : `mcp_server.py` (9 tools exposés)
- **Auth** : Chrome Profile 2 cookies + Bearer token (extrait du token base64)

## Endpoints READ (confirmés)
- `GET www.myfitnesspal.com/api/services/users/meals/mine` → templates repas sauvés
- `GET www.myfitnesspal.com/api/services/nutrient-goals` → objectifs journaliers
- `GET api.myfitnesspal.com/v2/diary?entry_date=YYYY-MM-DD` → agrégats par slot
- `GET api.myfitnesspal.com/v2/nutrition?q=...` → recherche aliments (v2 IDs)
- `GET api.myfitnesspal.com/v2/foods/{v2_id}` → détails aliment + serving sizes
- Diary HTML `GET www.myfitnesspal.com/food/diary?date=YYYY-MM-DD` → parsing entry_ids

## Endpoints WRITE (confirmés)
- `POST www.myfitnesspal.com/food/add` → ajouter aliment (Rails IDs requis)
  - `food_entry[meal_id]`: 0=Déjeuner, 1=Dîner
  - Retourne 204 toujours (même en échec)
- `POST api.myfitnesspal.com/v2/diary` → ajouter aliment (v2 IDs)
  - ⚠️ **CRITIQUE** : inclure `meal_position: 1` pour forcer le slot Dîner, sinon meal=None et invisible
  - Format : `{items: [{type:'food_entry', date, food:{id}, serving_size:{unit,value}, servings, meal_position:1}]}`
- `POST www.myfitnesspal.com/meal/create` → créer template depuis journal (confirmé)
  - Capture UNIQUEMENT les entrées du slot spécifié (Dîner = meal_id 1)
  - Les entrées v2 sans meal_position vont dans slot None → NON capturées
- `DELETE www.myfitnesspal.com/food/remove/{entry_id}` → supprimer entrée journal
- `DELETE www.myfitnesspal.com/api/services/users/meals/delete/{meal_id}` → supprimer template
- `POST www.myfitnesspal.com/food/edit_entry/{entry_id}` → modifier quantité (confirmé)

## Rails IDs connus (favoris Boris)
| Aliment | food_id | weight_id | Unité serving |
|---|---|---|---|
| Oeuf - Œuf | 2714639913 | 3131104598 | 53g (1 oeuf) |
| Pomme - Golden | 2714603448 | 3130999905 | 100 grammes |
| Tomates | 2985713186 | 3445012366 | 1 moyenne |
| Olive - Huile | 2714643503 | 3131130715 | 1 gram |
| Pomme de terre | 2714642345 | 3131121897 | 1 gram |
| Sauce bolo auchan | 3009524556 | 3472819080 | 1 gramme |
| Oignon | 2714641684 | 3131117186 | 1 gram |

## V2 IDs connus (pour les aliments hors favoris)
| Aliment | v2_id | unit | value | kcal/100g |
|---|---|---|---|---|
| Riz Cru | 159727286668909 | g | 100.0 | 340 |
| Steak Haché 5% | 124966272970413 | grammes | 100.0 | 193 |
| Thon émietté | 123840864650869 | g | 100.0 | 94 |
| Pâtes Panzani | 98002307665709 | gram | 100.0 | 365 |
| Viande Hachée 5% | 265291190644589 | g | 100.0 | 128 |
| Sauce Provençale Auchan | 159735775940461 | gram | 100.0 | 50 |

## Workflow : créer un template de repas
1. Choisir une date inutilisée (ex: 2020-06-XX)
2. Ajouter les aliments au journal sur cette date :
   - **Rails** (favoris) : `tools.add_food(food_id, weight_id, qty, date, 'Dîner')`
   - **V2** (hors favoris) : POST v2/diary avec `meal_position: 1` (OBLIGATOIRE)
3. `tools.create_saved_meal(name, date, 'Dîner')` → sauvegarde le template
4. Vérifier avec `tools.list_saved_meals()` que les calories et nb foods sont corrects
5. NE PAS supprimer les anciens templates avant vérification

## Problèmes connus
1. **v2 sans meal_position → slot None** : les entrées sont invisibles dans le HTML et non capturées par create_saved_meal
2. **v2 entries non supprimables via Rails** : pas de delete endpoint v2, et le Rails delete ne les trouve pas
3. **add_food (Rails) retourne 204 même en échec** : vérifier avec get_diary après
4. **copy_meal ignore from_meal/to_meal** : copie toujours Déjeuner
5. **Pas d'endpoint pour modifier les templates** : il faut delete + recreate
6. **Dates polluées** : 1999-01-01 et 2020-01-XX à 2020-05-XX ont des entrées v2 orphelines non supprimables
