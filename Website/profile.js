// ============================================
// BEACON — profile page behaviour
// ============================================

// Pull whatever was saved at signup (if anything), otherwise fall back
// to placeholder demo values so the page still looks right on its own.
let saved = {};
try {
  saved = JSON.parse(localStorage.getItem('beaconPlayer') || '{}');
} catch (e) {
  saved = {};
}

const username = saved.username || 'PLAYER';
const grade = saved.grade || '--';
const experience = saved.experience || 'Beginner';

document.getElementById('playerName').textContent = username.toUpperCase();
document.getElementById('academicClass').textContent = `CLASS ${grade}`;
document.getElementById('difficultyTier').textContent = experience.toUpperCase();

// show the uploaded photo (from signup), or a blank placeholder if none
const avatarRing = document.querySelector('.avatar-ring');
if (avatarRing) {
  avatarRing.innerHTML = saved.photo
    ? `<img src="${saved.photo}" alt="" />`
    : '<span class="avatar-glyph">&#128100;</span>';
}

// rank label follows difficulty tier, just for a bit of flavour
const rankByTier = {
  beginner: 'Arcade Novice',
  intermediate: 'Code Adventurer',
  expert: 'Quest Master'
};
document.getElementById('playerRank').textContent =
  rankByTier[experience.toLowerCase()] || 'Arcade Novice';

// XP bar — pulls the real accumulated XP saved from completed quest lessons
const xpCurrent = saved.xp || 0;
const xpMax = 1000;
document.getElementById('xpCurrent').textContent = xpCurrent;
document.getElementById('xpMax').textContent = xpMax;
document.getElementById('hudXp').textContent = String(xpCurrent).padStart(3, '0');
document.getElementById('hudXpMax').textContent = xpMax;
const pct = Math.max((xpCurrent / xpMax) * 100, 1.5); // small visible sliver at 0
document.getElementById('xpFill').style.width = pct + '%';
