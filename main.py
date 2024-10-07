import pygame as pg
import numpy as np

class Aplication():
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.FPS = 120
        self.