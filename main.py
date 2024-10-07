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
        self.drawing(50)

        pg.display.flip()
        pg.display.set_caption('Chess Bot vs Player Game   |   ' + str(round(self.clock.get_fps(), 1)))
        self.clock.tick(self.FPS)
    
    def drawing(self, a):
        for i in range(self.WIDTH//(a*2)):
            for j in range(self.HEIGHT//(a)):
                pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(i*a, j*a, a, a))
                pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(i*a +a, j*a, a, a))


if __name__ == '__main__':
    main = Aplication()
    while main.running:
        main.update()
