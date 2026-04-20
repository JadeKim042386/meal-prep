# 2025~2026 최신/최고급 웹 효과 기술 조사 리포트

> 조사일: 2026-04-19
> 목표: 순수 CSS/JS로 구현 가능한 화려한 웹 효과 기술 25가지+

---

## 1. CSS Scroll-Driven Animations (스크롤 기반 애니메이션)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음 (Chrome 115+, Safari 26+, Firefox 110+)
- **적용 가능 영역**: 헤더, 프로그레스바, 카드 리빌, 배경 전환
- **핵심 코드**:
```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

/* 스크롤 프로그레스바 */
.progress-bar {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 4px;
  background: linear-gradient(to right, #ff6b6b, #feca57);
  transform-origin: left;
  animation: grow-progress linear;
  animation-timeline: scroll();
}
@keyframes grow-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```
- **참고 URL**: https://scroll-driven-animations.style/, https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations

---

## 2. CSS View Transitions API (뷰 전환)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음 (Baseline 2025, 모든 주요 브라우저)
- **적용 가능 영역**: 페이지 전환, 모달, 탭 전환, SPA 라우팅
- **핵심 코드**:
```css
/* 전환 대상에 고유 이름 부여 */
.card { view-transition-name: card-hero; }

/* 전환 애니메이션 커스텀 */
::view-transition-old(card-hero) {
  animation: fade-out 0.3s ease-out;
}
::view-transition-new(card-hero) {
  animation: fade-in 0.3s ease-in;
}

@keyframes fade-out { to { opacity: 0; transform: scale(0.9); } }
@keyframes fade-in { from { opacity: 0; transform: scale(1.1); } }
```
```js
// JS로 전환 트리거
document.startViewTransition(() => {
  // DOM 변경 코드
  updateContent();
});
```
- **참고 URL**: https://developer.chrome.com/docs/web-platform/view-transitions

---

## 3. @property 애니메이티드 그라디언트
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음 (Chrome 85+, Firefox 128+, Safari 16.4+)
- **적용 가능 영역**: 배경, 버튼, 카드, 헤더
- **핵심 코드**:
```css
@property --gradient-angle {
  syntax: '<angle>';
  inherits: false;
  initial-value: 0deg;
}

@property --color-1 {
  syntax: '<color>';
  inherits: false;
  initial-value: #ff6b6b;
}

@property --color-2 {
  syntax: '<color>';
  inherits: false;
  initial-value: #feca57;
}

.animated-gradient {
  background: linear-gradient(var(--gradient-angle), var(--color-1), var(--color-2), var(--color-1));
  animation: rotate-gradient 4s linear infinite;
}

@keyframes rotate-gradient {
  to { --gradient-angle: 360deg; }
}
```
- **참고 URL**: https://dev.to/afif/we-can-finally-animate-css-gradient-kdk

---

## 4. 네온 글로우 텍스트 효과
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 헤더 타이틀, 로고, 강조 텍스트
- **핵심 코드**:
```css
.neon-text {
  color: #fff;
  font-family: 'Arial Black', sans-serif;
  text-shadow:
    0 0 7px #fff,
    0 0 10px #fff,
    0 0 21px #fff,
    0 0 42px #0fa,
    0 0 82px #0fa,
    0 0 92px #0fa,
    0 0 102px #0fa,
    0 0 151px #0fa;
  animation: neon-flicker 1.5s infinite alternate;
}

@keyframes neon-flicker {
  0%, 18%, 22%, 25%, 53%, 57%, 100% {
    text-shadow:
      0 0 4px #fff, 0 0 11px #fff, 0 0 19px #fff,
      0 0 40px #0fa, 0 0 80px #0fa, 0 0 90px #0fa,
      0 0 100px #0fa, 0 0 150px #0fa;
  }
  20%, 24%, 55% {
    text-shadow: none;
  }
}

/* 네온 박스 보더 */
.neon-box {
  border: 0.2rem solid #fff;
  border-radius: 2rem;
  padding: 0.4em;
  box-shadow: 0 0 .2rem #fff, 0 0 .2rem #fff,
    0 0 2rem #bc13fe, 0 0 0.8rem #bc13fe,
    0 0 2.8rem #bc13fe, inset 0 0 1.3rem #bc13fe;
}
```
- **참고 URL**: https://css-tricks.com/how-to-create-neon-text-with-css/

---

