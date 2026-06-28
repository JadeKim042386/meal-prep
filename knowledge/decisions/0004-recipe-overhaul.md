---
title: ADR 0004 Recipe Overhaul
type: note
permalink: adr-0004-recipe-overhaul
tags: [adr, decision, recipes, cooking]
---
# ADR 0004: Recipe Overhaul

- Date: 2026-06-28
- Status: Accepted

## Context
The original 98 recipes were scraped from 만개의레시피 / YouTube. They are generic and under-built: a single salt dump, no acid finish, no umami layering, no browning/texture-contrast, and seasonings often incoherent with the dish's cuisine. The user's verdict: "다 맛이 존나 없어." A static recipe pile cannot be improved by tweaking; it must be *designed*. We now have a principle/technique-centric cooking knowledge base ([[Cooking Knowledge Index]], [[ADR 0003 Cooking Knowledge Taxonomy]]) capable of grounding deliberate flavor design.

## Decision
Delete the scraped recipe set and replace it with ~50 original, genuinely-delicious meal-prep recipes designed from the KB and verified by KB-grounded adversarial review.

- Source of truth becomes `data/recipes/<category>.json` (6 authored files), replacing the scraped `data/recipes_*.json`.
- A new `scripts/build_data.py` merges them, computes stats, builds a default `weeklyPlan` + (archival) `shoppingList`, writes `data/structured_data.json`, and injects the minified JSON into the `const DATA = …;` line of `index.html` (the app's runtime source).
- Every recipe must pass a shared rubric: flavor gates (salt%/layering, finishing acid, umami synergy, Maillard/depth, fat balance, texture contrast, aromatic finish, grammar coherence, composition completeness), meal-prep gates (batch/store/reheat/make-ahead), and data gates (purchasable ingredients, technique-cued steps, plausible macros, valid schema).
- `scripts/validate.py` remains the machine integrity gate; the rubric review is the flavor gate. Both are mandatory.

## Consequences
- (+) Recipes are *designed for flavor*, not scraped — addresses the root cause.
- (+) A real build step (`build_data.py`) replaces hand-editing a 220 KB inline `DATA` line.
- (+) `data/recipes/` is organized, diffable, and regenerable.
- (−) One-time heavy authoring + adversarial-review cost (~50 recipes).
- (−) Flavor is verified by KB reasoning, not by actually cooking — a model, not a taste test.
- (−) Fewer recipes (~50 vs 98); mitigated by quality and by keeping mode coverage (korean / protein≥30 / cookTime≤20) above the app's thresholds.

## Relations
- supports [[Overview]]
- relation [[Cooking Knowledge Index]]
- builds-on [[ADR 0003 Cooking Knowledge Taxonomy]]
- baseline [[ADR 0001 Static Single-Page Architecture]]
