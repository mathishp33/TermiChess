import random
import chess.game as game
import torch
import torch.nn as nn
import torch.optim as optim
import pickle
import os


# class DumbyBot:
#     def __init__(self, team: int):
#         self.team = team
#         self.anticipated_moves = 2

#     def think(self, game: game.Game, moves: list):
#         self.given_game = game
#         self.games = []
#         self.count_down = self.anticipated_moves
#         self.turn = 16

#         self.moves = [[move, move.eaten_piece, self.given_game, []] for move in moves]

#         if self.anticipated_moves < 2:
#             self.finals_moves = self.moves
#             return self.anticipate(self.finals_moves)
#         self.count_down -= 1
        
#         while self.count_down > 0:
#             self.moves = self.parsifier(self.moves, self.given_game) 
            
#         self.counting_moves(self.moves)
            
#     def parsifier(self, moves: list, game: game):
#         for i, move in enumerate(moves):
#             ext_game = game
#             ext_game.move_generator.update_moves(self.turn)
#             ext_game.moves.append(move[0])
#             ext_game.move += 1
#             self.turn = 8 if self.turn == 16 else 16
#             self.count_down -= 1
#             for k, j in enumerate(ext_game.move_generator.moves):
#                 move[2].append([j, j.eaten_piece, self.given_game, []])

#         return moves

#     def counting_moves(self, moves: list):
#         self.better_score = []
#         for move in moves:
#             if move[3] != []:
#                 for move2 in move[3]:


class Randbot:
    def __init__(self, team: int):
        self.team = team

    def think(self, moves):
        return random.choice(moves)
                




class SimpleChessNet(nn.Module):
    def __init__(self, input_size=65, hidden_size=128):
        super(SimpleChessNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.out = nn.Linear(hidden_size, 1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        return self.out(x)

class ChessAI:
    def __init__(self, team, learning_rate=1e-3):
        self.team = team
        self.model = SimpleChessNet()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.CrossEntropyLoss()

        self.load("model.pckl")

    def encode_board(self, board):
        board_tensor = torch.tensor(board, dtype=torch.float32)
        team_tensor = torch.tensor([self.team], dtype=torch.float32)
        return torch.cat([board_tensor, team_tensor])

    def think(self, moves, board):
        self.model.eval()
        board_encoding = self.encode_board(board)
        scores = []

        for move in moves:
            move_tensor = board_encoding.clone()
            score = self.model(move_tensor)
            scores.append(score)

        scores_tensor = torch.cat(scores)
        best_index = torch.argmax(scores_tensor).item()
        return moves[best_index]

    def train(self, data, epochs=1):
        """
        Train the model with data: list of (board, legal_moves, correct_index).
        board: list of 64 int
        legal_moves: list of Move objects
        correct_index: index of the best move from legal_moves
        """
        self.model.train()
        for epoch in range(epochs):
            for board, moves, correct_index in data:
                board_encoding = self.encode_board(board)
                inputs = []

                for move in moves:
                    x = board_encoding.clone()
                    inputs.append(x)

                input_tensor = torch.stack(inputs)
                logits = self.model(input_tensor).squeeze()
                target = torch.tensor([correct_index], dtype=torch.long)

                loss = self.loss_fn(logits.unsqueeze(0), target)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({
                'optimizer_state': self.optimizer.state_dict(),
                'model_state': self.model.state_dict()
            }, f)
        print(f"Model saved to {filepath}")

    @classmethod
    def load(self, filepath, learning_rate=1e-3):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No file found at {filepath}")
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        instance = self(learning_rate=learning_rate)
        instance.model.load_state_dict(data['model_state'])
        instance.optimizer.load_state_dict(data['optimizer_state'])
        instance.model.eval()
        print(f"Model loaded from {filepath}")
        return instance
    


if __name__ == "__main__":
    ai = ChessAI(team=8)
    ai.save("model.pckl")