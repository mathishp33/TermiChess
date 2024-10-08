import pygame as pg
import os
import numpy as np

WHITE = 16
BLACK = 0

KING = 1
QUEEN = 2
BISHOP = 3
KNIGHT = 4
ROOK = 5
PAWN = 6

class Game():
    def __init__(self):
        self.board = np.ndarray(shape=(8, 8), dtype= int)
        self.board[0][0] = WHITE | PAWN
        

class Pieces():
    def __init__(self):
        self.board = Game()
        self.pieces_img, index = {}, 0b0000
        for i in ['white_1', 'black_1', 'white_2', 'black_2', 'white_3', 'black_3', 'white_4', 'black_4', 'white_5', 'black_5', 'white_6', 'black_6' ]:
            index = bin(int(index)-16) if 'white' in i else bin(int(index)-16) 
            self.pieces_img[index] = pg.image.load('\\ressources\\' + i + '.png')
            self.pieces = [self.pieces.append([i, j, self.board.board[i][j]]) for i in len(8) for j in range(8) if not self.board.board[i][j] == 0]
            
