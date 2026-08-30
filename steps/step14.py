"""Trust No One -- step 14: A jump.   Run it:  python3 steps/step14.py"""

import pygame   # the game library itself

VW, VH = 960, 640                     # the window, in pixels
TILE = 32                             # one square of the world

PW, PH = 20, 28                       # how big you are
SPD = 3.6                             # top walking speed, pixels per frame
GRAV = 0.35                           # pull per frame
MAXFALL = 12                          # the fastest you may fall
# up is negative. The kick you get on the frame you press
JUMP = -9.2                           # the kick upward, pixels per frame
LIVES = 5                             # how many you start with

# every tile is one letter: '#' brick  'G' exit  'P' spawn
ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces
L1 = [   # the level
    ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW,
    ROW,
    ROW,
    "                      ####               ######             ",
    "        #                                                   ",
    " P      #                                                G  ",
    "####  ##############    ####################################",
    "####  ##############    ####################################",
]
LEVELS = [L1]                          # the levels, in order: one so far

LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured
level = 0                                             # which level is loaded
SPAWN = (0, 0)                                        # where you start, found by load()
P = {}                                                # where you are, and how fast
lives = LIVES   # how many you have left, right now
over = False                                          # the run is finished

def load(i):   # load takes a number now: which level to start
    """Take level i, measure it, find where you start, and stand there."""
    global LVL, COLS, ROWS, level, SPAWN
    level = i
    rows = LEVELS[i]   # the level asked for, as its list of strings
    COLS = max(len(r) for r in rows)
    LVL = [r.ljust(COLS) for r in rows]   # pad every row to the same width
    ROWS = len(LVL)   # and the number of rows is the height
    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")
    LVL = [r.replace("P", " ") for r in LVL]   # then erase it
    place()   # back to the start

def reset():   # a whole fresh run
    """A whole fresh run: everything back to the beginning."""
    global lives, over
    lives = LIVES   # how many you have left, right now
    over = False   # true when the last heart has gone
    load(0)   # the first level

def place():   # stand at the start of the level
    """At the start of the level, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)   # start where the level
    P["g"] = False   # not on the ground, until step() says so
    # not mid-jump
    P["jump"] = False


def die():   # back to the start, standing still
    """Being killed. It costs a life, and the last one ends the run."""
    global lives, over
    lives -= 1   # one heart, spent
    if lives <= 0:   # that was the last one
        over = True   # nothing moves again until you ask for a new
        return place()   # put the body down and stop
    place()   # back to the start

def tile(c, r):   # what letter is at column c, row r?
    """What letter is at column c, row r? Off the map counts as empty air."""
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "   # off the edge of the map

def solid(ch):   # which letters stop you
    """Which letters stop you. Floor you cannot see and bricks that crumble are floor;
    a hologram is floor only until you are cursed."""
    return ch in "#~c"

def prect():   # your box, right now, as a Rect
    """Your box, right now."""
    return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)   # Rect wants whole pixels

def cells(rect):   # every tile a box overlaps
    """Every tile this box overlaps -- usually two to six of them."""
    for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):   # the -1 means touching
        for c in range(rect.left // TILE, (rect.right - 1) // TILE + 1):
            ch = tile(c, r)   # what is written in the square it has reached
            if ch != " ":
                yield c, r, ch   # hand them back one at a time as the loop asks

# two new arguments: pressed is the frame the button went down, held is whether it is still down
def step(left, right, pressed=False, held=False):
    if over: return                               # the run is finished

    P["vx"] = (right - left) * SPD   # True minus False is 1 minus 0
    # on the ground, and the button went down this exact frame
    if pressed and P["g"]:
        # the whole jump. Everything after this step is about when it is allowed
        P["vy"] = JUMP
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

    if P["y"] > ROWS * TILE:   # fell past the bottom row
        return die()   # back to the start, and nothing else this frame

LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "c": (150, 110, 70),
        "^": (170, 170, 180), "t": (170, 170, 180), "o": (240, 200, 60), "x": (240, 200, 60)}

def draw(scr):   # everything you see
    scr.fill((25, 25, 35))   # paint over the last frame, or it smears
    for r in range(ROWS):   # every row
        for c in range(COLS):   # ...every column
            ch = LVL[r][c]
            if ch == " ":   # air: nothing to draw
                continue
            box = pygame.Rect(c * TILE, r * TILE, TILE, TILE)   # grid to pixels
            if ch in "#%~c":
                col = LOOK[ch]   # the colour this letter is drawn in
                pygame.draw.rect(scr, col, box)
                pygame.draw.rect(scr, (0, 0, 0), box, 1)   # the last argument is a line width
                continue
    x, y = int(P["x"]), int(P["y"])   # where you are, as whole pixels
    pygame.draw.rect(scr, (240, 235, 220), (x, y, PW, PH), border_radius=4)

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    clk = pygame.time.Clock()   # our metronome
    reset()   # a whole fresh run
    while True:   # the game loop
        # true for one frame only: the frame the key goes down
        pressed = False
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
            if e.type == pygame.KEYDOWN:
                if over and e.key == pygame.K_SPACE: reset()   # space on the game over screen
                # KEYDOWN fires once, which is exactly what a jump needs
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,
             k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])
        draw(scr)   # one call now does all the drawing
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
