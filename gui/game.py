import pygame as pg
import os

class Game():
    def __init__(self):
        self.pieces_img = [pg.image.load('ressources\' + i + '.png') for i in ['white_0', 'black_0', 'white_1', 'black_1', 'white_2', 'black_2', 'white_3', 'black_3', 'white_4', 'black_4', 'white_5', 'black_5' ]]
        
g = Game()
print(g.pieces_img)