/* ===== RESERVATIONS PAGE JS ===== */

// Set min date to today
const resDateInput = document.getElementById('resDate');
if (resDateInput) {
  const today = new Date().toISOString().split('T')[0];
  resDateInput.min = today;
  resDateInput.value = today;
}

// Guest counter
let guests = 2;
function changeGuest(delta) {
  guests = Math.max(1, Math.min(20, guests + delta));
  document.getElementById('guestCount').textContent = guests;
}

// Time slot selection
function selectTime(el) {
  document.querySelectorAll('.time-slot').forEach(t => t.classList.remove('selected'));
  el.classList.add('selected');
}

// Multi-step form navigation
function goToStep(n) {
  // Validate step 1
  if (n === 2) {
    const fn = document.getElementById('firstName').value.trim();
    const ln = document.getElementById('lastName').value.trim();
    const em = document.getElementById('email').value.trim();
    const ph = document.getElementById('phone').value.trim();
    if (!fn || !ln || !em || !ph) {
      alert('Please fill in all required fields.');
      return;
    }
  }
  // Validate step 2
  if (n === 3) {
    const date = document.getElementById('resDate').value;
    const slot = document.querySelector('.time-slot.selected');
    if (!date || !slot) {
      alert('Please select a date and time.');
      return;
    }
    buildSummary();
  }
  // Switch panels
  [1, 2, 3].forEach(i => {
    document.getElementById('panel' + i).classList.toggle('active', i === n);
    const ind = document.getElementById('step' + i + 'Ind');
    if (ind) {
      ind.classList.toggle('active', i === n);
      ind.classList.toggle('done', i < n);
    }
  });
}

function buildSummary() {
  const fn = document.getElementById('firstName').value.trim();
  const ln = document.getElementById('lastName').value.trim();
  const em = document.getElementById('email').value.trim();
  const date = document.getElementById('resDate').value;
  const slot = document.querySelector('.time-slot.selected');
  const d = new Date(date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  const rows = [
    ['Guest Name', fn + ' ' + ln],
    ['Email', em],
    ['Guests', guests + (guests === 1 ? ' person' : ' people')],
    ['Date', d],
    ['Time', slot ? slot.textContent : '—'],
  ];
  const container = document.getElementById('summaryContent');
  container.innerHTML = rows.map(([label, val]) =>
    `<div class="summary-row"><span class="summary-label">${label}</span><span class="summary-val">${val}</span></div>`
  ).join('');
}

function confirmBooking() {
  const ref = 'SAV-' + Math.floor(100000 + Math.random() * 900000);
  document.getElementById('bookingRef').textContent = ref;
  const stepsBar = document.getElementById('stepsBar');
  if (stepsBar) stepsBar.style.display = 'none';
  [1, 2, 3].forEach(i => document.getElementById('panel' + i).classList.remove('active'));
  document.getElementById('successPanel').classList.add('active');
}
