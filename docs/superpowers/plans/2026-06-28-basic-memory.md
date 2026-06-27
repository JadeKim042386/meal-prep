# Basic Memory 기반 검색·문서화 시스템 (macOS 포팅) Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** macOS(zsh, miniconda uv 환경)에 Windows에서 운영 중인 Basic Memory(MCP) 지식메모리 시스템을 1:1로 재현한다. 중앙 허브(`desktop`) + 프로젝트(`meal-prep`) 하이브리드, SessionStart 훅·`/save-memory`·`CLAUDE.md` 풀 자동화, Q3-D 안전장치(`basic-memory status` 자동 점검 + 노트 규약 검증) 포함.

**Architecture:** 6계층(저장 Markdown / 색인 SQLite+fastembed / 엔진 basic-memory 0.22.1 / 연결 MCP user-scope 1개 / 자동화 zsh hook + slash command + CLAUDE.md / 구성 desktop+meal-prep 하이브리드). 진실의 원천은 `knowledge/*.md`; SessionStart 훅은 `${CLAUDE_PROJECT_DIR:-$PWD}` 기준 라우팅으로 `cat` 한 결과를 stdout으로 출력해 세션 컨텍스트에 자동 주입한다.

**Tech Stack:** Basic Memory 0.22.1 (Python, uv 설치), MCP (Claude Code user 스코프), zsh, jq, fastembed(bge-small-en, 로컬), SQLite.

**Spec:** `docs/superpowers/specs/2026-06-28-basic-memory-design.md` — 본 계획서는 그 스펙의 §1–§9 결정을 그대로 구현한다.

---

## 사전 준비

- **사용자 동의 항목**: 본 계획은 `~/.claude/settings.json`(user 스코프), `~/.claude/hooks/`, `~/.claude/commands/`, `~/Desktop/knowledge/`(신규 git repo), `~/Desktop/meal-prep/{CLAUDE.md,knowledge/}` 를 모두 작성/수정한다. 모두 사용자 머신 로컬·되돌릴 수 있는 변경.
- **확인사항**: `which uv` → 존재, `which jq` → 존재(없으면 `brew install jq`), 디스크 ≥ 500MB 여유(임베딩 모델 캐시).
- **참고 스킬**: 본 구현은 단계 검증 시 `@superpowers:verification-before-completion`을 따른다 — "통과했다"고 주장하기 전에 명령 결과를 직접 확인.

## File Structure

생성/수정 대상과 책임을 한눈에 잠금.

| 경로 | 동작 | 책임 |
|---|---|---|
| `~/.local/bin/basic-memory` | 생성(설치 산출물) | Basic Memory 엔진 바이너리 |
| `~/.claude/settings.json` | 수정 | SessionStart 훅 항목 추가 (user 스코프) |
| `~/.claude/hooks/basic-memory-session-start.sh` | 생성 | 라우팅된 handoff/overview를 stdout으로 출력 |
| `~/.claude/commands/save-memory.md` | 생성 | `/save-memory` 슬래시 명령 본문 (Claude가 따를 절차) |
| `~/Desktop/knowledge/` | 생성(폴더) | 중앙 허브 프로젝트 `desktop` 루트 |
| `~/Desktop/knowledge/overview.md` | 생성 | 빈 골격 |
| `~/Desktop/knowledge/handoff.md` | 생성 | 빈 골격 |
| `~/Desktop/knowledge/decisions/.gitkeep` | 생성 | 빈 폴더 보존 |
| `~/Desktop/knowledge/analysis/.gitkeep` | 생성 | 빈 폴더 보존 |
| `~/Desktop/knowledge/.gitignore` | 생성 | 색인/캐시 산출물 차단 |
| `~/Desktop/knowledge/.git/` | 생성(`git init`) | 신규 독립 리포지토리 |
| `~/Desktop/meal-prep/CLAUDE.md` | 생성 | 프로젝트 부트스트랩 (4줄) |
| `~/Desktop/meal-prep/knowledge/overview.md` | 생성 | 시드: 98 레시피·4 모드·기술 스택 |
| `~/Desktop/meal-prep/knowledge/handoff.md` | 생성 | 시드: 최근 커밋 흐름 + 다음 작업 |
| `~/Desktop/meal-prep/knowledge/data-artifacts.md` | 생성 | 시드: `data/*.json` 지도 |
| `~/Desktop/meal-prep/knowledge/decisions/0001-baseline.md` | 생성 | 시드: 베이스라인 ADR |
| `~/Desktop/meal-prep/.gitignore` | 수정(append) | `knowledge/` 내부 색인/캐시 차단(필요시) |

