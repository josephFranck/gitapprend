
from Chessnut import Game

def Chess_bot__with_scoring__0I1(obs):
    """
    Compact chess bot that prioritizes checkmates, captures, and key moves.
    """
    game = Game(obs.board)
    moves = list(game.get_moves())
    if not moves:
        return None
        
    # Piece values for capture evaluation. Same as in the game
    values = {'P':1, 'N':3, 'B':3, 'R':5, 'Q':9, 'K':0} # King does not matter here
    
    best_score = -9999
    best_moves = []
    
    for move in moves:
        score = 0
        # Try move and check for checkmate. This one is first priority.
        test_game = Game(obs.board)
        test_game.apply_move(move)
        if test_game.status == Game.CHECKMATE:
            return move
            
        # If caoture exists, evaluate captures
        captured = game.board.get_piece(Game.xy2i(move[2:4]))
        if captured != ' ':
            score = values.get(captured.upper(), 0)
            
        # Bonus for queen promotions
        if 'q' in move.lower():
            score += 8 # P = 1, Q = 9
            
        # Track best moves
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
            
    # Return a random best move
    return best_moves[0] if best_moves else random.choice(moves)
