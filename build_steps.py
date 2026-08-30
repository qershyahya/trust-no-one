"""Generate the fifty-seven runnable step files for Trust No One.

Every step file is a real pygame program: `py steps\\step14.py` opens a window and
plays. The last step, step57.py, is the finished game.

    python3 build_steps.py         # writes steps/step01.py .. steps/step57.py

Each piece of the program is emitted by a small function that knows what that piece
looks like at step n, so no line of the game is written down twice and the steps
cannot drift apart.
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
    "Floors: the up-down pass",          # 10
    "Walls: the sideways pass",          # 11
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
    "You fall before you die",           # 37
    "Sound, out of arithmetic",          # 38
    "A picture instead of a colour",      # 39
    "The rest of the tiles",              # 40
    "Cutting a strip into frames",        # 41
    "Run, jump, fall",                    # 42
    "A rim, so you can be seen",          # 43
    "The sky, and the graveyard",         # 44
    "The truth, as a picture",            # 45
    "Two doors",                          # 46
    "A stone, tumbling",                  # 47
    "A throw that looks like one",        # 48
    "Dust",                               # 49
    "Going down",                         # 50
    "The keys, on the screen",            # 51
    "The wizard, awake",                  # 52
    "He walks up and hits him",           # 53
    "A conversation",                     # 54
    "Levels you can edit",                # 55
    "Sounds from a pack",                 # 56
    "Four bars under all of it",          # 57
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
    (7, 17, 1, "P"),
    (10, 16, 8, "#"), (10, 17, 8, "#"),                # a block: walk through it, then into it
    (12, 18, 4, "  "), (12, 19, 4, "  "),              # and an edge to walk off                                   # where you start
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
        '            x         ##%#               ###&&##',
        '            x                         o             o',
        ' P   W                  ^^^       ^ ??                   G',
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
        '             ##%                   ##&&             ###                    ##',
        '                 x                                        o             x',
        ' P                                                                           G',
        '##########%%##&&####  %%#########%%#####    ######&&##########  %%##############',
        '####################tt^^################    ##################^^tt##############',
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
        '                                           ~o~',
        '               o                           ~~~                 x',
        '                         o            ~~                o',
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
        '                                          ###',
        '            x  o                 x   o               o  x',
        '',
        '',
        ' P                                                                           G',
        '##########ccccc###############cc#cccc#############cccc%ccc  ####################',
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
        '                           &&',
        ' P          ??                                !',
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
    out.append("LEVELS = [L1]                          # the levels, in order: one so far")
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
    """Every constant on its own line, with its final value, from the step it arrives.
    A value is assigned once; a later step only ever adds a line."""
    out = ["VW, VH = 960, 640                     # the window, in pixels"]
    if n >= 5:
        out.append("TILE = 32                             # one square of the world")
    out.append("")
    if n >= 2:
        out.append("PW, PH = 20, 28                       # how big you are")
    if n >= 3:
        out.append("SPD = 3.6                             # top walking speed, pixels per frame")
    if n >= 4:
        out.append("GRAV = 0.35                           # pull per frame")
        out.append("MAXFALL = 12                          # the fastest you may fall")
    if n >= 14:
        out.append("JUMP = -9.2                           # the kick upward, pixels per frame")
    if n >= 15:
        out.append("COYOTE = 7                            # you may still jump 7 frames after the edge")
    if n >= 16:
        out.append("BUFFER = 8                            # a press up to 8 frames early still counts")
    if n >= 17:
        out.append("CUT = 0.42                            # let go early and the jump is cut to this")
    if n >= 18:
        out.append("ACC, AIR, FRIC = 0.55, 0.32, 0.72     # how fast you gain speed, on the ground and off it, and lose it")
    if n >= 26:
        out.append("BOUNCE = -12.3                        # a trampoline: stronger than JUMP")
    if n >= 29:
        out.append("CRACK, AWAY = 18, 30                  # a cracked brick wobbles, drops, comes back")
    if n >= 35:
        out.append("GUST = [0.0, 0.0, 0.20, 0.25, 0.30]   # how hard the wind blows, level by level")
        out.append("SWING = [1.0, 1.0, 1.0, 1.5, 2.2]     # and how fast it turns around")
    if n >= 12:
        out.append("LIVES = 5                             # how many you start with")
    if n >= 37:
        out.append("FALL = 60                             # frames your body takes to come to rest")
    if n >= 25:
        out.append("SHOWN = 30                            # frames a struck square tells the truth")
    if n >= 24:
        out.append("CLEAR = 6                             # frames a stone ignores what it is inside")
    if n >= 48:
        out.append("THROW = 16                            # frames the throwing animation lasts")
    if n >= 52:
        out.append("HIT_FOR, CURSE = 16, 40               # he flinches for one, casts for the other")
    return "\n".join(out).strip("\n")


def emit_globals(n):
    """The game's state, one line per name, from the step each is first needed."""
    out = []
    if n >= 5:
        out.append("LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured")
        out.append("level = 0                                             # which level is loaded")
    if n >= 31:
        out.append("seed = 0                                              # this run's dice")
    if n >= 2:
        out.append("SPAWN = (64, 288)                                     # where you start" if n < 7 else
                   "SPAWN = (0, 0)                                        # where you start, found by load()")
        out.append("P = {}                                                # where you are, and how fast")
    if n >= 22:
        out.append("cursed = False")
        out.append("wizard = True")
    if n >= 33:
        out.append("won = False")
    if n >= 20:
        out.append("coins = 0")
    if n >= 29:
        out.append("frames = 0                                            # this level's clock")
    if n >= 15:
        out.append("coy = 0")
    if n >= 16:
        out.append("buf = 0")
    if n >= 36:
        out.append("warp = 0.0")
        out.append("blown = 0.0                                           # how far the air has travelled")
    if n >= 12:
        out.append("lives = LIVES")
        out.append("over = False                                          # the run is finished")
    if n >= 37:
        out.append("dying, body = 0, [0.0, 0.0, 0.0]")
    if n >= 40:
        out.append("beat = 0                                              # the pictures' own clock")
    if n >= 41:
        out.append("face = 1                                              # 1 right, -1 left")
    if n >= 48:
        out.append("throwing = 0")
    if n >= 52:
        out.append("flash = casting = 0")
    for name, init, since in (("COIN", "[]", 40), ("PLAYER", "{}", 41), ("SKY", "[]", 44),
                              ("TRUE", "{}", 45), ("FIRE", "[]", 45), ("DOOR_OK", "[]", 46),
                              ("DOOR_BAD", "[]", 46), ("DEMON", "[]", 46), ("SHOT", "[]", 47),
                              ("SMOKE", "[]", 49), ("PUFFS", "[]", 49), ("KEYS", "{}", 51),
                              ("WIZ, WIZ_L", "[], []", 52), ("HURT, HURT_L", "[], []", 52),
                              ("CAST, CAST_L", "[], []", 52)):
        if n >= since:
            out.append("%s = %s" % (name, init))
    for name, init, since in (("taken", "set()", 20), ("pebbles", "[]", 24), ("hit", "{}", 25),
                              ("gone", "set()", 29), ("crack", "{}", 29)):
        if n >= since:
            out.append("%s = %s" % (name, init))
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
    """load(i) from the day the level exists: the first level is level 0 of a list of one."""
    if n < 5:
        return None
    out = ["def load(i):",
           '    """Take level i, measure it, find where you start, and stand there."""',
           "    global LVL, COLS, ROWS, level" + (", SPAWN" if n >= 7 else "") + (", frames" if n >= 29 else ""),
           "    level = i"]
    if n >= 29:
        out.append("    frames = 0")
    out.append("    rows = LEVELS[i]")
    out.append("    COLS = max(len(r) for r in rows)")
    if n >= 31:
        out.append("    rng = random.Random(seed * 977 + i)")
        out.append("    LVL = [roll(r.ljust(COLS), rng) for r in rows]")
    else:
        out.append("    LVL = [r.ljust(COLS) for r in rows]")
    out.append("    ROWS = len(LVL)")
    if n >= 7:
        out.append('    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")')
        out.append('    LVL = [r.replace("P", " ") for r in LVL]')
    for name, since in (("taken", 20), ("pebbles", 24), ("hit", 25), ("gone", 29), ("crack", 29)):
        if n >= since:
            out.append("    %s.clear()" % name)
    out.append("    place()")
    return "\n".join(out)


