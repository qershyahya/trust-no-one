def self_test(path):
    """The finished step tests the whole game with no window. If that passes, the
    generated files are not just syntactically fine -- they play correctly."""
    env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy")
    r = subprocess.run([sys.executable, path, "--test"], capture_output=True, text=True, env=env)
    return r.returncode == 0 and r.stdout.strip().endswith("ok"), (r.stdout + r.stderr).strip()


"""Generate the thirty-seven runnable step files for Trust No One.

Every step file is a real pygame program: `py steps\\step14.py` opens a window and
plays. The last step, step37.py, is the finished game.

    python3 build_steps.py         # writes steps/step01.py .. steps/step37.py

Each piece of the program is emitted by a small function that knows what that piece
looks like at step n, so no line of the game is written down twice and the steps
cannot drift apart. Before it finishes, the last step is made to play the whole game
with no window and check its own answers.
"""
import ast
import difflib
import os
import subprocess
import sys
import textwrap
import tokenize
from io import StringIO

from lesson_text import NOTES

TITLES = [
    "A window that stays open",          # 1
    "A box on the screen",               # 2
    "Keys move the box",                 # 3
    "Gravity",                           # 4
    "The world is text",                 # 5
    "Drawing the world",                 # 6
    "Where you start",                   # 7
    "Your box as a Rect",                # 8
    "Which squares am I touching",       # 9
    "Walls: the sideways pass",          # 10
    "Floors: the up-down pass",          # 11
    "Falling out of the world",          # 12
    "Am I on the ground",                # 13
    "A jump",                            # 14
    "Coyote time",                       # 15
    "Jump buffer",                       # 16
    "Tap for a small hop",               # 17
    "Momentum",                          # 18
    "The camera",                        # 19
    "Coins",                             # 20
    "Spikes",                            # 21
    "The wizard, and the curse",         # 22
    "The brick that is not there",       # 23
    "Throwing a pebble",                 # 24
    "What the pebble reveals",           # 25
    "Spikes that are trampolines",       # 26
    "Coins that kill you",               # 27
    "Floor you cannot see",              # 28
    "Bricks that crumble",               # 29
    "The exit that lies",                # 30
    "Dice",                              # 31
    "Dice that cannot trap you",         # 32
    "Five levels",                       # 33
    "The bar along the top",             # 34
    "Wind",                              # 35
    "The warp",                          # 36
    "A robot that plays it for you",     # 37
]
LAST = len(TITLES)
HERE = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------- the level

# 60 columns, 20 rows. Rows 0-12 and 14 are empty sky.
BASE = {
    13: " " * 60,
    15: " " * 22 + "####" + " " * 15 + "######",
    16: " " * 60,
    17: " " * 57 + "G",
    18: "#" * 60,
    19: "#" * 60,
}
# (step, row, column, what to write) -- the world grows one lie at a time
PATCHES = [
    (7, 17, 1, "P"),                                   # where you start
    (14, 18, 20, "    "), (14, 19, 20, "    "),        # a pit to jump over
    (20, 13, 44, "o  o"), (20, 16, 38, "o"), (20, 16, 52, "o"),   # coins to collect
    (21, 17, 34, "^"),                                 # a spike on the path
    (22, 17, 15, "W"),                                 # the wizard
    (23, 18, 10, "%%%"), (23, 19, 10, "   "),          # a hologram bridging a hole
    (26, 19, 20, "tttt"),                              # spikes at the bottom of the pit
    (27, 16, 12, "x"),                                 # a coin that is not one
    (28, 18, 30, "~~~~"), (28, 19, 30, "    "),        # floor you cannot see
    (29, 18, 40, "cccc"), (29, 19, 40, "    "),        # floor that will not last
    (30, 17, 46, "!"),                                 # an exit that is not one
    (31, 18, 10, "&&&"), (31, 19, 20, "????"),         # rolled fresh every run
]

# The five levels of the finished game, and their names. This is where they live.
REAL_LEVELS = {
    'L1': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '                                            o  o',
        '',
        '                      ####               ###&&##',
        '            x                         o             o',
        ' P   W                   ??       ^ ??                   G',
        '##########   #######    ####################################',
        '##########ttt#######    ####################################',
    ],
    'L2': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '                                   o  o              o           o',
        '             ###                   ##&&             ###                    ##',
        '                 x                                        o             x',
        ' P                                                                           G',
        '##########%%##&&####  %%#########%%#####    ######&&##########  %%##############',
        '####################  tt################    ##################  tt##############',
    ],
    'L3': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '                                           ~~~                        ',
        '               o                            o                  o      ',
        '                         o                              o             ',
        ' P                                                                           G',
        '##########~~~   ~~~~##########  ~  ~  ~~##########~~~~~  ~ ~####################',
        '##########          ##########          ##########          ####################',
    ],
    'L4': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '                                          ###                         ',
        '            x  o                 x   o               o  x             ',
        '',
        '',
        ' P                                                                           G',
        '##########ccccc###############cc#cccc#############cccc#ccc  ####################',
        '##########     ###############       #############          ####################',
    ],
    'L5': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '                                                                                       G',
        '                                                                                      ####',
        '                                                                         o',
        '               o           x                         o                     x',
        '                           &&                                                  ',
        ' P          ??                                !                                 ',
        '##########  ##  ####ccccccc### ~  ~ ######%%######  ########cc#cc#####    #########%%#####',
        '##########  ##  ####       ###      ######tt######  ?????###     tt###    #########tt#####',
    ],
}
REAL_NAMES = ['I. The Curse', 'II. The Floor Lies', 'III. The Gaps Lie', 'IV. Nothing Holds', 'V. The Gauntlet']


