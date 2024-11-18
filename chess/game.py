import pygame as pg
import numpy as np
import platform
from chess.utils import *
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
    def __init__(self, mode: str):
        Game.current = self
        self.boardSize = 512
        self.board = np.zeros(64)
        self.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq")
        self.turn = WHITE
        self.castle = [True, True, True, True]
        self.moves: list[Move] = []
        self.move = 0
        self.move_generator = MoveGenerator(self)

        if mode == "GUI":
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

    def generate_possible_moves(self) -> list["Move"]:
        moves = []
        for y in range(8):
            for x in range(8):
                piece = self.board[position_to_index((x, y))]

    
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
    
    def get_piece_team(piece: int) -> int:
        return int(piece) & 24
    
    def get_piece_type(piece: int) -> int:
        return int(piece) & 7
    
    def get_char_from_piece(piece: int) -> str:
        t = Game.get_piece_type(piece)
        if Game.get_piece_team(piece) == WHITE:
            if t == KING: return "K"
            if t == QUEEN: return "Q"
            if t == BISHOP: return "B"
            if t == KNIGHT: return "N"
            if t == ROOK: return "R"
            if t == PAWN: return "P"
        elif Game.get_piece_team(piece) == BLACK:
            if t == KING: return "k"
            if t == QUEEN: return "q"
            if t == BISHOP: return "b"
            if t == KNIGHT: return "n"
            if t == ROOK: return "r"
            if t == PAWN: return "p"
        return " "

        
    
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

class Move:
    def __init__(self, ibefore: int, iafter: int, eaten_piece: int = 0, eaten_i = -1, castle: int = -1, en_passant: bool = False):
        self.start = ibefore
        self.end = iafter
        self.piece = Game.current.board[self.start]
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
            self.eaten_piece = Game.current.board[self.end]
            self.eaten_i = self.end

        Game.current.board[self.start] = 0
        Game.current.board[self.end] = self.piece
        if self.eaten_piece != 0:
            pg.mixer.Sound.play(Game.current.sounds["capture"])
        else:
            pg.mixer.Sound.play(Game.current.sounds["move"])

    def undo(self):
        if self.castle >= 0:
            pass
        Game.current.board[self.start] = self.piece
        Game.current.board[self.end] = 0
        Game.current.board[self.eaten_i] = self.eaten_piece
        pg.mixer.Sound.play(Game.current.sounds["move"])

    def is_similar(self, other) -> bool:
        return self.start == other.start and self.end == other.end and self.castle == other.castle

DIRS_OFFSET = [-1, -8, 1, 8, 7, -9, -7, 9]

class MoveGenerator:
    def __init__(self, parent: Game):
        self.parent = parent
        self.locate_pieces()
        self.precompute_move_data()
        self.generate_attacked_squares()

    def generate_attacked_squares(self):
        self.attacked_squares = np.zeros((2, 64))
        for i in self.tracked_pieces:
            self.get_piece_targets(i)
            
    def get_piece_targets(self, index: int):
        piece = self.parent.board[index]
        type_ = Game.get_piece_type(piece)
        start_index = 0 if type_ == QUEEN or type_ == ROOK else 4
        end_index = 4 if type_ == QUEEN or type_ == ROOK else 8
        if Game.get_piece_team(piece) == WHITE:
            for i in range(start_index, end_index):
                distances = self.move_data[i]
                for j in range(1, distances[i]+1):
                    self.attacked_squares[0][index + j * DIRS_OFFSET[i]] += 1

    def locate_pieces(self):
        self.tracked_pieces = []
        for i in range(64):
            if self.parent.board[i] != 0:
                self.tracked_pieces.append(i)

    def precompute_move_data(self):
        self.move_data = np.zeros((64, 4))
        for x in range(8):
            for y in range(8):
                left = x
                right = 7 - x
                top = y
                bottom = 7 - y
                self.move_data[8*y+x][0] = left
                self.move_data[8*y+x][1] = right
                self.move_data[8*y+x][2] = top
                self.move_data[8*y+x][3] = bottom