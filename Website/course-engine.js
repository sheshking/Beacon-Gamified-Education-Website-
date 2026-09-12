// ============================================
// BEACON — quest engine (shared by all 3 languages)
// NOTE: this file expects sfx.js to be loaded BEFORE it in each
// course-*.html page, which provides the global playSound() function.
// ============================================

let currentSectionKey = null;
let currentLessonIndex = 0;
let pyodideInstance = null;
let pyodideLoading = false;

// attempt tracking / hint & solution reveal state (per lesson visit)
let currentAttempts = 0;
let hintShownForCurrent = false;
let solutionShownForCurrent = false;

const HINT_THRESHOLD = 5;
const GAMEOVER_THRESHOLD = 7;

// ---------- Boss Fight state ----------

let bossQuestions = [];
let bossIndex = 0;
let bossAnswers = [];

const BOSS_OVERLAY_HTML = `
<div class="boss-overlay" id="bossOverlay">
  <div class="boss-panel boss-intro" id="bossIntro">
    <div class="boss-skull" id="bossSkull">&#128128;</div>
    <div class="boss-intro-title">BOSS FIGHT INCOMING</div>
    <div class="boss-intro-sub">Prepare your code...</div>
  </div>

  <div class="boss-panel boss-quiz" id="bossQuiz">
    <div class="boss-quiz-header">
      <span class="boss-quiz-progress" id="bossProgress">Question 1 / 5</span>
      <button type="button" class="boss-pause-btn" id="bossPauseBtn">&#9208; Pause</button>
    </div>
    <div class="boss-question-box" id="bossQuestionBox"></div>
    <div class="boss-quiz-footer">
      <span class="boss-result-msg" id="bossResultMsg"></span>
      <button type="button" class="boss-submit-btn" id="bossSubmitBtn">Submit Answer</button>
    </div>
  </div>

  <div class="boss-panel boss-pause-screen" id="bossPauseScreen">
    <div class="boss-pause-title">&#9208; PAUSED</div>
    <div class="boss-pause-sub">The boss waits. Come back whenever you're ready.</div>
    <div class="boss-modal-actions">
      <button type="button" class="boss-modal-btn primary" id="bossResumeBtn">Resume</button>
      <button type="button" class="boss-modal-btn secondary" id="bossQuitBtn">Quit Boss Fight</button>
    </div>
  </div>

  <div class="boss-panel boss-result-screen" id="bossResultScreen">
    <div class="boss-result-icon" id="bossResultIcon"></div>
    <div class="boss-result-title" id="bossResultTitle"></div>
    <div class="boss-result-sub" id="bossResultSub"></div>
    <div class="boss-result-xp" id="bossResultXp"></div>
    <button type="button" class="boss-modal-btn primary" id="bossCloseBtn">Close</button>
  </div>
</div>
`;

// ---------- player / progress storage ----------

function loadPlayer() {
  try {
    return JSON.parse(localStorage.getItem('beaconPlayer') || '{}');
  } catch (e) {
    return {};
  }
}

function savePlayer(player) {
  try {
    localStorage.setItem('beaconPlayer', JSON.stringify(player));
  } catch (e) { /* ignore */ }
}

function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem('beaconProgress') || '{}');
  } catch (e) {
    return {};
  }
}

function saveProgress(progress) {
  try {
    localStorage.setItem('beaconProgress', JSON.stringify(progress));
  } catch (e) { /* ignore */ }
}

function isLessonDone(langKey, lessonId) {
  const progress = loadProgress();
  return !!(progress[langKey] && progress[langKey].includes(lessonId));
}

function markLessonDone(langKey, lessonId) {
  const progress = loadProgress();
  if (!progress[langKey]) progress[langKey] = [];
  if (!progress[langKey].includes(lessonId)) progress[langKey].push(lessonId);
  saveProgress(progress);
}

// ---------- "no XP" tracking (lessons where the solution was revealed) ----------

function loadNoXpSet() {
  try {
    return new Set(JSON.parse(localStorage.getItem('beaconNoXp') || '[]'));
  } catch (e) {
    return new Set();
  }
}

function saveNoXpSet(set) {
  try {
    localStorage.setItem('beaconNoXp', JSON.stringify(Array.from(set)));
  } catch (e) { /* ignore */ }
}

function noXpKey(langKey, lessonId) {
  return langKey + ':' + lessonId;
}

function markNoXp(langKey, lessonId) {
  const set = loadNoXpSet();
  set.add(noXpKey(langKey, lessonId));
  saveNoXpSet(set);
}

function isNoXp(langKey, lessonId) {
  return loadNoXpSet().has(noXpKey(langKey, lessonId));
}

function updateHudXp() {
  const player = loadPlayer();
  const xp = player.xp || 0;
  const el = document.getElementById('hudXp');
  if (el) el.textContent = String(Math.min(xp, 999)).padStart(3, '0');
}

// ---------- statement splitting (respects quotes) ----------

