"""Trust No One -- step 53: He walks up and hits him.   Run it:  python3 steps/step53.py"""

import pygame   # the game library itself
import array
import math
import os
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
FALL = 60                             # frames your body takes to come to rest
SHOWN = 30                            # frames a struck square tells the truth
CLEAR = 6                             # frames a stone ignores what it is inside
THROW = 16                            # frames the throwing animation lasts
HIT_FOR, CURSE = 16, 40               # he flinches for one, casts for the other

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
dying, body = 0, [0.0, 0.0, 0.0]   # dying counts down while your body falls; body
beat = 0                                              # the pictures' own clock
face = 1                                              # 1 right, -1 left
throwing = 0   # frames left of the throw animation; while
flash = casting = 0   # frames left of his flinch, and of his spell
COIN = []   # the six pictures of a spinning coin
PLAYER = {}   # her animations by name, each a list of frames
SKY = []   # the two background layers, far and near
TRUE = {}   # what each liar really is, as a picture
FIRE = []   # eight frames of flame
DOOR_OK = []   # the way out, eight frames of it
DOOR_BAD = []   # the same door as it really is
DEMON = []   # what stands in the wrong door
SHOT = []   # the picture of the stone you throw
SMOKE = []   # eight frames of a plume
PUFFS = []   # every plume in the air: where, and how old
KEYS = {}   # the arrow keys
WIZ, WIZ_L = [], []   # him standing, facing right and facing left
HURT, HURT_L = [], []   # him flinching, both ways
CAST, CAST_L = [], []   # him taking your eyes
taken = set()   # which coins you already picked up
pebbles = []   # every stone in the air right now
hit = {}   # squares a stone has struck
gone = set()   # squares that have dropped away
crack = {}   # every cracked brick you have stood on

ART = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art")
PIC = {}   # one picture per letter of the level


def picture(name):   # open one file from the art folder
    """Open a picture. convert_alpha() re-packs it the way the screen wants,
    which makes every later blit far quicker."""
    return pygame.image.load(os.path.join(ART, name)).convert_alpha()


def cut(sheet, n):   # a strip of n frames
    """A strip of n frames, side by side, cut into a list. Each frame is trimmed
    down to the pixels that are actually drawn, so a 150-wide frame with a small
    character in it stops being mostly empty air."""
    wide, out = sheet.get_width() // n, []   # every frame is the same width
    for i in range(n):
        frame = sheet.subsurface((i * wide, 0, wide, sheet.get_height()))
        box = frame.get_bounding_rect()   # the smallest rectangle holding every pixel
        out.append(frame.subsurface(box).copy() if box.width else frame.copy())   # trimmed
    return out


def rimmed(pic, colour=(226, 236, 255)):   # a one-pixel outline
    """A one-pixel rim around a sprite. She is dark olive, the graveyard is nearly
    black, and without this she disappears into it. from_surface() makes a mask --
    which pixels are drawn at all -- and to_surface() paints that shape one colour."""
    w, h = pic.get_size()
    out = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)
    edge = pygame.mask.from_surface(pic).to_surface(setcolor=colour,   # a mask is which pixels
                                                    unsetcolor=(0, 0, 0, 0))
    for dx, dy in ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)):
        out.blit(edge, (dx, dy))    # the shape, eight times, one pixel out each way
    out.blit(pic, (1, 1))           # then the sprite itself, on top
    return out


def facing(frames):   # every frame
    """Every frame, ready to face either way. Built once at the start rather than
    flipped every frame -- flipping is slow, and a game does this sixty times a
    second."""
    return [{1: rimmed(f), -1: rimmed(pygame.transform.flip(f, True, False))}   # and now each
            for f in frames]

def tall(pic, height):   # scale to a height, keeping its shape
    """Scale a picture to a given height, keeping its shape."""
    k = height / pic.get_height()
    return pygame.transform.scale(pic, (max(1, int(pic.get_width() * k)), height))


