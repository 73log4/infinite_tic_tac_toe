import math
import random
from util import *
import pygame


def update_pygame():
    pygame.display.update()

def legal_square(x, y):
    """
    return true if the square with coordinates (x, y) exist.
    """
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def move_ended_game(board, x, y):
    """
    return true if the last move, played at (x, y), ended the game.
    """
    square_type = board[y][x].type
    for d in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        x1, y1 = last_square_in_row(board, x, y, d, square_type)
        x2, y2 = last_square_in_row(board, x, y, opposite_direction(d), square_type)
        if abs(x2 - x1) >= WIN_ROW - 1 or abs(y2 - y1) >= WIN_ROW - 1:
            return True
    return False

def last_square_in_row(board, x, y, d, line_type):
    """
    return the first free square from the specified square in direction d.
    """
    while legal_square(x + d[0], y + d[1]) and board[y + d[1]][x + d[0]].type == line_type:
        x, y = x + d[0], y + d[1]
    return x, y

def opposite_direction(d):
    return -d[0], -d[1]

def evaluate_new_board(board, possible_moves, move_x, move_y, player, undo_move=False):
    """
    change the board evaluation accordingly to the new move, and play the new move
    if reverse=True the function will evaluate the board as if the move was undo.
    """
    move_square = board[move_y][move_x]
    if undo_move:
        move_square.type = EMPTY_SQUARE
        move_square.occupied = False
        # calculate what are the neighborhood squares of the move square
        for d in DIRECTIONS:
            if legal_square(move_x + d[0], move_y + d[1]) and board[move_y + d[1]][move_x + d[0]].occupied:
                move_square.neigh_occupied_squares[d] = True
        # add square to possible moves if it is connected to some square
        if not move_square.not_connected():
            possible_moves.add((move_x, move_y))
    else:
        move_square.type = player
        move_square.occupied = True
        move_square.neigh_occupied_squares = {d: False for d in DIRECTIONS}
        if (move_x, move_y) in possible_moves:
            possible_moves.remove((move_x, move_y))
    for d in DIRECTIONS:
        d_x, d_y = move_x + d[0], move_y + d[1]
        if legal_square(d_x, d_y) and not board[d_y][d_x].occupied:
            if not undo_move and board[d_y][d_x].not_connected():  # found new square connected to a move
                possible_moves.add((d_x, d_y))
            # update the squares around the move square about the new state of the square
            board[d_y][d_x].neigh_occupied_squares[opposite_direction(d)] = False if undo_move else True
            if undo_move and board[d_y][d_x].not_connected():  # found square that was connected only to move square
                possible_moves.remove((d_x, d_y))
        # square that may be effected by the new state of the move square
        x, y = first_free_square(board, move_x, move_y, d)
        if x != -1:
            evaluate_square_direction(board, x, y, opposite_direction(d))
    return move_ended_game(board, move_x, move_y)

def create_connected_line_identification(board, x, y, n, d, line_type):
    """
    return the signature of the connected line, for the dict EVAL.
    """
    while legal_square(x, y) and n < WIN_ROW + 1:
        square_type = board[y][x].type
        if square_type == EMPTY_SQUARE:
            return n * line_type, 0
        elif square_type != line_type:
            return n * line_type, 1
        x, y = x + d[0], y + d[1]
        n += 1
    return n * line_type, 1

def evaluate_square_direction(board, x, y, d):
    """
    calculate the square's direction d evaluation.
    """
    if board[y + d[1]][x + d[0]].occupied:
        signature = create_connected_line_identification(board, x + 2*d[0], y + 2*d[1], 1, d, board[y+d[1]][x+d[0]].type)
        if abs(signature[0]) >= WIN_ROW:  # maybe delete
            return
        else:
            board[y][x].eval[d] = EVAL[signature]
            board[y][x].square_id[DIRECTIONS_INDEX[d]] = ROW_ID[signature]
    else:
        board[y][x].eval[d] = 0
        board[y][x].square_id[DIRECTIONS_INDEX[d]] = 0

def first_free_square(board, x, y, d):
    """
    return the first free square from the specified square in direction d.
    """
    while legal_square(x + d[0], y + d[1]) and board[y + d[1]][x + d[0]].occupied:
        x, y = x + d[0], y + d[1]
    if legal_square(x + d[0], y + d[1]):
        return x + d[0], y + d[1]
    return -1, -1