function splitTopLevel(code, sep) {
  const parts = [];
  let cur = '';
  let inStr = false, strCh = '';
  for (let i = 0; i < code.length; i++) {
    const ch = code[i];
    if (inStr) {
      cur += ch;
      if (ch === strCh && code[i - 1] !== '\\') inStr = false;
    } else if (ch === '"' || ch === "'") {
      inStr = true; strCh = ch; cur += ch;
    } else if (code.slice(i, i + sep.length) === sep) {
      parts.push(cur); cur = '';
      i += sep.length - 1;
    } else {
      cur += ch;
    }
  }
  if (cur.trim() !== '') parts.push(cur);
  return parts;
}

function stripComments(code) {
  return code
    .split('\n')
    .map((line) => {
      let inStr = false, strCh = '';
      for (let i = 0; i < line.length; i++) {
        const ch = line[i];
        if (inStr) {
          if (ch === strCh && line[i - 1] !== '\\') inStr = false;
        } else if (ch === '"' || ch === "'") {
          inStr = true; strCh = ch;
        } else if (line.slice(i, i + 2) === '//' || line.slice(i, i + 2) === '# ' || line[i] === '#') {
          return line.slice(0, i);
        }
      }
      return line;
    })
    .join('\n');
}

// ---------- tiny expression evaluator for the Java/C++ mini-interpreter ----------

function evalTerm(term, vars) {
  const t = term.trim();
  if (/^".*"$/.test(t) || /^'.*'$/.test(t)) {
    return t.slice(1, -1).replace(/\\n/g, '\n').replace(/\\"/g, '"');
  }
  if (/^-?\d+(\.\d+)?$/.test(t)) return Number(t);
  if (/^[A-Za-z_]\w*$/.test(t)) {
    if (t in vars) return vars[t];
    return t; // unknown identifier — treat as literal text rather than crash
  }
  // pure arithmetic sub-expression (digits, operators, parens, spaces only)
  if (/^[0-9+\-*/(). ]+$/.test(t)) {
    try { return Function(`"use strict";return (${t});`)(); } catch (e) { return t; }
  }
  return t;
}

function evalPlusExpr(expr, vars) {
  const terms = splitTopLevel(expr, '+').map((t) => evalTerm(t, vars));
  if (terms.length === 1) return terms[0];
  const hasString = terms.some((t) => typeof t === 'string');
  if (hasString) return terms.map((t) => String(t)).join('');
  return terms.reduce((a, b) => a + b, 0);
}

// ---------- Java / C++ mini interpreter ----------

function runMiniInterpreter(rawCode, lang) {
  const code = stripComments(rawCode);
  const statements = splitTopLevel(code, ';').map((s) => s.trim()).filter(Boolean);
  const vars = {};
  let output = '';

  const declareRe = /^(?:int|double|float|long|short|char|String|string|auto|bool)?\s*([A-Za-z_]\w*)\s*=\s*(.+)$/;
  const javaPrintRe = /^System\.out\.(println|print)\s*\((.*)\)$/;
  const cppCoutRe = /^cout\s*<<\s*(.+)$/;

  for (const stmt of statements) {
    let m;
    if (lang === 'java' && (m = stmt.match(javaPrintRe))) {
      const val = evalPlusExpr(m[2], vars);
      output += String(val) + (m[1] === 'println' ? '\n' : '');
      continue;
    }
    if (lang === 'cpp' && (m = stmt.match(cppCoutRe))) {
      const segments = splitTopLevel(m[1], '<<').map((s) => s.trim());
      for (const seg of segments) {
        if (seg === 'endl') { output += '\n'; continue; }
        if (/^"\\n"$/.test(seg)) { output += '\n'; continue; }
        output += String(evalPlusExpr(seg, vars));
      }
      continue;
    }
    if ((m = stmt.match(declareRe))) {
      vars[m[1]] = evalPlusExpr(m[2], vars);
      continue;
    }
    // anything else (blank lines, unrecognized syntax) is silently ignored —
    // this is a teaching-scoped interpreter, not a full compiler
  }

  return output;
}

// ---------- Python execution via Pyodide ----------

async function ensurePyodide(onStatus) {
  if (pyodideInstance) return pyodideInstance;
  if (pyodideLoading) {
    while (pyodideLoading) await new Promise((r) => setTimeout(r, 150));
    return pyodideInstance;
  }
  pyodideLoading = true;
  onStatus('Loading Python engine (first run only)…');
  pyodideInstance = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.0/full/'
  });
  pyodideLoading = false;
  return pyodideInstance;
}

async function runPython(code, onStatus) {
  const py = await ensurePyodide(onStatus);
  py.runPython('import sys, io\n_beacon_buf = io.StringIO()\nsys.stdout = _beacon_buf\nsys.stderr = _beacon_buf');
  let errorMsg = null;
  try {
    await py.runPythonAsync(code);
  } catch (e) {
    errorMsg = String(e).split('\n').slice(-2).join('\n');
  }
  const out = py.runPython('_beacon_buf.getvalue()');
  py.runPython('sys.stdout = sys.__stdout__\nsys.stderr = sys.__stderr__');
  return { output: out, error: errorMsg };
}

// ---------- output comparison ----------

