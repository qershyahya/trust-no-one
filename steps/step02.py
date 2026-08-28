"""Trust No One -- step 2: A box on the screen.   Run it:  python3 steps/step02.py"""

import sys   # sys is Python's own settings; this game uses
import pygame   # the game library itself

VW, VH = 960, 640   # the window, in pixels

# player width and height, in pixels. Smaller than a 32-pixel tile, on purpose
PW, PH = 20, 28                       # how big you are

# a dictionary: four numbers, each with a name. x and y are where; vx and vy are how fast, per
# frame
P = {"x": 64.0, "y": 288.0, "vx": 0.0, "vy": 0.0}     # where you are, and how fast

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    clk = pygame.time.Clock()   # our metronome
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
