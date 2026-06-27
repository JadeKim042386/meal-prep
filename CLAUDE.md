# meal-prep — Claude Bootstrap

This project has a Basic Memory store at `knowledge/`. SessionStart hook auto-injects `knowledge/handoff.md` and `knowledge/overview.md` — read those first; ask for them if missing.

## Memory conventions
- Note bodies in English; identifiers (recipe names, ingredient names, paths, tags) stay Korean as-is.
- Use `- [fact|decision|todo|risk] text #tag` for observations, `- relation [[Other Note]]` for relations.
- New decisions → `knowledge/decisions/000N-<slug>.md` (ADR template — see spec §6.3).

## Daily routine
- During work: 자연어로 "메모리에 기록해줘" 또는 `basic-memory tool write-note ...`
- End of session: `/save-memory` (handoff 갱신·status 점검·규약 검증·git 커밋 안내)

## References
- Spec: `docs/superpowers/specs/2026-06-28-basic-memory-design.md`
- Plan: `docs/superpowers/plans/2026-06-28-basic-memory.md`
