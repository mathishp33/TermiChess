import pygame as pg
import numpy as np
import gui.game as game

class Aplication():
    def __init__(self):
        self.size = 64
        self.RES = self.WIDTH, self.HEIGHT = self.size*8, self.size*8
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        pg.init()
        self.FPS = 120
        self.running = True
        self.clicking = False
        self.game = game.Pieces()

    def update(self):
        self.screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                exit()
                pg.quit()
            if pg.mouse.get_pressed()[0]:
                self.clicking = True
            else:
                self.clicking = False

        # do stuff
        self.drawing(50)

        pg.display.flip()
        pg.display.set_caption('Chess Bot vs Player Game   |   ' + str(round(self.clock.get_fps(), 1)))
        self.clock.tick(self.FPS)

    def drawing(self, a):
        colors = ((237, 212, 175), (170, 125, 92))
        for i in range(8):
            for j in range(8):
                pg.draw.rect(self.screen, colors[(i+j)%2], pg.Rect(self.size*i, self.size*j, self.size, self.size))
                
        for i in self.game.pieces:
            idle = i[2].get_rect(center=(i[0]*self.size/2+self.size/2, i[1]*self.size/2+self.size/2))
            self.screen.blit(i[2], idle)
