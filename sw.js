/* MyHome CarCare service worker — offline shell for GitHub Pages */
const CACHE = 'carcare-d2fe929e22';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon.svg',
  './assets/fa-subset.css',
  './assets/webfonts/fa-solid-900.woff2',
  './assets/webfonts/fa-regular-400.woff2',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-192-maskable.png',
  './icons/icon-512.png',
  './icons/icon-512-maskable.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  event.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req)
        .then((res) => {
          if (res && res.ok && new URL(req.url).origin === self.location.origin) {
            const copy = res.clone();
            caches.open(CACHE).then((cache) => cache.put(req, copy));
          }
          return res;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
