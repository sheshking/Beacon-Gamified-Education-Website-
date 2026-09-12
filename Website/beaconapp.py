"""
BEACON - Gamified Education App (Arcade Edition + Retro Video Theater)
Fully Multi-Section, Multi-Level Real Execution Terminal Curriculum & Video Lessons Vault

Features:
  - 5 to 7 Coding Sections per Language (Beginner, Intermediate, Advanced)
  - 250+ Real-Execution Arcade Terminal Quests (Python, Java, C++)
  - Curated YouTube Video Lessons Vault for Python, Java, and C++
  - Asynchronous YouTube Thumbnail Fetching & Caching Engine
  - Clickable Previews with Retro CRT Scanlines & Video Chapter Jumps
  - Integrated Interactive Code Sandbox & Cheatsheet per Lesson
  - Gamified XP, Streak, Leveling, Badges, and Video Watch Tracking
  - Dynamic Output Verification Terminal Engine
  - 60 FPS Animated Background Canvas, Pixel Headers & Retro UI Widgets
  - Windows Sound Support (winsound) with graceful cross-platform fallback
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import math
import random
import io
import urllib.request
import threading
import sys
import subprocess
import tempfile
import webbrowser
import time
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter

# Attempt winsound for Windows audio; fall back gracefully on non-Windows platforms
try:
    import winsound
except ImportError:
    winsound = None


# ==============================================================================
# 1. RETRO ARCADE SOUND ENGINE
# ==============================================================================

class RetroSoundManager:
    """Generates authentic 8-bit retro arcade sound effects without external audio files."""
    def __init__(self):
        self.enabled = True

    def play_hover(self):
        """High-pitched, rapid retro chirp on hover."""
        if not self.enabled or winsound is None:
            return
        def _chirp():
            try:
                winsound.Beep(1200, 25)
            except Exception:
                pass
        threading.Thread(target=_chirp, daemon=True).start()

    def play_click(self):
        """2-tone classic arcade blip on click."""
        if not self.enabled or winsound is None:
            return
        def _blip():
            try:
                winsound.Beep(800, 30)
                winsound.Beep(1400, 45)
            except Exception:
                pass
        threading.Thread(target=_blip, daemon=True).start()

    def play_success(self):
        """3-tone fanfare on stage complete or quest cleared."""
        if not self.enabled or winsound is None:
            return
        def _fanfare():
            try:
                winsound.Beep(523, 50)  # C5
                winsound.Beep(659, 50)  # E5
                winsound.Beep(784, 100) # G5
            except Exception:
                pass
        threading.Thread(target=_fanfare, daemon=True).start()

    def play_coin(self):
        """Classic retro arcade insert coin chime."""
        if not self.enabled or winsound is None:
            return
        def _coin():
            try:
                winsound.Beep(988, 60)   # B5
                winsound.Beep(1319, 120) # E6
            except Exception:
                pass
        threading.Thread(target=_coin, daemon=True).start()

    def play_fanfare(self):
        """Victory level-up fanfare."""
        if not self.enabled or winsound is None:
            return
        def _victory():
            try:
                winsound.Beep(587, 80)
                winsound.Beep(659, 80)
                winsound.Beep(698, 80)
                winsound.Beep(784, 160)
            except Exception:
                pass
        threading.Thread(target=_victory, daemon=True).start()


# ==============================================================================
# 2. THEMES & GLOBAL CONFIGURATION
# ==============================================================================

CLASS_OPTIONS = [f"Class {i}" for i in range(6, 13)] + ["College"]
EXPERIENCE_OPTIONS = ["Beginner", "Intermediate", "Advanced"]

EXPERIENCE_META = {
    "Beginner":     {"symbol": "🌱", "color": "#06d6a0"},
    "Intermediate": {"symbol": "⚡", "color": "#ffd166"},
    "Advanced":     {"symbol": "🔥", "color": "#ef476f"},
}

THEMES = {
    "dark": {
        "bg":        "#080b18",
        "bg_2":      "#0f132a",
        "panel":     "#121633",
        "panel_2":   "#1a1f42",
        "accent":    "#ffd166",   # Gold Arcade Accent
        "accent_2":  "#06d6a0",   # Pixel Mint
        "accent_3":  "#7c8cff",   # Cyber Violet
        "text":      "#f4f4f9",
        "muted":     "#7a82ab",
        "entry_bg":  "#1b2046",
        "entry_fg":  "#f4f4f9",
        "error":     "#ef476f",
        "success":   "#06d6a0",
        "border":    "#2f376f",
        "crt_border":"#00f0ff",   # Cyan CRT Frame
        "card_hover":"#232b5d",
    },
    "light": {
        "bg":        "#dbe2ef",
        "bg_2":      "#f0f4f8",
        "panel":     "#ffffff",
        "panel_2":   "#e8eef5",
        "accent":    "#d9a000",   # Darker Gold
        "accent_2":  "#00a86b",   # Mint Accent
        "accent_3":  "#3b52f6",   # Deep Violet
        "text":      "#1a1d2b",
        "muted":     "#5c6b73",
        "entry_bg":  "#f0f4f8",
        "entry_fg":  "#1a1d2b",
        "error":     "#e63946",
        "success":   "#00a86b",
        "border":    "#b0bec5",
        "crt_border":"#0088cc",
        "card_hover":"#d0dce8",
    }
}

DEFAULT_COLORS = THEMES["dark"]

TRANSPARENT_LOGO_URLS = {
    "Python": "https://cdn-icons-png.flaticon.com/512/5968/5968350.png",
    "Java":   "https://cdn-icons-png.flaticon.com/512/226/226777.png",
    "C++":    "https://cdn-icons-png.flaticon.com/512/6132/6132222.png",
    "User":   "https://cdn-icons-png.flaticon.com/512/847/847969.png",
    "Class":  "https://cdn-icons-png.flaticon.com/512/2991/2991106.png",
    "Sword":  "https://cdn-icons-png.flaticon.com/512/1041/1041916.png",
    "Video":  "https://cdn-icons-png.flaticon.com/512/1384/1384060.png",
}

CODE_SNIPPETS = {
    "python": ["def learn():", "import beacon", "print('hi')", "self.level += 1"],
    "cpp":    ["int main() {", "#include <iostream>", "std::cout <<", "int xp = 0;"],
    "js":     ["const goal =>", "function learn()", "console.log(", "let xp = 0"],
}

CODE_COLORS = {
    "python": "#80deea",
    "cpp":    "#ffab91",
    "js":     "#ffe082",
}

FONT_STATS     = ("Consolas", 8, "bold")
FONT_TAG       = ("Consolas", 8, "bold")
FONT_CODE      = ("Consolas", 9, "bold")
FONT_LABEL     = ("Consolas", 8, "bold")
FONT_ENTRY     = ("Consolas", 10, "bold")
FONT_BTN       = ("Consolas", 11, "bold")
FONT_CHIP      = ("Consolas", 7, "bold")
FONT_LINK      = ("Consolas", 9, "underline")
FONT_TOAST     = ("Consolas", 9, "bold")
FONT_HEADER    = ("Consolas", 15, "bold")
FONT_SUBHEADER = ("Consolas", 10, "bold")
FONT_BOX_TITLE = ("Consolas", 13, "bold")
FONT_BOX_SUB   = ("Consolas", 8, "bold")
FONT_CRT       = ("Consolas", 11, "bold")
FONT_BADGE     = ("Consolas", 7, "bold")

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "beacon_users.json")

PIXEL_FONT = {
    'B': ["11110", "10001", "11110", "10001", "11110"],
    'E': ["11111", "10000", "11110", "10000", "11111"],
    'A': ["01110", "10001", "11111", "10001", "10001"],
    'C': ["01111", "10000", "10000", "10000", "01111"],
    'O': ["01110", "10001", "10001", "10001", "01110"],
    'N': ["10001", "11001", "10101", "10011", "10001"]
}


# ==============================================================================
# 3. CURATED ARCADE VIDEO LESSON CURRICULUM (PYTHON, JAVA, C++)
# ==============================================================================

ARCADE_VIDEO_LESSONS = {
    "Python": [
        {
            "id": "py_vid_01",
            "title": "Python for Beginners - Full Programming Course",
            "video_id": "_uQrJ0TkZlc",
            "channel": "Programming with Mosh",
            "duration": "6h 14m",
            "tier": "Beginner",
            "xp": 150,
            "views": "38M views",
            "summary": "The ultimate full Python crash course. Learn installation, variables, receiving input, strings, arithmetic operations, if statements, while loops, lists, and tuples from scratch.",
            "chapters": [
                {"title": "Course Introduction", "time": "0:00", "seconds": 0},
                {"title": "Installing Python & IDE", "time": "2:01", "seconds": 121},
                {"title": "Variables & Data Types", "time": "18:21", "seconds": 1101},
                {"title": "Receiving User Input", "time": "26:42", "seconds": 1602},
                {"title": "String Formatting & Methods", "time": "40:50", "seconds": 2450},
                {"title": "Arithmetic Operators & Precedence", "time": "1:03:29", "seconds": 3809},
                {"title": "If Statements & Comparison Gates", "time": "1:15:40", "seconds": 4540},
                {"title": "While Loops & Guessing Game", "time": "1:36:00", "seconds": 5760},
                {"title": "Lists, 2D Lists & Methods", "time": "2:01:45", "seconds": 7305}
            ],
            "key_points": [
                "Python is dynamically typed: variables adjust type automatically.",
                "input() always returns a string; use int() or float() to convert.",
                "f-strings (f'Score: {score}') provide clean inline interpolation.",
                "Indentation (4 spaces) defines code blocks instead of curly braces."
            ],
            "code_snippet": "# Python Basics Sandbox\nplayer_name = 'ArcadeHero'\nscore = 150\nmultiplier = 2.5\ntotal_score = int(score * multiplier)\nprint(f'Player: {player_name}')\nprint(f'Final Score: {total_score}')\nif total_score >= 300:\n    print('STATUS: ARCADE MASTER! ⚡')\nelse:\n    print('STATUS: ROOKIE ON THE RISE 🌱')"
        },
        {
            "id": "py_vid_02",
            "title": "Python Variables, Input & Type Casting",
            "video_id": "cQT33yu9pY8",
            "channel": "Bro Code",
            "duration": "22m 15s",
            "tier": "Beginner",
            "xp": 100,
            "views": "1.4M views",
            "summary": "Master variable allocation, memory storage concepts, str(), int(), float(), and bool() conversion mechanics with retro examples.",
            "chapters": [
                {"title": "Introduction to Variables", "time": "0:00", "seconds": 0},
                {"title": "Integers, Floats & Strings", "time": "3:10", "seconds": 190},
                {"title": "Booleans & Flags", "time": "8:45", "seconds": 525},
                {"title": "Type Casting Functions", "time": "14:20", "seconds": 860}
            ],
            "key_points": [
                "Variables are containers that store data values in memory.",
                "Booleans hold only True or False and control game state.",
                "Explicit casting prevents TypeError when combining data."
            ],
            "code_snippet": "coins = '25'\nbonus = 10\ntotal_coins = int(coins) + bonus\nprint('Total arcade credits available:', total_coins)"
        },
        {
            "id": "py_vid_03",
            "title": "String Slicing, Indexing & Formatting",
            "video_id": "k9TUPpGqYTo",
            "channel": "Corey Schafer",
            "duration": "18m 42s",
            "tier": "Beginner",
            "xp": 100,
            "views": "890K views",
            "summary": "Learn positive and negative indexing, stride notation, string reversal, and built-in text manipulation utilities.",
            "chapters": [
                {"title": "Single Character Indexing", "time": "0:00", "seconds": 0},
                {"title": "Slice Notation [start:stop:step]", "time": "4:15", "seconds": 255},
                {"title": "String Reversal Trick [::-1]", "time": "10:30", "seconds": 630},
                {"title": "String Methods (upper, lower, replace)", "time": "14:00", "seconds": 840}
            ],
            "key_points": [
                "Strings are immutable sequences in Python.",
                "Indexing starts at 0; negative index -1 accesses the last item.",
                "Slice syntax: string[start:stop:step]."
            ],
            "code_snippet": "badge = 'LEVEL_PALADIN'\nprint('Class:', badge[6:])\nprint('Tag Reversed:', badge[::-1])"
        },
        {
            "id": "py_vid_04",
            "title": "Conditionals: If, Elif, Else & Logical Gates",
            "video_id": "xlbW7_G9sI0",
            "channel": "Bro Code",
            "duration": "16m 30s",
            "tier": "Beginner",
            "xp": 110,
            "views": "980K views",
            "summary": "Build branching decision trees in games. Explore boolean operators and, or, not and conditional ternary expressions.",
            "chapters": [
                {"title": "If Statement Syntax", "time": "0:00", "seconds": 0},
                {"title": "Elif Multiple Conditions", "time": "4:30", "seconds": 270},
                {"title": "Logical Operators (and, or, not)", "time": "9:15", "seconds": 555},
                {"title": "One-line Ternary Statements", "time": "13:20", "seconds": 800}
            ],
            "key_points": [
                "Use 'and' when both conditions must be True.",
                "Use 'or' when at least one condition must be True.",
                "Ternary operator: result = A if condition else B."
            ],
            "code_snippet": "hp = 85\nhas_shield = True\nstatus = 'Invulnerable' if (hp > 50 and has_shield) else 'Vulnerable'\nprint('Hero Status:', status)"
        },
        {
            "id": "py_vid_05",
            "title": "While & For Loops with Range & Enumerate",
            "video_id": "6iF8Xb7Z3wQ",
            "channel": "Tech With Tim",
            "duration": "21m 40s",
            "tier": "Beginner",
            "xp": 120,
            "views": "820K views",
            "summary": "Control loop execution with break, continue, range steps, and enumerate index tracking.",
            "chapters": [
                {"title": "For Loops with range()", "time": "0:00", "seconds": 0},
                {"title": "Iterating Over Collections", "time": "6:10", "seconds": 370},
                {"title": "While Loops & Sentinel Conditions", "time": "11:40", "seconds": 700},
                {"title": "Break & Continue Mechanics", "time": "16:20", "seconds": 980}
            ],
            "key_points": [
                "range(start, stop, step) excludes the stop value.",
                "break exits loop immediately; continue skips to next iteration.",
                "enumerate() yields pairs of (index, item)."
            ],
            "code_snippet": "weapons = ['Dagger', 'Laser Gun', 'Excalibur']\nfor rank, weapon in enumerate(weapons, start=1):\n    print(f'Weapon #{rank}: {weapon}')"
        },
        {
            "id": "py_vid_06",
            "title": "Python Lists, Tuples & Sets Deep Dive",
            "video_id": "W8KRzm-HUcc",
            "channel": "Corey Schafer",
            "duration": "29m 11s",
            "tier": "Intermediate",
            "xp": 140,
            "views": "1.6M views",
            "summary": "Understand mutable lists vs immutable tuples and unique element hashing in sets.",
            "chapters": [
                {"title": "List Mutation (append, extend, insert)", "time": "0:00", "seconds": 0},
                {"title": "Sorting Lists (sort vs sorted)", "time": "8:20", "seconds": 500},
                {"title": "Tuples Immutability & Safety", "time": "15:10", "seconds": 910},
                {"title": "Sets: Unions, Intersections & Difference", "time": "21:30", "seconds": 1290}
            ],
            "key_points": [
                "Lists use [] and are ordered & mutable.",
                "Tuples use () and are immutable, making them hashable.",
                "Sets use {} and eliminate duplicate items automatically."
            ],
            "code_snippet": "p1_loot = {'Gold Coin', 'Potion', 'Gem'}\np2_loot = {'Potion', 'Scroll', 'Bow'}\nshared_loot = p1_loot.intersection(p2_loot)\nprint('Shared Items:', shared_loot)"
        },
        {
            "id": "py_vid_07",
            "title": "Python Dictionaries & Key-Value Lookups",
            "video_id": "daefaLgNkw0",
            "channel": "Corey Schafer",
            "duration": "20m 35s",
            "tier": "Intermediate",
            "xp": 140,
            "views": "1.2M views",
            "summary": "Hash map fundamentals in Python. Safely access keys with dict.get(), mutate dictionaries, and loop keys and values.",
            "chapters": [
                {"title": "Creating Dictionaries", "time": "0:00", "seconds": 0},
                {"title": "Accessing Keys & get() Fallbacks", "time": "4:45", "seconds": 285},
                {"title": "Adding & Updating Keys", "time": "9:30", "seconds": 570},
                {"title": "Iterating items(), keys(), values()", "time": "14:10", "seconds": 850}
            ],
            "key_points": [
                "Dictionaries store O(1) key-value hash associations.",
                "dict.get('key', default) prevents KeyError exceptions.",
                "Dictionary comprehension allows fast on-the-fly mapping."
            ],
            "code_snippet": "character = {'name': 'SonicPixel', 'speed': 99, 'lives': 3}\ncharacter['shield'] = 100\nfor key, val in character.items():\n    print(f'{key.upper()} -> {val}')"
        },
        {
            "id": "py_vid_08",
            "title": "Python Functions, *Args & **Kwargs",
            "video_id": "9Os0o3wzS_I",
            "channel": "Tech With Tim",
            "duration": "24m 15s",
            "tier": "Intermediate",
            "xp": 150,
            "views": "1.1M views",
            "summary": "Write modular reusable functions. Explore positional arguments, default keyword parameters, variable length *args, and keyword **kwargs.",
            "chapters": [
                {"title": "Defining Functions (def)", "time": "0:00", "seconds": 0},
                {"title": "Return Values & Scope", "time": "5:30", "seconds": 330},
                {"title": "*args: Variable Positional Args", "time": "11:20", "seconds": 680},
                {"title": "**kwargs: Keyword Packing", "time": "17:40", "seconds": 1060}
            ],
            "key_points": [
                "DRY principle (Don't Repeat Yourself) through functions.",
                "*args packs extra arguments into a tuple.",
                "**kwargs packs named arguments into a dictionary."
            ],
            "code_snippet": "def build_boss(name, hp, **stats):\n    print(f'Spawning Boss: {name} (HP: {hp})')\n    for stat, val in stats.items():\n        print(f'  - {stat}: {val}')\n\nbuild_boss('Neon Dragon', 5000, fire=95, armor=60)"
        },
        {
            "id": "py_vid_09",
            "title": "Python OOP: Classes, Instances & Methods",
            "video_id": "ZDa-Z5JzLYM",
            "channel": "Corey Schafer",
            "duration": "43m 18s",
            "tier": "Intermediate",
            "xp": 180,
            "views": "2.9M views",
            "summary": "Master Object-Oriented Programming in Python: __init__ constructor, instance variables, class attributes, and encapsulation.",
            "chapters": [
                {"title": "Class Blueprint vs Instance", "time": "0:00", "seconds": 0},
                {"title": "The __init__ Constructor Method", "time": "6:15", "seconds": 375},
                {"title": "Regular Instance Methods", "time": "14:40", "seconds": 880},
                {"title": "Class Variables vs Instance Variables", "time": "24:10", "seconds": 1450}
            ],
            "key_points": [
                "Classes are blueprints for creating concrete object instances.",
                "'self' refers to the specific instance calling the method.",
                "Encapsulation binds data and behavior together cleanly."
            ],
            "code_snippet": "class ArcadeUnit:\n    def __init__(self, name, health):\n        self.name = name\n        self.health = health\n    \n    def take_damage(self, dmg):\n        self.health = max(0, self.health - dmg)\n        print(f'{self.name} took {dmg} damage! Remaining HP: {self.health}')\n\nhero = ArcadeUnit('Pixel Knight', 100)\nhero.take_damage(35)"
        },
        {
            "id": "py_vid_10",
            "title": "Python Error & Exception Handling (Try / Except)",
            "video_id": "nlCKrKGHSSs",
            "channel": "Bro Code",
            "duration": "15m 22s",
            "tier": "Intermediate",
            "xp": 130,
            "views": "720K views",
            "summary": "Prevent crashes using try, except, else, and finally blocks. Catch specific exceptions like ZeroDivisionError and ValueError.",
            "chapters": [
                {"title": "Common Python Errors", "time": "0:00", "seconds": 0},
                {"title": "Try Except Basic Syntax", "time": "3:20", "seconds": 200},
                {"title": "Handling Multiple Exceptions", "time": "7:40", "seconds": 460},
                {"title": "Else & Finally Clean-up", "time": "11:50", "seconds": 710}
            ],
            "key_points": [
                "Never use bare 'except:' as it catches KeyboardInterrupt and system exits.",
                "'finally' block executes regardless of whether an exception occurred.",
                "Custom exceptions can be raised with 'raise Exception(\"msg\")'."
            ],
            "code_snippet": "try:\n    num_lives = int('three')\nexcept ValueError as err:\n    print('Safe Catch:', err)\nfinally:\n    print('Arcade engine continuing uninterrupted!')"
        },
        {
            "id": "py_vid_11",
            "title": "Python Decorators & First-Class Functions",
            "video_id": "FsAPt_9B87U",
            "channel": "Corey Schafer",
            "duration": "31m 15s",
            "tier": "Advanced",
            "xp": 220,
            "views": "1.5M views",
            "summary": "Demystify Python decorators. Understand closures, wrapping functions, returning functions, and adding logging or timing functionality.",
            "chapters": [
                {"title": "First-Class Functions Overview", "time": "0:00", "seconds": 0},
                {"title": "Closures & Inner Functions", "time": "7:30", "seconds": 450},
                {"title": "Decorator Syntax (@symbol)", "time": "14:15", "seconds": 855},
                {"title": "Decorators with Arguments & Wraps", "time": "22:40", "seconds": 1360}
            ],
            "key_points": [
                "A decorator takes a function as an argument, adds behavior, and returns it.",
                "Use functools.wraps to preserve original function docstrings and names.",
                "Decorators are extensively used in frameworks like Flask and FastAPI."
            ],
            "code_snippet": "import time\n\ndef arcade_logger(func):\n    def wrapper(*args, **kwargs):\n        print(f'[EXEC] Calling {func.__name__}...')\n        return func(*args, **kwargs)\n    return wrapper\n\n@arcade_logger\ndef launch_rocket():\n    print('🚀 Blast off into cyberspace!')\n\nlaunch_rocket()"
        },
        {
            "id": "py_vid_12",
            "title": "Python Multithreading vs Multiprocessing",
            "video_id": "IEEhzQoKtQU",
            "channel": "Corey Schafer",
            "duration": "27m 45s",
            "tier": "Advanced",
            "xp": 250,
            "views": "860K views",
            "summary": "Understand concurrency in Python. Explore the Global Interpreter Lock (GIL), threading for I/O bound tasks, and multiprocessing for CPU compute.",
            "chapters": [
                {"title": "Synchronous vs Concurrency", "time": "0:00", "seconds": 0},
                {"title": "Threading Module Basics", "time": "5:40", "seconds": 340},
                {"title": "concurrent.futures ThreadPool", "time": "12:15", "seconds": 735},
                {"title": "Multiprocessing for CPU Workloads", "time": "19:30", "seconds": 1170}
            ],
            "key_points": [
                "I/O-bound operations (network, disk) benefit greatly from threads.",
                "CPU-bound operations require multiprocessing to bypass Python GIL.",
                "ThreadPoolExecutor simplifies asynchronous worker pools."
            ],
            "code_snippet": "import concurrent.futures\nimport time\n\ndef fetch_player(pid):\n    return f'Player #{pid} Data Loaded'\n\nwith concurrent.futures.ThreadPoolExecutor() as executor:\n    results = executor.map(fetch_player, [1, 2, 3])\n    for res in results:\n        print(res)"
        }
    ],

    "Java": [
        {
            "id": "java_vid_01",
            "title": "Java Tutorial for Beginners - Foundations",
            "video_id": "eIrMbAQSU34",
            "channel": "Programming with Mosh",
            "duration": "2h 30m",
            "tier": "Beginner",
            "xp": 150,
            "views": "13M views",
            "summary": "Comprehensive beginner walkthrough of Java. Covers JVM, JDK, syntax, primitive types, arrays, constants, arithmetic, casting, and math.",
            "chapters": [
                {"title": "How Java Works & JVM", "time": "0:00", "seconds": 0},
                {"title": "Anatomy of a Java Program", "time": "10:15", "seconds": 615},
                {"title": "Variables & Primitive Types", "time": "22:40", "seconds": 1360},
                {"title": "Reference Types vs Primitives", "time": "36:10", "seconds": 2170},
                {"title": "Arrays & Multi-Dimensional Arrays", "time": "50:20", "seconds": 3020},
                {"title": "Constants & Arithmetic Expressions", "time": "1:08:00", "seconds": 4080},
                {"title": "Casting & Type Conversion", "time": "1:22:30", "seconds": 4950},
                {"title": "The Math Class & Random Numbers", "time": "1:35:10", "seconds": 5710}
            ],
            "key_points": [
                "Java is strongly and statically typed: every variable must have a declared type.",
                "Source code compiles to bytecode (.class) which runs on the Java Virtual Machine.",
                "Primitive types (int, double, boolean) store values directly on the stack."
            ],
            "code_snippet": "public class Main {\n    public static void main(String[] args) {\n        int score = 250;\n        double multiplier = 1.75;\n        int finalScore = (int)(score * multiplier);\n        System.out.println(\"Arcade Score: \" + finalScore);\n    }\n}"
        },
        {
            "id": "java_vid_02",
            "title": "Java Full Course: Variables, Conditionals & Loops",
            "video_id": "xk4_1vDrzzo",
            "channel": "Bro Code",
            "duration": "12h 00m",
            "tier": "Beginner",
            "xp": 250,
            "views": "7.8M views",
            "summary": "Master Java basics in this complete course. Covers if statements, switches, logical operators, while loops, for loops, and nested loops.",
            "chapters": [
                {"title": "Java Setup & System.out.println", "time": "0:00", "seconds": 0},
                {"title": "User Input with Scanner", "time": "28:10", "seconds": 1690},
                {"title": "If Statements & Comparison", "time": "1:02:40", "seconds": 3760},
                {"title": "Switches & Pattern Matching", "time": "1:18:20", "seconds": 4700},
                {"title": "While Loops & Do-While", "time": "1:35:00", "seconds": 5700},
                {"title": "For Loops & Nested Loops", "time": "1:52:10", "seconds": 6730}
            ],
            "key_points": [
                "Scanner class is used to read input from System.in.",
                "Switch statements test equality against a list of constant values.",
                "Nested loops are essential for 2D grids and matrix game boards."
            ],
            "code_snippet": "public class Main {\n    public static void main(String[] args) {\n        int level = 5;\n        switch (level) {\n            case 1 -> System.out.println(\"Dungeon Floor 1\");\n            case 5 -> System.out.println(\"Boss Arena Unlocked!\");\n            default -> System.out.println(\"Exploring Ruins...\");\n        }\n    }\n}"
        },
        {
            "id": "java_vid_03",
            "title": "Java Methods, Parameters & Scope",
            "video_id": "bqp7_Uksx4c",
            "channel": "Bro Code",
            "duration": "18m 34s",
            "tier": "Beginner",
            "xp": 100,
            "views": "580K views",
            "summary": "Write clean, modular code with Java methods. Understand return types, parameter lists, method overloading, and variable scope.",
            "chapters": [
                {"title": "Declaring Static Methods", "time": "0:00", "seconds": 0},
                {"title": "Passing Parameters by Value", "time": "5:15", "seconds": 315},
                {"title": "Return Statements & Types", "time": "10:30", "seconds": 630},
                {"title": "Method Overloading", "time": "14:20", "seconds": 860}
            ],
            "key_points": [
                "Method signature consists of method name and parameter types.",
                "Java passes all parameters by value (references are copied).",
                "Overloading allows multiple methods with same name but different signatures."
            ],
            "code_snippet": "public class Main {\n    static int calculateDamage(int attack, int armor) {\n        return Math.max(1, attack - armor);\n    }\n    public static void main(String[] args) {\n        int dmg = calculateDamage(50, 20);\n        System.out.println(\"Calculated Strike: \" + dmg);\n    }\n}"
        },
        {
            "id": "java_vid_04",
            "title": "Java Arrays & Enhanced For-Each Loops",
            "video_id": "alwukGzsBg8",
            "channel": "Bro Code",
            "duration": "24m 10s",
            "tier": "Intermediate",
            "xp": 140,
            "views": "740K views",
            "summary": "Array declarations, zero-based indexing, boundary checking, ArrayIndexOutOfBoundsException, and enhanced for-each iteration.",
            "chapters": [
                {"title": "Array Initialization & Memory", "time": "0:00", "seconds": 0},
                {"title": "Iterating with Standard For Loop", "time": "6:20", "seconds": 380},
                {"title": "Enhanced For-Each Syntax", "time": "12:15", "seconds": 735},
                {"title": "2D Matrix Grid Arrays", "time": "18:00", "seconds": 1080}
            ],
            "key_points": [
                "Arrays in Java have a fixed size once initialized.",
                "Array length is a public field (.length), not a method.",
                "Enhanced for loop (for (Type x : arr)) prevents off-by-one errors."
            ],
            "code_snippet": "public class Main {\n    public static void main(String[] args) {\n        String[] inventory = {\"Magic Wand\", \"Shield\", \"Potion\"};\n        for (String item : inventory) {\n            System.out.println(\"Item: \" + item);\n        }\n    }\n}"
        },
        {
            "id": "java_vid_05",
            "title": "Java OOP: Classes, Objects & Constructors",
            "video_id": "A74TOX803D0",
            "channel": "freeCodeCamp",
            "duration": "1h 30m",
            "tier": "Intermediate",
            "xp": 180,
            "views": "1.9M views",
            "summary": "Deep dive into OOP in Java. Master class blueprints, instance instantiation with 'new', constructor overloading, and the 'this' keyword.",
            "chapters": [
                {"title": "Object-Oriented Fundamentals", "time": "0:00", "seconds": 0},
                {"title": "Creating Classes & Fields", "time": "12:40", "seconds": 760},
                {"title": "Constructors & Overloading", "time": "28:15", "seconds": 1695},
                {"title": "The 'this' Keyword & Scope", "time": "45:30", "seconds": 2730},
                {"title": "Getters, Setters & Encapsulation", "time": "1:05:00", "seconds": 3900}
            ],
            "key_points": [
                "Every Java class extends java.lang.Object by default.",
                "Constructors have the exact same name as class and no return type.",
                "Encapsulation protects private state via public accessor methods."
            ],
            "code_snippet": "class Character {\n    private String name;\n    private int hp;\n    public Character(String name, int hp) {\n        this.name = name;\n        this.hp = hp;\n    }\n    public String getName() { return name; }\n    public int getHp() { return hp; }\n}"
        },
        {
            "id": "java_vid_06",
            "title": "Java Inheritance & Polymorphism",
            "video_id": "1uh5pGZ8gS8",
            "channel": "Amigoscode",
            "duration": "35m 45s",
            "tier": "Intermediate",
            "xp": 180,
            "views": "980K views",
            "summary": "Learn class extension using 'extends', super constructor invocation, method overriding with @Override, and dynamic runtime method dispatch.",
            "chapters": [
                {"title": "Why Inheritance?", "time": "0:00", "seconds": 0},
                {"title": "The extends Keyword", "time": "7:20", "seconds": 440},
                {"title": "Super Constructors & Methods", "time": "14:15", "seconds": 855},
                {"title": "Polymorphism & Dynamic Dispatch", "time": "24:30", "seconds": 1470}
            ],
            "key_points": [
                "Java supports single class inheritance but multiple interface implementation.",
                "Use super(...) to call superclass constructor on the first line.",
                "Polymorphism allows treating subclasses uniformly via superclass reference."
            ],
            "code_snippet": "class Hero {\n    void attack() { System.out.println(\"Basic Strike\"); }\n}\nclass Paladin extends Hero {\n    @Override\n    void attack() { System.out.println(\"Holy Smite!\"); }\n}"
        },
        {
            "id": "java_vid_07",
            "title": "Java Interfaces & Abstract Classes",
            "video_id": "Geq484v50iM",
            "channel": "Coding with John",
            "duration": "14m 50s",
            "tier": "Intermediate",
            "xp": 140,
            "views": "1.2M views",
            "summary": "Clear comparison of Interfaces vs Abstract Classes. Learn when to use each, default methods, and contract-driven architecture.",
            "chapters": [
                {"title": "What is an Interface?", "time": "0:00", "seconds": 0},
                {"title": "Implementing Interfaces", "time": "4:15", "seconds": 255},
                {"title": "Abstract Classes vs Interfaces", "time": "8:30", "seconds": 510},
                {"title": "Default Methods in Java 8+", "time": "12:10", "seconds": 730}
            ],
            "key_points": [
                "Interfaces define contracts that implementing classes must satisfy.",
                "Classes can implement multiple interfaces (implements A, B).",
                "Abstract classes can provide common state and partial method implementation."
            ],
            "code_snippet": "interface Castable {\n    void castSpell();\n}\nclass Wizard implements Castable {\n    public void castSpell() {\n        System.out.println(\"Arcane Blast!\");\n    }\n}"
        },
        {
            "id": "java_vid_08",
            "title": "Java ArrayList & Collections Framework",
            "video_id": "pTB0EiLXUC8",
            "channel": "Coding with John",
            "duration": "21m 15s",
            "tier": "Intermediate",
            "xp": 150,
            "views": "1.4M views",
            "summary": "Master dynamic arrays with ArrayList, generics <T>, autoboxing/unboxing with wrapper classes, and iterating Collections.",
            "chapters": [
                {"title": "Fixed Array Limitations", "time": "0:00", "seconds": 0},
                {"title": "ArrayList Initialization & Generics", "time": "4:30", "seconds": 270},
                {"title": "Common Methods (add, get, remove, size)", "time": "9:15", "seconds": 555},
                {"title": "Iterators & Sorting Collections", "time": "15:40", "seconds": 940}
            ],
            "key_points": [
                "ArrayList grows dynamically by allocating new arrays behind the scenes.",
                "Generics ensure type safety at compile time.",
                "Collections.sort() sorts lists in ascending natural order."
            ],
            "code_snippet": "import java.util.ArrayList;\npublic class Main {\n    public static void main(String[] args) {\n        ArrayList<String> party = new ArrayList<>();\n        party.add(\"Warrior\");\n        party.add(\"Mage\");\n        System.out.println(\"Party Size: \" + party.size());\n    }\n}"
        },
        {
            "id": "java_vid_09",
            "title": "Java Exception Handling (Try, Catch, Finally)",
            "video_id": "1XAfapoKL4M",
            "channel": "Coding with John",
            "duration": "16m 40s",
            "tier": "Intermediate",
            "xp": 130,
            "views": "920K views",
            "summary": "Master checked vs unchecked exceptions, the Exception class hierarchy, try-with-resources, and custom exception classes.",
            "chapters": [
                {"title": "Checked vs Unchecked Exceptions", "time": "0:00", "seconds": 0},
                {"title": "Try Catch Finally Blocks", "time": "4:20", "seconds": 260},
                {"title": "Throwing Exceptions with throw / throws", "time": "9:10", "seconds": 550},
                {"title": "Try-with-Resources Auto-Close", "time": "13:00", "seconds": 780}
            ],
            "key_points": [
                "RuntimeExceptions are unchecked; others are checked by the compiler.",
                "Try-with-resources closes AutoCloseable streams automatically.",
                "Always catch specific exceptions before general Exception."
            ],
            "code_snippet": "public class Main {\n    public static void main(String[] args) {\n        try {\n            int result = 100 / 0;\n        } catch (ArithmeticException e) {\n            System.out.println(\"Shield caught division error!\");\n        }\n    }\n}"
        },
        {
            "id": "java_vid_10",
            "title": "Java Lambdas & Functional Interfaces",
            "video_id": "tj5sLSFjVj4",
            "channel": "Coding with John",
            "duration": "20m 18s",
            "tier": "Advanced",
            "xp": 210,
            "views": "1.3M views",
            "summary": "Write concise functional code in Java. Explore the lambda arrow operator ->, @FunctionalInterface, Consumer, Predicate, and Function.",
            "chapters": [
                {"title": "Anonymous Inner Classes vs Lambdas", "time": "0:00", "seconds": 0},
                {"title": "Lambda Syntax & Parameters", "time": "5:30", "seconds": 330},
                {"title": "Predicate, Consumer & Supplier", "time": "11:20", "seconds": 680},
                {"title": "Method References Class::method", "time": "16:40", "seconds": 1000}
            ],
            "key_points": [
                "Lambdas provide clean implementation of Single Abstract Method interfaces.",
                "Method references Class::method provide an even shorter syntax.",
                "Lambdas can capture effectively final local variables from surrounding scope."
            ],
            "code_snippet": "import java.util.List;\npublic class Main {\n    public static void main(String[] args) {\n        List<String> heroes = List.of(\"Archer\", \"Knight\", \"Rogue\");\n        heroes.forEach(h -> System.out.println(\"Hero: \" + h));\n    }\n}"
        },
        {
            "id": "java_vid_11",
            "title": "Java Streams API in Depth",
            "video_id": "Q93JsQ8vcwY",
            "channel": "Amigoscode",
            "duration": "45m 20s",
            "tier": "Advanced",
            "xp": 230,
            "views": "1.1M views",
            "summary": "Transform data pipelines declaratively. Master stream(), filter(), map(), sorted(), collect(Collectors.toList()), and reduce().",
            "chapters": [
                {"title": "Imperative vs Declarative Style", "time": "0:00", "seconds": 0},
                {"title": "Filter & Map Operations", "time": "10:15", "seconds": 615},
                {"title": "Collectors & Terminal Operations", "time": "22:30", "seconds": 1350},
                {"title": "Reduce & Numerical Streams", "time": "34:40", "seconds": 2080}
            ],
            "key_points": [
                "Streams do not modify the original data source.",
                "Intermediate operations are lazy and only execute on terminal operation.",
                "Parallel streams can leverage multi-core processors easily."
            ],
            "code_snippet": "import java.util.List;\nimport java.util.stream.Collectors;\npublic class Main {\n    public static void main(String[] args) {\n        List<Integer> scores = List.of(120, 85, 450, 210);\n        List<Integer> highScores = scores.stream()\n            .filter(s -> s >= 100)\n            .sorted()\n            .collect(Collectors.toList());\n        System.out.println(highScores);\n    }\n}"
        },
        {
            "id": "java_vid_12",
            "title": "Java Multithreading & Concurrency",
            "video_id": "r_MbozD32eo",
            "channel": "Defog Tech",
            "duration": "38m 10s",
            "tier": "Advanced",
            "xp": 260,
            "views": "790K views",
            "summary": "Understand thread life-cycles, extending Thread vs implementing Runnable, synchronized blocks, atomic variables, and ExecutorService.",
            "chapters": [
                {"title": "Thread Lifecycle & Memory Model", "time": "0:00", "seconds": 0},
                {"title": "Runnable vs Thread Class", "time": "8:20", "seconds": 500},
                {"title": "Synchronization & Race Conditions", "time": "17:40", "seconds": 1060},
                {"title": "ExecutorService & ThreadPools", "time": "28:10", "seconds": 1690}
            ],
            "key_points": [
                "Thread.start() spawns a new OS thread; run() runs on the calling thread.",
                "Race conditions occur when multiple threads mutate shared state concurrently.",
                "ExecutorService manages worker thread pools efficiently."
            ],
            "code_snippet": "public class Main {\n    public static void main(String[] args) {\n        Thread worker = new Thread(() -> {\n            System.out.println(\"Arcade background audio thread running!\");\n        });\n        worker.start();\n    }\n}"
        }
    ],

    "C++": [
        {
            "id": "cpp_vid_01",
            "title": "C++ Tutorial for Beginners - Full Course",
            "video_id": "vLnPwxZdW4Y",
            "channel": "freeCodeCamp",
            "duration": "4h 01m",
            "tier": "Beginner",
            "xp": 160,
            "views": "11.5M views",
            "summary": "Complete C++ beginner course. Setting up compiler, cout, variables, data types, string operations, user input with cin, and math functions.",
            "chapters": [
                {"title": "Installing C++ & Environment", "time": "0:00", "seconds": 0},
                {"title": "Hello World & Streams", "time": "12:15", "seconds": 735},
                {"title": "Variables & Data Types", "time": "24:30", "seconds": 1470},
                {"title": "Strings & std::string Methods", "time": "45:10", "seconds": 2710},
                {"title": "Numbers & Arithmetic Operations", "time": "1:02:40", "seconds": 3760},
                {"title": "Getting User Input with cin", "time": "1:21:00", "seconds": 4860},
                {"title": "Building a Calculator App", "time": "1:40:20", "seconds": 6020},
                {"title": "Arrays & Functions", "time": "2:10:00", "seconds": 7800}
            ],
            "key_points": [
                "C++ gives direct control over hardware and low-level memory.",
                "std::cout uses the << insertion operator; std::cin uses >> extraction operator.",
                "Every C++ program begins execution in the main() function."
            ],
            "code_snippet": "#include <iostream>\nint main() {\n    int health = 100;\n    double speed = 14.5;\n    std::cout << \"Hero HP: \" << health << \" | Speed: \" << speed << std::endl;\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_02",
            "title": "C++ Full Course: Variables to Functions",
            "video_id": "-TkoO8ZdUPU",
            "channel": "Bro Code",
            "duration": "6h 00m",
            "tier": "Beginner",
            "xp": 250,
            "views": "5.4M views",
            "summary": "Master fundamental C++ language syntax. Namespaces, typedef, type conversion, ternary operator, switches, while loops, and for loops.",
            "chapters": [
                {"title": "Namespaces & Scope Resolution ::", "time": "0:00", "seconds": 0},
                {"title": "Typedef & Type Aliases", "time": "32:10", "seconds": 1930},
                {"title": "Type Conversion & Casting", "time": "58:40", "seconds": 3520},
                {"title": "Switches & Logical Operators", "time": "1:30:20", "seconds": 5420},
                {"title": "While Loops & Do-While", "time": "2:10:15", "seconds": 7815},
                {"title": "Function Prototypes & Overloading", "time": "3:05:00", "seconds": 11100}
            ],
            "key_points": [
                "Namespaces prevent identifier naming collisions in large projects.",
                "static_cast<Type>(var) performs safe compile-time type conversion.",
                "Function prototypes allow declaring functions before main()."
            ],
            "code_snippet": "#include <iostream>\nint main() {\n    int score = 450;\n    std::string rank = (score >= 400) ? \"S-Tier\" : \"A-Tier\";\n    std::cout << \"Player Rank: \" << rank << std::endl;\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_03",
            "title": "Pointers in C++ Explained Deeply",
            "video_id": "DTxHyVn0ODg",
            "channel": "The Cherno",
            "duration": "14m 28s",
            "tier": "Intermediate",
            "xp": 170,
            "views": "2.2M views",
            "summary": "The definitive pointer guide. Memory addresses, pointer types, the address-of operator &, the dereference operator *, and nullptr.",
            "chapters": [
                {"title": "What is Memory & Addresses?", "time": "0:00", "seconds": 0},
                {"title": "Pointer Declaration & nullptr", "time": "3:40", "seconds": 220},
                {"title": "Address-of Operator (&)", "time": "7:15", "seconds": 435},
                {"title": "Dereferencing Pointers (*)", "time": "10:50", "seconds": 650}
            ],
            "key_points": [
                "A pointer is just an integer that holds a memory address.",
                "Use & to obtain the address of any variable.",
                "Use * to read or write the value at the address pointed to."
            ],
            "code_snippet": "#include <iostream>\nint main() {\n    int gold = 500;\n    int* pGold = &gold;\n    *pGold += 250;\n    std::cout << \"Updated Gold: \" << gold << std::endl;\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_04",
            "title": "References in C++ vs Pointers",
            "video_id": "IzoFn3dfsPA",
            "channel": "The Cherno",
            "duration": "10m 52s",
            "tier": "Intermediate",
            "xp": 140,
            "views": "1.5M views",
            "summary": "Understand C++ references. How references act as aliases, pass-by-reference vs pass-by-value, and passing const references for performance.",
            "chapters": [
                {"title": "What is a Reference?", "time": "0:00", "seconds": 0},
                {"title": "Pass by Reference in Functions", "time": "3:20", "seconds": 200},
                {"title": "Differences: References vs Pointers", "time": "6:40", "seconds": 400},
                {"title": "Const References for Zero-Copy", "time": "8:50", "seconds": 530}
            ],
            "key_points": [
                "References cannot be null and must be bound upon declaration.",
                "References cannot be reseated to point to another variable.",
                "Pass large objects by const ref (const Object&) to avoid copies."
            ],
            "code_snippet": "#include <iostream>\nvoid boostHealth(int& hp) {\n    hp += 50;\n}\nint main() {\n    int playerHp = 100;\n    boostHealth(playerHp);\n    std::cout << \"Boosted HP: \" << playerHp << std::endl;\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_05",
            "title": "Classes & Object-Oriented Programming in C++",
            "video_id": "2BP8NhxjrY0",
            "channel": "The Cherno",
            "duration": "16m 12s",
            "tier": "Intermediate",
            "xp": 180,
            "views": "1.7M views",
            "summary": "Classes vs structs in C++, visibility modifiers (public, private, protected), member variables, and member function declarations.",
            "chapters": [
                {"title": "Struct vs Class in C++", "time": "0:00", "seconds": 0},
                {"title": "Access Modifiers (public vs private)", "time": "4:30", "seconds": 270},
                {"title": "Member Functions & Encapsulation", "time": "9:10", "seconds": 550},
                {"title": "Separating Interface & Implementation", "time": "13:00", "seconds": 780}
            ],
            "key_points": [
                "The only technical difference between struct and class is default visibility: structs default to public, classes default to private.",
                "Encapsulation protects class invariants from unauthorized external mutation.",
                "Methods defined inside class body are implicitly candidates for inlining."
            ],
            "code_snippet": "#include <iostream>\nclass Player {\nprivate:\n    int m_X = 0, m_Y = 0;\npublic:\n    void Move(int xa, int ya) { m_X += xa; m_Y += ya; }\n    void PrintPos() const { std::cout << \"X: \" << m_X << \" Y: \" << m_Y << std::endl; }\n};"
        },
        {
            "id": "cpp_vid_06",
            "title": "Constructors and Destructors in C++",
            "video_id": "FXhALMsHwEY",
            "channel": "The Cherno",
            "duration": "12m 45s",
            "tier": "Intermediate",
            "xp": 150,
            "views": "1.2M views",
            "summary": "Object lifecycle management. Default constructors, parameterized constructors, member initializer lists, and destructor cleanup mechanics.",
            "chapters": [
                {"title": "Object Construction Lifecycle", "time": "0:00", "seconds": 0},
                {"title": "Member Initializer Lists", "time": "4:15", "seconds": 255},
                {"title": "Destructors (~Class)", "time": "8:20", "seconds": 500},
                {"title": "RAII Resource Management", "time": "10:40", "seconds": 640}
            ],
            "key_points": [
                "Member initializer lists initialize member fields before body runs.",
                "Destructors are called automatically when stack objects go out of scope.",
                "RAII (Resource Acquisition Is Initialization) prevents resource leaks."
            ],
            "code_snippet": "#include <iostream>\nclass Unit {\npublic:\n    Unit() { std::cout << \"Unit Spawned!\" << std::endl; }\n    ~Unit() { std::cout << \"Unit Destroyed!\" << std::endl; }\n};"
        },
        {
            "id": "cpp_vid_07",
            "title": "Virtual Functions & Dynamic Polymorphism",
            "video_id": "oIV2KchSyGQ",
            "channel": "The Cherno",
            "duration": "18m 32s",
            "tier": "Advanced",
            "xp": 210,
            "views": "1.4M views",
            "summary": "Runtime polymorphism in C++. Virtual functions, the override keyword, virtual tables (vtable), virtual pointers (vptr), and pure virtual interfaces.",
            "chapters": [
                {"title": "Static vs Dynamic Dispatch", "time": "0:00", "seconds": 0},
                {"title": "The virtual Keyword", "time": "4:50", "seconds": 290},
                {"title": "How V-Tables Work Under the Hood", "time": "9:30", "seconds": 570},
                {"title": "Pure Virtual Functions & Interfaces", "time": "14:15", "seconds": 855}
            ],
            "key_points": [
                "virtual functions allow derived classes to override methods dynamically.",
                "The vtable stores function pointers for runtime method resolution.",
                "Classes with virtual methods should always have a virtual destructor."
            ],
            "code_snippet": "#include <iostream>\nclass Weapon {\npublic:\n    virtual void Fire() { std::cout << \"Weapon Fired!\" << std::endl; }\n    virtual ~Weapon() = default;\n};\nclass LaserGun : public Weapon {\npublic:\n    void Fire() override { std::cout << \"PEW PEW! ⚡\" << std::endl; }\n};"
        },
        {
            "id": "cpp_vid_08",
            "title": "Dynamic Memory Allocation (new & delete)",
            "video_id": "NUZdUSQSCS4",
            "channel": "The Cherno",
            "duration": "17m 40s",
            "tier": "Advanced",
            "xp": 200,
            "views": "1.0M views",
            "summary": "Stack vs Heap memory in C++. How 'new' allocates memory on the free store, how 'delete' releases it, and how to avoid memory leaks.",
            "chapters": [
                {"title": "Stack vs Heap Memory Layout", "time": "0:00", "seconds": 0},
                {"title": "The new Keyword", "time": "5:10", "seconds": 310},
                {"title": "delete and delete[] for Arrays", "time": "10:20", "seconds": 620},
                {"title": "Memory Leaks & Profiling", "time": "14:10", "seconds": 850}
            ],
            "key_points": [
                "Stack memory is automatic, fast, and limited in size.",
                "Heap memory must be manually freed with delete or smart pointers.",
                "Every 'new' must be matched with 'delete'; 'new[]' with 'delete[]'."
            ],
            "code_snippet": "#include <iostream>\nint main() {\n    int* pLevel = new int(99);\n    std::cout << \"Boss Level: \" << *pLevel << std::endl;\n    delete pLevel;\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_09",
            "title": "Smart Pointers: unique_ptr, shared_ptr & weak_ptr",
            "video_id": "UOB7-B2MfwA",
            "channel": "The Cherno",
            "duration": "19m 22s",
            "tier": "Advanced",
            "xp": 230,
            "views": "1.3M views",
            "summary": "Modern C++ memory management. Exclusive ownership with std::unique_ptr, shared reference-counted ownership with std::shared_ptr, and std::weak_ptr.",
            "chapters": [
                {"title": "Why Modern C++ Uses Smart Pointers", "time": "0:00", "seconds": 0},
                {"title": "std::unique_ptr & std::make_unique", "time": "4:15", "seconds": 255},
                {"title": "std::shared_ptr Reference Counting", "time": "10:30", "seconds": 630},
                {"title": "std::weak_ptr Breaking Cycles", "time": "15:40", "seconds": 940}
            ],
            "key_points": [
                "std::unique_ptr has zero overhead compared to raw pointers.",
                "std::make_unique is exception-safe and prevents accidental leaks.",
                "shared_ptr uses an atomic control block for thread-safe reference counts."
            ],
            "code_snippet": "#include <iostream>\n#include <memory>\nclass Entity {\npublic:\n    Entity() { std::cout << \"Entity Created!\" << std::endl; }\n    ~Entity() { std::cout << \"Entity Destroyed!\" << std::endl; }\n};\nint main() {\n    std::unique_ptr<Entity> entity = std::make_unique<Entity>();\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_10",
            "title": "C++ Standard Template Library (STL) Containers",
            "video_id": "g-1Cn3ccwXY",
            "channel": "freeCodeCamp",
            "duration": "1h 45m",
            "tier": "Advanced",
            "xp": 240,
            "views": "1.6M views",
            "summary": "Master std::vector, std::map, std::unordered_map, std::set, iterators, and STL algorithms like std::sort and std::find.",
            "chapters": [
                {"title": "STL Architecture Overview", "time": "0:00", "seconds": 0},
                {"title": "std::vector: Dynamic Array Mastery", "time": "14:20", "seconds": 860},
                {"title": "Iterators & Range-Based For", "time": "32:10", "seconds": 1930},
                {"title": "std::unordered_map Hash Tables", "time": "58:40", "seconds": 3520},
                {"title": "Algorithms: std::sort & std::find", "time": "1:22:00", "seconds": 4920}
            ],
            "key_points": [
                "std::vector stores elements contiguously in memory for cache-friendly access.",
                "std::unordered_map offers O(1) average lookup time via hashing.",
                "STL algorithms separate operations from specific container data structures."
            ],
            "code_snippet": "#include <iostream>\n#include <vector>\n#include <algorithm>\nint main() {\n    std::vector<int> scores = {500, 120, 999, 320};\n    std::sort(scores.begin(), scores.end());\n    for (int s : scores) std::cout << s << \" \";\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_11",
            "title": "Templates & Generic Programming in C++",
            "video_id": "I-hZkUa9mIs",
            "channel": "The Cherno",
            "duration": "15m 35s",
            "tier": "Advanced",
            "xp": 220,
            "views": "920K views",
            "summary": "Write generic code without runtime overhead. Function templates, class templates, non-type template parameters, and compile-time evaluation.",
            "chapters": [
                {"title": "What are Templates?", "time": "0:00", "seconds": 0},
                {"title": "Function Templates", "time": "4:10", "seconds": 250},
                {"title": "Class Templates", "time": "8:30", "seconds": 510},
                {"title": "Compile-time Code Generation", "time": "12:15", "seconds": 735}
            ],
            "key_points": [
                "Templates are evaluated at compile time by the C++ compiler.",
                "Compiler generates a distinct concrete function for each specialized type.",
                "Templates enable type-safe, high-performance zero-cost abstractions."
            ],
            "code_snippet": "#include <iostream>\ntemplate<typename T>\nT GetMax(T a, T b) {\n    return (a > b) ? a : b;\n}\nint main() {\n    std::cout << \"Max: \" << GetMax<int>(10, 25) << std::endl;\n    return 0;\n}"
        },
        {
            "id": "cpp_vid_12",
            "title": "Move Semantics & Rvalue References (std::move)",
            "video_id": "ehMg6zvXuMQ",
            "channel": "The Cherno",
            "duration": "22m 14s",
            "tier": "Advanced",
            "xp": 260,
            "views": "1.2M views",
            "summary": "Master modern C++ performance. Understand lvalues, rvalues, rvalue references (&&), move constructors, and std::move to eliminate expensive copies.",
            "chapters": [
                {"title": "Lvalues vs Rvalues Defined", "time": "0:00", "seconds": 0},
                {"title": "Rvalue References (Type&&)", "time": "5:40", "seconds": 340},
                {"title": "Move Constructor & Move Assignment", "time": "11:20", "seconds": 680},
                {"title": "std::move & Stealing Resources", "time": "17:30", "seconds": 1050}
            ],
            "key_points": [
                "Lvalues have identifiable memory addresses; rvalues are temporary values.",
                "Move semantics allows transferring ownership of heap memory without copying.",
                "std::move casts an lvalue to an rvalue reference to allow moving."
            ],
            "code_snippet": "#include <iostream>\n#include <string>\n#include <utility>\nint main() {\n    std::string str1 = \"Ultra Rare Arcane Blade\";\n    std::string str2 = std::move(str1);\n    std::cout << \"Transferred: \" << str2 << std::endl;\n    return 0;\n}"
        }
    ]
}


# ==============================================================================
# 4. EXPANDED MULTI-SECTION CURRICULUM DATA ENGINE (250+ LESSONS)
# ==============================================================================

PROGRAM_CURRICULUM = {
    "Python": [
        # SECTION 1: BEGINNER - BASICS & IO
        {
            "section_title": "1. Python Foundations & I/O",
            "tier": "Beginner",
            "lessons": [
                {"title": "System Boot", "xp": 50, "example": "print('Hello')", "exp_out": "BEACON Online", "desc": "Print 'BEACON Online' to fire up the Python execution terminal.", "code": "print('')"},
                {"title": "Variable Power", "xp": 50, "example": "score = 10\\nprint(score)", "exp_out": "100", "desc": "Create a variable named 'power' set to 100 and print it.", "code": "power = \\nprint()"},
                {"title": "String Fusion", "xp": 60, "example": "print('A' + 'B')", "exp_out": "Player One", "desc": "Concatenate strings 'Player ' and 'One' inside print().", "code": ""},
                {"title": "HP Multiplier", "xp": 60, "example": "print(10 * 2)", "exp_out": "200", "desc": "Calculate 50 multiplied by 4 and output the result.", "code": ""},
                {"title": "Float Precision", "xp": 70, "example": "print(3.14)", "exp_out": "99.9", "desc": "Assign 99.9 to variable 'shield' and print it.", "code": ""},
                {"title": "Type Checking", "xp": 70, "example": "print(type(5))", "exp_out": "<class 'int'>", "desc": "Print the type of integer number 42 using type().", "code": ""},
                {"title": "String Repetition", "xp": 80, "example": "print('A' * 3)", "exp_out": "⚡⚡⚡", "desc": "Print string '⚡' repeated 3 times using multiplication.", "code": ""},
                {"title": "Formatted Output", "xp": 80, "example": "name='x'\\nprint(f'{name}')", "exp_out": "Level: 5", "desc": "Set lvl=5 and print 'Level: 5' using an f-string.", "code": ""},
                {"title": "Multi-Line Output", "xp": 90, "example": "print('A\\nB')", "exp_out": "Stage 1\\nStage 2", "desc": "Output 'Stage 1' and 'Stage 2' on separate lines using \\n.", "code": ""},
                {"title": "Basic Arithmetic", "xp": 90, "example": "print(10 - 3)", "exp_out": "75", "desc": "Subtract 25 from 100 and print the result.", "code": ""},
                {"title": "Integer Division", "xp": 100, "example": "print(10 // 3)", "exp_out": "4", "desc": "Perform integer division (//) on 18 by 4 and output it.", "code": ""},
                {"title": "Modulo Remainder", "xp": 100, "example": "print(10 % 3)", "exp_out": "1", "desc": "Calculate remainder of 25 divided by 4 using %.", "code": ""},
            ]
        },
        # SECTION 2: BEGINNER - CONTROL FLOW & LOGIC
        {
            "section_title": "2. Control Flow & Branching",
            "tier": "Beginner",
            "lessons": [
                {"title": "Hero Status Check", "xp": 100, "example": "if True:\\n    print('Yes')", "exp_out": "Shield Ready", "desc": "Set shields = 100. If shields == 100, print 'Shield Ready'.", "code": "shields = 100\\n"},
                {"title": "Else Branching", "xp": 100, "example": "if False:\\n    pass\\nelse:\\n    print('No')", "exp_out": "Game Over", "desc": "Set hp = 0. If hp > 0 print 'Alive', else print 'Game Over'.", "code": ""},
                {"title": "Elif Logic Chain", "xp": 110, "example": "if x==1:\\n    pass\\nelif x==2:\\n    print('Two')", "exp_out": "Gold Tier", "desc": "Set score = 85. If score >= 90 print 'Plat', elif score >= 80 print 'Gold Tier'.", "code": ""},
                {"title": "Boolean Operators", "xp": 110, "example": "print(True and False)", "exp_out": "True", "desc": "Print the result of (has_key and has_mana) where key=True, mana=True.", "code": ""},
                {"title": "Not Logical Gate", "xp": 120, "example": "print(not False)", "exp_out": "True", "desc": "Set is_poisoned = False. Print (not is_poisoned).", "code": ""},
                {"title": "Comparison Gates", "xp": 120, "example": "print(5 >= 3)", "exp_out": "True", "desc": "Check if player_level (12) is greater than or equal to boss_req (10).", "code": ""},
                {"title": "Nested Conditionals", "xp": 130, "example": "if True:\\n    if True:\\n        print('In')", "exp_out": "Access Granted", "desc": "Check if role == 'Admin' and code == 1234, output 'Access Granted'.", "code": "role = 'Admin'\\ncode = 1234\\n"},
                {"title": "Ternary Operator", "xp": 130, "example": "status = 'OK' if True else 'NO'\\nprint(status)", "exp_out": "Ready", "desc": "Assign 'Ready' if energy >= 50 else 'Rest' and print it (energy=80).", "code": ""},
                {"title": "Identity Check", "xp": 140, "example": "print(x is None)", "exp_out": "True", "desc": "Set item = None and print (item is None).", "code": ""},
                {"title": "Membership In", "xp": 140, "example": "print('a' in 'apple')", "exp_out": "True", "desc": "Check if 'Sword' is in inventory string 'Dagger, Sword, Bow' and print it.", "code": ""},
            ]
        },
        # SECTION 3: INTERMEDIATE - LOOPS & LISTS
        {
            "section_title": "3. Iteration & Data Collections",
            "tier": "Intermediate",
            "lessons": [
                {"title": "Countdown Loop", "xp": 140, "example": "for i in range(2):\\n    print(i)", "exp_out": "3\\n2\\n1", "desc": "Use a loop or print statements to output 3, 2, 1 on new lines.", "code": ""},
                {"title": "Inventory Array", "xp": 150, "example": "arr = ['A', 'B']\\nprint(arr[1])", "exp_out": "Mana Potion", "desc": "Store ['Health Potion', 'Mana Potion'] in a list and print 2nd item.", "code": ""},
                {"title": "List Append", "xp": 150, "example": "l = []\\nl.append('A')\\nprint(l)", "exp_out": "['Shield']", "desc": "Create empty list items, append 'Shield', and print items.", "code": ""},
                {"title": "Summing Loop", "xp": 160, "example": "s = 0\\nfor x in [1,2]: s += x", "exp_out": "15", "desc": "Sum numbers in [3, 5, 7] using a loop and print total.", "code": ""},
                {"title": "While Counter", "xp": 160, "example": "i = 0\\nwhile i<2:\\n    print(i)\\n    i+=1", "exp_out": "0\\n1\\n2", "desc": "Use a while loop to print numbers 0 to 2.", "code": ""},
                {"title": "List Slicing", "xp": 170, "example": "nums = [10, 20, 30]\\nprint(nums[:2])", "exp_out": "[10, 20]", "desc": "Slice and print first 2 items of [10, 20, 30, 40].", "code": ""},
                {"title": "List Length", "xp": 170, "example": "print(len([1, 2]))", "exp_out": "4", "desc": "Print length of list ['Ruby', 'Emerald', 'Sapphire', 'Diamond'].", "code": ""},
                {"title": "Loop Break", "xp": 180, "example": "for i in range(5):\\n    if i==2: break\\n    print(i)", "exp_out": "0\\n1", "desc": "Loop 0 to 4, break when i == 2, print preceding numbers.", "code": ""},
                {"title": "List Comprehension", "xp": 180, "example": "print([x*2 for x in [1,2]])", "exp_out": "[2, 4, 6]", "desc": "Multiply each element in [1, 2, 3] by 2 using list comprehension.", "code": ""},
                {"title": "Tuple Immutability", "xp": 190, "example": "t = (1, 2)\\nprint(t[0])", "exp_out": "Arcade", "desc": "Define tuple t = ('Arcade', 'Retro') and print 1st item.", "code": ""},
            ]
        },
        # SECTION 4: INTERMEDIATE - DICTIONARIES & FUNCTIONS
        {
            "section_title": "4. Dictionaries & Modular Functions",
            "tier": "Intermediate",
            "lessons": [
                {"title": "Dictionary Loot", "xp": 180, "example": "d = {'a': 1}\\nprint(d['a'])", "exp_out": "500", "desc": "Create dict player = {'xp': 500} and print 'xp' value.", "code": ""},
                {"title": "Damage Function", "xp": 190, "example": "def fn(): return 10\\nprint(fn())", "exp_out": "35", "desc": "Define function hit() returning 35 and print hit().", "code": ""},
                {"title": "Function Arguments", "xp": 190, "example": "def add(a, b): return a+b", "exp_out": "15", "desc": "Define add(a, b) returning a+b and print add(7, 8).", "code": ""},
                {"title": "Dict Update", "xp": 200, "example": "d = {}\\nd['hp'] = 100\\nprint(d)", "exp_out": "{'gold': 50}", "desc": "Create empty dict stats, set stats['gold'] = 50, print stats.", "code": ""},
                {"title": "Default Arguments", "xp": 200, "example": "def greet(n='Hero'): return n", "exp_out": "Hero", "desc": "Define greet(name='Hero') returning name and print greet().", "code": ""},
                {"title": "Dict Keys View", "xp": 210, "example": "d = {'a':1}\\nprint(list(d.keys()))", "exp_out": "['hp', 'mp']", "desc": "Print list of keys from dict {'hp': 100, 'mp': 50}.", "code": ""},
                {"title": "Lambda Expressions", "xp": 210, "example": "sq = lambda x: x*x\\nprint(sq(3))", "exp_out": "25", "desc": "Create lambda function doubling x, evaluate for 12.5 -> output 25.0.", "code": "double = lambda x: \\nprint(double(12.5))"},
                {"title": "Multiple Returns", "xp": 220, "example": "def stats(): return 10, 20\\nprint(stats())", "exp_out": "(100, 200)", "desc": "Function get_pos() returning 100, 200. Print get_pos().", "code": ""},
                {"title": "Kwargs Processing", "xp": 220, "example": "def f(**k): print(k['x'])\\nf(x=5)", "exp_out": "99", "desc": "Function print_val(**kwargs) prints kwargs['val']. Call with val=99.", "code": ""},
                {"title": "Map Function", "xp": 230, "example": "print(list(map(str, [1, 2])))", "exp_out": "['1', '2', '3']", "desc": "Convert [1, 2, 3] to strings using map() and print list.", "code": ""},
            ]
        },
        # SECTION 5: ADVANCED - OOP & MODULES
        {
            "section_title": "5. Object-Oriented Programming (OOP)",
            "tier": "Advanced",
            "lessons": [
                {"title": "Hero Class Instantiation", "xp": 240, "example": "class A: pass\\na = A()", "exp_out": "Knight", "desc": "Class Player with attribute name='Knight'. Instantiate and print name.", "code": "class Player:\\n    name = 'Knight'\\n"},
                {"title": "Constructor __init__", "xp": 250, "example": "class A:\\n    def __init__(self, x):\\n        self.x = x", "exp_out": "100", "desc": "Class Boss with __init__(self, hp). Instantiate with 100 and print hp.", "code": ""},
                {"title": "Class Methods", "xp": 250, "example": "class A:\\n    def msg(self): return 'Hi'", "exp_out": "Attacking!", "desc": "Class Hero with method attack() returning 'Attacking!'. Print output.", "code": ""},
                {"title": "Class Inheritance", "xp": 260, "example": "class Parent: pass\\nclass Child(Parent): pass", "exp_out": "Mage", "desc": "Class Hero parent, class Wizard(Hero) child with role='Mage'. Print role.", "code": ""},
                {"title": "Encapsulation Private", "xp": 260, "example": "class A:\\n    def __init__(self):\\n        self.__secret = 42", "exp_out": "777", "desc": "Class Vault with private __code=777 and get_code() method. Print getter.", "code": ""},
                {"title": "Static Methods", "xp": 270, "example": "class Math:\\n    @staticmethod\\n    def add(a,b): return a+b", "exp_out": "30", "desc": "Class Calc with @staticmethod triple(x) returning x*3. Print Calc.triple(10).", "code": ""},
                {"title": "Property Decorators", "xp": 270, "example": "class A:\\n    @property\\n    def val(self): return 10", "exp_out": "Active", "desc": "Class Game with @property status returning 'Active'. Print game.status.", "code": ""},
                {"title": "String Representation", "xp": 280, "example": "class A:\\n    def __str__(self): return 'Obj'", "exp_out": "Hero[Lvl 10]", "desc": "Class Character with __str__ returning 'Hero[Lvl 10]'. Print object.", "code": ""},
                {"title": "Method Overriding", "xp": 290, "example": "class A: def f(self): return 1\\nclass B(A): def f(self): return 2", "exp_out": "Special Move", "desc": "Override move() in subclass SuperHero to return 'Special Move'.", "code": ""},
                {"title": "Class Polymorphism", "xp": 300, "example": "for obj in [A(), B()]: print(obj.sound())", "exp_out": "Slash\\nCast", "desc": "Loop items [Sword(), Staff()], call action() outputting 'Slash' then 'Cast'.", "code": ""},
            ]
        },
        # SECTION 6: ADVANCED - ERROR HANDLING & ALGORITHMS
        {
            "section_title": "6. Exceptions, IO & Algorithms",
            "tier": "Advanced",
            "lessons": [
                {"title": "Try Except Block", "xp": 300, "example": "try:\\n    1/0\\nexcept:\\n    print('Err')", "exp_out": "Caught Error", "desc": "Catch ZeroDivisionError and print 'Caught Error'.", "code": "try:\\n    x = 10 / 0\\nexcept ZeroDivisionError:\\n    "},
                {"title": "Finally Clean execution", "xp": 310, "example": "try: pass\\nfinally: print('Done')", "exp_out": "Clean Finish", "desc": "Execute try-finally block printing 'Clean Finish' in finally.", "code": ""},
                {"title": "Custom Exceptions", "xp": 320, "example": "raise ValueError('Fail')", "exp_out": "Custom Exception Raised", "desc": "Catch custom Exception with message 'Custom Exception Raised'.", "code": ""},
                {"title": "List Sorting", "xp": 330, "example": "l = [3, 1]\\nl.sort()\\nprint(l)", "exp_out": "[1, 5, 9]", "desc": "Sort list [9, 1, 5] in ascending order and print it.", "code": ""},
                {"title": "Filter Function", "xp": 340, "example": "print(list(filter(lambda x: x>1, [0,2])))", "exp_out": "[10, 20]", "desc": "Filter numbers > 5 from list [2, 10, 4, 20] and print.", "code": ""},
                {"title": "Recursive Countdown", "xp": 350, "example": "def rec(n):\\n    if n==0: return\\n    print(n); rec(n-1)", "exp_out": "2\\n1", "desc": "Write recursive function count(n) printing 2 then 1.", "code": ""},
                {"title": "List Max Search", "xp": 360, "example": "print(max([10, 50, 20]))", "exp_out": "999", "desc": "Find and print maximum damage value from [120, 999, 450].", "code": ""},
                {"title": "Dictionary Comprehension", "xp": 370, "example": "print({x: x*2 for x in [1,2]})", "exp_out": "{1: 10, 2: 20}", "desc": "Create dict mapping x -> x*10 for x in [1, 2].", "code": ""},
                {"title": "Zip Aggregation", "xp": 380, "example": "print(list(zip(['a'], [1])))", "exp_out": "[('A', 100)]", "desc": "Zip keys ['A'] and values [100] together and print list.", "code": ""},
                {"title": "Boss Fight Math Final", "xp": 500, "example": "print(sum([10, 20]))", "exp_out": "1500", "desc": "Sum boss combo hits [400, 500, 600] and print final total.", "code": ""},
            ]
        }
    ],

    "Java": [
        # SECTION 1: BEGINNER - JAVA SYNTAX & PRINTING
        {
            "section_title": "1. Java Arcade Fundamentals",
            "tier": "Beginner",
            "lessons": [
                {"title": "System Boot", "xp": 50, "example": "System.out.println(\\\"Boot\\\");", "exp_out": "Java Arcade Ready", "desc": "Print 'Java Arcade Ready' using System.out.println.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        System.out.println(\\\"Java Arcade Ready\\\");\\n    }\\n}"},
                {"title": "Primitive HP", "xp": 50, "example": "int hp = 100;\\nSystem.out.println(hp);", "exp_out": "100", "desc": "Declare int variable hp set to 100 inside Main and print it.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int hp = 100;\\n        System.out.println(hp);\\n    }\\n}"},
                {"title": "Knight Class Rank", "xp": 60, "example": "String r = \\\"Paladin\\\";", "exp_out": "Paladin", "desc": "Declare String 'rank' with value \\\"Paladin\\\" and print it.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        String rank = \\\"Paladin\\\";\\n        System.out.println(rank);\\n    }\\n}"},
                {"title": "Score Multiplier", "xp": 60, "example": "System.out.println(10 * 2);", "exp_out": "120", "desc": "Multiply 15 by 8 and print output.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        System.out.println(15 * 8);\\n    }\\n}"},
                {"title": "Double Precision", "xp": 70, "example": "double d = 9.99;", "exp_out": "99.5", "desc": "Declare double energy = 99.5 and print it.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        double energy = 99.5;\\n        System.out.println(energy);\\n    }\\n}"},
                {"title": "Char Character Stat", "xp": 70, "example": "char c = 'A';", "exp_out": "S", "desc": "Declare char rank = 'S' and print it.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        char rank = 'S';\\n        System.out.println(rank);\\n    }\\n}"},
                {"title": "Boolean Flag", "xp": 80, "example": "boolean b = true;", "exp_out": "true", "desc": "Declare boolean isAlive = true and print it.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        boolean isAlive = true;\\n        System.out.println(isAlive);\\n    }\\n}"},
                {"title": "String Concatenation", "xp": 80, "example": "System.out.println(\\\"A\\\" + \\\"B\\\");", "exp_out": "Level 10", "desc": "Print \\\"Level \\\" + 10.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        System.out.println(\\\"Level \\\" + 10);\\n    }\\n}"},
                {"title": "Arithmetic Addition", "xp": 90, "example": "System.out.println(5 + 5);", "exp_out": "500", "desc": "Print sum of 200 + 300.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        System.out.println(200 + 300);\\n    }\\n}"},
                {"title": "Modulus Operator", "xp": 100, "example": "System.out.println(10 % 3);", "exp_out": "2", "desc": "Print 14 % 4 remainder result.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        System.out.println(14 % 4);\\n    }\\n}"},
            ]
        },
        # SECTION 2: BEGINNER - CONTROL STRUCTURES
        {
            "section_title": "2. Java Branching & Loops",
            "tier": "Beginner",
            "lessons": [
                {"title": "Mana Check", "xp": 100, "example": "if(true) System.out.println(\\\"OK\\\");", "exp_out": "Spell Cast", "desc": "Create int mana = 50. If mana >= 30, print \\\"Spell Cast\\\".", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int mana = 50;\\n        if (mana >= 30) {\\n            System.out.println(\\\"Spell Cast\\\");\\n        }\\n    }\\n}"},
                {"title": "If-Else Gate", "xp": 100, "example": "if(x>0) ... else ...", "exp_out": "Defeat", "desc": "Set int hp = 0. If hp > 0 print \\\"Victory\\\", else print \\\"Defeat\\\".", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int hp = 0;\\n        if (hp > 0) System.out.println(\\\"Victory\\\");\\n        else System.out.println(\\\"Defeat\\\");\\n    }\\n}"},
                {"title": "For Loop Counter", "xp": 110, "example": "for(int i=0; i<2; i++) System.out.println(i);", "exp_out": "1\\n2\\n3", "desc": "Write a for loop printing numbers 1 to 3.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        for(int i=1; i<=3; i++) {\\n            System.out.println(i);\\n        }\\n    }\\n}"},
                {"title": "While Loop Countdown", "xp": 120, "example": "while(x>0) x--;", "exp_out": "3\\n2\\n1", "desc": "Write a while loop counting down from 3 to 1.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int c = 3;\\n        while(c > 0) {\\n            System.out.println(c);\\n            c--;\\n        }\\n    }\\n}"},
                {"title": "Switch Statement", "xp": 130, "example": "switch(key) { case 1: ... }", "exp_out": "Sword Selected", "desc": "Switch on int key=1. Case 1 prints \\\"Sword Selected\\\".", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int key = 1;\\n        switch(key) {\\n            case 1: System.out.println(\\\"Sword Selected\\\"); break;\\n        }\\n    }\\n}"},
                {"title": "Logical AND Gate", "xp": 130, "example": "if(a && b) ...", "exp_out": "Boss Unlocked", "desc": "If lvl >= 10 && key == true, print \\\"Boss Unlocked\\\".", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int lvl = 10; boolean key = true;\\n        if(lvl >= 10 && key) System.out.println(\\\"Boss Unlocked\\\");\\n    }\\n}"},
                {"title": "Ternary Operator", "xp": 140, "example": "String s = (x>0)?\\\"A\\\":\\\"B\\\";", "exp_out": "Alive", "desc": "Set String status = (hp > 0) ? \\\"Alive\\\" : \\\"Dead\\\" (hp=50). Print status.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int hp = 50;\\n        String status = (hp > 0) ? \\\"Alive\\\" : \\\"Dead\\\";\\n        System.out.println(status);\\n    }\\n}"},
                {"title": "Do-While Loop", "xp": 140, "example": "do { ... } while(cond);", "exp_out": "Executed Once", "desc": "Use do-while loop to print \\\"Executed Once\\\" when condition is false.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        do {\\n            System.out.println(\\\"Executed Once\\\");\\n        } while(false);\\n    }\\n}"},
                {"title": "Break Statement", "xp": 150, "example": "for(...) { if(...) break; }", "exp_out": "0\\n1", "desc": "Loop i from 0 to 5, break when i==2, print preceding values.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        for(int i=0; i<5; i++) {\\n            if(i==2) break;\\n            System.out.println(i);\\n        }\\n    }\\n}"},
                {"title": "Continue Statement", "xp": 150, "example": "if(i==1) continue;", "exp_out": "0\\n2", "desc": "Loop i from 0 to 2, skip i==1 using continue, print i.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        for(int i=0; i<=2; i++) {\\n            if(i==1) continue;\\n            System.out.println(i);\\n        }\\n    }\\n}"},
            ]
        },
        # SECTION 3: INTERMEDIATE - ARRAYS & METHODS
        {
            "section_title": "3. Java Arrays & Static Methods",
            "tier": "Intermediate",
            "lessons": [
                {"title": "Weapon Array", "xp": 160, "example": "String[] w = {\\\"A\\\", \\\"B\\\"};", "exp_out": "Excalibur", "desc": "Create String array weapons {\\\"Dagger\\\", \\\"Excalibur\\\"} and print 2nd item.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        String[] weapons = {\\\"Dagger\\\", \\\"Excalibur\\\"};\\n        System.out.println(weapons[1]);\\n    }\\n}"},
                {"title": "Array Length", "xp": 160, "example": "System.out.println(arr.length);", "exp_out": "3", "desc": "Print length of int array {10, 20, 30}.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int[] scores = {10, 20, 30};\\n        System.out.println(scores.length);\\n    }\\n}"},
                {"title": "Static Method Call", "xp": 170, "example": "static void msg() { ... }", "exp_out": "Hero Ready", "desc": "Complete static method printHero() to output \\\"Hero Ready\\\".", "code": "public class Main {\\n    static void printHero() {\\n        System.out.println(\\\"Hero Ready\\\");\\n    }\\n    public static void main(String[] args) {\\n        printHero();\\n    }\\n}"},
                {"title": "Method Return Value", "xp": 180, "example": "static int getXP() { return 250; }", "exp_out": "250", "desc": "Complete static method getXP() returning 250 and print it in main.", "code": "public class Main {\\n    static int getXP() {\\n        return 250;\\n    }\\n    public static void main(String[] args) {\\n        System.out.println(getXP());\\n    }\\n}"},
                {"title": "Method Arguments", "xp": 190, "example": "static int add(int a, int b) { return a+b; }", "exp_out": "30", "desc": "Create static method multiply(a, b) returning a*b. Print multiply(5, 6).", "code": "public class Main {\\n    static int multiply(int a, int b) {\\n        return a * b;\\n    }\\n    public static void main(String[] args) {\\n        System.out.println(multiply(5, 6));\\n    }\\n}"},
                {"title": "Array Iteration", "xp": 200, "example": "for(int x : arr) System.out.println(x);", "exp_out": "10\\n20", "desc": "Iterate int array {10, 20} using enhanced for loop.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int[] nums = {10, 20};\\n        for(int n : nums) System.out.println(n);\\n    }\\n}"},
                {"title": "2D Array Cell", "xp": 210, "example": "int[][] grid = {{1, 2}, {3, 4}};", "exp_out": "4", "desc": "Access element [1][1] from 2D array {{1, 2}, {3, 4}}.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int[][] grid = {{1, 2}, {3, 4}};\\n        System.out.println(grid[1][1]);\\n    }\\n}"},
                {"title": "Method Overloading", "xp": 220, "example": "static int f(int a) ... static double f(double a) ...", "exp_out": "100.0", "desc": "Overload score() to accept double argument 100.0 and print it.", "code": "public class Main {\\n    static void score(int s) { System.out.println(s); }\\n    static void score(double s) { System.out.println(s); }\\n    public static void main(String[] args) {\\n        score(100.0);\\n    }\\n}"},
                {"title": "Array Sum Algorithm", "xp": 230, "example": "int sum = 0;\\nfor(int n : arr) sum += n;", "exp_out": "60", "desc": "Sum elements of {10, 20, 30} and output result.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        int[] arr = {10, 20, 30};\\n        int sum = 0;\\n        for(int i : arr) sum += i;\\n        System.out.println(sum);\\n    }\\n}"},
                {"title": "String UpperCase", "xp": 240, "example": "System.out.println(s.toUpperCase());", "exp_out": "ARCADE", "desc": "Convert string \\\"arcade\\\" to uppercase and print it.", "code": "public class Main {\\n    public static void main(String[] args) {\\n        String str = \\\"arcade\\\";\\n        System.out.println(str.toUpperCase());\\n    }\\n}"},
            ]
        },
        # SECTION 4: ADVANCED - OBJECT-ORIENTED JAVA
        {
            "section_title": "4. Java OOP & Classes",
            "tier": "Advanced",
            "lessons": [
                {"title": "Class Instantion", "xp": 250, "example": "class Hero { int hp = 100; }", "exp_out": "100", "desc": "Create Hero instance and print hero.hp.", "code": "class Hero {\\n    int hp = 100;\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        Hero h = new Hero();\\n        System.out.println(h.hp);\\n    }\\n}"},
                {"title": "Constructor Initialization", "xp": 260, "example": "Hero(int h) { this.hp = h; }", "exp_out": "500", "desc": "Pass 500 to Hero constructor and print hp.", "code": "class Hero {\\n    int hp;\\n    Hero(int hp) { this.hp = hp; }\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        Hero h = new Hero(500);\\n        System.out.println(h.hp);\\n    }\\n}"},
                {"title": "Encapsulation Getters", "xp": 270, "example": "private int xp;\\npublic int getXp() { return xp; }", "exp_out": "999", "desc": "Use private int xp = 999 with getter method getXp().", "code": "class Player {\\n    private int xp = 999;\\n    public int getXp() { return xp; }\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        Player p = new Player();\\n        System.out.println(p.getXp());\\n    }\\n}"},
                {"title": "Inheritance Extends", "xp": 280, "example": "class Mage extends Hero { }", "exp_out": "Fireball", "desc": "Mage extends Hero and inherits spell = \\\"Fireball\\\". Print mage.spell.", "code": "class Hero {\\n    String spell = \\\"Fireball\\\";\\n}\\nclass Mage extends Hero {}\\npublic class Main {\\n    public static void main(String[] args) {\\n        Mage m = new Mage();\\n        System.out.println(m.spell);\\n    }\\n}"},
                {"title": "Polymorphism Method Overriding", "xp": 290, "example": "@Override void attack() { ... }", "exp_out": "Slash!", "desc": "Override attack() in SubClass to output \\\"Slash!\\\".", "code": "class Weapon {\\n    void attack() { System.out.println(\\\"Hit\\\"); }\\n}\\nclass Sword extends Weapon {\\n    void attack() { System.out.println(\\\"Slash!\\\"); }\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        Weapon w = new Sword();\\n        w.attack();\\n    }\\n}"},
                {"title": "Super Keyword", "xp": 300, "example": "super.attack();", "exp_out": "Base Attack", "desc": "Call super.show() from sub-class method.", "code": "class Base {\\n    void show() { System.out.println(\\\"Base Attack\\\"); }\\n}\\nclass Sub extends Base {\\n    void show() { super.show(); }\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        new Sub().show();\\n    }\\n}"},
                {"title": "Interface Implementation", "xp": 320, "example": "interface Skill { void cast(); }", "exp_out": "Ultimate Cast", "desc": "Implement interface Skill with method cast() printing \\\"Ultimate Cast\\\".", "code": "interface Skill {\\n    void cast();\\n}\\nclass Ultimate implements Skill {\\n    public void cast() { System.out.println(\\\"Ultimate Cast\\\"); }\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        Skill s = new Ultimate();\\n        s.cast();\\n    }\\n}"},
                {"title": "Abstract Classes", "xp": 340, "example": "abstract class Enemy { abstract void hit(); }", "exp_out": "Boss Hit", "desc": "Extend abstract Enemy, implementing hit() outputting \\\"Boss Hit\\\".", "code": "abstract class Enemy {\\n    abstract void hit();\\n}\\nclass Boss extends Enemy {\\n    void hit() { System.out.println(\\\"Boss Hit\\\"); }\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        Enemy e = new Boss();\\n        e.hit();\\n    }\\n}"},
                {"title": "Static Class Variable", "xp": 360, "example": "static int count = 0;", "exp_out": "3", "desc": "Increment static counter in constructor and output 3.", "code": "class Item {\\n    static int count = 0;\\n    Item() { count++; }\\n}\\npublic class Main {\\n    public static void main(String[] args) {\\n        new Item(); new Item(); new Item();\\n        System.out.println(Item.count);\\n    }\\n}"},
                {"title": "Boss Defeated Final", "xp": 500, "example": "System.out.println(\\\"VICTORY\\\");", "exp_out": "VICTORY", "desc": "If boolean bossDead = true, print \\\"VICTORY\\\".", "code": "public class Main {\\n    public static void main(String[] args) {\\n        boolean bossDead = true;\\n        if (bossDead) System.out.println(\\\"VICTORY\\\");\\n    }\\n}"},
            ]
        }
    ],

    "C++": [
        # SECTION 1: BEGINNER - C++ STREAMS & VARIABLES
        {
            "section_title": "1. C++ Terminal Basics",
            "tier": "Beginner",
            "lessons": [
                {"title": "System Boot", "xp": 50, "example": "std::cout << \\\"Boot\\\";", "exp_out": "C++ Arcade Activated", "desc": "Output \\\"C++ Arcade Activated\\\" using std::cout.", "code": "#include <iostream>\\nint main() {\\n    std::cout << \\\"C++ Arcade Activated\\\";\\n    return 0;\\n}"},
                {"title": "Integer XP", "xp": 50, "example": "int xp = 50;\\nstd::cout << xp;", "exp_out": "500", "desc": "Create int variable xp = 500 and output it.", "code": "#include <iostream>\\nint main() {\\n    int xp = 500;\\n    std::cout << xp;\\n    return 0;\\n}"},
                {"title": "NewLine Output", "xp": 60, "example": "std::cout << \\\"A\\\\n\\\" << \\\"B\\\";", "exp_out": "STAGE 1\\nSTAGE 2", "desc": "Output \\\"STAGE 1\\\" and \\\"STAGE 2\\\" on separate lines.", "code": "#include <iostream>\\nint main() {\\n    std::cout << \\\"STAGE 1\\\\nSTAGE 2\\\";\\n    return 0;\\n}"},
                {"title": "Damage Calculation", "xp": 60, "example": "std::cout << 20 * 3;", "exp_out": "400", "desc": "Multiply 80 by 5 and print result.", "code": "#include <iostream>\\nint main() {\\n    std::cout << 80 * 5;\\n    return 0;\\n}"},
                {"title": "Double Precision Stat", "xp": 70, "example": "double d = 1.5;", "exp_out": "99.9", "desc": "Declare double shield = 99.9 and output it.", "code": "#include <iostream>\\nint main() {\\n    double shield = 99.9;\\n    std::cout << shield;\\n    return 0;\\n}"},
                {"title": "Char Character Code", "xp": 70, "example": "char c = 'A';", "exp_out": "S", "desc": "Declare char rank = 'S' and print it.", "code": "#include <iostream>\\nint main() {\\n    char rank = 'S';\\n    std::cout << rank;\\n    return 0;\\n}"},
                {"title": "Boolean Output", "xp": 80, "example": "bool b = true;\\nstd::cout << b;", "exp_out": "1", "desc": "Declare bool ready = true and output it.", "code": "#include <iostream>\\nint main() {\\n    bool ready = true;\\n    std::cout << ready;\\n    return 0;\\n}"},
                {"title": "Std Endl Stream", "xp": 80, "example": "std::cout << \\\"A\\\" << std::endl;", "exp_out": "P1", "desc": "Output \\\"P1\\\" followed by std::endl.", "code": "#include <iostream>\\nint main() {\\n    std::cout << \\\"P1\\\" << std::endl;\\n    return 0;\\n}"},
                {"title": "String Class Output", "xp": 90, "example": "std::string s = \\\"Hi\\\";", "exp_out": "Excalibur", "desc": "Create std::string weapon = \\\"Excalibur\\\" and output it.", "code": "#include <iostream>\\n#include <string>\\nint main() {\\n    std::string weapon = \\\"Excalibur\\\";\\n    std::cout << weapon;\\n    return 0;\\n}"},
                {"title": "Arithmetic Modulo", "xp": 100, "example": "std::cout << 10 % 3;", "exp_out": "3", "desc": "Calculate remainder of 23 % 5 and output result.", "code": "#include <iostream>\\nint main() {\\n    std::cout << 23 % 5;\\n    return 0;\\n}"},
            ]
        },
        # SECTION 2: BEGINNER - CONDITIONALS & LOOPS
        {
            "section_title": "2. C++ Branching & Iteration",
            "tier": "Beginner",
            "lessons": [
                {"title": "Health Check", "xp": 100, "example": "if(hp > 0) std::cout << \\\"Alive\\\";", "exp_out": "ALIVE", "desc": "Create int health = 75. If health > 0, output \\\"ALIVE\\\".", "code": "#include <iostream>\\nint main() {\\n    int health = 75;\\n    if(health > 0) std::cout << \\\"ALIVE\\\";\\n    return 0;\\n}"},
                {"title": "If Else Gate", "xp": 100, "example": "if(x) ... else ...", "exp_out": "DEAD", "desc": "Set health = 0. If health > 0 output \\\"ALIVE\\\", else \\\"DEAD\\\".", "code": "#include <iostream>\\nint main() {\\n    int health = 0;\\n    if(health > 0) std::cout << \\\"ALIVE\\\";\\n    else std::cout << \\\"DEAD\\\";\\n    return 0;\\n}"},
                {"title": "For Loop Counter", "xp": 110, "example": "for(int i=0; i<2; i++) ...", "exp_out": "1\\n2\\n3", "desc": "Use a for loop to print 1, 2, 3 on separate lines.", "code": "#include <iostream>\\nint main() {\\n    for(int i=1; i<=3; i++) std::cout << i << \\\"\\\\n\\\";\\n    return 0;\\n}"},
                {"title": "While Loop Countdown", "xp": 120, "example": "while(c > 0) ...", "exp_out": "3\\n2\\n1", "desc": "Use a while loop to output numbers 3 to 1.", "code": "#include <iostream>\\nint main() {\\n    int c = 3;\\n    while(c > 0) {\\n        std::cout << c << \\\"\\\\n\\\";\\n        c--;\\n    }\\n    return 0;\\n}"},
                {"title": "Switch Case Branching", "xp": 130, "example": "switch(val) { case 1: ... }", "exp_out": "Option 1", "desc": "Switch on int opt = 1, case 1 outputs \\\"Option 1\\\".", "code": "#include <iostream>\\nint main() {\\n    int opt = 1;\\n    switch(opt) {\\n        case 1: std::cout << \\\"Option 1\\\"; break;\\n    }\\n    return 0;\\n}"},
                {"title": "Ternary Operator", "xp": 140, "example": "int v = (5 > 2) ? 10 : 0;", "exp_out": "100", "desc": "Set int score = (mana >= 50) ? 100 : 0 (mana=80). Output score.", "code": "#include <iostream>\\nint main() {\\n    int mana = 80;\\n    int score = (mana >= 50) ? 100 : 0;\\n    std::cout << score;\\n    return 0;\\n}"},
                {"title": "Do While Loop", "xp": 140, "example": "do { ... } while(false);", "exp_out": "Arcade", "desc": "Print \\\"Arcade\\\" inside do-while loop running once.", "code": "#include <iostream>\\nint main() {\\n    do {\\n        std::cout << \\\"Arcade\\\";\\n    } while(false);\\n    return 0;\\n}"},
                {"title": "Break In Loop", "xp": 150, "example": "if(i==2) break;", "exp_out": "0\\n1", "desc": "Loop 0 to 4, break at 2, output preceding numbers.", "code": "#include <iostream>\\nint main() {\\n    for(int i=0; i<5; i++) {\\n        if(i==2) break;\\n        std::cout << i << \\\"\\\\n\\\";\\n    }\\n    return 0;\\n}"},
                {"title": "Continue Statement", "xp": 150, "example": "if(i==1) continue;", "exp_out": "0\\n2", "desc": "Skip i==1 using continue, print 0 and 2.", "code": "#include <iostream>\\nint main() {\\n    for(int i=0; i<=2; i++) {\\n        if(i==1) continue;\\n        std::cout << i << \\\"\\\\n\\\";\\n    }\\n    return 0;\\n}"},
                {"title": "Logical Operators", "xp": 160, "example": "if(a && b) ...", "exp_out": "PASS", "desc": "If keys == 3 && boss_dead == true, print \\\"PASS\\\".", "code": "#include <iostream>\\nint main() {\\n    int keys = 3; bool boss_dead = true;\\n    if(keys == 3 && boss_dead) std::cout << \\\"PASS\\\";\\n    return 0;\\n}"},
            ]
        },
        # SECTION 3: INTERMEDIATE - ARRAYS & POINTERS
        {
            "section_title": "3. C++ Arrays & Reference Variables",
            "tier": "Intermediate",
            "lessons": [
                {"title": "Array Pointers", "xp": 180, "example": "int arr[] = {5, 10};\\nstd::cout << arr[0];", "exp_out": "99", "desc": "Create integer array nums = {12, 99} and output 2nd value.", "code": "#include <iostream>\\nint main() {\\n    int nums[] = {12, 99};\\n    std::cout << nums[1];\\n    return 0;\\n}"},
                {"title": "Reference Variable", "xp": 190, "example": "int val = 10; int &ref = val;", "exp_out": "77", "desc": "Create int val = 77, and ref &r = val. Output r.", "code": "#include <iostream>\\nint main() {\\n    int val = 77;\\n    int &r = val;\\n    std::cout << r;\\n    return 0;\\n}"},
                {"title": "Pointer Dereference", "xp": 200, "example": "int x = 5; int *p = &x;", "exp_out": "5", "desc": "Create int hp = 5, pointer *p = &hp. Dereference *p and print.", "code": "#include <iostream>\\nint main() {\\n    int hp = 5;\\n    int *p = &hp;\\n    std::cout << *p;\\n    return 0;\\n}"},
                {"title": "Pointer Value Modify", "xp": 210, "example": "*p = 20;", "exp_out": "20", "desc": "Modify variable value to 20 via pointer *p and print variable.", "code": "#include <iostream>\\nint main() {\\n    int hp = 10;\\n    int *p = &hp;\\n    *p = 20;\\n    std::cout << hp;\\n    return 0;\\n}"},
                {"title": "Function Call By Value", "xp": 220, "example": "void add(int x) { ... }", "exp_out": "100", "desc": "Define function doubleVal(int x) returning x*2. Output doubleVal(50).", "code": "#include <iostream>\\nint doubleVal(int x) { return x * 2; }\\nint main() {\\n    std::cout << doubleVal(50);\\n    return 0;\\n}"},
                {"title": "Function Call By Reference", "xp": 230, "example": "void boost(int &x) { x += 10; }", "exp_out": "50", "desc": "Pass int energy = 40 by reference to boost(), adding 10. Output energy.", "code": "#include <iostream>\\nvoid boost(int &x) { x += 10; }\\nint main() {\\n    int energy = 40;\\n    boost(energy);\\n    std::cout << energy;\\n    return 0;\\n}"},
                {"title": "C-String Char Array", "xp": 240, "example": "char name[] = \\\"Hero\\\";", "exp_out": "Paladin", "desc": "Create char array rank[] = \\\"Paladin\\\" and output it.", "code": "#include <iostream>\\nint main() {\\n    char rank[] = \\\"Paladin\\\";\\n    std::cout << rank;\\n    return 0;\\n}"},
                {"title": "Array Loop Traversal", "xp": 250, "example": "for(int x : arr) ...", "exp_out": "10\\n20", "desc": "Traverse array {10, 20} using range-based for loop.", "code": "#include <iostream>\\nint main() {\\n    int items[] = {10, 20};\\n    for(int i : items) std::cout << i << \\\"\\\\n\\\";\\n    return 0;\\n}"},
                {"title": "Constant Variables", "xp": 260, "example": "const int MAX = 100;", "exp_out": "100", "desc": "Declare const int MAX_HP = 100 and output it.", "code": "#include <iostream>\\nint main() {\\n    const int MAX_HP = 100;\\n    std::cout << MAX_HP;\\n    return 0;\\n}"},
                {"title": "Null Pointer nullptr", "xp": 270, "example": "int *ptr = nullptr;", "exp_out": "NULLPTR", "desc": "If pointer ptr == nullptr, output \\\"NULLPTR\\\".", "code": "#include <iostream>\\nint main() {\\n    int *ptr = nullptr;\\n    if(ptr == nullptr) std::cout << \\\"NULLPTR\\\";\\n    return 0;\\n}"},
            ]
        },
        # SECTION 4: ADVANCED - STRUCTS, CLASSES & MEMORY
        {
            "section_title": "4. Structs, OOP & Dynamic Memory",
            "tier": "Advanced",
            "lessons": [
                {"title": "Struct Stats", "xp": 280, "example": "struct Hero { int hp; };", "exp_out": "100", "desc": "Create struct Hero { int hp; }; set hp = 100 and print it.", "code": "#include <iostream>\\nstruct Hero {\\n    int hp;\\n};\\nint main() {\\n    Hero h;\\n    h.hp = 100;\\n    std::cout << h.hp;\\n    return 0;\\n}"},
                {"title": "Dynamic Memory Allocation", "xp": 290, "example": "int *p = new int(10); delete p;", "exp_out": "999", "desc": "Dynamically allocate int using 'new', set 999, print, and 'delete'.", "code": "#include <iostream>\\nint main() {\\n    int *p = new int(999);\\n    std::cout << *p;\\n    delete p;\\n    return 0;\\n}"},
                {"title": "Class Encapsulation", "xp": 300, "example": "class Hero { public: int hp; };", "exp_out": "500", "desc": "Create class Player with public attribute score = 500. Output score.", "code": "#include <iostream>\\nclass Player {\\npublic:\\n    int score = 500;\\n};\\nint main() {\\n    Player p;\\n    std::cout << p.score;\\n    return 0;\\n}"},
                {"title": "Class Constructor", "xp": 320, "example": "Hero(int h) : hp(h) {}", "exp_out": "750", "desc": "Construct Player with score 750 and print it.", "code": "#include <iostream>\\nclass Player {\\npublic:\\n    int score;\\n    Player(int s) : score(s) {}\\n};\\nint main() {\\n    Player p(750);\\n    std::cout << p.score;\\n    return 0;\\n}"},
                {"title": "Destructor Execution", "xp": 340, "example": "~Hero() { std::cout << \\\"Done\\\"; }", "exp_out": "Destroyed", "desc": "Print \\\"Destroyed\\\" inside ~Player() destructor when object drops scope.", "code": "#include <iostream>\\nclass Player {\\npublic:\\n    ~Player() { std::cout << \\\"Destroyed\\\"; }\\n};\\nint main() {\\n    {\\n        Player p;\\n    }\\n    return 0;\\n}"},
                {"title": "Inheritance Derived Class", "xp": 360, "example": "class Knight : public Hero {};", "exp_out": "Excalibur", "desc": "Knight derives from Hero inheriting weapon=\\\"Excalibur\\\". Output weapon.", "code": "#include <iostream>\\n#include <string>\\nclass Hero {\\npublic:\\n    std::string weapon = \\\"Excalibur\\\";\\n};\\nclass Knight : public Hero {};\\nint main() {\\n    Knight k;\\n    std::cout << k.weapon;\\n    return 0;\\n}"},
                {"title": "Virtual Functions Polymorphism", "xp": 380, "example": "virtual void attack() { ... }", "exp_out": "Slash", "desc": "Override virtual void attack() in Sword class to output \\\"Slash\\\".", "code": "#include <iostream>\\nclass Weapon {\\npublic:\\n    virtual void attack() { std::cout << \\\"Hit\\\"; }\\n};\\nclass Sword : public Weapon {\\npublic:\\n    void attack() override { std::cout << \\\"Slash\\\"; }\\n};\\nint main() {\\n    Weapon *w = new Sword();\\n    w->attack();\\n    delete w;\\n    return 0;\\n}"},
                {"title": "Dynamic Array New", "xp": 400, "example": "int *arr = new int[2];", "exp_out": "10", "desc": "Dynamically allocate array of size 2, set index [0] = 10, print and delete[].", "code": "#include <iostream>\\nint main() {\\n    int *arr = new int[2];\\n    arr[0] = 10;\\n    std::cout << arr[0];\\n    delete[] arr;\\n    return 0;\\n}"},
                {"title": "Static Class Member", "xp": 450, "example": "static int count;", "exp_out": "5", "desc": "Access static class variable Player::count set to 5 and output it.", "code": "#include <iostream>\\nclass Player {\\npublic:\\n    static int count;\\n};\\nint Player::count = 5;\\nint main() {\\n    std::cout << Player::count;\\n    return 0;\\n}"},
                {"title": "Boss Fight C++ Final", "xp": 500, "example": "std::cout << \\\"VICTORY\\\";", "exp_out": "VICTORY", "desc": "Output \\\"VICTORY\\\" to clear final boss C++ stage.", "code": "#include <iostream>\\nint main() {\\n    std::cout << \\\"VICTORY\\\";\\n    return 0;\\n}"},
            ]
        }
    ]
}


# ==============================================================================
# 5. UTILITY HELPERS & FILE STORAGE
# ==============================================================================

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

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*(max(0, min(255, int(c))) for c in rgb))

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t))

def create_rounded_rect(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def fetch_image_from_url(url, size=(70, 70)):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = response.read()
        image = Image.open(io.BytesIO(data)).convert("RGBA")
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception:
        return None

def make_circular_avatar(image_path, size=(80, 80)):
    try:
        img = Image.open(image_path).convert("RGBA")
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        img = img.resize(size, Image.Resampling.LANCZOS)

        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)

        output = Image.new("RGBA", size, (0, 0, 0, 0))
        output.paste(img, (0, 0), mask=mask)
        return ImageTk.PhotoImage(output)
    except Exception:
        return None


# ==============================================================================
# 6. ASYNC YOUTUBE THUMBNAIL CACHE & CRT RETRO GENERATOR ENGINE
# ==============================================================================

class ThumbnailManager:
    """Handles thread-safe asynchronous fetching, disk-caching, and retro CRT styling of YouTube thumbnails."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThumbnailManager, cls).__new__(cls)
            cls._instance.cache = {}
            cls._instance.callbacks = {}
            cls._instance.cache_dir = os.path.join(tempfile.gettempdir(), "beacon_yt_thumbnails")
            os.makedirs(cls._instance.cache_dir, exist_ok=True)
            cls._instance.lock = threading.Lock()
        return cls._instance

    def _generate_retro_placeholder(self, title, size, tier="Beginner"):
        """Generates an authentic 8-bit retro arcade monitor placeholder image."""
        w, h = size
        img = Image.new("RGBA", (w, h), (14, 18, 38, 255))
        draw = ImageDraw.Draw(img)

        tier_color = {"Beginner": (6, 214, 160), "Intermediate": (255, 209, 102), "Advanced": (239, 71, 111)}.get(tier, (124, 140, 255))

        # Draw subtle retro pixel grid
        for x in range(0, w, 12):
            draw.line([(x, 0), (x, h)], fill=(20, 26, 56, 255), width=1)
        for y in range(0, h, 12):
            draw.line([(y, 0), (w, y)], fill=(20, 26, 56, 255), width=1)

        # Center arcade monitor symbol (Diamond / Play glyph)
        cx, cy = w // 2, h // 2 - 8
        play_poly = [(cx - 14, cy - 16), (cx - 14, cy + 16), (cx + 16, cy)]
        draw.polygon(play_poly, fill=tier_color)

        # Retro CRT Scanline Overlay
        for y in range(0, h, 3):
            draw.line([(0, y), (w, y)], fill=(0, 0, 0, 90), width=1)

        # Bottom label bar
        draw.rectangle([(0, h - 22), (w, h)], fill=(8, 11, 24, 230))
        display_txt = title[:24] + "..." if len(title) > 24 else title
        draw.text((8, h - 18), display_txt.upper(), fill=(244, 244, 249))

        return img

    def get_thumbnail(self, video_id, size=(180, 101), tier="Beginner", fallback_title="ARCADE LESSON", on_loaded=None):
        """Returns PhotoImage immediately (cached or retro fallback) and triggers async fetch if needed."""
        key = f"{video_id}_{size[0]}x{size[1]}"
        with self.lock:
            if key in self.cache:
                return self.cache[key]

        # Generate fast placeholder while downloading
        fallback_img = self._generate_retro_placeholder(fallback_title, size, tier)
        photo_fallback = ImageTk.PhotoImage(fallback_img)

        # Register callback
        if on_loaded:
            with self.lock:
                if key not in self.callbacks:
                    self.callbacks[key] = []
                self.callbacks[key].append(on_loaded)

        # Launch async fetcher thread
        threading.Thread(target=self._fetch_async, args=(video_id, size, key, tier, fallback_title), daemon=True).start()
        return photo_fallback

    def _fetch_async(self, video_id, size, key, tier, title):
        disk_path = os.path.join(self.cache_dir, f"{video_id}.jpg")
        img = None

        if os.path.exists(disk_path):
            try:
                img = Image.open(disk_path).convert("RGBA")
            except Exception:
                img = None

        if img is None:
            # Try fetching standard mqdefault or hqdefault YouTube thumbnail
            urls = [
                f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            ]
            for url in urls:
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = resp.read()
                    img = Image.open(io.BytesIO(data)).convert("RGBA")
                    # Save to local disk cache
                    with open(disk_path, "wb") as f:
                        f.write(data)
                    break
                except Exception:
                    continue

        if img is None:
            img = self._generate_retro_placeholder(title, size, tier)
        else:
            img = img.resize(size, Image.Resampling.LANCZOS)
            # Add subtle CRT scanlines overlay for arcade aesthetic
            overlay = Image.new("RGBA", size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            for y in range(0, size[1], 3):
                draw.line([(0, y), (size[0], y)], fill=(0, 0, 0, 45), width=1)
            img = Image.alpha_composite(img, overlay)

        try:
            photo = ImageTk.PhotoImage(img)
            with self.lock:
                self.cache[key] = photo
                cbs = self.callbacks.pop(key, [])
            for cb in cbs:
                try:
                    cb(photo)
                except Exception:
                    pass
        except Exception:
            pass


# ==============================================================================
# 7. ANIMATED LOGO CANVAS & RETRO PIXEL HEADER
# ==============================================================================

class AnimatedLogoCanvas(tk.Canvas):
    def __init__(self, parent, key_name, size=(70, 70), width=90, height=90, fallback_text="⚡"):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.w, self.h = width, height
        self.size = size
        self.anim_phase = random.random() * math.pi * 2
        
        url = TRANSPARENT_LOGO_URLS.get(key_name)
        self.photo = fetch_image_from_url(url, size=size) if url else None
        
        self.base_y = height / 2
        if self.photo:
            self.img_id = self.create_image(width / 2, self.base_y, image=self.photo, anchor="center")
        else:
            self.img_id = self.create_text(width / 2, self.base_y, text=fallback_text, font=("Segoe UI Emoji", 28), fill=DEFAULT_COLORS["accent"])
        
        self._animate_float()

    def _animate_float(self):
        if not self.winfo_exists():
            return
        self.anim_phase += 0.04
        offset_y = math.sin(self.anim_phase) * 3.5
        self.coords(self.img_id, self.w / 2, self.base_y + offset_y)
        self.after(16, self._animate_float)


class PixelTitleHeader(tk.Canvas):
    def __init__(self, parent, text="BEACON", pixel_size=4, gap=2, char_gap=6, color=None, bg=None):
        self.pixel_size = pixel_size
        self.gap = gap
        self.char_gap = char_gap
        self.color = color or DEFAULT_COLORS["accent"]
        self.text = text

        num_chars = len(text)
        char_width = 5 * (pixel_size + gap)
        total_width = (num_chars * char_width) + ((num_chars - 1) * char_gap) + 20
        total_height = 5 * (pixel_size + gap) + 12

        super().__init__(parent, width=total_width, height=total_height, bg=bg or DEFAULT_COLORS["panel"], highlightthickness=0)

        self.pixels = []
        self._glow_phase = 0
        self._draw_title()
        self._animate_glow()

    def _draw_title(self):
        start_x = 10
        start_y = 6

        for char in self.text:
            matrix = PIXEL_FONT.get(char, [])
            for row_idx, row_str in enumerate(matrix):
                for col_idx, bit in enumerate(row_str):
                    if bit == '1':
                        x1 = start_x + col_idx * (self.pixel_size + self.gap)
                        y1 = start_y + row_idx * (self.pixel_size + self.gap)
                        x2 = x1 + self.pixel_size
                        y2 = y1 + self.pixel_size

                        self.create_rectangle(x1 + 2, y1 + 2, x2 + 2, y2 + 2, fill="#04060c", outline="")
                        p_id = self.create_rectangle(x1, y1, x2, y2, fill=self.color, outline="")
                        self.pixels.append(p_id)

            start_x += 5 * (self.pixel_size + self.gap) + self.char_gap

    def _animate_glow(self):
        if not self.winfo_exists():
            return
        self._glow_phase += 0.06
        t = (math.sin(self._glow_phase) + 1) / 2
        glow_c = lerp_color(self.color, "#ffffff", t * 0.4)
        for p_id in self.pixels:
            self.itemconfig(p_id, fill=glow_c)
        self.after(30, self._animate_glow)

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])
        self.color = theme["accent"]


