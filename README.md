[README.md](https://github.com/user-attachments/files/32142239/README.md)<img width="1400" height="900" alt="profile" src="https://github.com/user-attachments/assets/6e1dd7dd-a6e1-405e-829f-54498c7bb081" />
<img width="1400" height="900" alt="login" src="https://github.com/user-attachments/assets/d981e315-bf5f-4f1c-b348-abf0e060c050" />
<img width="1400" height="900" alt="hub" src="https://github.com/user-attachments/assets/2e418b3c-d076-4141-93df-d6219bf5eb9b" />
<img width="1400" height="900" alt="home" src="https://github.com/user-attachments/assets/0228c38b-511e-47b6-a0ac-0fb2a48db35e" />
<img width="1400" height="900" alt="course-python" src="https://github.com/user-attachments/assets/278ba01f-5d5a-4f98-87c5-f0ae4d26f6bd" />
<img width="1400" height="900" alt="theater" src="https://github.com/user-attachments/assets/ff0ce250-f293-4414-98b5-b01a6b943208" />
<img width="1400" height="900" alt="signup" src="https://github.com/user-attachments/assets/10351056-285a-4879-b844-72f20d9cfa52" />
<img width="1400" height="900" alt="settings" src="https://github.com/user-attachments/assets/e4b738bd-0283-45f3-a89c-05ea26b7fb4a" />

# 🕹️ BEACON — Gamified Coding Learning Platform

BEACON teaches **Python, Java, and C++** through bite-sized terminal quests, real code execution, boss-fight quizzes, XP/leveling, and a curated video theater — wrapped in a retro synthwave/arcade aesthetic.

The project exists in **two forms**:

| | **Web App** | **Desktop App** |
|---|---|---|
| Stack | HTML / CSS / vanilla JS | Python + Tkinter (`beaconapp.py`) |
| Persistence | Browser `localStorage` | Local `beacon_users.json` file |
| Code execution | Pyodide (Python), regex-based checker (Java/C++) | Real `python exec()`, real `g++` / `javac`+`java` subprocess calls, with a regex fallback if no compiler is installed |
| Runs on | Any browser, no install | Any machine with Python + Tkinter (+ optional GCC/JDK) |

---

## 📸 Screenshots (Web App)

**Login**
<img width="1902" height="906" alt="image" src="https://github.com/user-attachments/assets/fdea9d68-2304-416d-acea-6761501f8afa" />

**Sign Up**
<img width="1900" height="907" alt="image" src="https://github.com/user-attachments/assets/e2de81c7-1671-450a-acd7-548da7914ff4" />

**Home — Quest Selection**
<img width="1901" height="907" alt="image" src="https://github.com/user-attachments/assets/3b0b8e5a-f78f-4880-9361-f7d9f18e7676" />

**Python Quest — Terminal Code Editor**
<img width="1900" height="908" alt="image" src="https://github.com/user-attachments/assets/94211e3a-0c87-461e-83f4-e915f264a4ae" />

**Player Profile**
<img width="1917" height="903" alt="image" src="https://github.com/user-attachments/assets/5442810a-8879-4135-910c-813521076e75" />

**Guild & FAQ Hub**
<img width="1897" height="911" alt="image" src="https://github.com/user-attachments/assets/4c7c8b99-0122-40a2-9826-e779ae13dba8" />

**Video Theater**
<img width="1896" height="911" alt="image" src="https://github.com/user-attachments/assets/6b62c232-4548-40ed-98cf-f9123033909b" />

**Settings**
****<img width="1900" height="907" alt="image" src="https://github.com/user-attachments/assets/6731466a-b0d6-4a0f-8b65-baf7258c827e" />
<img width="1637" height="722" alt="image" src="https://github.com/user-attachments/assets/b558716d-4106-4de6-86b9-3a762d43c974" />
<img width="1897" height="772" alt="image" src="https://github.com/user-attachments/assets/e6620f57-c5d0-4935-ab1f-35a2e6aaa1e7" />


> Screenshots were captured directly from the static site (`file://` render); the pixel-art lighthouse/sky background images referenced in `styles.css` aren't included in this repo, so the login/signup beam effect renders on a plain dark background here. The desktop app has no screenshots included since it requires a local Tkinter environment to run — see the code walkthrough below instead.

---

## 🌐 Part 1 — The Web App

A fully static site. No build step, no backend — everything lives in the browser.

### File Structure

```
beacon-web/
├── index.html / login.js / login.css     # Login page
├── signup.html / script.js               # Sign-up page (avatar photo upload, validation)
├── styles.css                            # Shared login/signup background (lighthouse scene)
│
├── home.html / home.js / home.css        # Dashboard — pick a quest language
├── hub.html / hub.js / hub.css           # Guild "About", FAQ, Feedback panels
├── profile.html / profile.js / profile.css   # XP, stats, badges
├── settings.html / settings.js / settings.css # Preferences + "Full Beam" upsell
├── theater.html / theater.js / theater.css / theater-data.js  # Video library
│
├── course-python.html / course-java.html / course-cpp.html    # Quest pages
├── course.css / course-engine.js         # Shared quest engine + boss fight logic
├── lessons-python.js / lessons-java.js / lessons-cpp.js        # Lesson + boss content
│
├── arcade-bg.css                         # Shared animated starfield/grid background
├── sfx.js                                # Shared sound effects manager
└── quest-loading-transition.html         # Standalone prototype (not linked into the live site)
```

### Key snippet — the in-browser code checker

`course-engine.js` runs Python for real via Pyodide, but Java/C++ have no compiler in the browser, so a lightweight interpreter checks output instead:

```javascript
// course-engine.js — simplified excerpt of the output verification flow
async function runCode(code) {
  if (currentLang === 'python') {
    const pyodide = await ensurePyodide();
    try {
      let output = '';
      pyodide.setStdout({ batched: (s) => (output += s + '\n') });
      await pyodide.runPythonAsync(code);
      return { output: output.trim(), error: null };
    } catch (err) {
      return { output: '', error: describePythonError(err) }; // plain-English hint
    }
  }
  // Java / C++: regex-based interpreter — checks print/cout statements,
  // variables, and basic math against the lesson's expected output.
  return runSimplifiedInterpreter(code, currentLang);
}
```

### Key snippet — avatar assignment at signup

```javascript
// script.js — a random avatar is picked once at signup and persisted
const avatarPool = [
  { emoji: '🧙', color: '#8b6bff' },
  { emoji: '🥷', color: '#9aa3d1' },
  { emoji: '🦸', color: '#ff3864' },
  { emoji: '🤖', color: '#35e0ff' },
  // ...
];
const avatar = avatarPool[Math.floor(Math.random() * avatarPool.length)];

localStorage.setItem('beaconPlayer', JSON.stringify({
  username: username.value.trim(),
  grade: grade.value,
  experience: experience.value,
  avatar: avatar.emoji,
  avatarColor: avatar.color
}));
```

### Running the Web App

```bash
git clone <your-repo-url>
cd beacon-web
python3 -m http.server 8000
# visit http://localhost:8000
```

> ⚠️ Keep every file in one flat folder — splitting into subfolders (e.g. `CSS/`, `JS/`) breaks the relative `<link>`/`<script>` paths unless you update them too.

### Web App Data Model (`localStorage`)

| Key | Stores |
|---|---|
| `beaconPlayer` | Username, grade, difficulty, avatar, XP, uploaded photo |
| `beaconSettings` | Sound / dark mode / email toggles, streak-freeze usage |
| `beaconWatched` | Which Video Theater entries are marked complete |

---

## 🖥️ Part 2 — The Desktop App (`beaconapp.py`)

A single-file Tkinter recreation of Beacon as a native desktop application — same curriculum and gamification concepts, rebuilt with hand-drawn canvas UI (no web view involved).

### Requirements

```bash
pip install pillow
# Optional, for real compiled execution instead of the regex fallback:
#   g++  (C++)      — from a standard build-tools install (e.g. MinGW, build-essential)
#   javac + java     — from a JDK
```

Python's `tkinter` module ships with most standard Python installs (on some Linux distros install it separately, e.g. `sudo apt install python3-tk`).

### Run it

```bash
python3 beaconapp.py
```

### Architecture at a Glance

`BeaconApp` (a `tk.Tk` subclass) builds every page once at startup and swaps between them with `.tkraise()` — a classic Tkinter multi-page pattern:

```python
class BeaconApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BEACON - Gamified Education Arcade & Video Theater")
        self.geometry("920x730")

        self.user_profile = {
            "name": "PLAYER 1", "xp": 0, "streak": 1,
            "watched_videos": set(), "membership": "free"
        }

        self.frames = {}
        pages = (
            LoginPage, SignupPage, ProgramSelectionPage, ArcadeLessonsPage,
            PythonQuestPage, JavaQuestPage, CppQuestPage,
            ProfilePage, SettingsPage, FeedbackPage, AboutUsPage, MonetizationPage
        )
        for PageClass in pages:
            frame = PageClass(parent=container, controller=self)
            self.frames[PageClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()
```

### Key snippet — real compiled execution (a step up from the web version)

Unlike the web app's regex-only checker, the desktop app actually **compiles and runs** C++ and Java through the system toolchain when available, falling back to the same kind of lightweight interpreter only if `g++`/`javac` aren't installed:

```python
def execute_terminal_code(self, code_str):
    if self.lang_name == "Python":
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            exec(code_str, {"__builtins__": __builtins__})
            return buffer.getvalue().strip(), None
        except Exception as e:
            return "", str(e)
        finally:
            sys.stdout = sys.__stdout__

    elif self.lang_name == "C++":
        with tempfile.TemporaryDirectory() as tmpdir:
            cpp_file, exe_file = os.path.join(tmpdir, "solution.cpp"), os.path.join(tmpdir, "solution.exe")
            open(cpp_file, "w").write(code_str)
            compile_res = subprocess.run(["g++", cpp_file, "-o", exe_file], capture_output=True, text=True, timeout=5)
            if compile_res.returncode != 0:
                return "", compile_res.stderr.strip()
            run_res = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
            return run_res.stdout.strip(), (run_res.stderr.strip() or None)
    # ...Java follows the same compile-then-run pattern with javac/java
```

### Key snippet — synthesized retro sound effects (no audio files needed)

```python
class RetroSoundManager:
    """Generates authentic 8-bit retro arcade sound effects without external audio files."""
    def play_success(self):
        """3-tone fanfare on stage complete or quest cleared."""
        if not self.enabled or winsound is None:
            return
        def _fanfare():
            winsound.Beep(523, 50)   # C5
            winsound.Beep(659, 50)   # E5
            winsound.Beep(784, 100)  # G5
        threading.Thread(target=_fanfare, daemon=True).start()
```

Sounds are generated with Windows' `winsound.Beep()` on a background thread (so the UI never blocks), and no-op gracefully on non-Windows platforms.

### Key snippet — async YouTube thumbnail caching

The desktop Video Theater fetches and disk-caches YouTube thumbnails off the main thread so scrolling the video list never stutters:

```python
def fetch_image_from_url(url, size=(70, 70)):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=4) as response:
        data = response.read()
    image = Image.open(io.BytesIO(data)).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)
```
(Wrapped by `ThumbnailManager`, which handles threading and an on-disk cache so each thumbnail is only downloaded once.)

### Key snippet — user persistence

No database — user profiles are read/written straight to a JSON file next to the script:

```python
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "beacon_users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
```

### Desktop App Page Map

| Page class | Purpose |
|---|---|
| `LoginPage` / `SignupPage` | Auth, backed by `beacon_users.json` |
| `ProgramSelectionPage` | Pick a language track |
| `ArcadeLessonsPage`, `PythonQuestPage`, `JavaQuestPage`, `CppQuestPage` | The quest/lesson terminal per language |
| `ArcadeVideoTheater` | Curated video library with cached thumbnails |
| `ProfilePage` | XP, streak, stats |
| `SettingsPage` | Sound / theme / difficulty preferences |
| `FeedbackPage` | In-app feedback form |
| `AboutUsPage` | Dev Guild credits |
| `MonetizationPage` (+ `CheckoutDialog`, `ReceiptDialog`) | "Full Beam" plan picker mockup |

---

## ⚠️ Known Limitations / Placeholders (both versions)

- **Login streaks** are placeholders — day-to-day tracking isn't fully live.
- **Badges** are a visual preview; unlock logic isn't wired up yet.
- **"Full Beam" premium tier** (web settings upsell, desktop `MonetizationPage`) is a UI mockup — no real payment processor is connected in either version.
- **Java/C++ checking** without a real compiler (web always, desktop only if `g++`/`javac` are missing) is pattern-based and only covers what the current lessons teach — it is not a full language implementation.
- `quest-loading-transition.html` is a standalone prototype, not linked into the live web site's navigation.

---

## 👥 Credits

Built by the Beacon Dev Guild:
- **Srijan Chattoraj** — Team Lead / App Dev
- **Daniel Marcelo** — Design Lead / App Dev
- **Shreshth Kumar Singh** — Main Web Dev
- **Anoushka Chaturvedi** — Web Dev
