import chess.game as game
import pygame as pg

class Move:
    def __init__(self, ibefore: int, iafter: int, eaten_piece: int = 0, eaten_i = -1, castle: int = -1, en_passant: bool = False):
        self.start = ibefore
        self.end = iafter
        self.piece = game.Game.current.board[self.start]
        self.eaten_piece = eaten_piece
        self.eaten_i = eaten_i
        self.castle = castle
        self.en_passant = en_passant

    def do(self):
        if self.en_passant:
            pass
        elif self.castle >= 0:
            pass
        else:
            self.eaten_piece = game.Game.current.board[self.end]
            self.eaten_i = self.end

        game.Game.current.board[self.start] = 0
        game.Game.current.board[self.end] = self.piece
        if self.eaten_piece != 0:
            pg.mixer.Sound.play(game.Game.current.sounds["capture"])
        else:
            pg.mixer.Sound.play(game.Game.current.sounds["move"])

    def undo(self):
        if self.castle >= 0:
            pass
        game.Game.current.board[self.start] = self.piece
        game.Game.current.board[self.end] = 0
        game.Game.current.board[self.eaten_i] = self.eaten_piece
        pg.mixer.Sound.play(game.Game.current.sounds["move"])