"""What the lesson says: the prose for each step, the note on each new line, and
the hover hint for every name in the code.

Kept apart from main.py so the lesson server stays readable.
"""

# ------------------------------------------------------------------ the steps
# title comes from build_steps.TITLES, so it is never written down twice.

STEP_TEXT = {
1: dict(why="Before any game, one thing: a rectangle that does not close. A game is a <b>loop</b> -- read what happened, move things, draw, wait, repeat, sixty times a second. One trip round that loop is a <b>frame</b>, and every number in this whole game is measured in frames.",
    trial="Nothing moves, and that is correct. A window running sixty times a second with nothing in it is already a game."),
2: dict(why="You are four numbers in a <b>dictionary</b> -- a labelled bag of values, read back as <code>P[\"x\"]</code>. Not a sprite, not a character: <b>where you are</b> and <b>how fast you are going</b>. Two small functions come with it and never change shape: <code>place()</code> puts you at <code>SPAWN</code>, and <code>reset()</code> is what a whole fresh run means -- for now, just that. Every later step adds a line to them; none takes one away.",
    trial="A box, sitting still, drawn fresh sixty times a second. Nothing reads vx and vy yet."),
3: dict(why="Keys set the speed; the speed moves the position. Never move x straight from a key -- everything later (gravity, wind, being pushed out of a wall) works by changing a speed, and none of it could touch you if the key wrote your position directly.",
    trial="Hold an arrow and you move; let go and you stop dead on that same frame. Sliding comes at step 18."),
4: dict(why="Gravity is not a fall. It is one number added to <b>vy</b> every frame, so falling gets faster the longer it lasts -- exactly like the real thing. <b>MAXFALL</b> caps it: uncapped, a long fall would cover a whole tile per frame and pass straight through a floor.",
    trial="You drop, and you keep dropping. There is no floor yet, and nothing to catch you -- use the restart button."),
5: dict(why="The level is not a picture. It is <b>text</b>: one letter per 32x32 square, which is what <code>TILE</code> means. Every row is one string of the same width, so you can count columns straight off the page. <code>load(i)</code> takes a level number from the start, even though <code>LEVELS</code> holds one level for now -- the finished game has five, and a function that changes its arguments halfway through a lesson is a function you learn twice.",
    trial="Nothing has changed on screen -- the level exists as data and nothing draws it yet. Read it in the code instead: that is the whole map."),
6: dict(why="Two loops and a lookup. Walk every row, walk every column, and paint a square in the colour that letter means. <code>//</code> is division that throws the remainder away, so pixel 100 is column 3. <code>LOOK</code> already lists every letter the game will ever have -- coins, spikes, bricks that lie -- because a table you extend one entry at a time is a table you rewrite eleven times.",
    trial="Bricks. The floor and the platform, drawn from text. The box still falls through them: nothing is solid yet."),
7: dict(why="The <code>P</code> in the level says where you start. <code>load()</code> finds it once, remembers it as <code>SPAWN</code>, then erases it, so the letter is never drawn or stood on. Your position now comes from the level, not from numbers typed in the file.",
    trial="You start on the left where the P was, and still fall through everything."),
8: dict(why="A <code>Rect</code> is pygame's box: left, top, width, height. It reports its own edges -- <code>.right</code>, <code>.bottom</code>, <code>.center</code> -- and that is what makes pushing out of a wall two lines instead of ten.",
    trial="Still no collision. This step only gives the next two steps something to ask questions about."),
9: dict(why="Which squares is that box sitting in? Divide its edges by <code>TILE</code> and you get a small range of rows and columns -- usually two to six squares. <code>yield</code> hands them back one at a time as the loop asks, instead of building a list.",
    trial="Nothing visible yet. Everything that touches the world -- walls, coins, spikes, the wizard -- goes through this one function."),
10: dict(why="The trick that makes collision easy: <b>move on one axis, fix that axis, then do the other</b>. Move both at once and you cannot tell whether you hit a wall or a floor. Down first, because falling is what you are doing every frame: move y, then look at every square you now overlap, and if it is solid put your <b>bottom</b> back on top of it.",
    trial="You land, and you stay landed. Now walk right into the block at column 8 -- you go straight through it, because nothing has fixed x yet. That is the next step."),
11: dict(why="The same three lines again, sideways. Moving right means your <b>right edge</b> stops at the brick's left face; moving left, the other way round. Two passes, each one only ever fixing the axis it just moved, is the whole of collision in this game. And one more line: the level has two ends, and walking off either of them is not a way out of it -- <code>min</code> caps a number, <code>max</code> floors it, and the two together pin you inside the level.",
    trial="Walk right. The block at column 8 stops you dead now, instead of letting you through. Hold left and you stop at the first column instead of walking out of the world."),
12: dict(why="Fall past the bottom row and nothing below will ever catch you, so the game has to notice. But being put back is not free: it costs one of five <code>LIVES</code>, and the last one ends the run -- <code>over</code> is the flag, and the first line of <code>step()</code> honours it, so nothing moves again until space starts a fresh run through <code>reset()</code>. <code>die()</code> and <code>place()</code> are two different things from the day they exist: one costs you, one does not.",
    trial="Walk right off the edge at column 4. You fall, and a moment later you are back at the start, one life down. Do it five times and everything stops."),
13: dict(why="The wrong way is to remember \"I hit something\". The right way is a question asked fresh every frame: <b>is anything solid one pixel below me?</b> One line, and it is the one thing the jump will need to know next step.",
    trial="Nothing visible changes yet. <code>P[\"g\"]</code> is being answered sixty times a second; step 14 is the first thing that asks."),
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
20: dict(why="Coins, and with them the first words on the screen. A font, a <b>surface</b> of text, and <code>blit</code> to copy it on -- that is all a HUD is. The hearts arrive with it, because lives have been counted since step 12 and nobody could see them; and so does the GAME OVER card, so the frozen screen from step 12 finally says why it froze.",
    trial="Walk into a coin: it vanishes and the count goes up. Five hearts top right. Fall five times and the card comes up; space starts again."),
21: dict(why="The same loop, one more letter, and the first thing that can kill you. A spike is drawn as a triangle and calls <code>die()</code> the moment you touch it. Nothing about it is a lie -- yet.",
    trial="Walk into the spike on purpose. Back to the start."),
22: dict(why="Here is the whole game, in one flag. Touch the wizard once and <code>cursed</code> becomes true; he vanishes and never comes back. Nothing else changes yet -- the flag is set and nothing reads it. The next step is what makes it matter.",
    trial="Walk into the purple block. It disappears, and everything looks exactly the same. That is on purpose."),
23: dict(why="The first lie. A <code>%</code> looks exactly like a brick -- same colour, same edge -- but <code>solid()</code> stops counting it the moment you are cursed. <code>LIARS</code> names every letter that will ever lie, six of them, though you have met one: a set you add to five more times is a set you never finished.",
    trial="Cross the bridge at columns 10-12 before the wizard: solid. Take the curse and come back: you fall straight through."),
24: dict(why="Click, and a stone leaves your middle at a speed set by how far away you clicked. Two rules are in from the start, because both were bugs the first time this game was written. A stone is born <b>inside</b> whatever square you are standing on, so for <code>CLEAR</code> frames it ignores everything -- otherwise standing on a coin killed every throw. And the wizard's letter stays in the level after he is gone, so his empty square must not count.",
    trial="Click anywhere. The stone flies, drops under its own half-gravity, and vanishes on whatever it hits."),
25: dict(why="What the stone tells you. Every square it strikes -- and the ring around it -- goes into <code>hit</code> with a countdown of <code>SHOWN</code> frames. For that half second a liar is drawn in its <code>TRUTH</code> colour, and everything struck wobbles (<code>shaken()</code>), so a brick that shook and stayed the same has told you it was honest. Then the countdown runs out and the level lies again. A truth that lasted for ever would make the second lap of every level a memory test.",
    trial="Throw a stone at the bridge. Half a second of dull brown -- the hologram admitting it -- and a wobble. Then it is a brick again."),
26: dict(why="The first lie that helps you. <code>t</code> is drawn exactly like a spike, and before the curse it kills exactly like one. Once you can see, it is a trampoline that throws you higher than you can jump -- <code>BOUNCE</code> is -12.3 against your jump's -9.2.",
    trial="Fall into the pit before the curse: you die. Get cursed, fall in again: you are fired back out."),
27: dict(why="And the first lie that hurts. <code>x</code> is drawn as a coin and counts as one -- until you are cursed, and then touching it kills you. The truth is worse than the illusion, which is the joke of the whole game.",
    trial="Take the coin above the bridge before the curse. Then get cursed and try the same square."),
28: dict(why="<code>~</code> is solid and simply never drawn. It is not invisible because of a bug -- <code>solid()</code> counts it, and the drawing code skips it unless a pebble has found it.",
    trial="Walk right past the bridge and over the gap in the floor that is not a gap. Then throw a pebble at it to see the shape you are standing on."),
29: dict(why="Floor with a clock. Stand on a <code>c</code> and its clock starts: <code>CRACK</code> frames of wobbling while it still holds you, <code>AWAY</code> frames as nothing at all, and then it builds itself back. Squares that have dropped are in <code>gone</code>, which <code>cells()</code> and the stone both respect. The last branch is worth reading: if you are standing in the square when its time is up, it waits rather than re-forming through you.",
    trial="Stand on a cracked brick, feel the wobble, step off, and watch it come back. Stay on it and you drop -- and there is nothing under it."),
30: dict(why="The cruellest letter. <code>!</code> is drawn as the green exit, and touching it sends you back to the start. A pebble tells them apart before you commit to the run.",
    trial="Touch the exit halfway along the level. Then throw a pebble at the one at the far right to check it before you walk into it."),
31: dict(why="If the traps sit in the same squares every run, the game is memorised in two goes. So <code>?</code> means spike-or-trampoline and <code>&amp;</code> means brick-or-hologram, rolled fresh each run from a <b>seed</b> -- one starting number that makes the dice repeatable when you need to re-open a bug.",
    trial="Press R a few times. Nothing looks different -- a spike and a trampoline are drawn the same, and so are a brick and a hologram -- but the floor is not the same floor."),
32: dict(why="The danger with dice: a run of <code>?</code> could come up all spikes, or a run of <code>&amp;</code> all hologram over a hole, and the level would be impossible. Two lines fix it forever: if the run contains nothing safe, force one square back to safe.",
    trial="Press R a lot. Every roll leaves a way through, whether or not you can see which square it is."),
33: dict(why="Five string-lists in a list, and <code>load(i)</code> is now the only thing that knows how to start one: measure it, roll its dice, find the P, wipe the last level's coins and rubble, drop you at the spawn. Touching <code>G</code> calls it with the next number. Level I goes back to being the real one from the finished game.",
    trial="Reach the green exit. Level II starts, with its own lie: the floor there is threaded with holograms."),
34: dict(why="The bar along the top: the level's name, its clock, the coins. That is all of it, on purpose -- a total clock would say nothing anyone reads, and the wind will have its own way of showing itself. <code>clock_str</code> turns frames into minutes and seconds.",
    trial="Five names, five clocks, and a title card for the first two seconds of each level."),
35: dict(why="Wind is an acceleration, not a speed: added to <code>vx</code> every frame, 2.2 times harder in the air where nothing resists it. <code>sin</code> is what makes it swing from pushing you right to pushing you left and back. Two lists, assigned once: <code>GUST</code> is how hard each level blows, <code>SWING</code> how fast it turns around -- multiplying <code>frames</code> before the sine speeds the swing up without touching the strength.",
    trial="You start cursed on level IV. Stand still and you still move. Jump straight up and see where you land."),
36: dict(why="The curse, made visible. <code>warp</code> is a jolt that fades a little every frame; <code>wobble()</code> photographs the finished frame and pastes it back in shifted bands -- it bends what you see, never what is true. <code>gusts()</code> draws the wind as streaks, and the sum inside it matters: the air is added up frame by frame into <code>blown</code>. Drawn at <code>frames * wind</code> instead, the streaks would follow how fast the wind is <i>changing</i>, and run against the shove for half of every swing.",
    trial="Touch the wizard: the screen tears. Cursed on a windy level, the streaks always blow the way you are being pushed."),
37: dict(why="You were being killed in mid-air and teleported away in the same frame, which reads as a glitch rather than a death. So death takes a moment now: your body is copied into <code>body</code>, the world holds still, and the body falls under the same gravity you do until it lands on the first thing that will hold it. Notice what <code>step()</code> does on the very first line -- while <code>dying</code> is counting, no input is read and no clock runs.",
    trial="Touch a killer coin in mid-air. You drop, you land on the floor, and only then are you put back at the start."),
38: dict(why="Sound, with no files at all. A note is a wave: a number that goes up and down, and how fast it does that is the pitch. <code>note()</code> writes the samples straight into an <code>array</code> of whole numbers and hands the bytes to the mixer; the fade at the end is not decoration -- a wave that stops dead is a click in the speaker. <code>TUNES</code> is every sound the game will ever make, written as notes, once: a jump slides up, a death slides down, the curse is one long slide all the way to the bottom. <b>Noise</b> is a random number every sample, which is what a thrown stone and the wind sound like -- and the wind plays all the time on its own channel, with <code>gusts()</code> setting how loud it is every frame.",
    trial="Jump, take a coin, throw a stone, die. Then go cursed to a windy level and listen to the gust build before it takes your jump away. Change 300 to 900 in the jump and hear what you did."),
39: dict(why="Everything so far has been drawn by <code>pygame.draw</code> -- rectangles, circles, triangles. A picture is not different in kind: <code>blit</code> copies one surface onto another, exactly where you say. <code>convert_alpha()</code> re-packs the file the way the screen wants it, which makes every later copy far quicker, and <code>subsurface</code> takes one 32x32 square out of a sheet without copying anything at all.",
    trial="The ground is stone now, and everything else is still a coloured box. That is the whole trick of this chapter: a picture if there is one for that letter, the old shape if there is not."),
40: dict(why="Six more letters, and one strip. The coin is not one picture but six, side by side in a file, and a clock of its own -- <code>beat</code> ticks once per frame <b>drawn</b>, not once per frame the world moves, so pictures keep animating when the world is held still. That matters in the opening, where the world waits for you to read.",
    trial="Coins spin, spikes are metal, bricks are brick. Only the player, the wizard and the doors are still shapes."),
41: dict(why="A sprite sheet is one long picture with the frames laid out in a row. <code>cut()</code> slices it and, more importantly, <b>trims</b> each frame; <code>facing()</code> builds every frame flipped as well, once, at startup, because flipping sixty times a second is slow. <code>pose()</code> answers one question -- which frame of her to draw right now -- and every later step adds a rule <i>above</i> its last line rather than rewriting it.",
    trial="She breathes. The same idle animation the artist drew, standing exactly where the white box used to."),
42: dict(why="One picture is a statue; the game needs to know which of four things you are doing. Not on the ground and going up is a jump, going down is a fall, moving fast on the ground is a run, and anything else is standing still. <code>facing()</code> builds every frame flipped as well, once, at startup -- flipping is slow, and a game does this sixty times a second.",
    trial="Run, and she runs. Jump, and she jumps. Turn around, and she turns around."),
43: dict(why="She is dark olive, the graveyard is nearly black, and against it she disappears. A rim fixes it without touching the artwork: <code>mask.from_surface</code> asks which pixels are drawn at all, <code>to_surface</code> paints that shape one flat colour, and drawing it eight times one pixel out in each direction leaves a one-pixel outline with the sprite on top.",
    trial="The same character, now readable against the night. Turn the rim off in <code>facing()</code> and see how badly you need it."),
44: dict(why="Two pictures behind the level, each drawn as many times as it takes to cover the screen. Dividing the camera before the shift is the whole idea: the far layer moves a quarter as fast as you, the near one a half, and your eye reads that difference as distance. That is <b>parallax</b>, and it costs one division.",
    trial="Walk. The moon barely moves, the mausoleums slide past, the ground races. Change the 4 to a 1 and the sky sticks to your face."),
45: dict(why="Until now a revealed lie was a duller colour, and you had to remember which colour meant what. Now the stone shows you the <b>thing itself</b>: a hole where the brick was, rubble, a ledge, a slime, a fire. Nothing to learn.",
    trial="Throw a stone at anything. For half a second you see what it really is -- and the fire moves, because that entry is a list of eight pictures rather than one."),
46: dict(why="The exit was a green rectangle, which is the last place the game still looked like a diagram. It is a door now, eight frames of it. The exit that lies is the same door until a stone finds it, and then it is red with something standing in it.",
    trial="Find the exit. Then throw a stone at one and see which kind you were walking into."),
47: dict(why="A white circle became a stone. The interesting line is the rotation: turning it by a number that grows with the position makes it <b>tumble</b>, which is what a thrown rock does. Aligning it to its direction of travel instead would read as an arrow, and an arrow is a different promise.",
    trial="Throw. It turns as it flies, and lands like a rock rather than pointing like a dart."),
48: dict(why="The pack has a throw animation, but the artist drew a big white arc across the middle of it -- a sword sweep, not a throw. <code>de_swoosh()</code> finds it by counting: every other frame has about forty near-white pixels, that one has over a thousand. Count them, and if there are too many, rub that colour out.",
    trial="Click. She throws, properly, and the arc that made it look like a sword is gone."),
49: dict(why="Dust where the stone lands. A puff is three numbers -- where, and how old -- and eight pictures played over half a second. The list is walked backwards with a copy, <code>PUFFS[:]</code>, because the loop deletes from it as it goes.",
    trial="Throw a stone at a wall. Dust comes off it."),
50: dict(why="You already fall before you die; now you can see it. The same eight-frame animation the artist drew for a death, played once over the fall, drawn wherever the body ends up rather than wherever you will restart.",
    trial="Walk into the spikes. She goes down where she landed, and only then are you put back."),
51: dict(why="Telling someone the controls in words is a wasted corner of the screen. The pack has every key as pixel art, in a grid -- so it is the same <code>subsurface</code> you used on the tileset, and the corner says arrow, arrow, space, click, R without a word of English.",
    trial="Bottom left. Four keys and a mouse, and nothing to read."),
52: dict(why="He has three animations: standing, being hit, and casting. Which one plays is a straight <code>if</code> on two counters, and which way he faces is a comparison -- if you are to his left, he is drawn from the mirrored list. A character who does not turn to face you reads as scenery.",
    trial="He is alive now, breathing on the spot. The other two animations have nothing to trigger them yet."),
53: dict(why="The opening plays itself. She is not driven by you: <code>scene_step()</code> calls the game's own <code>step()</code> with the right key held, so she walks at exactly the speed you will, on the same physics. She stops short of him, so the wizard-touch never fires, and swings. He flinches with the animation you gave him last step, raises his hands, and the curse lands when his spell finishes -- not when you press a key. And <code>reset()</code> gains one line: a fresh run starts at the title card, so a game over or a win sends you back through the story. There is no version of this game where you and the wizard share a platform outside it, because the game makes no sense uncursed.",
    trial="Press space on the title. Watch her walk up and hit him, and watch him take her eyes for it."),
54: dict(why="Seven lines, in bubbles above whoever is speaking. The bubble is measured from the text it holds -- <code>get_rect</code> then <code>inflate</code> for the padding, <code>clamp_ip</code> so it can never run off the screen -- and the tail is a triangle pointing back down at the speaker. His last line starts the spell, and the curse lands when the spell finishes rather than when you press a key.",
    trial="Read it through. He takes your eyes at the end of his own animation, and the game begins."),
55: dict(why="The levels have been Python strings all along, which means editing one meant editing the program. Now they are a text file, written out once and read back at startup. The bars around each row hold the width open, because an editor that trims trailing spaces would quietly narrow a level. A file that makes no sense is refused, with a reason -- a half-typed edit must never break the game you are playing.",
    trial="Look at the three coins at the start of level I -- then look for them in the <code>L1</code> strings on the left. They are not there. The file has already overruled the code, which is the whole point. Open <code>levels.txt</code>, move something, save, and start it again."),
56: dict(why="Six of the made-up sounds are replaced with recordings from a free pack. They are loaded last, on purpose, so each one quietly takes the place of the arithmetic version with the same name -- delete a line from <code>RECORDED</code> and you hear the square wave again.",
    trial="One press of space is a jump and a coin at once. Click for a stone, and walk right off the edge for the last one. The same events, in someone else's hands."),
57: dict(why="A tune is notes one after another, and you already have a function that makes a note. Four bars of A minor -- eight notes to a bar, the top half an octave up -- joined end to end into one array and handed to the mixer with <code>loops=-1</code>. It plays on its own channel, so it never interrupts a jump or a coin.",
    trial="Four bars of A minor, on their own channel, under everything."),
}


