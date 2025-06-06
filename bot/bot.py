import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
import pickle
import os


class Randbot:
    def __init__(self, team: int):
        self.team = team

    def think(self, moves, board):
        return random.choice(moves)


KING   = 0b00001
QUEEN  = 0b00010
BISHOP = 0b00011
KNIGHT = 0b00100
ROOK   = 0b00101
PAWN   = 0b00111

WHITE = 0b10000
BLACK = 0b01000

PIECE_TYPES = [KING, QUEEN, BISHOP, KNIGHT, ROOK, PAWN]

def encode_square(piece_int):
    piece_int = int(piece_int)
    if piece_int == 0:
        return np.zeros(8, dtype=np.float32)

    team = [1, 0] if (piece_int & WHITE) == WHITE else [0, 1] if (piece_int & BLACK) == BLACK else [0, 0]
    piece_type = piece_int & 0b00111
    piece_onehot = [1 if piece_type == pt else 0 for pt in PIECE_TYPES]

    return np.array(team + piece_onehot, dtype=np.float32)

def encode_board(board_int_list):
    return np.concatenate([encode_square(p) for p in board_int_list])

def encode_piece_type(piece_int):
    piece_int = int(piece_int)
    if piece_int == 0:
        return np.zeros(6, dtype=np.float32)
    piece_type = piece_int & 0b00111
    return np.array([1 if piece_type == pt else 0 for pt in PIECE_TYPES], dtype=np.float32)

class NN(nn.Module):
    def __init__(self, input_size=521, hidden_size=1024, num_layers=6, dropout_p=0.2):
        super().__init__()
        self.input_fc = nn.Linear(input_size, hidden_size)
        self.layers = nn.ModuleList([
            nn.Linear(hidden_size, hidden_size) for _ in range(num_layers)
        ])
        self.norms = nn.ModuleList([
            nn.LayerNorm(hidden_size) for _ in range(num_layers)
        ])
        self.out = nn.Linear(hidden_size, 1)
        self.act = nn.GELU()
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, x):
        x = self.act(self.input_fc(x))
        for layer, norm in zip(self.layers, self.norms):
            residual = x
            x = self.act(norm(layer(x)))
            x = self.dropout(x)
            x = x + residual
        return self.out(x).squeeze(-1)

class ChessAI:
    def __init__(self, team=8, learning_rate=1e-3):
        self.team = team
        self.input_size = 521
        self.model = NN(input_size=self.input_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.CrossEntropyLoss()
        self.should_train = False

    def encode_input(self, board, move):
        board_vec = torch.tensor(encode_board(board), dtype=torch.float32)
        team_tensor = torch.tensor([0.0 if self.team == 8 else 1.0], dtype=torch.float32)
        move_tensor = torch.tensor([move.start / 63.0, move.end / 63.0], dtype=torch.float32)
        piece_type_vec = torch.tensor(encode_piece_type(board[move.start]), dtype=torch.float32)
        return torch.cat([board_vec, team_tensor, move_tensor, piece_type_vec])

    def think(self, moves, board):
        if not moves:
            return None
        self.model.eval()
        with torch.no_grad():
            inputs = torch.stack([self.encode_input(board, move) for move in moves])
            scores = self.model(inputs)
            best_index = torch.argmax(scores).item()
            return moves[best_index]

    def train(self, data, epochs=1):
        self.model.train()
        total_loss = 0
        total = 0
        for _ in range(epochs):
            for board, moves, correct_index in data:
                input_tensor = torch.stack([self.encode_input(board, move) for move in moves])
                logits = self.model(input_tensor).unsqueeze(0)
                target = torch.tensor([correct_index], dtype=torch.long)

                loss = self.loss_fn(logits, target)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
                total += 1

        avg_loss = total_loss / total if total > 0 else 0
        print(f"Loss: {avg_loss:.4f}")

    def save(self, filepath, extra_metadata=None):
        save_data = {
            'model_state': self.model.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'metadata': extra_metadata or {}
        }
        with open(filepath, 'wb') as f:
            pickle.dump(save_data, f)
        print(f"AI saved to {filepath}")

    @classmethod
    def load(cls, filepath, learning_rate=1e-4, team=8):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No file found at {filepath}")

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        instance = cls(team=team, learning_rate=learning_rate)
        instance.model.load_state_dict(data['model_state'])
        instance.optimizer.load_state_dict(data['optimizer_state'])
        instance.model.eval()
        print(f"AI loaded from {filepath}")
        return instance, data.get('metadata', {})

if __name__ == '__main__':
    from training_data import Move

    method = 'load' #load or create
    if method == 'load':
        bot, metadata = ChessAI.load('bot.pckl')
        print(metadata)
    else:
        bot = ChessAI()

    with open('training_data.pckl', 'rb') as f:
        data = pickle.load(f)

    for i, sample in enumerate(data):
        bot.train([sample], epochs=5)
        if i % 50 == 0:
            bot.save('bot.pckl')
            print(f"Progress: {i} / {len(data)}")

    bot.save('bot.pckl')