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


"""
Moves will be stored either as 16-bit or 32-bit integers in the future, storing the following informations :
- The starting square, 'from', will be stored in the first 6 bits (starting from the right).
- The ending square, 'to', will be stored in the next 6 bits.
- The move's flags, stored in a 4-bit bitfield, will be organized as follows :
    - The first bit starting from the left will be set if the move is a promotion.
    - The next bit will be set if the move is a capture.
    - The 2 next bits are special bits, used for different purposes depending on the first 2 bits.
- In case of a 32-bit integer, the following informations will be stored after :
    - The main piece's state, encoded on 5 bits.
    - The other concerned piece's state, encoded on 5 bits (0b00000 if no piece).
    - The other concerned piece's index, encoded on 6 bits (0b000000 if no piece).
"""

QUIET_MOVE = 0
DOUBLE_PAWN_PUSH = 1
KING_CASTLE = 2
QUEEN_CASTLE = 3
CAPTURE = 4
EN_PASSANT = 5
KNIGHT_PROMOTION = 8
BISHOP_PROMOTION = 9
ROOK_PROMOTION = 10
QUEEN_PROMOTION = 11
KNIGHT_PROMOTION_CAPTURE = 12
BISHOP_PROMOTION_CAPTURE = 13
ROOK_PROMOTION_CAPTURE = 14
QUEEN_PROMOTION_CAPTURE = 15

def move16(from_: int, to: int, flags: int) -> np.int16:
    """
    Returns a 16-bit integer representing a move.
    """
    return np.int16((flags << 12) | (from_ << 6) | to)

def move16_from_move32(move: np.int32) -> np.int16:
    return move16(move32_get_from(move), move32_get_to(move), move32_get_flags(move))

def move16_get_flags(move: np.int16) -> np.int16:
    return (move >> 12) & 0xf

def move16_get_from(move: np.int16) -> np.int16:
    return (move >> 6) & 0x3f

def move16_get_to(move: np.int16) -> np.int16:
    return move & 0x3f

def move16_is_promotion(move: np.int16) -> bool:
    return move16_get_flags(move) >= 8

def move16_is_capture(move: np.int16) -> bool:
    return move16_get_flags(move) == CAPTURE or move16_get_flags(move) >= 12

def move16_is_castle(move: np.int16) -> bool:
    return move16_get_flags(move) == KING_CASTLE or move16_get_flags(move) == QUEEN_CASTLE


def move32(from_: int, to: int, flags: int, piece_state: int = -1, other_piece_state: int = 0, other_piece_index: int = 0) -> np.int32:
    """
    Returns a 32-bit integer representing a move.
    """
    if piece_state == -1:
        piece_state = Game.current.board[from_]
    return np.int32((other_piece_index << 26) | (other_piece_state << 21) | (piece_state << 16) | (flags << 12) | (from_ << 6) | to)

def move32_from_move16(move: np.int16, piece_state: int = -1, other_piece_state: int = 0, other_piece_index: int = 0) -> np.int32:
    return move32(move16_get_from(move), move16_get_to(move), move16_get_flags(move), piece_state, other_piece_state, other_piece_index)

def move32_get_piece_state(move: np.int32) -> np.int32:
    return (move >> 26) & 0x3f

def move32_get_other_piece_state(move: np.int32) -> np.int32:
    return (move >> 21) & 0x1f

def move32_get_piece_state(move: np.int32) -> np.int32:
    return (move >> 16) & 0x1f

def move32_get_flags(move: np.int32) -> np.int32:
    return (move >> 12) & 0xf

def move32_get_from(move: np.int32) -> np.int32:
    return (move >> 6) & 0x3f

def move32_get_to(move: np.int32) -> np.int32:
    return move & 0x3f

def move32_is_promotion(move: np.int32) -> bool:
    return move16_get_flags(move) >= 8

def move32_is_capture(move: np.int32) -> bool:
    return move16_get_flags(move) == CAPTURE or move16_get_flags(move) >= 12

def move32_is_castle(move: np.int32) -> bool:
    return move16_get_flags(move) == KING_CASTLE or move16_get_flags(move) == QUEEN_CASTLE

