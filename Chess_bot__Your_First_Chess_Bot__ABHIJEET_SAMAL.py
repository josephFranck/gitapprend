from Chessnut import Game
import random

def chess_bot__Your_First_Chess_Bot__ABHIJEET_SAMAL(obs):
    """
    Simple chess bot that prioritizes checkmates, then captures, queen promotions, then randomly moves.

    Args:
        obs: An object with a 'board' attribute representing the current board state as a FEN string.

    Returns:
        A string representing the chosen move in UCI notation (e.g., "e2e4")
    """
    # 0. Parse the current board state and generate legal moves using Chessnut library
    game = Game(obs.board)
    moves = list(game.get_moves())

    # 1. Check a subset of moves for checkmate
    for move in moves[:10]:
        g = Game(obs.board)
        g.apply_move(move)
        if g.status == Game.CHECKMATE:
            return move

    # 2. Check for captures
    for move in moves:
        if game.board.get_piece(Game.xy2i(move[2:4])) != ' ':
            return move

    # 3. Check for queen promotions
    for move in moves:
        if "q" in move.lower():
            return move

    # 4. Pawn structure management
    for move in moves:
        if move[0] == 'P':  # pawn move
            # Avoid weak pawns
            if game.board.get_piece(Game.xy2i(move[2:4])) == 'P':
                continue
            # Create pawn chains
            if game.board.get_piece(Game.xy2i(move[2:4] + '1')) == 'P':
                return move

    # 5. Piece development
    for move in moves:
        if move[0] in ['N', 'B', 'R', 'Q']:
            # Develop pieces towards the center
            if abs(Game.xy2i(move[2:4]) - 4) < 3:
                return move

  # 6. Attack and defense
    for move in moves:
        # Identify weak points in opponent's position
        opponent_piece = game.board.get_piece(Game.xy2i(move[2:4]))
        if opponent_piece!='' and opponent_piece!= 'K':
            return move

     # 7. Endgame play
    for move in moves:
        # Promote pawns to queens or rooks
        if move[0] == 'P' and move[2] == '8':
            return move

    # 4. Random move if no checkmates or captures
    return random.choice(moves)