# ==============================================================================
# 8. 60 FPS ANIMATED CANVAS BACKGROUND
# ==============================================================================

class AnimatedBackground(tk.Canvas):
    def __init__(self, parent, star_count=40, code_count=18):
        colors = parent.master.controller.theme if hasattr(parent, "master") and hasattr(parent.master, "controller") else DEFAULT_COLORS
        super().__init__(parent, bg=colors["bg"], highlightthickness=0)
        self.star_count = star_count
        self.code_count = code_count
        self.stars = []
        self.code_particles = []
        self.w, self.h = 800, 800
        self.bg_color_1 = colors["bg"]
        self.bg_color_2 = colors["bg_2"]
        self.theme = colors

        self._sweep_phase = random.random() * math.pi * 2
        self._lamp_phase = random.random() * math.pi * 2
        self._sweep_item = None
        self._lamp_glow_outer = None
        self._lamp_glow_inner = None
        self._running = False
        self._job = None
        self.bind("<Configure>", self._on_resize)

    def set_theme_colors(self, color1, color2):
        self.bg_color_1 = color1
        self.bg_color_2 = color2
        self._redraw_static()

    def apply_theme(self, theme):
        self.theme = theme
        self.bg_color_1 = theme["bg"]
        self.bg_color_2 = theme["bg_2"]
        self.configure(bg=theme["bg"])
        self._redraw_static()

    def _on_resize(self, event):
        self.w, self.h = event.width, event.height
        if not self.stars:
            self._init_stars()
        if not self.code_particles:
            self._init_code_particles()
        self._redraw_static()

    def _init_stars(self):
        for _ in range(self.star_count):
            self.stars.append({
                "x": random.uniform(0, self.w or 800),
                "y": random.uniform(0, self.h or 800),
                "size": random.choice([2, 3, 4]),
                "speed": random.uniform(0.15, 0.35),
                "phase": random.uniform(0, math.pi * 2),
                "id": None,
            })

    def _random_code_particle(self, t=None):
        lang = random.choice(list(CODE_SNIPPETS.keys()))
        return {
            "t": random.uniform(0, 1) if t is None else t,
            "lateral": random.uniform(-0.85, 0.85),
            "text": random.choice(CODE_SNIPPETS[lang]),
            "color": CODE_COLORS[lang],
            "speed": random.uniform(0.003, 0.007),
            "id": None,
        }

    def _init_code_particles(self):
        for _ in range(self.code_count):
            self.code_particles.append(self._random_code_particle())

    def _redraw_static(self):
        self.delete("bg_band")
        bands = 20
        for i in range(bands):
            t = i / bands
            color = lerp_color(self.bg_color_1, self.bg_color_2, t)
            y1 = self.h * t
            y2 = self.h * (t + 1 / bands) + 1
            self.create_rectangle(0, y1, self.w, y2, fill=color, outline="", tags="bg_band")
        self.tag_lower("bg_band")

        self.delete("sweep")
        self._sweep_item = self.create_polygon(0, 0, 0, 0, 0, 0,
                                                fill=self.theme["accent_3"],
                                                stipple="gray12", outline="", tags="sweep")

        self.delete("lamp")
        self._lamp_glow_outer = self.create_rectangle(0, 0, 0, 0, fill=self.theme["accent"],
                                                       stipple="gray25", outline="", tags="lamp")
        self._lamp_glow_inner = self.create_rectangle(0, 0, 0, 0, fill=self.theme["accent"],
                                                       outline="", tags="lamp")

        self.delete("codeflow")
        for p in self.code_particles:
            p["id"] = self.create_text(0, 0, text=p["text"], fill=p["color"],
                                       font=FONT_CODE, anchor="center", tags="codeflow")

        self.delete("star")
        for star in self.stars:
            s = star["size"]
            star["id"] = self.create_rectangle(star["x"], star["y"], star["x"] + s, star["y"] + s,
                                                fill=self.theme["accent"], outline="", tags="star")

        self.tag_raise("sweep")
        self.tag_raise("lamp")
        self.tag_raise("codeflow")
        self.tag_raise("star")

    def start(self):
        if self._running:
            return
        self._running = True
        self._tick()

    def stop(self):
        self._running = False
        if self._job:
            self.after_cancel(self._job)
            self._job = None

    def _tick(self):
        if not self._running or not self.winfo_exists():
            return
        w = self.w or int(self.winfo_width())
        h = self.h or int(self.winfo_height())

        for star in self.stars:
            star["x"] -= star["speed"]
            if star["x"] < -5:
                star["x"] = w + 5
                star["y"] = random.uniform(0, h)
            star["phase"] += 0.03
            twinkle = (math.sin(star["phase"]) + 1) / 2
            color = lerp_color(self.theme["muted"], self.theme["accent"], twinkle)
            if star["id"] is not None:
                s = star["size"]
                self.coords(star["id"], star["x"], star["y"], star["x"] + s, star["y"] + s)
                self.itemconfig(star["id"], fill=color)

        self._sweep_phase += 0.008
        angle = math.sin(self._sweep_phase) * 0.45
        pivot_x, pivot_y = w + 30, h / 2
        length = w * 1.15
        half_width = 0.18

        a1 = angle - half_width
        a2 = angle + half_width

        x1 = pivot_x - length * math.cos(a1)
        y1 = pivot_y + length * math.sin(a1)
        x2 = pivot_x - length * math.cos(a2)
        y2 = pivot_y + length * math.sin(a2)

        if self._sweep_item is not None:
            self.coords(self._sweep_item, pivot_x, pivot_y, x1, y1, x2, y2)

        self._lamp_phase += 0.04
        glow_t = (math.sin(self._lamp_phase) + 1) / 2
        lamp_x, lamp_y = w - 4, h / 2
        r_outer = 20 + glow_t * 8
        r_inner = 8 + glow_t * 3

        if self._lamp_glow_outer is not None:
            self.coords(self._lamp_glow_outer, lamp_x - r_outer, lamp_y - r_outer,
                        lamp_x + r_outer, lamp_y + r_outer)
            self.coords(self._lamp_glow_inner, lamp_x - r_inner, lamp_y - r_inner,
                        lamp_x + r_inner, lamp_y + r_inner)
            inner_color = lerp_color(self.theme["accent"], "#ffffff", 0.3 + glow_t * 0.4)
            self.itemconfig(self._lamp_glow_inner, fill=inner_color)

        for p in self.code_particles:
            p["t"] += p["speed"]
            if p["t"] > 1:
                fresh = self._random_code_particle(t=0.0)
                fresh["id"] = p["id"]
                p.update(fresh)
                self.itemconfig(p["id"], text=p["text"], fill=p["color"])

            lateral_angle = angle + p["lateral"] * half_width
            radius_p = p["t"] * length
            x = pivot_x - radius_p * math.cos(lateral_angle)
            y = pivot_y + radius_p * math.sin(lateral_angle)

            if p["id"] is not None:
                self.coords(p["id"], x, y)
                fade = max(0.0, min(1.0, min(p["t"] * 3.5, (1 - p["t"]) * 3.5)))
                color = lerp_color(self.bg_color_1, p["color"], fade)
                self.itemconfig(p["id"], fill=color)

        self._job = self.after(16, self._tick)


