/* ===== BASE / SHARED JS ===== */

// Mobile menu
function openMobile() { document.getElementById('mobileMenu').classList.add('open'); }
function closeMobile() { document.getElementById('mobileMenu').classList.remove('open'); }

// Close mobile menu on link click
document.querySelectorAll('.mobile-menu a').forEach(a => {
  a.addEventListener('click', closeMobile);
});

// Scroll reveal
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 80);
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
