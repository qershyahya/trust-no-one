"""Trust No One -- step 33: Five levels.   Run it:  python3 steps/step33.py"""

import math, random, sys
import pygame   # the game library itself

TILE, VW, VH = 32, 960, 640   # TILE is the size of one square, in pixels

# feel knobs, tuned at 60fps
GRAV, SPD, JUMP, BOUNCE, MAXFALL = 0.35, 3.6, -9.2, -12.3, 12   # BOUNCE is stronger than JUMP
ACC, AIR, FRIC = 0.55, 0.32, 0.72   # how fast you gain speed on the ground
COYOTE, BUFFER, CUT = 7, 8, 0.42     # late jump, early jump, tap = short hop
CRUMB = 26                            # frames a crumbling brick holds you
PW, PH = 20, 28

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
    "                      ####               ###&&##            ",
    "            x                         o             o       ",
    " P   W                   ??       ^ ??                   G  ",
    "##########   #######    ####################################",
    "##########ttt#######    ####################################",
]

# level II, The Floor Lies: the ground is threaded with holograms, and trampolines wait
# underneath
L2 = [
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
    "             ###                   ##&&             ###                    ##   ",
    "                 x                                        o             x       ",
    " P                                                                           G  ",
    "##########%%##&&####  %%#########%%#####    ######&&##########  %%##############",
    "####################  tt################    ##################  tt##############",
]
# level III, The Gaps Lie: those wide holes are mostly invisible floor. Walk over nothing
L3 = [
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
    "                                           ~~~                                  ",
    "               o                            o                  o                ",
    "                         o                              o                       ",
    " P                                                                           G  ",
    "##########~~~   ~~~~##########  ~  ~  ~~##########~~~~~  ~ ~####################",
    "##########          ##########          ##########          ####################",
]
# level IV, Nothing Holds: nearly every brick is cracked, so standing still is what kills you
L4 = [
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
    "##########ccccc###############cc#cccc#############cccc#ccc  ####################",
    "##########     ###############       #############          ####################",
]
# level V, The Gauntlet: one of everything, including the fake exit, and the strongest wind
L5 = [
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
# the whole game, in one list
LEVELS = [L1, L2, L3, L4, L5]
NAMES = ["I. The Curse", "II. The Floor Lies", "III. The Gaps Lie", "IV. Nothing Holds", "V. The Gauntlet"]

LIARS = set("%tx~c!")

LVL, COLS, ROWS, SPAWN, level, seed = [], 0, 0, (0, 0), 0, 0
P = {}
cursed = wizard = won = False
coins = frames = total = coy = buf = 0
taken, revealed, gone, pebbles, crumb = set(), set(), set(), [], {}

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

# load takes a number now: which level to start
def load(i):
    global LVL, COLS, ROWS, SPAWN, level, frames
    # remember which level we are on, and restart its clock
    level, frames = i, 0
    rows = LEVELS[i]
    COLS = max(len(r) for r in rows)
    # a different roll per level, still repeatable from the one seed
    rng = random.Random(seed * 977 + i)
    LVL = [roll(r.ljust(COLS), rng) for r in rows]
    ROWS = len(LVL)   # and the number of rows is the height
    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")
    LVL = [r.replace("P", " ") for r in LVL]   # then erase it
    taken.clear(); revealed.clear(); gone.clear(); pebbles.clear(); crumb.clear()
    die()   # back to the start

def reset():   # a whole fresh run
    global cursed, wizard, won, coins, total, seed
    seed = random.randrange(1 << 30)   # a new seed per run
    cursed, won, coins, total = False, False, 0, 0
    wizard = True
    load(0)

def die():   # back to the start, standing still
    """Back to the start, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0, g=False, jump=False)

def tile(c, r):   # what letter is at column c, row r?
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "   # off the edge of the map

def solid(ch):   # which letters stop you
    return ch in "#~c" or (ch == "%" and not cursed)

def prect():   # your box, right now, as a Rect
    return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)   # Rect wants whole pixels

def cells(rect):   # every tile a box overlaps
    for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):   # the -1 means touching
        for c in range(rect.left // TILE, (rect.right - 1) // TILE + 1):
            ch = tile(c, r)
            if ch != " " and (c, r) not in gone:
                yield c, r, ch   # hand them back one at a time as the loop asks

def step(left, right, pressed=False, held=False):   # two new arguments
    global cursed, wizard, won, coins, frames, total, coy, buf
    # this level's clock, and the run's clock
    frames += 1; total += 1

    want = (right - left) * SPD   # the speed you asked for
    a = ACC if P["g"] else AIR   # 0.55 of steering on the ground
    if want:
        P["vx"] += max(-a, min(a, want - P["vx"]))   # move toward the speed you want
    else:
        P["vx"] *= FRIC if P["g"] else 0.96   # let go and you slide to a stop
    coy = COYOTE if P["g"] else coy - 1   # a countdown that refills every time you touch
    buf = BUFFER if pressed else buf - 1   # the same kind of countdown
    if buf > 0 and coy > 0:   # pressed recently AND grounded recently
        P["vy"], buf, coy, P["jump"] = JUMP, 0, 0, True   # jump, spend both credits
    if P["jump"] and not held and P["vy"] < JUMP * CUT:   # let go early while still rising
        P["vy"], P["jump"] = JUMP * CUT, False    # let go early, hop short -- never cuts a trampoline
    if P["vy"] >= 0:   # once you are falling there is nothing left
        P["jump"] = False
    P["vy"] = min(P["vy"] + GRAV, MAXFALL)   # add gravity every frame

    P["x"] += P["vx"]
    r = prect()   # where that move put you
    for c, _, ch in cells(r):
        if solid(ch):
            if P["vx"] > 0: r.right = c * TILE   # moving right
            elif P["vx"] < 0: r.left = (c + 1) * TILE   # moving left: the other face
            P["x"] = float(r.x); P["vx"] = 0.0   # stop dead, or you keep pressing into it

    P["y"] += P["vy"]
    r = prect()   # where that move put you
    for _, rw, ch in cells(r):
        if solid(ch):
            if P["vy"] > 0: r.bottom = rw * TILE   # falling: land on top of it
            elif P["vy"] < 0: r.top = (rw + 1) * TILE   # rising: bonk your head
            P["y"] = float(r.y); P["vy"] = 0.0   # and the fall stops here
    # ponytail: 1px probe instead of trusting penetration -- sub-pixel gravity never sinks a full pixel
    P["g"] = P["vy"] >= 0 and any(solid(ch) for _, _, ch in cells(prect().move(0, 1)))

    if P["g"]:                                    # crumbling bricks only count while stood on
        for c, rw, ch in cells(prect().move(0, 1)):
            if ch == "c":
                crumb[(c, rw)] = crumb.get((c, rw), 0) + 1   # count the frames for that exact
                if crumb[(c, rw)] > CRUMB:   # held long enough
                    gone.add((c, rw))   # into gone

    if P["y"] > ROWS * TILE:   # fell past the bottom row
        return die()   # back to the start, and nothing else this frame
    for c, rw, ch in cells(prect()):   # every square you are standing in, this frame
        if ch == "^" or (ch == "t" and not cursed) or (ch == "x" and cursed):
            return die()   # back to the start, and nothing else this frame
        if ch == "t" and cursed:   # the spikes
            P["vy"], P["g"], P["jump"] = BOUNCE, False, False   # fire upward
        elif ch == "!":   # the exit that is not one
            return die()   # back to the start, and nothing else this frame
        elif (ch == "o" or ch == "x") and (c, rw) not in taken:   # the killer coin still counts
            taken.add((c, rw)); coins += 1   # remember it
        elif ch == "W" and wizard:   # touched the wizard
            wizard, cursed = False, True   # he vanishes, and you are cursed
        # the way out
        elif ch == "G":
            # another level to go?
            if level + 1 < len(LEVELS):
                # start it, and do nothing else this frame
                return load(level + 1)
            # that was the last one
            won = True

def throw(tx, ty):   # tx, ty is where you clicked, in world pixels
    cx, cy = P["x"] + PW / 2, P["y"] + PH / 2   # throw from your middle, not your corner
    dx, dy = tx - cx, ty - cy   # the arrow from you to the click
    d = max(1.0, (dx * dx + dy * dy) ** 0.5)   # its length
    sp = max(4.5, min(16.0, d / 20.0))        # close click = soft lob, far click = hard throw
    pebbles.append([cx, cy, dx / d * sp, dy / d * sp])   # dx/d is direction alone; times sp


def pebble_step():   # one frame for every pebble in the air
    for pb in pebbles[:]:   # the [:] makes a copy
        pb[3] += GRAV * 0.5   # pebbles fall too, at half weight
        pb[0] += pb[2]; pb[1] += pb[3]   # the same speed-changes-position rule as you
        c, r = int(pb[0]) // TILE, int(pb[1]) // TILE
        if not (0 <= c < COLS and 0 <= r < ROWS):   # left the map
            pebbles.remove(pb); continue
        if tile(c, r) != " " and (c, r) not in gone:
            revealed.update((c + i, r + j) for i in (-1, 0, 1) for j in (-1, 0, 1))
            pebbles.remove(pb)

LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "c": (150, 110, 70),
        "^": (170, 170, 180), "t": (170, 170, 180), "o": (240, 200, 60), "x": (240, 200, 60)}
# ponytail: a revealed lie keeps its own hue and goes darker/duller -- readable, never neon
TRUTH = {"%": (108, 84, 66), "t": (146, 162, 148), "x": (206, 168, 96),
         "~": (50, 50, 66), "c": (126, 92, 58), "!": (66, 178, 158)}

def edge(col):   # a darker version of any colour
    return tuple(max(0, v - 40) for v in col)

def draw(scr, font):   # draw needs the font now, for the coin counter
    cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))
    scr.fill((25, 25, 35))   # paint over the last frame, or it smears
    for r in range(ROWS):   # every row
        for c in range(cam // TILE, min(COLS, cam // TILE + VW // TILE + 2)):
            ch = LVL[r][c]
            if ch == " " or (c, r) in taken or (c, r) in gone or (ch == "W" and not wizard):
                continue
            box = pygame.Rect(c * TILE - cam, r * TILE, TILE, TILE)   # every drawn thing
            seen = (c, r) in revealed   # has a pebble told you about this square?
            if ch == "c" and crumb.get((c, r)):
                box = box.move(int(math.sin(frames) * 2), 0)      # about to give way
            lie = seen and ch in LIARS   # revealed, and actually a liar
            if ch in "ox":
                col = TRUTH[ch] if lie else LOOK[ch]   # the one line where a lie becomes
                pygame.draw.circle(scr, col, box.center, 9)
                if lie: pygame.draw.circle(scr, edge(col), box.center, 9, 2)
            elif ch in "^t":
                col = TRUTH[ch] if lie else LOOK[ch]   # the one line where a lie becomes
                pts = [box.bottomleft, (box.centerx, box.top), box.bottomright]
                pygame.draw.polygon(scr, col, pts)
                if lie: pygame.draw.polygon(scr, edge(col), pts, 2)
            elif ch == "W":
                pygame.draw.rect(scr, (160, 80, 220), box.inflate(-8, 0))   # the wizard
            elif ch in "G!":
                pygame.draw.rect(scr, TRUTH["!"] if seen and ch == "!" else (90, 230, 190), box.inflate(-6, -2))
            elif ch == "~":   # drawn only once a pebble has found it
                if seen:
                    pygame.draw.rect(scr, TRUTH["~"], box)
                    pygame.draw.rect(scr, edge(TRUTH["~"]), box, 1)
            else:
                col = TRUTH[ch] if lie else LOOK[ch]   # the one line where a lie becomes
                pygame.draw.rect(scr, col, box)
                pygame.draw.rect(scr, edge(col) if lie else (0, 0, 0), box, 2 if lie else 1)
                if ch == "c":
                    pygame.draw.line(scr, (90, 60, 40), box.topleft, box.center, 1)
    for pb in pebbles:
        pygame.draw.circle(scr, (230, 230, 230), (int(pb[0]) - cam, int(pb[1])), 3)
    pygame.draw.rect(scr, (240, 235, 220), (int(P["x"]) - cam, int(P["y"]), PW, PH), border_radius=4)
    scr.blit(font.render("coins %d" % coins, True, (255, 255, 255)), (10, 10))

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    font = pygame.font.SysFont(None, 24)   # any font the system has, at size 24
    clk = pygame.time.Clock()   # our metronome
    reset()
    while True:   # the game loop
        pressed = False   # true for one frame only
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: reset()
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True
            if e.type == pygame.MOUSEBUTTONDOWN:
                cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))
                throw(e.pos[0] + cam, e.pos[1])   # e.pos is where on screen you clicked; adding
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,
             k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])
        pebble_step()   # move the pebbles once per frame
        draw(scr, font)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
