"""What the lesson says: the prose for each step, the note on each new line, and
the hover hint for every name in the code.

Kept apart from main.py so the lesson server stays readable.
"""

# ------------------------------------------------------------------ the steps
# title comes from build_steps.TITLES, so it is never written down twice.

STEP_TEXT = {
1: dict(why="Before any game, one thing: a rectangle that does not close. A game is a <b>loop</b> -- read what happened, move things, draw, wait, repeat, sixty times a second. One trip round that loop is a <b>frame</b>, and every number in this whole game is measured in frames.",
    trial="Nothing moves, and that is correct. A window running sixty times a second with nothing in it is already a game."),
2: dict(why="You are four numbers in a <b>dictionary</b> -- a labelled bag of values, written <code>{\"x\": 64.0}</code> and read back as <code>P[\"x\"]</code>. Not a sprite, not a character: <b>where you are</b> and <b>how fast you are going</b>.",
    trial="A box, sitting still, drawn fresh sixty times a second. Nothing reads vx and vy yet."),
3: dict(why="Keys set the speed; the speed moves the position. Never move x straight from a key -- everything later (gravity, wind, being pushed out of a wall) works by changing a speed, and none of it could touch you if the key wrote your position directly.",
    trial="Hold an arrow and you move; let go and you stop dead on that same frame. Sliding comes at step 18."),
4: dict(why="Gravity is not a fall. It is one number added to <b>vy</b> every frame, so falling gets faster the longer it lasts -- exactly like the real thing. <b>MAXFALL</b> caps it: uncapped, a long fall would cover a whole tile per frame and pass straight through a floor.",
    trial="You drop, and you keep dropping. There is no floor yet, and nothing to catch you -- use the restart button."),
5: dict(why="The level is not a picture. It is <b>text</b>: one letter per 32x32 square, which is what <code>TILE</code> means. Every row is one string of the same width, so you can count columns straight off the page. <code>ROW</code> is just an empty one, so the sky is not thirteen lines of spaces.",
    trial="Nothing has changed on screen -- the level exists as data and nothing draws it yet. Read it in the code instead: that is the whole map."),
6: dict(why="Two loops and a lookup. Walk every row, walk every column, and paint a square in the colour that letter means. <code>//</code> is division that throws the remainder away, so pixel 100 is column 3.",
    trial="The world appears -- and you fall straight through it. Drawing a brick is not the same as touching one."),
7: dict(why="The <code>P</code> in the level says where you start. <code>load()</code> finds it once, remembers it as <code>SPAWN</code>, then erases it, so the letter is never drawn or stood on. Your position now comes from the level, not from numbers typed in the file.",
    trial="You start on the left where the P was, and still fall through everything."),
8: dict(why="A <code>Rect</code> is pygame's box: left, top, width, height. It reports its own edges -- <code>.right</code>, <code>.bottom</code>, <code>.center</code> -- and that is what makes pushing out of a wall two lines instead of ten.",
    trial="Still no collision. This step only gives the next two steps something to ask questions about."),
9: dict(why="Which squares is that box sitting in? Divide its edges by <code>TILE</code> and you get a small range of rows and columns -- usually two to six squares. <code>yield</code> hands them back one at a time as the loop asks, instead of building a list.",
    trial="Nothing visible yet. Everything that touches the world -- walls, coins, spikes, the wizard -- goes through this one function."),
10: dict(why="The trick that makes collision easy: <b>move on one axis, fix that axis, then do the other</b>. Move both at once and you cannot tell whether you hit a wall or a floor. Here is the sideways half: move x, then for every solid square you now overlap, snap your edge to its face and kill your speed.",
    trial="Walls stop you now -- but you still sink through the floor, because nothing has fixed y yet."),
11: dict(why="The same three lines again, downward. Falling means your <b>bottom</b> lands on the brick's top; rising means your <b>top</b> hits its underside. That is the entire difference between the two passes.",
    trial="You land. Walk into the floor's edge and you stop; jump is not built yet, so there is nowhere to go but along."),
12: dict(why="Fall past the bottom row and nothing below will ever catch you, so the game has to notice and put you back. <code>die()</code> resets every one of your numbers, not just position -- leftover speed is a classic bug.",
    trial="Walk off the end of the floor. You fall, and a moment later you are back at the start."),
13: dict(why="The wrong way is to remember \"I hit something\". The right way is a question asked fresh every frame: <b>is anything solid one pixel below me?</b> One line, never out of date, nothing to keep in sync. The box goes green while the answer is yes -- that is only so you can see it, and step 19 takes it away again.",
    trial="Walk off the ledge and watch the green vanish the instant you leave it, before you have visibly dropped."),
14: dict(why="One line: set <code>vy</code> to <code>JUMP</code>, which is -9.2. Negative, because screen y grows downward. <code>pressed</code> is true only on the frame the key goes down, which is why it comes from <code>KEYDOWN</code> and not from the held-keys list.",
    trial="Space jumps -- but only if you are exactly on the ground on exactly that frame. Try jumping the moment you run off the ledge and it will refuse. The next three steps are about that refusal."),
15: dict(why="Run off a ledge and press jump one frame too late and the game says no, while your eyes say you were still on the edge. <b>Coyote time</b> is a countdown that refills whenever you touch ground: for 7 frames after leaving it, a jump still works.",
    trial="Run off the ledge and jump late, on purpose. It works now. Seven frames is a tenth of a second -- nobody notices it, they just stop feeling cheated."),
16: dict(why="The opposite mistake: pressing jump a few frames before you land. <b>Buffer</b> remembers the press for 8 frames, so if you touch the ground while it is still remembered, you jump immediately instead of being ignored.",
    trial="Land and press jump slightly early. Instead of nothing, you bounce straight off on the landing frame."),
17: dict(why="Same button, two heights. If you let go while still rising fast, the rise is cut to 42% -- a tap becomes a hop, a hold becomes a full jump. One line, and it is most of what makes a platformer feel good.",
    trial="Tap Space, then hold Space. Two clearly different jumps, from one key."),
18: dict(why="Until now the key set your speed outright. Now it sets the speed you <b>want</b>, and you steer toward it -- quickly on the ground (<code>ACC</code>), slowly in the air (<code>AIR</code>) -- and slide to a stop with <code>FRIC</code> when you let go. This is where momentum comes from, and why mid-air control feels different from running.",
    trial="Run and let go: you keep sliding. Jump and try to turn around mid-air: you can, but slowly."),
19: dict(why="The camera does not move the world. It is one number: how far left everything gets drawn. Centre it on you, then <b>clamp</b> it with a max and a min so you never see past either end of the level.",
    trial="Walk right. The level used to run off the edge of the screen; now the world slides, and stops cleanly at both ends."),
20: dict(why="The first thing in the world that reacts to you. Every frame, look at the squares you overlap; if one is a coin you have not taken, add it to <code>taken</code> and count it. <code>taken</code> is a <b>set</b>, so a coin cannot be collected twice, and the drawing code skips anything in it.",
    trial="Walk over a coin. It disappears and the number top-left goes up. Walk back over the same square: nothing."),
21: dict(why="The same loop, one more letter, and the first thing that can kill you. A spike is drawn as a triangle and calls <code>die()</code> the moment you touch it. Nothing about it is a lie -- yet.",
    trial="Walk into the spike on purpose. Back to the start."),
22: dict(why="Here is the whole game, in one flag. Touch the wizard once and <code>cursed</code> becomes true; he vanishes and never comes back. Nothing else changes yet -- the flag is set and nothing reads it. The next step is what makes it matter.",
    trial="Walk into the purple block. It disappears, and everything looks exactly the same. That is on purpose."),
23: dict(why="<code>solid()</code> stops being about the letter and becomes about the letter <b>and whether you are cursed</b>. The three <code>%</code> tiles bridge a hole in the floor: a hologram that holds you up perfectly, right up until you know better.",
    trial="Cross the bridge over the hole before touching the wizard -- it holds. Then take the curse and step on it again. The level text never changed; only your reading of it did."),
24: dict(why="A curse with no counter-move is unfair, so you get a pebble. Click, and one flies from your middle toward the click, falling as it goes. Distance sets the strength: near click, gentle lob; far click, hard throw.",
    trial="Click near you, then far away. The pebbles land, and so far that is all they do."),
25: dict(why="Now the pebble earns its place. Wherever it hits, that square and the eight around it go into <code>revealed</code>, and from then on a liar is drawn in its true colour -- the same hue, gone dull. Honest tiles look identical either way, so a reveal never wastes your attention.",
    trial="Get cursed, then hit the bridge with a pebble from a distance. It turns dull brown: the hologram admitting it."),
26: dict(why="The first lie that helps you. <code>t</code> is drawn exactly like a spike, and before the curse it kills exactly like one. Once you can see, it is a trampoline that throws you higher than you can jump -- <code>BOUNCE</code> is -12.3 against your jump's -9.2.",
    trial="Fall into the pit before the curse: you die. Get cursed, fall in again: you are fired back out."),
27: dict(why="And the first lie that hurts. <code>x</code> is drawn as a coin and counts as one -- until you are cursed, and then touching it kills you. The truth is worse than the illusion, which is the joke of the whole game.",
    trial="Take the coin above the bridge before the curse. Then get cursed and try the same square."),
28: dict(why="<code>~</code> is solid and simply never drawn. It is not invisible because of a bug -- <code>solid()</code> counts it, and the drawing code skips it unless a pebble has found it.",
    trial="Walk right past the bridge and over the gap in the floor that is not a gap. Then throw a pebble at it to see the shape you are standing on."),
29: dict(why="Floor with a timer. While you stand on a <code>c</code>, a counter for that exact square goes up; past <code>CRUMB</code> frames -- 26, a bit under half a second -- the square goes into <code>gone</code>, and gone squares are neither drawn nor solid. It shakes for the last few frames so you get a warning.",
    trial="Stand still on the cracked stretch and count. Then try crossing it without stopping."),
30: dict(why="The cruellest letter. <code>!</code> is drawn as the green exit, and touching it sends you back to the start. A pebble tells them apart before you commit to the run.",
    trial="Touch the exit halfway along the level. Then throw a pebble at the one at the far right to check it before you walk into it."),
31: dict(why="If the traps sit in the same squares every run, the game is memorised in two goes. So <code>?</code> means spike-or-trampoline and <code>&amp;</code> means brick-or-hologram, rolled fresh each run from a <b>seed</b> -- one starting number that makes the dice repeatable when you need to re-open a bug.",
    trial="Press R a few times. Nothing looks different -- a spike and a trampoline are drawn the same, and so are a brick and a hologram -- but the floor is not the same floor."),
32: dict(why="The danger with dice: a run of <code>?</code> could come up all spikes, or a run of <code>&amp;</code> all hologram over a hole, and the level would be impossible. Two lines fix it forever: if the run contains nothing safe, force one square back to safe. Step 37's robot checks this across twelve seeds and five levels.",
    trial="Press R a lot. Every roll leaves a way through, whether or not you can see which square it is."),
33: dict(why="Five string-lists in a list, and <code>load(i)</code> is now the only thing that knows how to start one: measure it, roll its dice, find the P, wipe the last level's coins and rubble, drop you at the spawn. Touching <code>G</code> calls it with the next number. Level I goes back to being the real one from the finished game.",
    trial="Reach the green exit. Level II starts, with its own lie: the floor there is threaded with holograms."),
34: dict(why="The bar along the top -- which level, how long you have been on it, coins, total time -- and the line under it that tells a first-time player what the pebble is for. <code>clock_str</code> turns frames into minutes and seconds: 60 frames is a second.",
    trial="Watch the clock while you play. Finish the last level and the message changes."),
35: dict(why="<code>GUST</code> holds one number per level, and <code>sin</code> of the frame count rocks smoothly between -1 and 1 forever -- so the wind swings around instead of shoving one way. It pushes 2.2 times harder in the air, where you have no grip.",
    trial="The first two entries in GUST are 0.0, so levels I and II are calm on purpose. To feel it now: change that first 0.0 to 0.14 in the file, save, press R, and stand perfectly still."),
36: dict(why="The curse bending what you <b>see</b>. Every frame is photographed, cut into 5-pixel bands, and each band pasted back shifted by a different amount. <code>warp</code> is a number that spikes on a shock and fades -- so a death is a small wobble and meeting the wizard tears the screen.",
    trial="Get cursed and watch the whole picture breathe. Nothing about the level actually moved: throw a pebble and it still lands where the bricks really are."),
37: dict(why="You cannot hand-test twelve dice rolls across five levels before a jam deadline. So <code>step()</code> is called with fake key presses and the answers checked with <code>assert</code> -- a line that does nothing when it is right and stops the program when it is wrong. No window, no waiting.",
    trial="This is the finished game -- <code>steps/step37.py</code> is the whole thing. In a terminal: <code>python3 steps/step37.py --test</code> -- pygame prints a line or two of its own, then <b>ok</b>."),
}