def emit_reset(n):
    """A whole fresh run. Exists from the first P, and only ever gains a line."""
    if n < 2:
        return None
    names = ["lives", "over"] if n >= 12 else []
    if n >= 22:
        names = ["cursed", "wizard"] + names
    if n >= 20:
        names.append("coins")
    if n >= 31:
        names.append("seed")
    if n >= 33:
        names.append("won")
    if n >= 53:
        names += ["scene", "flash", "casting", "throwing"]
    if n >= 54:
        names.append("said")
    out = ["def reset():", '    """A whole fresh run: everything back to the beginning."""']
    if names:
        out.append("    global " + ", ".join(names))
    if n >= 31:
        out.append("    seed = random.randrange(1 << 30)")
    if n >= 22:
        out.append("    cursed = False")
        out.append("    wizard = True")
    if n >= 33:
        out.append("    won = False")
    if n >= 20:
        out.append("    coins = 0")
    if n >= 12:
        out.append("    lives = LIVES")
        out.append("    over = False")
    if n >= 53:
        out.append('    scene = "title"                             # a fresh run starts with the story:')
        out.append("    flash = casting = throwing = 0              # you are never here uncursed")
    if n >= 54:
        out.append("    said = 0")
    out.append("    load(0)" if n >= 5 else "    place()")
    return "\n".join(out)


def emit_die(n):
    """place() from the moment there is a P; die() from the first way to die."""
    if n < 2:
        return None
    out = ["def place():", '    """At the start of the level, standing still."""',
           "    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)"]
    if n >= 13:
        out.append('    P["g"] = False')
    if n >= 14:
        out.append('    P["jump"] = False')
    if n < 12:
        return "\n".join(out)
    glob = ["lives", "over"] + (["warp"] if n >= 36 else []) + (["dying"] if n >= 37 else [])
    die = ["", "", "def die():", '    """Being killed. It costs a life, and the last one ends the run."""',
           "    global " + ", ".join(glob)]
    if n >= 36:
        die.append("    warp = max(warp, 6.0)")
    die.append("    lives -= 1")
    if n >= 38:
        die.append('    beep("die")')
    die += ["    if lives <= 0:", "        over = True"]
    if n >= 38:
        die.append('        beep("gameover")')
    die.append("        return place()")
    if n >= 37:
        die += ['    body[0], body[1], body[2] = P["x"], P["y"], P["vy"]', "    dying = FALL"]
    else:
        die.append("    place()")
    out += die
    if n >= 37:
        out += ["", "", '''def fall():
    """Your body drops from wherever it was hit and comes to rest on the first thing
    that will hold it: ground, spikes, a trampoline. Then you are put back."""
    global dying
    dying -= 1
    body[2] = min(body[2] + GRAV, MAXFALL)
    body[1] += body[2]
    r = pygame.Rect(int(body[0]), int(body[1]), PW, PH)
    for _, rw, ch in cells(r):
        if solid(ch) or ch in "^t":
            r.bottom = rw * TILE
            body[1], body[2] = float(r.y), 0.0
    if body[1] > ROWS * TILE:
        dying = 0                                 # out of the world: nothing left to watch
    if dying <= 0:
        place()''']
    return "\n".join(out)


def emit_wind(n):
    if n < 35:
        return None
    return ("def wind():\n"
            '    """How hard it is blowing right now, and which way: sin() swings it."""\n'
            "    if not cursed:\n"
            "        return 0.0\n"
            "    return GUST[level] * math.sin(frames * SWING[level] / 110.0)")


def emit_tile(n):
    if n < 5:
        return None
    return ('def tile(c, r):\n'
            '    """What letter is at column c, row r? Off the map counts as empty air."""\n'
            '    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "')


def emit_solid(n):
    if n < 10:
        return None
    body = 'return ch in "#~c" or (ch == "%" and not cursed)' if n >= 23 else 'return ch in "#~c"'
    return ('def solid(ch):\n'
            '    """Which letters stop you. Floor you cannot see and bricks that crumble are floor;\n'
            '    a hologram is floor only until you are cursed."""\n'
            '    ' + body)


def emit_prect(n):
    if n < 8:
        return None
    return ('def prect():\n'
            '    """Your box, right now."""\n'
            '    return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)')


def emit_cells(n):
    if n < 9:
        return None
    test = 'if ch != " " and (c, r) not in gone:' if n >= 29 else 'if ch != " ":'
    return ('def cells(rect):\n'
            '    """Every tile this box overlaps -- usually two to six of them."""\n'
            '    for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):\n'
            '        for c in range(rect.left // TILE, (rect.right - 1) // TILE + 1):\n'
            '            ch = tile(c, r)\n'
            '            %s\n'
            '                yield c, r, ch') % test


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
    if n >= 15:
        glob.append("coy")
    if n >= 16:
        glob.append("buf")
    if n >= 36:
        glob.append("warp")
    if n >= 42:
        glob.append("face")
    if n >= 48:
        glob.append("throwing")
    if glob:
        body.append("    global " + ", ".join(glob))
    if n >= 36:
        body.append("    warp = max(0.0, warp - 0.16)                  # every jolt fades, even on the game over screen")
    if n >= 12:
        body.append("    if over: return                               # the run is finished")
    if n >= 33:
        body.append("    if won: return                                # and so is the game")
    if n >= 37:
        body += ["    if dying:                                     # you are on your way down",
                 "        return fall()"]
    if n >= 29:
        body.append("    frames += 1")
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
    if n >= 42:
        body += ['    if P["vx"] > 0.4: face = 1                    # you face the way you move',
                 '    elif P["vx"] < -0.4: face = -1']
    if n >= 48:
        body.append("    if throwing: throwing -= 1")

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
        if n >= 38:
            body.append('        beep("jump")')
        if n >= 17:
            tail = " -- never cuts a trampoline" if n >= 26 else ""
            body += ['    if P["jump"] and not held and P["vy"] < JUMP * CUT:',
                     '        P["vy"], P["jump"] = JUMP * CUT, False    # let go early, hop short' + tail,
                     '    if P["vy"] >= 0:',
                     '        P["jump"] = False']

    if n >= 4:
        body.append('    P["vy"] = min(P["vy"] + GRAV, MAXFALL)')
    body.append("")

    if n >= 11:
        body += ['    P["x"] += P["vx"]',
                 "    r = prect()",
                 "    for c, _, ch in cells(r):",
                 "        if solid(ch):",
                 '            if P["vx"] > 0: r.right = c * TILE',
                 '            elif P["vx"] < 0: r.left = (c + 1) * TILE',
                 '            P["x"] = float(r.x); P["vx"] = 0.0',
                 '    P["x"] = min(max(P["x"], 0.0), COLS * TILE - PW)']
    else:
        body.append('    P["x"] += P["vx"]')
    if n >= 10:
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
                 "    for cell in list(crack):                      # every cracked brick has a clock",
                 "        crack[cell] += 1",
                 "        if crack[cell] == CRACK:",
                 "            gone.add(cell)                        # the warning is over: it drops"]
        if n >= 38:
            body.append('            beep("fall")')
        body += ["        elif crack[cell] >= CRACK + AWAY:",
                 "            if prect().colliderect(pygame.Rect(cell[0] * TILE, cell[1] * TILE, TILE, TILE)):",
                 "                crack[cell] = CRACK + AWAY        # you are standing in its way: wait",
                 "            else:",
                 "                del crack[cell]; gone.discard(cell)",
                 '    if P["g"]:                                    # a brick you stand on starts its clock',
                 "        for c, rw, ch in cells(prect().move(0, 1)):",
                 '            if ch == "c" and (c, rw) not in crack:',
                 "                crack[(c, rw)] = 0"]

    if n >= 12:
        body += ["", '    if P["y"] > ROWS * TILE:', "        return die()"]

    if n >= 20:
        body.append("    for c, rw, ch in cells(prect()):")
        if n >= 21:
            body += ['        if ch == "^":', "            return die()"]
        if n >= 26:
            body += ['        if ch == "t" and not cursed:', "            return die()",
                     '        if ch == "t" and cursed:                  # the spikes that spring',
                     '            P["vy"], P["g"], P["jump"] = BOUNCE, False, False']
            if n >= 38:
                body.append('            beep("bounce")')
        if n >= 27:
            body += ['        if ch == "x" and cursed:', "            return die()"]
        if n >= 30:
            body += ['        if ch == "!":']
            if n >= 36:
                body.append("            warp = 22.0")
            body.append("            return die()")
        body += ['        if ch == "o" and (c, rw) not in taken:', "            taken.add((c, rw)); coins += 1"]
        if n >= 38:
            body.append('            beep("coin")')
        if n >= 27:
            body += ['        if ch == "x" and (c, rw) not in taken:   # the killer coin still counts',
                     "            taken.add((c, rw)); coins += 1"]
            if n >= 38:
                body.append('            beep("coin")')
        if n >= 22:
            body.append('        if ch == "W" and wizard:')
            body.append("            wizard, cursed = False, True")
            if n >= 36:
                body.append("            warp = 26.0                           # the biggest jolt in the game")
        if n >= 33:
            body += ['        if ch == "G":',
                     "            if level + 1 < len(LEVELS):"]
            if n >= 38:
                body.append('                beep("level")')
            body += ["                return load(level + 1)",
                     "            won = True"]
            if n >= 38:
                body.append('            beep("win")')

    text = sig + "\n" + "\n".join(body)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.rstrip()


