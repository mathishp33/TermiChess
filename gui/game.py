import pygame as pg
import platform

WHITE = 16
BLACK = 8

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
        self.board[5] = BLACK | KING

        prefix = "resources\\" if platform.system() == "Windows" else "resources/"

        self.pieces_tex = {
            0: None,

            WHITE | KING: pg.image.load(f"{prefix}white_1.png"),
            WHITE | QUEEN: pg.image.load(f"{prefix}white_2.png"),
            WHITE | BISHOP: pg.image.load(f"{prefix}white_3.png"),
            WHITE | KNIGHT: pg.image.load(f"{prefix}white_4.png"),
            WHITE | ROOK: pg.image.load(f"{prefix}white_5.png"),
            WHITE | PAWN: pg.image.load(f"{prefix}white_6.png"),

            BLACK | KING: pg.image.load(f"{prefix}black_1.png"),
            BLACK | QUEEN: pg.image.load(f"{prefix}black_2.png"),
            BLACK | BISHOP: pg.image.load(f"{prefix}black_3.png"),
            BLACK | KNIGHT: pg.image.load(f"{prefix}black_4.png"),
            BLACK | ROOK: pg.image.load(f"{prefix}black_5.png"),
            BLACK | PAWN: pg.image.load(f"{prefix}black_6.png"),
        }

        for key in self.pieces_tex.keys():
            if key != 0:
               self.pieces_tex[key] = pg.transform.scale(self.pieces_tex[key], (self.boardSize/8, self.boardSize/8))
        

            