## 5. Glassmorphism (글래스모피즘 / 프로스트 글래스)
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음 (Chrome 76+, Firefox 103+, Safari 9+)
- **적용 가능 영역**: 카드, 모달, 네비게이션, 오버레이
- **핵심 코드**:
```css
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* 다크모드 글래스 */
.glass-dark {
  background: rgba(17, 25, 40, 0.75);
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.125);
}
```
- **참고 URL**: https://ui.glass/generator/, https://playground.halfaccessible.com/blog/glassmorphism-design-trend-implementation-guide

---

## 6. 커서 트레일 효과 (Cursor Trail)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 전체 페이지 배경, 인터랙티브 섹션
- **핵심 코드**:
```js
const coords = [];
const TRAIL_LENGTH = 20;

document.addEventListener('mousemove', (e) => {
  coords.push({ x: e.clientX, y: e.clientY });
  if (coords.length > TRAIL_LENGTH) coords.shift();

  document.querySelectorAll('.trail-dot').forEach((dot, i) => {
    const coord = coords[coords.length - 1 - i];
    if (coord) {
      dot.style.left = coord.x + 'px';
      dot.style.top = coord.y + 'px';
      dot.style.opacity = 1 - (i / TRAIL_LENGTH);
      dot.style.transform = `scale(${1 - (i / TRAIL_LENGTH)})`;
    }
  });
});

// 초기화: TRAIL_LENGTH 만큼 dot div 생성
for (let i = 0; i < TRAIL_LENGTH; i++) {
  const dot = document.createElement('div');
  dot.className = 'trail-dot';
  document.body.appendChild(dot);
}
```
```css
.trail-dot {
  position: fixed;
  width: 12px; height: 12px;
  background: radial-gradient(circle, #ff6b6b, transparent);
  border-radius: 50%;
  pointer-events: none;
  transition: transform 0.1s, opacity 0.1s;
  z-index: 9999;
}
```
- **참고 URL**: https://github.com/tholman/cursor-effects

---

## 7. 파티클 애니메이션 (Canvas Particles)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 배경, 히어로 섹션, 인터랙티브 영역
- **핵심 코드**:
```js
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];
const PARTICLE_COUNT = 100;

class Particle {
  constructor() {
    this.x = Math.random() * canvas.width;
    this.y = Math.random() * canvas.height;
    this.size = Math.random() * 3 + 1;
    this.speedX = (Math.random() - 0.5) * 0.5;
    this.speedY = (Math.random() - 0.5) * 0.5;
    this.opacity = Math.random() * 0.5 + 0.2;
  }
  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
    if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
    ctx.fill();
  }
}

for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach(p => { p.update(); p.draw(); });
  // 연결선 그리기
  particles.forEach((a, i) => {
    particles.slice(i + 1).forEach(b => {
      const dist = Math.hypot(a.x - b.x, a.y - b.y);
      if (dist < 120) {
        ctx.strokeStyle = `rgba(255,255,255,${0.2 * (1 - dist/120)})`;
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    });
  });
  requestAnimationFrame(animate);
}
animate();
```
- **참고 URL**: https://cruip.com/how-to-create-a-beautiful-particle-animation-with-html-canvas/

---

## 8. 마그네틱 버튼 효과 (Magnetic Button)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 버튼, CTA, 네비게이션 링크
- **핵심 코드**:
```js
document.querySelectorAll('.magnetic-btn').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = 'translate(0, 0)';
  });
});
```
```css
.magnetic-btn {
  padding: 16px 32px;
  border: 2px solid #fff;
  background: transparent;
  color: #fff;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border-radius: 50px;
}
.magnetic-btn:hover {
  background: rgba(255,255,255,0.1);
}
```
- **참고 URL**: https://tympanus.net/codrops/2020/08/05/magnetic-buttons/

---

## 9. 3D 카드 틸트 효과 (3D Tilt Card)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 카드, 이미지 갤러리, 프로필
- **핵심 코드**:
```js
document.querySelectorAll('.tilt-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;
    const rotateX = (y - 0.5) * -20;
    const rotateY = (x - 0.5) * 20;
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1,1,1)';
  });
});
```
```css
.tilt-card {
  transition: transform 0.4s ease;
  transform-style: preserve-3d;
  border-radius: 16px;
  overflow: hidden;
}
.tilt-card .shine {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%),
    rgba(255,255,255,0.2), transparent 60%);
  pointer-events: none;
}
```
- **참고 URL**: https://micku7zu.github.io/vanilla-tilt.js/