function outputMatches(actual, expected) {
  const norm = (s) => s.split('\n').map((l) => l.trim()).filter((l, i, arr) => !(i === arr.length - 1 && l === ''));
  const a = norm(actual);
  const e = norm(expected);
  if (a.length !== e.length) return false;
  return a.every((line, i) => line === e[i]);
}

// ---------- error detection & plain-English explanations ----------

// Python: Pyodide already raises a real exception — we just translate the
// exception type into a plain-English "why this happened" line.
const PY_ERROR_EXPLAINERS = [
  { match: /IndentationError/, why: () =>
      "Python uses indentation (spaces) to know what belongs together. A line here is indented when it shouldn't be, or vice versa." },
  { match: /SyntaxError/, why: () =>
      "Python couldn't understand the structure of this line — often a missing colon, an unmatched quote or parenthesis, or a misspelled keyword." },
  { match: /NameError: name '(\w+)' is not defined/, why: (m) =>
      `"${m[1]}" was used before it was created, or its name doesn't exactly match how it was spelled when it was created.` },
  { match: /TypeError: can only concatenate str/, why: () =>
      "You tried to join text (a string) directly with a number. Wrap the number in str(...) first, e.g. 'XP: ' + str(xp)." },
  { match: /TypeError:/, why: () =>
      "An operation was used on a type of value it doesn't support — usually mixing text and numbers without converting one of them." },
  { match: /ZeroDivisionError/, why: () =>
      "The code tried to divide a number by zero, which isn't mathematically possible." },
  { match: /IndexError/, why: () =>
      "The code tried to reach a position in a list or string that doesn't exist (the index is out of range)." },
  { match: /KeyError/, why: () =>
      "The code tried to look up a dictionary key that was never set." },
  { match: /AttributeError/, why: () =>
      "The code tried to use a method or property that doesn't exist on that value's type." },
  { match: /ModuleNotFoundError|ImportError/, why: () =>
      "The code tried to import something that isn't available in this environment." },
  { match: /ValueError/, why: () =>
      "A value had the right type but wasn't a valid value for the operation — e.g. converting text that isn't actually a number." }
];

function explainPythonError(rawError) {
  for (const entry of PY_ERROR_EXPLAINERS) {
    const m = rawError.match(entry.match);
    if (m) return entry.why(m);
  }
  return "Something in the code stopped Python from running it — compare it closely against the example above for typos or missing punctuation.";
}