def emit_pebble(n):
    """The stone, in its final form from the day it exists: it clears your own feet, it flies
    through where the wizard stood, and from the next step it wakes squares for a while."""
    if n < 24:
        return None
    fade = ("    for cell in list(hit):                        # the truth fades on its own\n"
            "        hit[cell] -= 1\n"
            "        if hit[cell] <= 0:\n"
            "            del hit[cell]\n") if n >= 25 else ""
    hit_test = ('if ch != " " and (c, r) not in gone and (c, r) not in taken:' if n >= 29
                else 'if ch != " " and (c, r) not in taken:')
    reveal = ("            for i in (-1, 0, 1):\n"
              "                for j in (-1, 0, 1):\n"
              "                    hit[(c + i, r + j)] = SHOWN\n") if n >= 25 else ""
    if n >= 38:
        reveal += '            beep("knock")\n'
    if n >= 49:
        reveal += "            puff(pb[0], pb[1] + 6)               # dust off whatever it struck\n"
    aim = ('    global face, throwing\n'
           '    face = 1 if tx > P["x"] + PW / 2 else -1\n'
           '    throwing = THROW\n') if n >= 48 else ""
    if n >= 38:
        aim += '    beep("throw")\n'
    return ('def throw(tx, ty):\n'
            '    """Click far away for a hard throw, close for a soft lob."""\n'
            '%s'
            '    cx, cy = P["x"] + PW / 2, P["y"] + PH / 2\n'
            '    dx, dy = tx - cx, ty - cy\n'
            '    d = max(1.0, (dx * dx + dy * dy) ** 0.5)\n'
            '    sp = max(4.5, min(16.0, d / 20.0))        # close click = soft lob, far click = hard throw\n'
            '    pebbles.append([cx, cy, dx / d * sp, dy / d * sp, 0])   # the last number is its age\n'
            '\n'
            '\n'
            'def pebble_step():\n'
            '    """One frame for every stone in the air."""\n'
            '%s'
            '    for pb in pebbles[:]:\n'
            '        pb[3] += GRAV * 0.5\n'
            '%s'
            '        pb[0] += pb[2]; pb[1] += pb[3]\n'
            '        pb[4] += 1\n'
            '        c, r = int(pb[0]) // TILE, int(pb[1]) // TILE\n'
            '        if not (0 <= c < COLS and 0 <= r < ROWS):\n'
            '            pebbles.remove(pb); continue\n'
            '        ch = tile(c, r)\n'
            '        if ch == "W" and not wizard:              # he has gone: his square is air\n'
            '            continue\n'
            '        if pb[4] < CLEAR:                         # still leaving your hand\n'
            '            continue\n'
            '        %s\n'
            '%s'
            '            pebbles.remove(pb)') % (aim, fade, "        pb[2] += wind() * 1.6\n" if n >= 35 else "",
                                                 hit_test, reveal)


def emit_palette(n):
    """The colours of the shape-drawn world. Assigned once, with every letter the game will
    ever have -- and gone the day pictures replace them."""
    if n < 6 or n >= 40:
        return None
    return ('LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "c": (150, 110, 70),\n'
            '        "^": (170, 170, 180), "t": (170, 170, 180), "o": (240, 200, 60), "x": (240, 200, 60)}')


def emit_truth(n):
    if n < 25 or n >= 46:
        return None
    return ('# ponytail: a revealed lie keeps its own hue and goes darker/duller -- readable, never neon\n'
            'TRUTH = {"%": (108, 84, 66), "t": (146, 162, 148), "x": (206, 168, 96),\n'
            '         "~": (50, 50, 66), "c": (126, 92, 58), "!": (66, 178, 158)}')


def emit_liars(n):
    if n < 23:
        return None
    return 'LIARS = set("%tx~c!")                 # every letter that lies, including the ones you have not met yet'


def emit_edge(n):
    return None if n < 25 or n >= 46 else "def edge(col):\n    return tuple(max(0, v - 40) for v in col)"


def emit_shaken(n):
    if n < 25:
        return None
    return ('def shaken(n):\n'
            '    """How far a struck square is knocked sideways: a wobble that dies down."""\n'
            '    return int(math.sin(n * 0.9) * n / 6)')


def emit_heart(n):
    if n < 20:
        return None
    return ('''def heart(scr, x, y, full):
    """A small heart: two lobes and a point. Cheaper than a picture, and it never
    goes missing."""
    col = (222, 70, 90) if full else (70, 60, 66)
    pygame.draw.circle(scr, col, (x + 4, y + 4), 4)
    pygame.draw.circle(scr, col, (x + 11, y + 4), 4)
    pygame.draw.polygon(scr, col, [(x, y + 5), (x + 15, y + 5), (x + 7, y + 15)])''')


def emit_art(n):
    """The pictures: where they live, how to open one, and how to cut a strip up."""
    if n < 39:
        return None
    out = ['ART = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art")',
           "PIC = {}",
           "",
           "",
           "def picture(name):",
           '    """Open a picture. convert_alpha() re-packs it the way the screen wants,',
           '    which makes every later blit far quicker."""',
           "    return pygame.image.load(os.path.join(ART, name)).convert_alpha()"]
    if n >= 41:
        out += ["", "",
                "def cut(sheet, n):",
                '    """A strip of n frames, side by side, cut into a list. Each frame is trimmed',
                '    down to the pixels that are actually drawn, so a 150-wide frame with a small',
                '    character in it stops being mostly empty air."""',
                "    wide, out = sheet.get_width() // n, []",
                "    for i in range(n):",
                "        frame = sheet.subsurface((i * wide, 0, wide, sheet.get_height()))",
                "        box = frame.get_bounding_rect()",
                "        out.append(frame.subsurface(box).copy() if box.width else frame.copy())",
                "    return out"]
    if n >= 43:
        out += ["", "",
                "def rimmed(pic, colour=(226, 236, 255)):",
                '    """A one-pixel rim around a sprite. She is dark olive, the graveyard is nearly',
                '    black, and without this she disappears into it. from_surface() makes a mask --',
                '    which pixels are drawn at all -- and to_surface() paints that shape one colour."""',
                "    w, h = pic.get_size()",
                "    out = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)",
                "    edge = pygame.mask.from_surface(pic).to_surface(setcolor=colour,",
                "                                                    unsetcolor=(0, 0, 0, 0))",
                "    for dx, dy in ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)):",
                "        out.blit(edge, (dx, dy))    # the shape, eight times, one pixel out each way",
                "    out.blit(pic, (1, 1))           # then the sprite itself, on top",
                "    return out"]
    if n >= 41:
        out += ["", "",
                "def facing(frames):",
                '    """Every frame, ready to face either way. Built once at the start rather than',
                '    flipped every frame -- flipping is slow, and a game does this sixty times a',
                '    second."""',
                "    return [{1: %s, -1: %s}" % (("rimmed(f)", "rimmed(pygame.transform.flip(f, True, False))")
                                                if n >= 43 else ("f", "pygame.transform.flip(f, True, False)")),
                "            for f in frames]"]
    return "\n".join(out)