---

## 10. 3D 카드 플립 (Card Flip)
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 카드, 레시피 상세, 정보 토글
- **핵심 코드**:
```css
.flip-container {
  perspective: 1000px;
  width: 300px; height: 400px;
}
.flip-card {
  width: 100%; height: 100%;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  cursor: pointer;
}
.flip-container:hover .flip-card {
  transform: rotateY(180deg);
}
.flip-face {
  position: absolute;
  width: 100%; height: 100%;
  backface-visibility: hidden;
  border-radius: 16px;
}
.flip-back {
  transform: rotateY(180deg);
}
```
- **참고 URL**: https://www.w3schools.com/howto/howto_css_flip_card.asp

---

## 11. 텍스트 스크램블 효과 (Text Scramble)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 헤더 타이틀, 로딩 텍스트, 인터랙티브 텍스트
- **핵심 코드**:
```js
class TextScramble {
  constructor(el) {
    this.el = el;
    this.chars = '!<>-_\\/[]{}--=+*^?#________';
    this.frame = 0;
    this.queue = [];
  }
  setText(newText) {
    const oldText = this.el.innerText;
    const length = Math.max(oldText.length, newText.length);
    return new Promise(resolve => {
      this.queue = [];
      for (let i = 0; i < length; i++) {
        const from = oldText[i] || '';
        const to = newText[i] || '';
        const start = Math.floor(Math.random() * 40);
        const end = start + Math.floor(Math.random() * 40);
        this.queue.push({ from, to, start, end });
      }
      this.resolve = resolve;
      this.frame = 0;
      this.update();
    });
  }
  update() {
    let output = '', complete = 0;
    for (let i = 0; i < this.queue.length; i++) {
      let { from, to, start, end, char } = this.queue[i];
      if (this.frame >= end) { complete++; output += to; }
      else if (this.frame >= start) {
        if (!char || Math.random() < 0.28) {
          char = this.chars[Math.floor(Math.random() * this.chars.length)];
          this.queue[i].char = char;
        }
        output += `<span class="scramble-char">${char}</span>`;
      } else { output += from; }
    }
    this.el.innerHTML = output;
    if (complete === this.queue.length) { this.resolve(); }
    else { requestAnimationFrame(() => this.update()); this.frame++; }
  }
}
```
```css
.scramble-char {
  color: #feca57;
  opacity: 0.7;
}
```
- **참고 URL**: https://codepen.io/soulwire/pen/mEMPrK

---

## 12. Gooey 효과 (SVG 필터 메타볼)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 메뉴, 버튼 그룹, 로딩, 장식 요소
- **핵심 코드**:
```html
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="goo">
      <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"
        result="goo"/>
      <feBlend in="SourceGraphic" in2="goo"/>
    </filter>
  </defs>
</svg>
```
```css
.gooey-container {
  filter: url('#goo');
}
.gooey-blob {
  width: 80px; height: 80px;
  background: #ff6b6b;
  border-radius: 50%;
  position: absolute;
  animation: blob-move 3s ease-in-out infinite alternate;
}
@keyframes blob-move {
  0% { transform: translate(0, 0); }
  100% { transform: translate(100px, 50px); }
}
```
- **참고 URL**: https://css-tricks.com/gooey-effect/

---

## 13. Aurora (오로라) 배경 효과
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 히어로 배경, 전체 페이지 배경
- **핵심 코드**:
```css
.aurora-bg {
  position: relative;
  background: #0a0a2e;
  overflow: hidden;
}
.aurora-bg::before,
.aurora-bg::after {
  content: '';
  position: absolute;
  inset: -50%;
  background: conic-gradient(
    from 0deg at 50% 50%,
    transparent, #00ff88, transparent, #0088ff,
    transparent, #8800ff, transparent
  );
  animation: aurora-rotate 10s linear infinite;
  opacity: 0.3;
  filter: blur(80px);
}
.aurora-bg::after {
  animation-duration: 15s;
  animation-direction: reverse;
  opacity: 0.2;
}
@keyframes aurora-rotate {
  to { transform: rotate(360deg); }
}
```
- **참고 URL**: https://dev.to/oobleck/css-aurora-effect-569n, https://github.com/LunarLogic/auroral

---

