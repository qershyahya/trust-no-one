"""Trust No One -- step 5: The world is text.   Run it:  python3 steps/step05.py"""

import pygame   # the game library itself

VW, VH = 960, 640                     # the window, in pixels
# one square of the world is 32 pixels; column 5 starts at pixel 160
TILE = 32                             # one square of the world

PW, PH = 20, 28                       # how big you are
SPD = 3.6                             # top walking speed, pixels per frame
GRAV = 0.35                           # pull per frame
MAXFALL = 12                          # the fastest you may fall

# every tile is one letter: '#' brick  'G' exit  'P' spawn
# a name for an empty row, so the thirteen rows of sky above the level do not fill the screen
# with spaces
ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces
# the level: a list of strings, one per row, every row the same width so you can count columns
# straight off it
L1 = [
    ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW,
    ROW,
    ROW,
    "                      ####               ######             ",
    ROW,
    "                                                         G  ",
    "############################################################",
    "############################################################",
]
# the levels, in order. One so far; a function that takes a level number is ready for five
LEVELS = [L1]                          # the levels, in order: one so far

# LVL is the level as a list of strings; COLS and ROWS are its size, worked out by load()
LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured
# which level is loaded: 0 is the first
level = 0                                             # which level is loaded
SPAWN = (64, 288)                                     # where you start
P = {}                                                # where you are, and how fast

# load takes a number now: which level to start
def load(i):
    """Take level i, measure it, find where you start, and stand there."""
    global LVL, COLS, ROWS, level
    level = i
    # the level asked for, as its list of strings
    rows = LEVELS[i]
    COLS = max(len(r) for r in rows)
    # pad every row to the same width, so LVL[r][c] never runs off the end
    LVL = [r.ljust(COLS) for r in rows]
    # and the number of rows is the height
    ROWS = len(LVL)
    # back to the start
    place()

def reset():   # a whole fresh run
    """A whole fresh run: everything back to the beginning."""
    # the first level
    load(0)

def place():   # stand at the start of the level
    """At the start of the level, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)   # start where the level

# what letter is at column c, row r?
def tile(c, r):
    """What letter is at column c, row r? Off the map counts as empty air."""
    # off the edge of the map counts as empty air, so nothing else ever has to check for edges
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "

def step(left, right):   # one frame of you
    P["vx"] = (right - left) * SPD   # True minus False is 1 minus 0
    P["vy"] = min(P["vy"] + GRAV, MAXFALL)   # add gravity every frame

    P["x"] += P["vx"]
    P["y"] += P["vy"]

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
        scr.fill((25, 25, 35))   # paint over the last frame, or it smears
        pygame.draw.rect(scr, (240, 235, 220), (P["x"], P["y"], PW, PH), border_radius=4)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
