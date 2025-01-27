import numpy as np
import random
import chess.game as game

class DumbyBot:
    def __init__(self, team: int):
        self.team = team
        self.anticipated_moves = 3

    def think(self, game: game.Game, moves: list):
        self.given_game = game

        self.moves = [[move, []] for move in moves]
        self.games = []
        for move in self.moves:
            ext_game = self.given_game
            ext_game.move_generator.update_moves(8)
            ext_game.moves.append(move)
            ext_game.move += 1
            self.games.append([ext_game, []])

        self.moves = self.anticipate2(moves)
        self.do_move(self.next_move)
        
    def anticipate(self, moves: list) -> object:
        self.moves = {}
        for i, j in enumerate(moves):
            self.moves[j.eaten_piece] = j

        self.moves = dict(sorted(self.moves.items()))
        return list(self.moves.values())[-1]
    
    def anticipate2(self, moves: list) -> object:
        self.moves = {}
        for i, j in enumerate(moves):
            self.moves[j.eaten_piece] = j

        self.moves = dict(sorted(self.moves.items()))
        return list(self.moves.values())[0]
    
    def do_move(self, move: game.Move):
        g = game.Game.current
        if move in g.move_generator.moves:
            g.move_generator.update_moves(g.turn)
            g.moves.append(move)
            g.move += 1
            if g.turn == self.team:
                to_play = self.think(g.move_generator.moves)
                self.do_move(to_play)


class Randbot(DumbyBot):
    def __init__(self, team: int):
        super().__init__(team)

    def think(self, moves):
        return random.choice(moves)
                
                
if __name__ == '__main__':
    board = np.zeros(64)
    board[1] = 8 | 2
    pieces = [['None', (0, 0), [(0, 1)]]]
    