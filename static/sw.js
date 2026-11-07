/**
 * Service Worker για το does4u-fleet tracker.
 *
 * v1.0: μόνο install + minimal fetch handling.
 * Offline caching θα προστεθεί σε επόμενη έκδοση.
 */

// Ενεργοποίηση αμέσως χωρίς να περιμένει κλειστά tabs
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

// Ενεργοποίηση χωρίς reload
self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

// Pass-through fetch (cache logic μπορεί να προστεθεί εδώ)
self.addEventListener('fetch', (event) => {
  // Προς το παρόν δεν κάνουμε cache — απλά αφήνουμε το browser να φορτώσει
  // Αν χρειαστεί offline support αργότερα, θα προσθέσουμε Cache API εδώ.
});