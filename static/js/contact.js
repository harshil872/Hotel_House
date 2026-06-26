/* ===== CONTACT PAGE JS ===== */

// Contact form submit
function handleSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById('submitBtn');
  const msg = document.getElementById('successMsg');
  btn.textContent = 'Sending...';
  btn.classList.add('loading');
  setTimeout(() => {
    btn.textContent = 'Send Message';
    btn.classList.remove('loading');
    msg.classList.add('show');
    document.getElementById('contactForm').reset();
    setTimeout(() => msg.classList.remove('show'), 5000);
  }, 1800);
}

// Highlight today's row in hours table
const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const todayName = days[new Date().getDay()];
document.querySelectorAll('.hours-table tr').forEach(row => {
  const cell = row.querySelector('td:first-child');
  if (cell && cell.textContent.trim().startsWith(todayName)) {
    row.classList.add('today-highlight');
  }
});
