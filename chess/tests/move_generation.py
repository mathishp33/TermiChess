from chess.game import *

GAME = Game("TERMINAL")

def test_move_generation(depth: int, team: int = WHITE):
    if depth == 0:
        return 1
    
    moves_count = 0
    for move in GAME.move_generator.generate_legal_moves(team):
        move.do(True)
        moves_count += test_move_generation(depth - 1, WHITE if team == BLACK else BLACK)
        move.undo(True)
    return moves_count