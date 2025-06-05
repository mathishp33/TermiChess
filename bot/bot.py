import numpy as np
import random
import chess.game as game
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
                

#teams (int) : 
# 8: white
# 16: black


class NN(nn.Module):
    def __init__(self, input_size=67, hidden_size=1024, dropout_p=0.3):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.bn3 = nn.BatchNorm1d(hidden_size)
        self.fc4 = nn.Linear(hidden_size, hidden_size)
        self.bn4 = nn.BatchNorm1d(hidden_size)
        self.out = nn.Linear(hidden_size, 1)

        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        x = self.relu(self.bn3(self.fc3(x)))
        x = self.dropout(x)
        x = self.relu(self.bn4(self.fc4(x)))
        x = self.dropout(x)
        x = self.out(x).squeeze(-1)
        return x

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
    
    if (piece_int & WHITE) == WHITE:
        team = [1, 0]
    elif (piece_int & BLACK) == BLACK:
        team = [0, 1]
    else:
        team = [0, 0]

    piece_type = piece_int & 0b00111
    piece_onehot = [1 if piece_type == pt else 0 for pt in PIECE_TYPES]

    return np.array(team + piece_onehot, dtype=np.float32)

def encode_board(board_int_list):
    encoded = [encode_square(p) for p in board_int_list]
    return np.concatenate(encoded)

def encode_piece_type(piece_int):
    piece_int = int(piece_int)
    if piece_int == 0:
        return np.zeros(6, dtype=np.float32)
    piece_type = piece_int & 0b00111
    return np.array([1 if piece_type == pt else 0 for pt in PIECE_TYPES], dtype=np.float32)

class NN(nn.Module):
    def __init__(self, input_size=521, hidden_size=1024, dropout_p=0.3):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.bn3 = nn.BatchNorm1d(hidden_size)
        self.fc4 = nn.Linear(hidden_size, hidden_size)
        self.bn4 = nn.BatchNorm1d(hidden_size)
        self.out = nn.Linear(hidden_size, 1)

        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        x = self.relu(self.bn3(self.fc3(x)))
        x = self.dropout(x)
        x = self.relu(self.bn4(self.fc4(x)))
        x = self.dropout(x)
        x = self.out(x).squeeze(-1)
        return x

class ChessAI:
    def __init__(self, team, learning_rate=1e-4):
        self.team = team
        self.input_size = 521
        self.model = NN(input_size=self.input_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.CrossEntropyLoss()

    def encode_input(self, board, move):
        board_vec = torch.tensor(encode_board(board), dtype=torch.float32)
        team_tensor = torch.tensor([0.0 if self.team == 8 else 1.0], dtype=torch.float32)
        move_tensor = torch.tensor([move.start / 63.0, move.end / 63.0], dtype=torch.float32)

        moving_piece_int = board[move.start]
        piece_type_vec = torch.tensor(encode_piece_type(moving_piece_int), dtype=torch.float32)

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
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            total = 0

            for board, moves, correct_index in data:
                inputs = [self.encode_input(board, move) for move in moves]
                input_tensor = torch.stack(inputs)

                logits = self.model(input_tensor)
                logits = logits.unsqueeze(0)

                target = torch.tensor([correct_index], dtype=torch.long)

                loss = self.loss_fn(logits, target)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()

                pred_index = torch.argmax(logits).item()
                if pred_index == correct_index:
                    correct += 1
                total += 1

            avg_loss = total_loss / total
            accuracy = correct / total * 100
            print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f} - Accuracy: {accuracy:.2f}%")

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