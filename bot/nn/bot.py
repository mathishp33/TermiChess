import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


class ChessBot(nn.Module):
    def __init__(self):
        super(ChessBot, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 64 * 64)  # 64 squares × 64 possible target squares

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def train_bot(model, data, optimizer, criterion, epochs=10):
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for board, move in data:
            optimizer.zero_grad()
            board_tensor = board_to_tensor(board)
            target = move_to_target(move)
            prediction = model(board_tensor)
            loss = criterion(prediction, target)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {epoch_loss:.4f}")


def move_to_target(move):
    """Convert a move into a target tensor."""
    start, end = move.from_square, move.to_square
    target = np.zeros(64 * 64, dtype=float)
    target[start * 64 + end] = 1.0
    return torch.tensor(target, dtype=torch.float32)


if __name__ == "__main__":

    model = ChessBot()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCEWithLogitsLoss()

    moves = [] #GET THE MOVES


    training_data = [(board, move) for board, move in zip(boards, moves)]


    train_bot(model, training_data, optimizer, criterion)


    torch.save(model.state_dict(), "chess_bot.pth")
