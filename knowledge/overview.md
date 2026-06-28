---
title: Meal-Prep Overview
type: note
permalink: overview
tags: [project, overview, meal-prep]
---
# Meal-Prep Overview

Static single-page recipe collection and weekly meal-prep planner. Pure HTML/CSS/JS, deployed via GitHub Pages.

## Facts
- [fact] 50 original, KB-grounded recipes (korean 14 / western 9 / asian 9 / mediterranean 6 / mexican 6 / quickmeal 6) — designed for flavor, not scraped; see [[ADR 0004 Recipe Overhaul]] #recipes
- [fact] Recipes authored in `data/recipes/<category>.json`, built into `index.html` DATA via `scripts/build_data.py`; every recipe passed an adversarial KB flavor rubric #recipes
- [fact] 4 weekly plan modes: balanced / Korean-heavy / high-protein / 초간편 (super-simple) #modes
- [fact] Auto-generated shopping list backed by `localStorage` checkboxes #shopping-list
- [fact] Search by name, ingredient, or tag; category filters via tabs #search
- [fact] Single `index.html` + tiny CSS — no external runtime libraries #tech-stack
- [fact] Service worker (`sw.js`) for PWA install; manifest at `manifest.json` #pwa
- [fact] CSS uses `@property`, `animation-timeline`, `backdrop-filter`; JS uses IntersectionObserver and View Transitions #frontend
- [fact] Deployed at `jadekim042386.github.io/meal-prep` #deployment

## Knowledge Base
- [fact] `knowledge/cooking/` holds a principle/technique-centric cooking knowledge base (59 notes) built to *generate* novel recipes, not just store them — start at [[Cooking Knowledge Index]] #cooking
- [fact] Six domains: principles, flavor science, techniques, flavor-grammars (15 cuisines), ingredients, creativity #cooking

## Repo Layout
- `index.html` — app shell (HTML+CSS+JS inlined); `const DATA` is generated, not hand-edited
- `data/recipes/<category>.json` — authored recipe source of truth (6 files)
- `data/structured_data.json` — built artifact (archival)
- `knowledge/cooking/` — cooking knowledge base (see [[Cooking Knowledge Index]])
- `scripts/build_data.py` — merge recipes → DATA injection into index.html
- `scripts/validate.py` — data integrity checks
- `docs/` — Play Store listing drafts, PWA-to-store notes, superpowers specs/plans
- `sw.js`, `manifest.json`, icon assets — PWA scaffolding

## Relations
- has-data-map [[Data Artifacts]]
- has-handoff [[Handoff]]
- has-cooking-knowledge [[Cooking Knowledge Index]]
- baseline-decision [[ADR 0001 Static Single-Page Architecture]]
- cooking-knowledge-decision [[ADR 0003 Cooking Knowledge Taxonomy]]
