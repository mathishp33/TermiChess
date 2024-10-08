import pygame as pg
import os

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
        self.boardSize = 512
        self.board = [0 for i in range(64)]
        self.board[0] = WHITE | PAWN

        self.pieces_tex = {
            0: None,

            WHITE | KING: pg.image.load("resources\\white_1.png"),
            WHITE | QUEEN: pg.image.load("resources\\white_2.png"),
            WHITE | BISHOP: pg.image.load("resources\\white_3.png"),
            WHITE | KNIGHT: pg.image.load("resources\\white_4.png"),
            WHITE | ROOK: pg.image.load("resources\\white_5.png"),
            WHITE | PAWN: pg.image.load("resources\\white_6.png"),

            BLACK | KING: pg.image.load("resources\\black_1.png"),
            BLACK | QUEEN: pg.image.load("resources\\black_2.png"),
            BLACK | BISHOP: pg.image.load("resources\\black_3.png"),
            BLACK | KNIGHT: pg.image.load("resources\\black_4.png"),
            BLACK | ROOK: pg.image.load("resources\\black_5.png"),
            BLACK | PAWN: pg.image.load("resources\\black_6.png"),
        }
        

            