def real_level(name, rows):
    """Rewrite one of the finished game's levels as full-width rows."""
    width = max(len(r) for r in rows)
    out = ["%s = [" % name]
    for r in rows:
        out.append("    " + fmt_row(r, width) + ",")
    out.append("]")
    return "\n".join(out).replace("ROW", '"%s"' % (" " * width))


def grid_at(n):
    rows = {r: list(t.ljust(60)) for r, t in BASE.items()}
    for step, r, c, text in PATCHES:
        if step <= n:
            for i, ch in enumerate(text):
                rows[r][c + i] = ch
    return {r: "".join(v) for r, v in rows.items()}


def fmt_row(text, width=60):
    """One row, one string, every row the same width. Count columns straight off it."""
    text = text.ljust(width)
    return "ROW" if text.strip() == "" else '"%s"' % text


def emit_level(n):
    if n >= 33:
        return real_level("L1", REAL_LEVELS["L1"])
    g = grid_at(n)
    out = ['ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces',
           "L1 = [", "    " + ", ".join(["ROW"] * 13) + ","]
    out.append("    " + fmt_row(g[13]) + ",")
    out.append("    ROW,")
    for r in (15, 16, 17, 18, 19):
        out.append("    " + fmt_row(g[r]) + ",")
    out.append("]")
    return "\n".join(out)


def emit_alphabet(n):
    if n < 5:
        return None
    honest = "'#' brick"
    if n >= 20:
        honest += "  'o' coin"
    if n >= 21:
        honest += "  '^' spike"
    if n >= 22:
        honest += "  'W' wizard"
    honest += "  'G' exit  'P' spawn"
    if n < 23:
        return "# every tile is one letter: " + honest
    lies = []
    if n >= 23:
        lies.append("'%' hologram brick")
    if n >= 26:
        lies.append("'t' spike that is a trampoline")
    if n >= 27:
        lies.append("'x' coin that kills")
    if n >= 28:
        lies.append("'~' floor that isn't drawn")
    if n >= 29:
        lies.append("'c' brick that crumbles")
    if n >= 30:
        lies.append("'!' exit that warps you back")
    text = "# honest: " + honest + "\n# lies:   " + "   ".join(lies)
    if n >= 31:
        text += ("\n# rolled per run, so nothing can be memorised:\n"
                 "#         '?' spike or trampoline      '&' brick or hologram")
    if n >= 32:
        text += ("\n# every run of '?' keeps one trampoline and every run of '&' one real brick,"
                 " so no roll is a dead end")
    return text


# --------------------------------------------------------------- constants

def emit_consts(n):
    out = ["TILE, VW, VH = 32, 960, 640" if n >= 5 else "VW, VH = 960, 640", ""]
    if n < 14:
        if n >= 3:
            out.append("SPD = 3.6                             # top walking speed, pixels per frame")
        if n >= 4:
            out.append("GRAV, MAXFALL = 0.35, 12              # pull per frame, and the fastest you may fall")
        if n >= 2:
            out.append("PW, PH = 20, 28                       # how big you are")
    else:
        out.append("# feel knobs, tuned at 60fps")
        if n >= 26:
            out.append("GRAV, SPD, JUMP, BOUNCE, MAXFALL = 0.35, 3.6, -9.2, -12.3, 12")
        else:
            out.append("GRAV, SPD, JUMP, MAXFALL = 0.35, 3.6, -9.2, 12")
        if n >= 18:
            out.append("ACC, AIR, FRIC = 0.55, 0.32, 0.72")
        if n == 15:
            out.append("COYOTE = 7                            # you may still jump 7 frames after the edge")
        elif n == 16:
            out.append("COYOTE, BUFFER = 7, 8                 # late jump, early jump")
        elif n >= 17:
            out.append("COYOTE, BUFFER, CUT = 7, 8, 0.42     # late jump, early jump, tap = short hop")
        if n >= 29:
            out.append("CRUMB = 26                            # frames a crumbling brick holds you")
        if n >= 35:
            out.append("GUST = [0.0, 0.0, 0.04, 0.10, 0.14]   # per-level wind strength, sign flips every few seconds")
        out.append("PW, PH = 20, 28")
    return "\n".join(out).strip("\n")


def emit_globals(n):
    out = []
    if n >= 33:
        out.append("LVL, COLS, ROWS, SPAWN, level, seed = [], 0, 0, (0, 0), 0, 0")
    elif n >= 31:
        out.append("LVL, COLS, ROWS, SPAWN, seed = [], 0, 0, (0, 0), 0")
    elif n >= 7:
        out.append("LVL, COLS, ROWS, SPAWN = [], 0, 0, (0, 0)")
    elif n >= 5:
        out.append("LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured")

    if n >= 7:
        out.append("P = {}")
    elif n >= 2:
        out.append('P = {"x": 64.0, "y": 288.0, "vx": 0.0, "vy": 0.0}     # where you are, and how fast')

    if n >= 33:
        out.append("cursed = wizard = won = False")
    elif n >= 22:
        out.append("cursed = wizard = False")

    counters = []
    if n >= 20:
        counters.append("coins")
    if n >= 29:
        counters.append("frames")
    if n >= 33:
        counters.append("total")
    if n >= 15:
        counters.append("coy")
    if n >= 16:
        counters.append("buf")
    if counters:
        out.append(" = ".join(counters) + " = 0")
    if n >= 36:
        out.append("warp = 0.0")

    order = [("taken", "set()", 20), ("revealed", "set()", 25), ("gone", "set()", 29),
             ("pebbles", "[]", 24), ("crumb", "{}", 29)]
    bags = [(name, init) for name, init, since in order if n >= since]
    if bags:
        out.append(", ".join(b[0] for b in bags) + " = " + ", ".join(b[1] for b in bags))
    return "\n".join(out)