테스트 코드 파일은 없다 — 본 시스템은 **수동 검증 + 명령 출력 매칭**으로 검증한다(`§Task 12`).

---

## Task 1: Basic Memory 엔진 설치

**Files:**
- Install: `~/.local/bin/basic-memory` (uv tool 산출물)

- [ ] **Step 1: 기존 설치 여부 확인 (테스트 — 실패 기대)**

Run:
```bash
basic-memory --version 2>&1 || echo "NOT_INSTALLED"
```
Expected: `NOT_INSTALLED` (이미 설치되어 0.22.1+이면 Task 1 전체 건너뛰기)

- [ ] **Step 2: uv tool로 설치**

Run:
```bash
uv tool install basic-memory
```
Expected: `Installed 1 executable: basic-memory` (혹은 이미 설치됨 메시지)

- [ ] **Step 3: PATH 확인**

Run:
```bash
ls ~/.local/bin/basic-memory && echo "OK"
```
Expected: 경로 표시 + `OK`. 없으면 `uv tool dir` 확인 후 PATH(`~/.zshrc`) 점검.

- [ ] **Step 4: 버전 검증 (Step 1의 "통과 기대")**

Run:
```bash
basic-memory --version
```
Expected: `0.22.1` 이상.

- [ ] **Step 5: 커밋 — 해당 없음**

엔진 설치는 사용자 시스템에 한정된 변경으로 리포지토리 커밋 대상 아님. 다음 Task로 진행.

---

## Task 2: knowledge 디렉토리 골격 생성

**Files:**
- Create: `~/Desktop/knowledge/{decisions,analysis}/`
- Create: `~/Desktop/meal-prep/knowledge/{decisions,analysis}/`

- [ ] **Step 1: 사전 확인 (실패 기대)**

Run:
```bash
ls ~/Desktop/knowledge ~/Desktop/meal-prep/knowledge 2>&1
```
Expected: `No such file or directory` 2회.

- [ ] **Step 2: 폴더 생성**

Run:
```bash
mkdir -p ~/Desktop/knowledge/{decisions,analysis}
mkdir -p ~/Desktop/meal-prep/knowledge/{decisions,analysis}
```
Expected: 무반응(성공).

- [ ] **Step 3: 빈 폴더 보존용 `.gitkeep`**

Run:
```bash
touch ~/Desktop/knowledge/decisions/.gitkeep \
      ~/Desktop/knowledge/analysis/.gitkeep \
      ~/Desktop/meal-prep/knowledge/decisions/.gitkeep \
      ~/Desktop/meal-prep/knowledge/analysis/.gitkeep
```

- [ ] **Step 4: 검증**

Run:
```bash
ls -a ~/Desktop/knowledge ~/Desktop/meal-prep/knowledge
```
Expected: 각각 `decisions analysis` 폴더 표시.

- [ ] **Step 5: 커밋 — Task 11에서 함께**

---

## Task 3: 중앙 허브 시드 노트 (빈 골격) 작성

**Files:**
- Create: `~/Desktop/knowledge/overview.md`
- Create: `~/Desktop/knowledge/handoff.md`
- Create: `~/Desktop/knowledge/.gitignore`

- [ ] **Step 1: `overview.md` 작성**

Write `~/Desktop/knowledge/overview.md`:
```markdown
---
title: Desktop Hub Overview
type: note
permalink: overview
tags: [hub, overview]
---
# Desktop Hub Overview

Central knowledge hub for all non-project notes on this Mac.

- [fact] Hub root is `~/Desktop/knowledge/` #hub
- [fact] Per-project memory lives next to the project (e.g. `~/Desktop/meal-prep/knowledge/`) #routing
- [note] SessionStart hook routes by `${CLAUDE_PROJECT_DIR:-$PWD}` — if the project has its own handoff, the hub is skipped #automation

## Relations
- routes-to [[Handoff]]
```

- [ ] **Step 2: `handoff.md` 작성**

Write `~/Desktop/knowledge/handoff.md`:
```markdown
---
title: Desktop Hub Handoff
type: note
permalink: handoff
tags: [hub, handoff]
---
# Desktop Hub Handoff

- [fact] Initialized on 2026-06-28 as part of Basic Memory macOS port #setup
- [todo] Add per-topic notes here as they come up — design notes, research scratchpads, cross-project decisions #next

## Next Session
- Use `/save-memory` to record any cross-cutting work that doesn't belong to a single project.
```

