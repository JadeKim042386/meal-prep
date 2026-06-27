---
title: Basic Memory 기반 검색·문서화 시스템 (macOS 포팅) 디자인
date: 2026-06-28
status: approved-for-planning
author: joo
related:
  - Confluence: https://metacle.atlassian.net/wiki/spaces/~712020022412fbe83e45adbec20302509a4667/pages/1195048985/Basic+Memory
---

# Basic Memory 기반 검색·문서화 시스템 (macOS 포팅) 디자인

## 1. 배경 & 목표

### 1.1 배경
사용자(joo)는 Windows 환경에서 Basic Memory(basicmachines-co/basic-memory, v0.22.1) 기반의 파일형 지식메모리 시스템을 운영 중이다. 핵심 아이디어는 다음과 같다.

> 마크다운(저장) + SQLite·벡터(색인) + Basic Memory(엔진) + MCP(연결) + 훅·명령(자동화) → 세션이 죽어도 살아남는 구조화 메모리.

Windows에는 3개 프로젝트(`desktop`(중앙 허브), `fgip-pkg1`, `cable_project`)와 다음 자동화가 구성돼 있다.

- **SessionStart 훅** — 세션 시작 시 handoff/overview 자동 주입(프로젝트 라우팅 포함)
- **`/save-memory` 슬래시 명령** — 작업 기록·handoff 갱신·옵션 git 커밋
- **프로젝트별 `CLAUDE.md` 부트스트랩**

### 1.2 목표
macOS(`darwin`, zsh, miniconda 환경) 환경에 **동일한 6계층 시스템**을 동일한 운영 규약으로 재현한다. 첫 프로젝트는 `meal-prep`이며, 동시에 중앙 허브 `desktop`도 같이 셋업한다.

### 1.3 비목표 (YAGNI)
- Windows 기존 노트의 콘텐츠 마이그레이션 (대상 머신·프로젝트가 다름)
- 클라우드 동기화 / 다중 머신 페어링
- Obsidian 플러그인·테마 셋업 (선택사항)
- 새 검색 UI를 meal-prep 웹앱에 추가 (이 디자인의 범위 밖)

## 2. 결정 사항 요약

| 항목 | 결정 |
|---|---|
| 프로젝트 구성 | 하이브리드 — 중앙 허브 `desktop` + 프로젝트 `meal-prep` |
| 자동화 | 풀 패키지 — SessionStart 훅 + `/save-memory` + 프로젝트 `CLAUDE.md` + Q3-D 안전장치(`basic-memory status` 자동 점검, 노트 규약 검증) |
| 초기 시드 | 풀 시드 — meal-prep 현재 상태 반영(`overview`/`handoff`/`data-artifacts`/샘플 ADR), 중앙 허브는 빈 골격(`overview`/`handoff`) |
| 노트 작성 언어 | Windows 규칙 그대로 — 본문 영어, 식별자·경로·태그는 한국어 그대로, 대화는 한국어 |
| SessionStart 훅 구현 | zsh 셸 스크립트 (PowerShell 버전과 1:1, MCP 비의존) |

## 3. 아키텍처

### 3.1 6계층 매핑 (Windows ↔ macOS)

| 계층 | 기술 | macOS 위치 |
|---|---|---|
| 저장 | Markdown (knowledge/\*.md) | `~/Desktop/knowledge/`, `~/Desktop/meal-prep/knowledge/` |
| 색인 | SQLite memory.db + fastembed(bge-small-en) | basic-memory 기본 위치(`~/.basic-memory/` 등) |
| 엔진 | Basic Memory 0.22.1 (Python) | `~/.local/bin/basic-memory` (uv tool install 산출물) |
| 연결 | MCP (user 스코프 1개) | `claude mcp add basic-memory -s user -- ~/.local/bin/basic-memory mcp` |
| 자동화 | SessionStart 훅 / `/save-memory` / `CLAUDE.md` | `~/.claude/hooks/`, `~/.claude/commands/`, 프로젝트 루트 |
| 구성 | desktop(중앙) + meal-prep | basic-memory project add 로 등록 |

### 3.2 디렉토리 레이아웃