def emit_art_helpers(n):
    if n < 45:
        return None
    out = ['def tall(pic, height):',
           '    """Scale a picture to a given height, keeping its shape."""',
           "    k = height / pic.get_height()",
           "    return pygame.transform.scale(pic, (max(1, int(pic.get_width() * k)), height))",
           "", "",
           "def fit(pic):",
           '    """Trim a picture, scale it to fit one square, and stand it on the floor of that',
           '    square -- so a slime sits on the ground instead of floating in the middle."""',
           "    box = pic.get_bounding_rect()",
           "    pic = pic.subsurface(box).copy() if box.width else pic",
           "    k = min(TILE / pic.get_width(), TILE / pic.get_height())",
           "    pic = pygame.transform.scale(pic, (max(1, int(pic.get_width() * k)),",
           "                                       max(1, int(pic.get_height() * k))))",
           "    out = pygame.Surface((TILE, TILE), pygame.SRCALPHA)",
           "    out.blit(pic, ((TILE - pic.get_width()) // 2, TILE - pic.get_height()))",
           "    return out"]
    if n >= 48:
        out += ["", "",
                "SWOOSH = {(240, 240, 240), (214, 221, 225)}    # the two colours of the sword arc",
                "", "",
                "def de_swoosh(frames):",
                '    """Her throw frame carries a big white arc that reads as a sword sweep, not a',
                '    throw. Every other frame has about forty near-white pixels; that one has over a',
                '    thousand. So: count them, and if there are too many, rub that colour out."""',
                "    out = []",
                "    for frame in frames:",
                "        frame = frame.copy()",
                "        white = sum(1 for y in range(frame.get_height())",
                "                    for x in range(frame.get_width())",
                "                    if frame.get_at((x, y)).a and frame.get_at((x, y))[:3] in SWOOSH)",
                "        if white > 200:",
                "            for y in range(frame.get_height()):",
                "                for x in range(frame.get_width()):",
                "                    if frame.get_at((x, y)).a and frame.get_at((x, y))[:3] in SWOOSH:",
                "                        frame.set_at((x, y), (0, 0, 0, 0))",
                "            box = frame.get_bounding_rect()",
                "            frame = frame.subsurface(box).copy() if box.width else frame",
                "        out.append(frame)",
                "    return out"]
    if n >= 49:
        out += ["", "",
                "def puff(x, y):",
                '    """A plume of smoke, at a point in the world."""',
                "    PUFFS.append([x, y, 0])",
                "", "",
                "def smoke(scr, cam):",
                '    """Draw every plume and age it. They drift up and are gone in half a second."""',
                "    for p in PUFFS[:]:",
                "        p[2] += 1",
                "        i = p[2] // 4",
                "        if i >= len(SMOKE):",
                "            PUFFS.remove(p)",
                "            continue",
                "        pic = SMOKE[i]",
                "        scr.blit(pic, (int(p[0]) - cam - pic.get_width() // 2,",
                "                       int(p[1]) - pic.get_height() - p[2] // 3))"]
    return "\n".join(out)


def emit_build_art(n):
    """One function that opens every picture the game needs, called once from main()."""
    if n < 39:
        return None
    out = ["def art():", '    """Every picture, opened once. Doing this inside draw() would open the same',
           '    files sixty times a second."""',
           "    sheet = picture(\"tiles.png\")",
           "    cell = lambda c, r: sheet.subsurface((c * TILE, r * TILE, TILE, TILE)).copy()",
           '    PIC["#"] = cell(5, 1)                          # the ground: one 32x32 square of it']
    if n >= 40:
        out += ['    PIC["%"] = PIC["~"] = cell(5, 1)               # a lie has to look like the truth',
                '    PIC["c"] = cell(2, 1)',
                "    spike = picture(\"spikes.png\").subsurface((0, 0, 16, 16))",
                "    bed = pygame.Surface((TILE, TILE), pygame.SRCALPHA)",
                "    bed.blit(spike, (0, TILE - 16)); bed.blit(spike, (16, TILE - 16))",
                '    PIC["^"] = PIC["t"] = bed                      # two 16-pixel spikes fill a square',
                "    coin = picture(\"coin_gold.png\")",
                '    COIN[:] = [pygame.transform.scale(coin.subsurface((i * 16, 0, 16, 16)), (TILE, TILE))',
                "               for i in range(coin.get_width() // 16)]"]
    if n >= 41:
        out += ["", '    PLAYER["idle"] = facing(cut(picture("player_idle.png"), 8))']
    if n >= 42:
        out += ['    PLAYER["run"] = facing(cut(picture("player_run.png"), 8))',
                '    PLAYER["jump"] = facing(cut(picture("player_jump.png"), 2))',
                '    PLAYER["fall"] = facing(cut(picture("player_fall.png"), 2))']
    if n >= 44:
        out += ["", '    SKY.append(picture("sky.png"))                    # far away, and slow',
                '    SKY.append(picture("graveyard.png"))              # nearer, and twice as fast']
    if n >= 45:
        out += ["", "    # what each liar really is. No colour code to learn: you see the thing itself",
                '    TRUE["%"] = cell(8, 8)                         # a hole. There was never a brick',
                '    TRUE["c"] = cell(7, 8)                         # loose rubble',
                '    TRUE["~"] = cell(3, 8)                         # a stone ledge, holding you up',
                '    TRUE["t"] = fit(picture("slime.png").subsurface((0, 0, 24, 24)))',
                '    FIRE[:] = [fit(picture("fire/%d.png" % i)) for i in range(1, 9)]',
                '    TRUE["x"] = FIRE                               # a coin that is a fire']
    if n >= 46:
        out += ["", '    door = picture("portal.png")',
                "    for i in range(door.get_width() // 128):",
                "        one = tall(door.subsurface((i * 128, 0, 128, 128)), TILE * 2)",
                "        DOOR_BAD.append(one)                       # as it is: red, and a way back",
                "        green = one.copy()",
                "        green.fill((70, 255, 190, 255), special_flags=pygame.BLEND_RGBA_MULT)",
                "        DOOR_OK.append(green)                      # as you see it: a way out",
                '    for f in cut(picture("demon_idle.png"), 6):',
                "        DEMON.append(tall(f, 46))                  # what waits in the wrong door"]
    if n >= 47:
        out += ["", '    stone = picture("rocks.png").subsurface((0, 16, 16, 16))',
                "    box = stone.get_bounding_rect()",
                "    SHOT.append(pygame.transform.scale(stone.subsurface(box),",
                "                                       (max(8, box.width // 2), max(8, box.height // 2))))"]
    if n >= 48:
        out.append('    PLAYER["throw"] = facing(de_swoosh(cut(picture("player_throw.png"), 5)))')
    if n >= 49:
        out.append('    SMOKE[:] = [tall(picture("smoke/%d.png" % i), 34) for i in range(1, 9)]')
    if n >= 50:
        out.append('    PLAYER["death"] = facing(cut(picture("player_death.png"), 8))')
    if n >= 51:
        out += ["", '    keys = picture("keys.png")',
                "    icon = lambda c, r: pygame.transform.scale(",
                "        keys.subsurface((c * 16, r * 16, 16, 16)), (32, 32))",
                '    KEYS["left"], KEYS["right"] = icon(13, 13), icon(13, 15)',
                '    KEYS["space"] = icon(9, 8)',
                '    KEYS["click"] = pygame.transform.scale(',
                '        picture("mouse.png").subsurface((16, 48, 16, 16)), (32, 32))']
    if n >= 52:
        out += ["", "    for sheet_name, count, into, mirror in ((\"wizard_idle.png\", 8, WIZ, WIZ_L),",
                '                                            ("wizard_hurt.png", 4, HURT, HURT_L),',
                '                                            ("wizard_cast.png", 8, CAST, CAST_L)):',
                "        for f in cut(picture(sheet_name), count):",
                "            into.append(f)",
                "            mirror.append(pygame.transform.flip(f, True, False))"]
    if n >= 53:
        out.append('    PLAYER["swing"] = facing(cut(picture("player_swing.png"), 5))')
    return "\n".join(out)


