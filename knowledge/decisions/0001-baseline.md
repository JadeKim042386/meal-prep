---
title: ADR 0001 Static Single-Page Architecture
type: note
permalink: adr-0001-static-single-page
tags: [adr, decision, architecture]
---
# ADR 0001: Static Single-Page Architecture

- Date: 2026-06-28
- Status: Accepted (records existing baseline; not a new change)

## Context
The meal-prep planner targets a single user (and a small audience) and needs zero-cost hosting. Recipes and ingredients are bounded, change infrequently, and don't require server-side computation.

## Decision
Ship as a static single-page app:
- One `index.html` with inlined CSS/JS, no runtime framework
- Recipe data in versioned JSON files under `data/`
- Service worker for PWA install; data fits in browser memory
- Deploy via GitHub Pages

## Consequences
- (+) No server costs, no auth surface, no DB
- (+) Trivial to fork or self-host
- (+) Offline-first via PWA cache
- (−) Adding a new data source requires touching the loader in `index.html`
- (−) Search/clustering must run client-side (acceptable at 98 recipes)

## Relations
- supports [[Overview]]
- constrains [[Data Artifacts]]
