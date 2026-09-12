// NOTE: this file expects sfx.js to be loaded BEFORE it in home.html,
// which provides the global playSound() function.

// show the saved username and photo (from signup) in the badge, if we have one
try {
  const saved = JSON.parse(localStorage.getItem('beaconPlayer') || '{}');
  if (saved.username) {
    const nameEl = document.querySelector('.avatar-name');
    if (nameEl) nameEl.textContent = saved.username.toUpperCase();
  }
  const iconEl = document.querySelector('.avatar-icon');
  if (iconEl) {
    iconEl.innerHTML = saved.photo
      ? `<img src="${saved.photo}" alt="" />`
      : '&#128100;'; // blank placeholder person
  }
  const xpEl = document.getElementById('hudXp');
  if (xpEl) xpEl.textContent = String(Math.min(saved.xp || 0, 999)).padStart(3, '0');
} catch (e) {
  // no saved player — keep the default placeholder
}

// clicking a quest card (not its button) marks it as the selected language
document.querySelectorAll('.quest-card').forEach((card) => {
  // subtle hover tick
  card.addEventListener('mouseenter', () => playSound('hover'));

  card.addEventListener('click', (e) => {
    if (e.target.closest('.quest-btn')) return; // let the button's own click through
    playSound('click');
    document.querySelectorAll('.quest-card').forEach((c) => c.classList.remove('selected'));
    card.classList.add('selected');
  });
});

// "Start Quest" buttons: play a sound, then navigate once it's had a moment to play
document.querySelectorAll('.quest-btn').forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    playSound('questStart');
    const dest = btn.getAttribute('data-href');
    setTimeout(() => {
      if (dest) location.href = dest;
    }, 180); // short delay so the sound is audible before the page unloads
  });
});

// "Boss Fight" buttons: same navigate pattern, straight into that language's boss fight
document.querySelectorAll('.boss-btn').forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation(); // don't also trigger the card's "selected" click handler
    playSound('questStart');
    const dest = btn.getAttribute('data-href');
    setTimeout(() => {
      if (dest) location.href = dest;
    }, 180);
  });
});

// rotate through a few tips so the tip bar feels alive
const tips = [
  "If you're a beginner, try Python first to start earning XP immediately!",
  "Finish a lesson every day to keep your streak alive.",
  "Struggling with a topic? Replay it — repetition is how XP compounds.",
  "C++ is a great pick if you want to understand what's happening under the hood.",
  "Java quests unlock team projects once you hit Level 5."
];
let tipIndex = 0;
const tipEl = document.getElementById('tipText');
if (tipEl) {
  setInterval(() => {
    tipIndex = (tipIndex + 1) % tips.length;
    tipEl.style.opacity = 0;
    setTimeout(() => {
      tipEl.textContent = tips[tipIndex];
      tipEl.style.opacity = 1;
    }, 250);
  }, 6000);
  tipEl.style.transition = 'opacity .25s ease';
}
