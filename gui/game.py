import pygame as pg
import os

WHITE = 0
BLACK = 1

KING = 1
QUEEN = 2
BISHOP = 3
KNIGHT = 4
ROOK = 5
PAWN = 6

class Game():
    def __init__(self):
        self.board = [[[5,1], [4,1], [3,1], [2,1], [1,1], [3,1], [4,1], [5,1]],
                      [[6,1], [6,1], [6,1], [6,1], [6,1], [6,1], [6,1], [6,1]],
                      [[0], [0], [0], [0], [0], [0], [0], [0]],
                      [[0], [0], [0], [0], [0], [0], [0], [0]],
                      [[0], [0], [0], [0], [0], [0], [0], [0]],
                      [[0], [0], [0], [0], [0], [0], [0], [0]],
                      [[6,0], [6,0], [6,0], [6,0], [6,0], [6,0], [6,0], [6,0]],
                      [[5, 0], [4, 0], [3, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]]
        self.turn = 'Player'
        self.K_moves = [(0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (-1, 0)]
        self.Q_moves = [8, 8, 8, 8, 8, 8]
        self.B_moves = []
    def turn(self):
        
        
        self.turn = 'Bot'
        

class Pieces():
    def __init__(self):
        self.board = Game()
        self.pieces_index = ['white_1', 'black_1', 'white_2', 'black_2', 'white_3', 'black_3', 'white_4', 'black_4', 'white_5', 'black_5', 'white_6', 'black_6' ]
        self.pieces = []
        for i in range(8):
            for j in range(8):
                if not self.board.board[i][j] == [0]:
                    name_of = self.pieces_index[self.board.board[i][j][0]+self.board.board[i][j][1]*2-1]
                    item = [j, i,pg.image.load(('ressources\\' + name_of + '.png'))]
                    self.pieces.append(item)
        self.board.turn()
        
        
            