# --------------------------------------------------------------- functions

def emit_roll(n):
    if n < 31:
        return None
    guard = ("            if safe not in span:\n"
             "                span[rng.randrange(len(span))] = safe\n") if n >= 32 else ""
    doc = ('"""\'?\' and \'&\' pick a side per run -- but each run of them keeps one safe tile."""'
           if n >= 32 else '"""\'?\' and \'&\' pick a side per run, from this run\'s dice."""')
    return ('def roll(row, rng):\n'
            '    %s\n'
            '    out = list(row)\n'
            '    i = 0\n'
            '    while i < len(out):\n'
            '        if out[i] in "?&":\n'
            '            ch, j = out[i], i\n'
            '            while j < len(out) and out[j] == ch:\n'
            '                j += 1\n'
            '            safe, other = ("t", "^") if ch == "?" else ("#", "%%")\n'
            '            span = [rng.choice((safe, other)) for _ in range(j - i)]\n'
            '%s'
            '            out[i:j] = span\n'
            '            i = j\n'
            '        else:\n'
            '            i += 1\n'
            '    return "".join(out)') % (doc, guard)


def emit_load(n):
    if n < 5:
        return None
    if n >= 33:
        return '''def load(i):
    global LVL, COLS, ROWS, SPAWN, level, frames
    level, frames = i, 0
    rows = LEVELS[i]
    COLS = max(len(r) for r in rows)
    rng = random.Random(seed * 977 + i)
    LVL = [roll(r.ljust(COLS), rng) for r in rows]
    ROWS = len(LVL)
    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")
    LVL = [r.replace("P", " ") for r in LVL]
    taken.clear(); revealed.clear(); gone.clear(); pebbles.clear(); crumb.clear()
    die()'''
    out = ["def load():"]
    if n >= 7:
        out.append('    """Measure the level, find the P, then erase it so it is never drawn."""')
        out.append("    global LVL, COLS, ROWS, SPAWN")
    else:
        out.append('    """Pad every row to the same width, so LVL[r][c] never runs off the end."""')
        out.append("    global LVL, COLS, ROWS")
    out.append("    COLS = max(len(r) for r in L1)")
    if n >= 31:
        out.append("    rng = random.Random(seed * 977)")
        out.append("    LVL = [roll(r.ljust(COLS), rng) for r in L1]")
    else:
        out.append("    LVL = [r.ljust(COLS) for r in L1]")
    out.append("    ROWS = len(LVL)")
    if n >= 7:
        out.append('    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")')
        out.append('    LVL = [r.replace("P", " ") for r in LVL]')
    clears = [name for name, since in (("taken", 20), ("revealed", 25), ("gone", 29),
                                       ("pebbles", 24), ("crumb", 29)) if n >= since]
    if clears:
        out.append("    " + "; ".join("%s.clear()" % c for c in clears))
    if n >= 12:
        out.append("    die()")
    elif n >= 7:
        out.append('    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)')
    return "\n".join(out)


def emit_reset(n):
    if n < 22:
        return None
    if n >= 33:
        return '''def reset():
    global cursed, wizard, won, coins, total, seed
    seed = random.randrange(1 << 30)
    cursed, won, coins, total = False, False, 0, 0
    wizard = True
    load(0)'''
    names = ["cursed", "wizard", "coins"] + (["seed"] if n >= 31 else [])
    out = ["def reset():", "    global " + ", ".join(names)]
    if n >= 31:
        out.append("    seed = random.randrange(1 << 30)")
    out += ["    cursed, coins = False, 0", "    wizard = True", "    load()"]
    return "\n".join(out)


def emit_die(n):
    if n < 12:
        return None
    fields = 'x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0'
    if n >= 13:
        fields += ", g=False"
    if n >= 14:
        fields += ", jump=False"
    if n >= 36:
        return "def die():\n    global warp\n    warp = max(warp, 6.0)\n    P.update(%s)" % fields
    return 'def die():\n    """Back to the start, standing still."""\n    P.update(%s)' % fields


def emit_wind(n):
    if n < 35:
        return None
    return "def wind():\n    return GUST[level] * math.sin(frames / 110.0) if cursed else 0.0"


def emit_tile(n):
    if n < 5:
        return None
    doc = '    """What letter is at column c, row r? Off the map counts as empty air."""\n' if n < 33 else ""
    return 'def tile(c, r):\n%s    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "' % doc


def emit_solid(n):
    if n < 10:
        return None
    if n >= 29:
        body = 'return ch in "#~c" or (ch == "%" and not cursed)'
    elif n >= 28:
        body = 'return ch in "#~" or (ch == "%" and not cursed)'
    elif n >= 23:
        body = 'return ch == "#" or (ch == "%" and not cursed)'
    else:
        body = 'return ch == "#"'
    return "def solid(ch):\n    " + body


def emit_prect(n):
    if n < 8:
        return None
    doc = '    """Your box, right now."""\n' if n < 33 else ""
    return 'def prect():\n%s    return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)' % doc


def emit_cells(n):
    if n < 9:
        return None
    doc = '    """Every tile this box overlaps -- usually two to six of them."""\n' if n < 33 else ""
    test = 'if ch != " " and (c, r) not in gone:' if n >= 29 else 'if ch != " ":'
    return ('def cells(rect):\n%s'
            '    for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):\n'
            '        for c in range(rect.left // TILE, (rect.right - 1) // TILE + 1):\n'
            '            ch = tile(c, r)\n'
            '            %s\n'
            '                yield c, r, ch') % (doc, test)


