# Trust No One

A platformer where the level lies to you — and a lesson that builds it in front of you,
**one line at a time**, in 37 steps.

Open the lesson and you get one screen: the Python file on the left, and that exact file
**running** on the right. Not a video, not a copy — step 14 is `steps\step14.py`, playing.

---

## Start here (Windows)

### 1. Get Python

Open Microsoft Store, search **Python 3**, install it. Or download it from
[python.org/downloads](https://www.python.org/downloads/) — and on the **first screen** of
that installer, tick **"Add python.exe to PATH"** before you press Install. Nothing below
works without that tick.

To check it worked, press **Win+R**, type `cmd`, press Enter, and type:

```bat
py --version
```

You should see something like `Python 3.12.4`. If you see *'py' is not recognized*, Python
is not installed yet, or the PATH box was not ticked.

### 2. Get these files onto your computer

**The easy way — download the release:**

1. Open **[the latest release](https://github.com/qershyahya/trust-no-one/releases/latest)**
2. Under **Assets**, click **`trust-no-one.zip`**
   (or go straight to it: <https://github.com/qershyahya/trust-no-one/releases/latest/download/trust-no-one.zip>)
3. The file lands in your **Downloads** folder
4. **Right-click it → Extract All… → Extract**

You now have a folder called **`trust-no-one`**. Everything lives in there. Move it anywhere
you like — Desktop is fine.

**If you already have Git**, this is one line instead. In `cmd`:

```bat
cd %USERPROFILE%\Desktop
git clone https://github.com/qershyahya/trust-no-one.git
cd trust-no-one
```

That gives you a folder called `trust-no-one`, and `git pull` later fetches any changes.

### 3. Start the lesson

Open the folder you just extracted and **double-click `run-lesson.bat`**.

A black window opens, pygame installs itself if it is missing, and your browser opens the
lesson. Leave the black window alone while you work — closing it stops the lesson.

> Windows may show **"Windows protected your PC"** the first time. That is SmartScreen being
> careful about a file you downloaded, not a virus warning. Click **More info** →
> **Run anyway**. You can read the whole of `run-lesson.bat` in Notepad first; it is nine lines.

To just play the finished game, double-click **`play-the-game.bat`**.

### If you prefer typing

Open the folder in File Explorer, click the address bar at the top, type `cmd`, press
Enter — a black window opens **in that folder**. Then:

```bat
py -m pip install pygame
py main.py
```

Stop it with **Ctrl+C** in that window.

### macOS and Linux

Same three steps, with `python3` instead of `py`:

```bash
git clone https://github.com/qershyahya/trust-no-one.git
cd trust-no-one
python3 -m pip install pygame     # or: sudo apt install python3-pygame
python3 main.py
```

---

## What you are looking at

```
┌───────────────────────────────┬──────────────────────────┐
│  the code for this step       │   that code, running     │
│                               │                          │
│  green  = added at this step  │   ← →  walk              │
│  red    = removed here        │   Space jump             │
│  green italic = a comment     │   click throw a pebble   │
│                               │   R restart              │
└───────────────────────────────┴──────────────────────────┘
```

- **The step strip along the top** jumps to any of the 37 steps.
- **Hover any name** in the code — `GRAV`, `prect`, `min`, `blit` — and it tells you what it
  means. Abbreviations are spelled out; functions show what goes in and what comes out,
  *as they are at that step*.
- **Hover a line number** on an older line and it tells you which step wrote it. Click it and
  you go back to that step.
- **The controls under the screen appear as you build them.** At step 1 there is nothing to
  press. Jump appears at step 14, the pebble at step 24.

Nothing is uploaded and nothing is downloaded. The game runs on your own computer, in real
pygame, and its picture is sent to the page.

---

## Run one step on its own

Every step is a real program. Open one in a text editor — IDLE, Notepad, VS Code, anything —
change a number, run it again. That is the whole loop of making a game.

```bat
py steps\step07.py     :: floors and walls
py steps\step14.py     :: the jump
py steps\step37.py     :: the finished game
```

Things worth breaking: make `GRAV` 0.1, make `JUMP` -20, set `CRUMB` to 5, or change a `#` in
the level to a `%` and see what you fall through.

---

## The game itself

You run right, toward a green exit, picking up coins. A purple wizard curses you — and from
that moment the level is not what it looks like:

| letter | looks like | really is |
|:---:|---|---|
| `#` | a brick | a brick |
| `%` | a brick | a hologram, once you are cursed |
| `^` | spikes | spikes |
| `t` | spikes | a trampoline |
| `o` | a coin | a coin |
| `x` | a coin | it kills you |
| `~` | nothing | floor |
| `c` | a brick | it breaks after half a second |
| `G` | the exit | the exit |
| `!` | the exit | it throws you back to the start |

**Throw a pebble** at anything you do not trust. Whatever it hits is drawn in its true colour
from then on. That is your only way of telling them apart — and `?` and `&` are rolled fresh
every run, so a level cannot be memorised.

Five levels, each built on a different lie.

---

## The robot

You cannot hand-test twelve dice rolls across five levels before a jam deadline, so the game
tests itself, with no window at all:

```bat
py steps\step37.py --test
```

It plays itself with fake key presses and checks the answers — that a tap hops lower than a
held jump, that a hologram drops you once cursed, that invisible floor still holds you, and
that **no roll of the dice can ever produce a hole nobody could jump**. It prints one word,
`ok`, or stops on the line that is wrong and tells you which seed broke it.

---

## What is in here

| file | what it is |
|---|---|
| `run-lesson.bat` | double-click this to start the lesson (Windows) |
| `play-the-game.bat` | double-click this to play the finished game (Windows) |
| `main.py` | the lesson: runs the game, streams it to the page, serves the page |
| `lesson.html` | the page itself |
| `lesson_text.py` | what the lesson says: the prose, the line notes, the hover hints |
| `build_steps.py` | writes the 37 step files |
| `steps\step01.py` … `step37.py` | the lesson, as runnable programs. `step37.py` is the finished game |

The step files are **generated**. Every piece of the program is written down once, in
`build_steps.py`, which knows what that piece looks like at each step — so no two steps can
drift apart. Rebuild them any time:

```bat
py build_steps.py
```

It refuses to finish unless the last step still plays the whole game correctly, which it
checks by making it play itself.

## If something goes wrong

| what you see | what it means |
|---|---|
| `'py' is not recognized` | Python is not installed, or PATH was not ticked during install. Reinstall and tick **Add python.exe to PATH** |
| `ModuleNotFoundError: No module named 'pygame'` | type `py -m pip install pygame` |
| the black window flashes and vanishes | run it from `cmd` instead of double-clicking, so you can read the error |
| `Cannot use port 8756` | a lesson is already running. Open http://127.0.0.1:8756/ , or `set LESSON_PORT=8757 && py main.py` |
| the picture stops moving | the page tells you, and offers **restart this step** |

---

Made for a game jam, and for one student.
