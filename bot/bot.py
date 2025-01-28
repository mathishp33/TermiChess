import numpy as np
import random
import chess.game as game

class DumbyBot:
    def __init__(self, team: int):
        self.team = team
        self.anticipated_moves = 2

    def think(self, game: game.Game, moves: list):
        self.given_game = game
        self.games = []
        self.count_down = self.anticipated_moves
        self.turn = 16

        self.moves = [[move, move.eaten_piece, self.given_game, []] for move in moves]

        if self.anticipated_moves < 2:
            self.finals_moves = self.moves
            return self.anticipate(self.finals_moves)
        self.count_down -= 1
        
        while self.count_down > 0:
            self.moves = self.parsifier(self.moves, self.given_game) 
            
        self.counting_moves(self.moves)
            
    def parsifier(self, moves: list, game: game):
        for i, move in enumerate(moves):
            ext_game = game
            ext_game.move_generator.update_moves(self.turn)
            ext_game.moves.append(move[0])
            ext_game.move += 1
            self.turn = 8 if self.turn == 16 else 16
            self.count_down -= 1
            for k, j in enumerate(ext_game.move_generator.moves):
                move[2].append([j, j.eaten_piece, self.given_game, []])

        return moves

    def counting_moves(self, moves: list):
        self.better_score = []
        for move in moves:
            if move[3] != []:
                for move2 in move[3]:


class Randbot(DumbyBot):
    def __init__(self, team: int):
        super().__init__(team)

    def think(self, moves):
        return random.choice(moves)
                
                
if __name__ == '__main__':
    board = np.zeros(64)
    board[1] = 8 | 2
    pieces = [['None', (0, 0), [(0, 1)]]]
    