# ------------------------------------------------------------------ line notes
# Keys are the exact line, stripped. Prefix "N:" to mean "only at step N" -- the
# same line can mean different things at different steps.

NOTES = {
    # step 38 -- every sound, once
    "VOLUME = {                                       # how loud each one is, 0 to 1: the music sits": "one table of levels, so no sound is a surprise: the music at 0.30 is the reference, a warning sits above it, a blip below",
    "sound.set_volume(VOLUME[name])           # so no effect shouts over another": "every sound gets its level from the table, the made-up ones and the recordings alike",
    'pygame.mixer.Channel(1).set_volume(VOLUME["wind"] * min(1.0, abs(w) / max(GUST)))': "the wind's own level, scaled by how hard it is blowing against the strongest gust in the game",
    "TUNES = {                                        # every sound, as notes: (from, to, seconds)": "the whole soundtrack of effects on one page: each one a list of notes, from a pitch to a pitch over some seconds",
    '"curse": [(120, 38, 1.30)],                  # him taking your eyes: long, and all the way down': "the lowest note in the game, and the longest",
    'def note(f0, f1, secs, kind="square"):': "build a note from nothing but arithmetic: square for a game sound, sine for music, noise for wind and stone",
    'if kind == "noise":': "no pitch at all",
    "wave = random.uniform(-1.0, 1.0)": "a random number every sample is what a hiss is",
    "for name, parts in TUNES.items():": "every sound in the table",
    "tune += note(f0, f1, secs)": "the notes, one after another",
    'SOUND["throw"] = pygame.mixer.Sound(buffer=note(0, 0, 0.12, "noise").tobytes())': "a stone leaving your hand: a tenth of a second of noise",
    'SOUND["wind"] = pygame.mixer.Sound(buffer=note(0, 0, 2.0, "noise").tobytes())': "two seconds of noise, played end to end for ever",
    'pygame.mixer.Channel(1).play(SOUND["wind"], loops=-1)   # always blowing; how loud is': "its own channel, so it never interrupts a jump or a coin",
    "pygame.mixer.Channel(1).set_volume(0.0)                # for gusts() to say, every frame": "silent until there is wind",
    'if "wind" in SOUND:                           # the hiss follows the gust': "the wind you can hear: loudness set from wind() itself, every frame",
    'beep("gameover")': "four notes down",
    'beep("bounce")': "longer and higher than a jump",
    'beep("win")': "four notes up",
    'beep("throw")': "a tenth of a second of noise",
    'beep("hit")': "your swing landing",
    'beep("curse")': "one long slide, all the way down",
    'beep("talk")': "one blip per line",
    'tune += note(f, f, 0.5, "sine")': "half a beat each, joined end to end; sine, so it sounds like music rather than a game",

    # --- lines in the form the revision gave them
    'buf = 0': 'frames since the jump key went down, for the buffer',
    'PLAYER = {}': 'her animations by name, each a list of frames',
    'SKY = []': 'the two background layers, far and near',
    'TRUE = {}': 'what each liar really is, as a picture',
    'DOOR_OK = []': 'the way out, eight frames of it',
    'DOOR_BAD = []': 'the same door as it really is, once a stone has found it out',
    'DEMON = []': 'what stands in the wrong door',
    'SMOKE = []': 'eight frames of a plume',
    'PUFFS = []': 'every plume in the air: where, and how old',
    'KEYS = {}': 'the arrow keys, space and the mouse, as pictures for the corner of the screen',
    'WIZ, WIZ_L = [], []': 'him standing, facing right and facing left',
    'HURT, HURT_L = [], []': 'him flinching, both ways',
    'scene, wiz_at = "title", None                  # title -> walk -> hit -> cast -> None': 'one word for what the opening is doing; wiz_at is his square, found once the level is loaded',
    'def pose():': 'which frame of her to draw right now. Every later step adds a rule above the last line',
    'if ch in "#%~c":': "every kind of brick, including the ones that lie. They all look the same, on purpose",
    'VW, VH = 960, 640                     # the window, in pixels': 'the window, in pixels',
    'reset()': 'a whole fresh run -- which, right now, means standing at the start',
    'SPAWN = (64, 288)                                     # where you start': 'where you start, in pixels. From step 7 the level says where',
    'P = {}                                                # where you are, and how fast': 'your position and speed, filled in by place()',
    'GRAV = 0.35                           # pull per frame': 'added to vy every frame: falling gets faster the longer it lasts',
    'MAXFALL = 12                          # the fastest you may fall': 'uncapped, a long fall would cover a whole tile per frame and pass through a floor',
    'TILE = 32                             # one square of the world': 'one square of the world is 32 pixels; column 5 starts at pixel 160',
    'level = 0                                             # which level is loaded': 'which level is loaded: 0 is the first',
    'rows = LEVELS[i]': 'the level asked for, as its list of strings',
    'LVL = [r.ljust(COLS) for r in rows]': 'pad every row to the same width, so LVL[r][c] never runs off the end',
    'LEVELS = [L1]                          # the levels, in order: one so far': 'the levels, in order. One so far; a function that takes a level number is ready for five',
    'load(0)': 'the first level',
    'LOOK = {"#": (150, 110, 70), "%": (150, 110, 70), "c": (150, 110, 70),': 'every letter the game will ever have, and the colour it is drawn in. Assigned once',
    'if ch == " ":': 'air: nothing to draw',
    'col = LOOK[ch]': 'the colour this letter is drawn in',
    'x, y = int(P["x"]), int(P["y"])': 'where you are, as whole pixels',
    'SPAWN = (0, 0)                                        # where you start, found by load()': 'found by load() now: wherever the level has its P',
    'if over: return                               # the run is finished': 'the run is finished: no input, no movement, until space starts a new one',
    'if won: return                                # and so is the game': 'and so is the game',
    'P["g"] = False': 'not on the ground, until step() says so',
    'JUMP = -9.2                           # the kick upward, pixels per frame': 'up is negative. The kick you get on the frame you press',
    'P["jump"] = False': 'not mid-jump',
    'BUFFER = 8                            # a press up to 8 frames early still counts': 'a press up to 8 frames before you land still counts',
    'CUT = 0.42                            # let go early and the jump is cut to this': 'let go early while still rising and the rise is cut to this fraction',
    'ACC, AIR, FRIC = 0.55, 0.32, 0.72     # how fast you gain speed, on the ground and off it, and lose it': 'how fast you gain speed on the ground, in the air, and how fast you lose it',
    'here = P["x"]                                   # what the camera follows': 'what the camera follows -- you, unless a later step says otherwise',
    'cam = max(0, min(int(here) + PW // 2 - VW // 2, COLS * TILE - VW))': 'the camera: you in the middle, clamped so it never shows past either end',
    'coins = 0': 'how many you have taken',
    'taken.clear()': 'a fresh level has all its coins',
    'if (c, r) in taken:': 'a coin you took is not drawn',
    'if ch in "ox":': 'coins, honest and not: the same circle for both, on purpose',
    'if ch in "G!":': 'the way out, and the exit that lies: the same green rectangle for both',
    'col = (90, 230, 190)': 'exit green',
    'hud = "coins %d" % coins': 'the words along the top: one number, for now',
    'if over: return                               # the run is finished': 'the run is finished: a card over everything, and draw stops here',
    'font, big = pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 30)': 'two sizes: one for the bar, one for the message in the middle',
    'draw(scr, font, big)': 'draw() takes both fonts from the day it takes any',
    'if ch in "^t":': 'spikes, and the spikes that are not: the same triangle',
    'cursed = False': 'the curse: not yet',
    'if ch == "W" and not wizard:': 'once he is gone, his square is air',
    'LIARS = set("%tx~c!")                 # every letter that lies, including the ones you have not met yet': 'every letter that lies, including the five you have not met yet',
    'pebbles = []': 'every stone in the air right now',
    'pebbles.append([cx, cy, dx / d * sp, dy / d * sp, 0])   # the last number is its age': 'where it is, how fast, and its age in frames',
    'ch = tile(c, r)': 'what is written in the square it has reached',
    'if ch != " " and (c, r) not in taken:': 'something is written here, and it is not a coin you already took',
    'hit = {}': 'squares a stone has struck, each with a countdown',
    'TRUTH = {"%": (108, 84, 66), "t": (146, 162, 148), "x": (206, 168, 96),': 'what each liar looks like once a stone has found it out: the same hue, duller. Assigned once',
    'shake = hit.get((c, r), 0)               # frames of truth this square has left': 'how many frames of truth this square has left, or 0',
    'seen = shake > 0                         # telling the truth, for now': 'telling the truth, for now',
    'if lie: col = TRUTH[ch]': 'for half a second, the truth colour',
    'BOUNCE = -12.3                        # a trampoline: stronger than JUMP': 'a trampoline kicks harder than a jump',
    'if ch == "t" and not cursed:': 'before the curse, spikes that spring are just spikes',
    'if ch == "t" and cursed:                  # the spikes that spring': 'the spikes that spring',
    'if ch == "x" and cursed:': 'once cursed, the killer coin kills',
    'if ch == "x" and (c, rw) not in taken:   # the killer coin still counts': 'and before it, it is just a coin',
    "frames = 0                                            # this level's clock": "this level's clock, in frames",
    'gone = set()': 'squares that have dropped away: neither drawn nor solid',
    'crack = {}': 'every cracked brick you have stood on, and how far its clock has got',
    'if ch != " " and (c, r) not in gone:': 'something is written here and it has not dropped away',
    'if (c, r) in gone:': 'a square that has dropped away is not drawn',
    'if ch == "!":': 'the exit that is not one',
    'if seen and ch == "!": col = TRUTH["!"]': 'found out: the fake exit in its true colour',
    "seed = 0                                              # this run's dice": "this run's dice. The same seed rolls the same level every time",
    'won = False': 'the last exit has been reached',
    'if ch == "G":': 'the way out',
    'GUST = [0.0, 0.0, 0.20, 0.25, 0.30]   # how hard the wind blows, level by level': 'how hard it blows, level by level. Assigned once',
    'return 0.0': 'before the wizard there is no wind at all',
    'blown = 0.0                                           # how far the air has travelled': 'how far the air itself has travelled, added up frame by frame',
    'warp = 26.0                           # the biggest jolt in the game': 'the biggest jolt in the game',
    'if cursed or warp > 0:': 'the curse, and every jolt',
    'if dying: here = body[0]                     # the camera stays with your body': 'the camera stays with your body, not where you will restart',
    'x, y = int(body[0]) - cam, int(body[1])': 'where you fell, not where you restart',
    'pic = PIC.get(ch)': 'a picture, if there is one for this letter yet',
    'who = pose()[face]': 'the frame of her to draw, facing the way she points',
    'seq = PLAYER["idle"]': 'standing still',
    'return seq[(beat // 6) % len(seq)]': 'one picture every six frames: ten a second',
    'return [{1: f, -1: pygame.transform.flip(f, True, False)}': 'each frame twice: as drawn, and mirrored',
    'return [{1: rimmed(f), -1: rimmed(pygame.transform.flip(f, True, False))}': 'and now each with its rim',
    'scene, casting = "cast", CURSE': 'the swing is over: he raises his hands',
    'scene = "talk"': 'the swing is over: now he speaks',
    'if scene:': 'the story is on: a veil, and the words',
    # --- the lines where names first arrive, so every one is explained on the day it appears
    "LVL, COLS, ROWS = [], 0, 0                            # the level, once it is measured": "LVL is the level as a list of strings; COLS and ROWS are its size, worked out by load()",
    "coy = 0": "coyote frames left: how long ago you were last on the ground",
    "wizard = True": "he is standing in the level until you touch him",
    "58+:frames += 1": "this level's clock, and now the only one",
    '58+:KEYS["space"] = icon(9, 8)': "no R icon: a control you draw is a promise, and R no longer keeps one",
    "warp = 0.0": "how hard the screen is bending right now: a jolt that fades a little every frame",
    "COIN = []": "the six pictures of a spinning coin, filled in by art()",
    "FIRE = []": "eight frames of flame: a coin that kills, once a stone has found it",
    "SHOT = []": "the picture of the stone you throw",
    "SWOOSH = {(240, 240, 240), (214, 221, 225)}    # the two colours of the sword arc": "the two near-whites the artist used for the arc across the throw frame, so they can be rubbed out",
    "THROW = 16                            # frames the throwing animation lasts": "a bit over a quarter of a second",
    "throwing = 0": "frames left of the throw animation; while it is above zero it wins over every other pose",
    "CAST, CAST_L = [], []": "him taking your eyes, facing right and facing left",
    "HIT_FOR, CURSE = 16, 40               # he flinches for one, casts for the other": "the flinch lasts 16 frames; the spell takes 40, and the curse lands when it is done",
    "flash = casting = 0": "frames left of his flinch, and of his spell",
    'scene, wiz_at = "title", None                  # title -> walk -> hit -> talk -> cast -> None': "one word for what the opening is doing; wiz_at is his square, found once the level is loaded",
    "TALK = [                                       # who says it, and what": "the conversation, in order. The last line is his, and it starts the spell",
    "said = 0                                       # how far through TALK we are": "counts up with every press of space",
    'tip = "YOU MADE IT OUT \u2014 space to run it again" if won else (': "space, not R: R is gone",
    "if (over or won) and e.key == pygame.K_SPACE: reset()": "space starts a fresh run from the game over screen and from the win screen alike",
    "LEGEND = [": "the top of levels.txt: what every letter means, written into the file so it explains itself",
    'LEVELS_TXT = os.path.join(os.path.dirname(ART), "levels.txt")': "the text file the levels are read from, next to the game",
    "def load_recorded():": "six wav files from a free pack, loaded after the made-up sounds so they replace them by name",
    "face = 1                                              # 1 right, -1 left": "which way she points. Set from her speed, so she keeps facing the way she is sliding",
    'NAMES = ["I. The Curse", "II. The Floor Lies", "III. The Gaps Lie", "IV. Nothing Holds", "V. The Gauntlet"]': "one name per level, for the bar along the top",

    # step 66 -- a clock that keeps running
    "beat = 0                                              # the pictures' own clock": "the world's clock stops when the world does; this one never does",
    "global beat": "draw() is about to change it",
    "beat += 1                                     # one tick per frame drawn,": "once per picture, whether or not anything moved",

    # step 67 -- less in the bar
    'hud = "%s   %s   coins %d" % (NAMES[level], clock_str(frames), coins)': "the level and its clock and the coins. Nothing read the total, and the streaks already say the wind",

    # step 68 -- taking R away
    'for i, k in enumerate(("left", "right", "space", "click")):': "the keys that do something, and only those: a control you draw is a promise",

    # step 47 -- a picture instead of a colour
    'ART = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art")': "the art folder, found from this file rather than from wherever you happened to be standing when you ran it",
    "PIC = {}": "one picture per letter of the level, filled in by art()",
    "def picture(name):": "open one file from the art folder",
    "return pygame.image.load(os.path.join(ART, name)).convert_alpha()": "convert_alpha keeps the see-through parts and re-packs it the way the screen wants",
    "def art():": "every picture, opened once, before the first frame",
    'sheet = picture("tiles.png")': "one file with every tile in it, in a grid",
    "cell = lambda c, r: sheet.subsurface((c * TILE, r * TILE, TILE, TILE)).copy()": "subsurface is a window onto the same pixels -- no copying -- so .copy() takes a real one",
    'PIC["#"] = cell(5, 1)                          # the ground: one 32x32 square of it': "column 5, row 1 of the tile sheet",
    "if pic:": "a picture if there is one for this letter, the old shape if there is not",
    "scr.blit(pic, box)": "blit copies one surface onto another. This is how everything is drawn from here on",

    # step 48 -- the rest of the tiles
    'PIC["%"] = PIC["~"] = cell(5, 1)               # a lie has to look like the truth': "the same picture as the real brick, or it would not be a lie",
    "bed = pygame.Surface((TILE, TILE), pygame.SRCALPHA)": "an empty square with a see-through channel, to build a tile in",
    'PIC["^"] = PIC["t"] = bed                      # two 16-pixel spikes fill a square': "and the trampoline looks exactly like them",
    'if ch == "~" and not seen:': "floor you cannot see stays unseen until a stone finds it",

    # step 49 -- cutting a strip into frames
    "def cut(sheet, n):": "a strip of n frames, side by side, cut into a list",
    "wide, out = sheet.get_width() // n, []": "every frame is the same width, so the width of one is the whole divided by how many",
    "box = frame.get_bounding_rect()": "the smallest rectangle holding every pixel that is actually drawn",
    "out.append(frame.subsurface(box).copy() if box.width else frame.copy())": "trimmed, so a 150-wide frame with a small character in it stops being mostly air",
    'PLAYER["idle"] = facing(cut(picture("player_idle.png"), 8))': "eight frames of standing still",

    # step 50 -- run, jump, fall
    "def facing(frames):": "every frame, ready to face either way, built once at the start",
    'if P["vx"] > 0.4: face = 1                    # you face the way you move': "0.4 rather than 0, or you would flicker while sliding to a stop",
    'seq = PLAYER["jump"] if P["vy"] < 0 else PLAYER["fall"]': "going up or coming down: two different pictures",

    # step 51 -- a rim
    "def rimmed(pic, colour=(226, 236, 255)):": "a one-pixel outline, so she does not vanish into the night",
    "edge = pygame.mask.from_surface(pic).to_surface(setcolor=colour,": "a mask is which pixels are drawn at all; to_surface paints that shape one flat colour",
    "out.blit(edge, (dx, dy))    # the shape, eight times, one pixel out each way": "eight offsets: four sides and four corners",
    "out.blit(pic, (1, 1))           # then the sprite itself, on top": "in the middle of the two-pixel border the eight copies made",

    # step 52 -- the sky
    "scr.fill(SKY[0].get_at((4, 4)))               # the night, taken from the art": "one pixel out of the picture, so the sky above it matches exactly",
    "for layer, slower in ((SKY[0], 4), (SKY[1], 2)):": "the far layer divided by 4, the near one by 2",
    "scr.blit(layer, (x - (cam // slower) % wide, VH - layer.get_height()))": "dividing the camera is the whole of parallax: move less, look further away",

    # step 53 -- the truth as a picture
    "def fit(pic):": "trim a picture, scale it to one square, and stand it on the floor of that square",
    "def tall(pic, height):": "scale to a height, keeping its shape",
    'TRUE["%"] = cell(8, 8)                         # a hole. There was never a brick': "the darkest tile in the sheet",
    'FIRE[:] = [fit(picture("fire/%d.png" % i)) for i in range(1, 9)]': "eight frames of it, so the fire moves",
    "if seen and ch in TRUE:                  # for half a second, the truth": "the same countdown as before; only what it draws has changed",
    "if isinstance(pic, list):            # and a fire moves": "some entries are one picture and some are a list of them",

    # step 54 -- two doors
    "green.fill((70, 255, 190, 255), special_flags=pygame.BLEND_RGBA_MULT)": "multiply every pixel by that colour: the red door becomes a green one",
    "if fake:                             # and what is waiting in it": "the reason it throws you back",

    # step 55 -- a stone
    "spun = pygame.transform.rotate(SHOT[0], (pb[0] + pb[1]) * 3 % 360)": "turned by where it is, so it tumbles. Turning it to face its direction would read as an arrow",

    # step 56 -- the throw
    "def de_swoosh(frames):": "the artist drew a white arc across the throw frame; this rubs it out",
    "if white > 200:": "forty near-white pixels is a highlight, a thousand is the arc",
    "if throwing > 0:                              # mid-throw, whatever else": "the throw animation wins over standing, running and falling",
    "throwing = THROW": "and the animation runs itself down in step()",

    # step 57 -- dust
    "def puff(x, y):": "a plume of smoke: where it is, and how old",
    "def smoke(scr, cam):": "draw every plume and age it. Gone in half a second",
    "for p in PUFFS[:]:": "a copy of the list, because the loop deletes from it",
    "puff(pb[0], pb[1] + 6)               # dust off whatever it struck": "a little below the stone, so it comes off the surface",

    # step 58 -- going down
    'seq = PLAYER["death"]': "the animation the artist drew for it",

    # step 59 -- the keys
    'keys = picture("keys.png")': "every key on a keyboard, as pixel art, in one grid",
    "icon = lambda c, r: pygame.transform.scale(": "the same subsurface trick as the tile sheet, then doubled in size",

    # step 60 -- the wizard
    'at_you = P["x"] + PW / 2 < box.centerx + cam': "are you to his left? Then he is drawn from the mirrored list",
    "if casting > 0:                      # taking your eyes": "one counter per animation, and a plain if to choose",
    "wz = seq[min(len(seq) - 1, (CURSE - casting) * len(seq) // CURSE)]": "the counter, spread across however many frames the animation has",

    # step 61 -- he walks up and hits him
    "OPEN = [                                       # what you read before anything moves": "two lines, and then it plays itself",
    'scene, wiz_at = "title", None                  # title -> walk -> hit -> talk -> cast -> None': "one word for what the opening is doing right now",
    "def find_wizard():": "which square he is standing in -- read out of the level, not written down twice",
    "def scene_step():": "one frame of the opening. You are not driving",
    "step(0, 1)                                 # hold right, and nothing else": "her legs on the game's own physics, so she walks at the speed you will walk at",
    'if P["x"] + PW >= wiz_at[0] * TILE - 12:   # close enough to swing': "and stopping short means the game's own wizard-touch never fires",
    'P["vx"] = 0.0                          # stop, or she runs on the spot': "the animation is chosen by your speed, and she is not moving any more",
    "flash = HIT_FOR                        # the moment it lands": "halfway through the swing, not at the start of it",
    "def advance():": "space or a click. Only the parts you read wait for you",
    "if scene:                              # the story is playing": "so the keys do nothing and the world holds still",

    # step 62 -- a conversation
    "def bubble(scr, font, text, cx, top, colour):": "a speech bubble, measured from the text it holds",
    "box = t.get_rect(centerx=cx, top=top).inflate(26, 16)": "the text's own rectangle, grown by the padding",
    "box.clamp_ip(pygame.Rect(8, 8, VW - 16, VH - 16))": "clamp_ip shoves it back inside the screen if it would hang off the edge",
    "tx = max(box.left + 14, min(cx, box.right - 14))": "the tail points at the speaker, but never off the end of its own bubble",
    'scene, casting = "cast", CURSE          # he raises his hands': "his last line starts the spell; the curse lands when the spell finishes",

    # step 63 -- levels you can edit
    "def dump_levels():": "write the game's own levels out, once, so there is something to edit",
    'out += ["|%s|" % r.ljust(wide) for r in rows]': "the bars hold the width open: an editor that trims trailing spaces cannot narrow a level",
    "def read_levels():": "a name in brackets, then its rows, each inside a pair of bars",
    "def load_levels():": "take the levels from the file, if it makes sense",
    "if not levels or bad:": "a half-typed edit must not break the game you are playing",

    # step 64 -- sounds from a pack
    'RECORDED = {"jump": "jump.wav", "coin": "coin.wav", "die": "hurt.wav",': "six recordings, by the name of the sound each one replaces",
    "load_recorded()": "loaded last, so each one quietly takes the place of the made-up version",

    # step 65 -- four bars
    "def music():": "a tune is notes one after another, and you already have a function that makes a note",
    "f = chord[i % 3] * (2 if i >= 4 else 1)   # the top half of the bar, an octave up": "doubling a pitch is exactly one octave",
    "pygame.mixer.Channel(0).play(music(), loops=-1)": "loops=-1 means for ever, and its own channel means it never interrupts a jump",

    # step 37 -- the two ends of the level
    'P["x"] = min(max(P["x"], 0.0), COLS * TILE - PW)': "the level has two ends: max() keeps you off the left edge, min() off the right",

    # step 38 -- lives
    "LIVES = 5                             # how many you start with": "five hearts; lives counts down from this",
    "lives = LIVES": "how many you have left, right now",
    "def place():": "stand at the start of the level, costing nothing. Loading a level wants this; dying wants die()",
    "37+:def die():": "the same standing-still, but it costs you a life first",
    "lives -= 1": "one heart, spent",
    "place()": "back to the start",
    "for i in range(LIVES):": "one heart per life you started with",
    "heart(scr, VW - 30 - i * 22, 10, i < lives)": "the ones past lives are drawn dark, so you can see what you lost",
    "def heart(scr, x, y, full):": "a heart, drawn rather than loaded: two circles and a triangle",

    # step 39 -- game over
    "over = False": "true when the last heart has gone, and the run is finished",
    "if lives <= 0:": "that was the last one",
    "over = True": "nothing moves again until you ask for a new run",
    "return place()": "put the body down and stop",
    "if over and e.key == pygame.K_SPACE: reset()": "space on the game over screen: a whole new run",
    "if over:": "the run is finished: a card over everything, and draw stops here",
    "veil = pygame.Surface((VW, VH), pygame.SRCALPHA)": "a surface with an alpha channel, so it can be see-through",
    "veil.fill((8, 6, 12, 185))": "near-black, and 185 out of 255 opaque: the graveyard still shows underneath",
    'again = font.render("press space to try again", True, (222, 216, 206))': "the only thing left to do",
    'card = big.render("GAME OVER", True, (240, 120, 130))': "the only red text in the game",

    # step 40 -- you fall before you die
    "FALL = 60                             # frames your body takes to come to rest": "one second, at 60 frames a second",
    "dying, body = 0, [0.0, 0.0, 0.0]": "dying counts down while your body falls; body is where it is and how fast",
    'body[0], body[1], body[2] = P["x"], P["y"], P["vy"]': "copy yourself into the body, keeping the speed you were hit at",
    "dying = FALL": "and start the clock. Nothing else in the game moves until it runs out",
    "def fall():": "one frame of a body falling. The same gravity you have, and the same floors",
    'if solid(ch) or ch in "^t":': "ground, spikes or a trampoline: anything will hold a body",
    "if body[1] > ROWS * TILE:": "it fell out of the world, so there is nothing to watch",
    "if dying <= 0:": "the body has come to rest, and you have been dead long enough",
    "if dying:                                     # you are on your way down": "no keys, no clock, no wind: the world waits",
    "return fall()": "one frame of the fall instead of one frame of you",

    # step 41 -- a brick that comes back
    "CRACK, AWAY = 18, 30                  # a cracked brick wobbles, drops, comes back": "0.3 seconds of warning, half a second of nothing",
    "for cell in list(crack):                      # every cracked brick has a clock": "list() takes a copy, because the loop deletes from crack as it goes",
    "crack[cell] += 1": "one more frame on this brick's clock",
    "if crack[cell] == CRACK:": "the warning is over",
    "gone.add(cell)                        # the warning is over: it drops": "into gone, which means neither drawn nor solid",
    "elif crack[cell] >= CRACK + AWAY:": "its time away is up",
    "if prect().colliderect(pygame.Rect(cell[0] * TILE, cell[1] * TILE, TILE, TILE)):": "you are standing in the square it wants to fill",
    "crack[cell] = CRACK + AWAY        # you are standing in its way: wait": "hold the clock there and try again next frame, rather than building a brick through you",
    "del crack[cell]; gone.discard(cell)": "the clock is thrown away and the brick is solid again",
    'if P["g"]:                                    # a brick you stand on starts its clock': "and once started, stepping off will not save it",
    'if ch == "c" and (c, rw) not in crack:': "only start a clock that is not already running",
    "crack[(c, rw)] = 0": "that exact square, from frame zero",

    # step 42 -- the truth lasts half a second
    "SHOWN = 30                            # frames a struck square tells the truth": "half a second, and then it lies again",
    "for cell in list(hit):                        # the truth fades on its own": "one frame off every countdown, wherever they are",
    "hit[cell] -= 1": "a frame closer to lying again",
    "if hit[cell] <= 0:": "its half second is up",
    "del hit[cell]": "and the square goes back to looking like whatever it likes",
    "hit[(c + i, r + j)] = SHOWN": "the square and the ring around it, each with its own countdown",
    'if ch != " " and (c, r) not in gone and (c, r) not in taken:': "something is written here, it has not broken away, and it is not a coin you already took",
    "box = box.move(shaken(shake), 0)": "a struck square wobbles, so an honest one answers you too",
    "def shaken(n):": "the wobble: a sine that shrinks as the countdown runs out",

    # step 43 -- two things that stopped a stone
    "CLEAR = 6                             # frames a stone ignores what it is inside": "long enough to leave your hand",
    "pb[4] += 1": "one frame older",
    'if ch == "W" and not wizard:              # he has gone: his square is air': "his letter stays in the level after he does, and it was eating stones",
    "if pb[4] < CLEAR:                         # still leaving your hand": "without this, the square you are standing on kills every throw",

    # step 44 -- wind that turns around faster
    "SWING = [1.0, 1.0, 1.0, 1.5, 2.2]     # and how fast it turns around": "level V flips from pushing you right to pushing you left in about five seconds",
    "if not cursed:": "before the wizard there is no wind at all",
    "return GUST[level] * math.sin(frames * SWING[level] / 110.0)": "sin swings between -1 and 1; multiplying frames by SWING makes it swing faster",

    # step 45 -- streaks that blew the wrong way
    "blown += w * 26                               # this frame's worth of moving air": "the old code used frames * w, which follows how fast the wind is changing, not which way it blows",
    "x = int(i * 217 + blown) % (VW + 200) - 100": "now a streak moves at 26 * w, which can never disagree with the shove you feel",

    # step 46 -- sound out of arithmetic
    "SOUND = {}": "name -> a Sound the mixer can play",
    "rate, out = 22050, array.array(\"h\")": '22050 samples a second, each one a whole number ("h" is a 16-bit signed integer)',
    "total, phase = int(rate * secs), 0.0": "how many samples to write, and how far round the wave we are",
    "phase += 2 * math.pi * (f0 + (f1 - f0) * i / total) / rate": "walk round the circle a little further each sample; how far is the pitch",
    "wave = math.sin(phase)": "a smooth wave, between -1 and 1",
    "wave = 1.0 if wave > 0 else -1.0": "a square wave: all the way up, or all the way down",
    "out.append(int(wave * (1.0 - i / total) ** 3 * 8000))": "fade it out as it goes, or the end is a click, and 8000 is the volume",
    "def make_sounds():": "every sound in the game, built once when the game starts",
    "pygame.mixer.quit()": "pygame.init() may already have opened the mixer at its own settings, and a second init() would be ignored",
    "pygame.mixer.init(22050, -16, 1, 512)": "the same rate note() writes at, 16-bit, one channel, a small buffer so a jump sounds on time. Get this wrong and every sound plays at the wrong pitch",
    "except pygame.error:": "a machine with no sound card should still play the game",
    "def beep(name):": "play one, if it exists",
    "make_sounds()": "build the sounds before the first frame",
    'beep("jump")': "a note that slides up, which is what makes it sound like a jump",
    'beep("die")': "and one that slides down",

    # step 1
    "import pygame": "the game library itself",
    "def main():": "the whole game lives in here: set up once, then loop forever",
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

    # step 2
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
    'P["vy"] = min(P["vy"] + GRAV, MAXFALL)': "add gravity every frame, but never let falling pass 12 pixels a frame",
    '4:P["y"] += P["vy"]': "the same trick as x: speed changes position",

    # step 5
    'ROW = " " * 60                       # one empty row, so the sky is not 13 lines of spaces': "a name for an empty row, so the thirteen rows of sky above the level do not fill the screen with spaces",
    "L1 = [": "the level: a list of strings, one per row, every row the same width so you can count columns straight off it",
    "def tile(c, r):": "what letter is at column c, row r?",
    'return LVL[r][c] if 0 <= r < ROWS and 0 <= c < COLS else " "': "off the edge of the map counts as empty air, so nothing else ever has to check for edges",
    "ROWS = len(LVL)": "and the number of rows is the height",

    # step 6
    "def draw(scr):": "everything you see, rebuilt from nothing every frame",
    "for r in range(ROWS):": "every row...",
    "for c in range(COLS):": "...every column",
    "box = pygame.Rect(c * TILE, r * TILE, TILE, TILE)": "grid to pixels: where that square lands on screen",
    "pygame.draw.rect(scr, (0, 0, 0), box, 1)": "the last argument is a line width, so this draws only the outline",
    "draw(scr)": "one call now does all the drawing",

    # step 7
    'SPAWN = next((c * TILE, r * TILE) for r in range(ROWS) for c in range(COLS) if LVL[r][c] == "P")': "search every square for the P and stop at the first. Column 5 becomes 5 x 32 = 160 pixels",
    'LVL = [r.replace("P", " ") for r in LVL]': "then erase it, so the P is never drawn or stood on",
    'P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)': "start where the level says, standing still",

    # step 8
    "def prect():": "your box, right now, as a Rect",
    'return pygame.Rect(int(P["x"]), int(P["y"]), PW, PH)': "Rect wants whole pixels, so int() drops the fraction",

    # step 9
    "def cells(rect):": "every tile a box overlaps, usually two to six of them",
    "for r in range(rect.top // TILE, (rect.bottom - 1) // TILE + 1):": "the -1 means touching an edge exactly does not count as being inside",
    "yield c, r, ch": "hand them back one at a time as the loop asks, instead of building a list",

    # step 10
    "def solid(ch):": "which letters stop you",
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
    'if P["y"] > ROWS * TILE:': "fell past the bottom row",
    "return die()": "back to the start, and nothing else this frame",

    # step 13
    "# ponytail: 1px probe instead of trusting penetration -- sub-pixel gravity never sinks a full pixel": "ponytail: is the tag this author puts on a deliberate shortcut. Here: gravity of 0.35 can leave you a third of a pixel inside a brick, and a one-pixel probe does not care",
    'P["g"] = P["vy"] >= 0 and any(solid(ch) for _, _, ch in cells(prect().move(0, 1)))': "g for grounded. Move the box one pixel down and ask what is there. any() is True if at least one answer is",

    # step 14
    "def step(left, right, pressed=False, held=False):": "two new arguments: pressed is the frame the button went down, held is whether it is still down",
    'if pressed and P["g"]:': "on the ground, and the button went down this exact frame",
    'P["vy"] = JUMP': "the whole jump. Everything after this step is about when it is allowed",
    "if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w): pressed = True": "KEYDOWN fires once, which is exactly what a jump needs",
    "pressed = False": "true for one frame only: the frame the key goes down",

    # step 15
    "COYOTE = 7                            # you may still jump 7 frames after the edge": "named after the cartoon coyote, who only falls once he looks down",
    'coy = COYOTE if P["g"] else coy - 1': "a countdown that refills every time you touch the ground, and ticks away while you are in the air",
    "if pressed and coy > 0:": "pressed now, and grounded recently enough",
    'P["vy"], coy = JUMP, 0': "jump, and spend the credit so one ledge cannot give two jumps",

    # step 16
    "buf = BUFFER if pressed else buf - 1": "the same kind of countdown, for the button instead of the ground",
    "if buf > 0 and coy > 0:": "pressed recently AND grounded recently -- the two credits together",
    'P["vy"], buf, coy = JUMP, 0, 0': "jump, and spend both",

    # step 17
    'P["vy"], buf, coy, P["jump"] = JUMP, 0, 0, True': "jump, spend both credits, and remember that this rise is yours to cut",
    'if P["jump"] and not held and P["vy"] < JUMP * CUT:': "let go early while still rising fast?",
    'P["vy"], P["jump"] = JUMP * CUT, False    # let go early, hop short': "cut the rise to 42% of full: a tap becomes a hop",
    'if P["vy"] >= 0:': "once you are falling there is nothing left to cut",

    # step 18
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

    # step 21
    'if ch == "^":': "a real spike, which never lied to anybody",

    # step 22
    "def reset():": "a whole fresh run: wizard back, curse off, coins zero",
    "wizard, cursed = False, True": "he vanishes, and you are cursed. Nothing reads that flag yet",
    "pygame.draw.rect(scr, (160, 80, 220), box.inflate(-8, 0))": "the wizard: purple, and narrower than his square",

    # step 23

    # step 24
    "def throw(tx, ty):": "tx, ty is where you clicked, in world pixels",
    'cx, cy = P["x"] + PW / 2, P["y"] + PH / 2': "throw from your middle, not your corner",
    "dx, dy = tx - cx, ty - cy": "the arrow from you to the click",
    "d = max(1.0, (dx * dx + dy * dy) ** 0.5)": "its length. ** 0.5 is a square root, and max(1) stops a click on yourself dividing by zero",
    "sp = max(4.5, min(16.0, d / 20.0))        # close click = soft lob, far click = hard throw": "clamped at both ends, so no click is useless and none is absurd",
    "def pebble_step():": "one frame for every pebble in the air",
    "for pb in pebbles[:]:": "the [:] makes a copy, so removing pebbles while looping over them is safe",
    "pb[3] += GRAV * 0.5": "pebbles fall too, at half weight",
    "pb[0] += pb[2]; pb[1] += pb[3]": "the same speed-changes-position rule as you",
    "if not (0 <= c < COLS and 0 <= r < ROWS):": "left the map",
    "throw(e.pos[0] + cam, e.pos[1])": "e.pos is where on screen you clicked; adding cam makes it a place in the level",
    "pebble_step()": "move the pebbles once per frame, like everything else",

    # step 25
    "def edge(col):": "a darker version of any colour, for the outline",
    "lie = seen and ch in LIARS": "revealed, and actually a liar. Honest tiles look identical either way",

    # step 26
    'P["vy"], P["g"], P["jump"] = BOUNCE, False, False': "fire upward, and forget you were grounded or mid-jump -- so the cut in step 17 cannot shorten a trampoline",

    # step 27

    # step 28

    # step 29

    # step 30

    # step 31
    "def roll(row, rng):": "one row of the level, and this run's dice",
    'if out[i] in "?&":': "found a rollable square",
    "while j < len(out) and out[j] == ch:": "find the whole run of them, e.g. ????",
    'safe, other = ("t", "^") if ch == "?" else ("#", "%")': "which of the two you can survive",
    "span = [rng.choice((safe, other)) for _ in range(j - i)]": "roll each square in the run",
    "out[i:j] = span": "write the rolled squares back over the ?s",
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
    "rng = random.Random(seed * 977 + i)": "a different roll per level, still repeatable from the one seed",
    "if level + 1 < len(LEVELS):": "another level to go?",
    "return load(level + 1)": "start it, and do nothing else this frame",
    "won = True": "that was the last one",

    # step 34
    "def clock_str(f):": "frames into minutes and seconds: 60 frames is a second, 3600 a minute",
    'return "%d:%02d" % (f // 3600, f // 60 % 60)': "%02d pads to two digits, so it reads 1:05 and not 1:5",
    "def draw(scr, font, big):": "two fonts now: small for the bar, big for the message",
    "if frames < 140 and not won:": "for the first couple of seconds of a level, show its name instead of the tip",
    "scr.blit(t, t.get_rect(center=(VW // 2, 90)))": "get_rect(center=...) centres the text without any arithmetic",

    # step 35
    "def wind():": "how hard it is blowing, right now",
    'P["vx"] += wind() * (1.0 if P["g"] else 2.2)   # gusts shove hardest in the air': "feet on the ground resist it; mid-jump you are a leaf",
    "pb[2] += wind() * 1.6": "your pebbles get blown off course too",

    # step 36
    "warp = max(0.0, warp - 0.16)                  # every jolt fades, even on the game over screen": "a jolt fades a little every frame -- before the run-is-over check, or the last death's jolt would tear the game over screen for ever",
    "warp = 22.0": "the fake exit: a hard visual jolt as it throws you back",
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
    "WIZ_L": V("wizard, facing left", "WIZ mirrored, for when you are standing on his left. Built once at startup, because flipping every frame is slow."),
    "HURT_L": V("wizard flinching, facing left", "HURT mirrored."),
    "CAST_L": V("wizard casting, facing left", "CAST mirrored."),
    "SWOOSH": V("swoosh colours", "The two near-white colours the artist used for the arc across the throw frame. de_swoosh() rubs out exactly these, and nothing else.", "const"),
    "LEGEND": V("legend", "The comment block at the top of levels.txt: what every letter means, so the file explains itself to whoever opens it.", "const"),

    # --- the pictures
    "ART": V("art folder", "Where the pictures live: the art folder beside the steps folder, found from this file rather than from wherever you were standing when you ran it.", "const"),
    "PIC": V("pictures", "One picture per letter of the level. Filled in by art(); anything not in here is still drawn as a shape."),
    "COIN": V("coin frames", "The six pictures of a spinning coin."),
    "PLAYER": V("player frames", "Her animations, by name: idle, run, jump, fall, throw, swing, death. Each one a list of frames, each frame ready to face either way."),
    "SKY": V("sky layers", "The two background pictures: the moon and clouds, and the graveyard in front of them."),
    "TRUE": V("true pictures", "What each liar really is, as a picture rather than a colour: a hole, rubble, a ledge, a slime, a fire."),
    "FIRE": V("fire frames", "Eight frames of a flame -- what a coin that kills really is."),
    "DOOR_OK": V("the way out", "The exit, eight frames of it, tinted green."),
    "DOOR_BAD": V("the way back", "The same door in its own red, drawn only once a stone has found out what it is."),
    "DEMON": V("demon", "What is standing in the wrong door."),
    "SHOT": V("stone", "The picture of the stone you throw."),
    "SMOKE": V("smoke frames", "Eight frames of a plume of dust."),
    "PUFFS": V("puffs", "Every plume in the air right now: where it is and how old it is."),
    "KEYS": V("key icons", "The arrow keys, space, the mouse and R, as pictures, for the corner of the screen."),
    "WIZ": V("wizard frames", "Him standing. WIZ_L is the same list, mirrored, for when you are on his left."),
    "HURT": V("wizard flinching", "Him being hit. HURT_L is the mirrored version."),
    "CAST": V("wizard casting", "Him taking your eyes. CAST_L is the mirrored version."),
    "picture": F("picture(name)", "a file name", "a Surface",
                 "Opens one file from the art folder. convert_alpha() re-packs it the way the screen wants, which makes every later blit far quicker."),
    "art": F("art()", "nothing", "nothing", "Opens every picture the game needs, once, before the first frame."),
    "cut": F("cut(sheet, n)", "a strip and how many frames are in it", "a list of frames",
             "Slices a sprite sheet, and trims each frame down to the pixels actually drawn."),
    "facing": F("facing(frames)", "a list of frames", "a list of dicts, one per frame",
                "Each frame ready to face either way: [1] is right, [-1] is left. Built once at the start, because flipping sixty times a second is slow."),
    "rimmed": F("rimmed(pic, colour)", "a sprite", "the same sprite with a one-pixel rim",
                "A mask is which pixels are drawn at all. Painted one colour and stamped eight times, one pixel out in each direction, it becomes an outline."),
    "fit": F("fit(pic)", "a picture", "a picture exactly one square across",
             "Trims it, scales it to a tile, and stands it on the floor of that tile -- so a slime sits on the ground instead of floating."),
    "tall": F("tall(pic, height)", "a picture and a height", "a scaled picture", "Scales to a height, keeping its shape."),
    "de_swoosh": F("de_swoosh(frames)", "the frames of the throw", "the same frames, cleaned",
                   "The artist drew a white arc across one frame, which reads as a sword sweep. Counting near-white pixels finds it -- forty is a highlight, a thousand is the arc -- and it is rubbed out."),
    "puff": F("puff(x, y)", "a point in the world", "nothing", "Starts a plume of smoke there."),
    "smoke": F("smoke(scr, cam)", "the screen and the camera", "nothing", "Draws every plume and ages it. They drift up and are gone in half a second."),
    "blit": F("scr.blit(pic, at)", "a picture and where to put it", "nothing",
              "Copies one surface onto another. Every picture in this game is drawn with this."),
    "subsurface": F("sheet.subsurface(box)", "a rectangle", "a window onto the same pixels",
                    "Not a copy: a view. .copy() takes a real one when you need it."),
    "convert_alpha": F("pic.convert_alpha()", "nothing", "the same picture, re-packed",
                       "Rearranges the pixels the way the screen stores them, keeping the see-through parts. Every blit afterwards is far quicker."),
    "mask": V("mask", "pygame's yes/no map of which pixels of a picture are drawn at all. Used here to make an outline.", "lib"),
    "face": V("facing", "Which way she is pointing: 1 for right, -1 for left. Set from your speed, not from the key, so she keeps facing the way she is sliding."),
    "throwing": V("throwing", "Frames left of the throwing animation. While it is above zero it wins over standing, running and falling."),
    "THROW": V("throw frames", "How long the throwing animation lasts: 16 frames, a bit over a quarter of a second.", "const"),
    "flash": V("flash", "Frames left of the wizard's flinch."),
    "casting": V("casting", "Frames left of the wizard's spell. The curse lands when it reaches zero, not when you press a key."),
    "HIT_FOR": V("hit for", "How long he flinches: 16 frames.", "const"),
    "CURSE": V("curse frames", "How long the curse takes to cast: 40 frames, about two thirds of a second.", "const"),

    "beat": V("beat", "The pictures' own clock. It ticks once per frame drawn, so animation keeps going while the world is frozen for the story."),

    # --- the opening
    "scene": V("scene", "What the opening is doing right now: title, walk, hit, talk, cast -- or None once it is over and the game is yours."),
    "said": V("said", "How many lines of the conversation have been read."),
    "wiz_at": V("wizard's square", "Which square he is standing in, read out of the level rather than written down twice."),
    "OPEN": V("opening lines", "The two lines you read before anything moves.", "const"),
    "TALK": V("the conversation", "Who says what, in order. The last line is his.", "const"),
    "scene_step": F("scene_step()", "nothing", "nothing",
                    "One frame of the opening. Her walk calls the game's own step(), so she moves at exactly the speed you will."),
    "advance": F("advance()", "nothing", "nothing", "Space or a click: turns the page. Only the parts you read wait for you."),
    "find_wizard": F("find_wizard()", "nothing", "his column and row, or None", "Finds the W in the level."),
    "bubble": F("bubble(scr, font, text, cx, top, colour)", "the screen, the words, and where to point", "nothing",
                "A speech bubble measured from the text it holds, clamped inside the screen, with a tail pointing back at whoever spoke."),

    # --- the levels file, and the music
    "LEVELS_TXT": V("levels file", "The text file the levels are read from, beside the game.", "const"),
    "dump_levels": F("dump_levels()", "nothing", "nothing", "Writes the built-in levels out once, so there is something to edit."),
    "read_levels": F("read_levels()", "nothing", "the names and the rows", "Reads them back: a name in brackets, then rows inside bars."),
    "load_levels": F("load_levels()", "nothing", "nothing", "Uses the file if it makes sense, and keeps the built-in levels if it does not."),
    "RECORDED": V("recordings", "Six wav files from a free pack, by the name of the sound each one replaces.", "const"),
    "load_recorded": F("load_recorded()", "nothing", "nothing", "Loaded last, so each recording quietly replaces the made-up version of the same name."),
    "music": F("music()", "nothing", "a Sound", "Four bars of A minor, built out of notes one after another, played on its own channel for ever."),

    # --- lives, dying, and the end of a run
    "LIVES": V("lives", "How many hearts you start a run with: 5. The count that goes down is lives, in lower case.", "const"),
    "lives": V("lives", "How many hearts are left. die() spends one; reset() puts them back."),
    "over": V("over", "True once the last heart has gone. The loop stops stepping, draw() puts up GAME OVER, and space starts a new run."),
    "place": F("place()", "nothing", "nothing", "Puts you at the start of the level, standing still. Loading a level uses this -- it costs nothing. Being killed uses die(), which costs a life."),
    "heart": F("heart(scr, x, y, full)", "the screen, a corner, and whether it is a life you still have", "nothing",
               "One heart, drawn with two circles and a triangle. full=False draws it dark."),
    "FALL": V("fall time", "How many frames your body takes to come to rest after you are killed: 60, one second. Nothing else moves in that time.", "const"),
    "dying": V("dying", "Frames left of your body falling. While it is above zero, step() does nothing but drop the body."),
    "body": V("body", "Where your body is and how fast it is falling: [x, y, vy]. A plain list, because it is three numbers and nothing else."),
    "fall": F("fall()", "nothing", "nothing", "One frame of your body falling: the same gravity you have, and it stops on the first thing that will hold it -- ground, spikes or a trampoline. When it lands, place() puts you back."),

    # --- the brick that comes back
    "CRACK": V("crack time", "How many frames a cracked brick wobbles before it drops away: 18, about a third of a second.", "const"),
    "AWAY": V("away time", "How many frames a cracked brick stays gone before it builds itself back: 30, half a second.", "const"),
    "crack": V("crack clocks", "Every cracked brick you have stood on, and how many frames its clock has run. A square leaves this dict when the brick is whole again."),

    # --- the truth, and how long it lasts
    "SHOWN": V("shown for", "How many frames a struck square tells the truth: 30, half a second.", "const"),
    "hit": V("hit", "Squares a stone has struck, each with a countdown. While a square is in here it is drawn as what it really is, and it wobbles. When the countdown runs out it goes back to lying."),
    "pose": F("pose()", "nothing", "the frame of her to draw right now",
              "One question, answered by the newest rule that applies: dying, throwing, in the air, running, or standing still. Each later step adds a rule above the last line."),
    "shaken": F("shaken(n)", "frames of truth left", "a number of pixels",
                "How far a struck square is knocked sideways. The wobble shrinks as the countdown runs down, so it settles rather than stopping dead."),
    "CLEAR": V("clear of you", "How many frames a thrown stone ignores what it is flying through: 6. Without it, a stone thrown while you stand on something dies in your hand.", "const"),

    # --- the wind
    "SWING": V("swing rate", "How fast the wind turns around, level by level. It multiplies frames inside the sine, so a bigger number means the wind flips from right to left sooner -- without blowing any harder.", "const"),
    "blown": V("blown", "How far the moving air has travelled, added up frame by frame. The streaks are drawn from this, so they can never run against the wind."),

    # --- sound
    "SOUND": V("sounds", "Every sound in the game, by name. Built once, at startup, out of arithmetic."),
    "VOLUME": V("volumes", "How loud each sound plays, 0 to 1, in one table. The music at 0.30 is the reference: warnings a little above it, blips below, and the wind never above 0.35.", "const"),
    "TUNES": V("tunes", "Every sound the game makes, written as notes: a list of (from pitch, to pitch, seconds) per name. Assigned once.", "const"),
    "note": F("note(f0, f1, secs, kind)", "a starting pitch, an ending pitch, a length, and square, sine or noise", "an array of samples",
              "A note that slides from one pitch to the other. A wave is a number that goes up and down; how fast it does that is the pitch. It fades to nothing at the end, because a wave that stops dead is a click."),
    "make_sounds": F("make_sounds()", "nothing", "nothing", "Builds every sound and puts it in SOUND. If there is no sound card it gives up quietly and the game plays in silence."),
    "beep": F("beep(name)", "the name of a sound", "nothing", "Plays it, if it was built."),
    "array": V("array", "Python's own tight list of numbers, all of one type. \"h\" means a 16-bit whole number, which is exactly what a sound card wants.", "lib"),
    "tobytes": F("tobytes()", "nothing", "raw bytes", "Turns an array of numbers into the bytes the mixer reads."),
    "mixer": V("mixer", "pygame's sound part. init() opens the sound card; Sound(buffer=...) makes a playable sound out of raw bytes.", "lib"),

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
    "picture": {"name": "a file name inside the art folder"},
    "cut": {"sheet": "a strip of frames", "n": "how many frames are in it"},
    "facing": {"frames": "the frames of one animation"},
    "rimmed": {"pic": "a sprite", "colour": "the colour of the rim"},
    "fit": {"pic": "a picture"}, "tall": {"pic": "a picture", "height": "how tall to make it"},
    "de_swoosh": {"frames": "the frames of the throw"},
    "puff": {"x": "where, across", "y": "where, down"},
    "smoke": {"scr": "the screen", "cam": "how far the camera has scrolled"},
    "bubble": {"scr": "the screen", "font": "the small font", "text": "what is said",
               "cx": "the middle of whoever said it", "top": "where the bubble's top goes",
               "colour": "the border colour: red for him, blue for you"},
    "heart": {"scr": "the surface to draw on", "x": "the left edge", "y": "the top edge",
              "full": "true for a life you still have"},
    "shaken": {"n": "how many frames of truth the square has left"},
    "note": {"f0": "the pitch it starts on", "f1": "the pitch it ends on",
             "secs": "how long it lasts", "kind": "square for a game sound, sine for music, noise for wind"},
    "beep": {"name": "which sound to play"},
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
        (38, "One frame of you -- unless you are dying, in which case one frame of your body falling instead."),
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