## 14. 노이즈/그레인 텍스처 오버레이
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 전체 페이지 배경, 카드, 히어로 섹션
- **핵심 코드**:
```css
.grain-overlay::after {
  content: '';
  position: fixed;
  inset: -50%;
  width: 300%; height: 300%;
  opacity: 0.15;
  pointer-events: none;
  z-index: 9999;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  animation: grain 8s steps(10) infinite;
}
@keyframes grain {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-5%, -10%); }
  30% { transform: translate(7%, -25%); }
  50% { transform: translate(-15%, 10%); }
  70% { transform: translate(0%, 15%); }
  90% { transform: translate(-10%, 10%); }
}
```
- **참고 URL**: https://css-tricks.com/grainy-gradients/, https://css-tricks.com/snippets/css/animated-grainy-texture/

---

## 15. 글리치 텍스트 효과 (Glitch Text)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 헤더, 타이틀, 에러 페이지, 크리에이티브 섹션
- **핵심 코드**:
```css
.glitch {
  position: relative;
  font-size: 4rem;
  font-weight: 900;
  color: #fff;
}
.glitch::before, .glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
}
.glitch::before {
  color: #ff00ff;
  animation: glitch-1 2s infinite linear alternate-reverse;
  clip-path: inset(0 0 60% 0);
}
.glitch::after {
  color: #00ffff;
  animation: glitch-2 2s infinite linear alternate-reverse;
  clip-path: inset(40% 0 0 0);
}
@keyframes glitch-1 {
  0% { transform: translate(0); }
  20% { transform: translate(-3px, 3px); }
  40% { transform: translate(3px, -3px); }
  60% { transform: translate(-3px, -3px); }
  80% { transform: translate(3px, 3px); }
  100% { transform: translate(0); }
}
@keyframes glitch-2 {
  0% { transform: translate(0); }
  20% { transform: translate(3px, -3px); }
  40% { transform: translate(-3px, 3px); }
  60% { transform: translate(3px, 3px); }
  80% { transform: translate(-3px, -3px); }
  100% { transform: translate(0); }
}
```
- **참고 URL**: https://freefrontend.com/css-neon-effects/

---

## 16. CSS Mask 리빌 효과 (Mask Reveal / Wipe)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 이미지 리빌, 텍스트 등장, 섹션 전환
- **핵심 코드**:
```css
.mask-reveal {
  -webkit-mask-image: linear-gradient(to right, #000 50%, transparent 50%);
  mask-image: linear-gradient(to right, #000 50%, transparent 50%);
  -webkit-mask-size: 200% 100%;
  mask-size: 200% 100%;
  -webkit-mask-position: 100% 0;
  mask-position: 100% 0;
  animation: mask-wipe 1.5s ease forwards;
}

@keyframes mask-wipe {
  to {
    -webkit-mask-position: 0 0;
    mask-position: 0 0;
  }
}

/* 대각선 리빌 */
.mask-diagonal {
  -webkit-mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
  mask-image: linear-gradient(135deg, #000 50%, transparent 50%);
  -webkit-mask-size: 300% 300%;
  mask-size: 300% 300%;
  -webkit-mask-position: 100% 100%;
  mask-position: 100% 100%;
  animation: diagonal-wipe 2s ease forwards;
}
@keyframes diagonal-wipe {
  to { -webkit-mask-position: 0 0; mask-position: 0 0; }
}
```
- **참고 URL**: https://expensive.toys/blog/fancy-css-reveal-effects, https://www.smashingmagazine.com/2023/09/revealing-images-css-mask-animations/

---

## 17. Intersection Observer 스크롤 리빌 애니메이션
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 카드, 섹션, 이미지, 텍스트 모든 요소
- **핵심 코드**:
```css
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
/* 방향별 변형 */
.reveal-left { transform: translateX(-60px); }
.reveal-right { transform: translateX(60px); }
.reveal-scale { transform: scale(0.8); }
.reveal-left.visible, .reveal-right.visible, .reveal-scale.visible {
  opacity: 1;
  transform: translateX(0) scale(1);
}
```
```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```
- **참고 URL**: https://www.freecodecamp.org/news/scroll-animations-with-javascript-intersection-observer-api/

---