- [ ] **Step 3: `.gitignore` 작성 (색인/캐시 차단)**

Write `~/Desktop/knowledge/.gitignore`:
```
# Basic Memory keeps DB/cache outside this folder by default,
# but guard against any project-local artifacts just in case.
.bm-cache/
*.db
*.sqlite
*.sqlite-*
.DS_Store
```

- [ ] **Step 4: 검증**

Run:
```bash
ls ~/Desktop/knowledge && head -5 ~/Desktop/knowledge/overview.md
```
Expected: `overview.md handoff.md decisions analysis .gitignore` + frontmatter 첫 줄들.

- [ ] **Step 5: git init + 초기 커밋 (중앙 허브 = 신규 리포지토리)**

Run:
```bash
cd ~/Desktop/knowledge && git init && git add . && git commit -m "init: desktop hub skeleton"
```
Expected: `[main (root-commit) <sha>] init: desktop hub skeleton`.

---

## Task 4: meal-prep 시드 노트 작성 (풀 시드)

**Files:**
- Create: `~/Desktop/meal-prep/knowledge/overview.md`
- Create: `~/Desktop/meal-prep/knowledge/handoff.md`
- Create: `~/Desktop/meal-prep/knowledge/data-artifacts.md`
- Create: `~/Desktop/meal-prep/knowledge/decisions/0001-baseline.md`

- [ ] **Step 1: 프로젝트 상태 재확인**

Run:
```bash
cd ~/Desktop/meal-prep && ls data/*.json | xargs -n1 basename && git log --oneline -10
```
Expected: 7개 JSON (`ingredients`, `recipes_*`, `structured_data`) + 최근 커밋 10개. 시드에 그대로 반영.

- [ ] **Step 2: `overview.md` 작성**

Write `~/Desktop/meal-prep/knowledge/overview.md`:
```markdown
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
```

- [ ] **Step 3: `handoff.md` 작성**

Write `~/Desktop/meal-prep/knowledge/handoff.md`:
```markdown
---
title: Meal-Prep Handoff
type: note
permalink: handoff
tags: [project, handoff, meal-prep]
---
# Meal-Prep Handoff

> Entry point for every new session in this project. Read first.

## Current State (as of 2026-06-28)
- [fact] Last 3 commits: agglomerative-clustering theme labels for 초간편 mode, ingredient-similarity-based meal composition, pagination label simplification #recent
- [fact] Phase 2 menu reshape: 9 sides removed, 5 새 덮밥 added, 17 자취요리신 recipes integrated #phase-2
- [fact] Same-menu multi-recipe pagination infrastructure landed (commit `b6ce6c3`) #infrastructure
- [fact] Overnight-oats recipe stabilized (no chia, no almond slice — rancidity fix) #recipe-fix

## In Flight
- [note] Basic Memory documentation/search system being built on top of this project (see superpowers spec/plan dated 2026-06-28) #meta

## Next Session
- [todo] After Basic Memory setup completes, run the 8 verification checks (spec §8.1) and confirm `/clear` round-trip restores context #verify
- [todo] Consider adding `data-artifacts.md` entries as new JSON sources are introduced #data

## Relations
- references [[Overview]]
- references [[Data Artifacts]]
```

- [ ] **Step 4: `data-artifacts.md` 작성**

Write `~/Desktop/meal-prep/knowledge/data-artifacts.md`:
```markdown
---
title: Meal-Prep Data Artifacts
type: note
permalink: data-artifacts
tags: [project, data, meal-prep]
---
# Meal-Prep Data Artifacts

Pointer map for raw data files. Do not paste entire file contents into notes — record paths and roles only.

## JSON Sources
| File | Role |
|---|---|
| `data/ingredients.json` | Ingredient master list (Korean names, categories) |
| `data/recipes_korean.json` | Korean main dishes |
| `data/recipes_global.json` | Western / Asian / Mexican / Mediterranean dishes |
| `data/recipes_highprotein.json` | High-protein recipe set |
| `data/recipes_youtube.json` | Recipes ported from YouTube creators (e.g. 자취요리신) |
| `data/recipes_additional.json` | Misc additions (sides, drinks, snacks) |
| `data/structured_data.json` | Schema.org structured data for SEO/Open Graph |

## Scripts
- `scripts/validate.py` — verifies recipe schema and ingredient references

## Notes
- [fact] All recipe IDs and ingredient names are Korean and serve as identifiers #identifiers
- [risk] Adding new JSON sources without updating `index.html` loader will silently exclude them #risk

## Relations
- maps-for [[Overview]]
```

