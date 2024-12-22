
from Chessnut import Game
import time
import random

DEBUG = True

# Piece values for evaluation
PIECE_VALUES = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 10}

def log_message(message):
    """Helper function to print messages if DEBUG is True."""
    if DEBUG:
        current_time = time.time()
        print(f"[{current_time:.2f}] {message}")

def enhanced_heuristic_with_time_limit(obs, per_move_time, remaining_time):
    """
    Enhanced heuristic evaluation with adjusted scoring to prioritize captures and protect endangered pieces.
    Includes detailed logging via log_message.
    """
    game = Game(obs.board)
    moves = list(game.get_moves())
    random.shuffle(moves)  # Randomize moves to add variation
    log_message(f"Available moves: {moves}")

    best_score = float('-inf')
    best_move = None
    start_time = time.time()

    for move in moves:
        move_start = time.time()
        elapsed = move_start - start_time
        remaining = remaining_time - elapsed
        if remaining <= 0:
            log_message("Time limit for heuristic evaluation reached. Stopping.")
            break  # Stop evaluating if total time runs out

        log_message(f"Evaluating move: {move}. Elapsed: {elapsed:.2f}s, Remaining: {remaining:.2f}s")

        if elapsed >= per_move_time:
            log_message(f"Skipping move {move} due to per-move time limit.")
            continue  # Skip move if per-move time limit is exceeded

        move_score = 0
        from_square = move[:2]
        to_square = move[2:4]

        # Simulate the move
        new_game = Game(str(game))
        new_game.apply_move(move)

        # Immediate checkmate detection
        if new_game.status == Game.CHECKMATE:
            log_message(f"Checkmate detected with move: {move}. Returning immediately.")
            return move

        # Piece and target evaluation
        piece_moved = game.board.get_piece(Game.xy2i(from_square))
        target_piece = game.board.get_piece(Game.xy2i(to_square))

        # Add score for captures (material gain)
        if target_piece != ' ':
            # Increase capture bonus based on the value of the captured piece
            capture_value = PIECE_VALUES[target_piece.lower()]
            move_score += capture_value * 100  # Amplify the importance of captures
            log_message(f"Move {move} captures {target_piece}. Capture value: {capture_value}. Updated score: {move_score}")

            # Encourage favorable exchanges
            piece_value = PIECE_VALUES.get(piece_moved.lower(), 0)
            net_gain = capture_value - piece_value
            move_score += net_gain * 50  # Encourage exchanges where net gain is positive
            log_message(f"Net gain from exchange: {net_gain}. Updated score: {move_score}")

        # Prioritize pawn promotion
        if 'q' in move.lower():
            move_score += PIECE_VALUES['q'] * 100  # Increase bonus for promotion
            log_message(f"Move {move} promotes to queen. Updated score: {move_score}")

        # Center control bonus (e4, d4, e5, d5)
        if to_square in ['d4', 'e4', 'd5', 'e5']:
            move_score += 20
            log_message(f"Move {move} controls center. Updated score: {move_score}")

        # Check detection
        if new_game.status == Game.CHECK:
            move_score += 30
            log_message(f"Move {move} gives check. Updated score: {move_score}")

        # Evaluate if any own pieces are under attack after the move
        opponent_moves = list(new_game.get_moves())
        for opp_move in opponent_moves:
            opp_target_square = opp_move[2:4]
            own_piece = new_game.board.get_piece(Game.xy2i(opp_target_square))
            if own_piece != ' ' and own_piece.isupper():  # Assuming bot plays as White
                # Penalize based on the value of the endangered piece
                endangered_piece_value = PIECE_VALUES.get(own_piece.lower(), 0)
                move_score -= endangered_piece_value * 100  # Adjust penalty multiplier as needed
                log_message(f"Own piece {own_piece} at {opp_target_square} is endangered. Penalizing move. Updated score: {move_score}")

        # Update the best move if the score is better
        if move_score > best_score:
            best_score = move_score
            best_move = move
            log_message(f"New best move found: {best_move}. Best score updated to: {best_score}")

        move_end = time.time()
        log_message(f"Move {move} evaluation completed in {move_end - move_start:.2f}s.")

    log_message(f"Best move chosen: {best_move} with final score: {best_score}")
    return best_move if best_score > float('-inf') else None


def Chess_bot__LittleDeepBlue_0_10_4_debug__William_Guesdon(obs, config):
    """
    Combined chess agent with total and per-move time limits.
    """
    try:
        start_time = time.time()
        total_time_limit = 8.0
        per_move_time_limit = 0.1

        log_message("Starting agent evaluation")

        while True:
            elapsed_time = time.time() - start_time
            remaining_time = total_time_limit - elapsed_time

            log_message(f"Total elapsed: {elapsed_time:.2f}s, Remaining time: {remaining_time:.2f}s")

            if remaining_time <= 0.1:  # Grace period to avoid timeout
                log_message("Time is almost up. Defaulting to a random move.")
                break

            # Step 1: Use enhanced heuristic with per-move and remaining time limits
            move = enhanced_heuristic_with_time_limit(obs, per_move_time=per_move_time_limit, remaining_time=remaining_time)
            if move:
                log_message(f"Heuristic selected move: {move}")
                return move

        # Step 2: Default to a random move if time is exhausted
        game = Game(obs.board)
        random_move = random.choice(list(game.get_moves()))
        log_message(f"Random move chosen: {random_move}")
        return random_move

    except Exception as e:
        # Emergency fallback to a random move
        log_message(f"Error in agent: {e}")
        game = Game(obs.board)
        fallback_move = random.choice(list(game.get_moves()))
        log_message(f"Fallback random move chosen: {fallback_move}")
        return fallback_move