def total_score(board, possible_moves):
    """
    return the board score, evaluated by the difference between the positive and negative scores
    """
    sum1 = 0
    for move in possible_moves:
        x, y = move
        sum1 += board[y][x].total_score()
    return sum1

def mini_max(board, possible_moves, cnt, depth=MINI_MAX_DEPTH, alpha=-math.inf, beta=math.inf, maximizing_player=False):
    cnt[0] += 1  # increase count of nodes
    if depth == 0:
        return total_score(board, possible_moves), -1
    player_to_play = BOT_PLAYER if maximizing_player else -BOT_PLAYER
    if maximizing_player:
        max_eval = -math.inf
        possible_moves_lst = list(possible_moves)
        possible_moves_lst.sort(key=lambda m: board[m[1]][m[0]].abs_total_score(), reverse=True)
        winning_move = possible_moves_lst[0]
        for k in range(min(MINI_MAX_FIRST_MOVES, len(possible_moves_lst))):
            j, i = possible_moves_lst[k]
            if evaluate_new_board(board, possible_moves, j, i, player_to_play):
                evaluate_new_board(board, possible_moves, j, i, player_to_play, True)
                return math.inf, (j, i)
            evaluation = mini_max(board, possible_moves, cnt, min(depth - 1, depth_regulator(k)), alpha, beta, False)[0]
            evaluate_new_board(board, possible_moves, j, i, player_to_play, True)
            if evaluation > max_eval:
                max_eval = evaluation
                winning_move = (j, i)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                return max_eval, winning_move
        return max_eval, winning_move
    else:
        min_eval = math.inf
        possible_moves_lst = list(possible_moves)
        possible_moves_lst.sort(key=lambda m: board[m[1]][m[0]].abs_total_score(), reverse=True)
        winning_move = possible_moves_lst[0]
        for k in range(min(MINI_MAX_FIRST_MOVES, len(possible_moves_lst))):
            j, i = possible_moves_lst[k]
            if evaluate_new_board(board, possible_moves, j, i, player_to_play):
                evaluate_new_board(board, possible_moves, j, i, player_to_play, True)
                return -math.inf, (j, i)
            evaluation = mini_max(board, possible_moves, cnt, min(depth - 1, depth_regulator(k)), alpha, beta, True)[0]
            evaluate_new_board(board, possible_moves, j, i, player_to_play, True)
            if evaluation < min_eval:
                min_eval = evaluation
                winning_move = (j, i)
            beta = min(beta, evaluation)
            if beta <= alpha:
                return min_eval, winning_move
        return min_eval, winning_move

def best_move_2(board, possible_moves, bot_turn=True):
    max_score = bot_turn  # bot wants to maximize score
    cnt = [0]  # count nodes in search tree
    if len(possible_moves) == 8:  # beginning of game - play random
        return random.sample(possible_moves, 1)[0]
    move = mini_max(board, possible_moves, cnt, maximizing_player=max_score)[1]
    return move

def best_move(board, possible_moves, max_score=True):
    player = BOT_PLAYER if max_score else -BOT_PLAYER
    best_x, best_y = 0, 0
    max_score = -math.inf if max_score else math.inf
    if len(possible_moves) == 8:  # beginning of game - play random
        return random.sample(possible_moves, 1)[0]
    cnt = [0]  # count number of nodes in search tree
    possible_moves_lst = list(possible_moves)
    possible_moves_lst.sort(key=lambda m: board[m[1]][m[0]].abs_total_score(), reverse=True)
    for move in possible_moves_lst:
        update_pygame()
        j, i = move
        if evaluate_new_board(board, possible_moves, j, i, player):
            print(cnt[0])  # print number of nodes
            return j, i
        score, winning_move = mini_max(board, possible_moves, cnt, maximizing_player=not max_score)
        evaluate_new_board(board, possible_moves, j, i, player, True)
        if max_score:
            if score > max_score:
                best_x, best_y = j, i
                max_score = score
        else:
            if score < max_score:
                best_x, best_y = j, i
                max_score = score
    print(cnt[0])  # print number of nodes
    if best_x == best_y == 0:
        return list(possible_moves)[0]
    return best_x, best_y
