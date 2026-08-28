"""Trust No One -- step 24: Throwing a pebble.   Run it:  python3 steps/step24.py"""

import sys   # sys is Python's own settings; this game uses
import pygame   # the game library itself

TILE, VW, VH = 32, 960, 640   # TILE is the size of one square, in pixels

# feel knobs, tuned at 60fps
GRAV, SPD, JUMP, MAXFALL = 0.35, 3.6, -9.2, 12   # JUMP is negative because y grows downward
ACC, AIR, FRIC = 0.55, 0.32, 0.72   # how fast you gain speed on the ground
COYOTE, BUFFER, CUT = 7, 8, 0.42     # late jump, early jump, tap = short hop
PW, PH = 20, 28

# honest: '#' brick  'o' coin  '^' spike  'W' wizard  'G' exit  'P' spawn
# lies:   '%' hologram brick
ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces
L1 = [   # the level
    ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW, ROW,
    "                                            o  o            ",
    ROW,
    "                      ####               ######             ",
    "                                      o             o       ",
    " P             W                  ^                      G  ",
    "##########%%%#######    ####################################",
    "##########   #######    ####################################",
]

LIARS = set("%")   # every letter that is not what it looks like

LVL, COLS, ROWS, SPAWN = [], 0, 0, (0, 0)
P = {}
cursed = wizard = False   # two flags
coins = coy = buf = 0
taken, pebbles = set(), []

def load():   # get the level ready to play
    """Measure the level, find the P, then erase it so it is never drawn."""
    global LVL, COLS, ROWS, SPAWN   # change the variables outside this function
    COLS = max(len(r) for r in L1)   # the widest row sets the width of the world
    LVL = [r.ljust(COLS) for r in L1]   # pad every row to that width
    ROWS = len(LVL)   # and the number of rows is the height
    SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")
    LVL = [r.replace("P", " ") for r in LVL]   # then erase it
    taken.clear(); pebbles.clear()
    die()   # back to the start

def reset():   # a whole fresh run
    global cursed, wizard, coins
    cursed, coins = False, 0
    wizard = True
    load()   # build the level before the loop starts

def die():   # back to the start, standing still
    """Back to the start, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0, g=False, jump=False)

def tile(c, r):   # what letter is at column c, row r?
    """What letter is at column c, row r? Off the map counts as empty air."""
    return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "   # off the edge of the map

def solid(ch):   # which letters stop you
    return ch == "#" or (ch == "%" and not cursed)

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

def step(left, right, pressed=False, held=False):   # two new arguments
    global cursed, wizard, coins, coy, buf

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

    if P["y"] > ROWS * TILE:   # fell past the bottom row
        return die()   # back to the start, and nothing else this frame
    for c, rw, ch in cells(prect()):   # every square you are standing in, this frame
        if ch == "^":   # a real spike, which never lied to anybody
            return die()   # back to the start, and nothing else this frame
        elif ch == "o" and (c, rw) not in taken:
            taken.add((c, rw)); coins += 1   # remember it
        elif ch == "W" and wizard:   # touched the wizard
            wizard, cursed = False, True   # he vanishes, and you are cursed

# tx, ty is where you clicked, in world pixels
def throw(tx, ty):
    """Click far away for a hard throw, close for a soft lob."""
    # throw from your middle, not your corner
    cx, cy = P["x"] + PW / 2, P["y"] + PH / 2
    # the arrow from you to the click
    dx, dy = tx - cx, ty - cy
    # its length. ** 0.5 is a square root, and max(1) stops a click on yourself dividing by zero
    d = max(1.0, (dx * dx + dy * dy) ** 0.5)
    # clamped at both ends, so no click is useless and none is absurd
    sp = max(4.5, min(16.0, d / 20.0))        # close click = soft lob, far click = hard throw
    # dx/d is direction alone; times sp is direction with force. Each pebble is [x, y, vx, vy]
    pebbles.append([cx, cy, dx / d * sp, dy / d * sp])


# one frame for every pebble in the air
def pebble_step():
    # the [:] makes a copy, so removing pebbles while looping over them is safe
    for pb in pebbles[:]:
        # pebbles fall too, at half weight
        pb[3] += GRAV * 0.5
        # the same speed-changes-position rule as you
        pb[0] += pb[2]; pb[1] += pb[3]
        c, r = int(pb[0]) // TILE, int(pb[1]) // TILE
        # left the map
        if not (0 <= c < COLS and 0 <= r < ROWS):
            pebbles.remove(pb); continue
        if tile(c, r) != " ":
            pebbles.remove(pb)

LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "^": (170, 170, 180), "o": (240, 200, 60)}

def draw(scr, font):   # draw needs the font now, for the coin counter
    cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))
    scr.fill((25, 25, 35))   # paint over the last frame, or it smears
    for r in range(ROWS):   # every row
        for c in range(cam // TILE, min(COLS, cam // TILE + VW // TILE + 2)):
            ch = LVL[r][c]
            if ch == " " or (c, r) in taken or (ch == "W" and not wizard):
                continue
            box = pygame.Rect(c * TILE - cam, r * TILE, TILE, TILE)   # every drawn thing
            if ch == "o":
                pygame.draw.circle(scr, LOOK[ch], box.center, 9)   # coins are circles, radius 9
            elif ch == "^":
                pygame.draw.polygon(scr, LOOK[ch], [box.bottomleft, (box.centerx, box.top), box.bottomright])
            elif ch == "W":
                pygame.draw.rect(scr, (160, 80, 220), box.inflate(-8, 0))   # the wizard
            elif ch == "G":   # the way out
                pygame.draw.rect(scr, (90, 230, 190), box.inflate(-6, -2))
            else:
                pygame.draw.rect(scr, LOOK[ch], box)   # fill it with the colour for that letter
                pygame.draw.rect(scr, (0, 0, 0), box, 1)   # the last argument is a line width
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
                # centre on the middle of you, then clamp: never below 0, never past the last
                # column. The max and the min are the whole camera
                cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))
                # e.pos is where on screen you clicked; adding cam makes it a place in the level
                throw(e.pos[0] + cam, e.pos[1])
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,
             k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])
        # move the pebbles once per frame, like everything else
        pebble_step()
        draw(scr, font)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