// Java / C++: the teaching interpreter is regex-based and doesn't throw real
// syntax errors, so when code produces the wrong (often blank) output, this
// scans the raw source for the most common beginner mistakes and explains them.
function detectSyntaxIssues(rawCode, lang) {
  const issues = [];
  const lines = rawCode.split('\n');

  lines.forEach((rawLine, i) => {
    const lineNum = i + 1;
    const commentIdx = rawLine.indexOf('//');
    const line = (commentIdx >= 0 ? rawLine.slice(0, commentIdx) : rawLine).trim();
    if (!line) return; // blank or comment-only line

    // unmatched double quotes
    const quoteCount = (line.match(/"/g) || []).length;
    if (quoteCount % 2 !== 0) {
      issues.push(`Line ${lineNum}: there's an unmatched " — a piece of text was opened with a quote but never closed.`);
      return;
    }

    if (lang === 'java') {
      if (/^system\.out\.println/i.test(line) && !/^System\.out\.println/.test(line)) {
        issues.push(`Line ${lineNum}: Java is case-sensitive — it needs to be System.out.println, with a capital S and O.`);
      } else if (/^System\.out\.Println/.test(line)) {
        issues.push(`Line ${lineNum}: it's println with a lowercase "p", not Println.`);
      } else if (/^print\s*\(/.test(line) || /^console\.log/i.test(line)) {
        issues.push(`Line ${lineNum}: Java prints with System.out.println(...), not ${line.split('(')[0]}(...).`);
      }
    }

    if (lang === 'cpp') {
      if (/^Cout\b/.test(line) || /^COUT\b/.test(line)) {
        issues.push(`Line ${lineNum}: C++ is case-sensitive — it needs to be lowercase cout.`);
      } else if (/^print\s*\(/.test(line) || /^console\.log/i.test(line) || /^System\.out/.test(line)) {
        issues.push(`Line ${lineNum}: C++ prints with cout << ..., not ${line.split('(')[0]}(...).`);
      }
    }

    // missing semicolon on a line that clearly looks like a full statement
    const looksLikeStatement =
      /^(?:int|double|float|long|short|char|String|string|auto|bool)\s+\w+\s*=.+[^;]$/.test(line) ||
      /^\w+\s*=[^=].*[^;]$/.test(line) ||
      /^System\.out\.(?:println|print)\s*\(.*\)$/.test(line) ||
      /^cout\s*<<.*[^;]$/.test(line);
    if (looksLikeStatement && !/;\s*$/.test(line)) {
      issues.push(`Line ${lineNum} is missing a semicolon ; at the end — every statement in ${lang === 'java' ? 'Java' : 'C++'} needs one.`);
    }
  });

  // de-duplicate identical messages and cap how many we show at once
  return Array.from(new Set(issues)).slice(0, 3);
}

// ---------- extra UI injection (concept/hint/solution boxes, modal, attempts badge) ----------
// Injected at runtime so this single engine file can add the new UI to every
// course-*.html page without needing to hand-edit each one.

function injectExtraUI() {
  const exampleBox = document.getElementById('exampleBox');
  if (exampleBox && !document.getElementById('conceptBox')) {
    exampleBox.insertAdjacentHTML(
      'beforebegin',
      '<div class="block-label">Concept</div><div class="concept-box" id="conceptBox"></div>'
    );
  }

  const instructionText = document.getElementById('instructionText');
  if (instructionText && !document.getElementById('hintBox')) {
    instructionText.insertAdjacentHTML('afterend', '<div class="hint-box" id="hintBox"></div>');
  }

  const terminalBox = document.getElementById('terminalBox');
  if (terminalBox && !document.getElementById('solutionBox')) {
    terminalBox.insertAdjacentHTML('afterend', '<div class="solution-box" id="solutionBox"></div>');
  }

  const runRow = document.querySelector('.run-row');
  if (runRow && !document.getElementById('attemptsBadge')) {
    runRow.insertAdjacentHTML('beforeend', '<span class="attempts-badge" id="attemptsBadge"></span>');
  }

  if (!document.getElementById('beaconModalOverlay')) {
    document.body.insertAdjacentHTML(
      'beforeend',
      '<div class="beacon-modal-overlay" id="beaconModalOverlay">' +
        '<div class="beacon-modal-box" id="beaconModalBox">' +
          '<div class="beacon-modal-icon" id="beaconModalIcon"></div>' +
          '<div class="beacon-modal-title" id="beaconModalTitle"></div>' +
          '<div class="beacon-modal-message" id="beaconModalMessage"></div>' +
          '<div class="beacon-modal-actions" id="beaconModalActions"></div>' +
        '</div>' +
      '</div>'
    );
  }
}

function hideBeaconModal() {
  const overlay = document.getElementById('beaconModalOverlay');
  if (overlay) overlay.classList.remove('active');
}

// buttons: [{ label, className: 'primary'|'secondary', onClick }]
function showBeaconModal({ icon, title, message, tone, buttons }) {
  const overlay = document.getElementById('beaconModalOverlay');
  if (!overlay) return;

  document.getElementById('beaconModalIcon').textContent = icon || '';
  document.getElementById('beaconModalTitle').textContent = title || '';
  document.getElementById('beaconModalMessage').textContent = message || '';

  const box = document.getElementById('beaconModalBox');
  box.classList.remove('tone-danger');
  if (tone === 'danger') box.classList.add('tone-danger');

  const actions = document.getElementById('beaconModalActions');
  actions.innerHTML = '';
  (buttons || []).forEach((b) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'beacon-modal-btn ' + (b.className || 'secondary');
    btn.textContent = b.label;
    btn.addEventListener('click', () => {
      hideBeaconModal();
      if (b.onClick) b.onClick();
    });
    actions.appendChild(btn);
  });

  overlay.classList.add('active');
}

function escapeHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function updateAttemptsBadge() {
  const badge = document.getElementById('attemptsBadge');
  if (!badge) return;
  badge.textContent = currentAttempts > 0
    ? `Attempts: ${Math.min(currentAttempts, GAMEOVER_THRESHOLD)}/${GAMEOVER_THRESHOLD}`
    : '';
}

function revealHint(lesson) {
  const hintBox = document.getElementById('hintBox');
  if (hintBox && lesson.hint) {
    hintBox.textContent = '💡 HINT: ' + lesson.hint;
    hintBox.classList.add('show');
  }
  hintShownForCurrent = true;
  playSound('click');
}

function revealSolution(lesson) {
  const langKey = BEACON_LESSONS.langKey;
  markNoXp(langKey, lesson.id);

  const solutionBox = document.getElementById('solutionBox');
  if (solutionBox && lesson.solution) {
    solutionBox.innerHTML =
      '<div class="solution-label">SOLUTION — no XP for this lesson</div>' +
      '<pre>' + escapeHtml(lesson.solution) + '</pre>';
    solutionBox.classList.add('show');
  }
  solutionShownForCurrent = true;
}

function registerFailedAttempt(lesson) {
  currentAttempts += 1;
  updateAttemptsBadge();

  const langKey = BEACON_LESSONS.langKey;

  if (currentAttempts === HINT_THRESHOLD && !hintShownForCurrent && !isNoXp(langKey, lesson.id)) {
    showBeaconModal({
      icon: '🤔',
      title: 'STUCK?',
      message: `You've tried ${HINT_THRESHOLD} times. Would you like a hint?`,
      buttons: [
        { label: 'Show Hint', className: 'primary', onClick: () => revealHint(lesson) },
        { label: 'Keep Trying', className: 'secondary', onClick: () => playSound('click') }
      ]
    });
  }

  if (currentAttempts === GAMEOVER_THRESHOLD && !solutionShownForCurrent) {
    revealSolution(lesson);
    playSound('error');
    showBeaconModal({
      icon: '💀',
      title: 'GAME OVER',
      message: `Better luck next time! The solution has been revealed below the terminal — no XP will be earned for this lesson.`,
      tone: 'danger',
      buttons: [
        { label: 'Continue', className: 'primary', onClick: () => playSound('click') }
      ]
    });
  }
}

// ---------- Boss Fight: storage ----------

function bossStateKey(langKey) {
  return 'beaconBossState:' + langKey;
}

function saveBossState() {
  try {
    sessionStorage.setItem(
      bossStateKey(BEACON_LESSONS.langKey),
      JSON.stringify({ index: bossIndex, answers: bossAnswers })
    );
  } catch (e) { /* ignore */ }
}

function loadBossState() {
  try {
    const raw = sessionStorage.getItem(bossStateKey(BEACON_LESSONS.langKey));
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}

function clearBossState() {
  try {
    sessionStorage.removeItem(bossStateKey(BEACON_LESSONS.langKey));
  } catch (e) { /* ignore */ }
}

function loadBossBest() {
  try {
    return JSON.parse(localStorage.getItem('beaconBossBest') || '{}');
  } catch (e) {
    return {};
  }
}

function saveBossBest(obj) {
  try {
    localStorage.setItem('beaconBossBest', JSON.stringify(obj));
  } catch (e) { /* ignore */ }
}

function getBossBestXp(langKey) {
  return loadBossBest()[langKey] || 0;
}

function setBossBestXp(langKey, xp) {
  const best = loadBossBest();
  best[langKey] = xp;
  saveBossBest(best);
}

// ---------- Boss Fight: UI injection ----------

function injectBossFightUI() {
  const nav = document.querySelector('.quest-nav');
  if (nav && !document.getElementById('bossFightBtn')) {
    nav.insertAdjacentHTML(
      'beforeend',
      '<button type="button" class="boss-fight-btn" id="bossFightBtn">&#128128; Boss Fight</button>'
    );
  }
  if (!document.getElementById('bossOverlay')) {
    document.body.insertAdjacentHTML('beforeend', BOSS_OVERLAY_HTML);
  }
}

function showBossPanel(name) {
  ['bossIntro', 'bossQuiz', 'bossPauseScreen', 'bossResultScreen'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.classList.remove('active');
  });
  const map = { intro: 'bossIntro', quiz: 'bossQuiz', pause: 'bossPauseScreen', result: 'bossResultScreen' };
  const target = document.getElementById(map[name]);
  if (target) target.classList.add('active');
}

// ---------- Boss Fight: flow ----------

function openBossFight() {
  playSound('click');

  const bank = (typeof BEACON_BOSS !== 'undefined' && BEACON_BOSS.langKey === BEACON_LESSONS.langKey)
    ? BEACON_BOSS.questions
    : [];
  if (!bank.length) return;
  bossQuestions = bank;

  const overlay = document.getElementById('bossOverlay');
  overlay.classList.add('active');

  const saved = loadBossState();
  if (saved && Array.isArray(saved.answers) && saved.answers.length < bossQuestions.length) {
    bossIndex = saved.index;
    bossAnswers = saved.answers;
    showBossPanel('quiz');
    renderBossQuestion();
    return;
  }

  bossIndex = 0;
  bossAnswers = [];
  showBossPanel('intro');

  setTimeout(() => {
    showBossPanel('quiz');
    renderBossQuestion();
  }, 2200);
}

function closeBossFight() {
  const overlay = document.getElementById('bossOverlay');
  if (overlay) overlay.classList.remove('active');
}

function renderBossQuestion() {
  const q = bossQuestions[bossIndex];
  document.getElementById('bossProgress').textContent = `Question ${bossIndex + 1} / ${bossQuestions.length}`;

  const resultMsg = document.getElementById('bossResultMsg');
  resultMsg.textContent = '';
  resultMsg.className = 'boss-result-msg';

  const box = document.getElementById('bossQuestionBox');

  if (q.type === 'debug') {
    box.innerHTML =
      '<div class="boss-q-tag">DEBUG CHALLENGE</div>' +
      '<div class="boss-q-prompt">' + escapeHtml(q.prompt) + '</div>' +
      '<pre class="boss-q-code">' + escapeHtml(q.code) + '</pre>' +
      '<div class="boss-q-options" id="bossOptions"></div>';

    const optWrap = document.getElementById('bossOptions');
    q.options.forEach((opt) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'boss-option-btn';
      btn.textContent = opt.text;
      btn.dataset.optId = opt.id;
      btn.addEventListener('click', () => {
        optWrap.querySelectorAll('.boss-option-btn').forEach((el) => el.classList.remove('selected'));
        btn.classList.add('selected');
        optWrap.dataset.selected = opt.id;
      });
      optWrap.appendChild(btn);
    });
  } else {
    box.innerHTML =
      '<div class="boss-q-tag">CODE CHALLENGE</div>' +
      '<div class="boss-q-prompt">' + escapeHtml(q.prompt) + '</div>' +
      '<textarea class="code-editor boss-q-editor" id="bossCodeEditor" spellcheck="false">' +
      escapeHtml(q.starter || '') + '</textarea>' +
      '<div class="terminal-box" id="bossTerminal">[TERMINAL OUTPUT] Press \'Submit Answer\' to run your code...</div>';
  }
}

async function handleBossSubmit() {
  const q = bossQuestions[bossIndex];
  const resultMsg = document.getElementById('bossResultMsg');
  const submitBtn = document.getElementById('bossSubmitBtn');
  playSound('click');

  let correct = false;

  if (q.type === 'debug') {
    const optWrap = document.getElementById('bossOptions');
    const selected = optWrap ? optWrap.dataset.selected : null;
    if (!selected) {
      resultMsg.textContent = 'Pick an answer first.';
      resultMsg.className = 'boss-result-msg fail';
      return;
    }
    correct = selected === q.correctOptionId;
  } else {
    submitBtn.disabled = true;
    const code = document.getElementById('bossCodeEditor').value;
    const term = document.getElementById('bossTerminal');
    term.className = 'terminal-box';
    term.textContent = 'Running…';

    let output = '', error = null;
    if (BEACON_LESSONS.langKey === 'python') {
      const res = await runPython(code, (msg) => { term.textContent = msg; });
      output = res.output;
      error = res.error;
    } else {
      try {
        output = runMiniInterpreter(code, BEACON_LESSONS.langKey);
      } catch (e) {
        error = String(e);
      }
    }
    submitBtn.disabled = false;

    if (error) {
      term.className = 'terminal-box fail';
      if (BEACON_LESSONS.langKey === 'python') {
        term.textContent = error + '\n\n💡 Why: ' + explainPythonError(error);
      } else {
        term.textContent = error;
      }
      correct = false;
    } else {
      correct = outputMatches(output, q.expected);
      if (!correct && BEACON_LESSONS.langKey !== 'python') {
        const issues = detectSyntaxIssues(code, BEACON_LESSONS.langKey);
        if (issues.length > 0) {
          term.className = 'terminal-box fail';
          term.textContent =
            (output.trim() ? output.trim() + '\n\n' : '') +
            '⚠ Possible issue(s) found:\n' + issues.map((m) => '- ' + m).join('\n');
        } else {
          term.textContent = output.trim() || '(no output)';
          term.className = 'terminal-box fail';
        }
      } else {
        term.textContent = output.trim() || '(no output)';
        term.className = 'terminal-box ' + (correct ? 'pass' : 'fail');
      }
    }
  }

  bossAnswers.push({ id: q.id, correct: correct });
  bossIndex += 1;
  saveBossState();

  resultMsg.textContent = correct ? '✓ Correct!' : '✗ Incorrect.';
  resultMsg.className = 'boss-result-msg ' + (correct ? 'pass' : 'fail');
  playSound(correct ? 'success' : 'error');

  setTimeout(() => {
    if (bossIndex < bossQuestions.length) {
      renderBossQuestion();
    } else {
      finishBossFight();
    }
  }, 900);
}

function finishBossFight() {
  const total = bossQuestions.length;
  const correctCount = bossAnswers.filter((a) => a.correct).length;
  const langKey = BEACON_LESSONS.langKey;

  let tierXp, title, sub, icon, tone;
  if (correctCount === total) {
    tierXp = 50;
    title = 'MISSION ACCOMPLISHED';
    sub = 'Flawless victory — every challenge cleared!';
    icon = '🏆';
    tone = 'victory';
  } else if (correctCount >= Math.ceil(total / 2)) {
    tierXp = 30;
    title = 'SEE YOU SOON';
    sub = `${correctCount}/${total} correct — a solid run, but the boss lives on.`;
    icon = '🛡️';
    tone = 'partial';
  } else {
    tierXp = 0;
    title = 'MISSION FAILED';
    sub = `${correctCount}/${total} correct — regroup and try again.`;
    icon = '💀';
    tone = 'fail';
  }

  const best = getBossBestXp(langKey);
  let gainedXp = 0;
  if (tierXp > best) {
    gainedXp = tierXp - best;
    if (gainedXp > 0) {
      const player = loadPlayer();
      player.xp = (player.xp || 0) + gainedXp;
      savePlayer(player);
      updateHudXp();
    }
    setBossBestXp(langKey, tierXp);
  }

  clearBossState();

  document.getElementById('bossResultIcon').textContent = icon;
  const titleEl = document.getElementById('bossResultTitle');
  titleEl.textContent = title;
  titleEl.className = 'boss-result-title tone-' + tone;
  document.getElementById('bossResultSub').textContent = sub;
  document.getElementById('bossResultXp').textContent = gainedXp > 0
    ? `+${gainedXp} XP`
    : (tierXp > 0 ? 'Personal best already reached — no extra XP' : 'No XP earned');

  showBossPanel('result');
  playSound(tierXp === 50 ? 'achievement' : (tierXp === 30 ? 'success' : 'error'));
}

function initBossFightControls() {
  const fightBtn = document.getElementById('bossFightBtn');
  if (fightBtn) fightBtn.addEventListener('click', openBossFight);

  const submitBtn = document.getElementById('bossSubmitBtn');
  if (submitBtn) submitBtn.addEventListener('click', handleBossSubmit);

  const pauseBtn = document.getElementById('bossPauseBtn');
  if (pauseBtn) pauseBtn.addEventListener('click', () => {
    playSound('click');
    showBossPanel('pause');
  });

  const resumeBtn = document.getElementById('bossResumeBtn');
  if (resumeBtn) resumeBtn.addEventListener('click', () => {
    playSound('click');
    showBossPanel('quiz');
  });

  const quitBtn = document.getElementById('bossQuitBtn');
  if (quitBtn) quitBtn.addEventListener('click', () => {
    playSound('click');
    clearBossState();
    closeBossFight();
  });

  const closeBtn = document.getElementById('bossCloseBtn');
  if (closeBtn) closeBtn.addEventListener('click', () => {
    playSound('click');
    closeBossFight();
  });
}

// ---------- rendering ----------

function getSection(key) {
  return BEACON_LESSONS.sections.find((s) => s.key === key);
}

function renderSectionOptions() {
  const select = document.getElementById('sectionSelect');
  select.innerHTML = '';
  BEACON_LESSONS.sections.forEach((sec) => {
    const opt = document.createElement('option');
    opt.value = sec.key;
    opt.textContent = sec.label;
    if (sec.locked) opt.disabled = true;
    select.appendChild(opt);
  });
  select.value = currentSectionKey;
}

function renderLessonList() {
  const section = getSection(currentSectionKey);
  const list = document.getElementById('lessonList');
  list.innerHTML = '';
  section.lessons.forEach((lesson, idx) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'lesson-item';
    if (idx === currentLessonIndex) btn.classList.add('active');
    if (isLessonDone(BEACON_LESSONS.langKey, lesson.id)) btn.classList.add('done');
    btn.textContent = `${lesson.id}: ${lesson.title}`;
    btn.addEventListener('click', () => {
      playSound('click');
      currentLessonIndex = idx;
      renderLesson();
      renderLessonList();
    });
    list.appendChild(btn);
  });
}

function renderLesson() {
  const section = getSection(currentSectionKey);
  const lesson = section.lessons[currentLessonIndex];
  const langKey = BEACON_LESSONS.langKey;

  document.getElementById('questTitle').textContent =
    `[ ${BEACON_LESSONS.langLabel.toUpperCase()} ARCADE QUEST ]`;
  document.getElementById('lessonHeading').innerHTML =
    `${lesson.title} <span class="xp-tag">(+${lesson.xp} XP)</span>`;

  const conceptBox = document.getElementById('conceptBox');
  if (conceptBox) conceptBox.textContent = lesson.concept || '';

  document.getElementById('exampleBox').textContent = lesson.example;
  document.getElementById('instructionText').textContent = lesson.instruction;
  document.getElementById('codeEditor').value = lesson.starter;

  const term = document.getElementById('terminalBox');
  term.className = 'terminal-box';
  term.textContent = "[TERMINAL OUTPUT] Press 'EXECUTE CODE' to verify response...";

  document.getElementById('resultMsg').textContent = '';
  document.getElementById('resultMsg').className = 'result-msg';
  document.getElementById('nextBtn').classList.remove('show');
  document.getElementById('runBtn').disabled = false;

  // reset per-lesson attempt/hint/solution state for this visit
  currentAttempts = 0;
  hintShownForCurrent = false;
  solutionShownForCurrent = false;
  updateAttemptsBadge();

  const hintBox = document.getElementById('hintBox');
  if (hintBox) { hintBox.textContent = ''; hintBox.classList.remove('show'); }

  const solutionBox = document.getElementById('solutionBox');
  if (solutionBox) { solutionBox.innerHTML = ''; solutionBox.classList.remove('show'); }

  // if this lesson's solution was already revealed in a previous visit, show it again
  if (isNoXp(langKey, lesson.id)) {
    revealSolution(lesson);
  }
}

// ---------- XP + completion ----------

function awardXp(lesson) {
  const langKey = BEACON_LESSONS.langKey;
  const alreadyDone = isLessonDone(langKey, lesson.id);
  const blocked = isNoXp(langKey, lesson.id);

  if (!alreadyDone && !blocked) {
    const player = loadPlayer();
    player.xp = (player.xp || 0) + lesson.xp;
    savePlayer(player);
    markLessonDone(langKey, lesson.id);
    updateHudXp();
    playSound('xpGain');
    return lesson.xp;
  }

  if (!alreadyDone && blocked) {
    // still mark it complete so it shows a checkmark, but no XP is granted
    markLessonDone(langKey, lesson.id);
  }

  return 0;
}

// ---------- run button ----------

async function handleRun() {
  playSound('click');

  const section = getSection(currentSectionKey);
  const lesson = section.lessons[currentLessonIndex];
  const code = document.getElementById('codeEditor').value;
  const term = document.getElementById('terminalBox');
  const runBtn = document.getElementById('runBtn');
  const resultMsg = document.getElementById('resultMsg');

  runBtn.disabled = true;
  term.className = 'terminal-box';
  term.textContent = 'Running…';
  resultMsg.textContent = '';
  resultMsg.className = 'result-msg';

  let output = '';
  let error = null;

  if (BEACON_LESSONS.langKey === 'python') {
    const res = await runPython(code, (msg) => { term.textContent = msg; });
    output = res.output;
    error = res.error;
  } else {
    try {
      output = runMiniInterpreter(code, BEACON_LESSONS.langKey);
    } catch (e) {
      error = String(e);
    }
  }

  runBtn.disabled = false;

  if (error) {
    term.className = 'terminal-box fail';
    if (BEACON_LESSONS.langKey === 'python') {
      const why = explainPythonError(error);
      term.textContent = error + '\n\n💡 Why: ' + why;
      resultMsg.textContent = '✗ Error — ' + why;
    } else {
      term.textContent = error;
      resultMsg.textContent = "✗ Error — check your code and try again.";
    }
    resultMsg.className = 'result-msg fail';
    playSound('error');
    registerFailedAttempt(lesson);
    return;
  }

  const pass = outputMatches(output, lesson.expected);

  if (!pass && BEACON_LESSONS.langKey !== 'python') {
    const issues = detectSyntaxIssues(code, BEACON_LESSONS.langKey);
    if (issues.length > 0) {
      term.className = 'terminal-box fail';
      term.textContent =
        (output.trim() ? output.trim() + '\n\n' : '') +
        '⚠ Possible issue(s) found:\n' + issues.map((m) => '- ' + m).join('\n');
      resultMsg.textContent = '✗ Error — ' + issues[0];
      resultMsg.className = 'result-msg fail';
      playSound('error');
      registerFailedAttempt(lesson);
      return;
    }
  }

  term.textContent = output.trim() || '(no output)';

  if (pass) {
    term.className = 'terminal-box pass';
    const gained = awardXp(lesson); // plays 'xpGain' internally if XP was newly awarded
    const blocked = isNoXp(BEACON_LESSONS.langKey, lesson.id);

    if (gained > 0) {
      resultMsg.textContent = `✓ Correct! +${gained} XP`;
    } else if (blocked) {
      resultMsg.textContent = '✓ Correct! (solution was revealed — no XP)';
    } else {
      resultMsg.textContent = '✓ Correct! (already completed — no extra XP)';
    }
    resultMsg.className = 'result-msg pass';
    renderLessonList();

    if (gained === 0) playSound('success'); // still confirm correctness even with no new XP

    const isLast = currentLessonIndex === section.lessons.length - 1;
    const nextBtn = document.getElementById('nextBtn');
    if (!isLast) {
      nextBtn.textContent = 'Next Lesson ▶';
      nextBtn.classList.add('show');
    } else {
      nextBtn.classList.remove('show');
      resultMsg.textContent += ' — Section complete!';
      playSound('achievement'); // section-complete gets the bigger fanfare
    }
  } else {
    term.className = 'terminal-box fail';
    resultMsg.textContent = "✗ Not quite — check the expected output and try again.";
    resultMsg.className = 'result-msg fail';
    playSound('error');
    registerFailedAttempt(lesson);
  }
}

// ---------- init ----------

function initQuest() {
  injectExtraUI();
  injectBossFightUI();
  initBossFightControls();

  currentSectionKey = BEACON_LESSONS.sections[0].key;
  currentLessonIndex = 0;

  renderSectionOptions();
  renderLessonList();
  renderLesson();
  updateHudXp();

  const player = loadPlayer();
  if (player.username) {
    const el = document.getElementById('hudPlayer');
    if (el) el.textContent = player.username.toUpperCase();
  }

  document.getElementById('sectionSelect').addEventListener('change', (e) => {
    const sec = getSection(e.target.value);
    if (sec.locked) {
      e.target.value = currentSectionKey; // revert
      return;
    }
    playSound('click');
    currentSectionKey = e.target.value;
    currentLessonIndex = 0;
    renderLessonList();
    renderLesson();
  });

  document.getElementById('runBtn').addEventListener('click', handleRun);

  document.getElementById('nextBtn').addEventListener('click', () => {
    playSound('click');
    currentLessonIndex += 1;
    renderLesson();
    renderLessonList();
  });

  // Tab key inserts an indent instead of moving focus out of the editor
  document.getElementById('codeEditor').addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const el = e.target;
      const start = el.selectionStart, end = el.selectionEnd;
      el.value = el.value.slice(0, start) + '    ' + el.value.slice(end);
      el.selectionStart = el.selectionEnd = start + 4;
    }
  });

  // Arrived here via a "Boss Fight" button on the home page? Jump straight in.
  try {
    const params = new URLSearchParams(window.location.search);
    if (params.get('boss') === '1') {
      // strip the query param so a manual refresh doesn't keep relaunching it
      const cleanUrl = window.location.pathname + window.location.hash;
      window.history.replaceState({}, '', cleanUrl);
      setTimeout(openBossFight, 200);
    }
  } catch (e) { /* ignore — URLSearchParams unsupported or blocked */ }
}

document.addEventListener('DOMContentLoaded', initQuest);
