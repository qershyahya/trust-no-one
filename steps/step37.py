"""Trust No One -- step 37: You fall before you die.   Run it:  python3 steps/step37.py"""

import pygame   # the game library itself
import math
import random

VW, VH = 960, 640                     # the window, in pixels
TILE = 32                             # one square of the world

PW, PH = 20, 28                       # how big you are
SPD = 3.6                             # top walking speed, pixels per frame
GRAV = 0.35                           # pull per frame
MAXFALL = 12                          # the fastest you may fall
JUMP = -9.2                           # the kick upward, pixels per frame
COYOTE = 7                            # you may still jump 7 frames after the edge
BUFFER = 8                            # a press up to 8 frames early still counts
CUT = 0.42                            # let go early and the jump is cut to this
ACC, AIR, FRIC = 0.55, 0.32, 0.72     # how fast you gain speed, on the ground and off it, and lose it
BOUNCE = -12.3                        # a trampoline: stronger than JUMP
CRACK, AWAY = 18, 30                  # a cracked brick wobbles, drops, comes back
GUST = [0.0, 0.0, 0.20, 0.25, 0.30]   # how hard the wind blows, level by level
SWING = [1.0, 1.0, 1.0, 1.5, 2.2]     # and how fast it turns around
LIVES = 5                             # how many you start with
# one second, at 60 frames a second
FALL = 60                             # frames your body takes to come to rest
SHOWN = 30                            # frames a struck square tells the truth
CLEAR = 6                             # frames a stone ignores what it is inside

# honest: '#' brick  'o' coin  '^' spike  'W' wizard  'G' exit  'P' spawn
# lies:   '%' hologram brick   't' spike that is a trampoline   'x' coin that kills   '~' floor that isn't drawn   'c' brick that crumbles   '!' exit that warps you back
# rolled per run, so nothing can be memorised:
#         '?' spike or trampoline      '&' brick or hologram
# every run of '?' keeps one trampoline and every run of '&' one real brick, so no roll is a dead end
L1 = [   # the level
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                            o  o            ",
    "                                                            ",
    "            x         ##%#               ###&&##            ",
    "            x                         o             o       ",
    " P   W                  ^^^       ^ ??                   G  ",
    "##########   #######    ####################################",
    "##########ttt#######    ####################################",
]

L2 = [   # level II, The Floor Lies
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                   o  o              o           o              ",
    "             ##%                   ##&&             ###                    ##   ",
    "                 x                                        o             x       ",
    " P                                                                           G  ",
    "##########%%##&&####  %%#########%%#####    ######&&##########  %%##############",
    "####################tt^^################    ##################^^tt##############",
]
L3 = [   # level III, The Gaps Lie
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                           ~o~                                  ",
    "               o                           ~~~                 x                ",
    "                         o            ~~                o                       ",
    " P                                                                           G  ",
    "##########~~~   ~~~~##########  ~  ~  ~~##########~~~~~  ~ ~####################",
    "##########          ##########          ##########          ####################",
]
L4 = [   # level IV, Nothing Holds
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                                                                ",
    "                                          ###                                   ",
    "            x  o                 x   o               o  x                       ",
    "                                                                                ",
    "                                                                                ",
    " P                                                                           G  ",
    "##########ccccc###############cc#cccc#############cccc%ccc  ####################",
    "##########     ###############       #############          ####################",
]
L5 = [   # level V, The Gauntlet
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                          ",
    "                                                                                       G  ",
    "                                                                                      ####",
    "                                                                         o                ",
    "               o           x                         o                     x              ",
    "                           &&                                                             ",
    " P          ??                                !                                           ",
    "##########  ##  ####ccccccc### ~  ~ ######%%######  ########cc#cc#####    #########%%#####",
    "##########  ##  ####       ###      ######tt######  ?????###     tt###    #########tt#####",
]
LEVELS = [L1, L2, L3, L4, L5]   # the whole game, in one list
NAMES = ["I. The Curse", "II. The Floor Lies", "III. The Gaps Lie", "IV. Nothing Holds", "V. The Gauntlet"]

LIARS = set("%tx~c!")                 # every letter that lies, including the ones you have not met yet

LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured
level = 0                                             # which level is loaded
seed = 0                                              # this run's dice
SPAWN = (0, 0)                                        # where you start, found by load()
P = {}                                                # where you are, and how fast
cursed = False   # the curse: not yet
wizard = True   # he is standing in the level until you touch
won = False   # the last exit has been reached
coins = 0   # how many you have taken
frames = 0                                            # this level's clock
coy = 0   # coyote frames left
buf = 0   # frames since the jump key went down
warp = 0.0   # how hard the screen is bending right now
blown = 0.0                                           # how far the air has travelled
lives = LIVES   # how many you have left, right now
over = False                                          # the run is finished
# dying counts down while your body falls; body is where it is and how fast
dying, body = 0, [0.0, 0.0, 0.0]
taken = set()   # which coins you already picked up
pebbles = []   # every stone in the air right now
hit = {}   # squares a stone has struck
gone = set()   # squares that have dropped away
crack = {}   # every cracked brick you have stood on

def roll(row, rng):   # one row of the level, and this run's dice
    """'?' and '&' pick a side per run -- but each run of them keeps one safe tile."""
    out = list(row)
    i = 0
    while i < len(out):
        if out[i] in "?&":   # found a rollable square
            ch, j = out[i], i
            while j < len(out) and out[j] == ch:   # find the whole run of them, e.g
                j += 1
            safe, other = ("t", "^") if ch == "?" else ("#", "%")
            span = [rng.choice((safe, other)) for _ in range(j - i)]   # roll each square
            if safe not in span:   # every single one came up bad, so:
                span[rng.randrange(len(span))] = safe   # force one back
            out[i:j] = span   # write the rolled squares back over the ?s
            i = j
        else:
            i += 1
    return "".join(out)

def load(i):   # load takes a number now: which level to start
    """Take level i, measure it, find where you start, and stand there."""
    global LVL, COLS, ROWS, level, SPAWN, frames
    level = i
    frames = 0
    rows = LEVELS[i]   # the level asked for, as its list of strings
    COLS = max(len(r) for r in rows)
    rng = random.Random(seed * 977 + i)   # a different roll per level
    LVL = [roll(r.ljust(COLS), rng) for r in rows]
    ROWS = len(LVL)   # and the number of rows is the height
    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")
    LVL = [r.replace("P", " ") for r in LVL]   # then erase it
    taken.clear()   # a fresh level has all its coins
    pebbles.clear()
    hit.clear()
    gone.clear()
    crack.clear()
    place()   # back to the start

def reset():   # a whole fresh run
    """A whole fresh run: everything back to the beginning."""
    global cursed, wizard, lives, over, coins, seed, won
    seed = random.randrange(1 << 30)   # a new seed per run
    cursed = False   # the curse: not yet
    wizard = True   # he is standing in the level until you touch
    won = False   # the last exit has been reached
    coins = 0   # how many you have taken
    lives = LIVES   # how many you have left, right now
    over = False   # true when the last heart has gone
    load(0)   # the first level

