import numpy as np

class Bot:
    def __init__(self):
        pass

    def input(self, moves: list):
        pass

def turn(board, pieces):
    #pieces[i] = [type, pos, moves]
    moves = []
    for i in pieces:
        for move in i[2]:
            pos = i[1]
            next_move = (pos[0]+move[0], pos[1]+move[1])
            if int(board[next_move[0]*8 + next_move[1]]) & 24 == 8:
                moves.append(next_move)
                
    print(moves)
                
                
if __name__ == '__main__':
    board = np.zeros(64)
    board[1] = 8 | 2
    pieces = [['None', (0, 0), [(0, 1)]]]
    turn(board, pieces)