## 18. 컨페티 축하 효과 (Confetti)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 성공 페이지, 완료 모달, 축하 이벤트
- **핵심 코드**:
```js
function launchConfetti() {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:99999';
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const pieces = [];
  const colors = ['#ff6b6b','#feca57','#48dbfb','#ff9ff3','#54a0ff','#5f27cd'];

  for (let i = 0; i < 150; i++) {
    pieces.push({
      x: canvas.width / 2,
      y: canvas.height / 2,
      vx: (Math.random() - 0.5) * 20,
      vy: Math.random() * -18 - 5,
      w: Math.random() * 10 + 5,
      h: Math.random() * 6 + 3,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * 360,
      rotSpeed: (Math.random() - 0.5) * 10,
      gravity: 0.3 + Math.random() * 0.2
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let alive = false;
    pieces.forEach(p => {
      p.vy += p.gravity;
      p.x += p.vx;
      p.y += p.vy;
      p.rotation += p.rotSpeed;
      p.vx *= 0.99;
      if (p.y < canvas.height + 50) alive = true;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation * Math.PI / 180);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
      ctx.restore();
    });
    if (alive) requestAnimationFrame(animate);
    else canvas.remove();
  }
  animate();
}
```
- **참고 URL**: https://github.com/catdad/canvas-confetti

---

## 19. CSS Scroll Snap 풀페이지 섹션
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음 (96%+ 지원)
- **적용 가능 영역**: 풀페이지 레이아웃, 슬라이더, 갤러리
- **핵심 코드**:
```css
.snap-container {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}
.snap-section {
  height: 100vh;
  scroll-snap-align: start;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 수평 스크롤 갤러리 */
.snap-horizontal {
  display: flex;
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
  gap: 1rem;
}
.snap-horizontal > * {
  scroll-snap-align: center;
  flex: 0 0 80%;
}
```
- **참고 URL**: https://prismic.io/blog/css-scroll-effects

---

## 20. mix-blend-mode 텍스트 녹아웃 효과
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 히어로 타이틀, 배경 이미지 위 텍스트
- **핵심 코드**:
```css
/* 텍스트로 배경 이미지를 드러내는 효과 */
.knockout-text {
  position: relative;
  background-image: url('background.jpg');
  background-size: cover;
}
.knockout-text h1 {
  font-size: 8vw;
  font-weight: 900;
  color: #000;
  background: #fff;
  mix-blend-mode: screen;
  /* screen: 흰색은 사라지고 검은 텍스트가 아래 배경을 드러냄 */
}

/* 또는 background-clip 방식 */
.gradient-text {
  background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}
@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```
- **참고 URL**: https://css-tricks.com/css-techniques-and-effects-for-knockout-text/

---

## 21. 모핑 셰이프 (clip-path 애니메이션)
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 배경 장식, 섹션 디바이더, 버튼, 로더
- **핵심 코드**:
```css
.morph-shape {
  width: 300px; height: 300px;
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  animation: morph 8s ease-in-out infinite;
}
@keyframes morph {
  0%, 100% {
    border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  }
  25% {
    border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
  }
  50% {
    border-radius: 50% 60% 30% 60% / 30% 50% 70% 60%;
  }
  75% {
    border-radius: 60% 40% 60% 30% / 70% 40% 50% 60%;
  }
}

/* clip-path 모핑 (포인트 수 동일 필수) */
.clip-morph {
  animation: clip-shape 6s ease-in-out infinite alternate;
}
@keyframes clip-shape {
  0% {
    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
  }
  100% {
    clip-path: polygon(50% 20%, 80% 10%, 100% 60%, 70% 100%, 20% 80%);
  }
}
```
- **참고 URL**: https://blog.pixelfreestudio.com/how-to-implement-css-shape-morphing-animations/

---

## 22. Staggered 카드 등장 애니메이션
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 카드 그리드, 리스트, 메뉴 아이템
- **핵심 코드**:
```css
.stagger-card {
  opacity: 0;
  transform: translateY(30px);
  animation: stagger-in 0.6s ease forwards;
}
/* CSS 변수로 지연 시간 제어 */
.stagger-card:nth-child(1) { animation-delay: 0.1s; }
.stagger-card:nth-child(2) { animation-delay: 0.2s; }
.stagger-card:nth-child(3) { animation-delay: 0.3s; }
.stagger-card:nth-child(4) { animation-delay: 0.4s; }
.stagger-card:nth-child(5) { animation-delay: 0.5s; }
.stagger-card:nth-child(6) { animation-delay: 0.6s; }

@keyframes stagger-in {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 또는 CSS 변수 활용 (인라인 style="--i:0" 등) */
.stagger-dynamic {
  animation-delay: calc(0.1s * var(--i));
}
```
- **참고 URL**: https://css-tricks.com/different-approaches-for-creating-a-staggered-animation/

