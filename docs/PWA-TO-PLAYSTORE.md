# PWABuilder로 Play Store .aab 만들기

## 0. 사전 확인 (지금 단계)

✅ **완료된 항목**
- `manifest.json` (id, name, icons, shortcuts 포함)
- `sw.js` 서비스 워커
- `icon.svg`, `icon-maskable.svg`
- HTTPS (GitHub Pages 자동)

이 상태에서 PWABuilder가 자동으로 빠진 PNG 아이콘을 생성해 줍니다.

---

## 1. PWABuilder 점수 확인

1. https://www.pwabuilder.com/ 접속
2. 사이트 URL 입력: `https://jadekim042386.github.io/meal-prep/`
3. **Start** 클릭 → 분석 시작 (10~30초)
4. 결과 화면에서 점수 확인. 최소 80점 이상이면 Android 패키지 가능
5. 점수가 낮으면 화면에서 **Manifest / Service Worker / Security** 탭별로 빨간 경고 항목 확인 후 보완

---

## 2. Android 패키지 생성

1. 결과 화면 우상단의 **Package For Stores** 클릭
2. **Android** 카드 → **Generate Package**
3. 폼 입력 (대부분 자동 채워짐):

| 필드 | 값 |
|---|---|
| Package ID | `io.github.jadekim042386.mealprep` |
| App name | `밀프랩 플래너(Meal-Prep Planner)` |
| Launcher name | `밀프랩` |
| App version | `1.0.0` |
| App version code | `1` |
| Display mode | `standalone` |
| Status bar color | `#2c3e50` |
| Splash color | `#fdf6e3` |
| Icon URL | (자동) |
| Maskable icon URL | (자동) |
| Signing key | **Generate new** 선택 (PWABuilder가 만들어 줌) |
| **Include source code** | ☑ 체크 (Bubblewrap 프로젝트 다운로드용) |

4. **Download** 클릭 → ZIP 파일 받기

---

## 3. ZIP 내용 확인

압축 해제하면 다음이 들어 있습니다:

```
mealprep-pwa-android.zip
├── app-release-bundle.aab        ← Play Store 업로드용
├── app-release-signed.apk        ← 직접 설치 테스트용
├── signing.keystore              ← ★ 절대 분실 금지 (앱 업데이트에 필수)
├── signing-key-info.txt          ← keystore 비밀번호 + SHA-256 fingerprint
├── assetlinks.json               ← Digital Asset Links 파일
└── next-steps.html               ← PWABuilder 가이드
```

**🔐 중요**:
- `signing.keystore`와 `signing-key-info.txt`를 안전한 곳(예: 1Password, Google Drive)에 백업
- 분실 시 동일 앱으로 업데이트 불가능 (새 패키지 ID로 재출시해야 함)

---

## 4. Digital Asset Links 호스팅

`assetlinks.json`은 **루트 도메인**에 배치해야 TWA가 URL 바 없이 풀스크린으로 동작합니다.

**현재 상황**: 사이트가 `jadekim042386.github.io/meal-prep/` 서브 경로이므로, asset links는 `https://jadekim042386.github.io/.well-known/assetlinks.json` (루트)에 배치 필요.

### 옵션 A — 메인 GitHub Pages 저장소 사용 (무료, 권장)
1. GitHub에서 `jadekim042386.github.io` 라는 이름의 저장소 생성 (이미 있으면 그대로 사용)
2. 그 저장소에 `.well-known/assetlinks.json` 파일 추가
3. PWABuilder가 준 `assetlinks.json` 내용 그대로 복사
4. 커밋·푸시 → 잠시 후 `https://jadekim042386.github.io/.well-known/assetlinks.json` 에서 접근 가능
5. 검증: https://developers.google.com/digital-asset-links/tools/generator

### 옵션 B — 커스텀 도메인 (월 약 $1~)
1. 도메인 구입 (가비아·후이즈·Cloudflare 등)
2. GitHub Pages에 커스텀 도메인 연결 (`mealprep-guide.com` 같은 식)
3. 해당 도메인 루트에 `.well-known/assetlinks.json` 배치
4. 보너스: 네이버 서치 어드바이저 등록 가능 → 한국 검색 노출 큼

### 옵션 C — assetlinks 생략
- TWA 자체는 동작하지만 화면 상단에 URL 바가 표시됨 (덜 "앱"같음)
- Play Store 출시는 가능

---

## 5. Play Console 등록 및 배포

1. https://play.google.com/console 접속 → 계정 생성 ($25 1회 등록비)
2. **앱 만들기** → 이름·언어·타입(앱) 설정
3. **앱 콘텐츠** 섹션 모두 작성:
   - 개인정보처리방침 URL (필수, 간단한 페이지 만들어 사이트에 추가)
   - 광고 포함 여부, 콘텐츠 등급, 대상 연령
   - 데이터 안전 양식 (수집 데이터: 피드백 모달의 텍스트만)
4. **그래픽 자료** 업로드:
   - 앱 아이콘 512×512 (icon.svg에서 변환)
   - 그래픽 (1024×500) — Canva 등으로 간단히
   - 폰 스크린샷 2~8장
5. **프로덕션 트랙** → `app-release-bundle.aab` 업로드
6. 출시 검토 신청 (보통 1~3일 소요)

---

## 6. 직접 설치 테스트 (Play Store 등록 전)

`.apk` 파일로 본인 휴대폰에서 미리 테스트:
1. 휴대폰을 PC에 연결 (USB 디버깅 켜기)
2. `adb install app-release-signed.apk`
3. 또는 `.apk`를 휴대폰에 보내 직접 실행 (출처 불명 앱 허용 필요)

---

## 7. 다음 단계 (Phase 3 — 선택)

네이티브 기능(푸시 알림, 카메라, 백그라운드 동기화 등)이 필요하면 Capacitor로 재포장 가능. 현재 식단/장보기 앱 수준에서는 TWA로 충분합니다.

---

## 트러블슈팅

| 증상 | 원인 / 해결 |
|---|---|
| 앱 실행 시 URL 바가 보임 | assetlinks.json이 루트에 없거나 SHA-256 불일치 — 검증 도구로 확인 |
| 아이콘이 흰색 사각형 | maskable 아이콘 영역 부족 — `icon-maskable.svg`의 안전 영역(중앙 80%) 안에 있는지 확인 |
| 오프라인에서 빈 화면 | 서비스 워커 등록 실패 — Chrome DevTools → Application → Service Workers 확인 |
| Play Console 거부 (정책) | 개인정보처리방침 누락이 가장 흔함 |
