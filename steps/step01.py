"""Trust No One -- step 1: A window that stays open.   Run it:  python3 steps/step01.py"""

# the game library itself
import pygame

# the window, in pixels
VW, VH = 960, 640                     # the window, in pixels

# the whole game lives in here: set up once, then loop forever
def main():
    # wake the library up
    pygame.init()
    # make the window. scr is the surface everything gets drawn onto
    scr = pygame.display.set_mode((VW, VH))
    # the title on the window bar, when you run the file yourself
    pygame.display.set_caption("Trust No One")
    # our metronome
    clk = pygame.time.Clock()
    # the game loop. Forever, until we quit
    while True:
        # everything that happened since the last frame: keys, clicks, the window closing
        for e in pygame.event.get():
            # the X button on the window
            if e.type == pygame.QUIT:
                # leave main(), which ends the program
                return
        # paint over the last frame, or it smears. The three numbers are red, green, blue
        scr.fill((25, 25, 35))
        # show the frame you just drew
        pygame.display.flip()
        # sleep so the loop runs 60 times a second, not 4000
        clk.tick(60)

# run the game when you run this file, and stay quiet if another program loads it
if __name__ == "__main__":
    # start it
    main()
