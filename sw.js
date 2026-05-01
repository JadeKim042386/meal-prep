// Service Worker for 밀프랩 가이드 PWA
const CACHE_VERSION = 'mealprep-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './icon-maskable.svg',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-192.png',
  './icon-maskable-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET') return;
  // Network-first for HTML so updates land fast; cache fallback for offline
  if (event.request.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('.html')) {
    event.respondWith(
      fetch(event.request)
        .then(resp => {
          const respClone = resp.clone();
          caches.open(CACHE_VERSION).then(c => c.put(event.request, respClone));
          return resp;
        })
        .catch(() => caches.match(event.request).then(r => r || caches.match('./index.html')))
    );
    return;
  }
  // Cache-first for static assets
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(resp => {
      if (resp && resp.status === 200 && resp.type === 'basic') {
        const respClone = resp.clone();
        caches.open(CACHE_VERSION).then(c => c.put(event.request, respClone));
      }
      return resp;
    }).catch(() => cached))
  );
});
