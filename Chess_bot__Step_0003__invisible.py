
import time,random
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
    

def make_move(move, time_to_start_thinking, is_execute_print=False):
    duration = round(time.time() - time_to_start_thinking,3)
    if is_execute_print == True:
        print(f'[{move}, {duration}]')
    return move


def panic_mode(game, fen):
    # Aaaahhhh! Oh no, I'm running out of time!
    moves = game.get_moves()
    for move in moves:
        game.apply_move(move)
        if game.status == Game.CHECKMATE:
            return move
        game.set_fen(fen)
    return random.choice(moves)


def Chess_bot__Step_0003__invisible(obs):
    time_start = time.time()
    game = Game(obs.board)
    moves = list(game.get_moves())

    
    game = Game(fen=obs.board)  # Intialize the game state with the current FEN
    if obs.remainingOverageTime < 2:
        return panic_mode(game, obs.board)

    # Remove 'random' queen

    evas, moves_eva, eva_init = [],[], evaluate_position(game.board)
    
    for move in moves:
        g = Game(obs.board)
        g.apply_move(move)  
        eva_after = evaluate_position(g.board)
        moves_eva.append({
            'move': move,
            'max' : eva_after - eva_init}
        )
        evas.append(eva_after)

    if len(moves_eva) >= 1:
        moves_eva = sorted(moves_eva, key=lambda x: x['max'], reverse=True)
        max_move = moves_eva[0] if moves_eva != None and len(moves_eva) >= 1 else None
        if max_move != None:
            if max_move['max'] == 100 : 
                print(max_move)
                return make_move(max_move['move'],time_start)
            if max_move['max'] == 50  : 
                print(max_move)
                return make_move(max_move['move'],time_start)

    
    # don't give up the queen

    
    # evas, moves_eva, bad_moves = [],[],[]

    # for move in moves:
    #     g = Game(obs.board)
    #     g.apply_move(move)  
    #     eva_after = evaluate_position(g.board)
    #     moves_eva.append({
    #         'fen'            : g.get_fen(),
    #         'opp_moves'      : list(g.get_moves()),
    #         'move'           : move,
    #         'current_eva'    : eva_after - eva_init,
    #         'answer_opp_min' : 0}
    #     )
    #     evas.append(eva_after)

    #     print(len(oppo_moves))
    #     # print( 'qnt moves oppo = ',len(moves_eva['opp_moves']), oppo_moves)

    # opp_mins = []
        
    # for e in moves_eva:
    #     g = Game(e['fen'])
    #     opp_moves = list(g.get_moves())
    #     # afters = []
    #     # for move in opp_moves:
    #     #     g = Game(e['fen'])
    #     #     g.apply_move(move)
    #     #     eva_after = evaluate_position(g.board)
    #     #     afters.append(eva_after)
    #     # e['min'] = sorted(afters)[0]
    #     opp_mins.append(e['answer_opp_min'])
    
    # exact copy of Bovard Doerschuk-Tiberi
    # 1. Check a subset of moves for checkmate
    for move in moves:
        g = Game(obs.board)
        g.apply_move(move)
        if g.status == Game.CHECKMATE:
            return make_move(move,time_start)

    # 2. Check for captures
    for move in moves:
        if game.board.get_piece(Game.xy2i(move[2:4])) != ' ':
            #print(f'\n{move}\n')
            return make_move(move,time_start)

    # 3. Check for queen promotions
    for move in moves:
        if "q" in move.lower():
            #print(f'\n{move}\n')
            return make_move(move,time_start)

    # 4. Random move if no checkmates or captures

    move = random.choice(moves)
    
    return make_move(move,time_start)
