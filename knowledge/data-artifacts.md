---
title: Meal-Prep Data Artifacts
type: note
permalink: data-artifacts
tags: [project, data, meal-prep]
---
# Meal-Prep Data Artifacts

Pointer map for raw data files. Do not paste entire file contents into notes — record paths and roles only.

## JSON Sources
| File | Role |
|---|---|
| `data/ingredients.json` | Ingredient master list (Korean names, categories) |
| `data/recipes_korean.json` | Korean main dishes |
| `data/recipes_global.json` | Western / Asian / Mexican / Mediterranean dishes |
| `data/recipes_highprotein.json` | High-protein recipe set |
| `data/recipes_youtube.json` | Recipes ported from YouTube creators (e.g. 자취요리신) |
| `data/recipes_additional.json` | Misc additions (sides, drinks, snacks) |
| `data/structured_data.json` | Schema.org structured data for SEO/Open Graph |

## Scripts
- `scripts/validate.py` — verifies recipe schema and ingredient references

## Notes
- [fact] All recipe IDs and ingredient names are Korean and serve as identifiers #identifiers
- [risk] Adding new JSON sources without updating `index.html` loader will silently exclude them #risk

## Relations
- maps-for [[Overview]]
