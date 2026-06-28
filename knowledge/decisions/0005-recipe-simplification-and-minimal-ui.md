---
title: ADR 0005 Recipe Simplification and Minimal UI
type: note
permalink: adr-0005-recipe-simplification-and-minimal-ui
tags: [adr, decision, recipes, ui]
---
# ADR 0005: Recipe Simplification and Minimal UI

- Date: 2026-06-28
- Status: Accepted

## Context
After the recipe overhaul ([[ADR 0004 Recipe Overhaul]]), the user wanted the app simpler and more practical: (1) the top-of-page aggregate stats (visitor count, total recipes, average cook time, one-pan ratio) added no value, and (2) recipes should use simple ingredients, cook fast, and be real meals — not side dishes.

## Decision
1. **Minimal header UI** — remove the hits.sh visitor badge and the 4-card stats hero (`renderStats`/`animateCounters`/`statsGrid` + related CSS). Replace with the title + a one-line tagline ("간단한 재료로, 빠르게 만드는 한 주 식단"). Per-recipe cook time stays (useful per dish; only the aggregate hero is removed).
2. **Recipe constraints (rubric D5 + M4)** — every recipe must be `cookTime ≤ 20` min, `≤ 10` ingredient lines, and a **standalone one-dish meal** (no 반찬/밑반찬/나물/곁들임). Flavor gates G1–G9 still apply — fast/simple is not an excuse for flat.
3. **Regenerate all 50** across the same 6 categories via the established pipeline (roster → category authoring → adversarial KB review → `build_data.py`), replacing slow/complex/side-leaning dishes with simple, fast meals.

## Consequences
- (+) Cleaner first impression; the page leads with content, not vanity metrics.
- (+) Recipes match real weeknight constraints (fast, few ingredients, a full meal).
- (−) Some depth-from-time techniques (long braises) are out; depth now comes from fast levers (sear, bloom, umami stacking, finishing acid).
- (−) The `quickmeal` displayCategory is less distinct now that all recipes are ≤20 min; kept as a shared-pantry family for the 초간편 clusterer.
- (~) `isSideDish` in `index.html` becomes a no-op (no sides in data); left in place harmlessly.

## Relations
- supersedes-recipes [[ADR 0004 Recipe Overhaul]]
- relation [[Cooking Knowledge Index]]
- supports [[Overview]]
