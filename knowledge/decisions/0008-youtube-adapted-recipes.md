---
title: ADR 0008 YouTube-Adapted App Recipes
type: note
permalink: adr-0008-youtube-adapted-recipes
tags: [adr, decision, recipes]
---
# ADR 0008: YouTube-Adapted App Recipes

- Date: 2026-07-18
- Status: Accepted

## Context
A research pass compiled 165 source-verified recipes from 10 Korean 자취요리 YouTube channels (`knowledge/research/자취요리-youtube/`). The user wants some of these in the app. But the app is deliberately original & KB-grounded ([[ADR 0004 Recipe Overhaul]]) and constrained to simple/fast standalone meals ([[ADR 0005 Recipe Simplification and Minimal UI]]) — pasting scraped recipes verbatim would regress on both flavor quality and the meals-only rule.

## Decision
Curate ~30 **meal-type** YouTube recipes (excluding 반찬/간식/디저트 and dishes that duplicate the existing 58) and **adapt each through the KB flavor rubric** to app quality, rather than copying them verbatim. Authored into a new `data/recipes/youtube.json` (auto-merged by `scripts/build_data.py`), **added** to the existing set (58 → ~88), not replacing it.

- Every adapted recipe must still pass the rubric: ≤20 min, ≤10 ingredient lines, standalone meal (M4), and flavor gates G1–G9 (salt %, finishing acid, umami synergy, browning, texture, aroma, grammar coherence).
- Attribution: `source` = the original recipe URL (recipio.kr / YouTube), `sourceName` = `"<채널명> · YouTube (KB 각색)"` — credits the channel and marks it as an adaptation, not a verbatim copy.
- Same pipeline: curate roster → author → adversarial rubric review + fix → build → validate → deploy.

## Consequences
- (+) Brings the flavor/variety of popular 자취요리 into the app without losing the KB quality bar or the meals-only rule.
- (+) Sources are explicitly credited; recipes are adaptations, so no verbatim scraping into app data.
- (−) korean displayCategory grows further (already 22); mode/tab still scale fine.
- (−) "Adapted" recipes differ from the creators' originals by design — the app is not a faithful mirror of any channel.

## Relations
- builds-on [[ADR 0004 Recipe Overhaul]]
- builds-on [[ADR 0005 Recipe Simplification and Minimal UI]]
- relation [[자취요리 YouTube 채널 조사 인덱스]]
- supports [[Overview]]
