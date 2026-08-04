// ═══════════════════════════════════════════
// HOTEL HOUSE — BASE.JS
// Navbar scroll, mobile menu, reveal animations, counter
// ═══════════════════════════════════════════

// ── NAVBAR SCROLL ─────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  const isTransparent = navbar.classList.contains('transparent');
  const onScroll = () => {
    if (isTransparent) {
      navbar.classList.toggle('scrolled', window.scrollY > 60);
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ── MOBILE MENU ───────────────────────────
function openMobile() {
  document.getElementById('mobileMenu')?.classList.add('open');
  document.getElementById('mobileOverlay')?.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMobile() {
  document.getElementById('mobileMenu')?.classList.remove('open');
  document.getElementById('mobileOverlay')?.classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMobile(); });

// ── REVEAL ON SCROLL ──────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, i * 80);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// ── COUNTER ANIMATION ─────────────────────
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el    = entry.target;
      const end   = parseInt(el.dataset.count, 10);
      const dur   = 2000;
      const step  = end / (dur / 16);
      let current = 0;
      const timer = setInterval(() => {
        current += step;
        if (current >= end) {
          el.textContent = end.toLocaleString() + (el.dataset.suffix || '');
          clearInterval(timer);
        } else {
          el.textContent = Math.floor(current).toLocaleString();
        }
      }, 16);
      counterObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-num, .dash-stat-num[data-count]').forEach(el => {
  if (el.dataset.count) counterObserver.observe(el);
});

// ── AUTO-DISMISS TOASTS ───────────────────
setTimeout(() => {
  document.querySelectorAll('.toast').forEach(t => t.remove());
}, 5500);
