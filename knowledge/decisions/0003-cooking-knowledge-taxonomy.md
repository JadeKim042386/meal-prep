---
title: ADR 0003 Cooking Knowledge Taxonomy
type: note
permalink: adr-0003-cooking-knowledge-taxonomy
tags: [adr, decision, cooking, knowledge]
---
# ADR 0003: Cooking Knowledge Taxonomy

- Date: 2026-06-28
- Status: Accepted

## Context
The user wants a knowledge base that enables *creating* novel, delicious recipes — not just storing fixed ones. A large flat pile of recipes is shallow and does not transfer to invention. What generates creativity is the underlying layer: flavor science, technique mechanics, balance principles, ratios, and per-cuisine flavor "grammars."

## Decision
Build a **principle/technique-centric** knowledge base under `knowledge/cooking/`, organized into six domains, at maximum research depth (deep-research backed):

- `principles/` — universal rules (salt-fat-acid-heat, balancing, ratios, building depth, heat management)
- `flavor/` — taste & aroma science (umami synergy, pairing theory, aroma compound families)
- `techniques/` — transformation mechanisms (heat methods, maillard, emulsification, fermentation, sauces, doughs…)
- `flavor-grammars/` — per-cuisine pairing logic (the way each cuisine "thinks")
- `ingredients/` — ingredient behavior & creative substitution
- `creativity/` — synthesis layer that ties the others into an actual recipe-invention process

Recipes appear only as **illustrative examples** inside notes, never as the primary unit.

## Build method
Domain work is fanned out to ~9 parallel subagents (some domains split for load balance). Each subagent researches its domain (deep-research / multi-source web search with cross-verification) and writes markdown notes directly into its subdirectory, following the project's note conventions (English bodies; Korean identifiers; `- [type] text #tag` observations; `- relation` wikilinks). Notes cross-link richly across domains — those links are the substrate for creative connection.

## Consequences
- (+) Knowledge transfers to *new* dishes, not just stored ones
- (+) Cross-links between principle ↔ technique ↔ grammar enable flavor bridging
- (+) Parallel subagents keep build fast; distinct subdirs avoid write conflicts
- (−) High one-time research cost (max-depth deep-research across ~9 domains)
- (−) ~60 notes to maintain; factual claims (flavor science, ratios) need periodic review

## Relations
- supports [[Overview]]
- extends [[Handoff]]
