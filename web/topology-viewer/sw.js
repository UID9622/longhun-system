// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-1e6a71dc
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂拓扑 · Service Worker v1.1 · 离线缓存
const C = 'longhun-topology-v1.5';
const ASSETS = ['./', './index.html', './manifest.webmanifest',
  './icon.svg', './icon-180.png', './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(C).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      const cp = res.clone();
      caches.open(C).then(c => c.put(e.request, cp));
      return res;
    }).catch(() => caches.match('./index.html')))
  );
});
