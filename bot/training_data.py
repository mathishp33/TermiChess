import chess
import chess.engine
import pickle
import random


class Move:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return f"Move({self.start} -> {self.end})"

WHITE = 0b10000
BLACK = 0b01000
PIECE_MAP = {
    chess.KING:   0b00001,
    chess.QUEEN:  0b00010,
    chess.BISHOP: 0b00011,
    chess.KNIGHT: 0b00100,
    chess.ROOK:   0b00101,
    chess.PAWN:   0b00111,
}

def encode_piece(piece: chess.Piece) -> int:
    if piece is None:
        return 0
    team = WHITE if piece.color == chess.WHITE else BLACK
    return team | PIECE_MAP[piece.piece_type]

def board_to_encoded_list(board: chess.Board) -> list[int]:
    return [encode_piece(board.piece_at(i)) for i in range(64)]

def move_to_custom(move: chess.Move) -> Move:
    return Move(move.from_square, move.to_square)


def generate_training_sample(engine, board: chess.Board):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    result = engine.play(board, chess.engine.Limit(depth=12))
    best_move = result.move
    if best_move not in legal_moves:
        return None

    encoded_board = board_to_encoded_list(board)
    custom_moves = [move_to_custom(m) for m in legal_moves]
    correct_index = legal_moves.index(best_move)

    return (encoded_board, custom_moves, correct_index)

def collect_training_data(num_games=10, max_samples=1000, stockfish_path="C:/Users/Utilisateur/Downloads/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2.exe"): #stockfish pathd
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    data = []

    for _ in range(num_games):
        board = chess.Board()

        while not board.is_game_over() and len(data) < max_samples:
            sample = generate_training_sample(engine, board)
            if sample:
                data.append(sample)

            move = engine.play(board, chess.engine.Limit(depth=12)).move
            board.push(move)

    engine.quit()
    return data

def save_data(data, filepath="training_data.pckl"):
    with open(filepath, "wb") as f:
        pickle.dump(data, f)
    print(f"Saved {len(data)} samples to {filepath}")

if __name__ == "__main__":
    data = collect_training_data(num_games=100, max_samples=100000)
    save_data(data)