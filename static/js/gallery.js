/* ===== GALLERY PAGE JS ===== */

const galleryItems = document.querySelectorAll('.gallery-item');
const filterBtns = document.querySelectorAll('.filter-btn');

// Animate items on load
const galleryObs = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 55);
    }
  });
}, { threshold: 0.05 });
galleryItems.forEach(item => galleryObs.observe(item));

// Filter
filterBtns.forEach(btn => {
  btn.addEventListener('click', function () {
    filterBtns.forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const filter = this.dataset.filter;
    galleryItems.forEach(item => {
      const match = filter === 'all' || item.dataset.cat === filter;
      item.classList.toggle('hidden', !match);
    });
  });
});

// Lightbox
const lightbox = document.getElementById('lightbox');
const lbImg = document.getElementById('lbImg');
const lbCaption = document.getElementById('lbCaption');
let currentIdx = 0;

function getVisible() {
  return [...galleryItems].filter(i => !i.classList.contains('hidden'));
}

function openLightbox(idx) {
  currentIdx = idx;
  updateLightbox();
  lightbox.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function updateLightbox() {
  const visible = getVisible();
  if (!visible[currentIdx]) return;
  lbImg.src = visible[currentIdx].querySelector('img').src;
  lbCaption.textContent = visible[currentIdx].dataset.caption || '';
}

function closeLightbox() {
  lightbox.classList.remove('open');
  document.body.style.overflow = '';
}

galleryItems.forEach((item, i) => {
  item.addEventListener('click', () => {
    const visible = getVisible();
    const visibleIdx = visible.indexOf(item);
    if (visibleIdx >= 0) openLightbox(visibleIdx);
  });
});

document.getElementById('lbClose').addEventListener('click', closeLightbox);
document.getElementById('lbPrev').addEventListener('click', () => {
  const visible = getVisible();
  currentIdx = (currentIdx - 1 + visible.length) % visible.length;
  updateLightbox();
});
document.getElementById('lbNext').addEventListener('click', () => {
  const visible = getVisible();
  currentIdx = (currentIdx + 1) % visible.length;
  updateLightbox();
});
lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
document.addEventListener('keydown', e => {
  if (!lightbox.classList.contains('open')) return;
  const visible = getVisible();
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft') { currentIdx = (currentIdx - 1 + visible.length) % visible.length; updateLightbox(); }
  if (e.key === 'ArrowRight') { currentIdx = (currentIdx + 1) % visible.length; updateLightbox(); }
});
