
import Chessnut
from Chessnut import Game

def Chess_bot__starter_submission__Muhammad_Qasim_Shabbir(obs):
    
    # 0. Parse the current board state and generate legal moves using Chessnut library
    game = Game(obs.board)
    moves = list(game.get_moves())
    
    # Piece-square tables for positional evaluation
    piece_square_table = {
        'P': [  # Pawn
            0, 5, 5, 0, 5, 10, 50, 0,
            0, 5, 5, 0, 5, 10, 50, 0,
            0, 5, 10, 10, 10, 20, 50, 0,
            0, 10, 10, 20, 20, 30, 50, 0,
            0, 10, 20, 30, 30, 40, 50, 0,
            0, 10, 30, 40, 40, 50, 50, 0,
            0, 5, 5, 0, 5, 10, 50, 0,
            0, 0, 0, 0, 0, 0, 0, 0
        ],
        'N': [  # Knight
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ],
        'B': [  # Bishop
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ],
        'R': [  # Rook
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 5, 5, 0, 0, 0
        ],
        'Q': [  # Queen
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 5, 5, 5, 0, -5,
            0, 0, 5, 5, 5, 5, 0, -5,
            -10, 5, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ],
        'K': [  # King (early game)
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, 20, 0, 0, 0, 0, 20, 20,
            20, 30, 10, 0, 0, 10, 30, 20
        ]
    }

    # Function to evaluate material value
    def material_value(piece):
        values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
        return values.get(piece.upper(), 0)

    # Function to evaluate a move
    def evaluate_move(move):
        g = Game(obs.board)
        g.apply_move(move)

        # Material gain (captures)
        captured_piece = game.board.get_piece(Game.xy2i(move[2:4]))
        material_gain = material_value(captured_piece) if captured_piece != ' ' else 0
        
        # Positional value (basic example with piece-square tables)
        start_sq = Game.xy2i(move[:2])
        end_sq = Game.xy2i(move[2:4])
        piece = game.board.get_piece(start_sq).upper()
        positional_value = piece_square_table.get(piece, [0]*64)[end_sq] - \
                           piece_square_table.get(piece, [0]*64)[start_sq]
        
        # Combining material gain and positional value
        return material_gain + positional_value

    # 1. Check for checkmate moves
    for move in moves:
        g = Game(obs.board)
        g.apply_move(move)
        if g.status == Game.CHECKMATE:
            return move

    # 2. Evaluate and rank moves based on strategies
    scored_moves = [(move, evaluate_move(move)) for move in moves]
    scored_moves.sort(key=lambda x: x[1], reverse=True)

    # 3. Additional Strategies

    # 3.1. Center control strategy
    def center_control(board):
        center_squares = ['d4', 'd5', 'e4', 'e5']
        score = 0
        for square in center_squares:
            piece = board.get_piece(Game.xy2i(square))
            if piece != ' ':
                score += material_value(piece)
        return score
    
    # 3.2. King safety: prioritizing moves that protect the king
    def king_safety(board):
        king_square = board.find_king(1 if board.turn == 'w' else 0)
        safe_squares = [king_square]
        score = 0
        for sq in safe_squares:
            piece = board.get_piece(sq)
            if piece != ' ':
                score += material_value(piece)
        return score
    
    # 3.3. Threat detection: prioritize moves that threaten the opponent's high-value pieces
    def threat_detection(board):
        score = 0
        for move in moves:
            end_sq = Game.xy2i(move[2:4])
            opponent_piece = board.get_piece(end_sq)
            if opponent_piece != ' ' and material_value(opponent_piece) >= 5:
                score += material_value(opponent_piece)
        return score

    # Ranking moves based on the new strategies
    best_move = max(scored_moves, key=lambda x: x[1])[0]
    return best_move
