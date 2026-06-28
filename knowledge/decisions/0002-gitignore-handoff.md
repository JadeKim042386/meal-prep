---
title: ADR 0002 Gitignore Handoff
type: note
permalink: adr-0002-gitignore-handoff
tags: [adr, decision, git]
---
# ADR 0002: Gitignore handoff.md

- Date: 2026-06-28
- Status: Accepted

## Context
The Windows reference system tracks the entire `knowledge/` folder in git. On macOS, `handoff.md` is rewritten on every `/save-memory` call, which would produce a steady stream of low-value commits. This is a single-machine setup where git-as-backup for a constantly-churning file adds little.

## Decision
Track `overview.md`, `data-artifacts.md`, and `decisions/` (ADRs) in git, but gitignore `knowledge/handoff.md`. Decision history (ADRs) and stable project facts are preserved; the per-session churn stays local-only. The file remains the source of truth on disk and is re-injected by the SessionStart hook regardless of git status.

## Consequences
- (+) No commit noise from routine handoff updates
- (+) ADR + overview history stays clean and reviewable
- (−) handoff.md is not recoverable from git if lost — acceptable since it is a rolling pointer, not durable decision record
- (−) Slight deviation from the Windows reference (which tracks everything)

## Relations
- affects [[Handoff]]
- refines [[ADR 0001 Static Single-Page Architecture]]
