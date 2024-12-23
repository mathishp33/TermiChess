import pygame as pg
import numpy as np
import platform
from chess.utils import *
from gui.events.keyboard_events import *
from gui.events.event import *
import struct


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

    def do(self, discrete: bool = False):
        if self.en_passant:
            pass
        elif self.castle >= 0:
            pass
        else:
            self.eaten_piece = Game.current.board[self.end]
            self.eaten_i = self.end

        Game.current.board[self.start] = 0
        Game.current.board[self.end] = self.piece
        MoveGenerator.tracked_pieces.remove(self.start)
        if not self.en_passant:
            if not self.end in MoveGenerator.tracked_pieces:
                MoveGenerator.tracked_pieces.append(self.end)
        else:
            pass

        if not discrete:
            if self.eaten_piece != 0:
                pg.mixer.Sound.play(Game.current.sounds["capture"])
            else:
                pg.mixer.Sound.play(Game.current.sounds["move"])

    def undo(self, discrete: bool = False):
        if self.castle >= 0:
            pass
        Game.current.board[self.start] = self.piece
        Game.current.board[self.end] = 0
        Game.current.board[self.eaten_i] = self.eaten_piece
        if self.eaten_piece == 0:
            MoveGenerator.tracked_pieces.remove(self.end)
        if not self.en_passant:
            if not self.start in MoveGenerator.tracked_pieces:
                MoveGenerator.tracked_pieces.append(self.start)
        else:
            pass

        if not discrete:
            pg.mixer.Sound.play(Game.current.sounds["move"])

    def is_similar(self, other) -> bool:
        return self.start == other.start and self.end == other.end and self.castle == other.castle
    
    def __eq__(self, value):
        return value != None and self.start == value.start and self.end == value.end and self.castle == value.castle

DIRS_OFFSET = [-1, -8, 1, 8, 7, -9, -7, 9]
KNIGHT_JUMPS = [6, -10, -17, 15, -15, 17, -6, 10]