```
~/.local/bin/basic-memory                  ← uv tool install 산출물
~/.claude/
├── settings.json                          ← SessionStart 훅 등록 (user 스코프)
├── hooks/
│   └── basic-memory-session-start.sh      ← 신규
└── commands/
    └── save-memory.md                     ← 신규
~/Desktop/knowledge/                       ← 중앙 허브 프로젝트 `desktop`
├── overview.md, handoff.md                ← 빈 골격(시드)
├── decisions/, analysis/                  ← 빈 폴더
└── .git/                                  ← 신규 독립 리포지토리
~/Desktop/meal-prep/
├── CLAUDE.md                              ← 신규 부트스트랩
└── knowledge/                             ← 프로젝트 `meal-prep`
    ├── overview.md                        ← 시드: 98 레시피 / 4 모드 / 기술 스택
    ├── handoff.md                         ← 시드: 최근 커밋 흐름 + 다음 작업
    ├── data-artifacts.md                  ← 시드: data/*.json 지도
    └── decisions/0001-baseline.md         ← 시드: 첫 ADR
```

### 3.3 라우팅 규칙

SessionStart 훅은 `pwd`(또는 `CLAUDE_PROJECT_DIR`) 기준으로:

1. 현재 폴더에 `./knowledge/handoff.md` **존재 시** → 그 파일 + `./knowledge/overview.md`만 출력 (중앙 허브는 건너뜀)
2. **부재 시** → 중앙 허브 `~/Desktop/knowledge/{handoff,overview}.md` 출력
3. 둘 다 없으면 → 무음 종료 (exit 0)

이로써 meal-prep 폴더에선 meal-prep 노트만, 다른 폴더에선 중앙 허브 노트만 주입돼 **중복 주입이 방지**된다.

## 4. 컴포넌트

각 컴포넌트는 한 가지 책임을 가지며 인터페이스로 분리된다.

### 4.1 `basic-memory` 엔진 (외부 의존)

- **버전**: 0.22.1+
- **설치**: `uv tool install basic-memory`
- **인터페이스 (MCP 도구)**: `read-note`, `search-notes`, `write-note`, `build-context`, `recent-activity`
- **CLI**: `basic-memory project list|add|info|default`, `basic-memory status|reindex|doctor`
- **검증**: `basic-memory --version`, `basic-memory project list`

### 4.2 `~/.claude/hooks/basic-memory-session-start.sh` (신규)

- **트리거**: SessionStart (`startup`, `resume`, `/clear`)
- **입력**: 환경변수 `CLAUDE_PROJECT_DIR` (없으면 `pwd`)
- **출력**: stdout으로 마크다운 컨텍스트 (additionalContext로 자동 주입)
- **로직**:
  1. `$CLAUDE_PROJECT_DIR/knowledge/handoff.md` 존재 시 → 그 파일과 `overview.md` 출력 후 종료
  2. 그렇지 않으면 → `~/Desktop/knowledge/handoff.md`/`overview.md` 출력
  3. 둘 다 없으면 → 무음 종료
- **출력 헤더**: `<!-- bm: project=<name> -->` (디버그용)
- **안전장치**: 5초 타임아웃, 출력 16KB 캡, 어떤 오류도 exit 0 으로 마무리 (세션 자체를 막지 않음)

### 4.3 `~/.claude/commands/save-memory.md` (신규)

- **호출**: 대화에서 `/save-memory [선택 메모]`
- **동작 (Claude가 단계별로 수행)**:
  1. `pwd`로 현재 프로젝트 식별
  2. 이번 세션의 한 일·결정·다음 작업 요약
  3. MCP `write-note` 호출로 `handoff.md` 갱신, 신규 결정은 `decisions/000N-*.md`로 추가
  4. **(Q3-D 안전장치-1)** `basic-memory status` 실행 → clean 아니면 `reindex` 제안
  5. **(Q3-D 안전장치-2)** 작성된 노트의 frontmatter / `- [category]` 관찰 / `- relation [[...]]` 형식이 §6.2 규약과 일치하는지 검증, 위반 시 사용자에게 수정 제안
  6. (옵션) git commit 안내

### 4.4 `meal-prep/CLAUDE.md` (신규)

- **내용 4줄**:
  1. 이 프로젝트는 `knowledge/` 메모리를 보유함 (Basic Memory)
  2. 세션 시작 시 `knowledge/handoff.md`를 먼저 확인하라
  3. 노트 본문은 영어, 식별자(레시피명/재료명)/경로/태그는 한국어 그대로
  4. 일상 루틴 — 기록은 "메모리에 기록해줘", 종료는 `/save-memory`

