/* ===== INDEX / HOME PAGE JS ===== */

// Loader
window.addEventListener('load', () => {
  setTimeout(() => {
    const loader = document.getElementById('loader');
    if (loader) {
      loader.style.opacity = '0';
      loader.style.transition = 'opacity 0.5s';
      setTimeout(() => loader.style.display = 'none', 500);
    }
  }, 2200);
});

// Navbar scroll effect
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('solid', window.scrollY > 60);
  });
}

// Counter animation
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = +el.dataset.count;
    let current = 0;
    const step = target / 60;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        el.textContent = target.toLocaleString() + '+';
        clearInterval(timer);
      } else {
        el.textContent = Math.floor(current).toLocaleString();
      }
    }, 25);
  });
}
const statsGrid = document.querySelector('.stats-grid');
if (statsGrid) {
  const statsObs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) { animateCounters(); statsObs.disconnect(); }
  }, { threshold: 0.3 });
  statsObs.observe(statsGrid);
}

// Dish order button feedback
document.querySelectorAll('.dish-order').forEach(btn => {
  btn.addEventListener('click', function () {
    this.textContent = '✓ Added!';
    this.style.background = 'var(--gold)';
    this.style.color = 'var(--dark)';
    setTimeout(() => {
      this.textContent = 'Order Now';
      this.style.background = '';
      this.style.color = 'var(--gold)';
    }, 2000);
  });
});

// Parallax hero
window.addEventListener('scroll', () => {
  const heroBg = document.querySelector('.hero-bg');
  if (heroBg) heroBg.style.transform = `scale(1) translateY(${window.scrollY * 0.28}px)`;
});
