---
title: ADR 0006 Add Korean Soup Recipes
type: note
permalink: adr-0006-add-korean-soups
tags: [adr, decision, recipes]
---
# ADR 0006: Add Korean Soup Recipes

- Date: 2026-06-28
- Status: Accepted

## Context
After simplification ([[ADR 0005 Recipe Simplification and Minimal UI]]) the set skewed heavily to 덮밥/비빔밥 (rice bowls). The user wanted broth-based dishes (김치찌개, 된장찌개 등) for variety.

## Decision
Add 8 Korean soup/stew recipes (addition, not replacement — set grows 50 → 58), authored in a new `data/recipes/soup.json` (auto-merged by `scripts/build_data.py`). `displayCategory` = `korean`; each tagged `국물` + `찌개`/`탕`/`국` for search.

The 8: 돼지고기 김치찌개, 된장찌개, 해물 순두부찌개, 부대찌개, 소고기 미역국, 콩나물국밥, 어묵탕, 소고기 뭇국.

Same constraints as [[ADR 0005 Recipe Simplification and Minimal UI]]: ≤20 min, ≤10 ingredient lines, and a standalone meal (M4) — each soup includes 밥 so it is a complete one-bowl meal. Flavor rubric applies with soup-appropriate judgment: fermented depth (신김치/된장) and 멸치·다시마 다시 carry G3 umami; G2 acid is judged by the dish's tradition (kimchi/sundubu have built-in fermented acid; clear soups like 미역국/뭇국 are not traditionally acidified). Long-simmer soups (설렁탕/갈비탕) are excluded to stay ≤20 min — use 다시(팩)/신김치 fast bases.

## Consequences
- (+) Fixes the 덮밥/비빔밥 imbalance; adds comfort-food variety.
- (+) 58 recipes; korean displayCategory 14 → 22 (still tab-filterable; `국물` tag aids search).
- (−) Soups reheat well but the meal-prep value differs from bowls (store broth + rice; some add 두부/계란 fresh).

## Relations
- extends [[ADR 0005 Recipe Simplification and Minimal UI]]
- relation [[Cooking Knowledge Index]]
- supports [[Overview]]