- [ ] **Step 5: `decisions/0001-baseline.md` 작성 (베이스라인 ADR)**

Write `~/Desktop/meal-prep/knowledge/decisions/0001-baseline.md`:
```markdown
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
```

- [ ] **Step 6: 검증 — 4개 파일 존재 + frontmatter 정상**

Run:
```bash
ls ~/Desktop/meal-prep/knowledge/ ~/Desktop/meal-prep/knowledge/decisions/
head -6 ~/Desktop/meal-prep/knowledge/{overview,handoff,data-artifacts}.md
head -6 ~/Desktop/meal-prep/knowledge/decisions/0001-baseline.md
```
Expected: 4개 파일이 모두 보이고 각 `---`로 시작하는 frontmatter 표시.

- [ ] **Step 7: 커밋 — Task 11에서 함께**

---

## Task 5: Basic Memory 프로젝트 등록

**Files:** (Basic Memory 내부 설정만 — 리포지토리 영향 없음)

- [ ] **Step 1: 사전 상태 확인**

Run:
```bash
basic-memory project list
```
Expected: 빈 목록 또는 기본 `main` 하나(설치 직후 기본값에 따름).

- [ ] **Step 2: 두 프로젝트 등록**

Run:
```bash
basic-memory project add desktop ~/Desktop/knowledge
basic-memory project add meal-prep ~/Desktop/meal-prep/knowledge
```
Expected: 각각 `Added project ...` 류 메시지.

- [ ] **Step 3: 기본 프로젝트 지정**

Run:
```bash
basic-memory project default desktop
```

- [ ] **Step 4: 상태 점검 + 동기화 확인**

Run:
```bash
basic-memory project list
basic-memory status
```
Expected: 두 프로젝트 모두 표시, status 출력에 conflict/error 없음. 처음 등록 직후 file→DB 동기화 자동 수행됨.

- [ ] **Step 5: 색인 빌드 (임베딩 캐시 다운로드 포함)**

Run:
```bash
basic-memory reindex
```
Expected: 첫 실행이면 fastembed 모델(`bge-small-en`) 다운로드 후 인덱싱. 완료까지 1–3분.

**오프라인/다운로드 실패 시**: 네트워크 복구 후 재시도. 임베딩 없이도 엔진은 read/write/keyword-search가 동작하지만, **의미 기반 검색 품질이 떨어진다**. 다음 단계로 강행 가능하나 Task 12/점검 #5(검색)에서 누락 가능성 인지.

- [ ] **Step 6: 검증 — 시드 노트가 색인에 노출되는지**

Run:
```bash
basic-memory tool read-note overview --project meal-prep
```
Expected: meal-prep overview 본문 출력.

---

## Task 6: MCP user 스코프 등록

**Files:** Claude Code 내부 설정 (`claude mcp` 명령으로 관리)

- [ ] **Step 1: 사전 확인**

Run:
```bash
claude mcp list | grep -i basic-memory || echo "NOT_REGISTERED"
```
Expected: `NOT_REGISTERED`.

- [ ] **Step 2: user 스코프 등록**

Run:
```bash
claude mcp add basic-memory -s user -- ~/.local/bin/basic-memory mcp
```
Expected: 등록 성공 메시지.

- [ ] **Step 3: 등록 확인**

Run:
```bash
claude mcp list
```
Expected: `basic-memory` 항목 표시.

- [ ] **Step 4: 새 Claude Code 세션에서 연결 확인 (수동)**

사용자에게 안내: 새 터미널/세션에서 `claude` 진입 후 `/mcp` 또는 도구 목록에 `mcp__basic-memory__*` 확인. (이 단계는 현재 세션 종료가 필요해 자동화 불가)

---

## Task 7: SessionStart 훅 스크립트 작성

**Files:**
- Create: `~/.claude/hooks/basic-memory-session-start.sh`

- [ ] **Step 1: 스모크 테스트 스크립트 작성 (실패 기대)**

먼저 훅을 어떻게 호출할지 정한 뒤(테스트 — 실패 단계) 본체를 만든다. 임시 테스트 파일:

```bash
mkdir -p /tmp/bm-hook-test/{proj-with,proj-without}/knowledge
echo "---
title: T
type: note
permalink: handoff
---
# proj-with handoff" > /tmp/bm-hook-test/proj-with/knowledge/handoff.md

echo "---
title: O
type: note
permalink: overview
---
# proj-with overview" > /tmp/bm-hook-test/proj-with/knowledge/overview.md
```

