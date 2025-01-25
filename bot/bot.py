import numpy as np
import random
import chess.game as game

class DumbyBot:
    def __init__(self, team: int):
        self.team = team

    def think(self, moves: list):
        self.moves = {}
        for i, j in enumerate(moves):
            self.moves[j.eaten_piece] = j
        self.moves = dict(sorted(self.moves.items()))
        print(self.moves)

        return list(self.moves.values())[-1]


class Randbot(DumbyBot):
    def __init__(self, team: int):
        super().__init__(team)

    def think(self, moves):
        return random.choice(moves)
                
                
if __name__ == '__main__':
    board = np.zeros(64)
    board[1] = 8 | 2
    pieces = [['None', (0, 0), [(0, 1)]]]
    