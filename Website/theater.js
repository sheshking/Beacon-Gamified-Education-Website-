// ============================================
// BEACON — Video Theater behaviour
// ============================================

const LANGS = [
  { key: 'python', label: 'Python', icon: '&#128013;' },
  { key: 'java', label: 'Java', icon: '&#9749;' },
  { key: 'cpp', label: 'C++', icon: '&#128187;' }
];
const DIFFS = ['all', 'beginner', 'intermediate', 'advanced'];

let currentLang = 'python';
let currentDiff = 'all';
let currentVideo = null;

// ---------- player data ----------

function loadPlayer() {
  try { return JSON.parse(localStorage.getItem('beaconPlayer') || '{}'); }
  catch (e) { return {}; }
}
function savePlayer(p) {
  try { localStorage.setItem('beaconPlayer', JSON.stringify(p)); } catch (e) {}
}
function loadWatched() {
  try { return JSON.parse(localStorage.getItem('beaconWatched') || '{}'); }
  catch (e) { return {}; }
}
function saveWatched(w) {
  try { localStorage.setItem('beaconWatched', JSON.stringify(w)); } catch (e) {}
}
function videoKey(v) { return v.videoId || v.searchQuery; }

function playerDifficultyKey() {
  const p = loadPlayer();
  const exp = (p.experience || '').toLowerCase();
  if (exp === 'expert') return 'advanced';
  if (exp === 'intermediate') return 'intermediate';
  return 'beginner';
}

// ---------- rendering: tabs ----------

function renderLangTabs() {
  const el = document.getElementById('langTabs');
  el.innerHTML = '';
  LANGS.forEach((l) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'lang-tab' + (l.key === currentLang ? ' active' : '');
    btn.innerHTML = `${l.icon} ${l.label}`;
    btn.addEventListener('click', () => {
      currentLang = l.key;
      renderLangTabs();
      renderVideoList();
    });
    el.appendChild(btn);
  });
}

function renderDiffTabs() {
  const el = document.getElementById('diffTabs');
  el.innerHTML = '';
  DIFFS.forEach((d) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'diff-tab' + (d === currentDiff ? ' active' : '');
    btn.textContent = d.toUpperCase();
    btn.addEventListener('click', () => {
      currentDiff = d;
      renderDiffTabs();
      renderVideoList();
    });
    el.appendChild(btn);
  });
}

// ---------- rendering: video list ----------

function renderVideoList() {
  const list = THEATER_LIBRARY[currentLang] || [];
  const recommendedDiff = playerDifficultyKey();
  const filtered = currentDiff === 'all' ? list : list.filter((v) => v.difficulty === currentDiff);

  // recommended-first ordering
  const sorted = [...filtered].sort((a, b) => {
    const aRec = a.difficulty === recommendedDiff ? 0 : 1;
    const bRec = b.difficulty === recommendedDiff ? 0 : 1;
    return aRec - bRec;
  });

  const container = document.getElementById('videoList');
  container.innerHTML = '';

  if (sorted.length === 0) {
    container.innerHTML = '<div style="color:var(--ink-faint); font-size:15px; padding:10px;">No videos at this difficulty yet.</div>';
    return;
  }

  sorted.forEach((v) => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'video-card';
    if (currentVideo && videoKey(currentVideo) === videoKey(v)) card.classList.add('active');

    const thumbStyle = v.videoId
      ? `background-image:url('https://img.youtube.com/vi/${v.videoId}/hqdefault.jpg');`
      : `background:linear-gradient(135deg,#1c2450,#2a1440);`;

    const isRecommended = v.difficulty === recommendedDiff;

    card.innerHTML = `
      <div class="video-thumb" style="${thumbStyle}">
        ${isRecommended ? '<span class="badge-recommend">FOR YOU</span>' : ''}
        <span class="play-dot">&#9658;</span>
      </div>
      <div class="video-meta">
        <div class="v-title">${v.title}</div>
        <div class="v-creator">${v.creator} · ${v.duration}</div>
        <div class="v-tags">
          <span class="tag ${v.difficulty}">${v.difficulty}</span>
          <span class="tag xp">+${v.xp} XP</span>
        </div>
      </div>
    `;
    card.addEventListener('click', () => selectVideo(v));
    container.appendChild(card);
  });

  // auto-select first video if none selected or current one isn't in this list
  if (!currentVideo || !sorted.some((v) => videoKey(v) === videoKey(currentVideo))) {
    selectVideo(sorted[0]);
  }
}