스모크 테스트 — proj-with에서 호출:
```bash
echo '{"cwd":"/tmp/bm-hook-test/proj-with"}' | bash ~/.claude/hooks/basic-memory-session-start.sh
```
Expected (실패): `bash: ~/.claude/hooks/basic-memory-session-start.sh: No such file or directory`.

- [ ] **Step 2: 훅 본체 작성**

Write `~/.claude/hooks/basic-memory-session-start.sh`:
```bash
#!/bin/zsh
# Basic Memory SessionStart hook (macOS port).
# Routing rule: ${CLAUDE_PROJECT_DIR:-$PWD}/knowledge/handoff.md exists → emit project notes,
# else fall back to ~/Desktop/knowledge/handoff.md + overview.md (central hub).
# Output is injected into the Claude session as additionalContext.
#
# Hook input (stdin JSON): { "cwd": "...", "session_id": "...", "transcript_path": "...", "source": "startup|resume|clear|compact" }

set -e
set -o pipefail

# 5s overall timeout via background watchdog
( sleep 5 && kill -TERM $$ 2>/dev/null ) &
WATCHDOG_PID=$!
trap 'kill $WATCHDOG_PID 2>/dev/null; exit 0' EXIT INT TERM

HUB="$HOME/Desktop/knowledge"
INPUT="$(cat 2>/dev/null || true)"

# Prefer hook-provided cwd, then CLAUDE_PROJECT_DIR env, then $PWD
ROOT=""
if [[ -n "$INPUT" ]] && command -v jq >/dev/null 2>&1; then
  ROOT="$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null || true)"
fi
[[ -z "$ROOT" ]] && ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

PROJ_HANDOFF="$ROOT/knowledge/handoff.md"
PROJ_OVERVIEW="$ROOT/knowledge/overview.md"
HUB_HANDOFF="$HUB/handoff.md"
HUB_OVERVIEW="$HUB/overview.md"

emit() {
  local label="$1"; shift
  printf '<!-- bm: project=%s -->\n' "$label"
  for f in "$@"; do
    if [[ -f "$f" ]]; then
      printf '\n<!-- bm: file=%s -->\n' "$f"
      # Cap output per-file at ~8KB to stay under 16KB total
      head -c 8192 "$f"
      printf '\n'
    fi
  done
}

OUT=""
if [[ -f "$PROJ_HANDOFF" ]]; then
  PROJ_NAME="$(basename "$ROOT")"
  OUT="$(emit "$PROJ_NAME" "$PROJ_HANDOFF" "$PROJ_OVERVIEW")"
elif [[ -f "$HUB_HANDOFF" ]]; then
  OUT="$(emit "desktop" "$HUB_HANDOFF" "$HUB_OVERVIEW")"
fi

# Hard cap 16KB to avoid blowing context
if [[ -n "$OUT" ]]; then
  printf '%s' "$OUT" | head -c 16384
fi

exit 0
```

- [ ] **Step 3: 실행 비트 부여**

Run:
```bash
chmod +x ~/.claude/hooks/basic-memory-session-start.sh
ls -l ~/.claude/hooks/basic-memory-session-start.sh
```
Expected: `-rwxr-xr-x` 권한 표시.

- [ ] **Step 4: 프로젝트 라우팅 케이스 검증**

Run:
```bash
echo '{"cwd":"/tmp/bm-hook-test/proj-with"}' | ~/.claude/hooks/basic-memory-session-start.sh
```
Expected: 첫 줄이 `<!-- bm: project=proj-with -->`, 이후 `# proj-with handoff`와 `# proj-with overview` 둘 다 표시.

- [ ] **Step 5: 중앙 폴백 케이스 검증**

Run:
```bash
echo '{"cwd":"/tmp/bm-hook-test/proj-without"}' | ~/.claude/hooks/basic-memory-session-start.sh
```
Expected: 첫 줄이 `<!-- bm: project=desktop -->`, 이후 중앙 허브 handoff/overview 내용 표시.

- [ ] **Step 6: 둘 다 없음 케이스 (무음 종료)**

Run:
```bash
mkdir -p /tmp/bm-hook-test/empty
echo '{"cwd":"/tmp/bm-hook-test/empty"}' | ~/.claude/hooks/basic-memory-session-start.sh; echo "exit=$?"
```
Expected: 출력 거의 없음, `exit=0`. (중앙 허브에 노트가 있으면 폴백되어 desktop 라벨이 나와야 함 — Task 3 통과 후라면 그게 정상)