def emit_step(n):
    if n < 3:
        return None
    sig = "def step(left, right, pressed=False, held=False):" if n >= 14 else "def step(left, right):"
    body = []

    glob = []
    if n >= 22:
        glob += ["cursed", "wizard"]
    if n >= 33:
        glob.append("won")
    if n >= 20:
        glob.append("coins")
    if n >= 29:
        glob.append("frames")
    if n >= 33:
        glob.append("total")
    if n >= 15:
        glob.append("coy")
    if n >= 16:
        glob.append("buf")
    if n >= 36:
        glob.append("warp")
    if glob:
        body.append("    global " + ", ".join(glob))
    if n >= 33:
        body.append("    frames += 1; total += 1")
    elif n >= 29:
        body.append("    frames += 1")
    if n >= 36:
        body.append("    warp = max(0.0, warp - 0.16)")
    if body:
        body.append("")

    if n >= 18:
        body += ["    want = (right - left) * SPD",
                 '    a = ACC if P["g"] else AIR',
                 "    if want:",
                 '        P["vx"] += max(-a, min(a, want - P["vx"]))',
                 "    else:",
                 '        P["vx"] *= FRIC if P["g"] else 0.96']
    else:
        body.append('    P["vx"] = (right - left) * SPD')
    if n >= 35:
        body.append('    P["vx"] += wind() * (1.0 if P["g"] else 2.2)   # gusts shove hardest in the air')

    if n >= 14:
        if n >= 15:
            body.append('    coy = COYOTE if P["g"] else coy - 1')
        if n >= 16:
            body.append("    buf = BUFFER if pressed else buf - 1")
            body.append("    if buf > 0 and coy > 0:")
        elif n >= 15:
            body.append("    if pressed and coy > 0:")
        else:
            body.append('    if pressed and P["g"]:')
        names, values = ['P["vy"]'], ["JUMP"]
        if n >= 16:
            names += ["buf", "coy"]; values += ["0", "0"]
        elif n >= 15:
            names.append("coy"); values.append("0")
        if n >= 17:
            names.append('P["jump"]'); values.append("True")
        body.append("        " + ", ".join(names) + " = " + ", ".join(values))
        if n >= 17:
            tail = " -- never cuts a trampoline" if n >= 26 else ""
            body += ['    if P["jump"] and not held and P["vy"] < JUMP * CUT:',
                     '        P["vy"], P["jump"] = JUMP * CUT, False    # let go early, hop short' + tail,
                     '    if P["vy"] >= 0:',
                     '        P["jump"] = False']

    if n >= 4:
        body.append('    P["vy"] = min(P["vy"] + GRAV, MAXFALL)')
    body.append("")

    if n >= 10:
        body += ['    P["x"] += P["vx"]',
                 "    r = prect()",
                 "    for c, _, ch in cells(r):",
                 "        if solid(ch):",
                 '            if P["vx"] > 0: r.right = c * TILE',
                 '            elif P["vx"] < 0: r.left = (c + 1) * TILE',
                 '            P["x"] = float(r.x); P["vx"] = 0.0']
    else:
        body.append('    P["x"] += P["vx"]')
    if n >= 11:
        body += ["",
                 '    P["y"] += P["vy"]',
                 "    r = prect()",
                 "    for _, rw, ch in cells(r):",
                 "        if solid(ch):",
                 '            if P["vy"] > 0: r.bottom = rw * TILE',
                 '            elif P["vy"] < 0: r.top = (rw + 1) * TILE',
                 '            P["y"] = float(r.y); P["vy"] = 0.0']
    elif n >= 4:
        body.append('    P["y"] += P["vy"]')
    if n >= 13:
        body += ["    # ponytail: 1px probe instead of trusting penetration -- sub-pixel gravity never sinks a full pixel",
                 '    P["g"] = P["vy"] >= 0 and any(solid(ch) for _, _, ch in cells(prect().move(0, 1)))']

    if n >= 29:
        body += ["",
                 '    if P["g"]:                                    # crumbling bricks only count while stood on',
                 "        for c, rw, ch in cells(prect().move(0, 1)):",
                 '            if ch == "c":',
                 "                crumb[(c, rw)] = crumb.get((c, rw), 0) + 1",
                 "                if crumb[(c, rw)] > CRUMB:",
                 "                    gone.add((c, rw))"]

    if n >= 12:
        body += ["", '    if P["y"] > ROWS * TILE:',
                 "        return die()" if n >= 20 else "        die()"]

    if n >= 20:
        body.append("    for c, rw, ch in cells(prect()):")
        deadly = []
        if n >= 21:
            deadly.append('ch == "^"')
        if n >= 26:
            deadly.append('(ch == "t" and not cursed)')
        if n >= 27:
            deadly.append('(ch == "x" and cursed)')
        opened = False
        if deadly:
            body.append("        if " + " or ".join(deadly) + ":")
            body.append("            return die()")
            opened = True
        if n >= 26:
            body.append('        if ch == "t" and cursed:')
            body.append('            P["vy"], P["g"], P["jump"] = BOUNCE, False, False')
            opened = True
        if n >= 30:
            body.append('        %s ch == "!":' % ("elif" if opened else "if"))
            if n >= 36:
                body.append("            warp = 22.0")
            body.append("            return die()")
            opened = True
        coin = '(ch == "o" or ch == "x")' if n >= 27 else 'ch == "o"'
        body.append('        %s %s and (c, rw) not in taken:' % ("elif" if opened else "if", coin))
        body.append("            taken.add((c, rw)); coins += 1")
        if n >= 22:
            body.append('        elif ch == "W" and wizard:')
            body.append("            wizard, cursed, warp = False, True, 26.0" if n >= 36
                        else "            wizard, cursed = False, True")
        if n >= 33:
            body += ['        elif ch == "G":',
                     "            if level + 1 < len(LEVELS):",
                     "                return load(level + 1)",
                     "            won = True"]

    text = sig + "\n" + "\n".join(body)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.rstrip()


