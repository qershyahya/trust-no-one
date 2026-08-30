"""Trust No One -- step 20: Coins.   Run it:  python3 steps/step20.py"""

import pygame   # the game library itself

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
LIVES = 5                             # how many you start with

# every tile is one letter: '#' brick  'o' coin  'G' exit  'P' spawn
ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces
L1 = [   # the level
    ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW,
    "                                            o  o            ",
    ROW,
    "                      ####               ######             ",
    "        #                             o             o       ",
    " P      #                                                G  ",
    "####  ##############    ####################################",
    "####  ##############    ####################################",
]
LEVELS = [L1]                          # the levels, in order: one so far

LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured
level = 0                                             # which level is loaded
SPAWN = (0, 0)                                        # where you start, found by load()
P = {}                                                # where you are, and how fast
# how many you have taken
coins = 0
coy = 0   # coyote frames left
buf = 0   # frames since the jump key went down
lives = LIVES   # how many you have left, right now
over = False                                          # the run is finished
# which coins you already picked up, as (column, row) pairs. A set cannot hold the same one
# twice
taken = set()

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
    # a fresh level has all its coins
    taken.clear()
    place()   # back to the start

def reset():   # a whole fresh run
    """A whole fresh run: everything back to the beginning."""
    global lives, over, coins
    # how many you have taken
    coins = 0
    lives = LIVES   # how many you have left, right now
    over = False   # true when the last heart has gone
    load(0)   # the first level

def place():   # stand at the start of the level
    """At the start of the level, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)   # start where the level
    P["g"] = False   # not on the ground, until step() says so
    P["jump"] = False   # not mid-jump


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

def step(left, right, pressed=False, held=False):   # two new arguments
    global coins, coy, buf
    if over: return                               # the run is finished

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
        P["vy"], P["jump"] = JUMP * CUT, False    # let go early, hop short
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

    if P["y"] > ROWS * TILE:   # fell past the bottom row
        return die()   # back to the start, and nothing else this frame
    # every square you are standing in, this frame
    for c, rw, ch in cells(prect()):
        # a coin you have not had yet
        if ch == "o" and (c, rw) not in taken:
            # remember it, so it is neither drawn nor counted again
            taken.add((c, rw)); coins += 1

LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "c": (150, 110, 70),
        "^": (170, 170, 180), "t": (170, 170, 180), "o": (240, 200, 60), "x": (240, 200, 60)}

# a heart, drawn rather than loaded: two circles and a triangle
def heart(scr, x, y, full):
    """A small heart: two lobes and a point. Cheaper than a picture, and it never
    goes missing."""
    col = (222, 70, 90) if full else (70, 60, 66)
    pygame.draw.circle(scr, col, (x + 4, y + 4), 4)
    pygame.draw.circle(scr, col, (x + 11, y + 4), 4)
    pygame.draw.polygon(scr, col, [(x, y + 5), (x + 15, y + 5), (x + 7, y + 15)])

# two fonts now: small for the bar, big for the message
def draw(scr, font, big):
    here = P["x"]                                   # what the camera follows
    cam = max(0, min(int(here) + PW // 2 - VW // 2, COLS * TILE - VW))   # the camera
    scr.fill((25, 25, 35))   # paint over the last frame, or it smears
    for r in range(ROWS):   # every row
        for c in range(cam // TILE, min(COLS, cam // TILE + VW // TILE + 2)):
            ch = LVL[r][c]
            if ch == " ":   # air: nothing to draw
                continue
            # a coin you took is not drawn
            if (c, r) in taken:
                continue
            box = pygame.Rect(c * TILE - cam, r * TILE, TILE, TILE)   # every drawn thing
            # coins, honest and not: the same circle for both, on purpose
            if ch in "ox":
                # the colour this letter is drawn in
                col = LOOK[ch]
                pygame.draw.circle(scr, col, box.center, 9)
                continue
            # the way out, and the exit that lies: the same green rectangle for both
            if ch in "G!":
                # exit green
                col = (90, 230, 190)
                pygame.draw.rect(scr, col, box.inflate(-6, -2))
                continue
            if ch in "#%~c":
                col = LOOK[ch]   # the colour this letter is drawn in
                pygame.draw.rect(scr, col, box)
                pygame.draw.rect(scr, (0, 0, 0), box, 1)   # the last argument is a line width
                continue
    x, y = int(P["x"]) - cam, int(P["y"])
    pygame.draw.rect(scr, (240, 235, 220), (x, y, PW, PH), border_radius=4)
    # the words along the top: one number, for now
    hud = "coins %d" % coins
    # one heart per life you started with
    for i in range(LIVES):
        # the ones past lives are drawn dark, so you can see what you lost
        heart(scr, VW - 30 - i * 22, 10, i < lives)
    # the run is finished: a card over everything, and draw stops here
    if over:
        # a surface with an alpha channel, so it can be see-through
        veil = pygame.Surface((VW, VH), pygame.SRCALPHA)
        # near-black, and 185 out of 255 opaque: the graveyard still shows underneath
        veil.fill((8, 6, 12, 185))
        scr.blit(veil, (0, 0))
        # the only red text in the game
        card = big.render("GAME OVER", True, (240, 120, 130))
        scr.blit(card, card.get_rect(center=(VW // 2, VH // 2 - 20)))
        # the only thing left to do
        again = font.render("press space to try again", True, (222, 216, 206))
        scr.blit(again, again.get_rect(center=(VW // 2, VH // 2 + 24)))
        return
    scr.blit(font.render(hud, True, (255, 255, 255)), (10, 10))

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    # two sizes: one for the bar, one for the message in the middle
    font, big = pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 30)
    clk = pygame.time.Clock()   # our metronome
    reset()   # a whole fresh run
    while True:   # the game loop
        pressed = False   # true for one frame only
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
            if e.type == pygame.KEYDOWN:
                if over and e.key == pygame.K_SPACE: reset()   # space on the game over screen
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,
             k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])
        # draw() takes both fonts from the day it takes any
        draw(scr, font, big)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