- [ ] **Step 7: 정리**

Run:
```bash
rm -rf /tmp/bm-hook-test
```

- [ ] **Step 8: 커밋 — 해당 없음**

`~/.claude/` 는 사용자 글로벌 설정이므로 meal-prep 리포지토리에 들어가지 않음.

---

## Task 8: settings.json에 SessionStart 훅 등록

**Files:**
- Modify: `~/.claude/settings.json` (user 스코프, hooks.SessionStart 배열에 항목 추가)

- [ ] **Step 1: 백업**

Run:
```bash
cp ~/.claude/settings.json ~/.claude/settings.json.bak.$(date +%Y%m%d-%H%M%S)
```

- [ ] **Step 2: jq로 hook 항목 병합**

Run:
```bash
jq '.hooks.SessionStart = ((.hooks.SessionStart // []) + [{"matcher":"","hooks":[{"type":"command","command":"~/.claude/hooks/basic-memory-session-start.sh"}]}])' \
  ~/.claude/settings.json > ~/.claude/settings.json.new \
  && mv ~/.claude/settings.json.new ~/.claude/settings.json
```

- [ ] **Step 3: JSON 유효성 + 등록 확인**

Run:
```bash
jq '.hooks.SessionStart' ~/.claude/settings.json
```
Expected: 1개 이상의 항목, 그 중 하나의 `command`가 `~/.claude/hooks/basic-memory-session-start.sh`.

- [ ] **Step 4: 기존 SessionEnd 훅 보존 확인**

Run:
```bash
jq '.hooks.SessionEnd' ~/.claude/settings.json
```
Expected: `work-log-session-end.sh` 항목이 그대로.

- [ ] **Step 5: 새 Claude Code 세션에서 자동 주입 확인 (수동)**

사용자에게 안내 — meal-prep 폴더에서 새 세션 시작 시 첫 응답에서 `bm: project=meal-prep` 헤더가 인지된 정황(예: handoff 내용을 묻지 않아도 안다)을 확인. (Task 12에서 정식 점검 포함)

---

## Task 9: `/save-memory` 슬래시 명령 작성

**Files:**
- Create: `~/.claude/commands/save-memory.md`

- [ ] **Step 1: commands 디렉토리 생성**

Run:
```bash
mkdir -p ~/.claude/commands
```

- [ ] **Step 2: 명령 본문 작성**

Write `~/.claude/commands/save-memory.md`:
```markdown
---
description: 현재 세션의 결정·결과·다음 작업을 Basic Memory에 기록하고 handoff를 갱신합니다.
---

# /save-memory

당신은 지금 세션 마무리 작업을 합니다. 다음 단계를 **순서대로** 수행하세요. 각 단계는 결과를 확인하고 다음으로 넘어갑니다.

## 인자
사용자가 `/save-memory` 뒤에 자유 텍스트를 붙였으면 그것을 **추가 메모**로 취급해 기록 내용에 포함하세요.

## 단계

### 1. 프로젝트 식별
- `pwd` 또는 `${CLAUDE_PROJECT_DIR:-$PWD}` 로 현재 폴더 확인
- 그 폴더에 `knowledge/handoff.md` 있으면 **프로젝트 메모리**, 없으면 **중앙 허브(`~/Desktop/knowledge`)**
- 어느 쪽인지 사용자에게 한 줄로 알림

### 2. 세션 요약
- 이번 세션의 ① 완료한 일, ② 결정(있다면), ③ 다음 할 일을 각 3–5개 불릿으로 정리
- 영어로 작성. 식별자(파일경로·레시피명·태그)는 그대로 둠 — §스펙 §6.4 규약

### 3. handoff 갱신
- MCP `write-note` (또는 `basic-memory tool write-note`) 로 `handoff` 노트를 덮어쓰기
- 형식: frontmatter 유지, `## Current State` / `## In Flight` / `## Next Session` 섹션 구조 유지
- 갱신 후 새 본문을 사용자에게 보여줌

### 4. 신규 결정은 ADR로 분리
- 위 2번에서 "결정"이 있었다면 `decisions/000N-<slug>.md` 로 분리 작성 (ADR 템플릿 — 스펙 §6.3)
- 번호는 기존 `decisions/` 내 최대 ADR + 1
- handoff에는 `- decided [[ADR 000N <title>]]` 한 줄 링크

