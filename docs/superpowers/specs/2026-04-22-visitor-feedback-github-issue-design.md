# Visitor Feedback → GitHub Issue

## Overview

방문자가 GitHub 계정 없이 피드백을 제출하면 GitHub Issue로 자동 생성되는 기능.

## Architecture

```
[Browser] ── POST {body, turnstile_token} ──▶ [Supabase Edge Function]
                                                  │
                                          1. Turnstile 서버 검증
                                          2. GitHub API로 Issue 생성
                                                  │
                                                  ▼
                                          [GitHub Issue 생성]
```

## Components

### 1. Frontend (index.html)

- **플로팅 버튼**: 우하단 고정, 클릭 시 모달 오픈
- **모달 폼**: textarea(내용) + Cloudflare Turnstile 위젯 + 제출 버튼
- **상태 표시**: 제출 중 로딩, 성공/실패 메시지
- **Turnstile script**: `https://challenges.cloudflare.com/turnstile/v0/api.js` 로드

### 2. Supabase Edge Function (`create-issue`)

- **경로**: `POST /functions/v1/create-issue`
- **입력**: `{ body: string, turnstile_token: string }`
- **처리 흐름**:
  1. `body` 빈 값 검증 (최대 2000자)
  2. Turnstile 토큰 서버 사이드 검증 (`https://challenges.cloudflare.com/turnstile/v0/siteverify`)
  3. GitHub API `POST /repos/JadeKim042386/meal-prep/issues` 호출
- **환경 변수**: `GITHUB_TOKEN`, `TURNSTILE_SECRET_KEY`
- **CORS**: `https://jadekim042386.github.io` 허용

### 3. GitHub Issue 형식

```
제목: [피드백] 방문자 피드백 (YYYY-MM-DD)
본문: {사용자 입력 내용}
라벨: feedback
```

## External Setup (수동)

| 서비스 | 필요한 것 | 비고 |
|--------|----------|------|
| Cloudflare Turnstile | Site Key + Secret Key | dash.cloudflare.com에서 발급 |
| GitHub | Personal Access Token | repo scope, 이슈 생성 권한 |
| Supabase | 프로젝트 + Edge Function 배포 | 환경 변수 설정 필요 |

## Error Handling

- Turnstile 검증 실패 → 403 + "인증에 실패했습니다"
- GitHub API 실패 → 500 + "피드백 전송에 실패했습니다"
- 빈 내용 → 400 + "내용을 입력해주세요"
- 2000자 초과 → 400 + "2000자 이내로 입력해주세요"
