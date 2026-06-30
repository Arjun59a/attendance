const CACHE_NAME = "attendance-portal-v12"; // New version forces the phone browser to dump old broken caches
const ASSETS = [
  "./",
  "./portal.html",
  "./html5-qrcode.min.js"
];

// Instantly force installation of the clean caching rules
self.addEventListener("install", (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Immediately wipe away old broken cache versions from your phone
self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Network-first with immediate offline fallback strategy
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;

  e.respondWith(
    fetch(e.request)
      .then((response) => {
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(e.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(e.request, { ignoreSearch: true }).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          
          if (e.request.mode === 'navigate') {
            return caches.match('./portal.html', { ignoreSearch: true });
          }
        });
      })
  );
});