### 5. 안전장치 — 동기화 점검 (Q3-D)
- `basic-memory status` 실행
- 결과가 clean 이 아니면(예: pending sync, conflict) → 사용자에게 결과를 그대로 보여주고 `basic-memory reindex` 실행 여부 질문
- clean 이면 한 줄 "synced"만 보고

### 6. 안전장치 — 노트 규약 검증 (Q3-D)
이번 세션에 작성/수정한 모든 노트에 대해 다음을 확인:
- frontmatter 4필드 존재 (`title`, `type`, `permalink`, `tags`)
- 관찰 라인은 `- [category] text [#tag ...]` 형식
- 관계 라인은 `- relation [[Target Note]]` 형식
- 위반이 있으면 사용자에게 위반 항목과 수정안을 제시 (자동 수정 금지 — 사용자 확인 후 진행)

### 7. (옵션) git 커밋 안내
- 현재 폴더에서 `git status` 결과의 `knowledge/` 변경 항목을 사용자에게 보여줌
- 사용자가 커밋 진행을 원하면 메시지 제안: `memory: update handoff` (또는 ADR 추가 시 `memory: add ADR 000N <slug>`)
- 사용자가 명시적으로 요청하지 않은 자동 커밋은 금지

## 출력 형식
다음 순서대로 사용자에게 보고:
1. 프로젝트(메모리 위치) 한 줄
2. 갱신된 handoff 본문 (전체)
3. (있다면) 새 ADR 본문
4. status 결과 (synced 또는 상세)
5. (있다면) 규약 위반 보고
6. (있다면) 제안 커밋 메시지
```

- [ ] **Step 3: 검증**

Run:
```bash
ls ~/.claude/commands/save-memory.md && head -3 ~/.claude/commands/save-memory.md
```
Expected: 파일 존재, frontmatter `description:` 표시.

- [ ] **Step 4: 새 세션에서 명령 인식 확인 (수동)**

사용자에게 안내 — 새 Claude Code 세션에서 `/help` 또는 `/save-memory` 입력 시 인식되는지 확인.

- [ ] **Step 5: 커밋 — 해당 없음** (글로벌 `~/.claude/` 설정)

---

## Task 10: meal-prep `CLAUDE.md` 부트스트랩 작성

**Files:**
- Create: `~/Desktop/meal-prep/CLAUDE.md`

- [ ] **Step 1: 작성**

Write `~/Desktop/meal-prep/CLAUDE.md`:
```markdown
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
```

- [ ] **Step 2: 검증**

Run:
```bash
head -5 ~/Desktop/meal-prep/CLAUDE.md
```
Expected: `# meal-prep — Claude Bootstrap` 시작.

- [ ] **Step 3: 커밋 — Task 11에서 함께**

---

## Task 11: meal-prep 리포지토리에 knowledge + CLAUDE.md 커밋

**Files:**
- Stage: `CLAUDE.md`, `knowledge/`

- [ ] **Step 1: 상태 확인**

Run:
```bash
cd ~/Desktop/meal-prep && git status
```
Expected: untracked — `CLAUDE.md`, `knowledge/`.

- [ ] **Step 2: 색인/캐시 차단 — `.gitignore` 보강**

Run:
```bash
grep -qE '^knowledge/\.bm-cache' ~/Desktop/meal-prep/.gitignore 2>/dev/null || {
  printf '\n# Basic Memory project-local artifacts (if any)\nknowledge/.bm-cache/\nknowledge/*.db\nknowledge/*.sqlite\nknowledge/*.sqlite-*\n' >> ~/Desktop/meal-prep/.gitignore
}
cat ~/Desktop/meal-prep/.gitignore
```
Expected: 위 4줄이 포함됨.

- [ ] **Step 3: 스테이징**