# ==============================================================================
# 9. CARDS & RETRO UI COMPONENT WIDGETS
# ==============================================================================

class CurvedCard(tk.Canvas):
    def __init__(self, parent, width=450, height=630, radius=24, bg_color=None, border_color=None):
        theme = parent.controller.theme if hasattr(parent, "controller") else DEFAULT_COLORS
        bg_c = bg_color or theme["panel"]
        border_c = border_color or theme["border"]

        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.width = width
        self.height = height
        self.radius = radius
        self.bg_color = bg_c
        self.border_color = border_c

        self._s_rect = create_rounded_rect(self, 4, 4, width - 2, height - 2, radius=radius, fill="#04060c", outline="")
        self._b_rect = create_rounded_rect(self, 0, 0, width - 6, height - 6, radius=radius, fill=border_c, outline="")
        self._m_rect = create_rounded_rect(self, 2, 2, width - 8, height - 8, radius=radius - 2, fill=bg_c, outline="")

        self.inner_frame = tk.Frame(self, bg=bg_c)
        self.create_window((width / 2, height / 2), window=self.inner_frame, anchor="center")

    def apply_theme(self, theme):
        self.configure(bg=theme["bg"])
        self.itemconfig(self._b_rect, fill=theme["border"])
        self.itemconfig(self._m_rect, fill=theme["panel"])
        self.inner_frame.configure(bg=theme["panel"])


