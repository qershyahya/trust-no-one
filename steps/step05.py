"""Trust No One -- step 5: The world is text.   Run it:  python3 steps/step05.py"""

import sys   # sys is Python's own settings; this game uses
import pygame   # the game library itself

# TILE is the size of one square, in pixels. 960 / 32 = 30 squares across the window
TILE, VW, VH = 32, 960, 640

SPD = 3.6                             # top walking speed, pixels per frame
GRAV, MAXFALL = 0.35, 12              # pull per frame, and the fastest you may fall
PW, PH = 20, 28                       # how big you are

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

LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured
P = {"x": 64.0, "y": 288.0, "vx": 0.0, "vy": 0.0}     # where you are, and how fast

# get the level ready to play
def load():
    """Pad every row to the same width, so LVL[r][c] never runs off the end."""
    # change the variables outside this function instead of making new ones inside it
    global LVL, COLS, ROWS
    # the widest row sets the width of the world
    COLS = max(len(r) for r in L1)
    # pad every row to that width, so LVL[r][c] never runs off the end
    LVL = [r.ljust(COLS) for r in L1]
    # and the number of rows is the height
    ROWS = len(LVL)

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
    # build the level before the loop starts
    load()
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