Run:
```bash
cd ~/Desktop/meal-prep
git add CLAUDE.md knowledge/ .gitignore
git status --short
```
Expected: `A` 라인들로 CLAUDE.md, knowledge/*, .gitignore 표시 (이미 추적 중인 .gitignore면 `M`).

- [ ] **Step 4: 커밋**

Run:
```bash
git commit -m "$(cat <<'EOF'
docs: Basic Memory 시드 + CLAUDE.md 부트스트랩

knowledge/ 폴더에 overview / handoff / data-artifacts / 베이스라인 ADR
시드 노트 추가. CLAUDE.md로 세션 부트스트랩 규약(메모리 위치·노트 규약·일상 루틴) 명시.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: 검증**

Run:
```bash
git log --oneline -3
git status
```
Expected: 새 커밋 표시, working tree clean.

---

## Task 12: 8개 수락 점검 + `/clear` 라운드트립

스펙 §8.1의 8개 항목을 순서대로 통과시킨다. 모든 항목 통과 후 DoD 만족.

- [ ] **Step 1 (점검 #1): 엔진 버전**

Run:
```bash
basic-memory --version
```
Expected: `0.22.1` 이상.

- [ ] **Step 2 (점검 #2): 프로젝트 등록**

Run:
```bash
basic-memory project list
```
Expected: `desktop`, `meal-prep` 두 줄 모두 표시.

- [ ] **Step 3 (점검 #3): MCP 연결**

사용자에게 안내 — 새 Claude Code 세션에서 `/mcp` 입력. `basic-memory` 항목이 ✓ Connected 인지 사용자가 확인. (자동 검증 불가)

- [ ] **Step 4 (점검 #4): 시드 무결성**

Run:
```bash
basic-memory tool read-note overview --project meal-prep | head -10
basic-memory tool read-note handoff  --project meal-prep | head -10
basic-memory tool read-note overview --project desktop  | head -5
basic-memory tool read-note handoff  --project desktop  | head -5
```
Expected: 4개 모두 frontmatter + 본문 첫 줄 정상 출력.

- [ ] **Step 5 (점검 #5): 검색**

Run:
```bash
basic-memory tool search-notes "meal-prep" --project meal-prep
```
Expected: `overview` (그리고 `handoff`/`data-artifacts`) permalink가 hit으로 나옴.

- [ ] **Step 6 (점검 #6): 훅 — 프로젝트 라우팅**

Run:
```bash
echo "{\"cwd\":\"$HOME/Desktop/meal-prep\"}" | ~/.claude/hooks/basic-memory-session-start.sh | head -3
```
Expected: 1번째 줄 `<!-- bm: project=meal-prep -->`, 그 다음 meal-prep handoff 시작.

- [ ] **Step 7 (점검 #7): 훅 — 중앙 폴백**

`~/Downloads` 등 사용자 환경에 따라 `knowledge/handoff.md`가 있을 가능성을 배제하기 위해 결정적인 빈 임시 폴더로 검증한다.

Run:
```bash
TMP_EMPTY="$(mktemp -d)"
echo "{\"cwd\":\"$TMP_EMPTY\"}" | ~/.claude/hooks/basic-memory-session-start.sh | head -3
rmdir "$TMP_EMPTY"
```
Expected: 1번째 줄 `<!-- bm: project=desktop -->`, 그 다음 중앙 허브 handoff 시작.

- [ ] **Step 8 (점검 #8): `/save-memory` 왕복 (수동)**

사용자에게 안내 — meal-prep 폴더에서 새 Claude 세션 시작 → 자유롭게 "fake decision 1개 기록해줘" → `/save-memory` 호출 → handoff에 반영되는지 확인. 그 후:
```bash
basic-memory status
basic-memory tool recent-activity --project meal-prep | head -10
```
Expected: status clean, recent-activity에 방금 작성한 노트 표시.

- [ ] **Step 9: `/clear` 라운드트립 (수동)**

사용자에게 안내 — meal-prep 폴더 같은 세션에서 `/clear` 실행 → 직후 SessionStart 훅이 다시 발화해 handoff/overview가 자동 주입되는지 확인 (Claude에게 "메모리에서 본 handoff 첫 문장 알려줘" 식으로 물어 검증).

- [ ] **Step 10: 완료 보고**

8개 점검 + `/clear` 라운드트립 모두 통과 시, 본 작업은 DoD를 만족한 상태. 통과 결과를 정리해 사용자에게 보고하고 종료.

---

## Notes for the executor

- **사용자 확인이 필요한 단계가 있다**: Task 6/Step 4, Task 8/Step 5, Task 9/Step 4, Task 12/Step 3·8·9. 자동화로 처리 불가 — 반드시 사용자에게 명확히 안내하고 결과를 받아 다음으로 진행한다.
- **롤백 가이드**:
  - 훅 등록 되돌리기: `~/.claude/settings.json.bak.*` 백업으로 복원.
  - 프로젝트 등록 취소: `basic-memory project remove <name>`.
  - MCP 등록 취소: `claude mcp remove basic-memory -s user`.
- **검증 우선**: `@superpowers:verification-before-completion` 원칙에 따라, "통과했다"고 보고하기 전에 반드시 명령 결과(stdout)를 직접 확인한다.
- **재현성**: 각 Task의 검증 명령을 그대로 다시 실행해 결과가 동일한지 점검해 완료를 확정한다.