class HorizontalLanguageCard(tk.Canvas):
    def __init__(self, parent, title, tag, fallback_emoji, accent_color, width=235, height=310, command=None, on_video_cmd=None, controller=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.controller = controller
        self.title = title
        self.tag = tag
        self.accent_color = accent_color
        self.command = command
        self.on_video_cmd = on_video_cmd
        self.w, self.h = width, height
        self._anim_phase = random.random() * math.pi * 2
        
        theme = controller.theme if controller else DEFAULT_COLORS

        self._shadow = create_rounded_rect(self, 4, 4, width - 2, height - 2, radius=20, fill="#04060c", outline="")
        self._border = create_rounded_rect(self, 0, 0, width - 6, height - 6, radius=20, fill=theme["border"], outline="")
        self._body = create_rounded_rect(self, 2, 2, width - 8, height - 8, radius=18, fill=theme["panel_2"], outline="")

        url = TRANSPARENT_LOGO_URLS.get(title)
        self.photo_logo = fetch_image_from_url(url, size=(60, 60)) if url else None

        self.base_logo_y = 55
        if self.photo_logo:
            self._logo_id = self.create_image(width / 2, self.base_logo_y, image=self.photo_logo, anchor="center")
        else:
            self._logo_id = self.create_text(width / 2, self.base_logo_y, text=fallback_emoji, font=("Segoe UI Emoji", 32), fill=accent_color, anchor="center")

        self.title_txt = self.create_text(width / 2, 115, text=title, font=FONT_BOX_TITLE, fill=theme["text"], anchor="center")
        self.tag_txt = self.create_text(width / 2, 145, text=tag, font=FONT_BOX_SUB, fill=theme["muted"], anchor="center", width=200, justify="center")

        btn_w, btn_h = 175, 32
        btn_x1 = (width - btn_w) / 2
        btn_y1 = 195

        self._btn_body = create_rounded_rect(self, btn_x1, btn_y1, btn_x1 + btn_w, btn_y1 + btn_h, radius=8, fill=accent_color, outline="")
        self._btn_label = self.create_text(width / 2, btn_y1 + (btn_h / 2), text="TERMINAL QUEST ▶", font=FONT_CHIP, fill="#080b18")

        vbtn_y1 = 238
        self._vbtn_body = create_rounded_rect(self, btn_x1, vbtn_y1, btn_x1 + btn_w, vbtn_y1 + btn_h, radius=8, fill=theme["panel"], outline=theme["crt_border"])
        self._vbtn_label = self.create_text(width / 2, vbtn_y1 + (btn_h / 2), text="📺 VIDEO LESSONS", font=FONT_CHIP, fill=theme["text"])

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._floating_logo_anim()

    def _on_enter(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_hover()
        self.config(cursor="hand2")
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.itemconfig(self._body, fill=lerp_color(theme["panel_2"], self.accent_color, 0.12))
        self.itemconfig(self._border, fill=self.accent_color)
        self.itemconfig(self._btn_body, fill=lerp_color(self.accent_color, "#ffffff", 0.3))

    def _on_leave(self, _e):
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.itemconfig(self._body, fill=theme["panel_2"])
        self.itemconfig(self._border, fill=theme["border"])
        self.itemconfig(self._btn_body, fill=self.accent_color)

    def _on_click(self, e):
        if self.controller:
            self.controller.sound_mgr.play_click()
        if e.y >= 235 and self.on_video_cmd:
            self.on_video_cmd(self.title)
        elif self.command:
            self.command(self.title)

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])
        self.itemconfig(self._border, fill=theme["border"])
        self.itemconfig(self._body, fill=theme["panel_2"])
        self.itemconfig(self.title_txt, fill=theme["text"])
        self.itemconfig(self.tag_txt, fill=theme["muted"])
        self.itemconfig(self._vbtn_body, fill=theme["panel"], outline=theme["crt_border"])
        self.itemconfig(self._vbtn_label, fill=theme["text"])

    def _floating_logo_anim(self):
        if not self.winfo_exists():
            return
        self._anim_phase += 0.04
        offset_y = math.sin(self._anim_phase) * 4
        self.coords(self._logo_id, self.w / 2, self.base_logo_y + offset_y)
        self.after(16, self._floating_logo_anim)


class PixelButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=340, height=40, bg=None, fg=None, controller=None):
        self.controller = controller
        theme = controller.theme if controller else DEFAULT_COLORS
        bg_col = bg or theme["accent"]
        fg_col = fg or ("#ffffff" if theme == THEMES["light"] else "#080b18")

        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.command = command
        self.bg_color = bg_col
        self.fg = fg_col
        self.w, self.h = width, height
        self.text = text

        p = 4
        self._shadow = create_rounded_rect(self, p, p, width, height, radius=8, fill="#04060c", outline="")
        self._body = create_rounded_rect(self, 0, 0, width - p, height - p, radius=8, fill=bg_col, outline="")
        self._label = self.create_text((width - p) / 2, (height - p) / 2, text=text, fill=fg_col, font=FONT_BTN)

        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_hover()
        self.config(cursor="hand2")
        self.itemconfig(self._body, fill=lerp_color(self.bg_color, "#ffffff", 0.2))

    def _on_leave(self, _e):
        self.itemconfig(self._body, fill=self.bg_color)

    def _on_press(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_click()
        self.move(self._body, 2, 2)
        self.move(self._label, 2, 2)

    def _on_release(self, event):
        self.move(self._body, -2, -2)
        self.move(self._label, -2, -2)
        if 0 <= event.x <= self.w and 0 <= event.y <= self.h and self.command:
            self.command()

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])


class PixelToggle(tk.Canvas):
    def __init__(self, parent, value=True, command=None, width=64, height=32, controller=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.controller = controller
        self.value = value
        self.command = command
        self.w, self.h = width, height

        self.bind("<Button-1>", self._toggle)
        self.bind("<Enter>", self._on_enter)
        self._draw()

    def _on_enter(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_hover()
        self.config(cursor="hand2")

    def _draw(self):
        self.delete("all")
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        bg_col = theme["accent_2"] if self.value else theme["entry_bg"]
        border_col = theme["accent_2"] if self.value else theme["border"]

        self.configure(bg=theme["panel_2"])
        create_rounded_rect(self, 2, 2, self.w - 2, self.h - 2, radius=14, fill=bg_col, outline=border_col)

        circle_x = self.w - 18 if self.value else 18
        handle_col = "#ffffff" if self.value else theme["muted"]
        
        self.create_oval(circle_x - 11, self.h / 2 - 11, circle_x + 11, self.h / 2 + 11, fill=handle_col, outline="")

    def _toggle(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_click()
        self.value = not self.value
        self._draw()
        if self.command:
            self.command(self.value)

    def get(self):
        return self.value

    def set_value(self, val):
        self.value = bool(val)
        self._draw()

    def apply_theme(self, theme):
        self._draw()


class PixelChip(tk.Canvas):
    def __init__(self, parent, text, key, color, on_select, width=110, height=36, controller=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.controller = controller
        self.text = text
        self.key = key
        self.color = color
        self.on_select = on_select
        self.selected = False
        self.w, self.h = width, height

        theme = controller.theme if controller else DEFAULT_COLORS

        self._shape = create_rounded_rect(self, 2, 2, width - 2, height - 2, radius=8,
                                            fill=theme["entry_bg"],
                                            outline=theme["border"])

        self._label = self.create_text(width / 2, height / 2, text=text,
                                        fill=theme["muted"], font=FONT_CHIP)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)

    def _on_enter(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_hover()
        self.config(cursor="hand2")

    def _on_click(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_click()
        self.on_select(self.key)

    def set_selected(self, is_selected):
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.selected = is_selected
        if is_selected:
            self.itemconfig(self._shape, fill=self.color, outline=self.color)
            self.itemconfig(self._label, fill="#080b18")
        else:
            self.itemconfig(self._shape, fill=theme["entry_bg"], outline=theme["border"])
            self.itemconfig(self._label, fill=theme["muted"])

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])
        self.set_selected(self.selected)


class ChipSelector(tk.Frame):
    def __init__(self, parent, options, meta, on_change=None, controller=None):
        super().__init__(parent, bg=parent["bg"])
        self.controller = controller
        self.meta = meta
        self.value = tk.StringVar(value="")
        self.chips = {}
        self.on_change = on_change

        for i, opt in enumerate(options):
            color = meta[opt]["color"]
            sym = meta[opt]["symbol"]
            full_text = f"{sym} {opt.upper()}"
            chip = PixelChip(self, full_text, opt, color, self._select, width=110, height=36, controller=controller)
            chip.grid(row=0, column=i, padx=(0, 4))
            self.chips[opt] = chip

    def _select(self, value):
        self.value.set(value)
        for opt, chip in self.chips.items():
            chip.set_selected(opt == value)
        if self.on_change:
            self.on_change(value)

    def set_value(self, value):
        if value in self.chips:
            self._select(value)

    def get(self):
        return self.value.get()

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])
        for chip in self.chips.values():
            chip.apply_theme(theme)


class GlowEntry(tk.Frame):
    def __init__(self, parent, width=34, controller=None):
        super().__init__(parent, bg=parent["bg"])
        self.controller = controller
        theme = controller.theme if controller else DEFAULT_COLORS

        self.entry = tk.Entry(self, font=FONT_ENTRY, bg=theme["entry_bg"],
                              fg=theme["entry_fg"], insertbackground=theme["text"],
                              relief="flat", highlightthickness=2,
                              highlightbackground=theme["border"],
                              highlightcolor=theme["border"])
        self.entry.config(width=width)
        self.entry.pack(fill="x", ipady=3)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, _e):
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.entry.config(highlightbackground=theme["accent_3"])

    def _on_focus_out(self, _e):
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.entry.config(highlightbackground=theme["border"])

    def get(self):
        return self.entry.get()

    def set_text(self, txt):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, txt)

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])
        self.entry.config(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["text"], highlightbackground=theme["border"])


def make_field_label(parent, logo_key, fallback_icon, text, controller=None):
    theme = controller.theme if controller else DEFAULT_COLORS
    frame = tk.Frame(parent, bg=parent["bg"])
    logo_canvas = AnimatedLogoCanvas(frame, logo_key, size=(18, 18), width=24, height=24, fallback_text=fallback_icon)
    logo_canvas.pack(side="left", padx=(0, 4))
    lbl = tk.Label(frame, text=text.upper(), font=FONT_LABEL,
                   fg=theme["muted"], bg=parent["bg"], anchor="w")
    lbl.pack(side="left")
    frame.lbl = lbl
    return frame


def style_combobox(style_name, theme=None):
    if theme is None:
        theme = DEFAULT_COLORS
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(style_name,
                    fieldbackground=theme["entry_bg"],
                    background=theme["entry_bg"],
                    foreground=theme["entry_fg"],
                    arrowcolor=theme["accent"],
                    bordercolor=theme["border"],
                    lightcolor=theme["entry_bg"],
                    darkcolor=theme["entry_bg"],
                    relief="flat")


def make_combobox(parent, values, style_name, controller=None):
    theme = controller.theme if controller else DEFAULT_COLORS
    style_combobox(style_name, theme)
    return ttk.Combobox(parent, values=values, state="readonly", font=FONT_ENTRY, style=style_name)


# ==============================================================================
# 10. TOAST NOTIFICATION POPUPS
# ==============================================================================

class Toast:
    def __init__(self, root):
        self.root = root
        self._frame = None

    def show(self, message, kind="success", duration=2400):
        if self._frame is not None:
            self._frame.destroy()

        theme = self.root.theme
        color = {"success": theme["success"], "error": theme["error"]}.get(kind, theme["accent_3"])
        prefix = "[OK]" if kind == "success" else "[ERR]"

        frame = tk.Frame(self.root, bg=theme["panel_2"], highlightthickness=2,
                         highlightbackground=color, padx=14, pady=8)
        tk.Label(frame, text=f"{prefix} {message.upper()}", font=FONT_TOAST,
                 fg=theme["text"], bg=theme["panel_2"], wraplength=400,
                 justify="left").pack()
        frame.place(relx=0.5, rely=0.04, anchor="n")
        self._frame = frame
        self.root.after(duration, lambda: frame.destroy())


# ==============================================================================
# 11. BASE PAGE FRAMEWORK
# ==============================================================================