### 4.5 저장소 (`~/Desktop/knowledge/`, `~/Desktop/meal-prep/knowledge/`)

- **공통 노트**: `overview.md`, `handoff.md`, `data-artifacts.md`(필요 시), `decisions/`
- **시드 정책**:
  - 중앙 허브: `overview.md`(빈 골격) + `handoff.md`(빈 골격)
  - meal-prep: 4개 노트 모두 현재 프로젝트 상태 반영 (98 레시피, 4 모드, data/\*.json 지도, 베이스라인 ADR)
- **git**:
  - 중앙 허브: 신규 독립 리포지토리(`git init`)
  - meal-prep: 기존 리포지토리에 `knowledge/` 추가 후 커밋

## 5. 데이터 흐름

### 5.1 시나리오 A — 세션 시작 (자동 로드)

```
Claude Code 시작 / /clear / resume
   → SessionStart 훅 발화 (settings.json)
   → basic-memory-session-start.sh 실행
   → pwd 기반 라우팅으로 handoff/overview를 stdout으로 출력
   → 출력이 additionalContext로 세션에 주입
   → Claude는 첫 메시지 전에 이미 메모리 인지
```

**색인·MCP 비의존** — `cat`만으로 동작해 가장 견고. handoff/overview 두 노트만 결정적으로 주입한다.

### 5.2 시나리오 B — 작업 중 기록

```
사용자: "메모리에 기록해줘" 또는 /save-memory
   → Claude → MCP write-note (title, folder, content)
   → 엔진: knowledge/*.md 작성 → SQLite 색인 갱신 → fastembed 벡터 추가
   → (Q3-D) Claude → basic-memory status (동기화 OK 확인)
   → (Q3-D) Claude → 노트 규약 검증
   → 사용자에게 결과 보고 + 옵션 git commit 안내
```

### 5.3 시나리오 C — 조회·검색

```
사용자: "C 관련 메모리 찾아줘"
   → Claude → MCP search-notes "C ..."
   → 엔진: SQLite 키워드 + fastembed 의미 검색 → permalinks 반환
   → Claude → MCP read-note <permalink>  (필요한 노트만)
   → Claude가 결과 종합해 응답
```

**진실의 원천(파일) vs 캐시(색인)**: 검색으로 permalink를 얻고 실제 본문은 파일에서 읽는다. 색인이 망가져도 `basic-memory reindex`로 복구 가능.

## 6. 데이터 모델 / 노트 규약

### 6.1 frontmatter (모든 노트 공통)
```yaml
---
title: "<제목>"
type: note
permalink: <kebab-case-slug>
tags: [<tag1>, <tag2>]
---
```

### 6.2 관찰·관계 문법

| 요소 | 형식 | 예 |
|---|---|---|
| 관찰 | `- [category] text #tag` | `- [fact] Project ships 98 recipes #recipes` |
| 관계 | `- relation [[Target Note]]` | `- affects [[Data Artifacts]]` |

**범주(category) 예시**: `fact`, `decision`, `todo`, `risk`, `note`, `metric`.

### 6.3 ADR 템플릿 (`decisions/000N-topic.md`)
```markdown
---
title: ADR 000N Title
type: note
permalink: adr-000N-topic
tags: [adr, decision]
---
# ADR 000N: Title
- Date: YYYY-MM-DD
- Status: Accepted | Proposed | Superseded
## Context
## Decision
## Consequences
## Relations
- affects [[<Other Note>]]
```

### 6.4 언어 규약
- 노트 **본문 서술**: 영어
- **식별자·경로·태그값**(레시피명, 재료명, 파일경로 등): 한국어 그대로
- **대화**: 한국어 유지

## 7. 에러 처리