class MoveGenerator:
    tracked_pieces: list[int] = []

    def __init__(self, parent: Game):
        self.parent = parent
        self.checked = False
        self.checker = None
        self.pinned_pieces = []
        self.pin_lines = [[] for i in range(8)]
        self.attacked_squares = [[], []]
        self.precompute_move_data()
        self.locate_pieces()
        self.update_moves(WHITE)

    def update_moves(self, team):
        self.pin_lines = [[] for i in range(8)]
        self.pinned_pieces = []
        self.checked = False
        self.generate_attacked_squares(team)
        self.generate_pins(team)
        self.generate_legal_moves(team)

    def generate_pins(self, team):
        if not self.checked:
            k_index = -1
            for i in MoveGenerator.tracked_pieces:
                if self.parent.board[i] == KING | team:
                    k_index = i
                    break
            for i in range(len(DIRS_OFFSET)):
                dir = DIRS_OFFSET[i]
                distance = self.move_data[k_index][i]
                pinned_piece = 0
                add = False
                line = []
                pins = []
                for j in range(1, int(distance+1)):
                    square = k_index + dir * j
                    target = self.parent.board[square]
                    type_ = Game.get_piece_type(target)
                    team_ = Game.get_piece_team(target)
                    line.append(square)
                    if team_ == team:
                        if pinned_piece == 0:
                            pinned_piece = target
                            pins.append(square)
                        else:
                            break
                    elif team_ != 0:
                        if i < 4:
                            if (type_ == ROOK or type_ == QUEEN) and pinned_piece != 0:
                                if pinned_piece == 0:
                                    self.checked = True
                                    self.checker = square
                                add = True
                            break
                        else:
                            if (type_ == BISHOP or type_ == QUEEN):
                                if pinned_piece == 0:
                                    self.checked = True
                                    self.checker = square
                                add = True
                            break
                if add:
                    self.pin_lines[i] = line
                    self.pinned_pieces += pins
        else:
            for i in MoveGenerator.tracked_pieces:
                if Game.get_piece_team(self.parent.board[i]) == team:
                    self.pinned_pieces.append(i)


    def generate_legal_moves(self, team):
        self.moves: list[Move] = []
        for i in MoveGenerator.tracked_pieces:
            piece = self.parent.board[i]
            type_ = Game.get_piece_type(piece)
            team_ = Game.get_piece_team(piece)
            if team != team_: continue

            if type_ in [BISHOP, ROOK, QUEEN]:
                move_data = self.move_data[i]
                start_index = 0 if type_ == QUEEN or type_ == ROOK else 4
                end_index = 4 if type_ == ROOK else 8
                for j in range(start_index, end_index):
                    distance = move_data[j]
                    for k in range(1, int(distance)+1):
                        square = i + k * DIRS_OFFSET[j]
                        target_piece = self.parent.board[square]
                        if Game.get_piece_team(target_piece) == team_: break
                        if not i in self.pinned_pieces and not self.checked:
                            self.moves.append(Move(i, square))
                        elif self.checked and self.is_square_in_pins(square):
                            self.moves.append(Move(i, square))
                        if Game.get_piece_team(target_piece) != 0: break
            
            elif type_ == KNIGHT:
                if not i in self.pinned_pieces and not self.checked:
                    start_index = 0 if i % 8 > 1 else 2 if i % 8 > 0 else 4
                    end_index = 8 if i % 8 < 6 else 6 if i % 8 < 7 else 4
                    for j in range(start_index, end_index):
                        square = i + KNIGHT_JUMPS[j]
                        if not (square > -1 and square < 64): continue
                        target_piece = self.parent.board[square]
                        if Game.get_piece_team(target_piece) == team_: continue
                        self.moves.append(Move(i, square))
                elif self.checked:
                    start_index = 0 if i % 8 > 1 else 2 if i % 8 > 0 else 4
                    end_index = 8 if i % 8 < 6 else 6 if i % 8 < 7 else 4
                    for j in range(start_index, end_index):
                        square = i + KNIGHT_JUMPS[j]
                        if self.is_square_in_pins(square):
                            if not (square > -1 and square < 64): continue
                            target_piece = self.parent.board[square]
                            if Game.get_piece_team(target_piece) == team_: continue
                            self.moves.append(Move(i, square))   

            elif type_ == KING:
                move_data = self.move_data[i]
                for j in range(len(DIRS_OFFSET)):
                    dir = DIRS_OFFSET[j]
                    distance = move_data[j]
                    square = i + dir
                    if distance != 0:
                        target_piece = self.parent.board[square]
                        if Game.get_piece_team(target_piece) == team_: continue
                        if self.attacked_squares[0 if team_ == WHITE else 1][square] == 0: 
                            self.moves.append(Move(i, square))

            elif type_ == PAWN:
                offsets = (-9, -7, -8, -16, 6) if team_ == WHITE else (7, 9, 8, 16, 1)
                square = i + offsets[0]
                if square > -1 and square < 64:
                    target_piece = self.parent.board[square]
                    target_team = Game.get_piece_team(target_piece)
                    if target_team != team_ and target_team != 0:
                        if i % 8 > 0:
                            if not i in self.pinned_pieces and not self.checked:
                                self.moves.append(Move(i, square))
                            elif self.checked and self.is_square_in_pins(square):
                                self.moves.append(Move(i, square))
                square = i + offsets[1]
                if square > -1 and square < 64:
                    target_piece = self.parent.board[square]
                    target_team = Game.get_piece_team(target_piece)
                    if target_team != team_ and target_team != 0:
                        if i % 8 < 7:
                            if not i in self.pinned_pieces and not self.checked:
                                self.moves.append(Move(i, square))
                            elif self.checked and self.is_square_in_pins(square):
                                self.moves.append(Move(i, square))
                square = i + offsets[2]
                if square > -1 and square < 64:
                    blocking_piece = self.parent.board[square]
                    if blocking_piece == 0:
                        if not i in self.pinned_pieces and not self.checked:
                            self.moves.append(Move(i, square))
                        elif self.checked and self.is_square_in_pins(square):
                            self.moves.append(Move(i, square))
                    else:
                        continue
                if i // 8 == offsets[4]:
                    square = i + offsets[3]
                    blocking_piece = self.parent.board[square]
                    if blocking_piece == 0:
                        if not i in self.pinned_pieces and not self.checked:
                            self.moves.append(Move(i, square))
                        elif self.checked and self.is_square_in_pins(square):
                            self.moves.append(Move(i, square))
        return self.moves
    
    def is_square_in_pins(self, square: int, lines: str = "all"):
        for i in range(len(self.pin_lines)):
            line = self.pin_lines[i]
            if (lines == "all" or lines == "straight") and i < 4:
                if square in line:
                    return True
            elif (lines == "all" or lines == "diagonals") and i > 4:
                if square in line:
                    return True
        return False

    def generate_attacked_squares(self, team: int):
        self.attacked_squares = np.zeros((2, 64))
        for i in MoveGenerator.tracked_pieces:
            if Game.get_piece_team(self.parent.board[i]):
                self.get_piece_targets(i)
            
    def get_piece_targets(self, index: int):
        piece = self.parent.board[index]
        type_ = Game.get_piece_type(piece)
        team = Game.get_piece_team(piece)
        move_data = self.move_data[index]
        t_index = 0 if team == WHITE else 1

        if type_ in [BISHOP, ROOK, QUEEN]:
            start_index = 0 if type_ == QUEEN or type_ == ROOK else 4
            end_index = 4 if type_ == ROOK else 8
            for i in range(start_index, end_index):
                distance = move_data[i]
                for j in range(1, int(distance)+1):
                    square = index + j * DIRS_OFFSET[i]
                    self.attacked_squares[0 if t_index == 1 else 1][square] += 1
                    if self.parent.board[square] != 0: break
            
        elif type_ == KNIGHT:
            start_index = 0 if index % 8 > 1 else 2 if index % 8 > 0 else 4
            end_index = 8 if index % 8 < 6 else 6 if index % 8 < 7 else 4
            for j in range(start_index, end_index):
                square = index + KNIGHT_JUMPS[j]
                if not (square > -1 and square < 64): continue
                self.attacked_squares[0 if t_index == 1 else 1][square] += 1
                target = self.parent.board[square]
                if Game.get_piece_team(target) != team:
                    if Game.get_piece_type(target) == KING:
                        self.checked = True
                        self.checker = index
                        self.pin_lines[0].append(index)
                        self.pin_lines[4].append(index)
                
        elif type_ == KING:
            for i in range(len(DIRS_OFFSET)):
                dir = DIRS_OFFSET[i]
                distance = move_data[i]
                if distance != 0:
                    square = index + dir
                    self.attacked_squares[0 if t_index == 1 else 1][square] += 1
        
        elif type_ == PAWN:
            offsets = (-9, -7, -8, -16, 6) if team == WHITE else (7, 9, 8, 16, 1)
            square = index + offsets[0]
            if square > -1 and square < 64:
                if index % 8 > 0:
                    self.attacked_squares[0 if t_index == 1 else 1][square] += 1
                    target = self.parent.board[square]
                    if Game.get_piece_team(target) != team:
                        if Game.get_piece_type(target) == KING:
                            self.checked = True
                            self.checker = index
            square = index + offsets[1]
            if square > -1 and square < 64:
                if index % 8 < 7:
                    self.attacked_squares[0 if t_index == 1 else 1][square] += 1
                    target = self.parent.board[square]
                    if Game.get_piece_team(target) != team:
                        if Game.get_piece_type(target) == KING:
                            self.checked = True
                            self.checker = index
                            

    def locate_pieces(self):
        MoveGenerator.tracked_pieces = []
        for i in range(64):
            if self.parent.board[i] != 0:
                MoveGenerator.tracked_pieces.append(i)

    def precompute_move_data(self):
        self.move_data = np.zeros((64, 8))
        for x in range(8):
            for y in range(8):
                left = x
                right = 7 - x
                top = y
                bottom = 7 - y
                self.move_data[8*y+x][0] = left
                self.move_data[8*y+x][1] = top
                self.move_data[8*y+x][2] = right
                self.move_data[8*y+x][3] = bottom
                self.move_data[8*y+x][4] = min(left, bottom)
                self.move_data[8*y+x][5] = min(left, top)
                self.move_data[8*y+x][6] = min(right, top)
                self.move_data[8*y+x][7] = min(right, bottom)