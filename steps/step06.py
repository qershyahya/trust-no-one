"""Trust No One -- step 6: Drawing the world.   Run it:  python3 steps/step06.py"""

import sys   # sys is Python's own settings; this game uses
import pygame   # the game library itself

TILE, VW, VH = 32, 960, 640   # TILE is the size of one square, in pixels

SPD = 3.6                             # top walking speed, pixels per frame
GRAV, MAXFALL = 0.35, 12              # pull per frame, and the fastest you may fall
PW, PH = 20, 28                       # how big you are

# every tile is one letter: '#' brick  'G' exit  'P' spawn
ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces
L1 = [   # the level
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

def load():   # get the level ready to play
    """Pad every row to the same width, so LVL[r][c] never runs off the end."""
    global LVL, COLS, ROWS   # change the variables outside this function
    COLS = max(len(r) for r in L1)   # the widest row sets the width of the world
    LVL = [r.ljust(COLS) for r in L1]   # pad every row to that width
    ROWS = len(LVL)   # and the number of rows is the height

def tile(c, r):   # what letter is at column c, row r?
    """What letter is at column c, row r? Off the map counts as empty air."""
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "   # off the edge of the map

def step(left, right):   # one frame of you
    P["vx"] = (right - left) * SPD   # True minus False is 1 minus 0
    P["vy"] = min(P["vy"] + GRAV, MAXFALL)   # add gravity every frame

    P["x"] += P["vx"]
    P["y"] += P["vy"]

# letter to colour. The entire art department
LOOK = {"#": (150, 110, 70), "G": (90, 230, 190)}

# everything you see, rebuilt from nothing every frame
def draw(scr):
    # paint over the last frame, or it smears. The three numbers are red, green, blue
    scr.fill((25, 25, 35))
    # every row...
    for r in range(ROWS):
        # ...every column
        for c in range(COLS):
            ch = LVL[r][c]
            if ch == " ":
                continue
            # grid to pixels: where that square lands on screen
            box = pygame.Rect(c * TILE, r * TILE, TILE, TILE)
            # fill it with the colour for that letter
            pygame.draw.rect(scr, LOOK[ch], box)
            # the last argument is a line width, so this draws only the outline
            pygame.draw.rect(scr, (0, 0, 0), box, 1)
    pygame.draw.rect(scr, (240, 235, 220), (int(P["x"]), int(P["y"]), PW, PH), border_radius=4)

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    clk = pygame.time.Clock()   # our metronome
    load()   # build the level before the loop starts
    while True:   # the game loop
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d])
        # one call now does all the drawing
        draw(scr)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
