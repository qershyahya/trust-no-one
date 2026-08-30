"""Trust No One -- step 3: Keys move the box.   Run it:  python3 steps/step03.py"""

import pygame   # the game library itself

VW, VH = 960, 640                     # the window, in pixels

PW, PH = 20, 28                       # how big you are
# 3.6 x 60 frames = 216 pixels a second
SPD = 3.6                             # top walking speed, pixels per frame

SPAWN = (64, 288)                                     # where you start
P = {}                                                # where you are, and how fast

def reset():   # a whole fresh run
    """A whole fresh run: everything back to the beginning."""
    place()   # back to the start

def place():   # stand at the start of the level
    """At the start of the level, standing still."""
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)   # start where the level

# one frame of you. Called once per trip round the loop
def step(left, right):
    # True minus False is 1 minus 0. Hold both and they cancel to 0, which is right
    P["vx"] = (right - left) * SPD

    # speed changes position. This one line is movement
    P["x"] += P["vx"]

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
        # which keys are held down right now, as opposed to just pressed
        k = pygame.key.get_pressed()
        # arrows or A and D, either way
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d])
        scr.fill((25, 25, 35))   # paint over the last frame, or it smears
        pygame.draw.rect(scr, (240, 235, 220), (P["x"], P["y"], PW, PH), border_radius=4)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
