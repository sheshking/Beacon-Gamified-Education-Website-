// ============================================
// BEACON — Settings page behaviour
// ============================================

function loadPlayer() {
  try { return JSON.parse(localStorage.getItem('beaconPlayer') || '{}'); }
  catch (e) { return {}; }
}
function savePlayer(p) {
  try { localStorage.setItem('beaconPlayer', JSON.stringify(p)); } catch (e) {}
}
function loadSettings() {
  try { return JSON.parse(localStorage.getItem('beaconSettings') || '{}'); }
  catch (e) { return {}; }
}
function saveSettingsToStorage(s) {
  try { localStorage.setItem('beaconSettings', JSON.stringify(s)); } catch (e) {}
}

const player = loadPlayer();
const savedSettings = loadSettings();

// ---------- HUD ----------
document.getElementById('hudPlayer').textContent = (player.username || 'PLAYER').toUpperCase();
document.getElementById('hudXp').textContent = String(Math.min(player.xp || 0, 999)).padStart(3, '0');

// ---------- local buffered state (applied on Save) ----------
const state = {
  sound: savedSettings.sound !== undefined ? savedSettings.sound : true,
  dark: savedSettings.dark !== undefined ? savedSettings.dark : true,
  email: savedSettings.email !== undefined ? savedSettings.email : false
};

const DIFFICULTIES = ['Beginner', 'Intermediate', 'Advanced'];
// the rest of the site stores 'Expert' rather than 'Advanced' — map between them
function toDisplayDifficulty(stored) {
  return stored === 'Expert' ? 'Advanced' : (stored || 'Intermediate');
}
function toStoredDifficulty(display) {
  return display === 'Advanced' ? 'Expert' : display;
}
let currentDifficulty = toDisplayDifficulty(player.experience);

function applyToggleVisual(el, on) {
  el.classList.toggle('on', on);
}

// ---------- General toggles ----------
const toggleSound = document.getElementById('toggleSound');
const toggleDark = document.getElementById('toggleDark');
const toggleEmail = document.getElementById('toggleEmail');

applyToggleVisual(toggleSound, state.sound);
applyToggleVisual(toggleDark, state.dark);
applyToggleVisual(toggleEmail, state.email);

toggleSound.addEventListener('click', () => {
  state.sound = !state.sound;
  applyToggleVisual(toggleSound, state.sound);
});
toggleDark.addEventListener('click', () => {
  state.dark = !state.dark;
  applyToggleVisual(toggleDark, state.dark);
});
toggleEmail.addEventListener('click', () => {
  state.email = !state.email;
  applyToggleVisual(toggleEmail, state.email);
});

// ---------- Difficulty cycle ----------
const difficultyBtn = document.getElementById('difficultyBtn');
difficultyBtn.textContent = currentDifficulty + ' ▸';
difficultyBtn.addEventListener('click', () => {
  const idx = DIFFICULTIES.indexOf(currentDifficulty);
  currentDifficulty = DIFFICULTIES[(idx + 1) % DIFFICULTIES.length];
  difficultyBtn.textContent = currentDifficulty + ' ▸';
});

// ---------- Full Beam locked toggles + previews ----------
document.querySelectorAll('.toggle[data-locked]').forEach((el) => {
  el.addEventListener('click', () => {
    const key = el.dataset.locked;
    const tip = document.getElementById('tooltip-' + key);
    if (tip) tip.classList.toggle('show');
  });
});
document.querySelectorAll('.beam-preview').forEach((el) => {
  el.addEventListener('click', () => {
    const key = el.dataset.preview;
    const tip = document.getElementById('tooltip-' + key);
    if (tip) tip.classList.toggle('show');
  });
});
document.getElementById('rangeCheck')?.addEventListener('click', () => {
  document.getElementById('tooltip-range')?.classList.toggle('show');
});

// ---------- Full Beam pricing panel ----------
let selectedPlan = 'yearly';
document.querySelectorAll('.plan-card').forEach((card) => {
  card.addEventListener('click', () => {
    document.querySelectorAll('.plan-card').forEach((c) => c.classList.remove('selected'));
    card.classList.add('selected');
    selectedPlan = card.dataset.plan;
  });
});

const planNames = { yearly: 'Yearly (₹799/yr)', monthly: 'Monthly (₹99/mo)', crew: 'Crew ×4 (₹249/mo)' };
document.getElementById('promoCta').addEventListener('click', () => {
  const result = document.getElementById('promoResult');
  result.textContent =
    `🔒 No real checkout here — this build has no payment system connected, so Full Beam can't actually be turned on yet. You picked the ${planNames[selectedPlan]} plan though, so it's ready to wire up whenever billing exists.`;
  result.classList.add('show');
});

// ---------- Signal Freeze (the one real, non-locked Full Beam-adjacent feature) ----------
const freezeBox = document.getElementById('freezeBox');
const freezeCount = document.getElementById('freezeCount');
let freezeUsed = savedSettings.freezeUsed || false;

function renderFreeze() {
  if (freezeUsed) {
    freezeCount.textContent = '0 / 1 left';
    freezeBox.classList.add('used');
  } else {
    freezeCount.textContent = '1 / 1 left';
    freezeBox.classList.remove('used');
  }
}
renderFreeze();

freezeBox.addEventListener('click', () => {
  if (freezeUsed) return;
  freezeUsed = true;
  renderFreeze();
  const settings = loadSettings();
  settings.freezeUsed = true;
  saveSettingsToStorage(settings);
});

// ---------- Save Changes ----------
document.getElementById('saveBtn').addEventListener('click', () => {
  const settings = loadSettings();
  settings.sound = state.sound;
  settings.dark = state.dark;
  settings.email = state.email;
  saveSettingsToStorage(settings);

  const p = loadPlayer();
  p.experience = toStoredDifficulty(currentDifficulty);
  savePlayer(p);

  const confirm = document.getElementById('saveConfirm');
  confirm.classList.add('show');
  setTimeout(() => confirm.classList.remove('show'), 3000);
});