def emit_pebble(n):
    if n < 24:
        return None
    doc = '    """Click far away for a hard throw, close for a soft lob."""\n' if n < 33 else ""
    wind_line = "        pb[2] += wind() * 1.6\n" if n >= 35 else ""
    hit = 'if tile(c, r) != " " and (c, r) not in gone:' if n >= 29 else 'if tile(c, r) != " ":'
    reveal = ("            revealed.update((c + i, r + j) for i in (-1, 0, 1) for j in (-1, 0, 1))\n"
              if n >= 25 else "")
    return ('def throw(tx, ty):\n'
            '%s'
            '    cx, cy = P["x"] + PW / 2, P["y"] + PH / 2\n'
            '    dx, dy = tx - cx, ty - cy\n'
            '    d = max(1.0, (dx * dx + dy * dy) ** 0.5)\n'
            '    sp = max(4.5, min(16.0, d / 20.0))        # close click = soft lob, far click = hard throw\n'
            '    pebbles.append([cx, cy, dx / d * sp, dy / d * sp])\n'
            '\n'
            '\n'
            'def pebble_step():\n'
            '    for pb in pebbles[:]:\n'
            '        pb[3] += GRAV * 0.5\n'
            '%s'
            '        pb[0] += pb[2]; pb[1] += pb[3]\n'
            '        c, r = int(pb[0]) // TILE, int(pb[1]) // TILE\n'
            '        if not (0 <= c < COLS and 0 <= r < ROWS):\n'
            '            pebbles.remove(pb); continue\n'
            '        %s\n'
            '%s'
            '            pebbles.remove(pb)') % (doc, wind_line, hit, reveal)


def emit_palette(n):
    if n < 6:
        return None
    if n >= 29:
        text = ('LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "c": (150, 110, 70),\n'
                '        "^": (170, 170, 180), "t": (170, 170, 180), "o": (240, 200, 60), "x": (240, 200, 60)}')
    else:
        look = [('"#"', "(150, 110, 70)", 6)]
        if n < 22:
            look.append(('"G"', "(90, 230, 190)", 6))
        look += [('"%"', "(150, 110, 70)", 23), ('"^"', "(170, 170, 180)", 21),
                 ('"t"', "(170, 170, 180)", 26), ('"o"', "(240, 200, 60)", 20),
                 ('"x"', "(240, 200, 60)", 27)]
        items = ["%s: %s" % (k, v) for k, v, since in look if n >= since]
        text = "LOOK = {" + ", ".join(items) + "}"
    if n >= 25:
        text += "\n# ponytail: a revealed lie keeps its own hue and goes darker/duller -- readable, never neon\n"
        if n >= 30:
            text += ('TRUTH = {"%": (108, 84, 66), "t": (146, 162, 148), "x": (206, 168, 96),\n'
                     '         "~": (50, 50, 66), "c": (126, 92, 58), "!": (66, 178, 158)}')
        else:
            truth = [('"%"', "(108, 84, 66)", 25), ('"t"', "(146, 162, 148)", 26),
                     ('"x"', "(206, 168, 96)", 27), ('"~"', "(50, 50, 66)", 28),
                     ('"c"', "(126, 92, 58)", 29)]
            text += "TRUTH = {" + ", ".join("%s: %s" % (k, v) for k, v, since in truth if n >= since) + "}"
    return text


def emit_liars(n):
    if n < 23:
        return None
    letters = "%"
    for ch, since in (("t", 26), ("x", 27), ("~", 28), ("c", 29), ("!", 30)):
        if n >= since:
            letters += ch
    return 'LIARS = set("%s")' % letters


def emit_edge(n):
    return None if n < 25 else "def edge(col):\n    return tuple(max(0, v - 40) for v in col)"


def emit_clock(n):
    return None if n < 34 else 'def clock_str(f):\n    return "%d:%02d" % (f // 3600, f // 60 % 60)'


