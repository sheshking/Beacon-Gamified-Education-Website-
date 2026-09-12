// ============================================
// BEACON — Guild Intel & Feedback Hub behaviour
// ============================================

function loadPlayer() {
  try { return JSON.parse(localStorage.getItem('beaconPlayer') || '{}'); }
  catch (e) { return {}; }
}
function savePlayer(p) {
  try { localStorage.setItem('beaconPlayer', JSON.stringify(p)); } catch (e) {}
}

// ---------- HUD ----------

function refreshHud() {
  const p = loadPlayer();
  document.getElementById('hudPlayer').textContent = (p.username || 'PLAYER').toUpperCase();
  document.getElementById('hudXp').textContent = String(Math.min(p.xp || 0, 999)).padStart(3, '0');
  document.getElementById('uplinkName').textContent = (p.username || 'PLAYER').toUpperCase();
  document.getElementById('uplinkClass').textContent = p.grade || '--';
}

// ---------- tab switching ----------

document.querySelectorAll('.subnav-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.subnav-btn').forEach((b) => b.classList.remove('active'));
    document.querySelectorAll('.hub-panel').forEach((p) => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('panel-' + btn.dataset.panel).classList.add('active');
  });
});

// ---------- FAQ: accordion ----------

document.querySelectorAll('.faq-question').forEach((q) => {
  q.addEventListener('click', () => {
    const item = q.closest('.faq-item');
    const wasOpen = item.classList.contains('open');
    item.classList.toggle('open');
    q.querySelector('.fq-toggle').textContent = wasOpen ? '▼ EXPAND' : '▲ COLLAPSE';
  });
});

// ---------- FAQ: category filter + search ----------

let currentFaqCat = 'all';

function applyFaqFilter() {
  const search = document.getElementById('faqSearch').value.trim().toLowerCase();
  document.querySelectorAll('.faq-item').forEach((item) => {
    const matchesCat = currentFaqCat === 'all' || item.dataset.cat === currentFaqCat;
    const text = item.querySelector('.fq-text').textContent.toLowerCase();
    const matchesSearch = !search || text.includes(search);
    item.style.display = (matchesCat && matchesSearch) ? '' : 'none';
  });
}

document.querySelectorAll('.faq-cat').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.faq-cat').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    currentFaqCat = btn.dataset.cat;
    applyFaqFilter();
  });
});
document.getElementById('faqSearch').addEventListener('input', applyFaqFilter);

// ---------- FEEDBACK: rating ----------

const ratingMessages = {
  1: '💤 1 Coin: Rookie run — let us know what felt rough.',
  2: '🙂 2 Coins: Decent dungeon crawl.',
  3: '👍 3 Coins: Solid arcade session!',
  4: '🔥 4 Coins: Heroic playthrough!',
  5: '⚡ 5 Coins: God Tier Arcade Experience!'
};

let selectedRating = null;
document.querySelectorAll('.rating-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.rating-btn').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    selectedRating = btn.dataset.val;
    const fb = document.getElementById('ratingFeedback');
    fb.textContent = ratingMessages[selectedRating];
    fb.style.display = 'flex';
  });
});

// ---------- FEEDBACK: category ----------

let selectedCategory = 'praise';
document.querySelectorAll('.category-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.category-btn').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    selectedCategory = btn.dataset.cat;
  });
});

// ---------- FEEDBACK: submit ----------

document.getElementById('feedbackForm').addEventListener('submit', (e) => {
  e.preventDefault();

  const player = loadPlayer();
  player.xp = (player.xp || 0) + 25;
  savePlayer(player);
  refreshHud();

  const success = document.getElementById('fbSuccess');
  success.classList.add('show');

  document.getElementById('fbComments').value = '';
  setTimeout(() => success.classList.remove('show'), 4000);
});

refreshHud();
applyFaqFilter();
