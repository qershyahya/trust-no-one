"""Trust No One -- step 8: Your box as a Rect.   Run it:  python3 steps/step08.py"""

import pygame   # the game library itself

VW, VH = 960, 640                     # the window, in pixels
TILE = 32                             # one square of the world

PW, PH = 20, 28                       # how big you are
SPD = 3.6                             # top walking speed, pixels per frame
GRAV = 0.35                           # pull per frame
MAXFALL = 12                          # the fastest you may fall

# every tile is one letter: '#' brick  'G' exit  'P' spawn
ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces
L1 = [   # the level
    ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW,
    ROW,
    ROW,
    "                      ####               ######             ",
    ROW,
    " P                                                       G  ",
    "############################################################",
    "############################################################",
]
LEVELS = [L1]                          # the levels, in order: one so far

LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured
level = 0                                             # which level is loaded
SPAWN = (0, 0)                                        # where you start, found by load()
P = {}                                                # where you are, and how fast

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
    load(0)   # the first level

def place():   # stand at the start of the level
    """At the start of the level, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)   # start where the level

def tile(c, r):   # what letter is at column c, row r?
    """What letter is at column c, row r? Off the map counts as empty air."""
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "   # off the edge of the map

# your box, right now, as a Rect
def prect():
    """Your box, right now."""
    # Rect wants whole pixels, so int() drops the fraction
    return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)

def step(left, right):   # one frame of you
    P["vx"] = (right - left) * SPD   # True minus False is 1 minus 0
    P["vy"] = min(P["vy"] + GRAV, MAXFALL)   # add gravity every frame

    P["x"] += P["vx"]
    P["y"] += P["vy"]

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
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d])
        draw(scr)   # one call now does all the drawing
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