def emit_draw(n):
    if n < 6:
        return None
    args = "scr, font, big" if n >= 34 else ("scr, font" if n >= 20 else "scr")
    out = ["def draw(%s):" % args]
    if n >= 19:
        out.append('    cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))')
    out.append("    scr.fill((25, 25, 35))")
    out.append("    for r in range(ROWS):")
    out.append("        for c in range(cam // TILE, min(COLS, cam // TILE + VW // TILE + 2)):"
               if n >= 19 else "        for c in range(COLS):")
    out.append("            ch = LVL[r][c]")

    skip = ['ch == " "']
    if n >= 20:
        skip.append("(c, r) in taken")
    if n >= 29:
        skip.append("(c, r) in gone")
    if n >= 22:
        skip.append('(ch == "W" and not wizard)')
    out.append("            if " + " or ".join(skip) + ":")
    out.append("                continue")

    cam = " - cam" if n >= 19 else ""
    out.append("            box = pygame.Rect(c * TILE%s, r * TILE, TILE, TILE)" % cam)
    if n >= 25:
        out.append("            seen = (c, r) in revealed")
    if n >= 29:
        out.append('            if ch == "c" and crumb.get((c, r)):')
        out.append("                box = box.move(int(math.sin(frames) * 2), 0)      # about to give way")
    if n >= 25:
        out.append("            lie = seen and ch in LIARS")

    branches = []
    if n >= 20:
        if n >= 27:
            branches.append(('if ch in "ox":',
                             ["col = TRUTH[ch] if lie else LOOK[ch]",
                              "pygame.draw.circle(scr, col, box.center, 9)",
                              "if lie: pygame.draw.circle(scr, edge(col), box.center, 9, 2)"]))
        else:
            branches.append(('if ch == "o":', ["pygame.draw.circle(scr, LOOK[ch], box.center, 9)"]))
    if n >= 21:
        if n >= 26:
            branches.append(('elif ch in "^t":',
                             ["col = TRUTH[ch] if lie else LOOK[ch]",
                              "pts = [box.bottomleft, (box.centerx, box.top), box.bottomright]",
                              "pygame.draw.polygon(scr, col, pts)",
                              "if lie: pygame.draw.polygon(scr, edge(col), pts, 2)"]))
        else:
            branches.append(('elif ch == "^":',
                             ["pygame.draw.polygon(scr, LOOK[ch], [box.bottomleft, (box.centerx, box.top), box.bottomright])"]))
    if n >= 22:
        branches.append(('elif ch == "W":', ["pygame.draw.rect(scr, (160, 80, 220), box.inflate(-8, 0))"]))
    if n >= 20:
        if n >= 30:
            branches.append(('elif ch in "G!":',
                             ['pygame.draw.rect(scr, TRUTH["!"] if seen and ch == "!" else (90, 230, 190), box.inflate(-6, -2))']))
        else:
            branches.append(('elif ch == "G":', ["pygame.draw.rect(scr, (90, 230, 190), box.inflate(-6, -2))"]))
    if n >= 28:
        branches.append(('elif ch == "~":',
                         ["if seen:",
                          '    pygame.draw.rect(scr, TRUTH["~"], box)',
                          '    pygame.draw.rect(scr, edge(TRUTH["~"]), box, 1)']))

    brick = (["col = TRUTH[ch] if lie else LOOK[ch]",
              "pygame.draw.rect(scr, col, box)",
              "pygame.draw.rect(scr, edge(col) if lie else (0, 0, 0), box, 2 if lie else 1)"]
             if n >= 25 else
             ["pygame.draw.rect(scr, LOOK[ch], box)",
              "pygame.draw.rect(scr, (0, 0, 0), box, 1)"])
    if n >= 29:
        brick += ['if ch == "c":',
                  "    pygame.draw.line(scr, (90, 60, 40), box.topleft, box.center, 1)"]
    branches.append(("else:" if branches else None, brick))

    for head, lines in branches:
        if head:
            out.append("            " + head)
            out += ["                " + l for l in lines]
        else:
            out += ["            " + l for l in lines]

    if n >= 24:
        out.append("    for pb in pebbles:")
        out.append("        pygame.draw.circle(scr, (230, 230, 230), (int(pb[0])%s, int(pb[1])), 3)" % cam)

    if n >= 19:
        out.append('    pygame.draw.rect(scr, (240, 235, 220), (int(P["x"]) - cam, int(P["y"]), PW, PH), border_radius=4)')
    elif n >= 13:
        out.append('    you = (120, 240, 190) if P["g"] else (240, 235, 220)   # green while you are on the ground')
        out.append('    pygame.draw.rect(scr, you, (int(P["x"]), int(P["y"]), PW, PH), border_radius=4)')
    else:
        out.append('    pygame.draw.rect(scr, (240, 235, 220), (int(P["x"]), int(P["y"]), PW, PH), border_radius=4)')

    if n >= 36:
        out += ["", "    if cursed or warp > 0:", "        gusts(scr)", "        wobble(scr, 3.2 + warp * 1.8)"]
    if n >= 34:
        if n >= 35:
            out += ["    w = wind()",
                    '    blow = ("  wind " + ("<<<" if w < 0 else ">>>")) if abs(w) > 0.012 else ""',
                    '    hud = "%s   %s   coins %d   total %s%s" % (NAMES[level], clock_str(frames), coins, clock_str(total), blow)']
        else:
            out.append('    hud = "%s   %s   coins %d   total %s" % (NAMES[level], clock_str(frames), coins, clock_str(total))')
        out += ["    scr.blit(font.render(hud, True, (255, 255, 255)), (10, 10))",
                '    tip = "YOU MADE IT OUT \u2014 R to run it again" if won else (',
                '        "" if cursed else "click to throw a pebble \u2014 it tells you what a tile really is")',
                "    if frames < 140 and not won:",
                "        tip = NAMES[level]",
                "    if tip:",
                "        t = big.render(tip, True, (255, 255, 255))",
                "        scr.blit(t, t.get_rect(center=(VW // 2, 90)))"]
    elif n >= 20:
        out.append('    scr.blit(font.render("coins %d" % coins, True, (255, 255, 255)), (10, 10))')
    return "\n".join(out)


def emit_gusts(n):
    if n < 36:
        return None
    return '''def gusts(scr):
    """Streaks so the wind is visible before it throws your jump off."""
    w = wind()
    if abs(w) < 0.012:
        return
    ln = int(abs(w) * 90) + 6
    for i in range(26):
        y = (i * 131) % VH
        x = int(i * 217 + frames * w * 26) % (VW + 200) - 100
        pygame.draw.line(scr, (58, 58, 82), (x, y), (x + (ln if w > 0 else -ln), y), 1)


def wobble(scr, amt):
    """The curse warping what you see. Shifts bands, never the truth."""
    src = scr.copy()
    for y in range(0, VH, 5):
        dx = int(math.sin(frames / 11.0 + y / 26.0) * amt + math.sin(frames / 3.7 + y / 9.0) * amt * 0.35)
        scr.blit(src, (dx, y), (0, y, VW, 5))
    if amt > 8:                                   # heavy burst: the world tears
        ghost = src.copy(); ghost.set_alpha(110)
        scr.blit(ghost, (int(math.sin(frames / 5.0) * amt * 1.4), int(math.cos(frames / 6.0) * 3)))'''


