import pygame as pg
import numpy as np

class Aplication():
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        pg.init()
        self.FPS = 120
        self.running = True
        self.clicking = False

    def update(self):
        self.screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                exit()
            if pg.mouse.get_pressed()[0]:
                self.clicking = True
            else: 
                self.clicking = False

        # do stuff
        #
        #
        pg.display.flip()
        pg.display.set_caption(str(round(self.clock.get_fps(), 3)))
        self.clock.tick(self.FPS)


if __name__ == '__main__':
    main = Aplication()
    while main.running:
        main.update()