def emit_story(n):
    """The opening: she walks up to him, hits him, and he takes her eyes for it."""
    if n < 53:
        return None
    out = ['OPEN = [                                       # what you read before anything moves',
           '    "Midnight. A graveyard full of coins nobody came back for.",',
           '    "You came to take them. Someone is already standing on them.",',
           "]"]
    if n >= 54:
        out += ["TALK = [                                       # who says it, and what",
                '    ("wiz", "You strike me? For a handful of coins?"),',
                '    ("you", "They were lying on the floor. That makes them mine."),',
                '    ("wiz", "Then take my eyes as well. A fair trade."),',
                '    ("wiz", "From now on, what you see is what I choose."),',
                '    ("wiz", "A brick may be air. A coin may kill you. Spikes may be soft."),',
                '    ("wiz", "Throw a stone at a thing before you step on it. Stone does not lie."),',
                '    ("wiz", "TRUST NO ONE."),',
                "]"]
    out += ['scene, wiz_at = "title", None                  # title -> walk -> hit -> %s' %
            ("talk -> cast -> None" if n >= 54 else "cast -> None")]
    if n >= 54:
        out.append("said = 0                                       # how far through TALK we are")
    out += ["", "",
            "def find_wizard():",
            '    """Which square he is standing in. Read out of the level, not written down."""',
            "    for r, row in enumerate(LVL):",
            '        c = row.find("W")',
            "        if c >= 0:",
            "            return c, r",
            "    return None", "", "",
            "def scene_step():",
            '    """One frame of the opening. You are not driving: her legs run on the game\'s own',
            '    physics, so she walks at exactly the speed you will walk at."""',
            "    global scene, flash, throwing, face, cursed, wizard, warp, casting",
            "    if flash: flash -= 1                           # his flinch, running out",
            "    if casting: casting -= 1                       # and his spell, running out",
            '    if scene == "walk":',
            "        step(0, 1)                                 # hold right, and nothing else",
            "        if P[\"x\"] + PW >= wiz_at[0] * TILE - 12:   # close enough to swing",
            '            scene, throwing, face = "hit", THROW, 1',
            '            P["vx"] = 0.0                          # stop, or she runs on the spot',
            '    elif scene == "hit":',
            "        throwing -= 1",
            "        if throwing == THROW // 2:",
            "            flash = HIT_FOR                        # the moment it lands",
            '            beep("hit")',
            "        elif throwing <= 0:",
            '            scene = "talk"' if n >= 54 else '            scene, casting = "cast", CURSE',
            ]
    out += ['    elif scene == "cast" and casting <= 0:         # the spell has landed',
            "        scene, cursed, wizard, warp = None, True, False, 26.0"]
    out += ["", "",
            "def advance():",
            '    """Space or a click. Only the parts you read wait for you."""',
            "    global scene, wiz_at" + (", said, casting" if n >= 54 else ", casting"),
            '    if scene == "title":',
            "        wiz_at = find_wizard()",
            '        scene = "walk" if wiz_at else None']
    if n >= 54:
        out += ['    elif scene == "talk":',
                "        said += 1",
                '        beep("talk")',
                "        if said >= len(TALK):",
                '            scene, casting = "cast", CURSE          # he raises his hands',
                '            beep("curse")']
    if n >= 54:
        out += ["", "",
                "def bubble(scr, font, text, cx, top, colour):",
                '    """One speech bubble, with a tail pointing down at whoever said it."""',
                "    t = font.render(text, True, (240, 236, 228))",
                "    box = t.get_rect(centerx=cx, top=top).inflate(26, 16)",
                "    box.clamp_ip(pygame.Rect(8, 8, VW - 16, VH - 16))",
                "    pad = pygame.Surface(box.size, pygame.SRCALPHA)",
                "    pad.fill((10, 8, 14, 230))",
                "    scr.blit(pad, box)",
                "    pygame.draw.rect(scr, colour, box, 2, border_radius=9)",
                "    scr.blit(t, t.get_rect(center=box.center))",
                "    tx = max(box.left + 14, min(cx, box.right - 14))",
                "    pygame.draw.polygon(scr, colour, [(tx - 9, box.bottom - 2), (tx + 9, box.bottom - 2),",
                "                                      (tx, box.bottom + 12)])"]
    return "\n".join(out)


def emit_levels_file(n):
    if n < 55:
        return None
    return '''LEVELS_TXT = os.path.join(os.path.dirname(ART), "levels.txt")
LEGEND = [
    "# The five levels, as text. Edit this file and the game plays what you wrote.",
    "#",
    "# A level is everything between the two bars. One character is one square:",
    "#   #  brick      o  coin       ^  spikes      G  the way out    P  where you start",
    "#   %  looks like a brick, is not      x  looks like a coin, kills you",
    "#   t  looks like spikes, bounces      ~  floor you cannot see",
    "#   c  a brick that gives way          !  looks like the way out, is not",
    "#   ?  rolled: spikes or trampoline    &  rolled: brick or hologram",
    "",
]


def dump_levels():
    """Write the game's own levels out, once, so there is something to edit. The bars
    hold the width open -- an editor that trims trailing spaces cannot narrow a level."""
    out = list(LEGEND)
    for name, rows in zip(NAMES, LEVELS):
        out.append("[%s]" % name)
        wide = max(len(r) for r in rows)
        out += ["|%s|" % r.ljust(wide) for r in rows]
        out.append("")
    with open(LEVELS_TXT, "w") as f:
        f.write("\\n".join(out))


def read_levels():
    """A name in [brackets], then its rows, each inside a pair of bars. Anything else in
    the file is yours: comments, blank lines, notes to yourself."""
    names, levels, rows = [], [], None
    for line in open(LEVELS_TXT).read().splitlines():
        if line.startswith("[") and line.rstrip().endswith("]"):
            rows = []
            names.append(line.strip()[1:-1])
            levels.append(rows)
        elif line.startswith("|") and line.count("|") > 1 and rows is not None:
            rows.append(line[1:line.rindex("|")])
    return names, levels


def load_levels():
    """Take the levels from the text file, if it makes sense. Keep the built-in ones if
    it does not -- a half-typed edit must not break the game you are playing."""
    global NAMES, LEVELS
    if not os.path.exists(LEVELS_TXT):
        dump_levels()
    names, levels = read_levels()
    bad = [n for n, rows in zip(names, levels) if not rows or "P" not in "".join(rows)]
    if levels and "W" not in "".join(levels[0]):
        bad.append(names[0] + " (no W: the wizard, and so the whole opening)")
    if not levels or bad:
        print("levels.txt: %s -- keeping the built-in levels"
              % ("nothing found" if not levels else "no start in " + ", ".join(bad)))
        return
    NAMES, LEVELS = names, levels
    GUST[:] = (GUST + [GUST[-1]] * len(levels))[:len(levels)]
    SWING[:] = (SWING + [SWING[-1]] * len(levels))[:len(levels)]'''


