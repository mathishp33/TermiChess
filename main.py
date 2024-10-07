import pygame as pg
import numpy as np

class Aplication():
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.FPS = 120
        self.running = True
        self.clicking = False

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if pg.mouse.get_pressed()[0]:
                self.clicking = True
            else: 
                self.clicking = False
