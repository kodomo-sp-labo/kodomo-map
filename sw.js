// Service Worker — ネットワーク優先（network-first）方式
// 設計方針：
//   オンライン時は常にサーバーの最新版を取得する（＝HTMLを更新すれば全端末に即反映）。
//   オフライン時のみ、最後に取得できたキャッシュを表示する。
// キャッシュ優先方式にすると更新が届かなくなるため、意図的にこの方式を採用している。

const CACHE_NAME = 'kodomo-map-v1';

self.addEventListener('install', function (e) {
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE_NAME; })
            .map(function (k) { return caches.delete(k); })
      );
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  // GET以外や外部タイルサーバーへのリクエストはそのまま通す
  if (e.request.method !== 'GET') return;

  e.respondWith(
    fetch(e.request)
      .then(function (res) {
        // 取得成功：同一オリジンのものだけキャッシュを更新
        if (res.ok && new URL(e.request.url).origin === self.location.origin) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(function (c) { c.put(e.request, clone); });
        }
        return res;
      })
      .catch(function () {
        // オフライン時：キャッシュがあればそれを返す
        return caches.match(e.request);
      })
  );
});