---

## 23. 패럴랙스 스크롤 효과 (Parallax)
- **난이도**: 쉬움~보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 히어로 섹션, 배경 이미지, 멀티레이어 배경
- **핵심 코드**:
```css
/* 순수 CSS 패럴랙스 */
.parallax-container {
  height: 100vh;
  overflow-y: auto;
  perspective: 1px;
  transform-style: preserve-3d;
}
.parallax-bg {
  position: absolute;
  inset: 0;
  transform: translateZ(-2px) scale(3);
  z-index: -1;
  background: url('bg.jpg') center/cover;
}
.parallax-content {
  transform: translateZ(0);
  position: relative;
  background: #fff;
}

/* 또는 scroll-driven animation 방식 */
.parallax-element {
  animation: parallax-shift linear;
  animation-timeline: scroll();
}
@keyframes parallax-shift {
  from { transform: translateY(-100px); }
  to { transform: translateY(100px); }
}
```
- **참고 URL**: https://css-tricks.com/bringing-back-parallax-with-scroll-driven-css-animations/

---

## 24. Liquid Glass (Apple 스타일) 효과
- **난이도**: 보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 카드, 버튼, 네비게이션, 모달
- **핵심 코드**:
```css
.liquid-glass {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.15) 0%,
    rgba(255, 255, 255, 0.05) 50%,
    rgba(255, 255, 255, 0.15) 100%
  );
  backdrop-filter: blur(30px) saturate(200%) brightness(1.1);
  -webkit-backdrop-filter: blur(30px) saturate(200%) brightness(1.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 24px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    inset 0 -1px 0 rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}
/* 내부 반사광 효과 */
.liquid-glass::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    105deg,
    rgba(255, 255, 255, 0.3) 0%,
    transparent 40%,
    transparent 60%,
    rgba(255, 255, 255, 0.1) 100%
  );
  pointer-events: none;
}
```
- **참고 URL**: https://aethercss.lovable.app/, https://www.zignuts.com/blog/neumorphism-vs-glassmorphism

---

## 25. 타이프라이터 효과 (Typewriter)
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 히어로 텍스트, 소개 문구, 채팅 UI
- **핵심 코드**:
```css
/* 순수 CSS 타이프라이터 (고정 글자수) */
.typewriter {
  overflow: hidden;
  border-right: 3px solid #fff;
  white-space: nowrap;
  font-family: monospace;
  font-size: 1.5rem;
  width: 0;
  animation:
    typing 3s steps(30) forwards,
    blink 0.7s step-end infinite;
}
@keyframes typing {
  to { width: 100%; }
}
@keyframes blink {
  50% { border-color: transparent; }
}
```
```js
/* JS 다중 문장 타이프라이터 */
function typewriter(el, texts, speed = 80, pause = 2000) {
  let textIdx = 0, charIdx = 0, deleting = false;
  function tick() {
    const current = texts[textIdx];
    el.textContent = current.substring(0, charIdx);
    if (!deleting && charIdx < current.length) {
      charIdx++;
      setTimeout(tick, speed);
    } else if (!deleting) {
      setTimeout(() => { deleting = true; tick(); }, pause);
    } else if (charIdx > 0) {
      charIdx--;
      setTimeout(tick, speed / 2);
    } else {
      deleting = false;
      textIdx = (textIdx + 1) % texts.length;
      setTimeout(tick, 500);
    }
  }
  tick();
}
```
- **참고 URL**: https://www.jqueryscript.net/blog/best-typewriter-typing-animation.html

---

## 26. 애니메이티드 메시 그라디언트 배경
- **난이도**: 쉬움~보통
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 전체 페이지 배경, 히어로 섹션
- **핵심 코드**:
```css
.mesh-gradient {
  background:
    radial-gradient(at 40% 20%, #ff6b6b 0px, transparent 50%),
    radial-gradient(at 80% 0%, #feca57 0px, transparent 50%),
    radial-gradient(at 0% 50%, #48dbfb 0px, transparent 50%),
    radial-gradient(at 80% 50%, #ff9ff3 0px, transparent 50%),
    radial-gradient(at 0% 100%, #54a0ff 0px, transparent 50%),
    radial-gradient(at 80% 100%, #5f27cd 0px, transparent 50%);
  background-size: 200% 200%;
  animation: mesh-move 15s ease infinite;
}

@keyframes mesh-move {
  0% { background-position: 0% 0%; }
  25% { background-position: 50% 50%; }
  50% { background-position: 100% 100%; }
  75% { background-position: 50% 0%; }
  100% { background-position: 0% 0%; }
}
```
- **참고 URL**: https://csshero.org/mesher/, https://www.mshr.app/

