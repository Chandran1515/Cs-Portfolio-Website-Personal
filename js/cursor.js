export function initCursor() {
  const cursor = document.getElementById('cursor');
  const ring = document.getElementById('cursorRing');
  if (!cursor || !ring) return;

  let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;
  
  document.addEventListener('mousemove', e => {
    mouseX = e.clientX; mouseY = e.clientY;
    cursor.style.left = mouseX + 'px';
    cursor.style.top = mouseY + 'px';
  });

  function animateRing() {
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;
    ring.style.left = ringX + 'px';
    ring.style.top = ringY + 'px';
    requestAnimationFrame(animateRing);
  }
  animateRing();

  function attachHoverEvents() {
    document.querySelectorAll('a, button, .filter-btn, .work-card, .bim-card, .btn-primary, .btn-ghost').forEach(el => {
      // prevent multiple listeners
      if(el.dataset.cursorAttached) return;
      el.dataset.cursorAttached = "true";

      el.addEventListener('mouseenter', () => {
        cursor.style.transform = 'translate(-50%,-50%) scale(2.5)';
        ring.style.width = '50px'; ring.style.height = '50px';
        ring.style.opacity = '0.3';
      });
      el.addEventListener('mouseleave', () => {
        cursor.style.transform = 'translate(-50%,-50%) scale(1)';
        ring.style.width = '32px'; ring.style.height = '32px';
        ring.style.opacity = '0.5';
      });
    });
  }

  attachHoverEvents();
  window.attachHoverEvents = attachHoverEvents;
}