def emit_main(n):
    out = ["def main():", "    pygame.init()",
           "    scr = pygame.display.set_mode((VW, VH))",
           '    pygame.display.set_caption("Trust No One")']
    if n >= 34:
        out.append("    font, big = pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 30)")
    elif n >= 20:
        out.append("    font = pygame.font.SysFont(None, 24)")
    out.append("    clk = pygame.time.Clock()")
    if n >= 22:
        out.append("    reset()")
    elif n >= 5:
        out.append("    load()")
    out.append("    while True:")
    if n >= 14:
        out.append("        pressed = False")
    out += ["        for e in pygame.event.get():",
            "            if e.type == pygame.QUIT:",
            "                return"]
    if n >= 14:
        out += ["            if e.type == pygame.KEYDOWN:",
                "                if e.key == pygame.K_r: %s" % ("reset()" if n >= 22 else "load()"),
                "                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True"]
    if n >= 24:
        out.append("            if e.type == pygame.MOUSEBUTTONDOWN%s:" % (" and not won" if n >= 34 else ""))
        out.append('                cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))')
        out.append("                throw(e.pos[0] + cam, e.pos[1])")
    if n >= 3:
        out.append("        k = pygame.key.get_pressed()")
        if n >= 14:
            call = ["step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,",
                    "     k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])"]
        else:
            call = ["step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d])"]
        if n >= 34:
            out.append("        if not won:")
            out.append("            " + call[0])
            if len(call) > 1:
                out.append("                 " + call[1].strip())
            out.append("            pebble_step()")
        else:
            out.append("        " + call[0])
            if len(call) > 1:
                out.append("             " + call[1].strip())
            if n >= 24:
                out.append("        pebble_step()")
    if n >= 34:
        out.append("        draw(scr, font, big)")
    elif n >= 20:
        out.append("        draw(scr, font)")
    elif n >= 6:
        out.append("        draw(scr)")
    else:
        out.append("        scr.fill((25, 25, 35))")
        if n >= 2:
            out.append('        pygame.draw.rect(scr, (240, 235, 220), (P["x"], P["y"], PW, PH), border_radius=4)')
    out += ["        pygame.display.flip()", "        clk.tick(60)"]
    return "\n".join(out)


TEST = '''def test():
    """python3 steps/stepNN.py --test  -- plays the game with no window and checks the answers."""
    global LVL, COLS, ROWS, SPAWN, cursed
    reset()
    for _ in range(60): step(0, 1)
    assert P["x"] > SPAWN[0] + 100 and cursed, "walk right, meet the wizard"

    P.update(x=11.0 * TILE + 6, y=16.0 * TILE, vx=0.0, vy=0.0)   # L1's pit of spikes-that-spring
    assert min((step(0, 0) or P["y"]) for _ in range(80)) < 13 * TILE, "spike-trampoline launches"

    # short hop vs held jump
    load(0); held = min((step(0, 0, i == 0, True) or P["y"]) for i in range(80))
    load(0); tap = min((step(0, 0, i == 0, False) or P["y"]) for i in range(80))
    assert tap > held + 20, ("tapping must hop lower than holding", tap, held)

    # synthetic slab: hologram, invisible floor, crumbling brick, fake exit
    LVL = [" " * 10] * 17 + ["      !   ", "~~~~cc##%%", "##########"]
    COLS, ROWS, SPAWN = 10, 20, (8, 17 * TILE)
    cursed = False
    P.update(x=8.0 * TILE + 4, y=17.0 * TILE, vx=0.0, vy=0.0)
    for _ in range(30): step(0, 0)
    assert P["g"], "fake brick holds you up before the curse"
    cursed = True
    for _ in range(20): step(0, 0)
    assert not P["g"] or P["y"] > 18 * TILE, "hologram drops you once cursed"
    die()
    for _ in range(40): step(0, 0)
    assert P["g"] and P["y"] + PH <= 18 * TILE + 1, "invisible floor is still a floor"

    P.update(x=4.0 * TILE + 4, y=17.0 * TILE, vx=0.0, vy=0.0)
    for _ in range(CRUMB + 30): step(0, 0)
    assert (4, 18) in gone, "standing on a crumbling brick breaks it"

    P.update(x=6.0 * TILE + 4, y=17.0 * TILE, vx=0.0, vy=0.0)
    step(0, 0)
    assert P["x"] == SPAWN[0], "the fake exit warps you back to the start"
    load(0); throw(P["x"] + 40, P["y"]); near = abs(pebbles[-1][2])
    throw(P["x"] + 600, P["y"]); far = abs(pebbles[-1][2])
    assert far > near + 3, ("throw strength must follow click distance", near, far)

    load(4); cursed = True                       # windy level: standing still still drifts
    P.update(x=200.0, y=float(SPAWN[1]), vx=0.0, vy=0.0)
    x0 = P["x"]
    for _ in range(90): step(0, 0)
    assert abs(P["x"] - x0) > 1.0, "wind must push the player"
    # no roll of the dice may leave an uncrossable hole
    for sd in range(12):
        globals()["seed"] = sd
        for i in range(len(LEVELS)):
            load(i)
            holes, run = 0, 0
            for c in range(COLS):
                run = run + 1 if all(tile(c, r) == " " for r in (17, 18, 19)) else 0
                holes = max(holes, run)
            assert holes <= 5, ("uncrossable hole", i, sd, holes)
    globals()["seed"] = 0
    print("ok")'''.replace("stepNN", "step%02d" % LAST)


def real_levels():
    """L2..L5 and their names, written out as full-width rows."""
    out = [real_level(name, REAL_LEVELS[name]) for name in ("L2", "L3", "L4", "L5")]
    out.append("LEVELS = [L1, L2, L3, L4, L5]")
    out.append("NAMES = [" + ", ".join('"%s"' % n for n in REAL_NAMES) + "]")
    return "\n".join(out)