// ---------- monitor panel ----------

function youtubeWatchUrl(v) {
  if (v.videoId) return `https://www.youtube.com/watch?v=${v.videoId}`;
  return `https://www.youtube.com/results?search_query=${encodeURIComponent(v.searchQuery)}`;
}

function selectVideo(v) {
  currentVideo = v;
  renderVideoList();

  document.getElementById('feedName').textContent = v.creator.toUpperCase();
  document.getElementById('detailTitle').textContent = v.title;
  document.getElementById('detailDesc').textContent = v.description;
  document.getElementById('watchBtn').href = youtubeWatchUrl(v);
  document.getElementById('fallbackNote').hidden = !!v.videoId;

  const timestampList = document.getElementById('timestampList');
  timestampList.innerHTML = '';
  v.timestamps.forEach(([time, label]) => {
    const row = document.createElement('div');
    row.className = 'ts-row';
    row.innerHTML = `<span class="ts-time">${time}</span><span>${label}</span>`;
    timestampList.appendChild(row);
  });

  const screen = document.getElementById('screen');
  const thumbUrl = v.videoId
    ? `https://img.youtube.com/vi/${v.videoId}/hqdefault.jpg`
    : '';
  screen.style.backgroundImage = thumbUrl ? `url('${thumbUrl}')` : 'linear-gradient(135deg,#1c2450,#2a1440)';
  screen.innerHTML = `
    <div class="screen-overlay" id="screenOverlay">
      <div class="big-play">&#9658;</div>
      <div class="launch-text">[ CLICK TO LAUNCH STREAM IN BROWSER ]</div>
    </div>
    <div class="screen-scanlines"></div>
  `;
  document.getElementById('screenOverlay').addEventListener('click', () => launchStream(v));

  updateCompleteButton(v);
}

function launchStream(v) {
  const screen = document.getElementById('screen');
  if (v.videoId) {
    screen.innerHTML = `<iframe src="https://www.youtube.com/embed/${v.videoId}?autoplay=1" title="${v.title}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
  } else {
    window.open(youtubeWatchUrl(v), '_blank', 'noopener');
  }
}

function updateCompleteButton(v) {
  const watched = loadWatched();
  const btn = document.getElementById('completeBtn');
  if (watched[videoKey(v)]) {
    btn.textContent = '✓ Completed';
    btn.classList.add('done');
  } else {
    btn.textContent = '✓ Mark Complete (+XP)';
    btn.classList.remove('done');
  }
}

// ---------- init ----------

function initTheater() {
  renderLangTabs();
  renderDiffTabs();
  renderVideoList();

  document.getElementById('completeBtn').addEventListener('click', () => {
    if (!currentVideo) return;
    const watched = loadWatched();
    const key = videoKey(currentVideo);
    if (watched[key]) return; // already awarded

    watched[key] = true;
    saveWatched(watched);

    const player = loadPlayer();
    player.xp = (player.xp || 0) + currentVideo.xp;
    savePlayer(player);

    updateCompleteButton(currentVideo);
  });

  document.getElementById('copyBtn').addEventListener('click', async () => {
    if (!currentVideo) return;
    const url = youtubeWatchUrl(currentVideo);
    const btn = document.getElementById('copyBtn');
    try {
      await navigator.clipboard.writeText(url);
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => { btn.textContent = original; }, 1500);
    } catch (e) {
      prompt('Copy this link:', url);
    }
  });
}

document.addEventListener('DOMContentLoaded', initTheater);