def emit_sound(n):
    if n < 38:
        return None
    head = '''SOUND = {}


TUNES = {                                        # every sound, as notes: (from, to, seconds)
    "jump": [(300, 620, 0.13)],                  # up
    "coin": [(880, 880, 0.05), (1320, 1320, 0.10)],   # two blips, a fifth apart
    "die": [(440, 90, 0.40)],                    # down
    "knock": [(220, 120, 0.09)],                 # a stone landing
    "bounce": [(180, 780, 0.22)],                # a trampoline: longer and higher than a jump
    "fall": [(160, 50, 0.30)],                   # a brick dropping away
    "talk": [(520, 560, 0.05)],                  # one line of the conversation
    "hit": [(140, 60, 0.16)],                    # your swing landing on him
    "curse": [(120, 38, 1.30)],                  # him taking your eyes: long, and all the way down
    "level": [(523, 523, 0.12), (659, 659, 0.12), (784, 784, 0.12)],            # three notes up
    "win": [(523, 523, 0.16), (659, 659, 0.16), (784, 784, 0.16), (1047, 1047, 0.16)],
    "gameover": [(330, 330, 0.30), (262, 262, 0.30), (196, 196, 0.30), (131, 131, 0.30)],
}
VOLUME = {                                       # how loud each one is, 0 to 1: the music sits
    "jump": 0.30, "coin": 0.28, "die": 0.40,     # at 0.30, so a game sound is around that,
    "knock": 0.38, "bounce": 0.36, "fall": 0.36, # a warning above it and a blip below it
    "talk": 0.16, "hit": 0.48, "curse": 0.42,
    "level": 0.30, "win": 0.34, "gameover": 0.34,
    "throw": 0.22, "wind": 0.35,
}


def note(f0, f1, secs, kind="square"):
    """A note that slides from f0 to f1, written out as raw samples. A wave is a number
    that goes up and down; how fast it does that is the pitch. "noise" is no pitch at all:
    a random number every sample, which is what wind and a thrown stone sound like. The
    last line fades it out -- a wave that stops dead is a click in the speaker."""
    rate, out = 22050, array.array("h")
    total, phase = int(rate * secs), 0.0
    for i in range(total):
        phase += 2 * math.pi * (f0 + (f1 - f0) * i / total) / rate
        wave = math.sin(phase)
        if kind == "square":
            wave = 1.0 if wave > 0 else -1.0
        if kind == "noise":
            wave = random.uniform(-1.0, 1.0)
        out.append(int(wave * (1.0 - i / total) ** 3 * 8000))
    return out


def make_sounds():
    """Every sound in the game, made of arithmetic. Not one file."""
    try:
        # pygame.init() may already have opened the mixer at its own settings, and a second
        # init() would be ignored. Close it first, so the mixer is told the same rate and
        # channel count note() writes at -- otherwise every sound plays at the wrong pitch.
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 1, 512)
    except pygame.error:
        return                                    # no sound card: play on in silence
    for name, parts in TUNES.items():
        tune = array.array("h")
        for f0, f1, secs in parts:
            tune += note(f0, f1, secs)
        SOUND[name] = pygame.mixer.Sound(buffer=tune.tobytes())
    SOUND["throw"] = pygame.mixer.Sound(buffer=note(0, 0, 0.12, "noise").tobytes())
    SOUND["wind"] = pygame.mixer.Sound(buffer=note(0, 0, 2.0, "noise").tobytes())
    for name, sound in SOUND.items():
        sound.set_volume(VOLUME[name])           # so no effect shouts over another
    pygame.mixer.Channel(1).play(SOUND["wind"], loops=-1)   # always blowing; how loud is
    pygame.mixer.Channel(1).set_volume(0.0)                # for gusts() to say, every frame


def beep(name):
    if name in SOUND:
        SOUND[name].play()'''
    if n >= 56:
        head = head.replace('''def make_sounds():
    """Every sound in the game, made of arithmetic. Not one file."""''',
'''RECORDED = {"jump": "jump.wav", "coin": "coin.wav", "die": "hurt.wav",
            "fall": "explosion.wav", "level": "power_up.wav", "knock": "tap.wav"}


def make_sounds():
    """Every sound in the game. Most are arithmetic; six are recordings, loaded last so
    each one quietly replaces the made-up version of the same name."""''')
        head += '''


def load_recorded():
    """Six wav files from a free pack. A recording of a real coin beats a square wave."""
    for name, filename in RECORDED.items():
        path = os.path.join(ART, "sounds", filename)
        if os.path.exists(path):
            SOUND[name] = pygame.mixer.Sound(path)
            SOUND[name].set_volume(VOLUME[name])       # the same level as the sound it replaces'''
        head = head.replace('''    SOUND["throw"] = pygame.mixer.Sound(buffer=note(0, 0, 0.12, "noise").tobytes())''',
'''    load_recorded()
    SOUND["throw"] = pygame.mixer.Sound(buffer=note(0, 0, 0.12, "noise").tobytes())''')
        head = head.replace('''            SOUND[name].set_volume(VOLUME[name])       # the same level as the sound it replaces''',
'''            SOUND[name].set_volume(VOLUME[name])       # the same level as the sound it replaces''')
    if n >= 57:
        head += '''


def music():
    """Four bars of A minor, and nothing but notes one after another. A bar is four beats
    at sixty beats a minute; eight notes to a bar, so half a beat each. Play it on its own
    channel with loops=-1 and it goes round for ever, under everything else."""
    bars = [(220, 262, 330),                      # A minor
            (175, 220, 262),                      # F
            (262, 330, 392),                      # C
            (196, 247, 294)]                      # G
    tune = array.array("h")
    for chord in bars:
        for i in range(8):
            f = chord[i % 3] * (2 if i >= 4 else 1)   # the top half of the bar, an octave up
            tune += note(f, f, 0.5, "sine")
    return pygame.mixer.Sound(buffer=tune.tobytes())'''
    return head


def emit_clock(n):
    return None if n < 34 else 'def clock_str(f):\n    return "%d:%02d" % (f // 3600, f // 60 % 60)'