def bare(n):
    parts = ['"""Trust No One -- step %d: %s.   Run it:  python3 steps/step%02d.py"""'
             % (n, TITLES[n - 1], n)]
    if n >= 31:
        parts.append("import math, random, sys\nimport pygame")
    elif n >= 29:
        parts.append("import math, sys\nimport pygame")
    else:
        parts.append("import sys\nimport pygame")
    parts.append(emit_consts(n))
    if n >= 5:
        alpha = emit_alphabet(n)
        parts.append((alpha + "\n" + emit_level(n)) if alpha else emit_level(n))
    if n >= 33:
        parts.append(real_levels())
    for piece in (emit_liars(n), emit_globals(n), emit_roll(n), emit_load(n), emit_reset(n),
                  emit_die(n), emit_wind(n), emit_tile(n), emit_solid(n), emit_prect(n),
                  emit_cells(n), emit_step(n), emit_pebble(n), emit_palette(n), emit_edge(n),
                  emit_clock(n), emit_draw(n), emit_gusts(n), emit_main(n)):
        if piece:
            parts.append(piece)
    if n == LAST:
        parts.append(TEST)
        parts.append('if __name__ == "__main__":\n'
                     '    (test if "--test" in sys.argv else main)()')
    else:
        parts.append('if __name__ == "__main__":\n    main()')
    return "\n\n".join(parts) + "\n"


# --------------------------------------------------------------- the comments
# A line's explanation is written into the file itself. At the step where the
# line arrives it is spelled out in full, above the line. From the next step on
# it shrinks to a short trailing note, so the new work has room to be explained.

WIDTH = 96                                  # how wide a commented line may get


def note_for(n, line):
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    return NOTES.get("%d:%s" % (n, stripped)) or NOTES.get(stripped)


def shorten(note, room=46):
    """The one-line form: the first whole clause that fits, never a cut-off word."""
    text = note.split(" -- ")[0].split(". ")[0].strip().rstrip(".")
    for cut in (", which", ", so ", ": ", ", and ", ", "):
        if len(text) > room and cut in text:
            text = text.split(cut)[0].strip()
    if len(text) <= room:
        return text
    words, out = text.split(), ""
    for w in words:
        if len(out) + len(w) + 1 > room:
            break
        out += (" " if out else "") + w
    dangling = {"to", "by", "at", "the", "a", "an", "and", "or", "of", "in", "for",
                "with", "you", "it", "is", "as", "on", "that", "this", "than", "so",
                "most", "least", "up", "into", "from", "its"}
    words = out.split()
    while words and words[-1].lower() in dangling:
        words.pop()                             # never end on a dangling word
    return " ".join(words) if len(words) >= 3 else ""


def string_lines(text):
    """Lines inside a multi-line string. Never write a comment into one of those."""
    inside = set()
    try:
        for tok in tokenize.generate_tokens(StringIO(text).readline):
            if tok.type == tokenize.STRING and tok.end[0] > tok.start[0]:
                inside.update(range(tok.start[0] - 1, tok.end[0]))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return inside


def decorate(n):
    """Add this step's comments to the bare program."""
    text = bare(n)
    lines = text.splitlines()
    unsafe = string_lines(text)
    fresh = set()
    if n > 1:
        prev = bare(n - 1).splitlines()
        sm = difflib.SequenceMatcher(None, prev, lines, autojunk=False)
        for tag, _i1, _i2, j1, j2 in sm.get_opcodes():
            if tag in ("insert", "replace"):
                fresh.update(range(j1, j2))
    else:
        fresh = set(range(len(lines)))

    out = []
    for i, line in enumerate(lines):
        note = None if i in unsafe else note_for(n, line)
        if note and i in fresh:
            pad = line[:len(line) - len(line.lstrip())]
            out += [pad + "# " + w for w in textwrap.wrap(note, WIDTH - len(pad) - 2)]
            out.append(line)
        elif note:
            short = shorten(note, min(46, WIDTH - len(line) - 5))
            if short and "#" not in line and len(line) + len(short) + 5 <= WIDTH:
                out.append(line + "   # " + short)
            else:
                out.append(line)
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def differs_from_main(text):
    """The last step must be the real game, allowing for the async loop and docstrings."""
    real = open(os.path.join(HERE, "game.py")).read()

    def shape(src):
        out = {}
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body = [b for b in node.body
                        if not (isinstance(b, ast.Expr) and isinstance(b.value, ast.Constant)
                                and isinstance(b.value.value, str))]
                out[node.name] = ast.dump(ast.Module(body=body, type_ignores=[]))
        return out

    a, b = shape(text), shape(real)
    return [name for name in sorted(set(a) | set(b)) if a.get(name) != b.get(name)]


def main():
    out = os.path.join(HERE, "steps")
    os.makedirs(out, exist_ok=True)
    for old in os.listdir(out):
        if old.startswith("step") and old.endswith(".py"):
            os.remove(os.path.join(out, old))
    for n in range(1, LAST + 1):
        path = os.path.join(out, "step%02d.py" % n)
        with open(path, "w") as f:
            f.write(decorate(n))
        r = subprocess.run([sys.executable, "-m", "py_compile", path], capture_output=True, text=True)
        if r.returncode:
            print("COMPILE FAIL step%02d" % n)
            print(r.stderr)
            return 1
    ok, said = self_test(os.path.join(out, "step%02d.py" % LAST))
    if not ok:
        print("step%d does not pass its own checks:\n%s" % (LAST, said))
        return 1
    print("step%d plays correctly (its own checks all pass)" % LAST)
    print("wrote %d step files" % LAST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