---

## 27. 펄싱 글로우 호버 버튼
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 버튼, CTA, 링크
- **핵심 코드**:
```css
.glow-btn {
  padding: 14px 40px;
  border: none;
  border-radius: 50px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 1.1rem;
  cursor: pointer;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}
.glow-btn::before {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 54px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  z-index: -1;
  filter: blur(15px);
  opacity: 0;
  transition: opacity 0.3s ease;
}
.glow-btn:hover::before {
  opacity: 0.7;
}
.glow-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
}
/* 펄싱 효과 */
.glow-btn.pulsing::before {
  opacity: 0.5;
  animation: pulse-glow 2s ease-in-out infinite;
}
@keyframes pulse-glow {
  0%, 100% { filter: blur(15px); opacity: 0.4; }
  50% { filter: blur(25px); opacity: 0.7; }
}
```

---

## 28. Smooth Reveal 번호/카운터 애니메이션
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 통계 섹션, 대시보드, 성과 표시
- **핵심 코드**:
```js
function animateCounter(el, target, duration = 2000) {
  const start = 0;
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // easeOutExpo
    const ease = 1 - Math.pow(2, -10 * progress);
    el.textContent = Math.floor(start + (target - start) * ease);
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// Intersection Observer와 결합
const counterObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const target = parseInt(entry.target.dataset.target);
      animateCounter(entry.target, target);
      counterObserver.unobserve(entry.target);
    }
  });
});
document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));
```

---

## 29. CSS 물결/리플 클릭 효과 (Material Ripple)
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 버튼, 카드, 클릭 가능 요소
- **핵심 코드**:
```js
document.querySelectorAll('.ripple-btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    ripple.style.left = (e.clientX - rect.left) + 'px';
    ripple.style.top = (e.clientY - rect.top) + 'px';
    this.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove());
  });
});
```
```css
.ripple-btn {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.ripple {
  position: absolute;
  width: 10px; height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transform: translate(-50%, -50%) scale(0);
  animation: ripple-expand 0.6s ease-out;
  pointer-events: none;
}
@keyframes ripple-expand {
  to {
    transform: translate(-50%, -50%) scale(40);
    opacity: 0;
  }
}
```

---

## 30. 동적 텍스트 그라디언트 + 빛 반짝임 (Shimmer)
- **난이도**: 쉬움
- **외부 라이브러리 필요**: 아니오
- **브라우저 호환**: 좋음
- **적용 가능 영역**: 로딩 스켈레톤, 타이틀, 강조 텍스트
- **핵심 코드**:
```css
/* 텍스트 위 빛줄기 이동 효과 */
.shimmer-text {
  background: linear-gradient(
    120deg,
    #ff6b6b 0%, #feca57 25%,
    #ffffff 50%,
    #48dbfb 75%, #ff9ff3 100%
  );
  background-size: 200% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 3s ease-in-out infinite;
}
@keyframes shimmer {
  0% { background-position: 200% center; }
  100% { background-position: -200% center; }
}

/* 스켈레톤 로딩 shimmer */
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 8px;
}
@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

# 효과별 추천 적용 가이드

| 영역 | 추천 효과 |
|------|----------|
| **히어로 배경** | Aurora(#13), Mesh Gradient(#26), Particles(#7), @property Gradient(#3) |
| **카드** | Glassmorphism(#5), 3D Tilt(#9), Card Flip(#10), Liquid Glass(#24) |
| **텍스트** | Neon Glow(#4), Glitch(#15), Shimmer(#30), Knockout(#20), Scramble(#11) |
| **버튼** | Magnetic(#8), Ripple(#29), Glow Hover(#27) |
| **스크롤** | Scroll-Driven(#1), Parallax(#23), IO Reveal(#17), Scroll Snap(#19) |
| **전체 분위기** | Grain Overlay(#14), Cursor Trail(#6), Confetti(#18), Gooey(#12) |
| **페이지 전환** | View Transitions(#2), Mask Reveal(#16) |
| **리스트/그리드** | Staggered(#22), Counter(#28) |
| **장식 요소** | Morph Shape(#21), Gooey Blob(#12) |