def fit(pic):   # trim a picture, scale it to one square
    """Trim a picture, scale it to fit one square, and stand it on the floor of that
    square -- so a slime sits on the ground instead of floating in the middle."""
    box = pic.get_bounding_rect()
    pic = pic.subsurface(box).copy() if box.width else pic
    k = min(TILE / pic.get_width(), TILE / pic.get_height())
    pic = pygame.transform.scale(pic, (max(1, int(pic.get_width() * k)),
                                       max(1, int(pic.get_height() * k))))
    out = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    out.blit(pic, ((TILE - pic.get_width()) // 2, TILE - pic.get_height()))
    return out


SWOOSH = {(240, 240, 240), (214, 221, 225)}    # the two colours of the sword arc


def de_swoosh(frames):   # the artist drew a white arc across the throw
    """Her throw frame carries a big white arc that reads as a sword sweep, not a
    throw. Every other frame has about forty near-white pixels; that one has over a
    thousand. So: count them, and if there are too many, rub that colour out."""
    out = []
    for frame in frames:
        frame = frame.copy()
        white = sum(1 for y in range(frame.get_height())
                    for x in range(frame.get_width())
                    if frame.get_at((x, y)).a and frame.get_at((x, y))[:3] in SWOOSH)
        if white > 200:   # forty near-white pixels is a highlight
            for y in range(frame.get_height()):
                for x in range(frame.get_width()):
                    if frame.get_at((x, y)).a and frame.get_at((x, y))[:3] in SWOOSH:
                        frame.set_at((x, y), (0, 0, 0, 0))
            box = frame.get_bounding_rect()   # the smallest rectangle holding every pixel
            frame = frame.subsurface(box).copy() if box.width else frame
        out.append(frame)
    return out


def puff(x, y):   # a plume of smoke: where it is, and how old
    """A plume of smoke, at a point in the world."""
    PUFFS.append([x, y, 0])


def smoke(scr, cam):   # draw every plume and age it
    """Draw every plume and age it. They drift up and are gone in half a second."""
    for p in PUFFS[:]:   # a copy of the list
        p[2] += 1
        i = p[2] // 4
        if i >= len(SMOKE):
            PUFFS.remove(p)
            continue
        pic = SMOKE[i]
        scr.blit(pic, (int(p[0]) - cam - pic.get_width() // 2,
                       int(p[1]) - pic.get_height() - p[2] // 3))

def art():   # every picture
    """Every picture, opened once. Doing this inside draw() would open the same
    files sixty times a second."""
    sheet = picture("tiles.png")   # one file with every tile in it, in a grid
    cell = lambda c, r: sheet.subsurface((c * TILE, r * TILE, TILE, TILE)).copy()
    PIC["#"] = cell(5, 1)                          # the ground: one 32x32 square of it
    PIC["%"] = PIC["~"] = cell(5, 1)               # a lie has to look like the truth
    PIC["c"] = cell(2, 1)
    spike = picture("spikes.png").subsurface((0, 0, 16, 16))
    bed = pygame.Surface((TILE, TILE), pygame.SRCALPHA)   # an empty square with a see-through
    bed.blit(spike, (0, TILE - 16)); bed.blit(spike, (16, TILE - 16))
    PIC["^"] = PIC["t"] = bed                      # two 16-pixel spikes fill a square
    coin = picture("coin_gold.png")
    COIN[:] = [pygame.transform.scale(coin.subsurface((i * 16, 0, 16, 16)), (TILE, TILE))
               for i in range(coin.get_width() // 16)]

    PLAYER["idle"] = facing(cut(picture("player_idle.png"), 8))   # eight frames of standing
    PLAYER["run"] = facing(cut(picture("player_run.png"), 8))
    PLAYER["jump"] = facing(cut(picture("player_jump.png"), 2))
    PLAYER["fall"] = facing(cut(picture("player_fall.png"), 2))

    SKY.append(picture("sky.png"))                    # far away, and slow
    SKY.append(picture("graveyard.png"))              # nearer, and twice as fast

    # what each liar really is. No colour code to learn: you see the thing itself
    TRUE["%"] = cell(8, 8)                         # a hole. There was never a brick
    TRUE["c"] = cell(7, 8)                         # loose rubble
    TRUE["~"] = cell(3, 8)                         # a stone ledge, holding you up
    TRUE["t"] = fit(picture("slime.png").subsurface((0, 0, 24, 24)))
    FIRE[:] = [fit(picture("fire/%d.png" % i)) for i in range(1, 9)]   # eight frames of it
    TRUE["x"] = FIRE                               # a coin that is a fire

    door = picture("portal.png")
    for i in range(door.get_width() // 128):
        one = tall(door.subsurface((i * 128, 0, 128, 128)), TILE * 2)
        DOOR_BAD.append(one)                       # as it is: red, and a way back
        green = one.copy()
        green.fill((70, 255, 190, 255), special_flags=pygame.BLEND_RGBA_MULT)
        DOOR_OK.append(green)                      # as you see it: a way out
    for f in cut(picture("demon_idle.png"), 6):
        DEMON.append(tall(f, 46))                  # what waits in the wrong door

    stone = picture("rocks.png").subsurface((0, 16, 16, 16))
    box = stone.get_bounding_rect()
    SHOT.append(pygame.transform.scale(stone.subsurface(box),
                                       (max(8, box.width // 2), max(8, box.height // 2))))
    PLAYER["throw"] = facing(de_swoosh(cut(picture("player_throw.png"), 5)))
    SMOKE[:] = [tall(picture("smoke/%d.png" % i), 34) for i in range(1, 9)]
    PLAYER["death"] = facing(cut(picture("player_death.png"), 8))

    keys = picture("keys.png")   # every key on a keyboard
    icon = lambda c, r: pygame.transform.scale(   # the same subsurface trick as the tile sheet
        keys.subsurface((c * 16, r * 16, 16, 16)), (32, 32))
    KEYS["left"], KEYS["right"] = icon(13, 13), icon(13, 15)
    KEYS["space"] = icon(9, 8)
    KEYS["click"] = pygame.transform.scale(
        picture("mouse.png").subsurface((16, 48, 16, 16)), (32, 32))

    for sheet_name, count, into, mirror in (("wizard_idle.png", 8, WIZ, WIZ_L),
                                            ("wizard_hurt.png", 4, HURT, HURT_L),
                                            ("wizard_cast.png", 8, CAST, CAST_L)):
        for f in cut(picture(sheet_name), count):
            into.append(f)
            mirror.append(pygame.transform.flip(f, True, False))
    PLAYER["swing"] = facing(cut(picture("player_swing.png"), 5))

# two lines, and then it plays itself
OPEN = [                                       # what you read before anything moves
    "Midnight. A graveyard full of coins nobody came back for.",
    "You came to take them. Someone is already standing on them.",
]
# one word for what the opening is doing; wiz_at is his square, found once the level is loaded
scene, wiz_at = "title", None                  # title -> walk -> hit -> cast -> None


# which square he is standing in -- read out of the level, not written down twice
def find_wizard():
    """Which square he is standing in. Read out of the level, not written down."""
    for r, row in enumerate(LVL):
        c = row.find("W")
        if c >= 0:
            return c, r
    return None


# one frame of the opening. You are not driving
def scene_step():
    """One frame of the opening. You are not driving: her legs run on the game's own
    physics, so she walks at exactly the speed you will walk at."""
    global scene, flash, throwing, face, cursed, wizard, warp, casting
    if flash: flash -= 1                           # his flinch, running out
    if casting: casting -= 1                       # and his spell, running out
    if scene == "walk":
        # her legs on the game's own physics, so she walks at the speed you will walk at
        step(0, 1)                                 # hold right, and nothing else
        # and stopping short means the game's own wizard-touch never fires
        if P["x"] + PW >= wiz_at[0] * TILE - 12:   # close enough to swing
            scene, throwing, face = "hit", THROW, 1
            # the animation is chosen by your speed, and she is not moving any more
            P["vx"] = 0.0                          # stop, or she runs on the spot
    elif scene == "hit":
        throwing -= 1
        if throwing == THROW // 2:
            # halfway through the swing, not at the start of it
            flash = HIT_FOR                        # the moment it lands
            # your swing landing
            beep("hit")
        elif throwing <= 0:
            # the swing is over: he raises his hands
            scene, casting = "cast", CURSE
    elif scene == "cast" and casting <= 0:         # the spell has landed
        scene, cursed, wizard, warp = None, True, False, 26.0


# space or a click. Only the parts you read wait for you
def advance():
    """Space or a click. Only the parts you read wait for you."""
    global scene, wiz_at, casting
    if scene == "title":
        wiz_at = find_wizard()
        scene = "walk" if wiz_at else None

SOUND = {}   # name -> a Sound the mixer can play


TUNES = {                                        # every sound, as notes: (from, to, seconds)
    "jump": [(300, 620, 0.13)],                  # up
    "coin": [(880, 880, 0.05), (1320, 1320, 0.10)],   # two blips, a fifth apart
    "die": [(440, 90, 0.40)],                    # down
    "knock": [(220, 120, 0.09)],                 # a stone landing
    "bounce": [(180, 780, 0.22)],                # a trampoline: longer and higher than a jump
    "fall": [(160, 50, 0.30)],                   # a brick dropping away
    "talk": [(520, 560, 0.05)],                  # one line of the conversation
    "hit": [(140, 60, 0.16)],                    # your swing landing on him
    "curse": [(120, 38, 1.30)],                  # him taking your eyes: long, and all the way down
    "level": [(523, 523, 0.12), (659, 659, 0.12), (784, 784, 0.12)],            # three notes up
    "win": [(523, 523, 0.16), (659, 659, 0.16), (784, 784, 0.16), (1047, 1047, 0.16)],
    "gameover": [(330, 330, 0.30), (262, 262, 0.30), (196, 196, 0.30), (131, 131, 0.30)],
}
VOLUME = {                                       # how loud each one is, 0 to 1: the music sits
    "jump": 0.30, "coin": 0.28, "die": 0.40,     # at 0.30, so a game sound is around that,
    "knock": 0.38, "bounce": 0.36, "fall": 0.36, # a warning above it and a blip below it
    "talk": 0.16, "hit": 0.48, "curse": 0.42,
    "level": 0.30, "win": 0.34, "gameover": 0.34,
    "throw": 0.22, "wind": 0.35,
}


def note(f0, f1, secs, kind="square"):   # build a note from nothing but arithmetic
    """A note that slides from f0 to f1, written out as raw samples. A wave is a number
    that goes up and down; how fast it does that is the pitch. "noise" is no pitch at all:
    a random number every sample, which is what wind and a thrown stone sound like. The
    last line fades it out -- a wave that stops dead is a click in the speaker."""
    rate, out = 22050, array.array("h")   # 22050 samples a second
    total, phase = int(rate * secs), 0.0   # how many samples to write
    for i in range(total):
        phase += 2 * math.pi * (f0 + (f1 - f0) * i / total) / rate   # walk round the circle
        wave = math.sin(phase)   # a smooth wave, between -1 and 1
        if kind == "square":
            wave = 1.0 if wave > 0 else -1.0   # a square wave
        if kind == "noise":   # no pitch at all
            wave = random.uniform(-1.0, 1.0)   # a random number every sample is what a hiss is
        out.append(int(wave * (1.0 - i / total) ** 3 * 8000))   # fade it out as it goes
    return out


def make_sounds():   # every sound in the game
    """Every sound in the game, made of arithmetic. Not one file."""
    try:
        # pygame.init() may already have opened the mixer at its own settings, and a second
        # init() would be ignored. Close it first, so the mixer is told the same rate and
        # channel count note() writes at -- otherwise every sound plays at the wrong pitch.
        pygame.mixer.quit()   # pygame.init() may already have opened
        pygame.mixer.init(22050, -16, 1, 512)   # the same rate note() writes at
    except pygame.error:   # a machine with no sound card should still play
        return                                    # no sound card: play on in silence
    for name, parts in TUNES.items():   # every sound in the table
        tune = array.array("h")
        for f0, f1, secs in parts:
            tune += note(f0, f1, secs)   # the notes, one after another
        SOUND[name] = pygame.mixer.Sound(buffer=tune.tobytes())
    SOUND["throw"] = pygame.mixer.Sound(buffer=note(0, 0, 0.12, "noise").tobytes())
    SOUND["wind"] = pygame.mixer.Sound(buffer=note(0, 0, 2.0, "noise").tobytes())
    for name, sound in SOUND.items():
        sound.set_volume(VOLUME[name])           # so no effect shouts over another
    pygame.mixer.Channel(1).play(SOUND["wind"], loops=-1)   # always blowing; how loud is
    pygame.mixer.Channel(1).set_volume(0.0)                # for gusts() to say, every frame


def beep(name):   # play one, if it exists
    if name in SOUND:
        SOUND[name].play()

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
    global cursed, wizard, lives, over, coins, seed, won, scene, flash, casting, throwing
    seed = random.randrange(1 << 30)   # a new seed per run
    cursed = False   # the curse: not yet
    wizard = True   # he is standing in the level until you touch
    won = False   # the last exit has been reached
    coins = 0   # how many you have taken
    lives = LIVES   # how many you have left, right now
    over = False   # true when the last heart has gone
    scene = "title"                             # a fresh run starts with the story:
    flash = casting = throwing = 0              # you are never here uncursed
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
    beep("die")   # and one that slides down
    if lives <= 0:   # that was the last one
        over = True   # nothing moves again until you ask for a new
        beep("gameover")   # four notes down
        return place()   # put the body down and stop
    body[0], body[1], body[2] = P["x"], P["y"], P["vy"]   # copy yourself into the body
    dying = FALL   # and start the clock


def fall():   # one frame of a body falling
    """Your body drops from wherever it was hit and comes to rest on the first thing
    that will hold it: ground, spikes, a trampoline. Then you are put back."""
    global dying
    dying -= 1
    body[2] = min(body[2] + GRAV, MAXFALL)
    body[1] += body[2]
    r = pygame.Rect(int(body[0]), int(body[1]), PW, PH)
    for _, rw, ch in cells(r):
        if solid(ch) or ch in "^t":   # ground, spikes or a trampoline
            r.bottom = rw * TILE
            body[1], body[2] = float(r.y), 0.0
    if body[1] > ROWS * TILE:   # it fell out of the world
        dying = 0                                 # out of the world: nothing left to watch
    if dying <= 0:   # the body has come to rest
        place()   # back to the start

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
    global cursed, wizard, won, coins, frames, coy, buf, warp, face, throwing
    warp = max(0.0, warp - 0.16)                  # every jolt fades, even on the game over screen
    if over: return                               # the run is finished
    if won: return                                # and so is the game
    if dying:                                     # you are on your way down
        return fall()   # one frame of the fall instead of one frame
    frames += 1

    want = (right - left) * SPD   # the speed you asked for
    a = ACC if P["g"] else AIR   # 0.55 of steering on the ground
    if want:
        P["vx"] += max(-a, min(a, want - P["vx"]))   # move toward the speed you want
    else:
        P["vx"] *= FRIC if P["g"] else 0.96   # let go and you slide to a stop
    P["vx"] += wind() * (1.0 if P["g"] else 2.2)   # gusts shove hardest in the air
    if P["vx"] > 0.4: face = 1                    # you face the way you move
    elif P["vx"] < -0.4: face = -1
    if throwing: throwing -= 1
    coy = COYOTE if P["g"] else coy - 1   # a countdown that refills every time you touch
    buf = BUFFER if pressed else buf - 1   # the same kind of countdown
    if buf > 0 and coy > 0:   # pressed recently AND grounded recently
        P["vy"], buf, coy, P["jump"] = JUMP, 0, 0, True   # jump, spend both credits
        beep("jump")   # a note that slides up
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
            beep("fall")
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
            beep("bounce")   # longer and higher than a jump
        if ch == "x" and cursed:   # once cursed, the killer coin kills
            return die()   # back to the start, and nothing else this frame
        if ch == "!":   # the exit that is not one
            warp = 22.0   # the fake exit
            return die()   # back to the start, and nothing else this frame
        if ch == "o" and (c, rw) not in taken:   # a coin you have not had yet
            taken.add((c, rw)); coins += 1   # remember it
            beep("coin")
        if ch == "x" and (c, rw) not in taken:   # the killer coin still counts
            taken.add((c, rw)); coins += 1   # remember it
            beep("coin")
        if ch == "W" and wizard:
            wizard, cursed = False, True   # he vanishes, and you are cursed
            warp = 26.0                           # the biggest jolt in the game
        if ch == "G":   # the way out
            if level + 1 < len(LEVELS):   # another level to go?
                beep("level")
                return load(level + 1)   # start it, and do nothing else this frame
            won = True   # that was the last one
            beep("win")   # four notes up

def throw(tx, ty):   # tx, ty is where you clicked, in world pixels
    """Click far away for a hard throw, close for a soft lob."""
    global face, throwing
    face = 1 if tx > P["x"] + PW / 2 else -1
    throwing = THROW   # and the animation runs itself down in step()
    beep("throw")   # a tenth of a second of noise
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
            beep("knock")
            puff(pb[0], pb[1] + 6)               # dust off whatever it struck
            pebbles.remove(pb)

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

def pose():   # which frame of her to draw right now
    """The frame of her to draw right now: the newest rule that applies wins."""
    if dying:                                     # she goes down where she fell
        seq = PLAYER["death"]   # the animation the artist drew for it
        return seq[min(len(seq) - 1, (FALL - dying) * len(seq) // (FALL - 12))]
    if throwing > 0:                              # mid-throw, whatever else
        seq = PLAYER["swing"] if scene == "hit" else PLAYER["throw"]
        return seq[min(len(seq) - 1, (THROW - throwing) * len(seq) // THROW)]
    if not P["g"]:
        seq = PLAYER["jump"] if P["vy"] < 0 else PLAYER["fall"]   # going up or coming down
        return seq[(beat // 6) % len(seq)]   # one picture every six frames: ten a second
    if abs(P["vx"]) > 0.6:
        seq = PLAYER["run"]
        return seq[(beat // 6) % len(seq)]   # one picture every six frames: ten a second
    seq = PLAYER["idle"]   # standing still
    return seq[(beat // 6) % len(seq)]   # one picture every six frames: ten a second

def draw(scr, font, big):   # two fonts now
    global beat   # draw() is about to change it
    beat += 1                                     # one tick per frame drawn,
                                                  # even when nothing else moves
    here = P["x"]                                   # what the camera follows
    if dying: here = body[0]                     # the camera stays with your body
    cam = max(0, min(int(here) + PW // 2 - VW // 2, COLS * TILE - VW))   # the camera
    scr.fill(SKY[0].get_at((4, 4)))               # the night, taken from the art
    for layer, slower in ((SKY[0], 4), (SKY[1], 2)):   # the far layer divided by 4
        wide = layer.get_width()
        for x in range(-wide, VW + wide, wide):
            # divide the camera and the far layer drifts slower: that is parallax
            scr.blit(layer, (x - (cam // slower) % wide, VH - layer.get_height()))
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
            pic = COIN[(beat // 6) % len(COIN)] if ch in "ox" else PIC.get(ch)
            if seen and ch in TRUE:                  # for half a second, the truth
                pic = TRUE[ch]
                if isinstance(pic, list):            # and a fire moves
                    pic = pic[(beat // 5) % len(pic)]
            if pic:   # a picture if there is one for this letter
                scr.blit(pic, box)   # blit copies one surface onto another
                continue
            if ch == "W":
                # he turns to face you: everything he does is aimed at where you stand
                at_you = P["x"] + PW / 2 < box.centerx + cam   # are you to his left? Then he
                if casting > 0:                      # taking your eyes
                    seq = CAST_L if at_you else CAST
                    wz = seq[min(len(seq) - 1, (CURSE - casting) * len(seq) // CURSE)]
                elif flash > 0:                      # your swing just landed
                    seq = HURT_L if at_you else HURT
                    wz = seq[min(len(seq) - 1, (HIT_FOR - flash) * len(seq) // HIT_FOR)]
                else:
                    seq = WIZ_L if at_you else WIZ
                    wz = seq[(beat // 8) % len(seq)]
                scr.blit(wz, (box.centerx - wz.get_width() // 2, box.bottom - wz.get_height()))
                continue
            if ch in "G!":   # the way out, and the exit that lies
                fake = ch == "!" and lie
                door = (DOOR_BAD if fake else DOOR_OK)[(beat // 7) % len(DOOR_OK)]
                scr.blit(door, (box.centerx - door.get_width() // 2,
                                box.bottom - door.get_height()))
                if fake:                             # and what is waiting in it
                    dm = DEMON[(beat // 9) % len(DEMON)]
                    scr.blit(dm, (box.centerx - dm.get_width() // 2,
                                  box.bottom - dm.get_height()))
                continue
    for pb in pebbles:
        # turned a little further every frame, so it tumbles instead of pointing
        spun = pygame.transform.rotate(SHOT[0], (pb[0] + pb[1]) * 3 % 360)   # turned by where
        scr.blit(spun, (int(pb[0]) - cam - spun.get_width() // 2,
                        int(pb[1]) - spun.get_height() // 2))
    x, y = int(P["x"]) - cam, int(P["y"])
    if dying:                                     # where you fell, not where you restart
        x, y = int(body[0]) - cam, int(body[1])   # where you fell, not where you restart
    who = pose()[face]   # the frame of her to draw
    scr.blit(who, (x + PW // 2 - who.get_width() // 2, y + PH - who.get_height()))
    smoke(scr, cam)

    if cursed or warp > 0:   # the curse, and every jolt
        gusts(scr)
        wobble(scr, 3.2 + warp * 1.8)
    hud = "%s   %s   coins %d" % (NAMES[level], clock_str(frames), coins)
    for i in range(LIVES):   # one heart per life you started with
        heart(scr, VW - 30 - i * 22, 10, i < lives)   # the ones past lives are drawn dark
    for i, k in enumerate(("left", "right", "space", "click")):   # the keys that do something
        scr.blit(KEYS[k], (10 + i * 36, VH - 42))
    if over:   # the run is finished
        veil = pygame.Surface((VW, VH), pygame.SRCALPHA)   # a surface with an alpha channel
        veil.fill((8, 6, 12, 185))   # near-black, and 185 out of 255 opaque
        scr.blit(veil, (0, 0))
        card = big.render("GAME OVER", True, (240, 120, 130))   # the only red text in the game
        scr.blit(card, card.get_rect(center=(VW // 2, VH // 2 - 20)))
        again = font.render("press space to try again", True, (222, 216, 206))
        scr.blit(again, again.get_rect(center=(VW // 2, VH // 2 + 24)))
        return
    # the story is on: a veil, and the words
    if scene:
        dim = {'title': 165, 'walk': 70, 'hit': 70, 'talk': 120, 'cast': 60}
        # a surface with an alpha channel, so it can be see-through
        veil = pygame.Surface((VW, VH), pygame.SRCALPHA)
        veil.fill((8, 6, 12, dim[scene]))
        scr.blit(veil, (0, 0))
        if scene == "title":
            card = big.render("TRUST NO ONE", True, (232, 226, 210))
            scr.blit(card, card.get_rect(center=(VW // 2, 170)))
            for i, line in enumerate(OPEN):
                t = font.render(line, True, (232, 226, 210))
                scr.blit(t, t.get_rect(center=(VW // 2, 250 + i * 34)))
        if scene in ("title", "talk"):
            go = font.render("press space", True, (150, 140, 130))
            scr.blit(go, go.get_rect(bottomright=(VW - 12, VH - 12)))
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
    if "wind" in SOUND:                           # the hiss follows the gust
        pygame.mixer.Channel(1).set_volume(VOLUME["wind"] * min(1.0, abs(w) / max(GUST)))
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
    art()
    make_sounds()   # build the sounds before the first frame
    reset()   # a whole fresh run
    while True:   # the game loop
        pressed = False   # true for one frame only
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
            if e.type == pygame.KEYDOWN:
                if (over or won) and e.key == pygame.K_SPACE: reset()   # space starts a fresh
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True
                if scene and e.key == pygame.K_SPACE: advance()
            if e.type == pygame.MOUSEBUTTONDOWN and not won and not scene:
                cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))
                throw(e.pos[0] + cam, e.pos[1])   # e.pos is where on screen you clicked; adding
            if e.type == pygame.MOUSEBUTTONDOWN and scene:
                advance()          # a click turns the page of the story
        k = pygame.key.get_pressed()   # which keys are held down right now
        # so the keys do nothing and the world holds still
        if scene:                              # the story is playing
            scene_step()
        else:
            step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d], pressed,
                 k[pygame.K_SPACE] or k[pygame.K_UP] or k[pygame.K_w])
            # move the pebbles once per frame, like everything else
            pebble_step()
        draw(scr, font, big)   # draw() takes both fonts from the day it takes
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
