---
title: Meal-Prep Overview
type: note
permalink: overview
tags: [project, overview, meal-prep]
---
# Meal-Prep Overview

Static single-page recipe collection and weekly meal-prep planner. Pure HTML/CSS/JS, deployed via GitHub Pages.

## Facts
- [fact] 98 recipes across Korean / Western / Asian / Mexican / Mediterranean / quick categories #recipes
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
- `index.html` — app shell (HTML+CSS+JS inlined)
- `data/*.json` — recipe and ingredient sources (see [[Data Artifacts]])
- `knowledge/cooking/` — cooking knowledge base (see [[Cooking Knowledge Index]])
- `scripts/validate.py` — data integrity checks
- `docs/` — Play Store listing drafts, PWA-to-store notes, superpowers specs/plans
- `sw.js`, `manifest.json`, icon assets — PWA scaffolding

## Relations
- has-data-map [[Data Artifacts]]
- has-handoff [[Handoff]]
- has-cooking-knowledge [[Cooking Knowledge Index]]
- baseline-decision [[ADR 0001 Static Single-Page Architecture]]
- cooking-knowledge-decision [[ADR 0003 Cooking Knowledge Taxonomy]]
