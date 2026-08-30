"""Trust No One -- step 2: A box on the screen.   Run it:  python3 steps/step02.py"""

import pygame   # the game library itself

VW, VH = 960, 640                     # the window, in pixels

# player width and height, in pixels. Smaller than a 32-pixel tile, on purpose
PW, PH = 20, 28                       # how big you are

# where you start, in pixels. From step 7 the level says where
SPAWN = (64, 288)                                     # where you start
# your position and speed, filled in by place()
P = {}                                                # where you are, and how fast

# a whole fresh run: wizard back, curse off, coins zero
def reset():
    """A whole fresh run: everything back to the beginning."""
    # back to the start
    place()

# stand at the start of the level, costing nothing. Loading a level wants this; dying wants
# die()
def place():
    """At the start of the level, standing still."""
    # start where the level says, standing still
    P.update(x=float(SPAWN[0]), y=float(SPAWN[1]), vx=0.0, vy=0.0)

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    clk = pygame.time.Clock()   # our metronome
    # a whole fresh run -- which, right now, means standing at the start
    reset()
    while True:   # the game loop
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
        scr.fill((25, 25, 35))   # paint over the last frame, or it smears
        # you are an off-white rectangle. That is enough to start
        pygame.draw.rect(scr, (240, 235, 220), (P["x"], P["y"], PW, PH), border_radius=4)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
