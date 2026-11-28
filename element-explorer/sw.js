// Offline support: the page is network-first, everything else cache-first.
const CORE = 'elx-core-v5';
const FILES = ['./', 'index.html', 'vendor/three.min.js', 'vendor/peerjs.min.js', 'manifest.webmanifest', 'icons/icon.svg', 'icons/icon-192.png', 'icons/icon-512.png', 'fonts/ys-text-regular.woff2', 'fonts/ys-text-bold.woff2', 'fonts/ttkb.ttf'];
self.addEventListener('install', e => e.waitUntil(caches.open(CORE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('elx-core') && k !== CORE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isPage = url.origin === location.origin && (url.pathname.endsWith('/') || url.pathname.endsWith('.html'));
  const isManifest = url.pathname.endsWith('audio/manifest.json');
  if (isPage || isManifest) {
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(CORE).then(k => k.put(req, c)); return r; })
      .catch(() => caches.match(req)));
    return;
  }
  e.respondWith(caches.match(req).then(m => m || fetch(req).then(r => {
    if (r.ok || r.type === 'opaque') { const c = r.clone(); caches.open(CORE).then(k => k.put(req, c)); }
    return r;
  })));
});
