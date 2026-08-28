"""Trust No One -- step 4: Gravity.   Run it:  python3 steps/step04.py"""

import sys   # sys is Python's own settings; this game uses
import pygame   # the game library itself

VW, VH = 960, 640   # the window, in pixels

SPD = 3.6                             # top walking speed, pixels per frame
# 0.35 looks like nothing until it has been added sixty times a second
GRAV, MAXFALL = 0.35, 12              # pull per frame, and the fastest you may fall
PW, PH = 20, 28                       # how big you are

P = {"x": 64.0, "y": 288.0, "vx": 0.0, "vy": 0.0}     # where you are, and how fast

def step(left, right):   # one frame of you
    P["vx"] = (right - left) * SPD   # True minus False is 1 minus 0
    # add gravity every frame, but never let falling pass 12 pixels a frame
    P["vy"] = min(P["vy"] + GRAV, MAXFALL)

    P["x"] += P["vx"]
    # the same trick as x: speed changes position
    P["y"] += P["vy"]

def main():   # the whole game lives in here
    pygame.init()   # wake the library up
    scr = pygame.display.set_mode((VW, VH))   # make the window
    pygame.display.set_caption("Trust No One")   # the title on the window bar
    clk = pygame.time.Clock()   # our metronome
    while True:   # the game loop
        for e in pygame.event.get():   # everything that happened since the last frame
            if e.type == pygame.QUIT:   # the X button on the window
                return
        k = pygame.key.get_pressed()   # which keys are held down right now
        step(k[pygame.K_LEFT] or k[pygame.K_a], k[pygame.K_RIGHT] or k[pygame.K_d])
        scr.fill((25, 25, 35))   # paint over the last frame, or it smears
        pygame.draw.rect(scr, (240, 235, 220), (P["x"], P["y"], PW, PH), border_radius=4)
        pygame.display.flip()   # show the frame you just drew
        clk.tick(60)   # sleep so the loop runs 60 times a second

if __name__ == "__main__":   # run the game when you run this file
    main()   # start it