"""
This class will be deprecated soon.
"""
 
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
        self.check_count = 0
        self.checker = None
        self.pinned_pieces = []
        self.pin_lines = [[] for i in range(8)]
        self.anti_retreat_squares = []
        self.attacked_squares = [[], []]
        self.precompute_move_data()
        self.locate_pieces()
        self.update_moves(WHITE)

    def update_moves(self, team):
        self.pin_lines = [[] for i in range(8)]
        self.pinned_pieces = []
        self.anti_retreat_squares = []
        self.check_count = 0
        self.generate_attacked_squares(team)
        self.generate_pins(team)
        self.generate_legal_moves(team)

    def generate_pins(self, team):
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
                        if type_ == ROOK or type_ == QUEEN:
                            if pinned_piece == 0:
                                self.check_count += 1
                                self.checker = square
                            add = True
                        break
                    else:
                        if type_ == BISHOP or type_ == QUEEN:
                            if pinned_piece == 0:
                                self.check_count += 1
                                self.checker = square
                            add = True
                        break
            if add:
                self.pin_lines[i] = line
                self.pinned_pieces += pins


    def generate_legal_moves(self, team) -> list[Move]:
        print(self.check_count)
        print(self.pin_lines)
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
                        if not i in self.pinned_pieces and self.check_count == 0:
                            self.moves.append(Move(i, square))
                        elif self.check_count > 0 and self.is_square_in_pins(square):
                            self.moves.append(Move(i, square))
                        if Game.get_piece_team(target_piece) != 0: break
            
            elif type_ == KNIGHT:
                if not i in self.pinned_pieces and self.check_count == 0:
                    start_index = 0 if i % 8 > 1 else 2 if i % 8 > 0 else 4
                    end_index = 8 if i % 8 < 6 else 6 if i % 8 < 7 else 4
                    for j in range(start_index, end_index):
                        square = i + KNIGHT_JUMPS[j]
                        if not (square > -1 and square < 64): continue
                        target_piece = self.parent.board[square]
                        if Game.get_piece_team(target_piece) == team_: continue
                        self.moves.append(Move(i, square))
                elif self.check_count > 0:
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
                            if self.check_count == 0 or not square in self.anti_retreat_squares:
                                self.moves.append(Move(i, square))

            elif type_ == PAWN:
                offsets = (-9, -7, -8, -16, 6) if team_ == WHITE else (7, 9, 8, 16, 1)
                square = i + offsets[0]
                if square > -1 and square < 64:
                    target_piece = self.parent.board[square]
                    target_team = Game.get_piece_team(target_piece)
                    if target_team != team_ and target_team != 0:
                        if i % 8 > 0:
                            if not i in self.pinned_pieces and self.check_count == 0:
                                self.moves.append(Move(i, square))
                            elif self.check_count > 0 and self.is_square_in_pins(square):
                                self.moves.append(Move(i, square))
                square = i + offsets[1]
                if square > -1 and square < 64:
                    target_piece = self.parent.board[square]
                    target_team = Game.get_piece_team(target_piece)
                    if target_team != team_ and target_team != 0:
                        if i % 8 < 7:
                            if not i in self.pinned_pieces and self.check_count == 0:
                                self.moves.append(Move(i, square))
                            elif self.check_count and self.is_square_in_pins(square):
                                self.moves.append(Move(i, square))
                square = i + offsets[2]
                if square > -1 and square < 64:
                    blocking_piece = self.parent.board[square]
                    if blocking_piece == 0:
                        if not i in self.pinned_pieces and self.check_count == 0:
                            self.moves.append(Move(i, square))
                        elif self.check_count > 0 and self.is_square_in_pins(square):
                            self.moves.append(Move(i, square))
                    else:
                        continue
                if i // 8 == offsets[4]:
                    square = i + offsets[3]
                    blocking_piece = self.parent.board[square]
                    if blocking_piece == 0:
                        if not i in self.pinned_pieces and self.check_count == 0:
                            self.moves.append(Move(i, square))
                        elif self.check_count > 0 and self.is_square_in_pins(square):
                            self.moves.append(Move(i, square))
        return self.moves
    
    def is_square_in_pins(self, square: int, lines: str = "all") -> bool:
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
                    piece = self.parent.board[square]
                    if piece != 0:
                        if Game.get_piece_team(piece) != team:
                            if Game.get_piece_type(piece) == KING:
                                self.anti_retreat_squares.append(square + DIRS_OFFSET[i])
                        break
            
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
                        self.check_count += 1
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
                            self.check_count += 1
                            self.checker = index
            square = index + offsets[1]
            if square > -1 and square < 64:
                if index % 8 < 7:
                    self.attacked_squares[0 if t_index == 1 else 1][square] += 1
                    target = self.parent.board[square]
                    if Game.get_piece_team(target) != team:
                        if Game.get_piece_type(target) == KING:
                            self.check_count += 1
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