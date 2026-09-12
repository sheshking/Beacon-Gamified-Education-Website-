// ============================================
// BEACON — shared sound effects
// Include this ONE script (before home.js / course-engine.js)
// on every page that should be able to play sounds.
//
// Respects the "Sound Effects" toggle saved from settings.html
// (localStorage key: beaconSettings.sound). Defaults to ON if
// no preference has been saved yet.
// ============================================

const BeaconSounds = {
  click: new Audio('assets/sounds/click.wav'),
  hover: new Audio('assets/sounds/hover.wav'),
  success: new Audio('assets/sounds/success.wav'),
  error: new Audio('assets/sounds/error.wav'),
  achievement: new Audio('assets/sounds/achievement.wav'),
  levelUp: new Audio('assets/sounds/level_up.wav'),
  xpGain: new Audio('assets/sounds/xp_gain.wav'),
  notification: new Audio('assets/sounds/notification.wav'),
  questStart: new Audio('assets/sounds/quest_start.wav'),
  streak: new Audio('assets/sounds/streak.wav'),
};

function soundEffectsEnabled() {
  try {
    const settings = JSON.parse(localStorage.getItem('beaconSettings') || '{}');
    return settings.sound !== undefined ? settings.sound : true; // default ON
  } catch (e) {
    return true;
  }
}

function playSound(name) {
  if (!soundEffectsEnabled()) return;
  const s = BeaconSounds[name];
  if (!s) return;
  s.currentTime = 0; // rewind so rapid repeated triggers replay from the start
  s.play().catch(() => {}); // ignore browser autoplay-block errors before first interaction
}