| 실패 지점 | 증상 | 처리 |
|---|---|---|
| basic-memory 미설치 | MCP 도구 호출 시 "tool not found" | `uv tool install basic-memory` 안내 (CLAUDE.md에 명시) |
| MCP 서버 미등록 | `/mcp`에 안 보임 | `claude mcp add basic-memory -s user -- ~/.local/bin/basic-memory mcp` 재실행 |
| 훅 — 시드 파일 없음 | (시드 전) handoff/overview 미존재 | 훅이 무음 종료(exit 0). 세션은 정상 시작 |
| 훅 — 권한 오류 | 실행 비트 미부여 | `chmod +x` 안내 + settings.json 절대경로 확인 |
| 동기화 미스매치 | 수동 편집 후 색인 안 됨 | `/save-memory`의 status 점검이 자동 감지 → `reindex` 제안 |
| 규약 위반 노트 | frontmatter 누락 / `[category]` 누락 | `/save-memory`가 작성 직후 검증 → 사용자에게 수정 제안 |
| 대용량 폴더 잘못 등록 | reindex 멈춤 | 프로젝트 경로는 항상 `knowledge/` 폴더만 (코드 전체 등록 금지) |
| 검색 결과 0건 | 키워드 불일치 | `recent-activity`로 폴백 + 사용자에게 다른 표현 제안 |
| Git 미초기화(중앙 허브) | `git commit` 실패 | `/save-memory`가 감지 시 `git init` 1회 안내 |

## 8. 테스트 & 완료 기준

### 8.1 8개 수동/자동 점검 항목
1. **엔진**: `basic-memory --version` → 0.22.1+ 출력
2. **프로젝트 등록**: `basic-memory project list` → `desktop`, `meal-prep` 둘 다 표시
3. **MCP 연결**: 새 세션에서 `/mcp` → `basic-memory` ✓ Connected
4. **시드 무결성**: `read-note overview`, `read-note handoff` 정상 출력
5. **검색**: `search-notes "meal-prep"` → meal-prep overview hit
6. **훅 — 프로젝트 라우팅**: meal-prep 폴더에서 새 세션 시작 → `<!-- bm: project=meal-prep -->` 헤더와 handoff/overview 주입 확인
7. **훅 — 중앙 폴백**: `~/Downloads` 등에서 새 세션 → desktop 노트 주입 확인
8. **`/save-memory` 왕복**: 가짜 결정 1개 기록 → handoff에 반영 → `basic-memory status` clean → `recent-activity` 노출

### 8.2 Definition of Done
- 위 8개 점검 항목 전부 통과
- meal-prep `CLAUDE.md`가 새 세션 부트스트랩으로 동작 (수동 `cat` 없이도 Claude가 메모리를 인지)
- 시드 노트가 git에 커밋
  - 중앙 허브: 신규 리포지토리에 초기 커밋
  - meal-prep: 기존 리포지토리에 추가 커밋
- `/clear` 1회 사이클 후 컨텍스트가 자동 복원되는 것을 사람이 직접 확인

## 9. 핵심 설계 결정 (요약)

| 결정 | 이유 |
|---|---|
| 저장은 순수 Markdown | 사람이 읽고·편집·git 추적 가능, 도구 비종속 |
| 임베딩은 로컬 fastembed | 외부 API/비용/유출 없음, 오프라인 동작 |
| MCP는 user 스코프 1개 | 설치·연결 1회로 전 프로젝트 공용 |
| 하이브리드(중앙+분리) | 일상은 중앙 desktop, 큰 프로젝트는 격리 — 검색 혼선 방지 |
| 자동 로드는 SessionStart 훅 | 명령 없이 매 세션·/clear마다 결정적 주입 |
| 훅은 zsh + `cat` | MCP 비의존, Windows PowerShell 버전과 1:1, 디버깅 쉬움 |
| 프로젝트는 `knowledge/` 폴더만 | 코드 전체 지정 시 수만 파일 스캔으로 실패 (Windows 교훈) |
| 핸드오프 갱신은 `/save-memory` | 완료/결정/다음할일을 한 번에 외부화 → /clear 안전 |
| Q3-D 안전장치 | `basic-memory status` 자동 점검 + 노트 규약 검증으로 사일런트 손상 방지 |

## 10. 다음 단계
- 본 디자인을 기반으로 `writing-plans` 스킬로 구현 계획서 작성
- 구현 계획은 (1) 엔진 설치 & 프로젝트 등록, (2) MCP 연결, (3) 훅·슬래시 명령·CLAUDE.md, (4) 시드 노트 작성, (5) 8개 점검 항목 실행 — 다섯 단계로 나누는 것을 기본 가이드라인으로 한다.