# ------------------------------------------------------------------ line notes
# Keys are the exact line, stripped. Prefix "N:" to mean "only at step N" -- the
# same line can mean different things at different steps.

NOTES = {
    # step 1
    "import pygame": "the game library itself",
    "import sys": "sys is Python's own settings; this game uses it once, in step 37, to read what you typed after the filename",
    "def main():": "the whole game lives in here: set up once, then loop forever",
    "VW, VH = 960, 640": "the window, in pixels",
    "pygame.init()": "wake the library up",
    "scr = pygame.display.set_mode((VW, VH))": "make the window. scr is the surface everything gets drawn onto",
    'pygame.display.set_caption("Trust No One")': "the title on the window bar, when you run the file yourself",
    "clk = pygame.time.Clock()": "our metronome",
    "while True:": "the game loop. Forever, until we quit",
    "for e in pygame.event.get():": "everything that happened since the last frame: keys, clicks, the window closing",
    "if e.type == pygame.QUIT:": "the X button on the window",
    "1:return": "leave main(), which ends the program",
    "scr.fill((25, 25, 35))": "paint over the last frame, or it smears. The three numbers are red, green, blue",
    "pygame.display.flip()": "show the frame you just drew",
    "clk.tick(60)": "sleep so the loop runs 60 times a second, not 4000",
    'if __name__ == "__main__":': "run the game when you run this file, and stay quiet if another program loads it",
    "main()": "start it",
    '(test if "--test" in sys.argv else main)()': "run the robot if you asked for it on the command line, otherwise play",

    # step 2
    'P = {"x": 64.0, "y": 288.0, "vx": 0.0, "vy": 0.0}     # where you are, and how fast': "a dictionary: four numbers, each with a name. x and y are where; vx and vy are how fast, per frame",
    "PW, PH = 20, 28                       # how big you are": "player width and height, in pixels. Smaller than a 32-pixel tile, on purpose",
    'pygame.draw.rect(scr, (240, 235, 220), (P["x"], P["y"], PW, PH), border_radius=4)': "you are an off-white rectangle. That is enough to start",

    # step 3
    "SPD = 3.6                             # top walking speed, pixels per frame": "3.6 x 60 frames = 216 pixels a second",
    "def step(left, right):": "one frame of you. Called once per trip round the loop",
    'P["vx"] = (right - left) * SPD': "True minus False is 1 minus 0. Hold both and they cancel to 0, which is right",
    '3:P["x"] += P["vx"]': "speed changes position. This one line is movement",
    "k = pygame.key.get_pressed()": "which keys are held down right now, as opposed to just pressed",
    "step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d])": "arrows or A and D, either way",

    # step 4
    "GRAV, MAXFALL = 0.35, 12              # pull per frame, and the fastest you may fall": "0.35 looks like nothing until it has been added sixty times a second",
    'P["vy"] = min(P["vy"] + GRAV, MAXFALL)': "add gravity every frame, but never let falling pass 12 pixels a frame",
    '4:P["y"] += P["vy"]': "the same trick as x: speed changes position",

    # step 5
    'ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces': "a name for an empty row, so the thirteen rows of sky above the level do not fill the screen with spaces",
    "L1 = [": "the level: a list of strings, one per row, every row the same width so you can count columns straight off it",
    "TILE, VW, VH = 32, 960, 640": "TILE is the size of one square, in pixels. 960 / 32 = 30 squares across the window",
    "def tile(c, r):": "what letter is at column c, row r?",
    'return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "': "off the edge of the map counts as empty air, so nothing else ever has to check for edges",
    "def load():": "get the level ready to play",
    "global LVL, COLS, ROWS": "change the variables outside this function instead of making new ones inside it",
    "global LVL, COLS, ROWS, SPAWN": "change the variables outside this function instead of making new ones inside it",
    "COLS = max(len(r) for r in L1)": "the widest row sets the width of the world",
    "LVL = [r.ljust(COLS) for r in L1]": "pad every row to that width, so LVL[r][c] never runs off the end",
    "ROWS = len(LVL)": "and the number of rows is the height",

    # step 6
    'LOOK = {"#": (150, 110, 70), "G": (90, 230, 190)}': "letter to colour. The entire art department",
    "def draw(scr):": "everything you see, rebuilt from nothing every frame",
    "for r in range(ROWS):": "every row...",
    "for c in range(COLS):": "...every column",
    "box = pygame.Rect(c * TILE, r * TILE, TILE, TILE)": "grid to pixels: where that square lands on screen",
    "pygame.draw.rect(scr, LOOK[ch], box)": "fill it with the colour for that letter",
    "pygame.draw.rect(scr, (0, 0, 0), box, 1)": "the last argument is a line width, so this draws only the outline",
    "load()": "build the level before the loop starts",
    "draw(scr)": "one call now does all the drawing",

    # step 7
    'SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")': "search every square for the P and stop at the first. Column 5 becomes 5 x 32 = 160 pixels",
    'LVL = [r.replace("P", " ") for r in LVL]': "then erase it, so the P is never drawn or stood on",
    'P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)': "start where the level says, standing still",
    "7:P = {}": "empty now: load() fills it, so where you start lives in the level instead of being typed here",

    # step 8
    "def prect():": "your box, right now, as a Rect",
    'return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)': "Rect wants whole pixels, so int() drops the fraction",

    # step 9
    "def cells(rect):": "every tile a box overlaps, usually two to six of them",
    "for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):": "the -1 means touching an edge exactly does not count as being inside",
    "yield c, r, ch": "hand them back one at a time as the loop asks, instead of building a list",

    # step 10
    "def solid(ch):": "which letters stop you",
    'return ch == "#"': "only bricks. For now",
    '10:P["x"] += P["vx"]': "sideways first, on its own",
    "r = prect()": "where that move put you",
    'if P["vx"] > 0: r.right = c * TILE': "moving right: snap your right edge to the brick's left face",
    'elif P["vx"] < 0: r.left = (c + 1) * TILE': "moving left: the other face",
    'P["x"] = float(r.x); P["vx"] = 0.0': "stop dead, or you keep pressing into it",

    # step 11
    '11:P["y"] += P["vy"]': "and only now, vertically: the same three lines again",
    'if P["vy"] > 0: r.bottom = rw * TILE': "falling: land on top of it",
    'elif P["vy"] < 0: r.top = (rw + 1) * TILE': "rising: bonk your head",
    'P["y"] = float(r.y); P["vy"] = 0.0': "and the fall stops here",

    # step 12
    "def die():": "back to the start, standing still",
    'P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0, g=False)': "every one of your numbers, not just position. Leftover speed is a classic bug",
    'if P["y"] > ROWS * TILE:': "fell past the bottom row",
    "die()": "back to the start",
    "return die()": "back to the start, and nothing else this frame",

    # step 13
    "# ponytail: 1px probe instead of trusting penetration -- sub-pixel gravity never sinks a full pixel": "ponytail: is the tag this author puts on a deliberate shortcut. Here: gravity of 0.35 can leave you a third of a pixel inside a brick, and a one-pixel probe does not care",
    'P["g"] = P["vy"] >= 0 and any(solid(ch) for _, _, ch in cells(prect().move(0, 1)))': "g for grounded. Move the box one pixel down and ask what is there. any() is True if at least one answer is",
    'you = (120, 240, 190) if P["g"] else (240, 235, 220)   # green while you are on the ground': "proof on screen that the line above works. Step 19 takes it away again",

    # step 14
    "GRAV, SPD, JUMP, MAXFALL = 0.35, 3.6, -9.2, 12": "JUMP is negative because y grows downward: up is a negative speed",
    "def step(left, right, pressed=False, held=False):": "two new arguments: pressed is the frame the button went down, held is whether it is still down",
    'if pressed and P["g"]:': "on the ground, and the button went down this exact frame",
    'P["vy"] = JUMP': "the whole jump. Everything after this step is about when it is allowed",
    "if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True": "KEYDOWN fires once, which is exactly what a jump needs",
    "pressed = False": "true for one frame only: the frame the key goes down",
    "if e.key == pygame.K_r: load()": "R rebuilds the level and puts you back at the start",

    # step 15
    "COYOTE = 7                            # you may still jump 7 frames after the edge": "named after the cartoon coyote, who only falls once he looks down",
    'coy = COYOTE if P["g"] else coy - 1': "a countdown that refills every time you touch the ground, and ticks away while you are in the air",
    "if pressed and coy > 0:": "pressed now, and grounded recently enough",
    'P["vy"], coy = JUMP, 0': "jump, and spend the credit so one ledge cannot give two jumps",

    # step 16
    "COYOTE, BUFFER = 7, 8                 # late jump, early jump": "seven frames of grace after the ledge, eight before the landing",
    "buf = BUFFER if pressed else buf - 1": "the same kind of countdown, for the button instead of the ground",
    "if buf > 0 and coy > 0:": "pressed recently AND grounded recently -- the two credits together",
    'P["vy"], buf, coy = JUMP, 0, 0': "jump, and spend both",

    # step 17
    "COYOTE, BUFFER, CUT = 7, 8, 0.42     # late jump, early jump, tap = short hop": "three numbers that are the whole difference between clumsy and fair",
    'P["vy"], buf, coy, P["jump"] = JUMP, 0, 0, True': "jump, spend both credits, and remember that this rise is yours to cut",
    'if P["jump"] and not held and P["vy"] < JUMP * CUT:': "let go early while still rising fast?",
    'P["vy"], P["jump"] = JUMP * CUT, False    # let go early, hop short': "cut the rise to 42% of full: a tap becomes a hop",
    'if P["vy"] >= 0:': "once you are falling there is nothing left to cut",

    # step 18
    "ACC, AIR, FRIC = 0.55, 0.32, 0.72": "how fast you gain speed on the ground, how fast in the air, and how fast you lose it",
    "want = (right - left) * SPD": "the speed you asked for -- which is no longer the speed you get",
    'a = ACC if P["g"] else AIR': "0.55 of steering on the ground, 0.32 in the air",
    'P["vx"] += max(-a, min(a, want - P["vx"]))': "move toward the speed you want by at most a. Never snap to it",
    'P["vx"] *= FRIC if P["g"] else 0.96': "let go and you slide to a stop: quickly on the ground, slowly in the air",

    # step 19
    'cam = max(0, min(int(P["x"]) + PW // 2 - VW // 2, COLS * TILE - VW))': "centre on the middle of you, then clamp: never below 0, never past the last column. The max and the min are the whole camera",
    "for c in range(cam // TILE, min(COLS, cam // TILE + VW // TILE + 2)):": "only draw the columns on screen. Free speed",
    "box = pygame.Rect(c * TILE - cam, r * TILE, TILE, TILE)": "every drawn thing subtracts cam. Nothing else in the game knows the camera exists",

    # step 20
    "taken = set()": "which coins you already picked up, as (column, row) pairs. A set cannot hold the same one twice",
    "for c, rw, ch in cells(prect()):": "every square you are standing in, this frame",
    'if ch == "o" and (c, rw) not in taken:': "a coin you have not had yet",
    "taken.add((c, rw)); coins += 1": "remember it, so it is neither drawn nor counted again",
    "def draw(scr, font):": "draw needs the font now, for the coin counter",
    "font = pygame.font.SysFont(None, 24)": "any font the system has, at size 24",
    'scr.blit(font.render("coins %d" % coins, True, (255, 255, 255)), (10, 10))': "render makes a small picture of the text and blit pastes it on. %d drops the number into the string",
    "pygame.draw.circle(scr, LOOK[ch], box.center, 9)": "coins are circles, radius 9",

    # step 21
    'if ch == "^":': "a real spike, which never lied to anybody",
    "pygame.draw.polygon(scr, LOOK[ch], [box.bottomleft, (box.centerx, box.top), box.bottomright])": "a triangle: two bottom corners and the top middle",

    # step 22
    "cursed = wizard = False": "two flags. The entire twist hangs off the first",
    "def reset():": "a whole fresh run: wizard back, curse off, coins zero",
    'elif ch == "W" and wizard:': "touched the wizard, and he is still here to touch",
    "wizard, cursed = False, True": "he vanishes, and you are cursed. Nothing reads that flag yet",
    "pygame.draw.rect(scr, (160, 80, 220), box.inflate(-8, 0))": "the wizard: purple, and narrower than his square",

    # step 23
    'LIARS = set("%")': "every letter that is not what it looks like. One, so far",
    'return ch == "#" or (ch == "%" and not cursed)': "a hologram is solid only while you still believe in it",

    # step 24
    "def throw(tx, ty):": "tx, ty is where you clicked, in world pixels",
    'cx, cy = P["x"] + PW / 2, P["y"] + PH / 2': "throw from your middle, not your corner",
    "dx, dy = tx - cx, ty - cy": "the arrow from you to the click",
    "d = max(1.0, (dx * dx + dy * dy) ** 0.5)": "its length. ** 0.5 is a square root, and max(1) stops a click on yourself dividing by zero",
    "sp = max(4.5, min(16.0, d / 20.0))        # close click = soft lob, far click = hard throw": "clamped at both ends, so no click is useless and none is absurd",
    "pebbles.append([cx, cy, dx / d * sp, dy / d * sp])": "dx/d is direction alone; times sp is direction with force. Each pebble is [x, y, vx, vy]",
    "def pebble_step():": "one frame for every pebble in the air",
    "for pb in pebbles[:]:": "the [:] makes a copy, so removing pebbles while looping over them is safe",
    "pb[3] += GRAV * 0.5": "pebbles fall too, at half weight",
    "pb[0] += pb[2]; pb[1] += pb[3]": "the same speed-changes-position rule as you",
    "if not (0 <= c < COLS and 0 <= r < ROWS):": "left the map",
    "throw(e.pos[0] + cam, e.pos[1])": "e.pos is where on screen you clicked; adding cam makes it a place in the level",
    "pebble_step()": "move the pebbles once per frame, like everything else",

    # step 25
    "revealed.update((c + i, r + j) for i in (-1, 0, 1) for j in (-1, 0, 1))": "reveal a 3x3 patch around the hit, not a single tile: a splash of truth",
    "def edge(col):": "a darker version of any colour, for the outline",
    "seen = (c, r) in revealed": "has a pebble told you about this square?",
    "lie = seen and ch in LIARS": "revealed, and actually a liar. Honest tiles look identical either way",
    "col = TRUTH[ch] if lie else LOOK[ch]": "the one line where a lie becomes visible",

    # step 26
    "GRAV, SPD, JUMP, BOUNCE, MAXFALL = 0.35, 3.6, -9.2, -12.3, 12": "BOUNCE is stronger than JUMP: a trampoline throws you higher than you can jump",
    'if ch == "t" and cursed:': "the spikes, once you can see them for what they are",
    'P["vy"], P["g"], P["jump"] = BOUNCE, False, False': "fire upward, and forget you were grounded or mid-jump -- so the cut in step 17 cannot shorten a trampoline",

    # step 27
    'elif (ch == "o" or ch == "x") and (c, rw) not in taken:': "the killer coin still counts as a coin, if it has not killed you first",

    # step 28
    'return ch in "#~" or (ch == "%" and not cursed)': "the invisible floor is solid like any brick; it is only the drawing that leaves it out",
    'elif ch == "~":': "drawn only once a pebble has found it",

    # step 29
    "CRUMB = 26                            # frames a crumbling brick holds you": "26 frames is a little under half a second",
    'if P["g"]:': "crumbling counts only while you are actually standing on it",
    "crumb[(c, rw)] = crumb.get((c, rw), 0) + 1": "count the frames for that exact square. .get with a 0 means the first frame needs no special case",
    "if crumb[(c, rw)] > CRUMB:": "held long enough",
    "gone.add((c, rw))": "into gone, and gone squares are neither drawn nor solid",
    'box = box.move(int(math.sin(frames) * 2), 0)      # about to give way': "shake it two pixels, so you get a warning",

    # step 30
    'elif ch == "!":': "the exit that is not one",

    # step 31
    "def roll(row, rng):": "one row of the level, and this run's dice",
    'if out[i] in "?&":': "found a rollable square",
    "while j < len(out) and out[j] == ch:": "find the whole run of them, e.g. ????",
    'safe, other = ("t", "^") if ch == "?" else ("#", "%")': "which of the two you can survive",
    "span = [rng.choice((safe, other)) for _ in range(j - i)]": "roll each square in the run",
    "out[i:j] = span": "write the rolled squares back over the ?s",
    "rng = random.Random(seed * 977)": "one seed gives the same level every time, which is how you re-open a bug",
    "seed = random.randrange(1 << 30)": "a new seed per run, so no two runs are the same. 1 << 30 is just a big number",

    # step 32
    "if safe not in span:": "every single one came up bad, so:",
    "span[rng.randrange(len(span))] = safe": "force one back. Those two lines are the whole guarantee",

    # step 33
    "LEVELS = [L1, L2, L3, L4, L5]": "the whole game, in one list",
    "L2 = [": "level II, The Floor Lies: the ground is threaded with holograms, and trampolines wait underneath",
    "L3 = [": "level III, The Gaps Lie: those wide holes are mostly invisible floor. Walk over nothing",
    "L4 = [": "level IV, Nothing Holds: nearly every brick is cracked, so standing still is what kills you",
    "L5 = [": "level V, The Gauntlet: one of everything, including the fake exit, and the strongest wind",
    "def load(i):": "load takes a number now: which level to start",
    "level, frames = i, 0": "remember which level we are on, and restart its clock",
    "rng = random.Random(seed * 977 + i)": "a different roll per level, still repeatable from the one seed",
    "taken.clear(); revealed.clear(); gone.clear(); pebbles.clear(); crumb.clear()": "every level starts clean. Forgetting one of these is a real bug",
    'elif ch == "G":': "the way out",
    "if level + 1 < len(LEVELS):": "another level to go?",
    "return load(level + 1)": "start it, and do nothing else this frame",
    "won = True": "that was the last one",

    # step 34
    "def clock_str(f):": "frames into minutes and seconds: 60 frames is a second, 3600 a minute",
    'return "%d:%02d" % (f // 3600, f // 60 % 60)': "%02d pads to two digits, so it reads 1:05 and not 1:5",
    "def draw(scr, font, big):": "two fonts now: small for the bar, big for the message",
    'hud = "%s   %s   coins %d   total %s" % (NAMES[level], clock_str(frames), coins, clock_str(total))': "which level, its time, coins, and the run's total",
    "if frames < 140 and not won:": "for the first couple of seconds of a level, show its name instead of the tip",
    "scr.blit(t, t.get_rect(center=(VW // 2, 90)))": "get_rect(center=...) centres the text without any arithmetic",
    "if not won:": "once you have won, stop simulating: the victory screen holds still",
    "frames += 1; total += 1": "this level's clock, and the run's clock",

    # step 35
    "GUST = [0.0, 0.0, 0.04, 0.10, 0.14]   # per-level wind strength, sign flips every few seconds": "one number per level, and the first two are 0.0 -- levels I and II are calm on purpose",
    "def wind():": "how hard it is blowing, right now",
    "return GUST[level] * math.sin(frames / 110.0) if cursed else 0.0": "sin rocks between -1 and 1, so the wind swings around instead of shoving one way forever",
    'P["vx"] += wind() * (1.0 if P["g"] else 2.2)   # gusts shove hardest in the air': "feet on the ground resist it; mid-jump you are a leaf",
    "pb[2] += wind() * 1.6": "your pebbles get blown off course too",
    'blow = ("  wind " + ("<<<" if w < 0 else ">>>")) if abs(w) > 0.012 else ""': "and the bar says which way, in case you missed it",

    # step 36
    "warp = max(0.0, warp - 0.16)": "warp is a fading number: a shock spikes it and it settles back down",
    "warp = 22.0": "the fake exit: a hard visual jolt as it throws you back",
    "wizard, cursed, warp = False, True, 26.0": "the biggest jolt in the game, at the moment the world turns on you",
    "warp = max(warp, 6.0)": "a small jolt on every death, so it always registers",
    "def gusts(scr):": "the wind, made visible before it can surprise you",
    "if abs(w) < 0.012:": "too gentle to bother drawing",
    "ln = int(abs(w) * 90) + 6": "stronger wind, longer streaks",
    "def wobble(scr, amt):": "the curse bending what you see. It never moves anything real",
    "src = scr.copy()": "a photograph of the finished frame",
    "for y in range(0, VH, 5):": "cut it into 5-pixel bands",
    "dx = int(math.sin(frames / 11.0 + y / 26.0) * amt + math.sin(frames / 3.7 + y / 9.0) * amt * 0.35)": "two sines at different speeds, so it never settles into a pattern",
    "scr.blit(src, (dx, y), (0, y, VW, 5))": "paste each band back, shifted. The third argument picks which slice of the photograph to use",
    "ghost = src.copy(); ghost.set_alpha(110)": "a half-transparent second copy, for the hardest jolts",

    # step 37
    "def test():": "the robot. No window, no keyboard, no waiting",
    "for _ in range(60): step(0, 1)": "hold right for 60 frames: one second of walking",
    'assert P["x"] > SPAWN[0] + 100 and cursed, "walk right, meet the wizard"': "assert says this must be true. If it is not, the program stops here and prints that message",
    'assert tap > held + 20, ("tapping must hop lower than holding", tap, held)': "bigger y is lower on screen. If this ever fails, CUT is broken",
    'LVL = [" " * 10] * 17 + ["      !   ", "~~~~cc##%%", "##########"]': "a tiny level built by hand, with one of every liar in it, so each can be tested on its own",
    'assert (4, 18) in gone, "standing on a crumbling brick breaks it"': "stood still for CRUMB + 30 frames, so it must be gone by now",
    'assert abs(P["x"] - x0) > 1.0, "wind must push the player"': "no keys held at all, and you still moved: that is the wind",
    'assert holes <= 5, ("uncrossable hole", i, sd, holes)': "5 empty columns is jumpable at this SPD and JUMP; 6 would be a level nobody could finish",
    'globals()["seed"] = sd': "reach out and set the module's own seed, so load() rolls the dice we want",
    'print("ok")': "the whole point: one word, or a stop with the message and the seed that broke it",
    'if "--test" in sys.argv:': "sys.argv is whatever you typed after the filename",
}


