/* ===== MENU PAGE JS ===== */

// Filter functionality
const filterBtns = document.querySelectorAll('.filter-btn');
const menuCards = document.querySelectorAll('.menu-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', function () {
    filterBtns.forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const filter = this.dataset.filter;
    menuCards.forEach((card, i) => {
      const match = filter === 'all' || card.dataset.cat === filter;
      card.classList.toggle('hidden', !match);
      if (match) {
        card.style.animationDelay = (i * 0.05) + 's';
        card.style.animation = 'none';
        card.offsetHeight; // reflow
        card.style.animation = '';
      }
    });
  });
});

// Add to cart button feedback
document.querySelectorAll('.add-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    this.innerHTML = '✓';
    this.style.background = 'var(--gold)';
    this.style.color = 'var(--dark)';
    setTimeout(() => {
      this.innerHTML = '+';
      this.style.background = '';
      this.style.color = 'var(--gold)';
    }, 1500);
  });
});
