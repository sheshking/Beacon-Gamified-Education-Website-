// ============================================
// BEACON — login page behaviour
// ============================================

function loadPlayer() {
  try { return JSON.parse(localStorage.getItem('beaconPlayer') || '{}'); }
  catch (e) { return {}; }
}
function savePlayer(p) {
  try { localStorage.setItem('beaconPlayer', JSON.stringify(p)); } catch (e) {}
}

const player = loadPlayer();
const hasSavedPlayer = !!player.username;

// ---------- personalize HUD + form for a returning player ----------
if (hasSavedPlayer) {
  document.getElementById('hudPlayer').textContent = player.username;
  document.getElementById('usernameInput').value = player.username;
} else {
  document.getElementById('hudPlayer').textContent = 'GUEST';
}

const xp = player.xp || 0;
const level = Math.floor(xp / 100) + 1;
document.getElementById('hudLevel').textContent = String(level).padStart(2, '0');
document.getElementById('xpLabel').textContent = `${xp}/1000 XP`;
document.getElementById('xpFill').style.width = Math.min((xp / 1000) * 100, 100) + '%';

// reflect the returning player's saved difficulty as the active pill
const pillGroup = document.getElementById('pillGroup');
const pills = pillGroup.querySelectorAll('.pill');
let selectedDifficulty = player.experience || 'Intermediate';
pills.forEach((p) => {
  p.classList.toggle('active', p.dataset.val === selectedDifficulty);
});
pills.forEach((p) => {
  p.addEventListener('click', () => {
    pills.forEach((x) => x.classList.remove('active'));
    p.classList.add('active');
    selectedDifficulty = p.dataset.val;
  });
});

// ---------- login submit ----------
document.getElementById('loginForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const entered = document.getElementById('usernameInput').value.trim();
  const errorEl = document.getElementById('loginError');

  const matches = hasSavedPlayer && entered.toLowerCase() === player.username.toLowerCase();

  if (!entered || !matches) {
    errorEl.classList.add('show');
    return;
  }

  errorEl.classList.remove('show');
  player.experience = selectedDifficulty;
  savePlayer(player);
  window.location.href = 'home.html';
});
