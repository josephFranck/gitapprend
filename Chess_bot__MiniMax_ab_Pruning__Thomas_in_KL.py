
import time
import random
import Chessnut
from Chessnut import Game


piece_sym = ['K', 'k', 'Q', 'q', 'R', 'r', 'B', 'b', 'N', 'n', 'P', 'p']
piece_val = [0, 0, 100, 100, 50, 50, 30, 30, 30, 30, 10, 10]
piece_val_dict = dict(zip(piece_sym, piece_val))


def evaluate_position(board):
    total_score = 0
    for square in range(64):
        piece = board.get_piece(square)
        if piece != ' ':
            piece_value = piece_val_dict.get(piece.upper(), 0)
            if piece.isupper(): 
                total_score += piece_value # White piece
            else: 
                total_score -= piece_value # Black piece
    return total_score


# Minimax algorithm with alpha-beta pruning to evaluate and choose the best move for the bot.
def minimax(game, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or game.status in [Game.CHECKMATE, Game.STALEMATE]:
        return evaluate_position(game.board), None
    moves = list(game.get_moves())
    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            g = Game(game.get_fen())
            g.apply_move(move)
            eval_score, _ = minimax(g, depth - 1, False, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            g = Game(game.get_fen())
            g.apply_move(move)
            eval_score, _ = minimax(g, depth - 1, True, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move

default_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    
def Chess_bot__MiniMax_ab_Pruning__Thomas_in_KL(obs):
    # Get FEN string from the Board object
    game = Game(obs.board)
    moves = list(game.get_moves())
    
    # 1. Try to detect checkmate
    for move in moves:
        g = Game(obs.board)
        g.apply_move(move)
        if g.status == Game.CHECKMATE:
            return move

    # 2. Check for queen promotions
    for move in moves:
        if "q" in move.lower():
            return move

    # 3. Use minimax algorithm with a depth of 3 to find the best move
    _, best_move = minimax(game, 1, True)
    return best_move if best_move else random.choice(moves)