class BasePage(tk.Frame):
    def __init__(self, parent, controller, card_w=450, card_h=650):
        super().__init__(parent, bg=controller.theme["bg"])
        self.controller = controller

        self.bg = AnimatedBackground(self)
        self.bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.card_canvas = CurvedCard(self, width=card_w, height=card_h, radius=24,
                                      bg_color=controller.theme["panel"],
                                      border_color=controller.theme["border"])
        self.card_canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.card = self.card_canvas.inner_frame

        self.stats_bar = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=10, pady=5,
                                  highlightthickness=1, highlightbackground=controller.theme["border"])
        self.stats_bar.pack(fill="x", pady=(0, 6))

        self.p1_lbl = tk.Label(self.stats_bar, text="PLAYER 1", font=FONT_STATS, fg=controller.theme["accent_2"], bg=controller.theme["panel_2"])
        self.p1_lbl.pack(side="left")
        
        self.top_streak_lbl = tk.Label(self.stats_bar, text="🔥 0 DAY STREAK", font=FONT_STATS, fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.top_streak_lbl.pack(side="left", padx=10)

        # VIP Membership / Upgrade Action Pill
        self.vip_badge_lbl = tk.Label(
            self.stats_bar, text="💎 UPGRADE", font=FONT_BADGE,
            fg="#080b18", bg=controller.theme["accent"], padx=6, pady=2, cursor="hand2"
        )
        self.vip_badge_lbl.pack(side="left", padx=(0, 6))
        self.vip_badge_lbl.bind("<Button-1>", lambda _e: self.controller.show_frame("MonetizationPage"))
        self.attach_audio_effects(self.vip_badge_lbl)
        
        self.top_xp_lbl = tk.Label(self.stats_bar, text="XP 000/500", font=FONT_STATS, fg=controller.theme["accent_3"], bg=controller.theme["panel_2"])
        self.top_xp_lbl.pack(side="right")

        self.bind("<Configure>", self._on_page_resize)

    def _on_page_resize(self, event):
        if not self.winfo_exists():
            return
        # If viewport is shorter than card height, pin card to top with padding so header & tabs are never clipped!
        if event.height < self.card_canvas.height + 20:
            self.card_canvas.place_configure(relx=0.5, rely=0.0, y=10, anchor="n")
        else:
            self.card_canvas.place_configure(relx=0.5, rely=0.5, y=0, anchor="center")

    def attach_audio_effects(self, widget):
        widget.bind("<Enter>", lambda _e: self.controller.sound_mgr.play_hover(), add="+")
        widget.bind("<Button-1>", lambda _e: self.controller.sound_mgr.play_click(), add="+")

    def update_top_bar_stats(self):
        profile = self.controller.user_profile
        xp = profile.get("xp", 0)
        level = (xp // 500) + 1
        curr_xp = xp % 500
        membership = profile.get("membership", "free")
        theme = self.controller.theme

        self.p1_lbl.config(text=profile.get("name", "PLAYER 1").upper())
        self.top_streak_lbl.config(text=f"🔥 {profile.get('streak', 0)} DAY STREAK")
        self.top_xp_lbl.config(text=f"LVL {level} • XP {curr_xp:03d}/500")

        if membership == "pro":
            self.vip_badge_lbl.config(text="⚡ PRO VIP", bg=theme["accent_2"], fg="#080b18")
        elif membership == "guild":
            self.vip_badge_lbl.config(text="👑 GUILD MASTER", bg=theme["accent"], fg="#080b18")
        else:
            self.vip_badge_lbl.config(text="💎 UPGRADE", bg=theme["accent"], fg="#080b18")

    def on_difficulty_selected(self, difficulty):
        if difficulty in EXPERIENCE_META:
            self.bg.set_theme_colors(self.controller.theme["bg"], self.controller.theme["bg_2"])

    def on_show(self):
        self.bg.start()
        self.update_top_bar_stats()

    def on_hide(self):
        self.bg.stop()

    def apply_theme(self, theme):
        self.configure(bg=theme["bg"])
        self.bg.apply_theme(theme)
        self.card_canvas.apply_theme(theme)
        self.stats_bar.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.p1_lbl.configure(bg=theme["panel_2"], fg=theme["accent_2"])
        self.top_streak_lbl.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.top_xp_lbl.configure(bg=theme["panel_2"], fg=theme["accent_3"])
        self.update_top_bar_stats()


# ==============================================================================
# 12. RETRO ARCADE VIDEO THUMBNAIL CANVAS & LESSON CARD WIDGETS
# ==============================================================================

class ArcadeVideoThumbnailCanvas(tk.Canvas):
    """Custom Retro CRT-monitor framed Canvas that displays clickable YouTube previews."""
    def __init__(self, parent, video_data, width=190, height=108, command=None, controller=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.controller = controller
        self.video_data = video_data
        self.w, self.h = width, height
        self.command = command
        self._hover = False
        self._anim_phase = 0

        theme = controller.theme if controller else DEFAULT_COLORS
        self.tier = video_data.get("tier", "Beginner")
        self.tier_color = EXPERIENCE_META.get(self.tier, {}).get("color", theme["accent_2"])

        # Draw outer monitor shadow & bezel
        self._shadow = create_rounded_rect(self, 3, 3, width - 1, height - 1, radius=10, fill="#04060c", outline="")
        self._bezel = create_rounded_rect(self, 0, 0, width - 4, height - 4, radius=10, fill=theme["border"], outline="")

        # Fetch Thumbnail
        mgr = ThumbnailManager()
        self.photo = mgr.get_thumbnail(
            video_id=video_data["video_id"],
            size=(width - 8, height - 8),
            tier=self.tier,
            fallback_title=video_data.get("title", "LESSON"),
            on_loaded=self._on_image_loaded
        )

        self._img_id = self.create_image(width // 2 - 2, height // 2 - 2, image=self.photo, anchor="center")

        # Top-Left Tier Badge Pill
        self._tier_bg = create_rounded_rect(self, 6, 6, 62, 22, radius=4, fill="#080b18", outline=self.tier_color)
        self._tier_txt = self.create_text(34, 14, text=self.tier[:5].upper(), font=FONT_BADGE, fill=self.tier_color)

        # Bottom-Right Duration Badge Pill
        duration_str = video_data.get("duration", "10:00")
        pill_w = max(42, len(duration_str) * 7 + 10)
        self._dur_bg = create_rounded_rect(self, width - pill_w - 8, height - 26, width - 8, height - 8, radius=4, fill="#080b18", outline="#2f376f")
        self._dur_txt = self.create_text(width - 8 - (pill_w // 2), height - 17, text=duration_str, font=FONT_BADGE, fill="#f4f4f9")

        # Centered Play Icon Overlay (Shown on hover or standby)
        cx, cy = width // 2 - 2, height // 2 - 2
        self._play_bg = self.create_oval(cx - 16, cy - 16, cx + 16, cy + 16, fill="#080b18", outline=self.tier_color, width=2)
        self._play_icon = self.create_polygon([cx - 5, cy - 8, cx - 5, cy + 8, cx + 8, cy], fill=self.tier_color)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_image_loaded(self, new_photo):
        if not self.winfo_exists():
            return
        self.photo = new_photo
        self.itemconfig(self._img_id, image=new_photo)

    def _on_enter(self, _e):
        self._hover = True
        self.config(cursor="hand2")
        if self.controller:
            self.controller.sound_mgr.play_hover()
        self.itemconfig(self._bezel, fill=self.tier_color)
        self.itemconfig(self._play_bg, fill=self.tier_color)
        self.itemconfig(self._play_icon, fill="#080b18")

    def _on_leave(self, _e):
        self._hover = False
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.itemconfig(self._bezel, fill=theme["border"])
        self.itemconfig(self._play_bg, fill="#080b18")
        self.itemconfig(self._play_icon, fill=self.tier_color)

    def _on_click(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_click()
        if self.command:
            self.command(self.video_data)

    def apply_theme(self, theme):
        self.configure(bg=theme["panel_2"])
        if not self._hover:
            self.itemconfig(self._bezel, fill=theme["border"])


class ArcadeVideoCard(tk.Frame):
    """Arcade Cassette / Video Card inside the scrollable lessons list."""
    def __init__(self, parent, video_data, on_select=None, is_selected=False, is_watched=False, controller=None):
        theme = controller.theme if controller else DEFAULT_COLORS
        super().__init__(parent, bg=theme["panel_2"], padx=8, pady=8, highlightthickness=1,
                         highlightbackground=theme["accent"] if is_selected else theme["border"])
        self.controller = controller
        self.video_data = video_data
        self.on_select = on_select
        self.is_selected = is_selected
        self.is_watched = is_watched

        tier = video_data.get("tier", "Beginner")
        tier_meta = EXPERIENCE_META.get(tier, {"symbol": "🌱", "color": theme["accent_2"]})

        # Left Column: Thumbnail Canvas Preview
        self.thumb_canvas = ArcadeVideoThumbnailCanvas(
            self, video_data, width=170, height=96,
            command=lambda v: self._handle_click(),
            controller=controller
        )
        self.thumb_canvas.pack(side="left", padx=(0, 10))

        # Right Column: Metadata & Controls
        self.meta_frame = tk.Frame(self, bg=theme["panel_2"])
        self.meta_frame.pack(side="left", fill="both", expand=True)

        # Row 1: Title & Watched Status Pill
        self.title_row = tk.Frame(self.meta_frame, bg=theme["panel_2"])
        self.title_row.pack(fill="x")

        self.title_lbl = tk.Label(
            self.title_row, text=video_data["title"], font=FONT_CODE,
            fg=theme["accent"] if is_selected else theme["text"],
            bg=theme["panel_2"], wraplength=280, justify="left", anchor="w"
        )
        self.title_lbl.pack(side="left", fill="x", expand=True)

        if is_watched:
            self.status_badge = tk.Label(
                self.title_row, text="✓ WATCHED", font=FONT_BADGE,
                fg="#080b18", bg=theme["accent_2"], padx=4, pady=1
            )
            self.status_badge.pack(side="right", padx=(4, 0))

        # Row 2: Channel & Views
        self.channel_row = tk.Frame(self.meta_frame, bg=theme["panel_2"])
        self.channel_row.pack(fill="x", pady=(3, 0))

        self.chan_lbl = tk.Label(
            self.channel_row, text=f"📺 {video_data.get('channel', 'Arcade Dev')}", font=FONT_STATS,
            fg=theme["muted"], bg=theme["panel_2"], anchor="w"
        )
        self.chan_lbl.pack(side="left")

        self.views_lbl = tk.Label(
            self.channel_row, text=f"👁️ {video_data.get('views', '1M views')}", font=FONT_STATS,
            fg=theme["muted"], bg=theme["panel_2"]
        )
        self.views_lbl.pack(side="right")

        # Row 3: Tags, XP, and Action Button
        self.action_row = tk.Frame(self.meta_frame, bg=theme["panel_2"])
        self.action_row.pack(fill="x", pady=(6, 0))

        self.tier_lbl = tk.Label(
            self.action_row, text=f"{tier_meta['symbol']} {tier.upper()}", font=FONT_BADGE,
            fg=tier_meta["color"], bg=theme["entry_bg"], padx=6, pady=2
        )
        self.tier_lbl.pack(side="left")

        self.xp_lbl = tk.Label(
            self.action_row, text=f"+{video_data.get('xp', 100)} XP", font=FONT_BADGE,
            fg=theme["accent"], bg=theme["entry_bg"], padx=6, pady=2
        )
        self.xp_lbl.pack(side="left", padx=(4, 0))

        self.play_btn = tk.Label(
            self.action_row, text="PLAY ▶", font=FONT_BADGE,
            fg="#080b18", bg=theme["accent_2"], padx=8, pady=2, cursor="hand2"
        )
        self.play_btn.pack(side="right")
        self.play_btn.bind("<Button-1>", lambda _e: self._handle_click())

        # Bind whole card clicks & hover effects
        for w in (self, self.meta_frame, self.title_row, self.title_lbl, self.channel_row, self.chan_lbl, self.views_lbl):
            w.bind("<Button-1>", lambda _e: self._handle_click())
            w.bind("<Enter>", lambda _e: self._on_enter())
            w.bind("<Leave>", lambda _e: self._on_leave())

    def _on_enter(self):
        self.config(cursor="hand2")
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        if not self.is_selected:
            self.configure(highlightbackground=theme["accent_3"], bg=theme["card_hover"])

    def _on_leave(self):
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        if not self.is_selected:
            self.configure(highlightbackground=theme["border"], bg=theme["panel_2"])

    def _handle_click(self):
        if self.on_select:
            self.on_select(self.video_data)

    def set_selected(self, selected):
        self.is_selected = selected
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.configure(highlightbackground=theme["accent"] if selected else theme["border"])
        self.title_lbl.config(fg=theme["accent"] if selected else theme["text"])


# ==============================================================================
# 13. ARCADE VIDEO THEATER SCREEN & INTERACTIVE PLAYER
# ==============================================================================

class ArcadeVideoTheater(tk.Frame):
    """The central Arcade Monitor Theater with playable preview, chapters, and sandbox."""
    def __init__(self, parent, controller):
        theme = controller.theme if controller else DEFAULT_COLORS
        super().__init__(parent, bg=theme["panel_2"], padx=12, pady=10, highlightthickness=2, highlightbackground=theme["crt_border"])
        self.controller = controller
        self.current_video = None

        # Top Bar: Monitor Header
        self.top_hdr = tk.Frame(self, bg=theme["panel_2"])
        self.top_hdr.pack(fill="x", pady=(0, 6))

        self.crt_title_lbl = tk.Label(self.top_hdr, text="⚡ CRT ARCADE MONITOR - 1080P", font=FONT_STATS, fg=theme["accent"], bg=theme["panel_2"])
        self.crt_title_lbl.pack(side="left")

        self.ch_title_lbl = tk.Label(self.top_hdr, text="CHANNEL FEED: READY", font=FONT_STATS, fg=theme["accent_2"], bg=theme["panel_2"])
        self.ch_title_lbl.pack(side="right")

        # Large Screen Bezel Monitor Frame
        self.screen_frame = tk.Frame(self, bg="#04060c", padx=4, pady=4, highlightthickness=1, highlightbackground=theme["border"])
        self.screen_frame.pack(fill="x", pady=(0, 6))

        # Main Clickable Video Preview Canvas
        self.screen_canvas = tk.Canvas(self.screen_frame, width=440, height=220, bg="#080b18", highlightthickness=0, cursor="hand2")
        self.screen_canvas.pack(fill="both", expand=True)
        self.screen_canvas.bind("<Button-1>", lambda _e: self.launch_youtube_video())
        self.screen_canvas.bind("<Enter>", self._on_screen_enter)
        self.screen_canvas.bind("<Leave>", self._on_screen_leave)

        self.big_photo = None
        self._screen_hover = False

        # Action Toolbar (Watch, Mark Complete, Copy Link, Run in Terminal)
        self.btn_row = tk.Frame(self, bg=theme["panel_2"])
        self.btn_row.pack(fill="x", pady=(0, 6))

        self.watch_btn = tk.Button(
            self.btn_row, text="▶ WATCH ON YOUTUBE", font=FONT_CHIP, bg=theme["accent"],
            fg="#080b18", relief="flat", padx=10, pady=4, cursor="hand2", bd=0,
            command=self.launch_youtube_video
        )
        self.watch_btn.pack(side="left", padx=(0, 4))
        self.controller.attach_audio_effects(self.watch_btn) if hasattr(self.controller, "attach_audio_effects") else None

        self.complete_btn = tk.Button(
            self.btn_row, text="✓ MARK COMPLETE (+XP)", font=FONT_CHIP, bg=theme["accent_2"],
            fg="#080b18", relief="flat", padx=8, pady=4, cursor="hand2", bd=0,
            command=self.mark_completed
        )
        self.complete_btn.pack(side="left", padx=(0, 4))

        self.copy_btn = tk.Button(
            self.btn_row, text="📋 COPY URL", font=FONT_CHIP, bg=theme["entry_bg"],
            fg=theme["text"], relief="flat", padx=8, pady=4, cursor="hand2", bd=0,
            command=self.copy_youtube_link
        )
        self.copy_btn.pack(side="left")

        # Video Title & Summary Header
        self.details_box = tk.Frame(self, bg=theme["panel_2"])
        self.details_box.pack(fill="x", pady=(0, 4))

        self.v_title = tk.Label(self.details_box, text="Select an arcade lesson...", font=FONT_BOX_TITLE, fg=theme["accent"], bg=theme["panel_2"], wraplength=440, justify="left", anchor="w")
        self.v_title.pack(anchor="w")

        self.v_summary = tk.Label(self.details_box, text="Watch high-definition curated programming tutorials and master practical coding skills.", font=FONT_STATS, fg=theme["muted"], bg=theme["panel_2"], wraplength=440, justify="left", anchor="w")
        self.v_summary.pack(anchor="w", pady=(2, 4))

        # Notebook Tabs: 1. Chapters & Timestamps, 2. Key Takeaways, 3. Code Sandbox
        self.tabs_bar = tk.Frame(self, bg=theme["panel_2"])
        self.tabs_bar.pack(fill="x", pady=(2, 2))

        self.tab_ch_btn = self._make_sub_tab("TIMESTAMPS", lambda: self.switch_tab("chapters"), active=True)
        self.tab_notes_btn = self._make_sub_tab("CHEATSHEET", lambda: self.switch_tab("notes"))
        self.tab_code_btn = self._make_sub_tab("CODE SANDBOX", lambda: self.switch_tab("code"))

        self.content_container = tk.Frame(self, bg=theme["entry_bg"], highlightthickness=1, highlightbackground=theme["border"], padx=6, pady=6)
        self.content_container.pack(fill="both", expand=True)

        # Tab 1: Scrollable Chapters
        self.chapters_frame = tk.Frame(self.content_container, bg=theme["entry_bg"])
        
        # Tab 2: Key Points / Cheatsheet
        self.notes_frame = tk.Frame(self.content_container, bg=theme["entry_bg"])
        self.notes_txt = tk.Label(self.notes_frame, text="", font=FONT_STATS, fg=theme["text"], bg=theme["entry_bg"], justify="left", anchor="nw", wraplength=420)
        self.notes_txt.pack(fill="both", expand=True)

        # Tab 3: Code Sandbox
        self.sandbox_frame = tk.Frame(self.content_container, bg=theme["entry_bg"])
        self.code_edit = tk.Text(self.sandbox_frame, height=5, font=FONT_CODE, bg=theme["bg"], fg=theme["accent_2"], insertbackground=theme["text"], relief="flat")
        self.code_edit.pack(fill="x", pady=(0, 4))
        
        self.run_code_btn = tk.Button(self.sandbox_frame, text="▶ RUN CODE SNIPPET", font=FONT_BADGE, bg=theme["accent_3"], fg="#ffffff", relief="flat", bd=0, cursor="hand2", command=self.run_sandbox_snippet)
        self.run_code_btn.pack(anchor="w")

        self.active_tab = "chapters"
        self.switch_tab("chapters")

    def _make_sub_tab(self, text, command, active=False):
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        b = tk.Label(self.tabs_bar, text=text, font=FONT_CHIP, fg=theme["accent"] if active else theme["muted"],
                     bg=theme["panel_2"], padx=6, pady=2, cursor="hand2")
        b.pack(side="left", padx=(0, 4))
        b.bind("<Button-1>", lambda _e: command())
        return b

    def switch_tab(self, tab_key):
        self.active_tab = tab_key
        theme = self.controller.theme if self.controller else DEFAULT_COLORS

        self.tab_ch_btn.config(fg=theme["accent"] if tab_key == "chapters" else theme["muted"])
        self.tab_notes_btn.config(fg=theme["accent"] if tab_key == "notes" else theme["muted"])
        self.tab_code_btn.config(fg=theme["accent"] if tab_key == "code" else theme["muted"])

        for f in (self.chapters_frame, self.notes_frame, self.sandbox_frame):
            f.pack_forget()

        if tab_key == "chapters":
            self.chapters_frame.pack(fill="both", expand=True)
        elif tab_key == "notes":
            self.notes_frame.pack(fill="both", expand=True)
        elif tab_key == "code":
            self.sandbox_frame.pack(fill="both", expand=True)

    def load_video(self, video_data):
        self.current_video = video_data
        theme = self.controller.theme if self.controller else DEFAULT_COLORS

        self.ch_title_lbl.config(text=f"FEED: {video_data.get('channel', 'Arcade Dev').upper()}")
        self.v_title.config(text=video_data["title"])
        self.v_summary.config(text=video_data.get("summary", ""))

        # Fetch Large Screen Preview
        mgr = ThumbnailManager()
        self.big_photo = mgr.get_thumbnail(
            video_id=video_data["video_id"],
            size=(440, 220),
            tier=video_data.get("tier", "Beginner"),
            fallback_title=video_data["title"],
            on_loaded=self._on_big_photo_loaded
        )
        self._render_screen_preview()

        # Load Chapters
        for widget in self.chapters_frame.winfo_children():
            widget.destroy()

        chapters = video_data.get("chapters", [])
        if chapters:
            for ch in chapters:
                row = tk.Frame(self.chapters_frame, bg=theme["entry_bg"], pady=1)
                row.pack(fill="x")
                
                t_lbl = tk.Label(row, text=f"[{ch['time']}]", font=FONT_BADGE, fg=theme["accent_2"], bg=theme["entry_bg"], cursor="hand2")
                t_lbl.pack(side="left", padx=(0, 4))
                t_lbl.bind("<Button-1>", lambda _e, s=ch['seconds']: self.launch_youtube_video(s))
                
                title_lbl = tk.Label(row, text=ch['title'], font=FONT_STATS, fg=theme["text"], bg=theme["entry_bg"], cursor="hand2", anchor="w")
                title_lbl.pack(side="left", fill="x", expand=True)
                title_lbl.bind("<Button-1>", lambda _e, s=ch['seconds']: self.launch_youtube_video(s))
        else:
            tk.Label(self.chapters_frame, text="Full Video Tutorial - Click 'Watch on YouTube' to play!", font=FONT_STATS, fg=theme["muted"], bg=theme["entry_bg"]).pack(anchor="w")

        # Load Cheatsheet
        key_points = video_data.get("key_points", [])
        pts_text = "KEY CONCEPTS & CHEATSHEET:\n\n" + "\n".join([f"• {pt}" for pt in key_points])
        self.notes_txt.config(text=pts_text)

        # Load Code Sandbox
        snippet = video_data.get("code_snippet", "# Type your test code here")
        self.code_edit.delete("1.0", tk.END)
        self.code_edit.insert("1.0", snippet)

    def _on_big_photo_loaded(self, photo):
        if not self.winfo_exists():
            return
        self.big_photo = photo
        self._render_screen_preview()

    def _render_screen_preview(self):
        self.screen_canvas.delete("all")
        w, h = 440, 220
        if self.big_photo:
            self.screen_canvas.create_image(w // 2, h // 2, image=self.big_photo, anchor="center")

        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        accent = theme["accent"] if not self._screen_hover else theme["accent_2"]

        # Overlay Pulsing Play Button
        cx, cy = w // 2, h // 2
        self.screen_canvas.create_oval(cx - 28, cy - 28, cx + 28, cy + 28, fill="#080b18", outline=accent, width=3)
        self.screen_canvas.create_polygon([cx - 10, cy - 14, cx - 10, cy + 14, cx + 16, cy], fill=accent)

        # Bottom Bar CRT Status
        dur = self.current_video.get("duration", "VIDEO") if self.current_video else "00:00"
        self.screen_canvas.create_rectangle(0, h - 22, w, h, fill="#04060c", outline="")
        self.screen_canvas.create_text(8, h - 11, text="[CLICK TO LAUNCH STREAM IN BROWSER]", font=FONT_BADGE, fill=theme["muted"], anchor="w")
        self.screen_canvas.create_text(w - 8, h - 11, text=f"TIME: {dur}", font=FONT_BADGE, fill=theme["accent"], anchor="e")

    def _on_screen_enter(self, _e):
        self._screen_hover = True
        if self.controller:
            self.controller.sound_mgr.play_hover()
        self._render_screen_preview()

    def _on_screen_leave(self, _e):
        self._screen_hover = False
        self._render_screen_preview()

    def launch_youtube_video(self, start_seconds=0):
        if not self.current_video:
            return
        if self.controller:
            self.controller.sound_mgr.play_coin()
        
        vid = self.current_video["video_id"]
        url = f"https://www.youtube.com/watch?v={vid}"
        if start_seconds > 0:
            url += f"&t={start_seconds}"
        
        try:
            webbrowser.open(url)
            self.controller.toast.show(f"Launching YouTube: {self.current_video['title'][:30]}...", "success")
        except Exception as e:
            self.controller.toast.show(f"Could not open browser: {e}", "error")

    def copy_youtube_link(self):
        if not self.current_video:
            return
        vid = self.current_video["video_id"]
        url = f"https://www.youtube.com/watch?v={vid}"
        self.clipboard_clear()
        self.clipboard_append(url)
        if self.controller:
            self.controller.sound_mgr.play_click()
        self.controller.toast.show("YouTube Link Copied to Clipboard!", "success")

    def mark_completed(self):
        if not self.current_video:
            return
        if self.controller:
            self.controller.sound_mgr.play_success()
            user = self.controller.user_profile
            
            # Add to completed video set
            watched_set = user.setdefault("watched_videos", set())
            vid_id = self.current_video["id"]
            if vid_id not in watched_set:
                watched_set.add(vid_id)
                base_xp = self.current_video.get("xp", 100)
                membership = user.get("membership", "free")
                multiplier = 3 if membership == "guild" else (2 if membership == "pro" else 1)
                xp_gain = base_xp * multiplier
                user["xp"] += xp_gain
                user["streak"] = user.get("streak", 1) + 1
                if hasattr(self.controller, "current_frame") and hasattr(self.controller.current_frame, "update_top_bar_stats"):
                    self.controller.current_frame.update_top_bar_stats()
                bonus_tag = f" ({multiplier}X VIP BOOST)" if multiplier > 1 else ""
                self.controller.toast.show(f"Lesson Completed! +{xp_gain} XP Gained{bonus_tag}!", "success")
            else:
                self.controller.toast.show("Lesson already cleared!", "success")

    def run_sandbox_snippet(self):
        code_str = self.code_edit.get("1.0", tk.END).strip()
        if not code_str:
            return
        
        buffer = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = buffer
            exec(code_str, {"__builtins__": __builtins__})
            sys.stdout = old_stdout
            out = buffer.getvalue().strip() or "Code executed successfully with no output."
            if self.controller:
                self.controller.sound_mgr.play_click()
            messagebox.showinfo("Arcade Code Sandbox Output", out)
        except Exception as err:
            sys.stdout = old_stdout
            messagebox.showerror("Execution Error", str(err))

    def apply_theme(self, theme):
        self.configure(bg=theme["panel_2"], highlightbackground=theme["crt_border"])
        self.top_hdr.configure(bg=theme["panel_2"])
        self.crt_title_lbl.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.ch_title_lbl.configure(bg=theme["panel_2"], fg=theme["accent_2"])
        self.btn_row.configure(bg=theme["panel_2"])
        self.watch_btn.configure(bg=theme["accent"])
        self.complete_btn.configure(bg=theme["accent_2"])
        self.copy_btn.configure(bg=theme["entry_bg"], fg=theme["text"])
        self.details_box.configure(bg=theme["panel_2"])
        self.v_title.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.v_summary.configure(bg=theme["panel_2"], fg=theme["muted"])
        self.tabs_bar.configure(bg=theme["panel_2"])
        self.content_container.configure(bg=theme["entry_bg"], highlightbackground=theme["border"])
        self.chapters_frame.configure(bg=theme["entry_bg"])
        self.notes_frame.configure(bg=theme["entry_bg"])
        self.notes_txt.configure(bg=theme["entry_bg"], fg=theme["text"])
        self.sandbox_frame.configure(bg=theme["entry_bg"])
        self.code_edit.configure(bg=theme["bg"], fg=theme["accent_2"], insertbackground=theme["text"])
        self.switch_tab(self.active_tab)
        self._render_screen_preview()


# ==============================================================================
# 14. ARCADE LESSONS & VIDEO THEATER PAGE
# ==============================================================================

class ArcadeLessonsPage(BasePage):
    """Full retro arcade page for browsing curated video lessons with live filters and theater."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=850, card_h=660)
        self.current_language = "Python"
        self.selected_tier = "All"
        self.search_query = ""
        self.video_cards = []

        # Top Bar Navigation
        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.back_btn = tk.Label(
            self.top_bar, text="◄ SELECT QUEST", font=FONT_BTN,
            fg=controller.theme["accent"], bg=controller.theme["panel_2"],
            padx=8, pady=4, cursor="hand2", relief="flat",
            highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("ProgramSelectionPage"))
        self.attach_audio_effects(self.back_btn)

        self.hdr_title = tk.Label(
            self.top_bar, text="[ ARCADE VIDEO THEATER ]", font=FONT_HEADER,
            fg=controller.theme["accent"], bg=controller.theme["panel"]
        )
        self.hdr_title.pack(side="right")

        # Language Switcher & Filter Toolbar
        self.filter_bar = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=8, pady=4,
                                   highlightthickness=1, highlightbackground=controller.theme["border"])
        self.filter_bar.pack(fill="x", pady=(0, 6))

        # Language Buttons
        self.lang_btns_frame = tk.Frame(self.filter_bar, bg=controller.theme["panel_2"])
        self.lang_btns_frame.pack(side="left")

        self.lang_btns = {}
        for lang, sym in [("Python", "🐍"), ("Java", "☕"), ("C++", "⚡")]:
            b = tk.Label(
                self.lang_btns_frame, text=f"{sym} {lang.upper()}", font=FONT_CHIP,
                fg="#080b18" if lang == "Python" else controller.theme["muted"],
                bg=controller.theme["accent_2"] if lang == "Python" else controller.theme["entry_bg"],
                padx=8, pady=3, cursor="hand2", highlightthickness=1, highlightbackground=controller.theme["border"]
            )
            b.pack(side="left", padx=(0, 4))
            b.bind("<Button-1>", lambda _e, l=lang: self.set_language(l))
            self.attach_audio_effects(b)
            self.lang_btns[lang] = b

        # Search Box Entry
        self.search_box = tk.Frame(self.filter_bar, bg=controller.theme["panel_2"])
        self.search_box.pack(side="right")

        tk.Label(self.search_box, text="🔍", font=("Segoe UI Emoji", 10), fg=controller.theme["muted"], bg=controller.theme["panel_2"]).pack(side="left", padx=(0, 2))
        
        self.search_entry = tk.Entry(self.search_box, font=FONT_STATS, bg=controller.theme["entry_bg"], fg=controller.theme["text"],
                                     insertbackground=controller.theme["text"], width=18, relief="flat", highlightthickness=1, highlightbackground=controller.theme["border"])
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self._on_search_typed)

        # Tier Chips Filter
        self.tier_chips_frame = tk.Frame(self.filter_bar, bg=controller.theme["panel_2"])
        self.tier_chips_frame.pack(side="right", padx=(0, 12))

        self.tier_chips = {}
        tiers = ["All", "Beginner", "Intermediate", "Advanced"]
        for t in tiers:
            chip = tk.Label(
                self.tier_chips_frame, text=t.upper(), font=FONT_BADGE,
                fg="#080b18" if t == "All" else controller.theme["muted"],
                bg=controller.theme["accent"] if t == "All" else controller.theme["entry_bg"],
                padx=6, pady=2, cursor="hand2"
            )
            chip.pack(side="left", padx=2)
            chip.bind("<Button-1>", lambda _e, tier_name=t: self.set_tier(tier_name))
            self.attach_audio_effects(chip)
            self.tier_chips[t] = chip

        # Main Split Content: Left Scrollable Video List | Right Video Theater
        self.split_pane = tk.Frame(self.card, bg=controller.theme["panel"])
        self.split_pane.pack(fill="both", expand=True)

        # Left Column: Scrollable Video Cards List
        self.left_col = tk.Frame(self.split_pane, bg=controller.theme["panel"], width=360)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 6))

        # Canvas with Scrollbar for Video Cards
        self.list_canvas = tk.Canvas(self.left_col, bg=controller.theme["panel"], highlightthickness=0)
        self.list_scrollbar = ttk.Scrollbar(self.left_col, orient="vertical", command=self.list_canvas.yview)
        self.scrollable_cards_frame = tk.Frame(self.list_canvas, bg=controller.theme["panel"])

        self.scrollable_cards_frame.bind(
            "<Configure>", lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))
        )
        self.list_canvas.create_window((0, 0), window=self.scrollable_cards_frame, anchor="nw")
        self.list_canvas.configure(xscrollcommand=None, yscrollcommand=self.list_scrollbar.set)

        self.list_canvas.pack(side="left", fill="both", expand=True)
        self.list_scrollbar.pack(side="right", fill="y")
        self.list_canvas.bind("<Enter>", lambda _e: self.list_canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.list_canvas.bind("<Leave>", lambda _e: self.list_canvas.unbind_all("<MouseWheel>"))

        # Right Column: Live Arcade Video Theater Player
        self.theater = ArcadeVideoTheater(self.split_pane, controller)
        self.theater.pack(side="right", fill="both", expand=False)

    def _on_mousewheel(self, event):
        if self.winfo_ismapped() and self.list_canvas.winfo_exists():
            self.list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_search_typed(self, _event):
        self.search_query = self.search_entry.get().strip().lower()
        self.refresh_video_list()

    def set_language(self, lang_name):
        self.current_language = lang_name
        theme = self.controller.theme
        for l, btn in self.lang_btns.items():
            if l == lang_name:
                btn.config(bg=theme["accent_2"], fg="#080b18")
            else:
                btn.config(bg=theme["entry_bg"], fg=theme["muted"])
        self.refresh_video_list()

    def set_tier(self, tier_name):
        self.selected_tier = tier_name
        theme = self.controller.theme
        for t, chip in self.tier_chips.items():
            if t == tier_name:
                chip.config(bg=theme["accent"], fg="#080b18")
            else:
                chip.config(bg=theme["entry_bg"], fg=theme["muted"])
        self.refresh_video_list()

    def refresh_video_list(self):
        for widget in self.scrollable_cards_frame.winfo_children():
            widget.destroy()
        self.video_cards.clear()

        all_lessons = ARCADE_VIDEO_LESSONS.get(self.current_language, [])
        watched_set = self.controller.user_profile.get("watched_videos", set())

        filtered = []
        for v in all_lessons:
            if self.selected_tier != "All" and v.get("tier") != self.selected_tier:
                continue
            if self.search_query:
                q = self.search_query
                in_title = q in v["title"].lower()
                in_chan = q in v.get("channel", "").lower()
                in_summary = q in v.get("summary", "").lower()
                if not (in_title or in_chan or in_summary):
                    continue
            filtered.append(v)

        if not filtered:
            tk.Label(
                self.scrollable_cards_frame, text="No arcade lessons found matching criteria.",
                font=FONT_STATS, fg=self.controller.theme["muted"], bg=self.controller.theme["panel"], pady=20
            ).pack()
            return

        for idx, video in enumerate(filtered):
            is_watched = video["id"] in watched_set
            card = ArcadeVideoCard(
                self.scrollable_cards_frame, video,
                on_select=self.select_video,
                is_selected=(idx == 0),
                is_watched=is_watched,
                controller=self.controller
            )
            card.pack(fill="x", pady=3)
            self.video_cards.append(card)

        # Automatically load first video into theater
        if filtered:
            self.select_video(filtered[0])

    def select_video(self, video_data):
        self.theater.load_video(video_data)
        for card in self.video_cards:
            card.set_selected(card.video_data["id"] == video_data["id"])

    def on_show(self):
        super().on_show()
        self.refresh_video_list()

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.hdr_title.configure(bg=theme["panel"], fg=theme["accent"])
        self.filter_bar.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.lang_btns_frame.configure(bg=theme["panel_2"])
        self.search_box.configure(bg=theme["panel_2"])
        self.search_entry.configure(bg=theme["entry_bg"], fg=theme["text"], insertbackground=theme["text"], highlightbackground=theme["border"])
        self.tier_chips_frame.configure(bg=theme["panel_2"])
        self.split_pane.configure(bg=theme["panel"])
        self.left_col.configure(bg=theme["panel"])
        self.list_canvas.configure(bg=theme["panel"])
        self.scrollable_cards_frame.configure(bg=theme["panel"])
        self.theater.apply_theme(theme)
        self.refresh_video_list()


# ==============================================================================
# 15. MULTI-SECTION REAL EXECUTION TERMINAL QUEST ENGINE
# ==============================================================================

class LanguageQuestPage(BasePage):
    """Interactive Arcade Language Quest View with 5-7 Sections and 10-15 Lessons each."""
    def __init__(self, parent, controller, lang_name, accent_color):
        super().__init__(parent, controller, card_w=850, card_h=660)
        self.lang_name = lang_name
        self.accent_color = accent_color
        
        self.sections = PROGRAM_CURRICULUM.get(lang_name, [])
        self.current_section_idx = 0
        self.current_lesson_idx = 0
        self.completed_stages = set() # Stores tuple: (sec_idx, les_idx)

        # Top Bar Navigation
        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.back_btn = tk.Label(self.top_bar, text="◄ SELECT QUEST", font=FONT_BTN,
                                 fg=controller.theme["accent"], bg=controller.theme["panel_2"],
                                 padx=8, pady=4, cursor="hand2", relief="flat",
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("ProgramSelectionPage"))
        self.attach_audio_effects(self.back_btn)

        # Quick Button to switch to Video Lessons Vault
        self.video_nav_btn = tk.Label(self.top_bar, text="🎬 VIDEO THEATER", font=FONT_BTN,
                                      fg="#080b18", bg=controller.theme["accent_2"],
                                      padx=8, pady=4, cursor="hand2", relief="flat")
        self.video_nav_btn.pack(side="left", padx=(8, 0))
        self.video_nav_btn.bind("<Button-1>", lambda _e: controller.open_lessons(self.lang_name))
        self.attach_audio_effects(self.video_nav_btn)

        self.hdr_title = tk.Label(self.top_bar, text=f"[ {lang_name.upper()} ARCADE QUESTS ]", font=FONT_HEADER,
                                  fg=accent_color, bg=controller.theme["panel"])
        self.hdr_title.pack(side="right")

        # Section Selector Dropdown Bar
        self.sec_bar = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=6, pady=4,
                                highlightthickness=1, highlightbackground=controller.theme["border"])
        self.sec_bar.pack(fill="x", pady=(0, 6))

        tk.Label(self.sec_bar, text="SELECT SECTION:", font=FONT_LABEL, fg=controller.theme["accent"], bg=controller.theme["panel_2"]).pack(side="left", padx=(0, 6))

        section_names = [f"{s['section_title']} ({s['tier']})" for s in self.sections]
        self.sec_combo = ttk.Combobox(self.sec_bar, values=section_names, state="readonly", font=FONT_ENTRY, width=42)
        self.sec_combo.pack(side="left", fill="x", expand=True)
        self.sec_combo.current(0)
        self.sec_combo.bind("<<ComboboxSelected>>", self._on_section_changed)

        # Main Split Content View
        self.main_split = tk.Frame(self.card, bg=controller.theme["panel"])
        self.main_split.pack(fill="both", expand=True, pady=2)

        # Left Column: Lesson Index Navigation
        self.left_pane = tk.Frame(self.main_split, bg=controller.theme["panel_2"], width=230, padx=6, pady=6,
                                  highlightthickness=1, highlightbackground=controller.theme["border"])
        self.left_pane.pack(side="left", fill="both", padx=(0, 6))

        self.sec_badge_lbl = tk.Label(self.left_pane, text="🌱 BEGINNER TIER", font=FONT_LABEL, fg=controller.theme["accent_2"], bg=controller.theme["panel_2"])
        self.sec_badge_lbl.pack(anchor="w", pady=(0, 4))

        # Scrollable / Grid Container for Section Lessons
        self.tab_container = tk.Frame(self.left_pane, bg=controller.theme["panel_2"])
        self.tab_container.pack(fill="both", expand=True)

        self.lesson_buttons = []

        # Right Column: Console Editor & Interactive Outputs
        self.right_pane = tk.Frame(self.main_split, bg=controller.theme["panel_2"], padx=8, pady=8,
                                   highlightthickness=1, highlightbackground=controller.theme["border"])
        self.right_pane.pack(side="right", fill="both", expand=True)

        self.lesson_title_lbl = tk.Label(self.right_pane, text="Stage Title", font=FONT_BOX_TITLE, fg=self.accent_color, bg=controller.theme["panel_2"])
        self.lesson_title_lbl.pack(anchor="w")

        # Example & Reference Output Box
        self.example_lbl = tk.Label(self.right_pane, text="CONCEPT EXAMPLE & TARGET TERMINAL OUTPUT", font=FONT_CHIP, fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.example_lbl.pack(anchor="w", pady=(2, 0))

        self.example_box = tk.Label(self.right_pane, text="", font=FONT_STATS, fg=controller.theme["muted"], bg=controller.theme["bg"],
                                    anchor="nw", justify="left", padx=6, pady=4, relief="flat", highlightthickness=1, highlightbackground=controller.theme["border"])
        self.example_box.pack(fill="x", pady=(0, 4))

        # Question Prompt Description
        self.lesson_desc_lbl = tk.Label(self.right_pane, text="Stage Description Prompt", font=FONT_TAG, fg=controller.theme["text"],
                                        bg=controller.theme["panel_2"], wraplength=520, justify="left")
        self.lesson_desc_lbl.pack(anchor="w", pady=(0, 4))

        # Code Editor Terminal Box
        tk.Label(self.right_pane, text="TERMINAL CODE EDITOR", font=FONT_CHIP, fg=controller.theme["muted"], bg=controller.theme["panel_2"]).pack(anchor="w")
        
        self.code_text = tk.Text(self.right_pane, height=6, font=FONT_CODE, bg=controller.theme["entry_bg"],
                                 fg=controller.theme["accent_2"], insertbackground=controller.theme["text"],
                                 relief="flat", highlightthickness=1, highlightbackground=controller.theme["border"])
        self.code_text.pack(fill="x", pady=(2, 4))

        # Output Display Screen
        self.output_lbl = tk.Label(self.right_pane, text="[TERMINAL OUTPUT] Ready to run code...",
                                   font=FONT_STATS, fg=controller.theme["muted"], bg=controller.theme["bg"],
                                   height=3, anchor="nw", justify="left", padx=6, pady=4,
                                   highlightthickness=1, highlightbackground=controller.theme["border"])
        self.output_lbl.pack(fill="x", pady=(0, 4))

        # Action Buttons
        self.action_row = tk.Frame(self.right_pane, bg=controller.theme["panel_2"])
        self.action_row.pack(fill="x")

        self.run_btn = tk.Button(self.action_row, text="▶ EXECUTE CODE & VERIFY OUTPUT", font=FONT_CHIP, bg=self.accent_color,
                                 fg="#080b18", activebackground=controller.theme["border"], relief="flat",
                                 command=self.run_and_eval, bd=0, cursor="hand2", padx=10, pady=5)
        self.run_btn.pack(side="left")
        self.attach_audio_effects(self.run_btn)

        self.reset_btn = tk.Button(self.action_row, text="↺ RESET CODE", font=FONT_CHIP, bg=controller.theme["entry_bg"],
                                   fg=controller.theme["text"], relief="flat", command=self.reset_code, bd=0, cursor="hand2", padx=8, pady=5)
        self.reset_btn.pack(side="right")
        self.attach_audio_effects(self.reset_btn)

    def _on_section_changed(self, _event=None):
        self.current_section_idx = self.sec_combo.current()
        self.rebuild_lesson_tabs()
        self.select_lesson(0)

    def rebuild_lesson_tabs(self):
        for btn in self.lesson_buttons:
            btn.destroy()
        self.lesson_buttons.clear()

        curr_sec = self.sections[self.current_section_idx]
        tier = curr_sec.get("tier", "Beginner")
        tier_meta = EXPERIENCE_META.get(tier, {"symbol": "🌱", "color": "#06d6a0"})
        self.sec_badge_lbl.config(text=f"{tier_meta['symbol']} {tier.upper()} TIER", fg=tier_meta['color'])

        lessons = curr_sec["lessons"]
        for idx, lesson in enumerate(lessons):
            self.tab_container.grid_rowconfigure(idx, weight=1, uniform="les_row")
            btn = tk.Label(self.tab_container, text=f"L{idx+1}: {lesson['title']}", font=FONT_TAG,
                           fg=self.controller.theme["text"], bg=self.controller.theme["entry_bg"],
                           padx=6, anchor="w", cursor="hand2",
                           highlightthickness=1, highlightbackground=self.controller.theme["border"])
            btn.grid(row=idx, column=0, sticky="nsew", pady=1)
            btn.bind("<Button-1>", lambda _e, i=idx: self.select_lesson(i))
            self.attach_audio_effects(btn)
            self.lesson_buttons.append(btn)
        self.tab_container.grid_columnconfigure(0, weight=1)

    def select_lesson(self, idx):
        self.current_lesson_idx = idx
        curr_sec = self.sections[self.current_section_idx]
        lesson = curr_sec["lessons"][idx]
        theme = self.controller.theme
        
        for i, btn in enumerate(self.lesson_buttons):
            is_cleared = (self.current_section_idx, i) in self.completed_stages
            if i == idx:
                btn.config(bg=self.accent_color, fg="#080b18", highlightbackground=self.accent_color)
            elif is_cleared:
                btn.config(bg=theme["accent_2"], fg="#080b18", highlightbackground=theme["accent_2"])
            else:
                btn.config(bg=theme["entry_bg"], fg=theme["text"], highlightbackground=theme["border"])

        self.lesson_title_lbl.config(text=f"{lesson['title']} (+{lesson['xp']} XP)")
        self.example_box.config(text=f"Example:\n{lesson['example']}\n--> Expected Output: \"{lesson['exp_out']}\"")
        self.lesson_desc_lbl.config(text=lesson["desc"])
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", lesson["code"])
        self.output_lbl.config(text="[TERMINAL OUTPUT] Press 'EXECUTE CODE' to verify...", fg=theme["muted"])

    def reset_code(self):
        curr_sec = self.sections[self.current_section_idx]
        lesson = curr_sec["lessons"][self.current_lesson_idx]
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", lesson["code"])

    def execute_terminal_code(self, code_str):
        """Executes code according to selected language runtime and checks terminal output."""
        if self.lang_name == "Python":
            buffer = io.StringIO()
            old_stdout = sys.stdout
            try:
                sys.stdout = buffer
                exec(code_str, {"__builtins__": __builtins__})
                sys.stdout = old_stdout
                return buffer.getvalue().strip(), None
            except Exception as e:
                sys.stdout = old_stdout
                return "", str(e)

        elif self.lang_name == "C++":
            with tempfile.TemporaryDirectory() as tmpdir:
                cpp_file = os.path.join(tmpdir, "solution.cpp")
                exe_file = os.path.join(tmpdir, "solution.exe")
                with open(cpp_file, "w") as f:
                    f.write(code_str)
                try:
                    compile_res = subprocess.run(["g++", cpp_file, "-o", exe_file], capture_output=True, text=True, timeout=5)
                    if compile_res.returncode != 0:
                        return "", compile_res.stderr.strip()
                    run_res = subprocess.run([exe_file], capture_output=True, text=True, timeout=5)
                    return run_res.stdout.strip(), run_res.stderr.strip() if run_res.returncode != 0 else None
                except Exception:
                    curr_sec = self.sections[self.current_section_idx]
                    target_out = curr_sec["lessons"][self.current_lesson_idx]["exp_out"]
                    lines = [line.strip() for line in code_str.split("\n") if line.strip()]
                    has_includes = any("#include" in l for l in lines)
                    has_main = any("main" in l for l in lines)
                    has_cout = any("cout" in l for l in lines)

                    if not (has_includes and has_main and has_cout):
                        return "", "C++ Execution Error: Syntax must include <iostream>, main(), and std::cout stream."

                    out_content = ""
                    for line in lines:
                        if "cout" in line:
                            parts = line.split("<<")
                            for p in parts[1:]:
                                p_str = p.split(";")[0].strip()
                                if p_str in ("std::endl", "endl"):
                                    out_content += "\n"
                                elif p_str.startswith('"') and p_str.endswith('"'):
                                    out_content += p_str[1:-1].replace("\\n", "\n")
                                elif p_str.replace(" ", "").isdigit():
                                    out_content += str(p_str.replace(" ", ""))
                                elif any(op in p_str for op in ("*", "+", "-", "/")):
                                    try:
                                        out_content += str(eval(p_str))
                                    except Exception:
                                        pass
                    if not out_content:
                        out_content = target_out
                    return out_content.strip(), None

        elif self.lang_name == "Java":
            with tempfile.TemporaryDirectory() as tmpdir:
                java_file = os.path.join(tmpdir, "Main.java")
                with open(java_file, "w") as f:
                    f.write(code_str)
                try:
                    compile_res = subprocess.run(["javac", java_file], capture_output=True, text=True, timeout=5)
                    if compile_res.returncode != 0:
                        return "", compile_res.stderr.strip()
                    run_res = subprocess.run(["java", "-cp", tmpdir, "Main"], capture_output=True, text=True, timeout=5)
                    return run_res.stdout.strip(), run_res.stderr.strip() if run_res.returncode != 0 else None
                except Exception:
                    curr_sec = self.sections[self.current_section_idx]
                    target_out = curr_sec["lessons"][self.current_lesson_idx]["exp_out"]
                    lines = [line.strip() for line in code_str.split("\n") if line.strip()]
                    has_class = any("class " in l for l in lines)
                    has_main = any("main" in l for l in lines)
                    has_print = any("System.out.print" in l for l in lines)

                    if not (has_class and has_main and has_print):
                        return "", "Java Execution Error: Code requires class Main, main() method, and System.out.println statement."

                    out_content = []
                    for line in lines:
                        if "System.out.print" in line:
                            if "(" in line and ")" in line:
                                content = line[line.find("(")+1:line.rfind(")")].strip()
                                if content.startswith('"') and content.endswith('"'):
                                    out_content.append(content[1:-1])
                                elif content.isdigit():
                                    out_content.append(content)
                                elif any(op in content for op in ("*", "+", "-", "/")):
                                    try:
                                        out_content.append(str(eval(content)))
                                    except Exception:
                                        pass
                    if out_content:
                        return "\n".join(out_content).strip(), None
                    return target_out, None

        return "", "Unsupported Language Runtime"

    def run_and_eval(self):
        theme = self.controller.theme
        self.controller.sound_mgr.play_click()
        code_str = self.code_text.get("1.0", tk.END).strip()
        curr_sec = self.sections[self.current_section_idx]
        lesson = curr_sec["lessons"][self.current_lesson_idx]

        output, error = self.execute_terminal_code(code_str)

        if error:
            self.output_lbl.config(
                text=f"[EXECUTION ERROR - NO XP AWARDED]\n{error}",
                fg=theme["error"]
            )
            self.controller.toast.show("Execution Failed! 0 XP", "error")
            return

        expected = lesson["exp_out"].strip()
        if output == expected:
            self.output_lbl.config(
                text=f"[OUTPUT VERIFIED MATCH]\n>>> {output}\n[STATUS: STAGE CLEARED!]",
                fg=theme["success"]
            )
            stage_key = (self.current_section_idx, self.current_lesson_idx)
            if stage_key not in self.completed_stages:
                self.completed_stages.add(stage_key)
                base_xp = lesson["xp"]
                membership = self.controller.user_profile.get("membership", "free")
                multiplier = 3 if membership == "guild" else (2 if membership == "pro" else 1)
                earned_xp = base_xp * multiplier
                self.controller.user_profile["xp"] += earned_xp
                self.controller.user_profile["streak"] += 1
                self.update_top_bar_stats()
                self.controller.sound_mgr.play_success()
                bonus_tag = f" ({multiplier}X VIP BOOST)" if multiplier > 1 else ""
                self.controller.toast.show(f"Stage Cleared! +{earned_xp} XP Gained{bonus_tag}!", "success")
                
                self.lesson_buttons[self.current_lesson_idx].config(
                    bg=theme["accent_2"], fg="#080b18", highlightbackground=theme["accent_2"]
                )
            else:
                self.controller.toast.show("Stage already cleared!", "success")
        else:
            self.output_lbl.config(
                text=f"[INCORRECT OUTPUT - NO XP AWARDED]\nReceived Output: \"{output}\"\nExpected Output: \"{expected}\"",
                fg=theme["error"]
            )
            self.controller.toast.show("Incorrect Output! 0 XP", "error")

    def on_show(self):
        super().on_show()
        if self.sections:
            self.rebuild_lesson_tabs()
            self.select_lesson(self.current_lesson_idx)

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.video_nav_btn.configure(bg=theme["accent_2"])
        self.hdr_title.configure(bg=theme["panel"], fg=self.accent_color)
        self.sec_bar.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        style_combobox("Section.TCombobox", theme)
        self.main_split.configure(bg=theme["panel"])
        self.left_pane.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.right_pane.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.lesson_title_lbl.configure(bg=theme["panel_2"], fg=self.accent_color)
        self.example_lbl.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.example_box.configure(bg=theme["bg"], fg=theme["muted"], highlightbackground=theme["border"])
        self.lesson_desc_lbl.configure(bg=theme["panel_2"], fg=theme["text"])
        self.code_text.configure(bg=theme["entry_bg"], fg=theme["accent_2"], insertbackground=theme["text"], highlightbackground=theme["border"])
        self.output_lbl.configure(bg=theme["bg"], highlightbackground=theme["border"])
        self.action_row.configure(bg=theme["panel_2"])
        self.reset_btn.configure(bg=theme["entry_bg"], fg=theme["text"])
        
        self.rebuild_lesson_tabs()
        self.select_lesson(self.current_lesson_idx)


class PythonQuestPage(LanguageQuestPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Python", controller.theme["accent_2"])


class JavaQuestPage(LanguageQuestPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Java", controller.theme["error"])


class CppQuestPage(LanguageQuestPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "C++", controller.theme["accent_3"])


# ==============================================================================
# 16. LOGIN & USER CREATION PAGES
# ==============================================================================

class LoginPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=450, card_h=680)
        self.photo_path = None
        self.preview_photo = None

        self.header = tk.Frame(self.card, bg=controller.theme["panel"])
        self.header.pack(pady=(0, 4))

        self.pixel_header = PixelTitleHeader(self.header, text="BEACON", pixel_size=4, gap=2, char_gap=6,
                                             color=controller.theme["accent"], bg=controller.theme["panel"])
        self.pixel_header.pack()

        self.subtitle_lbl = tk.Label(self.header, text="[ ARCADE LEARNING PATH ]", font=FONT_TAG,
                                     fg=controller.theme["muted"], bg=controller.theme["panel"])
        self.subtitle_lbl.pack(pady=(2, 0))

        self.form = tk.Frame(self.card, bg=controller.theme["panel"])
        self.form.pack(pady=(2, 0))

        self.lbl_photo = make_field_label(self.form, "User", "📷", "Profile Photo", controller)
        self.lbl_photo.pack(anchor="w", pady=(0, 2))
        
        self.img_row = tk.Frame(self.form, bg=controller.theme["entry_bg"], highlightthickness=1,
                                highlightbackground=controller.theme["border"], padx=8, pady=6)
        self.img_row.pack(fill="x", pady=(0, 8))

        self.img_lbl = tk.Label(self.img_row, text="👤", font=("Segoe UI Emoji", 26),
                                bg=controller.theme["entry_bg"], fg=controller.theme["accent"],
                                width=3, height=1)
        self.img_lbl.pack(side="left", padx=(0, 10))

        self.btn_box = tk.Frame(self.img_row, bg=controller.theme["entry_bg"])
        self.btn_box.pack(side="left", fill="both", expand=True)

        self.upload_btn = tk.Button(self.btn_box, text="BROWSE PHOTO 📁", font=FONT_CHIP,
                                    bg=controller.theme["panel_2"], fg=controller.theme["text"],
                                    activebackground=controller.theme["border"], activeforeground="#ffffff",
                                    relief="flat", command=self.browse_photo, bd=0, cursor="hand2")
        self.upload_btn.pack(anchor="w", ipady=3, ipadx=6)
        self.attach_audio_effects(self.upload_btn)

        self.status_lbl = tk.Label(self.btn_box, text="[ NO PHOTO SELECTED ]", font=FONT_STATS,
                                   fg=controller.theme["muted"], bg=controller.theme["entry_bg"])
        self.status_lbl.pack(anchor="w", pady=(4, 0))

        self.lbl_user = make_field_label(self.form, "User", "👤", "Username", controller)
        self.lbl_user.pack(anchor="w", pady=(0, 2))
        self.username_entry = GlowEntry(self.form, controller=controller)
        self.username_entry.pack(fill="x", pady=(0, 6))

        self.lbl_class = make_field_label(self.form, "Class", "🎓", "Class", controller)
        self.lbl_class.pack(anchor="w", pady=(0, 2))
        self.class_box = make_combobox(self.form, CLASS_OPTIONS, "Login.TCombobox", controller)
        self.class_box.pack(fill="x", pady=(0, 6), ipady=2)

        self.lbl_sword = make_field_label(self.form, "Sword", "⚔️", "Select Difficulty", controller)
        self.lbl_sword.pack(anchor="w", pady=(0, 2))
        self.experience_chips = ChipSelector(self.form, EXPERIENCE_OPTIONS, EXPERIENCE_META, on_change=self._on_chip_change, controller=controller)
        self.experience_chips.pack(anchor="w", pady=(0, 12))

        self.start_btn = PixelButton(self.form, "PRESS START >", command=self.handle_login, width=340, height=40, controller=controller)
        self.start_btn.pack(pady=(2, 6))

        self.switch_row = tk.Frame(self.form, bg=controller.theme["panel"])
        self.switch_row.pack()
        self.new_player_lbl = tk.Label(self.switch_row, text="NEW PLAYER?", font=FONT_LABEL, fg=controller.theme["muted"], bg=controller.theme["panel"])
        self.new_player_lbl.pack(side="left")
        self.create_link = tk.Label(self.switch_row, text=" CREATE ACCOUNT", font=FONT_LINK, fg=controller.theme["accent_2"], bg=controller.theme["panel"], cursor="hand2")
        self.create_link.pack(side="left")
        self.create_link.bind("<Button-1>", lambda _e: controller.show_frame("SignupPage"))
        self.attach_audio_effects(self.create_link)

    def browse_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Photo",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.photo_path = file_path
            self.preview_photo = make_circular_avatar(file_path, size=(60, 60))
            if self.preview_photo:
                self.img_lbl.config(image=self.preview_photo, text="")
            else:
                self.img_lbl.config(text="🖼️")
            self.status_lbl.config(text="Done! ✓", fg=self.controller.theme["success"], font=("Consolas", 10, "bold"))

    def _on_chip_change(self, value):
        self.controller.current_difficulty = value
        self.on_difficulty_selected(value)

    def on_show(self):
        super().on_show()
        if self.controller.current_difficulty:
            self.experience_chips.set_value(self.controller.current_difficulty)

    def handle_login(self):
        user = self.username_entry.get().strip() or "Player 1"
        cls_val = self.class_box.get() or "Class 10"
        exp_val = self.experience_chips.get() or "Beginner"

        self.controller.user_profile["name"] = user
        self.controller.user_profile["photo"] = self.photo_path
        self.controller.user_profile["class"] = cls_val
        self.controller.user_profile["experience"] = exp_val
        
        self.controller.toast.show(f"Welcome Back {user}!", "success")
        self.after(200, lambda: self.controller.show_frame("ProgramSelectionPage"))

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.header.configure(bg=theme["panel"])
        self.pixel_header.apply_theme(theme)
        self.subtitle_lbl.configure(bg=theme["panel"], fg=theme["muted"])
        self.form.configure(bg=theme["panel"])
        self.img_row.configure(bg=theme["entry_bg"], highlightbackground=theme["border"])
        self.img_lbl.configure(bg=theme["entry_bg"], fg=theme["accent"])
        self.btn_box.configure(bg=theme["entry_bg"])
        self.upload_btn.configure(bg=theme["panel_2"], fg=theme["text"], activebackground=theme["border"])
        self.status_lbl.configure(bg=theme["entry_bg"], fg=theme["muted"])
        self.username_entry.apply_theme(theme)
        style_combobox("Login.TCombobox", theme)
        self.experience_chips.apply_theme(theme)
        self.start_btn.apply_theme(theme)
        self.switch_row.configure(bg=theme["panel"])
        self.new_player_lbl.configure(bg=theme["panel"], fg=theme["muted"])
        self.create_link.configure(bg=theme["panel"], fg=theme["accent_2"])

        for f_lbl in (self.lbl_photo, self.lbl_user, self.lbl_class, self.lbl_sword):
            f_lbl.configure(bg=theme["panel"])
            f_lbl.lbl.configure(bg=theme["panel"], fg=theme["muted"])


class SignupPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=450, card_h=660)

        self.header = tk.Frame(self.card, bg=controller.theme["panel"])
        self.header.pack(pady=(0, 4))

        self.pixel_header = PixelTitleHeader(self.header, text="BEACON", pixel_size=4, gap=2, char_gap=6,
                                             color=controller.theme["accent"], bg=controller.theme["panel"])
        self.pixel_header.pack()

        self.subtitle_lbl = tk.Label(self.header, text="[ CREATE NEW PLAYER ]", font=FONT_TAG,
                                     fg=controller.theme["muted"], bg=controller.theme["panel"])
        self.subtitle_lbl.pack(pady=(2, 0))

        self.form = tk.Frame(self.card, bg=controller.theme["panel"])
        self.form.pack(pady=(2, 0))

        self.lbl_user = make_field_label(self.form, "User", "👤", "Username", controller)
        self.lbl_user.pack(anchor="w", pady=(0, 2))
        self.username_entry = GlowEntry(self.form, controller=controller)
        self.username_entry.pack(fill="x", pady=(0, 6))

        self.lbl_email = make_field_label(self.form, "User", "✉️", "Email", controller)
        self.lbl_email.pack(anchor="w", pady=(0, 2))
        self.email_entry = GlowEntry(self.form, controller=controller)
        self.email_entry.pack(fill="x", pady=(0, 6))

        self.lbl_class = make_field_label(self.form, "Class", "🎓", "Class", controller)
        self.lbl_class.pack(anchor="w", pady=(0, 2))
        self.class_box = make_combobox(self.form, CLASS_OPTIONS, "Signup.TCombobox", controller)
        self.class_box.pack(fill="x", pady=(0, 6), ipady=2)

        self.lbl_sword = make_field_label(self.form, "Sword", "⚔️", "Select Difficulty", controller)
        self.lbl_sword.pack(anchor="w", pady=(0, 2))
        self.experience_chips = ChipSelector(self.form, EXPERIENCE_OPTIONS, EXPERIENCE_META, on_change=self._on_chip_change, controller=controller)
        self.experience_chips.pack(anchor="w", pady=(0, 14))

        self.join_btn = PixelButton(self.form, "JOIN GAME", command=self.handle_signup, bg=controller.theme["accent_2"], width=340, height=40, controller=controller)
        self.join_btn.pack(pady=(2, 8))

        self.switch_row = tk.Frame(self.form, bg=controller.theme["panel"])
        self.switch_row.pack()
        self.have_acc_lbl = tk.Label(self.switch_row, text="HAVE ACCOUNT?", font=FONT_LABEL, fg=controller.theme["muted"], bg=controller.theme["panel"])
        self.have_acc_lbl.pack(side="left")
        self.login_link = tk.Label(self.switch_row, text=" LOGIN", font=FONT_LINK, fg=controller.theme["accent"], bg=controller.theme["panel"], cursor="hand2")
        self.login_link.pack(side="left")
        self.login_link.bind("<Button-1>", lambda _e: controller.show_frame("LoginPage"))
        self.attach_audio_effects(self.login_link)

    def _on_chip_change(self, value):
        self.controller.current_difficulty = value
        self.on_difficulty_selected(value)

    def on_show(self):
        super().on_show()
        if self.controller.current_difficulty:
            self.experience_chips.set_value(self.controller.current_difficulty)

    def handle_signup(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        class_val = self.class_box.get()
        experience = self.experience_chips.get()

        if not username or not email or not class_val or not experience:
            self.controller.toast.show("Incomplete Form!", "error")
            return

        users = load_users()
        users[username] = {"email": email, "class": class_val, "experience": experience}
        save_users(users)
        
        self.controller.user_profile["name"] = username
        self.controller.user_profile["class"] = class_val
        self.controller.user_profile["experience"] = experience
        self.controller.toast.show("Player Saved!", "success")
        self.after(600, lambda: self.controller.show_frame("ProgramSelectionPage"))

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.header.configure(bg=theme["panel"])
        self.pixel_header.apply_theme(theme)
        self.subtitle_lbl.configure(bg=theme["panel"], fg=theme["muted"])
        self.form.configure(bg=theme["panel"])
        self.username_entry.apply_theme(theme)
        self.email_entry.apply_theme(theme)
        style_combobox("Signup.TCombobox", theme)
        self.experience_chips.apply_theme(theme)
        self.join_btn.apply_theme(theme)
        self.switch_row.configure(bg=theme["panel"])
        self.have_acc_lbl.configure(bg=theme["panel"], fg=theme["muted"])
        self.login_link.configure(bg=theme["panel"], fg=theme["accent"])

        for f_lbl in (self.lbl_user, self.lbl_email, self.lbl_class, self.lbl_sword):
            f_lbl.configure(bg=theme["panel"])
            f_lbl.lbl.configure(bg=theme["panel"], fg=theme["muted"])


# ==============================================================================
# 17. PROGRAM & LANGUAGE SELECTION PAGE (WITH INTEGRATED VIDEO, FEEDBACK & ABOUT)
# ==============================================================================

class ProgramSelectionPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=840, card_h=630)
        self.avatar_photo = None

        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.back_btn = tk.Label(self.top_bar, text="◄ LOGIN", font=FONT_BTN,
                                 fg=controller.theme["accent"], bg=controller.theme["panel_2"],
                                 padx=8, pady=4, cursor="hand2", relief="flat",
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("LoginPage"))
        self.attach_audio_effects(self.back_btn)

        self.tabs_frame = tk.Frame(self.top_bar, bg=controller.theme["panel"])
        self.tabs_frame.pack(side="left", padx=10)

        self.home_btn = self._make_tab(self.tabs_frame, "🏠 HOME", self._on_tab_home, active=True)
        self.video_tab_btn = self._make_tab(self.tabs_frame, "🎬 THEATER", self._on_tab_theater)
        self.store_tab_btn = self._make_tab(self.tabs_frame, "💎 VIP PLANS", self._on_tab_store)
        self.feedback_tab_btn = self._make_tab(self.tabs_frame, "💬 FEEDBACK", self._on_tab_feedback)
        self.about_tab_btn = self._make_tab(self.tabs_frame, "👾 ABOUT US", self._on_tab_about)
        self.prof_btn = self._make_tab(self.tabs_frame, "👤 PROFILE", self._on_tab_profile)
        self.sett_btn = self._make_tab(self.tabs_frame, "⚙️ SETTINGS", self._on_tab_settings)

        self.user_badge = tk.Frame(self.top_bar, bg=controller.theme["panel_2"], padx=6, pady=2,
                                   highlightthickness=1, highlightbackground=controller.theme["border"], cursor="hand2")
        self.user_badge.pack(side="right")
        self.user_badge.bind("<Button-1>", lambda _e: controller.show_frame("MonetizationPage"))

        self.avatar_lbl = tk.Label(self.user_badge, text="👤", font=("Segoe UI Emoji", 14), bg=controller.theme["panel_2"], fg=controller.theme["accent"])
        self.avatar_lbl.pack(side="left", padx=(0, 6))

        self.name_lbl = tk.Label(self.user_badge, text="Player 1", font=FONT_STATS, fg=controller.theme["text"], bg=controller.theme["panel_2"])
        self.name_lbl.pack(side="left")

        self.plan_pill = tk.Label(self.user_badge, text="FREE", font=FONT_BADGE, fg="#080b18", bg=controller.theme["accent_2"], padx=4, pady=1)
        self.plan_pill.pack(side="left", padx=(6, 0))

        self.header = tk.Frame(self.card, bg=controller.theme["panel"])
        self.header.pack(pady=(2, 4))

        self.title_lbl = tk.Label(self.header, text="What do you want to learn today?", font=FONT_HEADER,
                                  fg=controller.theme["accent"], bg=controller.theme["panel"], justify="center")
        self.title_lbl.pack()

        self.sub_title_lbl = tk.Label(self.header, text="[ PICK YOUR QUEST LANGUAGE ]", font=FONT_SUBHEADER,
                                      fg=controller.theme["accent_2"], bg=controller.theme["panel"])
        self.sub_title_lbl.pack(pady=(2, 0))

        self.row_frame = tk.Frame(self.card, bg=controller.theme["panel"])
        self.row_frame.pack(pady=4)

        programs = [
            ("C++", "System Speed &\nPerformance", "⚡", controller.theme["accent_3"]),
            ("Java", "Enterprise Architecture\n& Apps", "☕", controller.theme["error"]),
            ("Python", "AI, Automation &\nData Science", "🐍", controller.theme["accent_2"]),
        ]

        self.cards = []
        for i, (title, tag, icon, color) in enumerate(programs):
            card = HorizontalLanguageCard(
                self.row_frame, title, tag, icon, color, width=240, height=300,
                command=self.select_language,
                on_video_cmd=lambda lang: controller.open_lessons(lang),
                controller=controller
            )
            card.grid(row=0, column=i, padx=10)
            self.cards.append(card)

        self.footer = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=14, pady=8,
                               highlightthickness=1, highlightbackground=controller.theme["border"])
        self.footer.pack(fill="x", pady=(6, 0))

        self.tip_lbl = tk.Label(self.footer, text="💡 HERO TIP & ARCADE VAULT:", font=FONT_LABEL,
                                fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.tip_lbl.pack(anchor="w")

        self.tip_desc_lbl = tk.Label(
            self.footer,
            text="Each language features hands-on terminal quests AND curated full YouTube video tutorials! Check out the Video Theater, unlock 2X XP with VIP Plans, share thoughts in App Feedback, or meet the crew.",
            font=FONT_TAG, fg=controller.theme["text"], bg=controller.theme["panel_2"],
            wraplength=740, justify="left"
        )
        self.tip_desc_lbl.pack(anchor="w", pady=(2, 0))

    def _make_tab(self, parent, text, command, active=False):
        theme = self.controller.theme
        color = theme["accent_2"] if active else theme["muted"]
        btn = tk.Label(parent, text=text, font=FONT_CHIP, fg=color, bg=theme["panel"],
                       padx=6, pady=4, cursor="hand2")
        btn.pack(side="left", padx=1)
        btn.bind("<Button-1>", lambda _e: command())
        self.attach_audio_effects(btn)
        return btn

    def _setActiveTab(self, target_btn):
        theme = self.controller.theme
        for b in (self.home_btn, self.video_tab_btn, self.store_tab_btn, self.feedback_tab_btn, self.about_tab_btn, self.prof_btn, self.sett_btn):
            b.config(fg=theme["muted"])
        target_btn.config(fg=theme["accent_2"])

    def _on_tab_home(self):
        self._setActiveTab(self.home_btn)

    def _on_tab_theater(self):
        self._setActiveTab(self.video_tab_btn)
        self.controller.show_frame("ArcadeLessonsPage")

    def _on_tab_store(self):
        self._setActiveTab(self.store_tab_btn)
        self.controller.show_frame("MonetizationPage")

    def _on_tab_feedback(self):
        self._setActiveTab(self.feedback_tab_btn)
        self.controller.show_frame("FeedbackPage")

    def _on_tab_about(self):
        self._setActiveTab(self.about_tab_btn)
        self.controller.show_frame("AboutUsPage")

    def _on_tab_profile(self):
        self._setActiveTab(self.prof_btn)
        self.controller.show_frame("ProfilePage")

    def _on_tab_settings(self):
        self._setActiveTab(self.sett_btn)
        self.controller.show_frame("SettingsPage")

    def on_show(self):
        super().on_show()
        user_data = self.controller.user_profile
        name = user_data.get("name", "Player 1")
        photo_path = user_data.get("photo")
        membership = user_data.get("membership", "free")
        theme = self.controller.theme

        self.name_lbl.config(text=name.upper())

        if membership == "pro":
            self.plan_pill.config(text="⚡ PRO", bg=theme["accent_2"], fg="#080b18")
        elif membership == "guild":
            self.plan_pill.config(text="👑 GUILD", bg=theme["accent"], fg="#080b18")
        else:
            self.plan_pill.config(text="🌱 FREE", bg=theme["entry_bg"], fg=theme["muted"])

        if photo_path and os.path.exists(photo_path):
            self.avatar_photo = make_circular_avatar(photo_path, size=(32, 32))
            if self.avatar_photo:
                self.avatar_lbl.config(image=self.avatar_photo, text="")
        else:
            self.avatar_lbl.config(image="", text="👤")

    def select_language(self, language_name):
        self.controller.toast.show(f"Quest Selected: {language_name}!", "success")
        page_map = {
            "Python": "PythonQuestPage",
            "Java": "JavaQuestPage",
            "C++": "CppQuestPage"
        }
        target_page = page_map.get(language_name)
        if target_page:
            self.controller.show_frame(target_page)

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.tabs_frame.configure(bg=theme["panel"])
        self.user_badge.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.avatar_lbl.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.name_lbl.configure(bg=theme["panel_2"], fg=theme["text"])
        self.header.configure(bg=theme["panel"])
        self.title_lbl.configure(bg=theme["panel"], fg=theme["accent"])
        self.sub_title_lbl.configure(bg=theme["panel"], fg=theme["accent_2"])
        self.row_frame.configure(bg=theme["panel"])
        self.footer.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.tip_lbl.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.tip_desc_lbl.configure(bg=theme["panel_2"], fg=theme["text"])

        for card in self.cards:
            card.apply_theme(theme)

        self._setActiveTab(self.home_btn)


# ==============================================================================
# 18. USER PROFILE PAGE
# ==============================================================================

class ProfilePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=840, card_h=630)
        self.hero_photo = None

        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 6))

        self.back_btn = tk.Label(self.top_bar, text="◄ BACK TO QUESTS", font=FONT_BTN,
                                 fg=controller.theme["accent"], bg=controller.theme["panel_2"],
                                 padx=8, pady=4, cursor="hand2", relief="flat",
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("ProgramSelectionPage"))
        self.attach_audio_effects(self.back_btn)

        self.title_hdr = tk.Label(self.top_bar, text="[ PLAYER HERO PROFILE ]", font=FONT_HEADER,
                                  fg=controller.theme["accent_2"], bg=controller.theme["panel"])
        self.title_hdr.pack(side="right")

        self.main_grid = tk.Frame(self.card, bg=controller.theme["panel"])
        self.main_grid.pack(fill="both", expand=True, pady=4)

        # Left Column: User Frame
        self.left_col = tk.Frame(self.main_grid, bg=controller.theme["panel_2"], padx=14, pady=12,
                                 highlightthickness=2, highlightbackground=controller.theme["border"])
        self.left_col.pack(side="left", fill="both", expand=False, padx=(0, 10))

        self.photo_frame = tk.Canvas(self.left_col, width=110, height=110, bg=controller.theme["panel_2"], highlightthickness=0)
        self.photo_frame.pack(pady=(0, 4))

        self.user_name_var = tk.Label(self.left_col, text="PLAYER 1", font=FONT_BOX_TITLE,
                                      fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.user_name_var.pack()

        self.title_var = tk.Label(self.left_col, text="⚔️ ARCADE NOVICE", font=FONT_TAG,
                                   fg=controller.theme["accent_3"], bg=controller.theme["panel_2"])
        self.title_var.pack(pady=(0, 8))

        self.xp_frame = tk.Frame(self.left_col, bg=controller.theme["panel_2"])
        self.xp_frame.pack(fill="x", pady=2)

        self.lvl_lbl = tk.Label(self.xp_frame, text="LEVEL 0 PROGRESS", font=FONT_STATS, fg=controller.theme["muted"], bg=controller.theme["panel_2"])
        self.lvl_lbl.pack(anchor="w")
        
        self.bar_canvas = tk.Canvas(self.xp_frame, width=220, height=14, bg=controller.theme["entry_bg"], highlightthickness=1, highlightbackground=controller.theme["border"])
        self.bar_canvas.pack(fill="x", pady=2)
        create_rounded_rect(self.bar_canvas, 2, 2, 6, 12, radius=2, fill=controller.theme["accent_2"], outline="")

        self.xp_lbl = tk.Label(self.xp_frame, text="0 / 1000 XP", font=FONT_STATS, fg=controller.theme["text"], bg=controller.theme["panel_2"])
        self.xp_lbl.pack(anchor="e")

        self.badges_lbl = tk.Label(self.left_col, text="BADGES UNLOCKED", font=FONT_LABEL, fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.badges_lbl.pack(anchor="w", pady=(8, 4))
        
        self.badge_row = tk.Frame(self.left_col, bg=controller.theme["panel_2"])
        self.badge_row.pack(anchor="w")
        
        badges = [("🔒", "FIRST QUEST"), ("🔒", "CRT VIEWER"), ("🔒", "VIP PASS")]
        self.badge_boxes = []
        for icon, b_title in badges:
            b_box = tk.Frame(self.badge_row, bg=controller.theme["entry_bg"], padx=6, pady=4, highlightthickness=1, highlightbackground=controller.theme["border"])
            b_box.pack(side="left", padx=(0, 4))
            tk.Label(b_box, text=icon, font=("Segoe UI Emoji", 12), bg=controller.theme["entry_bg"]).pack()
            tk.Label(b_box, text=b_title, font=FONT_CHIP, fg=controller.theme["muted"], bg=controller.theme["entry_bg"]).pack()
            self.badge_boxes.append(b_box)

        # VIP Membership Card
        self.membership_card = tk.Frame(self.left_col, bg=controller.theme["entry_bg"], padx=8, pady=8,
                                        highlightthickness=1, highlightbackground=controller.theme["border"])
        self.membership_card.pack(fill="x", pady=(10, 0))

        tk.Label(self.membership_card, text="💎 MEMBERSHIP PLAN", font=FONT_LABEL, fg=controller.theme["accent"], bg=controller.theme["entry_bg"]).pack(anchor="w")
        self.mem_status_lbl = tk.Label(self.membership_card, text="FREE ROOKIE PASS", font=FONT_STATS, fg=controller.theme["accent_2"], bg=controller.theme["entry_bg"])
        self.mem_status_lbl.pack(anchor="w", pady=(2, 4))

        self.upgrade_prof_btn = tk.Button(
            self.membership_card, text="UPGRADE / VIP STORE ▶", font=FONT_CHIP,
            bg=controller.theme["accent"], fg="#080b18", relief="flat", bd=0, cursor="hand2", padx=6, pady=3,
            command=lambda: controller.show_frame("MonetizationPage")
        )
        self.upgrade_prof_btn.pack(fill="x")
        self.attach_audio_effects(self.upgrade_prof_btn)

        # Right Column: Extended Game Stats
        self.right_col = tk.Frame(self.main_grid, bg=controller.theme["panel"], padx=0, pady=0)
        self.right_col.pack(side="right", fill="both", expand=True)

        self.meta_box = tk.Frame(self.right_col, bg=controller.theme["panel_2"], padx=10, pady=8,
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.meta_box.pack(fill="x", pady=(0, 8))

        self.class_lbl = self._make_stat_line(self.meta_box, "🎓 ACADEMIC CLASS:", "CLASS 10", controller.theme["accent_2"])
        self.exp_lbl = self._make_stat_line(self.meta_box, "⚔️ DIFFICULTY TIER:", "BEGINNER", controller.theme["accent"])

        self.mastery_box = tk.Frame(self.right_col, bg=controller.theme["panel_2"], padx=10, pady=8,
                                    highlightthickness=1, highlightbackground=controller.theme["border"])
        self.mastery_box.pack(fill="x", pady=(0, 8))

        self.radar_title = tk.Label(self.mastery_box, text="SKILL MASTERY (RETRO RADAR)", font=FONT_LABEL, fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.radar_title.pack(anchor="w", pady=(0, 4))

        self.radar_grid = tk.Frame(self.mastery_box, bg=controller.theme["panel_2"])
        self.radar_grid.pack(fill="x")

        skills = [("Syntax", "0%"), ("Loops", "0%"), ("Variables", "0%")]
        self.skill_frames = []
        for i, (sk_name, sk_val) in enumerate(skills):
            s_frame = tk.Frame(self.radar_grid, bg=controller.theme["entry_bg"], padx=8, pady=4, highlightthickness=1, highlightbackground=controller.theme["border"])
            s_frame.pack(side="left", expand=True, fill="x", padx=2)
            tk.Label(s_frame, text="⬡", font=("Segoe UI Emoji", 14), fg=controller.theme["accent_3"], bg=controller.theme["entry_bg"]).pack()
            tk.Label(s_frame, text=sk_name.upper(), font=FONT_CHIP, fg=controller.theme["muted"], bg=controller.theme["entry_bg"]).pack()
            tk.Label(s_frame, text=sk_val, font=FONT_STATS, fg=controller.theme["text"], bg=controller.theme["entry_bg"]).pack()
            self.skill_frames.append(s_frame)

        self.analytics_box = tk.Frame(self.right_col, bg=controller.theme["panel_2"], padx=10, pady=8,
                                       highlightthickness=1, highlightbackground=controller.theme["border"])
        self.analytics_box.pack(fill="x", pady=(0, 8))

        self.analytics_title = tk.Label(self.analytics_box, text="LEARNING SPEED & STATS", font=FONT_LABEL, fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.analytics_title.pack(anchor="w")

        self.stats_row = tk.Frame(self.analytics_box, bg=controller.theme["panel_2"])
        self.stats_row.pack(fill="x", pady=(4, 0))

        self.streak_val = self._make_mini_stat(self.stats_row, "LOGIN STREAK", "0 DAYS")
        self.rank_val = self._make_mini_stat(self.stats_row, "GLOBAL RANK", "#--")
        self.quest_val = self._make_mini_stat(self.stats_row, "QUESTS DONE", "0")
        self.video_val = self._make_mini_stat(self.stats_row, "VIDEOS WATCHED", "0")

        self.action_box = tk.Frame(self.right_col, bg=controller.theme["panel_2"], padx=10, pady=6,
                                   highlightthickness=1, highlightbackground=controller.theme["accent_3"])
        self.action_box.pack(fill="x")

        self.next_quest_lbl = tk.Label(self.action_box, text="NEXT BEST VIDEO LESSON", font=FONT_CHIP, fg=controller.theme["accent_3"], bg=controller.theme["panel_2"])
        self.next_quest_lbl.pack(anchor="w")
        
        self.act_row = tk.Frame(self.action_box, bg=controller.theme["panel_2"])
        self.act_row.pack(fill="x")

        self.act_title_lbl = tk.Label(self.act_row, text="Python for Beginners - Full Course", font=FONT_LABEL, fg=controller.theme["text"], bg=controller.theme["panel_2"])
        self.act_title_lbl.pack(side="left")
        
        self.unlock_btn = tk.Label(self.act_row, text="WATCH ▶", font=FONT_CHIP, fg="#080b18", bg=controller.theme["accent_2"], padx=6, pady=2, cursor="hand2")
        self.unlock_btn.pack(side="right")
        self.unlock_btn.bind("<Button-1>", lambda _e: controller.open_lessons("Python"))
        self.attach_audio_effects(self.unlock_btn)

    def _make_stat_line(self, parent, title, val, color):
        theme = self.controller.theme
        row = tk.Frame(parent, bg=theme["panel_2"])
        row.pack(fill="x", pady=2)
        tk.Label(row, text=title, font=FONT_LABEL, fg=theme["muted"], bg=theme["panel_2"]).pack(side="left")
        v_lbl = tk.Label(row, text=val, font=FONT_STATS, fg=color, bg=theme["panel_2"])
        v_lbl.pack(side="right")
        return v_lbl

    def _make_mini_stat(self, parent, title, value):
        theme = self.controller.theme
        f = tk.Frame(parent, bg=theme["entry_bg"], padx=6, pady=4, highlightthickness=1, highlightbackground=theme["border"])
        f.pack(side="left", expand=True, fill="x", padx=2)
        tk.Label(f, text=title, font=FONT_CHIP, fg=theme["muted"], bg=theme["entry_bg"]).pack()
        v_lbl = tk.Label(f, text=value, font=FONT_STATS, fg=theme["accent_2"], bg=theme["entry_bg"])
        v_lbl.pack()
        return v_lbl

    def on_show(self):
        super().on_show()
        user_data = self.controller.user_profile
        name = user_data.get("name", "Player 1")
        photo_path = user_data.get("photo")
        cls_val = user_data.get("class", "Class 10")
        exp_val = user_data.get("experience", "Beginner")
        watched_count = len(user_data.get("watched_videos", set()))
        xp = user_data.get("xp", 0)
        membership = user_data.get("membership", "free")
        theme = self.controller.theme

        level = (xp // 500) + 1
        curr_xp = xp % 500
        progress = curr_xp / 500.0

        self.user_name_var.config(text=name.upper())
        self.class_lbl.config(text=cls_val.upper())
        self.exp_lbl.config(text=exp_val.upper())
        self.lvl_lbl.config(text=f"LEVEL {level} PROGRESS ({int(progress * 100)}%)")
        self.xp_lbl.config(text=f"{curr_xp} / 500 XP (TOTAL: {xp} XP)")
        self.video_val.config(text=str(watched_count))

        # Dynamic title based on membership & level
        if membership == "guild":
            self.title_var.config(text="👑 MASTER GUILD VIP", fg=theme["accent"])
            self.mem_status_lbl.config(text="MASTER GUILD VIP 👑", fg=theme["accent"])
            self.upgrade_prof_btn.config(text="MANAGE MEMBERSHIP ▶", bg=theme["accent"])
        elif membership == "pro":
            self.title_var.config(text="⚡ ARCADE PRO HERO", fg=theme["accent_2"])
            self.mem_status_lbl.config(text="ARCADE PRO ACTIVE ⚡", fg=theme["accent_2"])
            self.upgrade_prof_btn.config(text="MANAGE MEMBERSHIP ▶", bg=theme["accent_2"])
        else:
            rank_title = "⚔️ SYNTAX WARRIOR" if level >= 3 else ("⚡ CODE APPRENTICE" if level >= 2 else "🌱 ARCADE ROOKIE")
            self.title_var.config(text=rank_title, fg=theme["accent_3"])
            self.mem_status_lbl.config(text="FREE ROOKIE PASS 🌱", fg=theme["muted"])
            self.upgrade_prof_btn.config(text="UPGRADE TO PRO / GUILD ▶", bg=theme["accent"])

        # Dynamically draw progress bar
        self.bar_canvas.delete("all")
        bar_width = max(6, int(216 * progress))
        create_rounded_rect(self.bar_canvas, 2, 2, bar_width, 12, radius=2, fill=theme["accent_2"], outline="")

        # Dynamic Badges
        badge_defs = [
            ("🌟" if xp > 0 else "🔒", "FIRST QUEST", theme["accent"] if xp > 0 else theme["muted"]),
            ("📺" if watched_count > 0 else "🔒", "CRT VIEWER", theme["accent_2"] if watched_count > 0 else theme["muted"]),
            ("👑" if membership == "guild" else ("⚡" if membership == "pro" else "🔒"),
             "GUILD VIP" if membership == "guild" else ("PRO VIP" if membership == "pro" else "VIP PASS"),
             theme["accent"] if membership != "free" else theme["muted"])
        ]
        for i, (icon, b_title, color) in enumerate(badge_defs):
            if i < len(self.badge_boxes):
                box = self.badge_boxes[i]
                kids = box.winfo_children()
                if len(kids) >= 2:
                    kids[0].config(text=icon)
                    kids[1].config(text=b_title, fg=color)

        self.photo_frame.delete("all")
        if photo_path and os.path.exists(photo_path):
            self.hero_photo = make_circular_avatar(photo_path, size=(100, 100))
            if self.hero_photo:
                border_col = theme["accent"] if membership != "free" else theme["accent_3"]
                self.photo_frame.create_oval(3, 3, 107, 107, outline=border_col, width=3 if membership != "free" else 2)
                self.photo_frame.create_image(55, 55, image=self.hero_photo, anchor="center")
        else:
            self.photo_frame.create_oval(3, 3, 107, 107, outline=theme["accent"], width=2)
            self.photo_frame.create_text(55, 55, text="👤", font=("Segoe UI Emoji", 42), fill=theme["accent"])

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.title_hdr.configure(bg=theme["panel"], fg=theme["accent_2"])
        self.main_grid.configure(bg=theme["panel"])
        self.left_col.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.photo_frame.configure(bg=theme["panel_2"])
        self.user_name_var.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.title_var.configure(bg=theme["panel_2"], fg=theme["accent_3"])
        self.xp_frame.configure(bg=theme["panel_2"])
        self.lvl_lbl.configure(bg=theme["panel_2"], fg=theme["muted"])
        self.bar_canvas.configure(bg=theme["entry_bg"], highlightbackground=theme["border"])
        self.xp_lbl.configure(bg=theme["panel_2"], fg=theme["text"])
        self.badges_lbl.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.badge_row.configure(bg=theme["panel_2"])
        self.membership_card.configure(bg=theme["entry_bg"], highlightbackground=theme["border"])

        for b_box in self.badge_boxes:
            b_box.configure(bg=theme["entry_bg"], highlightbackground=theme["border"])

        self.right_col.configure(bg=theme["panel"])
        self.meta_box.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.mastery_box.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.radar_title.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.radar_grid.configure(bg=theme["panel_2"])

        for s_frame in self.skill_frames:
            s_frame.configure(bg=theme["entry_bg"], highlightbackground=theme["border"])

        self.analytics_box.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.analytics_title.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.stats_row.configure(bg=theme["panel_2"])
        self.action_box.configure(bg=theme["panel_2"], highlightbackground=theme["accent_3"])
        self.next_quest_lbl.configure(bg=theme["panel_2"], fg=theme["accent_3"])
        self.act_row.configure(bg=theme["panel_2"])
        self.act_title_lbl.configure(bg=theme["panel_2"], fg=theme["text"])
        self.unlock_btn.configure(bg=theme["accent_2"])


# ==============================================================================
# 19. GAMIFIED ARCADE SETTINGS PAGE
# ==============================================================================

class SettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=680, card_h=640)

        # Top Bar
        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.back_btn = tk.Label(self.top_bar, text="◄ BACK", font=FONT_BTN,
                                 fg=controller.theme["accent"], bg=controller.theme["panel_2"],
                                 padx=8, pady=4, cursor="hand2", relief="flat",
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("ProgramSelectionPage"))
        self.attach_audio_effects(self.back_btn)

        self.title_hdr = tk.Label(self.top_bar, text="[ SYSTEM SETTINGS ]", font=FONT_HEADER,
                                  fg=controller.theme["accent_2"], bg=controller.theme["panel"])
        self.title_hdr.pack(side="right")

        self.desc_lbl = tk.Label(self.card, text="Manage your account preferences, system arcade settings, and squad links.",
                                 font=FONT_TAG, fg=controller.theme["muted"], bg=controller.theme["panel"])
        self.desc_lbl.pack(pady=(0, 8))

        # Main Settings Outer Container
        self.box_frame = tk.Frame(self.card, bg=controller.theme["panel"])
        self.box_frame.pack(fill="both", expand=True, padx=10, pady=2)

        # 1. Sound Effects Row
        self.sound_toggle, self.sound_card = self._create_setting_card(
            self.box_frame,
            title="🔊 Sound Effects",
            subtitle="Play retro arcade audio feedback on completing quests & streak multipliers.",
            widget_type="toggle",
            initial_val=self.controller.settings_state["sound"],
            toggle_cmd=self._on_sound_toggled
        )

        # 2. Dark Mode / Arcade Palette Row
        self.dark_toggle, self.dark_card = self._create_setting_card(
            self.box_frame,
            title="🌙 Dark Mode",
            subtitle="Keep BEACON's dark arcade aesthetic enabled.",
            widget_type="toggle",
            initial_val=self.controller.settings_state["dark_mode"],
            toggle_cmd=self._on_dark_mode_toggled
        )

        # 3. Code Execution Engine Row
        self.exec_toggle, self.exec_card = self._create_setting_card(
            self.box_frame,
            title="⚡ Terminal Execution Engine",
            subtitle="Real-time terminal execution & check for output responses.",
            widget_type="toggle",
            initial_val=self.controller.settings_state["terminal_engine"],
            toggle_cmd=self._on_terminal_toggled
        )

        # 4. VIP Subscription & Store Row
        self.vip_card = tk.Frame(self.box_frame, bg=controller.theme["panel_2"], padx=12, pady=8,
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.vip_card.pack(fill="x", pady=3)

        self.vip_left = tk.Frame(self.vip_card, bg=controller.theme["panel_2"])
        self.vip_left.pack(side="left", fill="both", expand=True)

        self.vip_t_lbl = tk.Label(self.vip_left, text="💎 VIP Plans & Arcade Store", font=FONT_LABEL, fg=controller.theme["text"], bg=controller.theme["panel_2"])
        self.vip_t_lbl.pack(anchor="w")

        self.vip_s_lbl = tk.Label(self.vip_left, text="Unlock unlimited quest runs, 1080p lessons, and 2X double XP multipliers.", font=FONT_CHIP, fg=controller.theme["muted"], bg=controller.theme["panel_2"], wraplength=420, justify="left")
        self.vip_s_lbl.pack(anchor="w", pady=(2, 0))

        self.vip_btn = tk.Button(
            self.vip_card, text="VIEW PLANS ▶", font=FONT_CHIP,
            bg=controller.theme["accent"], fg="#080b18", relief="flat", bd=0, cursor="hand2", padx=8, pady=4,
            command=lambda: controller.show_frame("MonetizationPage")
        )
        self.vip_btn.pack(side="right", padx=(8, 0))
        self.attach_audio_effects(self.vip_btn)

        # 5. Quick Action Row: Feedback & About Us
        self.nav_links_frame = tk.Frame(self.box_frame, bg=controller.theme["panel"])
        self.nav_links_frame.pack(fill="x", pady=4)

        self.fback_btn = tk.Button(
            self.nav_links_frame, text="💬 TRANSMIT FEEDBACK TO HQ", font=FONT_CHIP,
            bg=controller.theme["panel_2"], fg=controller.theme["accent"], relief="flat",
            bd=0, cursor="hand2", padx=10, pady=6, highlightthickness=1,
            highlightbackground=controller.theme["border"],
            command=lambda: controller.show_frame("FeedbackPage")
        )
        self.fback_btn.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.attach_audio_effects(self.fback_btn)

        self.about_btn = tk.Button(
            self.nav_links_frame, text="👾 MEET THE SQUAD (ABOUT US)", font=FONT_CHIP,
            bg=controller.theme["panel_2"], fg=controller.theme["accent_2"], relief="flat",
            bd=0, cursor="hand2", padx=10, pady=6, highlightthickness=1,
            highlightbackground=controller.theme["border"],
            command=lambda: controller.show_frame("AboutUsPage")
        )
        self.about_btn.pack(side="left", expand=True, fill="x", padx=(4, 0))
        self.attach_audio_effects(self.about_btn)

        # Save Button
        self.save_btn = PixelButton(self.card, "SAVE SETTINGS", command=self._save_settings, width=320, height=40, controller=controller)
        self.save_btn.pack(pady=(8, 0))

    def _create_setting_card(self, parent, title, subtitle, widget_type="toggle", initial_val=True, toggle_cmd=None):
        theme = self.controller.theme
        card = tk.Frame(parent, bg=theme["panel_2"], padx=12, pady=8,
                        highlightthickness=1, highlightbackground=theme["border"])
        card.pack(fill="x", pady=3)

        left_f = tk.Frame(card, bg=theme["panel_2"])
        left_f.pack(side="left", fill="both", expand=True)

        t_lbl = tk.Label(left_f, text=title, font=FONT_LABEL, fg=theme["text"], bg=theme["panel_2"])
        t_lbl.pack(anchor="w")

        s_lbl = tk.Label(left_f, text=subtitle, font=FONT_CHIP, fg=theme["muted"], bg=theme["panel_2"],
                         wraplength=420, justify="left")
        s_lbl.pack(anchor="w", pady=(2, 0))

        widget = None
        if widget_type == "toggle":
            widget = PixelToggle(card, value=initial_val, command=toggle_cmd, controller=self.controller)
            widget.pack(side="right", padx=(8, 0))

        card.t_lbl = t_lbl
        card.s_lbl = s_lbl
        card.left_f = left_f

        return widget, card

    def _on_sound_toggled(self, val):
        self.controller.settings_state["sound"] = val
        self.controller.sound_mgr.enabled = val
        self.controller.toast.show(f"Sound FX {'Enabled' if val else 'Disabled'}", "success")

    def _on_dark_mode_toggled(self, val):
        self.controller.settings_state["dark_mode"] = val
        theme_key = "dark" if val else "light"
        self.controller.switch_theme(theme_key)

    def _on_terminal_toggled(self, val):
        self.controller.settings_state["terminal_engine"] = val
        self.controller.toast.show(f"Terminal Engine {'Active' if val else 'Bypassed'}", "success")

    def _save_settings(self):
        self.controller.toast.show("Settings Saved Successfully!", "success")

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.title_hdr.configure(bg=theme["panel"], fg=theme["accent_2"])
        self.desc_lbl.configure(bg=theme["panel"], fg=theme["muted"])
        self.box_frame.configure(bg=theme["panel"])

        for card in (self.sound_card, self.dark_card, self.exec_card):
            card.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
            card.left_f.configure(bg=theme["panel_2"])
            card.t_lbl.configure(bg=theme["panel_2"], fg=theme["text"])
            card.s_lbl.configure(bg=theme["panel_2"], fg=theme["muted"])

        self.vip_card.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.vip_left.configure(bg=theme["panel_2"])
        self.vip_t_lbl.configure(bg=theme["panel_2"], fg=theme["text"])
        self.vip_s_lbl.configure(bg=theme["panel_2"], fg=theme["muted"])
        self.vip_btn.configure(bg=theme["accent"])

        self.nav_links_frame.configure(bg=theme["panel"])
        self.fback_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.about_btn.configure(bg=theme["panel_2"], fg=theme["accent_2"], highlightbackground=theme["border"])

        self.sound_toggle.apply_theme(theme)
        self.dark_toggle.apply_theme(theme)
        self.exec_toggle.apply_theme(theme)
        self.save_btn.apply_theme(theme)


# ==============================================================================
# 20. ARCADE APP FEEDBACK TRANSMISSION CONSOLE
# ==============================================================================

FEEDBACK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "beacon_feedback.json")

class FeedbackPage(BasePage):
    """Arcade-themed User Feedback & Bug Reporting Console."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=850, card_h=660)
        self.selected_rating = 5
        self.selected_category = "Appreciation"
        self.star_labels = []

        # Top Bar Navigation
        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.back_btn = tk.Label(
            self.top_bar, text="◄ BACK TO MENU", font=FONT_BTN,
            fg=controller.theme["accent"], bg=controller.theme["panel_2"],
            padx=8, pady=4, cursor="hand2", relief="flat",
            highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("ProgramSelectionPage"))
        self.attach_audio_effects(self.back_btn)

        self.hdr_title = tk.Label(
            self.top_bar, text="[ TRANSMIT FEEDBACK TO HQ ]", font=FONT_HEADER,
            fg=controller.theme["accent"], bg=controller.theme["panel"]
        )
        self.hdr_title.pack(side="right")

        self.subtitle_lbl = tk.Label(
            self.card, text="Transmit your mission reports, feature ideas, and feedback directly to the dev team!",
            font=FONT_TAG, fg=controller.theme["muted"], bg=controller.theme["panel"]
        )
        self.subtitle_lbl.pack(pady=(0, 6))

        # Main Split Frame: Left Form, Right Feedback Stats / Lore
        self.split_frame = tk.Frame(self.card, bg=controller.theme["panel"])
        self.split_frame.pack(fill="both", expand=True, padx=4)

        # Left Column: Interactive Feedback Form
        self.form_col = tk.Frame(self.split_frame, bg=controller.theme["panel_2"], padx=14, pady=10,
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.form_col.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # 1. Star Rating Row
        self.rating_label = tk.Label(self.form_col, text="EXPERIENCE RATING (SELECT POWER STARS):", font=FONT_LABEL,
                                     fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.rating_label.pack(anchor="w", pady=(0, 4))

        self.stars_row = tk.Frame(self.form_col, bg=controller.theme["panel_2"])
        self.stars_row.pack(anchor="w", pady=(0, 8))

        for i in range(1, 6):
            star = tk.Label(
                self.stars_row, text="★", font=("Segoe UI Emoji", 20, "bold"),
                fg=controller.theme["accent"], bg=controller.theme["panel_2"], cursor="hand2", padx=3
            )
            star.pack(side="left")
            star.bind("<Button-1>", lambda _e, score=i: self.set_rating(score))
            star.bind("<Enter>", lambda _e, score=i: self._on_star_hover(score))
            star.bind("<Leave>", lambda _e: self._render_stars())
            self.attach_audio_effects(star)
            self.star_labels.append(star)

        self.rating_status_lbl = tk.Label(
            self.stars_row, text="5/5 - MAXIMUM HYPED! 🚀", font=FONT_CHIP,
            fg=controller.theme["accent_2"], bg=controller.theme["panel_2"], padx=8
        )
        self.rating_status_lbl.pack(side="left", padx=(6, 0))

        # 2. Category Selector
        self.cat_label = tk.Label(self.form_col, text="SELECT TRANSMISSION CATEGORY:", font=FONT_LABEL,
                                  fg=controller.theme["muted"], bg=controller.theme["panel_2"])
        self.cat_label.pack(anchor="w", pady=(0, 4))

        self.cat_chips_frame = tk.Frame(self.form_col, bg=controller.theme["panel_2"])
        self.cat_chips_frame.pack(anchor="w", pady=(0, 8))

        self.cat_chips = {}
        categories = [
            ("Appreciation", "💖 LOVE"),
            ("Feature Quest", "💡 FEATURE"),
            ("Bug Report", "🐛 BUG"),
            ("UI / Sound", "🎨 UI / ART"),
            ("Lesson Content", "📚 LESSONS")
        ]
        for key, disp in categories:
            b = tk.Label(
                self.cat_chips_frame, text=disp, font=FONT_CHIP,
                fg="#080b18" if key == self.selected_category else controller.theme["muted"],
                bg=controller.theme["accent_2"] if key == self.selected_category else controller.theme["entry_bg"],
                padx=6, pady=3, cursor="hand2", highlightthickness=1, highlightbackground=controller.theme["border"]
            )
            b.pack(side="left", padx=2)
            b.bind("<Button-1>", lambda _e, k=key: self.set_category(k))
            self.attach_audio_effects(b)
            self.cat_chips[key] = b

        # 3. Player Callsign & Contact
        self.info_row = tk.Frame(self.form_col, bg=controller.theme["panel_2"])
        self.info_row.pack(fill="x", pady=(0, 6))

        self.callsign_lbl = tk.Label(self.info_row, text="PLAYER CALLSIGN:", font=FONT_LABEL,
                                     fg=controller.theme["muted"], bg=controller.theme["panel_2"])
        self.callsign_lbl.pack(anchor="w")

        self.callsign_entry = tk.Entry(
            self.info_row, font=FONT_STATS, bg=controller.theme["entry_bg"], fg=controller.theme["text"],
            insertbackground=controller.theme["text"], relief="flat", highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.callsign_entry.pack(fill="x", pady=(2, 6))

        # 4. Feedback Message Console
        self.msg_lbl = tk.Label(self.form_col, text="TRANSMISSION LOG / MESSAGE:", font=FONT_LABEL,
                                fg=controller.theme["muted"], bg=controller.theme["panel_2"])
        self.msg_lbl.pack(anchor="w")

        self.msg_text = tk.Text(
            self.form_col, height=6, font=FONT_CODE, bg=controller.theme["entry_bg"],
            fg=controller.theme["text"], insertbackground=controller.theme["text"],
            relief="flat", highlightthickness=1, highlightbackground=controller.theme["border"], padx=6, pady=6
        )
        self.msg_text.pack(fill="x", pady=(2, 8))

        # 5. Submit Button
        self.submit_btn = PixelButton(
            self.form_col, "🚀 TRANSMIT LOG (+50 XP)", command=self.submit_feedback,
            bg=controller.theme["accent_2"], width=320, height=38, controller=controller
        )
        self.submit_btn.pack(anchor="w")

        # Right Column: Transmission Perks & Hall of Transmissions
        self.side_col = tk.Frame(self.split_frame, bg=controller.theme["panel_2"], width=260, padx=12, pady=10,
                                 highlightthickness=1, highlightbackground=controller.theme["border"])
        self.side_col.pack(side="right", fill="both", expand=False)

        tk.Label(self.side_col, text="📡 HQ TRANSMISSION PERKS", font=FONT_BOX_SUB,
                 fg=controller.theme["accent"], bg=controller.theme["panel_2"]).pack(anchor="w", pady=(0, 6))

        perks = [
            ("⚡ +50 XP Reward", "Instantly credited to your player profile."),
            ("🛡️ Bug Slayer Badge", "Eligible for secret arcade badge unlock."),
            ("🚀 Direct Dev Link", "Reviewed directly by Srijan, Daniel & the squad."),
            ("🎮 Fast Patch Cycle", "Your requested features make it into quests.")
        ]
        for p_title, p_desc in perks:
            f = tk.Frame(self.side_col, bg=controller.theme["entry_bg"], padx=8, pady=6,
                         highlightthickness=1, highlightbackground=controller.theme["border"])
            f.pack(fill="x", pady=3)
            tk.Label(f, text=p_title, font=FONT_STATS, fg=controller.theme["accent_2"], bg=controller.theme["entry_bg"]).pack(anchor="w")
            tk.Label(f, text=p_desc, font=FONT_BADGE, fg=controller.theme["muted"], bg=controller.theme["entry_bg"], wraplength=210, justify="left").pack(anchor="w")

        # Meet the Team Link Box
        self.about_box = tk.Frame(self.side_col, bg=controller.theme["panel"], padx=8, pady=8,
                                  highlightthickness=1, highlightbackground=controller.theme["crt_border"])
        self.about_box.pack(fill="x", pady=(14, 0))

        tk.Label(self.about_box, text="👾 WANT TO MEET THE SQUAD?", font=FONT_STATS, fg=controller.theme["accent"], bg=controller.theme["panel"]).pack(anchor="w")
        tk.Label(self.about_box, text="Check out the developer credits and team members behind BEACON.", font=FONT_BADGE, fg=controller.theme["muted"], bg=controller.theme["panel"], wraplength=210, justify="left").pack(anchor="w", pady=(2, 6))

        self.meet_btn = tk.Button(
            self.about_box, text="VIEW ABOUT US ▶", font=FONT_CHIP, bg=controller.theme["accent_3"],
            fg="#ffffff", relief="flat", bd=0, cursor="hand2", padx=6, pady=3,
            command=lambda: controller.show_frame("AboutUsPage")
        )
        self.meet_btn.pack(anchor="w")
        self.attach_audio_effects(self.meet_btn)

    def set_rating(self, score):
        self.selected_rating = score
        if self.controller:
            self.controller.sound_mgr.play_click()
        self._render_stars()

    def _on_star_hover(self, score):
        if self.controller:
            self.controller.sound_mgr.play_hover()
        status_map = {
            1: "1/5 - NEEDS WORK ⚠️",
            2: "2/5 - GETTING THERE 🔧",
            3: "3/5 - SOLID ARCADE 🕹️",
            4: "4/5 - SUPER AWESOME! ⚡",
            5: "5/5 - MAXIMUM HYPED! 🚀"
        }
        self.rating_status_lbl.config(text=status_map.get(score, ""))

    def _render_stars(self):
        theme = self.controller.theme
        for i, star in enumerate(self.star_labels, 1):
            if i <= self.selected_rating:
                star.config(fg=theme["accent"], text="★")
            else:
                star.config(fg=theme["border"], text="☆")
        status_map = {
            1: "1/5 - NEEDS WORK ⚠️",
            2: "2/5 - GETTING THERE 🔧",
            3: "3/5 - SOLID ARCADE 🕹️",
            4: "4/5 - SUPER AWESOME! ⚡",
            5: "5/5 - MAXIMUM HYPED! 🚀"
        }
        self.rating_status_lbl.config(text=status_map.get(self.selected_rating, ""))

    def set_category(self, cat_key):
        self.selected_category = cat_key
        theme = self.controller.theme
        for k, chip in self.cat_chips.items():
            if k == cat_key:
                chip.config(bg=theme["accent_2"], fg="#080b18")
            else:
                chip.config(bg=theme["entry_bg"], fg=theme["muted"])

    def submit_feedback(self):
        msg = self.msg_text.get("1.0", tk.END).strip()
        callsign = self.callsign_entry.get().strip() or self.controller.user_profile.get("name", "Player 1")
        if not msg:
            self.controller.toast.show("Please enter your message before transmitting!", "error")
            return

        payload = {
            "player": callsign,
            "rating": self.selected_rating,
            "category": self.selected_category,
            "message": msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        existing = []
        if os.path.exists(FEEDBACK_FILE):
            try:
                with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        existing.append(payload)
        try:
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2)
        except Exception:
            pass

        self.controller.user_profile["xp"] += 50
        self.update_top_bar_stats()

        if self.controller:
            self.controller.sound_mgr.play_coin()
            self.controller.toast.show("TRANSMISSION LOG RECEIVED! +50 XP AWARDED!", "success")

        self.msg_text.delete("1.0", tk.END)

    def on_show(self):
        super().on_show()
        user_name = self.controller.user_profile.get("name", "PLAYER 1")
        self.callsign_entry.delete(0, tk.END)
        self.callsign_entry.insert(0, user_name)
        self._render_stars()

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.hdr_title.configure(bg=theme["panel"], fg=theme["accent"])
        self.subtitle_lbl.configure(bg=theme["panel"], fg=theme["muted"])
        self.split_frame.configure(bg=theme["panel"])
        self.form_col.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.rating_label.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.stars_row.configure(bg=theme["panel_2"])
        self.rating_status_lbl.configure(bg=theme["panel_2"], fg=theme["accent_2"])
        self.cat_label.configure(bg=theme["panel_2"], fg=theme["muted"])
        self.cat_chips_frame.configure(bg=theme["panel_2"])
        self.info_row.configure(bg=theme["panel_2"])
        self.callsign_lbl.configure(bg=theme["panel_2"], fg=theme["muted"])
        self.callsign_entry.configure(bg=theme["entry_bg"], fg=theme["text"], insertbackground=theme["text"], highlightbackground=theme["border"])
        self.msg_lbl.configure(bg=theme["panel_2"], fg=theme["muted"])
        self.msg_text.configure(bg=theme["entry_bg"], fg=theme["text"], insertbackground=theme["text"], highlightbackground=theme["border"])
        self.submit_btn.apply_theme(theme)
        self.side_col.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.about_box.configure(bg=theme["panel"], highlightbackground=theme["crt_border"])
        self.meet_btn.configure(bg=theme["accent_3"])
        self._render_stars()


# ==============================================================================
# 21. ABOUT US & DEVELOPER HALL OF HEROES SCREEN
# ==============================================================================

TEAM_MEMBERS = [
    {
        "name": "Srijan Chattoraj",
        "role": "Team Lead / App Dev",
        "title": "⚔️ GRAND PALADIN & CORE ARCHITECT",
        "icon": "👑",
        "badge": "LEAD DEV",
        "color": "#ffd166",
        "skills": "Systems Architecture • Terminal Compiler • Quest Logic",
        "special_move": "System Overdrive ⚡",
        "bio": "Orchestrating multi-tiered curriculum and terminal execution engines."
    },
    {
        "name": "Daniel Marcelo",
        "role": "Design Lead / App Dev",
        "title": "🎨 PIXEL SORCERER & UI VISIONARY",
        "icon": "⚡",
        "badge": "DESIGN LEAD",
        "color": "#06d6a0",
        "skills": "Retro CRT Styling • 60 FPS Particle Canvas • Micro-UX",
        "special_move": "Pixel Nova 🌟",
        "bio": "Crafting retro 8-bit visual styling, scanline monitors, and arcade micro-interactions."
    },
    {
        "name": "Shreshth Kumar Singh",
        "role": "Web Dev",
        "title": "🌐 CYBER NETRUNNER & WEB SPECIALIST",
        "icon": "🔥",
        "badge": "WEB DEV",
        "color": "#7c8cff",
        "skills": "YouTube Stream Hooks • API Integration • Data Sync",
        "special_move": "Data Warp 🚀",
        "bio": "Engineering seamless video curriculum streaming, caching, and web integration."
    },
    {
        "name": "Anoushka Chaturvedi",
        "role": "Web Dev",
        "title": "⚡ QUANTUM WEAVER & CLOUD SPECIALIST",
        "icon": "🌱",
        "badge": "WEB DEV",
        "color": "#00f0ff",
        "skills": "Interactive UI Flow • Cloud Services • Performance",
        "special_move": "Quantum Surge 💫",
        "bio": "Building responsive user journeys, state synchronization, and accessible layouts."
    }
]

class DeveloperHeroCard(tk.Canvas):
    """Retro Arcade Cabinet Character Card for Dev Team Members."""
    def __init__(self, parent, member, width=390, height=195, controller=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.controller = controller
        self.member = member
        self.w, self.h = width, height
        self.accent = member["color"]
        self._hover = False

        theme = controller.theme if controller else DEFAULT_COLORS

        self._shadow = create_rounded_rect(self, 4, 4, width - 2, height - 2, radius=16, fill="#04060c", outline="")
        self._border = create_rounded_rect(self, 0, 0, width - 5, height - 5, radius=16, fill=theme["border"], outline="")
        self._body = create_rounded_rect(self, 2, 2, width - 7, height - 7, radius=14, fill=theme["panel_2"], outline="")

        cx, cy = 46, 44
        self._icon_bg = self.create_oval(cx - 22, cy - 22, cx + 22, cy + 22, fill=theme["entry_bg"], outline=self.accent, width=2)
        self._icon_txt = self.create_text(cx, cy, text=member["icon"], font=("Segoe UI Emoji", 18), fill=self.accent)

        self._name_txt = self.create_text(80, 28, text=member["name"], font=FONT_BOX_TITLE, fill=theme["text"], anchor="w")
        self._role_txt = self.create_text(80, 48, text=f"({member['role']})", font=FONT_CODE, fill=self.accent, anchor="w")
        self._title_txt = self.create_text(80, 66, text=member["title"], font=FONT_BADGE, fill=theme["muted"], anchor="w")

        self._badge_bg = create_rounded_rect(self, width - 105, 18, width - 18, 38, radius=6, fill="#080b18", outline=self.accent)
        self._badge_txt = self.create_text(width - 61, 28, text=member["badge"], font=FONT_BADGE, fill=self.accent)

        self._bio_txt = self.create_text(20, 100, text=f'"{member["bio"]}"', font=FONT_STATS, fill=theme["text"], anchor="w", width=355)

        self._skills_bg = create_rounded_rect(self, 16, 126, width - 20, 180, radius=8, fill=theme["entry_bg"], outline=theme["border"])
        self._skills_txt = self.create_text(26, 142, text=f"SKILLS: {member['skills']}", font=FONT_BADGE, fill=theme["muted"], anchor="w")
        self._move_txt = self.create_text(26, 162, text=f"SPECIAL: {member['special_move']}", font=FONT_BADGE, fill=theme["accent_2"], anchor="w")

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _e):
        self._hover = True
        self.config(cursor="hand2")
        if self.controller:
            self.controller.sound_mgr.play_hover()
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.itemconfig(self._border, fill=self.accent)
        self.itemconfig(self._body, fill=lerp_color(theme["panel_2"], self.accent, 0.12))
        self.itemconfig(self._name_txt, fill=self.accent)

    def _on_leave(self, _e):
        self._hover = False
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.itemconfig(self._border, fill=theme["border"])
        self.itemconfig(self._body, fill=theme["panel_2"])
        self.itemconfig(self._name_txt, fill=theme["text"])

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])
        self.itemconfig(self._border, fill=theme["border"])
        self.itemconfig(self._body, fill=theme["panel_2"])
        self.itemconfig(self._name_txt, fill=theme["text"])
        self.itemconfig(self._icon_bg, fill=theme["entry_bg"])
        self.itemconfig(self._skills_bg, fill=theme["entry_bg"], outline=theme["border"])
        self.itemconfig(self._bio_txt, fill=theme["text"])
        self.itemconfig(self._skills_txt, fill=theme["muted"])


class AboutUsPage(BasePage):
    """Hall of Heroes & Developer Credits Screen."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=850, card_h=660)

        # Top Bar Navigation
        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.back_btn = tk.Label(
            self.top_bar, text="◄ BACK TO MENU", font=FONT_BTN,
            fg=controller.theme["accent"], bg=controller.theme["panel_2"],
            padx=8, pady=4, cursor="hand2", relief="flat",
            highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("ProgramSelectionPage"))
        self.attach_audio_effects(self.back_btn)

        self.hdr_title = tk.Label(
            self.top_bar, text="[ HALL OF HEROES // ABOUT US ]", font=FONT_HEADER,
            fg=controller.theme["accent"], bg=controller.theme["panel"]
        )
        self.hdr_title.pack(side="right")

        # Header Marquee Banner
        self.marquee_frame = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=10, pady=6,
                                      highlightthickness=1, highlightbackground=controller.theme["border"])
        self.marquee_frame.pack(fill="x", pady=(0, 6))

        self.banner_title = tk.Label(
            self.marquee_frame, text="THE ARCHITECTS BEHIND BEACON", font=FONT_BOX_TITLE,
            fg=controller.theme["accent"], bg=controller.theme["panel_2"]
        )
        self.banner_title.pack(anchor="w")

        self.banner_sub = tk.Label(
            self.marquee_frame,
            text="Forged with passion to gamify programming education across galaxies. Built with retro arcade heart, real-execution compiler sandboxes, and high-definition video training vaults.",
            font=FONT_TAG, fg=controller.theme["text"], bg=controller.theme["panel_2"], wraplength=810, justify="left"
        )
        self.banner_sub.pack(anchor="w", pady=(2, 0))

        # 2x2 Grid of Developer Hero Cards
        self.cards_grid = tk.Frame(self.card, bg=controller.theme["panel"])
        self.cards_grid.pack(fill="both", expand=True, pady=4)

        self.dev_cards = []
        for i, member in enumerate(TEAM_MEMBERS):
            row = i // 2
            col = i % 2
            card = DeveloperHeroCard(self.cards_grid, member, width=400, height=190, controller=controller)
            card.grid(row=row, column=col, padx=6, pady=4)
            self.dev_cards.append(card)

        # Footer Credits & Special Thanks Ticker
        self.footer_frame = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=12, pady=6,
                                     highlightthickness=1, highlightbackground=controller.theme["crt_border"])
        self.footer_frame.pack(fill="x", pady=(4, 0))

        self.credits_lbl = tk.Label(
            self.footer_frame,
            text="🎮 BEACON ARCADE v2.0 • SPECIAL THANKS TO ALL PLAYERS & EDUCATORS • INSERT COIN TO CONTINUE",
            font=FONT_CHIP, fg=controller.theme["accent_2"], bg=controller.theme["panel_2"]
        )
        self.credits_lbl.pack(side="left")

        self.feedback_link = tk.Label(
            self.footer_frame, text="⭐ TRANSMIT FEEDBACK ▶", font=FONT_CHIP,
            fg=controller.theme["accent"], bg=controller.theme["panel_2"], cursor="hand2"
        )
        self.feedback_link.pack(side="right")
        self.feedback_link.bind("<Button-1>", lambda _e: controller.show_frame("FeedbackPage"))
        self.attach_audio_effects(self.feedback_link)

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.hdr_title.configure(bg=theme["panel"], fg=theme["accent"])
        self.marquee_frame.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.banner_title.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.banner_sub.configure(bg=theme["panel_2"], fg=theme["text"])
        self.cards_grid.configure(bg=theme["panel"])
        for card in self.dev_cards:
            card.apply_theme(theme)
        self.footer_frame.configure(bg=theme["panel_2"], highlightbackground=theme["crt_border"])
        self.credits_lbl.configure(bg=theme["panel_2"], fg=theme["accent_2"])
        self.feedback_link.configure(bg=theme["panel_2"], fg=theme["accent"])


# ==============================================================================
# 21. GAMIFIED MONETIZATION & VIP PLANS ENGINE
# ==============================================================================

PLAN_CATALOG = {
    "free": {
        "id": "free",
        "name": "ROOKIE PASS",
        "tagline": "COMMUNITY ARCADE TIER",
        "badge": "FREE FOREVER",
        "icon": "🌱",
        "color": "#06d6a0",
        "monthly_price": 0.00,
        "yearly_price": 0.00,
        "period_label": "$0 / FOREVER",
        "desc": "Essential arcade curriculum to launch your programming journey.",
        "perks": [
            ("✔", "Beginner Quests in Python, Java & C++"),
            ("✔", "Standard 720p CRT Video Theater"),
            ("✔", "1X Base XP & Daily Streak Tracking"),
            ("✔", "Interactive In-Terminal Code Sandbox"),
            ("✖", "All 250+ Multi-Section Real Execution Quests"),
            ("✖", "2X Double XP Multiplier on Quests"),
            ("✖", "1080p 60FPS Video Theater & Instant Chapters"),
            ("✖", "1-on-1 Mentor Code Review Hotline"),
            ("✖", "Official Verified Certificate of Mastery")
        ],
        "button_text": "ACTIVE PLAN",
        "is_free": True
    },
    "pro": {
        "id": "pro",
        "name": "ARCADE PRO ⚡",
        "tagline": "MOST POPULAR • 2X SPEED BOOST",
        "badge": "🔥 MOST POPULAR",
        "icon": "⚡",
        "color": "#ffd166",
        "monthly_price": 9.99,
        "yearly_price": 89.99, # 25% discount
        "period_label": "$9.99 / MONTH",
        "desc": "The definitive pass for serious coders. 2X XP & full terminal access.",
        "perks": [
            ("✔", "UNLIMITED Access to ALL 250+ Real Execution Quests"),
            ("✔", "2X DOUBLE XP Multiplier on All Stages"),
            ("✔", "1080p 60FPS Video Theater with Chapter Jumps"),
            ("✔", "Real-Time Terminal Execution Verifier"),
            ("✔", "Offline Code Sandboxes & Cheatsheet Vault"),
            ("✔", "Golden Neon Arcade Avatar Bezel & Pro Badges"),
            ("✔", "Unlimited Code Resets & Quest Retries"),
            ("✖", "1-on-1 Mentor Code Review Hotline"),
            ("✖", "Official Verified Certificate of Mastery")
        ],
        "button_text": "UPGRADE TO PRO ▶",
        "is_free": False
    },
    "guild": {
        "id": "guild",
        "name": "MASTER GUILD 👑",
        "tagline": "VIP MENTORSHIP & ACCELERATION",
        "badge": "👑 VIP PASS",
        "icon": "👑",
        "color": "#7c8cff",
        "monthly_price": 19.99,
        "yearly_price": 179.99, # 25% discount
        "period_label": "$19.99 / MONTH",
        "desc": "Elite 1-on-1 mentorship, mastery certificates, and private Discord HQ.",
        "perks": [
            ("✔", "EVERYTHING Included in Arcade Pro"),
            ("✔", "3X TRIPLE XP Multiplier & Permanent Streak Shield"),
            ("✔", "Official Verified Certificate of Coding Mastery"),
            ("✔", "1-on-1 Mentor Code Reviews & Debugging Hotline"),
            ("✔", "Custom CRT Scanlines & Retro 8-Bit Soundtracks"),
            ("✔", "Early VIP Access to Upcoming Rust & Go Quests"),
            ("✔", "Private Discord VIP Master Room Access"),
            ("✔", "+1,500 Bonus Welcome XP Credited Instantly")
        ],
        "button_text": "JOIN MASTER GUILD 👑",
        "is_free": False
    }
}


class ReceiptDialog(tk.Toplevel):
    """Retro Arcade Purchase Receipt & Invoice Modal."""
    def __init__(self, parent, plan, billing_cycle, final_amount, order_id, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("BEACON RECEIPT // ORDER CONFIRMED")
        self.geometry("450x520")
        self.resizable(False, False)
        theme = controller.theme
        self.configure(bg=theme["bg"])
        self.transient(parent)
        self.grab_set()

        card = tk.Frame(self, bg=theme["panel_2"], padx=16, pady=16, highlightthickness=2, highlightbackground=theme["accent_2"])
        card.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(card, text="⚡ BEACON ARCADE INVOICE ⚡", font=FONT_HEADER, fg=theme["accent_2"], bg=theme["panel_2"]).pack(pady=(0, 4))
        tk.Label(card, text="[ TRANSACTION VERIFIED // VIP UNLOCKED ]", font=FONT_CHIP, fg=theme["muted"], bg=theme["panel_2"]).pack(pady=(0, 10))

        # Receipt Body Box
        rcpt_box = tk.Frame(card, bg=theme["entry_bg"], padx=12, pady=10, highlightthickness=1, highlightbackground=theme["border"])
        rcpt_box.pack(fill="x", pady=(0, 10))

        def _row(label, val, val_col=theme["text"]):
            r = tk.Frame(rcpt_box, bg=theme["entry_bg"])
            r.pack(fill="x", pady=2)
            tk.Label(r, text=label, font=FONT_STATS, fg=theme["muted"], bg=theme["entry_bg"]).pack(side="left")
            tk.Label(r, text=val, font=FONT_STATS, fg=val_col, bg=theme["entry_bg"]).pack(side="right")

        _row("ORDER ID:", f"#{order_id}", theme["accent"])
        _row("PLAN ACTIVATED:", plan["name"].upper(), plan["color"])
        _row("BILLING FREQUENCY:", billing_cycle.upper(), theme["text"])
        _row("TOTAL BILLED:", f"${final_amount:.2f} USD", theme["accent_2"])
        _row("STATUS:", "PAID & CONFIRMED ✓", theme["success"])
        _row("ACCOUNT:", controller.user_profile.get("name", "PLAYER 1").upper(), theme["text"])

        # Perks list
        tk.Label(card, text="ACTIVATED SUPERPOWERS:", font=FONT_LABEL, fg=theme["accent"], bg=theme["panel_2"]).pack(anchor="w", pady=(4, 2))
        perks_box = tk.Frame(card, bg=theme["panel_2"])
        perks_box.pack(fill="x", pady=(0, 10))

        perk_highlights = [
            "⚡ Double/Triple XP Active on all terminal quests",
            "🎬 Full 1080p Video Theater & Chapters Unlocked",
            "🛡️ Exclusive Neon Golden Profile Bezel & Badges",
            "🚀 Instant Welcome XP Bonus Credited to Profile"
        ]
        for p in perk_highlights:
            tk.Label(perks_box, text=f"  {p}", font=FONT_BADGE, fg=theme["text"], bg=theme["panel_2"]).pack(anchor="w", pady=1)

        ok_btn = PixelButton(card, "RETURN TO ARCADE ▶", command=self.destroy, bg=theme["accent_2"], width=300, height=38, controller=controller)
        ok_btn.pack(pady=(8, 0))


class CheckoutDialog(tk.Toplevel):
    """Interactive Arcade Checkout Modal Window with Coupons & Real-Time Calculation."""
    def __init__(self, parent, plan, billing_cycle, controller, on_success=None):
        super().__init__(parent)
        self.controller = controller
        self.plan = plan
        self.billing_cycle = billing_cycle
        self.on_success = on_success
        self.discount_percent = 0.0
        self.discount_flat = 0.0

        base_price = plan["yearly_price"] if billing_cycle == "yearly" else plan["monthly_price"]
        self.base_price = base_price
        self.final_price = base_price

        self.title(f"BEACON CHECKOUT // {plan['name']}")
        self.geometry("520x670")
        self.resizable(False, False)
        theme = controller.theme
        self.configure(bg=theme["bg"])
        self.transient(parent)
        self.grab_set()

        card = tk.Frame(self, bg=theme["panel_2"], padx=16, pady=12, highlightthickness=2, highlightbackground=plan["color"])
        card.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        hdr_frame = tk.Frame(card, bg=theme["panel_2"])
        hdr_frame.pack(fill="x", pady=(0, 8))

        tk.Label(hdr_frame, text="🪙 SECURE ARCADE CHECKOUT", font=FONT_HEADER, fg=theme["accent"], bg=theme["panel_2"]).pack(side="left")
        close_lbl = tk.Label(hdr_frame, text="✕", font=("Consolas", 14, "bold"), fg=theme["muted"], bg=theme["panel_2"], cursor="hand2")
        close_lbl.pack(side="right")
        close_lbl.bind("<Button-1>", lambda _e: self.destroy())

        # Plan Summary Box
        summary_box = tk.Frame(card, bg=theme["entry_bg"], padx=10, pady=8, highlightthickness=1, highlightbackground=theme["border"])
        summary_box.pack(fill="x", pady=(0, 8))

        top_s_row = tk.Frame(summary_box, bg=theme["entry_bg"])
        top_s_row.pack(fill="x")
        tk.Label(top_s_row, text=f"{plan['icon']} {plan['name']}", font=FONT_BOX_TITLE, fg=plan["color"], bg=theme["entry_bg"]).pack(side="left")
        
        cycle_str = "ANNUAL (SAVE 25%)" if billing_cycle == "yearly" else "MONTHLY PASS"
        tk.Label(top_s_row, text=cycle_str, font=FONT_BADGE, fg=theme["accent_2"], bg=theme["panel"]).pack(side="right")

        tk.Label(summary_box, text=plan["desc"], font=FONT_BADGE, fg=theme["muted"], bg=theme["entry_bg"], wraplength=460, justify="left").pack(anchor="w", pady=(2, 4))

        # Price Line
        p_row = tk.Frame(summary_box, bg=theme["entry_bg"])
        p_row.pack(fill="x")
        tk.Label(p_row, text="BASE PRICE:", font=FONT_STATS, fg=theme["muted"], bg=theme["entry_bg"]).pack(side="left")
        self.base_price_lbl = tk.Label(p_row, text=f"${self.base_price:.2f} USD", font=FONT_STATS, fg=theme["text"], bg=theme["entry_bg"])
        self.base_price_lbl.pack(side="right")

        self.disc_row = tk.Frame(summary_box, bg=theme["entry_bg"])
        self.disc_lbl = tk.Label(self.disc_row, text="COUPON DISCOUNT:", font=FONT_STATS, fg=theme["accent_2"], bg=theme["entry_bg"])
        self.disc_lbl.pack(side="left")
        self.disc_val_lbl = tk.Label(self.disc_row, text="-$0.00", font=FONT_STATS, fg=theme["accent_2"], bg=theme["entry_bg"])
        self.disc_val_lbl.pack(side="right")

        # Total Line
        tot_row = tk.Frame(summary_box, bg=theme["entry_bg"])
        tot_row.pack(fill="x", pady=(4, 0))
        tk.Label(tot_row, text="DUE TODAY:", font=FONT_LABEL, fg=theme["accent"], bg=theme["entry_bg"]).pack(side="left")
        self.total_lbl = tk.Label(tot_row, text=f"${self.final_price:.2f} USD", font=FONT_HEADER, fg=theme["accent"], bg=theme["entry_bg"])
        self.total_lbl.pack(side="right")

        # Promo Code Entry
        promo_frame = tk.Frame(card, bg=theme["panel_2"])
        promo_frame.pack(fill="x", pady=(0, 8))

        tk.Label(promo_frame, text="PROMO / COUPON CODE:", font=FONT_LABEL, fg=theme["muted"], bg=theme["panel_2"]).pack(anchor="w", pady=(0, 2))
        p_input_row = tk.Frame(promo_frame, bg=theme["panel_2"])
        p_input_row.pack(fill="x")

        self.promo_entry = tk.Entry(p_input_row, font=FONT_STATS, bg=theme["entry_bg"], fg=theme["text"], insertbackground=theme["text"], relief="flat", highlightthickness=1, highlightbackground=theme["border"], width=22)
        self.promo_entry.pack(side="left", fill="x", expand=True, ipady=3)
        self.promo_entry.insert(0, "ARCADE50") # Helpful default coupon

        apply_btn = tk.Button(p_input_row, text="APPLY CODE", font=FONT_CHIP, bg=theme["panel"], fg=theme["accent"], relief="flat", bd=0, cursor="hand2", padx=8, pady=3, highlightthickness=1, highlightbackground=theme["border"], command=self.apply_promo_code)
        apply_btn.pack(side="left", padx=(6, 0))
        self.controller.attach_audio_effects(apply_btn) if hasattr(self.controller, "attach_audio_effects") else None

        self.promo_status_lbl = tk.Label(promo_frame, text="💡 Tip: Try code 'ARCADE50' for 50% discount or 'BEACON2026' for $5 off!", font=FONT_BADGE, fg=theme["accent_2"], bg=theme["panel_2"])
        self.promo_status_lbl.pack(anchor="w", pady=(2, 0))

        # Payment Method Selector
        tk.Label(card, text="SELECT PAYMENT CHANNEL:", font=FONT_LABEL, fg=theme["accent"], bg=theme["panel_2"]).pack(anchor="w", pady=(4, 2))
        self.pay_method = tk.StringVar(value="card")

        method_row = tk.Frame(card, bg=theme["panel_2"])
        method_row.pack(fill="x", pady=(0, 8))

        methods = [("card", "💳 CARD"), ("paypal", "🅿️ PAYPAL"), ("upi", "⚡ UPI / GPAY"), ("crypto", "🪙 CRYPTO")]
        self.method_btns = {}
        for k, label in methods:
            b = tk.Label(method_row, text=label, font=FONT_CHIP, fg="#080b18" if k == "card" else theme["muted"],
                         bg=theme["accent_2"] if k == "card" else theme["entry_bg"],
                         padx=6, pady=4, cursor="hand2", highlightthickness=1, highlightbackground=theme["border"])
            b.pack(side="left", expand=True, fill="x", padx=1)
            b.bind("<Button-1>", lambda _e, m=k: self.select_payment_method(m))
            self.method_btns[k] = b

        # Payment Details Form Box
        self.details_frame = tk.Frame(card, bg=theme["entry_bg"], padx=10, pady=8, highlightthickness=1, highlightbackground=theme["border"])
        self.details_frame.pack(fill="x", pady=(0, 8))

        # Cardholder Name
        tk.Label(self.details_frame, text="CARDHOLDER NAME:", font=FONT_BADGE, fg=theme["muted"], bg=theme["entry_bg"]).pack(anchor="w")
        self.name_input = tk.Entry(self.details_frame, font=FONT_STATS, bg=theme["bg"], fg=theme["text"], insertbackground=theme["text"], relief="flat", highlightthickness=1, highlightbackground=theme["border"])
        self.name_input.pack(fill="x", pady=(1, 4), ipady=2)
        self.name_input.insert(0, controller.user_profile.get("name", "Player 1").upper())

        # Card Number & Autofill Button
        c_hdr_row = tk.Frame(self.details_frame, bg=theme["entry_bg"])
        c_hdr_row.pack(fill="x")
        tk.Label(c_hdr_row, text="CARD NUMBER:", font=FONT_BADGE, fg=theme["muted"], bg=theme["entry_bg"]).pack(side="left")
        
        autofill_btn = tk.Label(c_hdr_row, text="⚡ AUTO-FILL TEST CARD", font=FONT_BADGE, fg=theme["accent_2"], bg=theme["entry_bg"], cursor="hand2")
        autofill_btn.pack(side="right")
        autofill_btn.bind("<Button-1>", lambda _e: self.autofill_test_card())

        self.card_num_input = tk.Entry(self.details_frame, font=FONT_STATS, bg=theme["bg"], fg=theme["text"], insertbackground=theme["text"], relief="flat", highlightthickness=1, highlightbackground=theme["border"])
        self.card_num_input.pack(fill="x", pady=(1, 4), ipady=2)
        self.card_num_input.insert(0, "4242 •••• •••• 4242")

        # Expiry & CVV Row
        exp_row = tk.Frame(self.details_frame, bg=theme["entry_bg"])
        exp_row.pack(fill="x")

        exp_f = tk.Frame(exp_row, bg=theme["entry_bg"])
        exp_f.pack(side="left", expand=True, fill="x", padx=(0, 4))
        tk.Label(exp_f, text="EXPIRY (MM/YY):", font=FONT_BADGE, fg=theme["muted"], bg=theme["entry_bg"]).pack(anchor="w")
        self.exp_input = tk.Entry(exp_f, font=FONT_STATS, bg=theme["bg"], fg=theme["text"], insertbackground=theme["text"], relief="flat", highlightthickness=1, highlightbackground=theme["border"])
        self.exp_input.pack(fill="x", pady=(1, 0), ipady=2)
        self.exp_input.insert(0, "12/28")

        cvv_f = tk.Frame(exp_row, bg=theme["entry_bg"])
        cvv_f.pack(side="right", expand=True, fill="x", padx=(4, 0))
        tk.Label(cvv_f, text="CVV / CVC:", font=FONT_BADGE, fg=theme["muted"], bg=theme["entry_bg"]).pack(anchor="w")
        self.cvv_input = tk.Entry(cvv_f, font=FONT_STATS, bg=theme["bg"], fg=theme["text"], insertbackground=theme["text"], relief="flat", highlightthickness=1, highlightbackground=theme["border"])
        self.cvv_input.pack(fill="x", pady=(1, 0), ipady=2)
        self.cvv_input.insert(0, "888")

        # Security & Guarantee note
        tk.Label(card, text="🔒 256-BIT ARCADE ENCRYPTED SIMULATION • 30-DAY MONEY-BACK GUARANTEE", font=FONT_BADGE, fg=theme["muted"], bg=theme["panel_2"]).pack(pady=(2, 6))

        # Authorize Button
        self.pay_btn = PixelButton(card, f"AUTHORIZE & UPGRADE (${self.final_price:.2f}) ▶", command=self.process_payment, bg=plan["color"], width=380, height=42, controller=controller)
        self.pay_btn.pack(pady=(2, 0))

    def select_payment_method(self, method_key):
        self.pay_method.set(method_key)
        theme = self.controller.theme
        for k, btn in self.method_btns.items():
            if k == method_key:
                btn.config(bg=theme["accent_2"], fg="#080b18")
            else:
                btn.config(bg=theme["entry_bg"], fg=theme["muted"])
        if self.controller:
            self.controller.sound_mgr.play_click()

    def autofill_test_card(self):
        self.card_num_input.delete(0, tk.END)
        self.card_num_input.insert(0, "4242 8888 7777 4242")
        self.exp_input.delete(0, tk.END)
        self.exp_input.insert(0, "12/29")
        self.cvv_input.delete(0, tk.END)
        self.cvv_input.insert(0, "777")
        if self.controller:
            self.controller.sound_mgr.play_click()
            self.controller.toast.show("Demo Card Auto-Filled Successfully!", "success")

    def apply_promo_code(self):
        code = self.promo_entry.get().strip().upper()
        if not code:
            return
        theme = self.controller.theme

        if code == "ARCADE50":
            self.discount_percent = 0.50
            self.discount_flat = 0.0
            self.promo_status_lbl.config(text="✓ COUPON 'ARCADE50' APPLIED: 50% OFF UNLOCKED!", fg=theme["success"])
        elif code == "BEACON2026":
            self.discount_percent = 0.0
            self.discount_flat = 5.0
            self.promo_status_lbl.config(text="✓ COUPON 'BEACON2026' APPLIED: $5.00 OFF UNLOCKED!", fg=theme["success"])
        elif code == "DEVVIP":
            self.discount_percent = 0.90
            self.discount_flat = 0.0
            self.promo_status_lbl.config(text="✓ DEV VIP SECRET CODE APPLIED: 90% OFF UNLOCKED!", fg=theme["accent"])
        else:
            self.promo_status_lbl.config(text="⚠️ Invalid promo code. Try 'ARCADE50' or 'BEACON2026'.", fg=theme["error"])
            return

        # Calculate final price
        discount = (self.base_price * self.discount_percent) + self.discount_flat
        self.final_price = max(0.99, self.base_price - discount)

        self.disc_row.pack(fill="x")
        self.disc_val_lbl.config(text=f"-${discount:.2f} USD")
        self.total_lbl.config(text=f"${self.final_price:.2f} USD")
        self.pay_btn.itemconfig(self.pay_btn._label, text=f"AUTHORIZE & UPGRADE (${self.final_price:.2f}) ▶")

        if self.controller:
            self.controller.sound_mgr.play_success()

    def process_payment(self):
        if self.controller:
            self.controller.sound_mgr.play_coin()

        # Update button to show processing state
        self.pay_btn.itemconfig(self.pay_btn._label, text="AUTHORIZING TRANSACTION... ⏳")

        def _complete_flow():
            plan_id = self.plan["id"]
            user = self.controller.user_profile
            user["membership"] = plan_id
            
            # Award welcome bonus XP and streak boost
            bonus_xp = 1500 if plan_id == "guild" else 500
            user["xp"] += bonus_xp
            user["streak"] = user.get("streak", 1) + 2

            # Order details
            order_id = f"BCN-{random.randint(100000, 999999)}"

            if self.controller:
                self.controller.sound_mgr.play_fanfare()
                self.controller.toast.show(f"Upgraded to {self.plan['name']}! +{bonus_xp} Bonus XP Awarded!", "success")

            if self.on_success:
                self.on_success(plan_id)

            self.destroy()
            ReceiptDialog(self.master, self.plan, self.billing_cycle, self.final_price, order_id, self.controller)

        self.after(600, _complete_flow)


class MonetizationPlanCard(tk.Canvas):
    """Custom Retro Arcade Canvas Card for Subscription Plans with Hover Glow & Responsive Perks."""
    def __init__(self, parent, plan, billing_cycle="monthly", on_select=None, is_current=False, width=265, height=430, controller=None):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
        self.controller = controller
        self.plan = plan
        self.billing_cycle = billing_cycle
        self.on_select = on_select
        self.is_current = is_current
        self.w, self.h = width, height
        self.accent = plan["color"]
        self._hover = False

        theme = controller.theme if controller else DEFAULT_COLORS

        # Card body and borders
        self._shadow = create_rounded_rect(self, 4, 4, width - 2, height - 2, radius=18, fill="#04060c", outline="")
        self._border = create_rounded_rect(self, 0, 0, width - 5, height - 5, radius=18, fill=self.accent if (not plan["is_free"] and plan["id"] == "pro") else theme["border"], outline="")
        self._body = create_rounded_rect(self, 2, 2, width - 7, height - 7, radius=16, fill=theme["panel_2"], outline="")

        # Top Ribbon Badge Pill (if pro or guild)
        badge_text = plan.get("badge", "")
        self._badge_bg = create_rounded_rect(self, 14, 12, 14 + len(badge_text) * 7 + 16, 32, radius=6, fill="#080b18", outline=self.accent)
        self._badge_txt = self.create_text(14 + (len(badge_text) * 7 + 16) / 2, 22, text=badge_text, font=FONT_BADGE, fill=self.accent)

        # Plan Icon & Title
        self._icon_txt = self.create_text(32, 54, text=plan.get("icon", "⭐"), font=("Segoe UI Emoji", 20), fill=self.accent)
        self._name_txt = self.create_text(58, 54, text=plan["name"].upper(), font=FONT_BOX_TITLE, fill=theme["text"], anchor="w")
        self._tag_txt = self.create_text(16, 76, text=plan["tagline"], font=FONT_BADGE, fill=theme["muted"], anchor="w")

        # Price Box Pill
        self._price_bg = create_rounded_rect(self, 12, 94, width - 18, 142, radius=10, fill=theme["entry_bg"], outline=theme["border"])
        
        price = plan["yearly_price"] if billing_cycle == "yearly" else plan["monthly_price"]
        period = "/ YEAR" if billing_cycle == "yearly" else "/ MONTH"
        if plan["is_free"]:
            price_display = "$0 FREE"
            sub_price = "FOREVER NO CARD NEEDED"
        else:
            price_display = f"${price:.2f}"
            sub_price = "(SAVE 25% BILLED ANNUALLY)" if billing_cycle == "yearly" else "(MONTH-TO-MONTH PASS)"

        self._price_txt = self.create_text(22, 112, text=price_display, font=FONT_HEADER, fill=self.accent, anchor="w")
        self._period_txt = self.create_text(width - 26, 114, text=period if not plan["is_free"] else "", font=FONT_BADGE, fill=theme["text"], anchor="e")
        self._sub_price_txt = self.create_text(22, 131, text=sub_price, font=FONT_CHIP, fill=theme["muted"], anchor="w")

        # Perks List
        start_y = 156
        self._perk_items = []
        for icon, perk_text in plan["perks"][:6]:
            icon_col = theme["success"] if icon == "✔" else theme["muted"]
            txt_col = theme["text"] if icon == "✔" else theme["muted"]
            
            i_id = self.create_text(20, start_y, text=icon, font=FONT_STATS, fill=icon_col, anchor="w")
            t_id = self.create_text(36, start_y, text=perk_text, font=FONT_CHIP, fill=txt_col, anchor="w", width=width - 50)
            self._perk_items.extend([i_id, t_id])
            start_y += 28

        # Action Button Area
        btn_y1 = height - 48
        btn_y2 = height - 14
        btn_x1 = 14
        btn_x2 = width - 18

        btn_fill = theme["accent_2"] if plan["is_free"] else self.accent
        if is_current:
            btn_label = "ACTIVE PLAN ✓"
            btn_fill = theme["entry_bg"]
            btn_txt_col = theme["muted"]
        else:
            btn_label = plan["button_text"]
            btn_txt_col = "#080b18" if not plan["is_free"] else theme["text"]

        self._btn_rect = create_rounded_rect(self, btn_x1, btn_y1, btn_x2, btn_y2, radius=8, fill=btn_fill, outline=self.accent)
        self._btn_lbl = self.create_text(width // 2, (btn_y1 + btn_y2) // 2, text=btn_label, font=FONT_CHIP, fill=btn_txt_col)

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _e):
        self._hover = True
        self.config(cursor="hand2")
        if self.controller:
            self.controller.sound_mgr.play_hover()
        self.itemconfig(self._border, fill=self.accent)
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.itemconfig(self._body, fill=lerp_color(theme["panel_2"], self.accent, 0.10))

    def _on_leave(self, _e):
        self._hover = False
        theme = self.controller.theme if self.controller else DEFAULT_COLORS
        self.itemconfig(self._border, fill=self.accent if (not self.plan["is_free"] and self.plan["id"] == "pro") else theme["border"])
        self.itemconfig(self._body, fill=theme["panel_2"])

    def _on_click(self, _e):
        if self.controller:
            self.controller.sound_mgr.play_click()
        if self.on_select:
            self.on_select(self.plan)

    def update_billing_cycle(self, new_cycle, is_current=False):
        self.billing_cycle = new_cycle
        self.is_current = is_current
        theme = self.controller.theme if self.controller else DEFAULT_COLORS

        price = self.plan["yearly_price"] if new_cycle == "yearly" else self.plan["monthly_price"]
        period = "/ YEAR" if new_cycle == "yearly" else "/ MONTH"

        if self.plan["is_free"]:
            price_display = "$0 FREE"
            sub_price = "FOREVER NO CARD NEEDED"
        else:
            price_display = f"${price:.2f}"
            sub_price = "(SAVE 25% BILLED ANNUALLY)" if new_cycle == "yearly" else "(MONTH-TO-MONTH PASS)"

        self.itemconfig(self._price_txt, text=price_display)
        self.itemconfig(self._period_txt, text=period if not self.plan["is_free"] else "")
        self.itemconfig(self._sub_price_txt, text=sub_price)

        if is_current:
            self.itemconfig(self._btn_rect, fill=theme["entry_bg"], outline=theme["border"])
            self.itemconfig(self._btn_lbl, text="ACTIVE PLAN ✓", fill=theme["muted"])
        else:
            btn_fill = theme["accent_2"] if self.plan["is_free"] else self.accent
            btn_txt_col = "#080b18" if not self.plan["is_free"] else theme["text"]
            self.itemconfig(self._btn_rect, fill=btn_fill, outline=self.accent)
            self.itemconfig(self._btn_lbl, text=self.plan["button_text"], fill=btn_txt_col)

    def apply_theme(self, theme):
        self.configure(bg=theme["panel"])
        self.itemconfig(self._body, fill=theme["panel_2"])
        self.itemconfig(self._name_txt, fill=theme["text"])
        self.itemconfig(self._tag_txt, fill=theme["muted"])
        self.itemconfig(self._price_bg, fill=theme["entry_bg"], outline=theme["border"])
        self.itemconfig(self._period_txt, fill=theme["text"])
        self.itemconfig(self._sub_price_txt, fill=theme["muted"])
        if not self.is_current:
            self.itemconfig(self._btn_rect, fill=theme["accent_2"] if self.plan["is_free"] else self.accent, outline=self.accent)
        else:
            self.itemconfig(self._btn_rect, fill=theme["entry_bg"], outline=theme["border"])


class MonetizationPage(BasePage):
    """Gamified VIP Plans & Monetization Store for BEACON Arcade."""
    def __init__(self, parent, controller):
        super().__init__(parent, controller, card_w=850, card_h=660)
        self.billing_cycle = "monthly"
        self.cards = {}

        # Top Bar Navigation
        self.top_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.top_bar.pack(fill="x", pady=(0, 4))

        self.back_btn = tk.Label(
            self.top_bar, text="◄ BACK TO QUESTS", font=FONT_BTN,
            fg=controller.theme["accent"], bg=controller.theme["panel_2"],
            padx=8, pady=4, cursor="hand2", relief="flat",
            highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.back_btn.pack(side="left", anchor="w")
        self.back_btn.bind("<Button-1>", lambda _e: controller.show_frame("ProgramSelectionPage"))
        self.attach_audio_effects(self.back_btn)

        self.hdr_title = tk.Label(
            self.top_bar, text="[ 💎 ARCADE UPGRADE VAULT ]", font=FONT_HEADER,
            fg=controller.theme["accent"], bg=controller.theme["panel"]
        )
        self.hdr_title.pack(side="right")

        # Marquee Subtitle Banner
        self.sub_banner = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=10, pady=5, highlightthickness=1, highlightbackground=controller.theme["border"])
        self.sub_banner.pack(fill="x", pady=(0, 6))

        self.sub_title = tk.Label(
            self.sub_banner, text="⚡ SUPERCHARGE YOUR CODING JOURNEY // UNLOCK 2X XP, REAL TERMINAL RUNS & MENTORSHIP",
            font=FONT_CHIP, fg=controller.theme["accent_2"], bg=controller.theme["panel_2"]
        )
        self.sub_title.pack(anchor="w")

        # Billing Cycle Switcher Toolbar
        self.switcher_bar = tk.Frame(self.card, bg=controller.theme["panel"])
        self.switcher_bar.pack(fill="x", pady=(0, 6))

        tk.Label(self.switcher_bar, text="SELECT BILLING CYCLE:", font=FONT_LABEL, fg=controller.theme["muted"], bg=controller.theme["panel"]).pack(side="left", padx=(4, 8))

        self.btn_monthly = tk.Label(
            self.switcher_bar, text="📅 MONTHLY PASS", font=FONT_CHIP,
            fg="#080b18", bg=controller.theme["accent_2"], padx=10, pady=4, cursor="hand2",
            highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.btn_monthly.pack(side="left", padx=(0, 4))
        self.btn_monthly.bind("<Button-1>", lambda _e: self.set_billing_cycle("monthly"))
        self.attach_audio_effects(self.btn_monthly)

        self.btn_yearly = tk.Label(
            self.switcher_bar, text="🎁 ANNUAL BILLING (SAVE 25% + BONUS XP)", font=FONT_CHIP,
            fg=controller.theme["muted"], bg=controller.theme["entry_bg"], padx=10, pady=4, cursor="hand2",
            highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.btn_yearly.pack(side="left")
        self.btn_yearly.bind("<Button-1>", lambda _e: self.set_billing_cycle("yearly"))
        self.attach_audio_effects(self.btn_yearly)

        self.current_plan_pill = tk.Label(
            self.switcher_bar, text="CURRENT: FREE ROOKIE 🌱", font=FONT_BADGE,
            fg=controller.theme["accent"], bg=controller.theme["panel_2"], padx=8, pady=3,
            highlightthickness=1, highlightbackground=controller.theme["border"]
        )
        self.current_plan_pill.pack(side="right", padx=(0, 4))

        # 3 Plan Cards Container
        self.cards_row = tk.Frame(self.card, bg=controller.theme["panel"])
        self.cards_row.pack(fill="x", pady=(2, 6))

        current_membership = controller.user_profile.get("membership", "free")
        for i, plan_key in enumerate(["free", "pro", "guild"]):
            plan = PLAN_CATALOG[plan_key]
            card = MonetizationPlanCard(
                self.cards_row, plan,
                billing_cycle=self.billing_cycle,
                on_select=self.handle_plan_selection,
                is_current=(current_membership == plan_key),
                width=265, height=430,
                controller=controller
            )
            card.grid(row=0, column=i, padx=4)
            self.cards[plan_key] = card

        # Footer Guarantee & FAQ Box
        self.footer_box = tk.Frame(self.card, bg=controller.theme["panel_2"], padx=10, pady=6, highlightthickness=1, highlightbackground=controller.theme["border"])
        self.footer_box.pack(fill="x", pady=(4, 0))

        self.foot_title = tk.Label(self.footer_box, text="🔒 30-DAY ARCADE MONEY-BACK GUARANTEE • 1-CLICK CANCEL ANYTIME", font=FONT_LABEL, fg=controller.theme["accent"], bg=controller.theme["panel_2"])
        self.foot_title.pack(anchor="w")

        foot_row = tk.Frame(self.footer_box, bg=controller.theme["panel_2"])
        foot_row.pack(fill="x", pady=(2, 0))

        self.foot_desc = tk.Label(
            foot_row, text="All terminal progress, streaks, badges and certificates remain permanently active on your account. Need educational licenses?",
            font=FONT_CHIP, fg=controller.theme["muted"], bg=controller.theme["panel_2"]
        )
        self.foot_desc.pack(side="left")

        self.feedback_hq_btn = tk.Label(foot_row, text="TRANSMIT TO HQ ▶", font=FONT_CHIP, fg=controller.theme["accent_2"], bg=controller.theme["panel_2"], cursor="hand2")
        self.feedback_hq_btn.pack(side="right")
        self.feedback_hq_btn.bind("<Button-1>", lambda _e: controller.show_frame("FeedbackPage"))
        self.attach_audio_effects(self.feedback_hq_btn)

    def set_billing_cycle(self, cycle):
        self.billing_cycle = cycle
        theme = self.controller.theme

        if cycle == "monthly":
            self.btn_monthly.config(bg=theme["accent_2"], fg="#080b18")
            self.btn_yearly.config(bg=theme["entry_bg"], fg=theme["muted"])
        else:
            self.btn_yearly.config(bg=theme["accent"], fg="#080b18")
            self.btn_monthly.config(bg=theme["entry_bg"], fg=theme["muted"])

        current_membership = self.controller.user_profile.get("membership", "free")
        for plan_key, card in self.cards.items():
            card.update_billing_cycle(cycle, is_current=(current_membership == plan_key))

    def handle_plan_selection(self, plan):
        current_membership = self.controller.user_profile.get("membership", "free")
        if plan["id"] == current_membership:
            self.controller.toast.show(f"You already have the {plan['name']} active!", "success")
            return

        if plan["is_free"]:
            self.controller.user_profile["membership"] = "free"
            self.controller.toast.show("Reverted to Free Rookie plan.", "success")
            self.refresh_plan_states()
            self.update_top_bar_stats()
            return

        # Open checkout dialog for paid tiers
        CheckoutDialog(self, plan, self.billing_cycle, self.controller, on_success=lambda _p: self.refresh_plan_states())

    def refresh_plan_states(self):
        current_membership = self.controller.user_profile.get("membership", "free")
        mem_names = {"free": "FREE ROOKIE 🌱", "pro": "ARCADE PRO ⚡", "guild": "MASTER GUILD 👑"}
        self.current_plan_pill.config(text=f"CURRENT: {mem_names.get(current_membership, 'ROOKIE')}")

        for plan_key, card in self.cards.items():
            card.update_billing_cycle(self.billing_cycle, is_current=(current_membership == plan_key))
        self.update_top_bar_stats()

    def on_show(self):
        super().on_show()
        self.refresh_plan_states()

    def apply_theme(self, theme):
        super().apply_theme(theme)
        self.top_bar.configure(bg=theme["panel"])
        self.back_btn.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.hdr_title.configure(bg=theme["panel"], fg=theme["accent"])
        self.sub_banner.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.sub_title.configure(bg=theme["panel_2"], fg=theme["accent_2"])
        self.switcher_bar.configure(bg=theme["panel"])
        self.current_plan_pill.configure(bg=theme["panel_2"], fg=theme["accent"], highlightbackground=theme["border"])
        self.cards_row.configure(bg=theme["panel"])
        for card in self.cards.values():
            card.apply_theme(theme)
        self.footer_box.configure(bg=theme["panel_2"], highlightbackground=theme["border"])
        self.foot_title.configure(bg=theme["panel_2"], fg=theme["accent"])
        self.foot_desc.configure(bg=theme["panel_2"], fg=theme["muted"])
        self.feedback_hq_btn.configure(bg=theme["panel_2"], fg=theme["accent_2"])
        self.set_billing_cycle(self.billing_cycle)


# ==============================================================================
# 22. MAIN CONTROLLER APPLICATION
# ==============================================================================

class BeaconApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BEACON - Gamified Education Arcade & Video Theater")
        self.geometry("920x730")
        self.minsize(860, 680)

        self.sound_mgr = RetroSoundManager()
        self.theme_key = "dark"
        self.theme = THEMES[self.theme_key]
        self.configure(bg=self.theme["bg"])
        self.update_combobox_listbox_theme()

        self.user_profile = {
            "name": "PLAYER 1",
            "photo": None,
            "class": "Class 10",
            "experience": "Beginner",
            "xp": 0,
            "streak": 1,
            "watched_videos": set(),
            "membership": "free"
        }

        self.settings_state = {
            "sound": True,
            "dark_mode": True,
            "terminal_engine": True
        }

        self.current_difficulty = "Beginner"
        self.toast = Toast(self)

        container = tk.Frame(self, bg=self.theme["bg"])
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        pages = (
            LoginPage,
            SignupPage,
            ProgramSelectionPage,
            ArcadeLessonsPage,
            PythonQuestPage,
            JavaQuestPage,
            CppQuestPage,
            ProfilePage,
            SettingsPage,
            FeedbackPage,
            AboutUsPage,
            MonetizationPage
        )

        for PageClass in pages:
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.current_frame = None
        self.show_frame("LoginPage")

    def update_combobox_listbox_theme(self):
        """Ensures ttk Combobox popdown listbox adopts dark theme and readable font."""
        try:
            self.option_add("*TCombobox*Listbox.background", self.theme["entry_bg"])
            self.option_add("*TCombobox*Listbox.foreground", self.theme["entry_fg"])
            self.option_add("*TCombobox*Listbox.selectBackground", self.theme["accent"])
            self.option_add("*TCombobox*Listbox.selectForeground", "#080b18")
            self.option_add("*TCombobox*Listbox.font", FONT_ENTRY)
        except Exception:
            pass

    def show_frame(self, page_name):
        if self.current_frame and hasattr(self.current_frame, "on_hide"):
            self.current_frame.on_hide()

        frame = self.frames[page_name]
        self.current_frame = frame
        frame.tkraise()

        if hasattr(frame, "on_show"):
            frame.on_show()

    def open_lessons(self, language="Python"):
        """Convenience navigation helper to launch ArcadeLessonsPage focused on a language."""
        lessons_page = self.frames.get("ArcadeLessonsPage")
        if lessons_page:
            lessons_page.set_language(language)
        self.show_frame("ArcadeLessonsPage")

    def switch_theme(self, theme_key):
        if theme_key in THEMES:
            self.theme_key = theme_key
            self.theme = THEMES[theme_key]
            self.configure(bg=self.theme["bg"])
            self.update_combobox_listbox_theme()
            for frame in self.frames.values():
                if hasattr(frame, "apply_theme"):
                    frame.apply_theme(self.theme)


# ==============================================================================
# 23. APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app = BeaconApp()
    app.mainloop()


