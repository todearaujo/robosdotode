// simple pwa config
var cacheVersion = new Date().getTime();
var staticCacheName = "flask-pwa-v" + cacheVersion

var filesToCache = [
    '/',
    '/templates/offline',
    '/static/48.png',
    '/static/72.png',
    '/static/96.png',
    '/static/128.png',
    '/static/192.png',
    '/static/384.png',
    '/static/512.png',
    '/static/favicon-16x16.png',
    '/static/favicon-32x32.png',
    '/static/favicon.ico',
];

// Cache on install
self.addEventListener("install", event => {
  this.skipWaiting();
  event.waitUntil(
    caches.open(staticCacheName)
      .then(cache => {
        return cache.addAll(filesToCache);
      })
  )
});

// Clear cache on activate
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => (cacheName.startsWith("flask-pwa-")))
          .filter(cacheName => (cacheName !== staticCacheName))
          .map(cacheName => caches.delete(cacheName))
      );
    })
  );
});

// Serve from cache, and return offline page if client is offline 
this.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate' || (event.request.method === 'GET' && event.request.headers.get('accept').includes('text/html'))) {
    event.respondWith(
      fetch(event.request.url).catch(error => {
        return caches.match('/templates/offline');
      })
    );
  } else{
    event.respondWith(caches.match(event.request)
        .then(function (response) {
        return response || fetch(event.request);
      })
    );
  }
});