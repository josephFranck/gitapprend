
import logging
from Chessnut import Game

# Configure Debugging and Logging
DEBUG = True
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def debug(message):
    """Utility function for debugging."""
    if DEBUG:
        logging.debug(message)

# Constants
PIECE_VALUES = {
    "p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0,
    "P": -1, "N": -3, "B": -3, "R": -5, "Q": -9, "K": 0
}
CENTER_SQUARES = {"d4", "d5", "e4", "e5"}

def load_weights():
    """Load weights for move prioritization."""
    # Optional: Extend with dynamic learning
    return {"central_control": 3, "captures": 5, "check": 10, "promotion": 15}

WEIGHTS = load_weights()

def parse_board_from_fen(fen):
    """
    Parse the board from the FEN string into a dictionary representation.
    Returns a dictionary where keys are square names (e.g., "a1") and values are pieces (e.g., "P", "r").
    """
    rows = fen.split()[0].split("/")
    board = {}
    for rank_idx, row in enumerate(rows):
        file_idx = 0
        for char in row:
            if char.isdigit():
                file_idx += int(char)  # Skip empty squares
            else:
                square = f"{chr(file_idx + ord('a'))}{8 - rank_idx}"
                board[square] = char
                file_idx += 1
    return board

def get_game_phase(game):
    """
    Determine the game phase: opening, midgame, or endgame.
    Based on material count.
    """
    fen = game.get_fen()
    board = parse_board_from_fen(fen)
    material_count = sum(abs(PIECE_VALUES[piece.lower()]) for piece in board.values() if piece != " ")
    if material_count > 30:
        return "opening"
    elif 20 < material_count <= 30:
        return "midgame"
    else:
        return "end"

def prioritize_moves(game, moves):
    """
    Prioritize moves based on first principles and game phase.
    """
    game_phase = get_game_phase(game)
    prioritized_moves = []

    for move in moves:
        piece = game.board.get_piece(Game.xy2i(move[:2]))
        target_square = move[2:4]
        target_piece = game.board.get_piece(Game.xy2i(target_square))

        # Checkmate moves (highest priority)
        g = Game(game.get_fen())
        g.apply_move(move)
        if g.status == Game.CHECKMATE:
            debug(f"Checkmate move found: {move}")
            return [move]

        # Endgame: Aggressively target the king
        if game_phase == "end":
            if g.status == Game.CHECK:
                debug(f"Check move in endgame: {move}")
                prioritized_moves.append((move, WEIGHTS["check"]))
            elif target_piece == 'K':  # Target the king
                debug(f"King-targeting move: {move}")
                prioritized_moves.append((move, WEIGHTS["check"]))
            continue

        # Captures (high priority)
        if target_piece != ' ':
            debug(f"Capture move: {move}, Captures: {target_piece}")
            prioritized_moves.append((move, WEIGHTS["captures"] + PIECE_VALUES.get(target_piece.lower(), 0)))

        # Central control (medium priority)
        elif target_square in CENTER_SQUARES:
            debug(f"Central control move: {move}")
            prioritized_moves.append((move, WEIGHTS["central_control"]))

        # Development of knights and bishops (early-game priority)
        elif piece.lower() in {'n', 'b'}:
            debug(f"Development move: {move}")
            prioritized_moves.append((move, 1))

        # Pawn promotion (endgame priority)
        elif piece.lower() == 'p':
            rank = int(target_square[1])
            if (rank == 8 and piece.islower()) or (rank == 1 and piece.isupper()):
                debug(f"Pawn promotion move: {move}")
                prioritized_moves.append((move, WEIGHTS["promotion"]))

        # Default: Other moves (low priority)
        else:
            prioritized_moves.append((move, 0))

    # Sort moves by priority (descending)
    prioritized_moves.sort(key=lambda x: x[1], reverse=True)
    return [move for move, _ in prioritized_moves]

def Chess_bot__AGN_Cube4D_DRE__Callum_Maystone(obs):
    """
    Enhanced chess bot using prioritized move evaluation.
    """
    game = Game(obs.board)
    moves = list(game.get_moves())

    if not moves:
        return None  # No legal moves available

    # Prioritize moves based on first principles
    prioritized_moves = prioritize_moves(game, moves)

    # Pick the best move (highest priority)
    best_move = prioritized_moves[0] if prioritized_moves else random.choice(moves)
    debug(f"Best move selected: {best_move}")
    return best_move