def emit_draw(n):
    if n < 6:
        return None
    tick = "beat" if n >= 40 else "frames"
    args = "scr, font, big" if n >= 20 else "scr"
    out = ["def draw(%s):" % args]
    if n >= 40:
        out += ["    global beat",
                "    beat += 1                                     # one tick per frame drawn,",
                "                                                  # even when nothing else moves"]
    if n >= 19:
        out.append('    here = P["x"]                                   # what the camera follows')
        if n >= 37:
            out.append("    if dying: here = body[0]                     # the camera stays with your body")
        out.append("    cam = max(0, min(int(here) + PW // 2 - VW // 2, COLS * TILE - VW))")
    if n >= 44:
        out += ["    scr.fill(SKY[0].get_at((4, 4)))               # the night, taken from the art",
                "    for layer, slower in ((SKY[0], 4), (SKY[1], 2)):",
                "        wide = layer.get_width()",
                "        for x in range(-wide, VW + wide, wide):",
                "            # divide the camera and the far layer drifts slower: that is parallax",
                "            scr.blit(layer, (x - (cam // slower) % wide, VH - layer.get_height()))"]
    else:
        out.append("    scr.fill((25, 25, 35))")
    out.append("    for r in range(ROWS):")
    out.append("        for c in range(cam // TILE, min(COLS, cam // TILE + VW // TILE + 2)):"
               if n >= 19 else "        for c in range(COLS):")
    out.append("            ch = LVL[r][c]")
    out.append('            if ch == " ":')
    out.append("                continue")
    if n >= 20:
        out += ["            if (c, r) in taken:", "                continue"]
    if n >= 29:
        out += ["            if (c, r) in gone:", "                continue"]
    if n >= 22:
        out += ['            if ch == "W" and not wizard:', "                continue"]
    cam = " - cam" if n >= 19 else ""
    out.append("            box = pygame.Rect(c * TILE%s, r * TILE, TILE, TILE)" % cam)
    if n >= 25:
        out += ["            shake = hit.get((c, r), 0)               # frames of truth this square has left",
                "            seen = shake > 0                         # telling the truth, for now",
                '            if ch != "#":                            # the ground stays put',
                "                box = box.move(shaken(shake), 0)",
                "            lie = seen and ch in LIARS"]
    if n >= 29:
        out += ['            if ch == "c" and (c, r) in crack:        # counting down under your feet',
                "                box = box.move(int(math.sin(frames) * 2), 0)"]
    if n >= 28:
        out += ['            if ch == "~" and not seen:', "                continue"]

    branches = []
    if n >= 39:                                     # a picture, if there is one for this letter
        lookup = ['pic = COIN[(%s // 6) %% len(COIN)] if ch in "ox" else PIC.get(ch)' % tick
                  if n >= 40 else "pic = PIC.get(ch)"]
        if n >= 45:
            lookup += ["if seen and ch in TRUE:                  # for half a second, the truth",
                       "    pic = TRUE[ch]",
                       "    if isinstance(pic, list):            # and a fire moves",
                       "        pic = pic[(%s // 5) %% len(pic)]" % tick]
        out += ["            " + l for l in lookup]
        branches.append(("if pic:", ["scr.blit(pic, box)"]))
    if n < 40:
        if n >= 20:
            if n >= 25:
                branches.append(('if ch in "ox":',
                                 ["col = LOOK[ch]",
                                  "if lie: col = TRUTH[ch]",
                                  "pygame.draw.circle(scr, col, box.center, 9)",
                                  "if lie: pygame.draw.circle(scr, edge(col), box.center, 9, 2)"]))
            else:
                branches.append(('if ch in "ox":', ["col = LOOK[ch]", "pygame.draw.circle(scr, col, box.center, 9)"]))
        if n >= 21:
            if n >= 25:
                branches.append(('if ch in "^t":',
                                 ["col = LOOK[ch]",
                                  "if lie: col = TRUTH[ch]",
                                  "pts = [box.bottomleft, (box.centerx, box.top), box.bottomright]",
                                  "pygame.draw.polygon(scr, col, pts)",
                                  "if lie: pygame.draw.polygon(scr, edge(col), pts, 2)"]))
            else:
                branches.append(('if ch in "^t":',
                                 ["col = LOOK[ch]",
                                  "pts = [box.bottomleft, (box.centerx, box.top), box.bottomright]",
                                  "pygame.draw.polygon(scr, col, pts)"]))
    if n >= 52:
        branches.append(('if ch == "W":',
                         ["# he turns to face you: everything he does is aimed at where you stand",
                          'at_you = P["x"] + PW / 2 < box.centerx + cam',
                          "if casting > 0:                      # taking your eyes",
                          "    seq = CAST_L if at_you else CAST",
                          "    wz = seq[min(len(seq) - 1, (CURSE - casting) * len(seq) // CURSE)]",
                          "elif flash > 0:                      # your swing just landed",
                          "    seq = HURT_L if at_you else HURT",
                          "    wz = seq[min(len(seq) - 1, (HIT_FOR - flash) * len(seq) // HIT_FOR)]",
                          "else:",
                          "    seq = WIZ_L if at_you else WIZ",
                          "    wz = seq[(%s // 8) %% len(seq)]" % tick,
                          "scr.blit(wz, (box.centerx - wz.get_width() // 2, box.bottom - wz.get_height()))"]))
    elif n >= 22:
        branches.append(('if ch == "W":', ["pygame.draw.rect(scr, (160, 80, 220), box.inflate(-8, 0))"]))
    if n >= 46:
        branches.append(('if ch in "G!":',
                         ['fake = ch == "!" and lie',
                          'door = (DOOR_BAD if fake else DOOR_OK)[(%s // 7) %% len(DOOR_OK)]' % tick,
                          "scr.blit(door, (box.centerx - door.get_width() // 2,",
                          "                box.bottom - door.get_height()))",
                          "if fake:                             # and what is waiting in it",
                          "    dm = DEMON[(%s // 9) %% len(DEMON)]" % tick,
                          "    scr.blit(dm, (box.centerx - dm.get_width() // 2,",
                          "                  box.bottom - dm.get_height()))"]))
    elif n >= 20:
        door = ["col = (90, 230, 190)"]
        if n >= 30:
            door.append('if seen and ch == "!": col = TRUTH["!"]')
        door.append("pygame.draw.rect(scr, col, box.inflate(-6, -2))")
        branches.append(('if ch in "G!":', door))
    if 28 <= n < 40:
        branches.append(('if ch == "~":',
                         ['pygame.draw.rect(scr, TRUTH["~"], box)',
                          'pygame.draw.rect(scr, edge(TRUTH["~"]), box, 1)']))
    if n < 40:
        brick = ["col = LOOK[ch]"]
        if n >= 25:
            brick.append("if lie: col = TRUTH[ch]")
        brick.append("pygame.draw.rect(scr, col, box)")
        brick.append("pygame.draw.rect(scr, edge(col) if lie else (0, 0, 0), box, 2 if lie else 1)" if n >= 25
                     else "pygame.draw.rect(scr, (0, 0, 0), box, 1)")
        if n >= 29:
            brick += ['if ch == "c":',
                      "    pygame.draw.line(scr, (90, 60, 40), box.topleft, box.center, 1)"]
        branches.append(('if ch in "#%~c":', brick))
    # every branch is its own `if ... continue`, so adding one never rewrites another
    for head, lines in branches:
        out.append("            " + head)
        out += ["                " + l for l in lines]
        out.append("                continue")

    if n >= 47:
        out += ["    for pb in pebbles:",
                "        # turned a little further every frame, so it tumbles instead of pointing",
                "        spun = pygame.transform.rotate(SHOT[0], (pb[0] + pb[1]) * 3 % 360)",
                "        scr.blit(spun, (int(pb[0]) - cam - spun.get_width() // 2,",
                "                        int(pb[1]) - spun.get_height() // 2))"]
    elif n >= 24:
        out.append("    for pb in pebbles:")
        out.append("        pygame.draw.circle(scr, (230, 230, 230), (int(pb[0])%s, int(pb[1])), 3)" % cam)

    # the player: where, then what
    out.append('    x, y = int(P["x"])%s, int(P["y"])' % cam)
    if n >= 37:
        out.append("    if dying:                                     # where you fell, not where you restart")
        out.append("        x, y = int(body[0])%s, int(body[1])" % cam)
    if n >= 41:
        out += ["    who = pose()[face]",
                "    scr.blit(who, (x + PW // 2 - who.get_width() // 2, y + PH - who.get_height()))"]
    else:
        out.append("    pygame.draw.rect(scr, (240, 235, 220), (x, y, PW, PH), border_radius=4)")

    if n >= 49:
        out.append("    smoke(scr, cam)")
    if n >= 36:
        out += ["", "    if cursed or warp > 0:", "        gusts(scr)", "        wobble(scr, 3.2 + warp * 1.8)"]
    if n >= 20:
        out.append('    hud = "%s   %s   coins %d" % (NAMES[level], clock_str(frames), coins)' if n >= 34
                   else '    hud = "coins %d" % coins')
        out += ["    for i in range(LIVES):",
                "        heart(scr, VW - 30 - i * 22, 10, i < lives)"]
        if n >= 51:
            out += ['    for i, k in enumerate(("left", "right", "space", "click")):',
                    "        scr.blit(KEYS[k], (10 + i * 36, VH - 42))"]
        out += ["    if over:",
                "        veil = pygame.Surface((VW, VH), pygame.SRCALPHA)",
                "        veil.fill((8, 6, 12, 185))",
                "        scr.blit(veil, (0, 0))",
                '        card = big.render("GAME OVER", True, (240, 120, 130))',
                "        scr.blit(card, card.get_rect(center=(VW // 2, VH // 2 - 20)))",
                '        again = font.render("press space to try again", True, (222, 216, 206))',
                "        scr.blit(again, again.get_rect(center=(VW // 2, VH // 2 + 24)))",
                "        return"]
        if n >= 53:
            dim = {"title": 165, "walk": 70, "hit": 70, "talk": 120, "cast": 60}
            out += ["    if scene:",
                    "        dim = %r" % dim,
                    "        veil = pygame.Surface((VW, VH), pygame.SRCALPHA)",
                    "        veil.fill((8, 6, 12, dim[scene]))",
                    "        scr.blit(veil, (0, 0))",
                    '        if scene == "title":',
                    '            card = big.render("TRUST NO ONE", True, (232, 226, 210))',
                    "            scr.blit(card, card.get_rect(center=(VW // 2, 170)))",
                    "            for i, line in enumerate(OPEN):",
                    "                t = font.render(line, True, (232, 226, 210))",
                    "                scr.blit(t, t.get_rect(center=(VW // 2, 250 + i * 34)))"]
            if n >= 54:
                out += ['        if scene == "talk":',
                        "            who_says, text = TALK[said]",
                        '            if who_says == "wiz":',
                        "                bubble(scr, font, text, wiz_at[0] * TILE + TILE // 2 - cam,",
                        "                       (wiz_at[1] + 1) * TILE - WIZ[0].get_height() - 58,",
                        "                       (196, 90, 90))",
                        "            else:",
                        '                bubble(scr, font, text, int(P["x"]) + PW // 2 - cam,',
                        '                       int(P["y"]) - 34, (150, 210, 235))']
            out += ['        if scene in ("title", "talk"):',
                    '            go = font.render("press space", True, (150, 140, 130))',
                    "            scr.blit(go, go.get_rect(bottomright=(VW - 12, VH - 12)))",
                    "        return"]
        out.append("    scr.blit(font.render(hud, True, (255, 255, 255)), (10, 10))")
        if n >= 34:
            out += ['    tip = "YOU MADE IT OUT — space to run it again" if won else (',
                    '        "" if cursed else "click to throw a pebble — it tells you what a tile really is")',
                    "    if frames < 140 and not won:",
                    "        tip = NAMES[level]",
                    "    if tip:",
                    "        t = big.render(tip, True, (255, 255, 255))",
                    "        scr.blit(t, t.get_rect(center=(VW // 2, 90)))"]
    return "\n".join(out)