# ------------------------------------------------------------------ hover hints
# Every name the code uses, for the tooltip that follows the cursor.
#   kind:   const | var | func | lib | key
#   expand: what an abbreviation actually stands for
#   sig / ret: only for functions -- what goes in, what comes out

def F(sig, takes, ret, text):
    return dict(kind="func", sig=sig, takes=takes, ret=ret, text=text)


def V(expand, text, kind="var"):
    return dict(kind=kind, expand=expand, text=text)


SYMBOLS = {
    # --- the shape of the world
    "TILE": V("tile size", "How big one square of the world is, in pixels: 32. Column 5 starts at pixel 160.", "const"),
    "VW": V("view width", "The window's width in pixels: 960, which is 30 squares.", "const"),
    "VH": V("view height", "The window's height in pixels: 640, which is 20 squares.", "const"),
    "COLS": V("columns", "How many squares wide this level is. Worked out by load() from the longest row.", "const"),
    "ROWS": V("rows", "How many squares tall this level is: just the number of strings in the level.", "const"),
    "LVL": V("level", "The level being played: a list of strings, one per row, all padded to the same width."),
    "L1": V("level 1", "Level I, The Curse, written out as text. One letter per square."),
    "L2": V("level 2", "Level II, The Floor Lies: holograms threaded through the ground."),
    "L3": V("level 3", "Level III, The Gaps Lie: wide holes that are mostly invisible floor."),
    "L4": V("level 4", "Level IV, Nothing Holds: nearly every brick cracked."),
    "L5": V("level 5", "Level V, The Gauntlet: one of everything, and the strongest wind."),
    "LEVELS": V("levels", "All five levels in one list, so load(2) means 'the third one'."),
    "NAMES": V("names", "The title of each level, shown on the bar for the first two seconds."),
    "ROW": V("row", "One empty row of the level -- 60 spaces -- so the sky is not written out thirteen times."),
    "SPAWN": V("spawn point", "Where you start, in pixels, found once by load() from the P in the level."),
    "level": V("level number", "Which of the five levels is being played, counting from 0."),
    "seed": V("seed", "The number the dice start from. The same seed always builds the same level, which is how you re-open a bug."),

    # --- you
    "P": V("player", "You: a dictionary of numbers. x and y are where you are, vx and vy how fast you are moving, g whether you are on the ground, jump whether this rise can still be cut short."),
    "PW": V("player width", "How wide you are: 20 pixels, narrower than a square on purpose.", "const"),
    "PH": V("player height", "How tall you are: 28 pixels.", "const"),
    "SPD": V("speed", "Top walking speed: 3.6 pixels per frame, which is 216 a second.", "const"),
    "GRAV": V("gravity", "Added to your falling speed every frame: 0.35.", "const"),
    "MAXFALL": V("maximum fall", "The fastest you may ever fall: 12 pixels a frame. Without it a long fall would pass straight through a floor.", "const"),
    "JUMP": V("jump speed", "The upward speed a jump gives you: -9.2. Negative because screen y grows downward.", "const"),
    "BOUNCE": V("bounce speed", "What a trampoline gives you: -12.3, stronger than your own jump.", "const"),
    "ACC": V("acceleration", "How fast you gain speed on the ground: 0.55 per frame.", "const"),
    "AIR": V("air acceleration", "How fast you gain speed in the air: 0.32 per frame. Less control once you leave the floor.", "const"),
    "FRIC": V("friction", "What your speed is multiplied by each frame when you let go on the ground: 0.72, so you slide to a stop.", "const"),
    "COYOTE": V("coyote time", "How many frames after leaving a ledge a jump still counts: 7. Named after the cartoon coyote who only falls once he looks down.", "const"),
    "BUFFER": V("jump buffer", "How many frames early a jump press is remembered: 8.", "const"),
    "CUT": V("cut", "How much of a rise is left when you let go early: 0.42, so a tap is a small hop.", "const"),
    "CRUMB": V("crumble time", "How many frames a cracked brick holds you before it breaks: 26, a bit under half a second.", "const"),
    "GUST": V("gusts", "How strong the wind is on each level, in order. The first two are 0.0, so levels I and II are calm.", "const"),
    "coy": V("coyote counter", "The countdown left on coyote time. Refills to COYOTE whenever you touch ground, ticks down in the air."),
    "buf": V("buffer counter", "The countdown left on a remembered jump press."),
    "frames": V("frames", "How many frames this level has been running. Sixty of them is one second."),
    "total": V("total frames", "How many frames the whole run has taken, across every level."),
    "coins": V("coins", "How many coins you have picked up this run."),
    "cursed": V("cursed", "False until you touch the wizard. Once True, every lie in the level starts behaving differently."),
    "wizard": V("wizard here", "True while the wizard is still standing in the level. He vanishes the moment you touch him."),
    "won": V("won", "True once you touch the exit on the last level. The game then stops simulating and holds still."),
    "warp": V("warp", "How badly the picture is being bent right now. A shock spikes it and it fades by 0.16 a frame."),
    "taken": V("taken coins", "The squares whose coins you already picked up, as (column, row) pairs. A set, so nothing counts twice."),
    "revealed": V("revealed squares", "Every square a pebble has told you the truth about."),
    "gone": V("gone squares", "Squares that have crumbled away. Neither drawn nor solid any more."),
    "crumb": V("crumble counters", "How many frames you have stood on each cracked brick, keyed by (column, row)."),
    "pebbles": V("pebbles", "Every pebble in the air right now. Each one is a list: [x, y, vx, vy]."),
    "LIARS": V("liars", "The set of letters that are not what they look like."),
    "LOOK": V("look", "What each letter is drawn as: letter to colour."),
    "TRUTH": V("truth", "What a letter is drawn as once a pebble has revealed it: the same hue, gone dull."),

    # --- the game's own functions
    "roll": F("roll(row, rng)", "one row of the level, and this run's dice",
              "the same row with every ? and & replaced by a real letter",
              "Rolls the per-run tiles. Every run of them keeps one safe square, so no roll can make the level impossible."),
    "load": F("load(i)", "which level to start (0 to 4)", "nothing -- it sets up LVL, COLS, ROWS and SPAWN",
              "Starts a level: measure it, roll its dice, find the P, wipe the last level's coins and rubble, put you at the spawn."),
    "reset": F("reset()", "nothing", "nothing", "A whole fresh run: new seed, curse off, wizard back, coins zero, level I."),
    "die": F("die()", "nothing", "nothing", "Puts you back at the spawn with every one of your numbers cleared -- position and speed both."),
    "wind": F("wind()", "nothing", "a small number, positive or negative",
              "How hard the wind is blowing this frame. Zero unless you are cursed."),
    "tile": F("tile(c, r)", "a column and a row", "the letter at that square, or a space",
              "Reads one square of the level. Anywhere off the map counts as empty air, so nothing else has to check for edges."),
    "solid": F("solid(ch)", "one letter", "True or False",
               "Whether that letter stops you. This is where the curse changes the world: a hologram is solid only while you still believe in it."),
    "prect": F("prect()", "nothing", "a pygame Rect", "Your box, right now, as a rectangle the collision code can measure."),
    "cells": F("cells(rect)", "a rectangle", "each (column, row, letter) it overlaps, one at a time",
               "Which squares a box is sitting in. Everything that touches the world goes through here."),
    "step": F("step(left, right, pressed, held)",
              "left/right: is that key down. pressed: did jump go down this frame. held: is jump still down",
              "nothing -- it changes P and the counters",
              "One frame of you: steer, jump, fall, get pushed out of walls, then react to whatever you are touching."),
    "throw": F("throw(tx, ty)", "where you clicked, in world pixels", "nothing -- it adds a pebble",
               "Throws a pebble from your middle toward the click. The further the click, the harder the throw."),
    "pebble_step": F("pebble_step()", "nothing", "nothing",
                     "Moves every pebble one frame, and reveals what any of them hit."),
    "edge": F("edge(col)", "a colour", "a darker colour", "Used for the outline on a revealed lie."),
    "clock_str": F("clock_str(f)", "a number of frames", 'text like "1:05"',
                   "Turns frames into minutes and seconds. Sixty frames is a second."),
    "draw": F("draw(scr, font, big)", "the screen to draw on, and two fonts", "nothing",
              "Rebuilds the whole picture from scratch: level, pebbles, you, the warp, then the bar along the top."),
    "gusts": F("gusts(scr)", "the screen", "nothing", "Draws the wind as streaks, so you can see it before it moves you."),
    "wobble": F("wobble(scr, amt)", "the screen, and how hard to bend it", "nothing",
                "Photographs the finished frame, cuts it into 5-pixel bands and pastes them back shifted. It bends what you see, never what is true."),
    "main": F("main()", "nothing", "nothing", "The game loop: read what happened, move things, draw, wait, repeat."),
    "test": F("test()", "nothing", "nothing -- it prints ok, or stops on the line that is wrong",
              "The robot: plays the game with fake key presses and checks the answers, with no window at all."),

    # --- names that only live for a moment
    "scr": V("screen", "The surface everything is drawn onto. Handed to draw() every frame."),
    "clk": V("clock", "pygame's metronome. clk.tick(60) sleeps just long enough to keep the loop at 60 frames a second."),
    "font": V("font", "The small font, used for the bar along the top."),
    "big": V("big font", "The larger font, used for the message in the middle."),
    "e": V("event", "One thing that happened: a key going down, a click, the window closing."),
    "k": V("keys", "Which keys are held down right now. k[pygame.K_LEFT] is True while left is down."),
    "pressed": V("pressed", "True only on the frame the jump key went down, which is what a jump needs."),
    "held": V("held", "True while the jump key is still down. Letting go early is what cuts a jump short."),
    "want": V("wanted speed", "The speed the keys are asking for. You steer toward it instead of snapping to it."),
    "cam": V("camera", "How far left the whole world is drawn. That is the entire camera."),
    "box": V("box", "The rectangle one square of the level occupies on screen."),
    "ch": V("character", "One letter from the level: what is in that square."),
    "c": V("column", "A column number in the level grid."),
    "r": V("row", "A row number: which row of the level you are looking at."),
    "rw": V("row", "A row number. Called rw here because r is already the rectangle."),
    "pb": V("pebble", "One pebble in the air: [x, y, vx, vy]."),
    "cx": V("centre x", "The middle of you, across."),
    "cy": V("centre y", "The middle of you, down."),
    "dx": V("delta x", "A distance across: how far the click is from you, or how far a band of the picture is shifted."),
    "dy": V("delta y", "A distance down: how far the click is from you."),
    "d": V("distance", "How far away the click was, in pixels."),
    "sp": V("speed", "How hard the pebble is thrown, worked out from that distance."),
    "seen": V("seen", "Whether a pebble has revealed this square."),
    "lie": V("lie", "Whether this square is a liar you have already revealed. Only then is it drawn differently."),
    "col": V("colour", "The colour this square is about to be drawn in."),
    "hud": V("heads-up display", "The line of text along the top: level, time, coins, total."),
    "tip": V("tip", "The message in the middle of the screen: the level's name, then advice, then victory."),
    "blow": V("blow", "The little wind arrows on the bar, if it is blowing hard enough to matter."),
    "src": V("source", "A photograph of the finished frame, taken so the warp has something to bend."),
    "ghost": V("ghost", "A half-transparent second copy of the frame, for the hardest jolts."),
    "amt": V("amount", "How hard to bend the picture this frame."),
    "ln": V("length", "How long each wind streak is drawn."),
    "w": V("wind", "How hard the wind is blowing this frame."),
    "rng": V("random number generator", "This run's dice. Built from the seed, so the same seed rolls the same level."),
    "span": V("span", "One run of ? or & squares, after the dice have decided each one."),
    "safe": V("safe letter", "The survivable side of a rolled square: a trampoline for ?, a real brick for &."),
    "other": V("other letter", "The dangerous side: a spike for ?, a hologram for &."),
    "rows": V("rows", "The level being loaded, before it is padded and rolled."),
    "holes": V("holes", "The widest run of completely empty columns found in a level. More than 5 would be uncrossable."),
    "run": V("run", "How many empty columns in a row we have counted so far."),
    "sd": V("seed", "Which seed the robot is testing this time around."),
    "tap": V("tap", "The highest point reached by tapping the jump key."),
    "near": V("near throw", "The speed of a pebble thrown at something close."),
    "far": V("far throw", "The speed of a pebble thrown at something distant."),

    # --- pygame and Python
    "pygame": V("pygame", "The library that opens the window, reads the keyboard and draws shapes.", "lib"),
    "math": V("math", "Python's maths library. This game uses only math.sin, for the wind and the warp.", "lib"),
    "random": V("random", "Python's dice. Seeded here, so a level can be rolled the same way twice.", "lib"),
    "sys": V("sys", "Python's own settings. Used once, to read what you typed after the filename.", "lib"),
    "init": F("pygame.init()", "nothing", "nothing", "Wakes pygame up. Nothing else works before it."),
    "set_mode": F("pygame.display.set_mode((w, h))", "the size you want", "the surface to draw on", "Makes the window."),
    "set_caption": F("pygame.display.set_caption(text)", "some text", "nothing", "Sets the title on the window bar."),
    "Clock": F("pygame.time.Clock()", "nothing", "a clock", "A metronome. Its tick(60) sleeps to hold the loop at 60 frames a second."),
    "tick": F("clk.tick(60)", "frames per second", "nothing", "Sleeps just long enough that the loop runs at that speed instead of as fast as the machine can."),
    "flip": F("pygame.display.flip()", "nothing", "nothing", "Shows the frame you have just drawn."),
    "fill": F("scr.fill(colour)", "a colour", "nothing", "Paints over everything. Without it, last frame smears into this one."),
    "Rect": F("pygame.Rect(left, top, width, height)", "a position and a size", "a rectangle",
              "pygame's box. It reports its own edges: .right, .bottom, .center, .move(), .inflate()."),
    "rect": F("pygame.draw.rect(scr, colour, box, width)", "where and what colour; width 0 fills, more than 0 outlines", "nothing", "Draws a rectangle."),
    "circle": F("pygame.draw.circle(scr, colour, centre, radius)", "a middle and a radius", "nothing", "Draws a circle. Coins are circles of radius 9."),
    "polygon": F("pygame.draw.polygon(scr, colour, points)", "a list of corners", "nothing", "Draws a shape from corners. A spike is three of them."),
    "line": F("pygame.draw.line(scr, colour, start, end, width)", "two points", "nothing", "Draws a straight line."),
    "blit": F("scr.blit(picture, (x, y))", "a picture and where to put it", "nothing",
              "Pastes one picture onto another. Text, and each band of the warp, arrive this way."),
    "render": F("font.render(text, True, colour)", "the text and its colour", "a small picture of that text",
                "Fonts do not draw text: they make a picture of it, which you then blit."),
    "SysFont": F("pygame.font.SysFont(None, 24)", "a font name (None means any) and a size", "a font", "Picks a font the computer already has."),
    "get_pressed": F("pygame.key.get_pressed()", "nothing", "a lookup of every key, True if held",
                     "Which keys are down right now -- not which were just pressed."),
    "get": F("pygame.event.get()", "nothing", "a list of everything that happened",
             "Empties the queue of events since last frame. Also the name of a dictionary's .get(key, default)."),
    "update": F("P.update(x=1, y=2)", "names and values", "nothing", "Sets several entries of a dictionary at once."),
    "move": F("rect.move(dx, dy)", "a shift", "a new rectangle, shifted", "Does not change the original -- that is why the ground probe is safe."),
    "inflate": F("rect.inflate(dw, dh)", "how much to grow by; negative shrinks", "a new rectangle", "Used to draw the wizard narrower than his square."),
    "min": F("min(a, b)", "some numbers", "the smallest", "Used to cap: min(speed + GRAV, MAXFALL) is 'add gravity, but never past the cap'."),
    "max": F("max(a, b)", "some numbers", "the biggest", "Used as a floor. max and min together are a clamp -- that is the whole camera."),
    "abs": F("abs(x)", "a number", "the same number without its sign", "How hard the wind blows, whichever way it is going."),
    "any": F("any(...)", "a sequence of True/False", "True if at least one is True", "'Is there anything solid below me' is one any()."),
    "all": F("all(...)", "a sequence of True/False", "True only if every one is", "Used by the robot to spot a completely empty column."),
    "next": F("next(...)", "a sequence", "its first item", "Used to find the P and stop looking."),
    "len": F("len(x)", "a list or string", "how many items are in it", ""),
    "range": F("range(n)", "a count (or start, stop)", "the numbers to loop over", ""),
    "set": F("set(x)", "letters or items, or nothing", "a bag with no duplicates and no order",
             'set("%tx") makes three separate letters. Asking "is it in here" is instant.'),
    "int": F("int(x)", "a number", "the whole part, fraction dropped", "Pixels are whole; your position is not."),
    "float": F("float(x)", "a number", "the same number with a fraction", "Positions are kept as fractions so gravity of 0.35 is not lost."),
    "tuple": F("tuple(x)", "a sequence", "a fixed sequence", "Colours are tuples: (255, 0, 0)."),
    "print": F("print(x)", "anything", "nothing", "Writes it in the terminal."),
    "sin": F("math.sin(x)", "a number", "a number between -1 and 1",
             "Rocks smoothly back and forth forever. Both the wind and the warp are sin of the frame count."),
    "append": F("list.append(x)", "one item", "nothing", "Adds it to the end of a list."),
    "remove": F("list.remove(x)", "one item", "nothing", "Takes it out of a list."),
    "add": F("set.add(x)", "one item", "nothing", "Puts it in a set. Adding the same thing twice changes nothing."),
    "clear": F("clear()", "nothing", "nothing", "Empties a set, list or dictionary. Every level starts by clearing these."),
    "ljust": F('"ab".ljust(5)', "a width", "the string padded with spaces to that width", "How every row of the level ends up the same length."),
    "replace": F('"aXb".replace("X", " ")', "what to find, what to put there", "a new string", "How the P is erased once it has been found."),
    "join": F('"".join(parts)', "a list of strings", "one string", "Puts the rolled squares back together into a row."),
    "copy": F("scr.copy()", "nothing", "a separate copy", "The warp photographs the frame this way before bending it."),
    "set_alpha": F("surface.set_alpha(110)", "how solid, 0 to 255", "nothing", "Makes the ghost copy half-transparent."),
    "get_rect": F("picture.get_rect(center=(x, y))", "where to put it", "a rectangle in that position",
                  "Centres text without any arithmetic."),
    "get_surface": F("pygame.display.get_surface()", "nothing", "the window's surface", ""),
    "randrange": F("rng.randrange(n)", "a count", "a whole number below it", "Which square in the run gets forced back to safe."),
    "choice": F("rng.choice((a, b))", "some options", "one of them", "The actual coin flip for a ? or & square."),
    "Random": F("random.Random(seed)", "a seed", "a dice-roller", "Same seed, same rolls, every time."),
    "globals": F("globals()", "nothing", "the module's own names", "Used by the robot to set the seed from inside a function."),
}