def place():   # stand at the start of the level
    """At the start of the level, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)   # start where the level
    P["g"] = False   # not on the ground, until step() says so
    P["jump"] = False   # not mid-jump


def die():   # the same standing-still
    """Being killed. It costs a life, and the last one ends the run."""
    global lives, over, warp, dying
    warp = max(warp, 6.0)   # a small jolt on every death
    lives -= 1   # one heart, spent
    if lives <= 0:   # that was the last one
        over = True   # nothing moves again until you ask for a new
        return place()   # put the body down and stop
    # copy yourself into the body, keeping the speed you were hit at
    body[0], body[1], body[2] = P["x"], P["y"], P["vy"]
    # and start the clock. Nothing else in the game moves until it runs out
    dying = FALL


# one frame of a body falling. The same gravity you have, and the same floors
def fall():
    """Your body drops from wherever it was hit and comes to rest on the first thing
    that will hold it: ground, spikes, a trampoline. Then you are put back."""
    global dying
    dying -= 1
    body[2] = min(body[2] + GRAV, MAXFALL)
    body[1] += body[2]
    r = pygame.Rect(int(body[0]), int(body[1]), PW, PH)
    for _, rw, ch in cells(r):
        # ground, spikes or a trampoline: anything will hold a body
        if solid(ch) or ch in "^t":
            r.bottom = rw * TILE
            body[1], body[2] = float(r.y), 0.0
    # it fell out of the world, so there is nothing to watch
    if body[1] > ROWS * TILE:
        dying = 0                                 # out of the world: nothing left to watch
    # the body has come to rest, and you have been dead long enough
    if dying <= 0:
        # back to the start
        place()

def wind():   # how hard it is blowing, right now
    """How hard it is blowing right now, and which way: sin() swings it."""
    if not cursed:   # before the wizard there is no wind at all
        return 0.0   # before the wizard there is no wind at all
    return GUST[level] * math.sin(frames * SWING[level] / 110.0)   # sin swings between -1

def tile(c, r):   # what letter is at column c, row r?
    """What letter is at column c, row r? Off the map counts as empty air."""
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "   # off the edge of the map

def solid(ch):   # which letters stop you
    """Which letters stop you. Floor you cannot see and bricks that crumble are floor;
    a hologram is floor only until you are cursed."""
    return ch in "#~c" or (ch == "%" and not cursed)

def prect():   # your box, right now, as a Rect
    """Your box, right now."""
    return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)   # Rect wants whole pixels

def cells(rect):   # every tile a box overlaps
    """Every tile this box overlaps -- usually two to six of them."""
    for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):   # the -1 means touching
        for c in range(rect.left // TILE, (rect.right - 1) // TILE + 1):
            ch = tile(c, r)   # what is written in the square it has reached
            if ch != " " and (c, r) not in gone:   # something is written here and it has not
                yield c, r, ch   # hand them back one at a time as the loop asks

def step(left, right, pressed=False, held=False):   # two new arguments
    global cursed, wizard, won, coins, frames, coy, buf, warp
    warp = max(0.0, warp - 0.16)                  # every jolt fades, even on the game over screen
    if over: return                               # the run is finished
    if won: return                                # and so is the game
    # no keys, no clock, no wind: the world waits
    if dying:                                     # you are on your way down
        # one frame of the fall instead of one frame of you
        return fall()
    frames += 1

    want = (right - left) * SPD   # the speed you asked for
    a = ACC if P["g"] else AIR   # 0.55 of steering on the ground
    if want:
        P["vx"] += max(-a, min(a, want - P["vx"]))   # move toward the speed you want
    else:
        P["vx"] *= FRIC if P["g"] else 0.96   # let go and you slide to a stop
    P["vx"] += wind() * (1.0 if P["g"] else 2.2)   # gusts shove hardest in the air
    coy = COYOTE if P["g"] else coy - 1   # a countdown that refills every time you touch
    buf = BUFFER if pressed else buf - 1   # the same kind of countdown
    if buf > 0 and coy > 0:   # pressed recently AND grounded recently
        P["vy"], buf, coy, P["jump"] = JUMP, 0, 0, True   # jump, spend both credits
    if P["jump"] and not held and P["vy"] < JUMP * CUT:   # let go early while still rising
        P["vy"], P["jump"] = JUMP * CUT, False    # let go early, hop short -- never cuts a trampoline
    if P["vy"] >= 0:   # once you are falling there is nothing left
        P["jump"] = False   # not mid-jump
    P["vy"] = min(P["vy"] + GRAV, MAXFALL)   # add gravity every frame

    P["x"] += P["vx"]
    r = prect()   # where that move put you
    for c, _, ch in cells(r):
        if solid(ch):
            if P["vx"] > 0: r.right = c * TILE   # moving right
            elif P["vx"] < 0: r.left = (c + 1) * TILE   # moving left: the other face
            P["x"] = float(r.x); P["vx"] = 0.0   # stop dead, or you keep pressing into it
    P["x"] = min(max(P["x"], 0.0), COLS * TILE - PW)   # the level has two ends

    P["y"] += P["vy"]
    r = prect()   # where that move put you
    for _, rw, ch in cells(r):
        if solid(ch):
            if P["vy"] > 0: r.bottom = rw * TILE   # falling: land on top of it
            elif P["vy"] < 0: r.top = (rw + 1) * TILE   # rising: bonk your head
            P["y"] = float(r.y); P["vy"] = 0.0   # and the fall stops here
    # ponytail: 1px probe instead of trusting penetration -- sub-pixel gravity never sinks a full pixel
    P["g"] = P["vy"] >= 0 and any(solid(ch) for _, _, ch in cells(prect().move(0, 1)))

    for cell in list(crack):                      # every cracked brick has a clock
        crack[cell] += 1   # one more frame on this brick's clock
        if crack[cell] == CRACK:   # the warning is over
            gone.add(cell)                        # the warning is over: it drops
        elif crack[cell] >= CRACK + AWAY:   # its time away is up
            if prect().colliderect(pygame.Rect(cell[0] * TILE, cell[1] * TILE, TILE, TILE)):
                crack[cell] = CRACK + AWAY        # you are standing in its way: wait
            else:
                del crack[cell]; gone.discard(cell)   # the clock is thrown away and the brick
    if P["g"]:                                    # a brick you stand on starts its clock
        for c, rw, ch in cells(prect().move(0, 1)):
            if ch == "c" and (c, rw) not in crack:   # only start a clock that is not already
                crack[(c, rw)] = 0   # that exact square, from frame zero

    if P["y"] > ROWS * TILE:   # fell past the bottom row
        return die()   # back to the start, and nothing else this frame
    for c, rw, ch in cells(prect()):   # every square you are standing in, this frame
        if ch == "^":   # a real spike, which never lied to anybody
            return die()   # back to the start, and nothing else this frame
        if ch == "t" and not cursed:   # before the curse
            return die()   # back to the start, and nothing else this frame
        if ch == "t" and cursed:                  # the spikes that spring
            P["vy"], P["g"], P["jump"] = BOUNCE, False, False   # fire upward
        if ch == "x" and cursed:   # once cursed, the killer coin kills
            return die()   # back to the start, and nothing else this frame
        if ch == "!":   # the exit that is not one
            warp = 22.0   # the fake exit
            return die()   # back to the start, and nothing else this frame
        if ch == "o" and (c, rw) not in taken:   # a coin you have not had yet
            taken.add((c, rw)); coins += 1   # remember it
        if ch == "x" and (c, rw) not in taken:   # the killer coin still counts
            taken.add((c, rw)); coins += 1   # remember it
        if ch == "W" and wizard:
            wizard, cursed = False, True   # he vanishes, and you are cursed
            warp = 26.0                           # the biggest jolt in the game
        if ch == "G":   # the way out
            if level + 1 < len(LEVELS):   # another level to go?
                return load(level + 1)   # start it, and do nothing else this frame
            won = True   # that was the last one

def throw(tx, ty):   # tx, ty is where you clicked, in world pixels
    """Click far away for a hard throw, close for a soft lob."""
    cx, cy = P["x"] + PW / 2, P["y"] + PH / 2   # throw from your middle, not your corner
    dx, dy = tx - cx, ty - cy   # the arrow from you to the click
    d = max(1.0, (dx * dx + dy * dy) ** 0.5)   # its length
    sp = max(4.5, min(16.0, d / 20.0))        # close click = soft lob, far click = hard throw
    pebbles.append([cx, cy, dx / d * sp, dy / d * sp, 0])   # the last number is its age


def pebble_step():   # one frame for every pebble in the air
    """One frame for every stone in the air."""
    for cell in list(hit):                        # the truth fades on its own
        hit[cell] -= 1   # a frame closer to lying again
        if hit[cell] <= 0:   # its half second is up
            del hit[cell]   # and the square goes back to looking like
    for pb in pebbles[:]:   # the [:] makes a copy
        pb[3] += GRAV * 0.5   # pebbles fall too, at half weight
        pb[2] += wind() * 1.6   # your pebbles get blown off course too
        pb[0] += pb[2]; pb[1] += pb[3]   # the same speed-changes-position rule as you
        pb[4] += 1   # one frame older
        c, r = int(pb[0]) // TILE, int(pb[1]) // TILE
        if not (0 <= c < COLS and 0 <= r < ROWS):   # left the map
            pebbles.remove(pb); continue
        ch = tile(c, r)   # what is written in the square it has reached
        if ch == "W" and not wizard:              # he has gone: his square is air
            continue
        if pb[4] < CLEAR:                         # still leaving your hand
            continue
        if ch != " " and (c, r) not in gone and (c, r) not in taken:   # something is written
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    hit[(c + i, r + j)] = SHOWN   # the square and the ring around it
            pebbles.remove(pb)

LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "c": (150, 110, 70),
        "^": (170, 170, 180), "t": (170, 170, 180), "o": (240, 200, 60), "x": (240, 200, 60)}

# ponytail: a revealed lie keeps its own hue and goes darker/duller -- readable, never neon
TRUTH = {"%": (108, 84, 66), "t": (146, 162, 148), "x": (206, 168, 96),   # what each liar looks
         "~": (50, 50, 66), "c": (126, 92, 58), "!": (66, 178, 158)}

def edge(col):   # a darker version of any colour
    return tuple(max(0, v - 40) for v in col)

def shaken(n):   # the wobble
    """How far a struck square is knocked sideways: a wobble that dies down."""
    return int(math.sin(n * 0.9) * n / 6)

def heart(scr, x, y, full):   # a heart, drawn rather than loaded
    """A small heart: two lobes and a point. Cheaper than a picture, and it never
    goes missing."""
    col = (222, 70, 90) if full else (70, 60, 66)
    pygame.draw.circle(scr, col, (x + 4, y + 4), 4)
    pygame.draw.circle(scr, col, (x + 11, y + 4), 4)
    pygame.draw.polygon(scr, col, [(x, y + 5), (x + 15, y + 5), (x + 7, y + 15)])

def clock_str(f):   # frames into minutes and seconds
    return "%d:%02d" % (f // 3600, f // 60 % 60)   # %02d pads to two digits

def draw(scr, font, big):   # two fonts now
    here = P["x"]                                   # what the camera follows
    # the camera stays with your body, not where you will restart
    if dying: here = body[0]                     # the camera stays with your body
    cam = max(0, min(int(here) + PW // 2 - VW // 2, COLS * TILE - VW))   # the camera
    scr.fill((25, 25, 35))   # paint over the last frame, or it smears
    for r in range(ROWS):   # every row
        for c in range(cam // TILE, min(COLS, cam // TILE + VW // TILE + 2)):
            ch = LVL[r][c]
            if ch == " ":   # air: nothing to draw
                continue
            if (c, r) in taken:   # a coin you took is not drawn
                continue
            if (c, r) in gone:   # a square that has dropped away is not drawn
                continue
            if ch == "W" and not wizard:   # once he is gone, his square is air
                continue
            box = pygame.Rect(c * TILE - cam, r * TILE, TILE, TILE)   # every drawn thing
            shake = hit.get((c, r), 0)               # frames of truth this square has left
            seen = shake > 0                         # telling the truth, for now
            if ch != "#":                            # the ground stays put
                box = box.move(shaken(shake), 0)   # a struck square wobbles
            lie = seen and ch in LIARS   # revealed, and actually a liar
            if ch == "c" and (c, r) in crack:        # counting down under your feet
                box = box.move(int(math.sin(frames) * 2), 0)
            if ch == "~" and not seen:   # floor you cannot see stays unseen until
                continue
            if ch in "ox":   # coins, honest and not
                col = LOOK[ch]   # the colour this letter is drawn in
                if lie: col = TRUTH[ch]   # for half a second, the truth colour
                pygame.draw.circle(scr, col, box.center, 9)
                if lie: pygame.draw.circle(scr, edge(col), box.center, 9, 2)
                continue
            if ch in "^t":   # spikes, and the spikes that are not
                col = LOOK[ch]   # the colour this letter is drawn in
                if lie: col = TRUTH[ch]   # for half a second, the truth colour
                pts = [box.bottomleft, (box.centerx, box.top), box.bottomright]
                pygame.draw.polygon(scr, col, pts)
                if lie: pygame.draw.polygon(scr, edge(col), pts, 2)
                continue
            if ch == "W":
                pygame.draw.rect(scr, (160, 80, 220), box.inflate(-8, 0))   # the wizard
                continue
            if ch in "G!":   # the way out, and the exit that lies
                col = (90, 230, 190)   # exit green
                if seen and ch == "!": col = TRUTH["!"]   # found out
                pygame.draw.rect(scr, col, box.inflate(-6, -2))
                continue
            if ch == "~":
                pygame.draw.rect(scr, TRUTH["~"], box)
                pygame.draw.rect(scr, edge(TRUTH["~"]), box, 1)
                continue
            if ch in "#%~c":
                col = LOOK[ch]   # the colour this letter is drawn in
                if lie: col = TRUTH[ch]   # for half a second, the truth colour
                pygame.draw.rect(scr, col, box)
                pygame.draw.rect(scr, edge(col) if lie else (0, 0, 0), box, 2 if lie else 1)
                if ch == "c":
                    pygame.draw.line(scr, (90, 60, 40), box.topleft, box.center, 1)
                continue
    for pb in pebbles:
        pygame.draw.circle(scr, (230, 230, 230), (int(pb[0]) - cam, int(pb[1])), 3)
    x, y = int(P["x"]) - cam, int(P["y"])
    if dying:                                     # where you fell, not where you restart
        # where you fell, not where you restart
        x, y = int(body[0]) - cam, int(body[1])
    pygame.draw.rect(scr, (240, 235, 220), (x, y, PW, PH), border_radius=4)

    if cursed or warp > 0:   # the curse, and every jolt
        gusts(scr)
        wobble(scr, 3.2 + warp * 1.8)
    hud = "%s   %s   coins %d" % (NAMES[level], clock_str(frames), coins)
    for i in range(LIVES):   # one heart per life you started with
        heart(scr, VW - 30 - i * 22, 10, i < lives)   # the ones past lives are drawn dark
    if over:   # the run is finished
        veil = pygame.Surface((VW, VH), pygame.SRCALPHA)   # a surface with an alpha channel
        veil.fill((8, 6, 12, 185))   # near-black, and 185 out of 255 opaque
        scr.blit(veil, (0, 0))
        card = big.render("GAME OVER", True, (240, 120, 130))   # the only red text in the game
        scr.blit(card, card.get_rect(center=(VW // 2, VH // 2 - 20)))
        again = font.render("press space to try again", True, (222, 216, 206))
        scr.blit(again, again.get_rect(center=(VW // 2, VH // 2 + 24)))
        return
    scr.blit(font.render(hud, True, (255, 255, 255)), (10, 10))
    tip = "YOU MADE IT OUT — space to run it again" if won else (   # space, not R: R is gone
        "" if cursed else "click to throw a pebble — it tells you what a tile really is")
    if frames < 140 and not won:   # for the first couple of seconds of a level
        tip = NAMES[level]
    if tip:
        t = big.render(tip, True, (255, 255, 255))
        scr.blit(t, t.get_rect(center=(VW // 2, 90)))   # get_rect(center=...) centres the text

def gusts(scr):   # the wind
    """Streaks so the wind is visible before it throws your jump off. The air is added up
    frame by frame -- drawing at frames * wind would follow how fast the wind is changing,
    not which way it blows, and run against the shove for half of every swing."""
    global blown
    w = wind()
    blown += w * 26                               # this frame's worth of moving air
    if abs(w) < 0.012:   # too gentle to bother drawing
        return
    ln = int(abs(w) * 90) + 6   # stronger wind, longer streaks
    for i in range(26):
        y = (i * 131) % VH
        x = int(i * 217 + blown) % (VW + 200) - 100   # now a streak moves at 26 * w
        pygame.draw.line(scr, (58, 58, 82), (x, y), (x + (ln if w > 0 else -ln), y), 1)


def wobble(scr, amt):   # the curse bending what you see
    """The curse warping what you see. Shifts bands, never the truth."""
    src = scr.copy()   # a photograph of the finished frame
    for y in range(0, VH, 5):   # cut it into 5-pixel bands
        dx = int(math.sin(frames / 11.0 + y / 26.0) * amt + math.sin(frames / 3.7 + y / 9.0) * amt * 0.35)
        scr.blit(src, (dx, y), (0, y, VW, 5))   # paste each band back, shifted
    if amt > 8:                                   # heavy burst: the world tears
        ghost = src.copy(); ghost.set_alpha(110)   # a half-transparent second copy
        scr.blit(ghost, (int(math.sin(frames / 5.0) * amt * 1.4), int(math.cos(frames / 6.0) * 3)))

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    font, big = pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 30)   # two sizes
    clk = pygame.time.Clock()   # our metronome
    reset()   # a whole fresh run
    while True:   # the game loop
        pressed = False   # true for one frame only
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
            if e.type == pygame.KEYDOWN:
                if (over or won) and e.key == pygame.K_SPACE: reset()   # space starts a fresh
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True
            if e.type == pygame.MOUSEBUTTONDOWN and not won:
                cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))
                throw(e.pos[0] + cam, e.pos[1])   # e.pos is where on screen you clicked; adding
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,
             k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])
        pebble_step()   # move the pebbles once per frame
        draw(scr, font, big)   # draw() takes both fonts from the day it takes
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