def emit_pose(n):
    """Which picture of her to draw. Every later step adds a rule above the last line."""
    if n < 41:
        return None
    tick = "beat"
    out = ["def pose():", '    """The frame of her to draw right now: the newest rule that applies wins."""']
    if n >= 50:
        out += ["    if dying:                                     # she goes down where she fell",
                '        seq = PLAYER["death"]',
                "        return seq[min(len(seq) - 1, (FALL - dying) * len(seq) // (FALL - 12))]"]
    if n >= 48:
        out += ["    if throwing > 0:                              # mid-throw, whatever else",
                '        seq = %s' % ('PLAYER["swing"] if scene == "hit" else PLAYER["throw"]' if n >= 53
                                      else 'PLAYER["throw"]'),
                "        return seq[min(len(seq) - 1, (THROW - throwing) * len(seq) // THROW)]"]
    if n >= 42:
        out += ['    if not P["g"]:',
                '        seq = PLAYER["jump"] if P["vy"] < 0 else PLAYER["fall"]',
                "        return seq[(%s // 6) %% len(seq)]" % tick,
                '    if abs(P["vx"]) > 0.6:',
                '        seq = PLAYER["run"]',
                "        return seq[(%s // 6) %% len(seq)]" % tick]
    out += ['    seq = PLAYER["idle"]', "    return seq[(%s // 6) %% len(seq)]" % tick]
    return "\n".join(out)


def emit_gusts(n):
    if n < 36:
        return None
    return '''def gusts(scr):
    """Streaks so the wind is visible before it throws your jump off. The air is added up
    frame by frame -- drawing at frames * wind would follow how fast the wind is changing,
    not which way it blows, and run against the shove for half of every swing."""
    global blown
    w = wind()
    blown += w * 26                               # this frame's worth of moving air
WINDVOL    if abs(w) < 0.012:
        return
    ln = int(abs(w) * 90) + 6
    for i in range(26):
        y = (i * 131) % VH
        x = int(i * 217 + blown) % (VW + 200) - 100
        pygame.draw.line(scr, (58, 58, 82), (x, y), (x + (ln if w > 0 else -ln), y), 1)


def wobble(scr, amt):
    """The curse warping what you see. Shifts bands, never the truth."""
    src = scr.copy()
    for y in range(0, VH, 5):
        dx = int(math.sin(frames / 11.0 + y / 26.0) * amt + math.sin(frames / 3.7 + y / 9.0) * amt * 0.35)
        scr.blit(src, (dx, y), (0, y, VW, 5))
    if amt > 8:                                   # heavy burst: the world tears
        ghost = src.copy(); ghost.set_alpha(110)
        scr.blit(ghost, (int(math.sin(frames / 5.0) * amt * 1.4), int(math.cos(frames / 6.0) * 3)))'''.replace(
        "WINDVOL", '''    if "wind" in SOUND:                           # the hiss follows the gust
        pygame.mixer.Channel(1).set_volume(VOLUME["wind"] * min(1.0, abs(w) / max(GUST)))
''' if n >= 38 else "")


def emit_main(n):
    out = ["def main():", "    pygame.init()",
           "    scr = pygame.display.set_mode((VW, VH))",
           '    pygame.display.set_caption("Trust No One")']
    if n >= 20:
        out.append("    font, big = pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 30)")
    out.append("    clk = pygame.time.Clock()")
    if n >= 55:
        out.append("    load_levels()")
    if n >= 39:
        out.append("    art()")
    if n >= 38:
        out.append("    make_sounds()")
    if n >= 57:
        out += ["    if SOUND:                                 # four bars, for ever, underneath",
                "        pygame.mixer.Channel(0).play(music(), loops=-1)",
                "        pygame.mixer.Channel(0).set_volume(0.30)"]
    if n >= 2:
        out.append("    reset()")
    out.append("    while True:")
    if n >= 14:
        out.append("        pressed = False")
    out += ["        for e in pygame.event.get():",
            "            if e.type == pygame.QUIT:",
            "                return"]
    if n >= 12:
        out.append("            if e.type == pygame.KEYDOWN:")
        out.append("                if %s and e.key == pygame.K_SPACE: reset()" % ("(over or won)" if n >= 33 else "over"))
        if n >= 14:
            out.append("                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True")
        if n >= 53:
            out.append("                if scene and e.key == pygame.K_SPACE: advance()")
    if n >= 24:
        guard = " and not won" if n >= 33 else ""
        if n >= 53:
            guard += " and not scene"
        out.append("            if e.type == pygame.MOUSEBUTTONDOWN%s:" % guard)
        out.append('                cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))')
        out.append("                throw(e.pos[0] + cam, e.pos[1])")
        if n >= 53:
            out += ["            if e.type == pygame.MOUSEBUTTONDOWN and scene:",
                    "                advance()          # a click turns the page of the story"]
    if n >= 3:
        out.append("        k = pygame.key.get_pressed()")
        if n >= 14:
            call = ["step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,",
                    "     k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])"]
        else:
            call = ["step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d])"]
        if n >= 53:
            out += ["        if scene:                              # the story is playing",
                    "            scene_step()",
                    "        else:"]
        pad = "            " if n >= 53 else "        "
        out.append(pad + call[0])
        if len(call) > 1:
            out.append(pad + "     " + call[1].strip())
        if n >= 24:
            out.append(pad + "pebble_step()")
    if n >= 20:
        out.append("        draw(scr, font, big)")
    elif n >= 6:
        out.append("        draw(scr)")
    else:
        out.append("        scr.fill((25, 25, 35))")
        if n >= 2:
            out.append('        pygame.draw.rect(scr, (240, 235, 220), (P["x"], P["y"], PW, PH), border_radius=4)')
    out += ["        pygame.display.flip()", "        clk.tick(60)"]
    return "\n".join(out)


def real_levels():
    """L2..L5 and their names, written out as full-width rows."""
    out = [real_level(name, REAL_LEVELS[name]) for name in ("L2", "L3", "L4", "L5")]
    out.append("LEVELS = [L1, L2, L3, L4, L5]")
    out.append("NAMES = [" + ", ".join('"%s"' % n for n in REAL_NAMES) + "]")
    return "\n".join(out)


def bare(n):
    parts = ['"""Trust No One -- step %d: %s.   Run it:  python3 steps/step%02d.py"""'
             % (n, TITLES[n - 1], n)]
    imports = ["import pygame"]
    if n >= 25: imports.append("import math")
    if n >= 31: imports.append("import random")
    if n >= 38: imports.append("import array")
    if n >= 39: imports.append("import os")
    parts.append("\n".join(sorted(imports, key=lambda m: (m != "import pygame", m))))
    parts.append(emit_consts(n))
    if n >= 5:
        alpha = emit_alphabet(n)
        parts.append((alpha + "\n" + emit_level(n)) if alpha else emit_level(n))
    if n >= 33:
        parts.append(real_levels())
    for piece in (emit_liars(n), emit_globals(n), emit_art(n), emit_art_helpers(n), emit_build_art(n), emit_story(n), emit_levels_file(n), emit_sound(n), emit_roll(n), emit_load(n),
                  emit_reset(n), emit_die(n), emit_wind(n), emit_tile(n), emit_solid(n),
                  emit_prect(n), emit_cells(n), emit_step(n), emit_pebble(n), emit_palette(n),
                  emit_truth(n), emit_edge(n), emit_shaken(n), emit_heart(n), emit_clock(n), emit_pose(n), emit_draw(n),
                  emit_gusts(n), emit_main(n)):
        if piece:
            parts.append(piece)
    parts.append('if __name__ == "__main__":\n    main()')
    return "\n\n".join(parts) + "\n"


# --------------------------------------------------------------- the comments
# A line's explanation is written into the file itself. At the step where the
# line arrives it is spelled out in full, above the line. From the next step on
# it shrinks to a short trailing note, so the new work has room to be explained.

WIDTH = 96                                  # how wide a commented line may get


def note_for(n, line):
    """The note for a line. "N:line" means only at step N, "N+:line" means from step N
    on -- which is what a line needs when its meaning changes and then stays changed."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    exact = NOTES.get("%d:%s" % (n, stripped))
    if exact:
        return exact
    for start in range(n, 0, -1):
        note = NOTES.get("%d+:%s" % (start, stripped))
        if note:
            return note
    return NOTES.get(stripped)


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
    print("wrote %d step files" % LAST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
