"""Trust No One -- step 14: A jump.   Run it:  python3 steps/step14.py"""

import sys   # sys is Python's own settings; this game uses
import pygame   # the game library itself

TILE, VW, VH = 32, 960, 640   # TILE is the size of one square, in pixels

# feel knobs, tuned at 60fps
# JUMP is negative because y grows downward: up is a negative speed
GRAV, SPD, JUMP, MAXFALL = 0.35, 3.6, -9.2, 12
PW, PH = 20, 28

# every tile is one letter: '#' brick  'G' exit  'P' spawn
ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces
L1 = [   # the level
    ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW,
    ROW,
    ROW,
    "                      ####               ######             ",
    ROW,
    " P                                                       G  ",
    "####################    ####################################",
    "####################    ####################################",
]

LVL, COLS, ROWS, SPAWN = [], 0, 0, (0, 0)
P = {}

def load():   # get the level ready to play
    """Measure the level, find the P, then erase it so it is never drawn."""
    global LVL, COLS, ROWS, SPAWN   # change the variables outside this function
    COLS = max(len(r) for r in L1)   # the widest row sets the width of the world
    LVL = [r.ljust(COLS) for r in L1]   # pad every row to that width
    ROWS = len(LVL)   # and the number of rows is the height
    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")
    LVL = [r.replace("P", " ") for r in LVL]   # then erase it
    die()   # back to the start

def die():   # back to the start, standing still
    """Back to the start, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0, g=False, jump=False)

def tile(c, r):   # what letter is at column c, row r?
    """What letter is at column c, row r? Off the map counts as empty air."""
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "   # off the edge of the map

def solid(ch):   # which letters stop you
    return ch == "#"

def prect():   # your box, right now, as a Rect
    """Your box, right now."""
    return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)   # Rect wants whole pixels

def cells(rect):   # every tile a box overlaps
    """Every tile this box overlaps -- usually two to six of them."""
    for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):   # the -1 means touching
        for c in range(rect.left // TILE, (rect.right - 1) // TILE + 1):
            ch = tile(c, r)
            if ch != " ":
                yield c, r, ch   # hand them back one at a time as the loop asks

# two new arguments: pressed is the frame the button went down, held is whether it is still down
def step(left, right, pressed=False, held=False):
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
        die()   # back to the start

LOOK = {"#": (150, 110, 70), "G": (90, 230, 190)}

def draw(scr):   # everything you see
    scr.fill((25, 25, 35))   # paint over the last frame, or it smears
    for r in range(ROWS):   # every row
        for c in range(COLS):   # ...every column
            ch = LVL[r][c]
            if ch == " ":
                continue
            box = pygame.Rect(c * TILE, r * TILE, TILE, TILE)   # grid to pixels
            pygame.draw.rect(scr, LOOK[ch], box)   # fill it with the colour for that letter
            pygame.draw.rect(scr, (0, 0, 0), box, 1)   # the last argument is a line width
    you = (120, 240, 190) if P["g"] else (240, 235, 220)   # green while you are on the ground
    pygame.draw.rect(scr, you, (int(P["x"]), int(P["y"]), PW, PH), border_radius=4)

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    clk = pygame.time.Clock()   # our metronome
    load()   # build the level before the loop starts
    while True:   # the game loop
        # true for one frame only: the frame the key goes down
        pressed = False
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
            if e.type == pygame.KEYDOWN:
                # R rebuilds the level and puts you back at the start
                if e.key == pygame.K_r: load()
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
