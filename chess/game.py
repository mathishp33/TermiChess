import pygame as pg
import platform
from chess.move import *
from gui.events.keyboard_events import *
from gui.events.event import *


'''
The system used is a 5-bit encoding, with the first 2 bits representing the team of the piece.
    WHITE = 0b10000
    BLACK = 0b01000

The last 3 bits represent the type of piece.
    KING   = 0b00001
    QUEEN  = 0b00010
    BISHOP = 0b00011
    KNIGHT = 0b00100
    ROOK   = 0b00101
    PAWN   = 0b00111

If we want a white rook for example, we do a bitwise OR operation.
Example: WHITE | ROOK = 16 | 5
                      = 0b10101
'''
WHITE = 16
BLACK = 8

KING = 1
QUEEN = 2
BISHOP = 3
KNIGHT = 4
ROOK = 5
PAWN = 6

class Game():
    current = None
    def __init__(self):
        Game.current = self
        self.boardSize = 512
        self.board = [0 for i in range(64)]
        self.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq")
        self.turn = WHITE
        self.castle = [True, True, True, True]
        self.moves: list[Move] = []
        self.move = 0

        s = "\\" if platform.system() == "Windows" else "/"

        self.pieces_tex = {
            0: None,

            WHITE | KING: pg.image.load(f"resources{s}imgs{s}white_1.png"),
            WHITE | QUEEN: pg.image.load(f"resources{s}imgs{s}white_2.png"),
            WHITE | BISHOP: pg.image.load(f"resources{s}imgs{s}white_3.png"),
            WHITE | KNIGHT: pg.image.load(f"resources{s}imgs{s}white_4.png"),
            WHITE | ROOK: pg.image.load(f"resources{s}imgs{s}white_5.png"),
            WHITE | PAWN: pg.image.load(f"resources{s}imgs{s}white_6.png"),

            BLACK | KING: pg.image.load(f"resources{s}imgs{s}black_1.png"),
            BLACK | QUEEN: pg.image.load(f"resources{s}imgs{s}black_2.png"),
            BLACK | BISHOP: pg.image.load(f"resources{s}imgs{s}black_3.png"),
            BLACK | KNIGHT: pg.image.load(f"resources{s}imgs{s}black_4.png"),
            BLACK | ROOK: pg.image.load(f"resources{s}imgs{s}black_5.png"),
            BLACK | PAWN: pg.image.load(f"resources{s}imgs{s}black_6.png"),
        }
        self.sounds = {
            "move": pg.mixer.Sound(f"resources{s}sounds{s}move.wav"),
            "capture": pg.mixer.Sound(f"resources{s}sounds{s}capture.wav"),
            "check": pg.mixer.Sound(f"resources{s}sounds{s}move-check.wav"),
            "promote": pg.mixer.Sound(f"resources{s}sounds{s}promote.wav"),
        }

        for key in self.pieces_tex.keys():
            if key != 0:
               self.pieces_tex[key] = pg.transform.scale(self.pieces_tex[key], (self.boardSize/8, self.boardSize/8))
    
    def from_fen(self, fen: str):
        x, y = 0, 0
        phase = 0
        self.castle = [True, True, True, True]
        for c in fen:
            if c == ' ':
                phase += 1
                continue
            if phase == 0:
                team = 0
                type = 0
                if c == '/':
                    x = 0
                    y += 1
                    continue
                if c.isnumeric():
                    x += int(c)
                    continue
                if c.islower():
                    team = BLACK
                else:
                    team = WHITE
                c = c.lower()
                if c == 'k':
                    type = KING
                elif c == 'q':
                    type = QUEEN
                elif c == 'b':
                    type = BISHOP
                elif c == 'n':
                    type = KNIGHT
                elif c == 'r':
                    type = ROOK
                elif c == 'p':
                    type = PAWN
            
                self.board[y*8+x] = team | type
                x += 1
            elif phase == 1:
                if c == 'w':
                    self.turn = WHITE
                elif c == 'b':
                    self.turn = BLACK
            elif phase == 2:
                if c == '-':
                    self.castle = [False, False, False, False]
                elif c == 'K':
                    self.castle[0] = True
                elif c == 'Q':
                    self.castle[1] = True
                elif c == 'k':
                    self.castle[2] = True
                elif c == 'q':
                    self.castle[3] = True

    def fen(self) -> str:
        raise NotImplementedError()
    
@event_listener
def onKeyPress(event: KeyPressEvent):
    i = Game.current.move
    if event.key == pg.K_RIGHT:
        if i < len(Game.current.moves):
            Game.current.move += 1
            Game.current.moves[i].do()
    elif event.key == pg.K_LEFT:
        if i > 0:
            Game.current.move -= 1
            Game.current.moves[i-1].undo()
