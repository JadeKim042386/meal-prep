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

## Repo Layout
- `index.html` — app shell (HTML+CSS+JS inlined)
- `data/*.json` — recipe and ingredient sources (see [[Data Artifacts]])
- `scripts/validate.py` — data integrity checks
- `docs/` — Play Store listing drafts, PWA-to-store notes, superpowers specs/plans
- `sw.js`, `manifest.json`, icon assets — PWA scaffolding

## Relations
- has-data-map [[Data Artifacts]]
- has-handoff [[Handoff]]
- baseline-decision [[ADR 0001 Static Single-Page Architecture]]
