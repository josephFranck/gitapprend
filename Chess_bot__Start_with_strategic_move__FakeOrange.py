
import random
from Chessnut import Game

# define piece values
PIECE_VALUES = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 50}

def evaluate_capture(game, move):
    """
    Evaluate the value of a capture move based on the target piece's value.

    Args:
        game: Current Game object.
        move: A move string in UCI format.

    Returns:
        Integer value representing the target piece's value.
    """
    target_square = move[2:4]  # Target position of the move
    target_piece = game.board.get_piece(Game.xy2i(target_square))
    if target_piece != ' ':
        return PIECE_VALUES[target_piece.lower()]
    return 0


def Chess_bot__Start_with_strategic_move__FakeOrange(obs):
    # 0. Parse the current board state and generate legal moves
    game = Game(obs.board)
    moves = list(game.get_moves())

    # 1. Check for checkmate
    for move in moves:
        g = Game(obs.board)
        g.apply_move(move)
        if g.status == Game.CHECKMATE:
            return move

    # 2. Check for valuable captures
    capture_moves = [(move, evaluate_capture(game, move)) for move in moves]
    capture_moves = [m for m in capture_moves if m[1] > 0]  # Filter only capture moves
    if capture_moves:
        return max(capture_moves, key=lambda x: x[1])[0]  # Return the move with the highest capture value

    # 3. Check for queen promotions
    promotion_moves = [move for move in moves if "q" in move.lower()]
    if promotion_moves:
        return random.choice(promotion_moves)

    # 4. Random move if no better options
    return random.choice(moves)
