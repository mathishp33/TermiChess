import numpy as np
import random
import chess.game as game

class Bot:
    def __init__(self, team: int):
        self.team = team

    def think(self, moves: list):
        """
        This is an interface function that takes the list of all possible moves, and returns a Move object.
        This returns nothing if not overriden by a subclass.
        """
        pass

class Randbot(Bot):
    def __init__(self, team: int):
        super().__init__(team)

    def think(self, moves):
        return random.choice(moves)
                
                
if __name__ == '__main__':
    board = np.zeros(64)
    board[1] = 8 | 2
    pieces = [['None', (0, 0), [(0, 1)]]]
    