# --------------------------------------------------- functions, step by step
# A function's shape changes as the lesson goes on, so its hint must too. The
# signature is read from the file itself; these fill in what each argument is
# for, and what the function does at the point you are looking at it.

PARAMS = {
    "step": {"left": "is the left key down", "right": "is the right key down",
             "pressed": "did the jump key go down on this frame",
             "held": "is the jump key still down"},
    "draw": {"scr": "the surface to draw on", "font": "the small font, for the bar",
             "big": "the bigger font, for the message in the middle"},
    "load": {"i": "which level to start, 0 to 4"},
    "tile": {"c": "a column", "r": "a row"},
    "solid": {"ch": "one letter from the level"},
    "cells": {"rect": "a rectangle, usually your own box"},
    "throw": {"tx": "where you clicked, across", "ty": "where you clicked, down"},
    "edge": {"col": "a colour"},
    "clock_str": {"f": "a number of frames"},
    "wobble": {"scr": "the screen", "amt": "how hard to bend it"},
    "gusts": {"scr": "the screen"},
    "roll": {"row": "one row of the level", "rng": "this run's dice"},
}

# name -> what it means inside one particular function, when the general meaning
# would be wrong there.
LOCALS = {
    ("step", "r"): ("your box", "Your own box after that move, as a Rect. The lines under it push it back out of anything solid."),
    ("prect", "r"): ("row", "A row number."),
}

