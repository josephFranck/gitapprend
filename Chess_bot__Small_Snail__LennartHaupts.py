
import random
from Chessnut import Game

# Value map for chess pieces
value_map = {
    " ": 0,
    "p": 10,   "P": 10,  # Pawns
    "n": 30,   "N": 30,  # Knights
    "b": 35,   "B": 35,  # Bishops
    "r": 50,   "R": 50,  # Rooks
    "q": 90,   "Q": 90,  # Queens
    "k": 200, "K": 200
}

standard_board_map = {
    "a8": -1, "b8": 2, "c8": 3, "d8": 3, "e8": 3, "f8": 3, "g8": 2, "h8": -1,
    "a7": 0, "b7": 1, "c7": 1, "d7": 1, "e7": 1, "f7": 1, "g7": 1, "h7": 0,
    "a6": 0, "b6": 3, "c6": 4, "d6": 4, "e6": 4, "f6": 4, "g6": 3, "h6": 0,
    "a5": 0, "b5": 3, "c5": 5, "d5": 8, "e5": 8, "f5": 5, "g5": 3, "h5": 0,
    "a4": 0, "b4": 3, "c4": 5, "d4": 8, "e4": 8, "f4": 5, "g4": 3, "h4": 0,
    "a3": 0, "b3": 3, "c3": 4, "d3": 4, "e3": 4, "f3": 4, "g3": 3, "h3": 0,
    "a2": 0, "b2": 1, "c2": 1, "d2": 1, "e2": 1, "f2": 1, "g2": 1, "h2": 0,
    "a1": -1, "b1": 2, "c1": 3, "d1": 3, "e1": 3, "f1": 3, "g1": 2, "h1": -1
    }

pawn_board_map = {
    "a8": 8, "b8": 8, "c8": 8, "d8": 8, "e8": 8, "f8": 8, "g8": 8, "h8": 8,
    "a7": 8, "b7": 8, "c7": 8, "d7": 8, "e7": 8, "f7": 8, "g7": 8, "h7": 8,
    "a6": 0, "b6": 0, "c6": 4, "d6": 4, "e6": 4, "f6": 4, "g6": 0, "h6": 0,
    "a5": 0, "b5": 2, "c5": 5, "d5": 8, "e5": 8, "f5": 5, "g5": 2, "h5": 0,
    "a4": 0, "b4": 2, "c4": 5, "d4": 8, "e4": 8, "f4": 5, "g4": 2, "h4": 0,
    "a3": 0, "b3": 0, "c3": 4, "d3": 4, "e3": 4, "f3": 4, "g3": 0, "h3": 0,
    "a2": 8, "b2": 8, "c2": 8, "d2": 8, "e2": 8, "f2": 8, "g2": 8, "h2": 8,
    "a1": 8, "b1": 8, "c1": 8, "d1": 8, "e1": 8, "f1": 8, "g1": 8, "h1": 8
}

king_board_map = {
    "a8": -2, "b8": -2, "c8": -3, "d8": -4, "e8": -4, "f8": -3, "g8": -2, "h8": -2,
    "a7": -2, "b7": -3, "c7": -4, "d7": -5, "e7": -5, "f7": -4, "g7": -3, "h7": -2,
    "a6": -3, "b6": -4, "c6": -5, "d6": -6, "e6": -6, "f6": -5, "g6": -4, "h6": -3,
    "a5": -4, "b5": -5, "c5": -6, "d5": -7, "e5": -7, "f5": -6, "g5": -5, "h5": -4,
    "a4": -4, "b4": -5, "c4": -6, "d4": -7, "e4": -7, "f4": -6, "g4": -5, "h4": -4,
    "a3": -3, "b3": -4, "c3": -5, "d3": -6, "e3": -6, "f3": -5, "g3": -4, "h3": -3,
    "a2": -2, "b2": -3, "c2": -4, "d2": -5, "e2": -5, "f2": -4, "g2": -3, "h2": -2,
    "a1": -2, "b1": -2, "c1": -3, "d1": -4, "e1": -4, "f1": -3, "g1": -2, "h1": -2
}

rook_board_map = {
    "a8": 5, "b8": 6, "c8": 7, "d8": 8, "e8": 8, "f8": 7, "g8": 6, "h8": 5,
    "a7": 4, "b7": 5, "c7": 6, "d7": 7, "e7": 7, "f7": 6, "g7": 5, "h7": 4,
    "a6": 3, "b6": 4, "c6": 5, "d6": 6, "e6": 6, "f6": 5, "g6": 4, "h6": 3,
    "a5": 3, "b5": 4, "c5": 5, "d5": 6, "e5": 6, "f5": 5, "g5": 4, "h5": 3,
    "a4": 3, "b4": 4, "c4": 5, "d4": 6, "e4": 6, "f4": 5, "g4": 4, "h4": 3,
    "a3": 3, "b3": 4, "c3": 5, "d3": 6, "e3": 6, "f3": 5, "g3": 4, "h3": 3,
    "a2": 4, "b2": 5, "c2": 6, "d2": 7, "e2": 7, "f2": 6, "g2": 5, "h2": 4,
    "a1": 5, "b1": 6, "c1": 7, "d1": 8, "e1": 8, "f1": 7, "g1": 6, "h1": 5
}

board_map = {
    10: pawn_board_map,
    30: standard_board_map,
    35: standard_board_map,
    50: rook_board_map,
    90: standard_board_map,
    200: king_board_map
}

def check_for_simple_threat(opponent_moves, cell, piece_value):
    # Checks if piece could be attacked by opponent's piece
    for move in opponent_moves:
        if cell == move[2:4]:
            return piece_value
    return 0

def find_move(game, fen):
    moves = game.get_moves()
    best_move = None
    best_value = -100

    for move in moves:
        piece_value = value_map[game.board.get_piece(game.xy2i(move[:2]))]
        capture_value = value_map[game.board.get_piece(game.xy2i(move[2:4]))]
        game.apply_move(move)

        if game.status == Game.CHECKMATE:
            return move

        # Get opponent's moves and calculate potential capture value
        opponent_moves = game.get_moves()
        netto_value = capture_value - check_for_simple_threat(opponent_moves, move[2:4], piece_value)

        if netto_value >= 0:
            netto_value += board_map[piece_value][move[2:4]] 
            if netto_value > best_value:
                best_value = netto_value 
                best_move = move
                if netto_value >= 10:  # Early exit if sufficient gain is found
                    return best_move

        # Reset game state after each move
        game.set_fen(fen)

    if best_move:
        return best_move
    return random.choice(moves)

def panic_mode(game, fen):
    # Aaaahhhh! Oh no, I'm running out of time!
    moves = game.get_moves()
    
    for move in moves:
        game.apply_move(move)
        if game.status == Game.CHECKMATE:
            return move
        game.set_fen(fen)
    return random.choice(moves)

def Chess_bot__Small_Snail__LennartHaupts(obs):
    game = Game(fen=obs.board)  # Intialize the game state with the current FEN
    if obs.remainingOverageTime < 2:
        if obs.remainingOverageTime < 0.9:
            return random.choice(game.get_moves())
        return panic_mode(game, obs.board)

    # Find the "best" move using the evaluation function
    return find_move(game, obs.board)