TEXT_BY_STEP = {
    "step": [
        (3, "One frame of you: the keys set your speed, and the speed moves you."),
        (4, "One frame of you: the keys set your speed, gravity adds to it, and both move you."),
        (10, "One frame of you: move sideways, then get pushed back out of anything solid you ended up inside."),
        (11, "One frame of you: move on one axis and push out, then the other. That order is what makes it work."),
        (13, "One frame of you: move, push out of walls, then work out whether you are standing on something."),
        (14, "One frame of you: jump if asked, fall, move, and push out of walls."),
        (18, "One frame of you: steer toward the speed you want, jump, fall, move, push out of walls."),
        (20, "One frame of you: steer, jump, move, push out of walls, then react to whatever you are touching."),
        (35, "One frame of you: steer, take the wind, jump, move, push out of walls, then react to what you touch."),
    ],
    "solid": [
        (10, "Whether that letter stops you. Only bricks, so far."),
        (23, "Whether that letter stops you -- and where the curse changes the world: a hologram is solid only while you still believe in it."),
        (28, "Whether that letter stops you. Bricks, invisible floor and cracked bricks all do; a hologram only until you are cursed."),
    ],
    "draw": [
        (6, "Rebuilds the picture from nothing: every square of the level, then you."),
        (13, "Rebuilds the picture, and paints you green while you are standing on something."),
        (19, "Rebuilds the picture shifted by the camera, so the world can be wider than the window."),
        (20, "Rebuilds the picture: the level, you, and the coin count."),
        (25, "Rebuilds the picture, drawing any liar a pebble has revealed in its true colour."),
        (34, "Rebuilds the whole picture: level, pebbles, you, then the bar along the top and the message."),
    ],
    "load": [
        (5, "Measures the level and pads every row to the same width."),
        (7, "Measures the level, finds the P and remembers it as SPAWN, then erases it."),
        (31, "Measures the level, rolls this run's dice over it, finds the P, then erases it."),
        (33, "Starts level i: measure it, roll its dice, find the P, wipe the last level's coins and rubble, put you at the spawn."),
    ],
    "main": [
        (1, "Opens the window and runs the loop: read what happened, draw, wait, repeat."),
        (3, "Opens the window and runs the loop: read the keys, move you, draw, wait, repeat."),
        (24, "Opens the window and runs the loop: events, keys, one step of the game, the pebbles, then draw."),
    ],
    "reset": [
        (22, "A fresh run: wizard back, curse off, coins zero."),
        (33, "A fresh run: a new seed, curse off, wizard back, coins and clocks zero, level I."),
    ],
    "die": [(12, "Puts you back at the spawn with every one of your numbers cleared.")],
    "roll": [
        (31, "Rolls the ? and & squares for this run."),
        (32, "Rolls the ? and & squares, keeping one safe square in every run of them, so no roll can make the level impossible."),
    ],
    "pebble_step": [
        (24, "Moves every pebble one frame, and drops the ones that hit something."),
        (25, "Moves every pebble one frame, and reveals whatever any of them hit."),
    ],
}
