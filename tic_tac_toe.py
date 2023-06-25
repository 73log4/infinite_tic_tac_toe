import pygame
import math
import time
import random

# -------------------------------------------

MODE = 'L'
SHOW_LAST_MOVE = False
MINI_MAX_FIRST_MOVES = 20
MINI_MAX_DEPTH = 5
MAX_SQUARE_SCORE = 2048
WIN_ROW = 5
X_PLAYER = 1
O_PLAYER = -1
PLAYER_ID = {1: "X", -1: "O"}
EMPTY_SQUARE = 0
BOT_PLAYER = 1

STARTING_PLAYER = BOT_PLAYER

BOARD_SIZE = 12
SCREEN_SIZE = 650
SQUARE_SIZE = SCREEN_SIZE // BOARD_SIZE
SCREEN_COLOR = (47, 47, 47) if MODE == 'D' else (230, 230, 230)
PLAYERS_COLOR = (48, 204, 116) if MODE == 'D' else (103, 128, 254)  # (48, 204, 116), (255, 124, 8)
LINE_COLOR = (35, 35, 35) if MODE == 'D' else (180, 180, 180)
LAST_COLOR = (54, 54, 54) if MODE == 'D' else (212, 212, 212)
# the entries in the dict are (length of connected line, blocked or not (1 or 0))
EVAL = {(1, 1): 2, (-1, 1): -2, (1, 0): 8, (-1, 0): -8, (2, 1): 4, (-2, 1): -4, (2, 0): 32, (-2, 0): -32, (3, 1): 16,
        (-3, 1): -16, (3, 0): 128, (-3, 0): -128, (4, 1): 128, (-4, 1): -128, (4, 0): 256, (-4, 0): -256}

ROW_ID = {(0, 0): 0, (1, 1): 1, (-1, 1): 2, (1, 0): 3, (-1, 0): 4, (2, 1): 5, (-2, 1): 6, (2, 0): 7, (-2, 0): 8,
          (3, 1): 9,
          (-3, 1): 10, (3, 0): 11, (-3, 0): 12, (4, 1): 13, (-4, 1): 14, (4, 0): 15, (-4, 0): 16}

DIRECTIONS = [(1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (0, 1)]
DIRECTIONS_INDEX = {(1, 1): 0, (1, 0): 1, (1, -1): 2, (0, -1): 3, (-1, -1): 4, (-1, 0): 5, (-1, 1): 6, (0, 1): 7}


def depth_regulator(n):
    if 0 <= n <= 6:
        return MINI_MAX_DEPTH - 1
    elif 7 <= n <= 10:
        return MINI_MAX_DEPTH - 2
    else:
        return 3

# ------------------------------------------------------

class Square:
    def __init__(self):
        self.occupied = False
        self.type = EMPTY_SQUARE
        self.eval = {d: 0 for d in DIRECTIONS}
        self.square_id = [0] * 8
        self.neigh_occupied_squares = {d: False for d in DIRECTIONS}

    def not_connected(self):
        return not any(self.neigh_occupied_squares.values())

    def total_score(self):
        return sum(self.eval.values())

    def abs_total_score(self):
        sum1 = 0
        values = self.eval.values()
        for i in values:
            sum1 += abs(i)
        return sum1

# ----------------------------------------------

CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 3
X_MARGIN = 1 / 6
X_WIDTH = 4


def draw_circle(screen, x, y):
    """
    draw a circle to the screen, with center at the square (x,y)
    """
    center = ((x + 1 / 2) * SQUARE_SIZE, (y + 1 / 2) * SQUARE_SIZE)
    pygame.draw.circle(screen, PLAYERS_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)


def draw_X(screen, x, y):
    """
    draw an X in the middle of the square (x,y)
    """
    color = PLAYERS_COLOR
    corner1 = ((x + X_MARGIN) * SQUARE_SIZE, (y + X_MARGIN) * SQUARE_SIZE)
    corner3 = ((x + 1 - X_MARGIN) * SQUARE_SIZE, (y + 1 - X_MARGIN) * SQUARE_SIZE)
    corner2 = ((x + 1 - X_MARGIN) * SQUARE_SIZE, (y + X_MARGIN) * SQUARE_SIZE)
    corner4 = ((x + X_MARGIN) * SQUARE_SIZE, (y + 1 - X_MARGIN) * SQUARE_SIZE)
    pygame.draw.line(screen, color, corner1, corner3, X_WIDTH)
    pygame.draw.line(screen, color, corner2, corner4, X_WIDTH)


def draw_last_move(screen, x, y):
    pygame.draw.rect(screen, LAST_COLOR, pygame.Rect(SQUARE_SIZE * x, SQUARE_SIZE * y,
                                                     SQUARE_SIZE, SQUARE_SIZE))


def draw_square_score(screen, x, y, score):
    pygame.draw.rect(screen, (min(score, 255), 0, 0), pygame.Rect(SQUARE_SIZE * x, SQUARE_SIZE * y,
                                                        SQUARE_SIZE, SQUARE_SIZE))


def draw_board(board, screen, last_move, first_turn):
    """
    draw the current board situation.
    """
    screen.fill(SCREEN_COLOR)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (j, i) == last_move:
                if not first_turn:
                    draw_last_move(screen, j, i)
            if not board[i][j].occupied:
                pass
                # draw_square_score(screen, j, i, board[i][j].abs_total_score())
            if board[i][j].type == BOT_PLAYER:
                draw_X(screen, j, i)
            elif board[i][j].type == -BOT_PLAYER:
                draw_circle(screen, j, i)
            else:
                pass  # draw_eval(board, j, i, screen)

    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, SCREEN_SIZE), 2)
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * i), (SCREEN_SIZE, SQUARE_SIZE * i), 2)


def draw_eval(board, x, y, screen):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(str(board[y][x].abs_total_score()), True, PLAYERS_COLOR, SCREEN_COLOR)
    text_rect = text.get_rect()
    text_rect.center = ((x + 1 / 2) * SQUARE_SIZE, (y + 1 / 2) * SQUARE_SIZE)
    screen.blit(text, text_rect)

def draw_end_game_result(screen, winner):
    font = pygame.font.SysFont("calibri", 42)
    text = font.render(f'Player {PLAYER_ID[winner]} Wins!', True, PLAYERS_COLOR, SCREEN_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE // 2, 28)
    screen.blit(text, text_rect)
    text2 = font.render('To play again press 3', True, PLAYERS_COLOR, SCREEN_COLOR)
    text_rect2 = text2.get_rect()
    text_rect2.center = (SCREEN_SIZE // 2, 60)
    screen.blit(text2, text_rect2)

def draw_start_text(screen):
    font = pygame.font.SysFont("calibri", 42)
    text1 = font.render('To play first press 1', True, PLAYERS_COLOR, SCREEN_COLOR)
    text_rect1 = text1.get_rect()
    text_rect1.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2)
    text2 = font.render('To play second press 2', True, PLAYERS_COLOR, SCREEN_COLOR)
    text_rect2 = text2.get_rect()
    text_rect2.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 40)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)

# --------------------------------------------

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
    print(cnt[0])
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

# ---------------------------------------

def start_game_against_bot():
    board = [[Square() for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    possible_moves = {(BOARD_SIZE // 2, BOARD_SIZE // 2)}

    pygame.init()
    pygame.display.set_caption('Tic Tac Toe')
    # pygame_icon = pygame.image.load('icon.png')
    # pygame.display.set_icon(pygame_icon)
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

    mouse = [0, 0]
    game_ended = False
    winner = None
    # game over setup

    bot_turn = True if STARTING_PLAYER == BOT_PLAYER else False
    player_move = not bot_turn
    last_move = (BOARD_SIZE // 2, BOARD_SIZE // 2)
    game_started = False
    first_turn = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and not game_ended and not bot_turn:
                x, y = mouse[0] // SQUARE_SIZE, mouse[1] // SQUARE_SIZE
                if board[y][x].occupied:
                    continue
                player_move = True
                last_move = (x, y)
            if event.type == pygame.KEYDOWN and not game_started:
                if event.key == pygame.K_1:
                    bot_turn = False
                    game_started = True
                elif event.key == pygame.K_2:
                    bot_turn = True
                    game_started = True
            if event.type == pygame.KEYDOWN and game_ended:
                if event.key == pygame.K_3:
                    game_ended = False
                    board = [[Square() for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
                    possible_moves = {(BOARD_SIZE // 2, BOARD_SIZE // 2)}
                    bot_turn = True if STARTING_PLAYER == BOT_PLAYER else False
                    player_move = not bot_turn
                    last_move = (BOARD_SIZE // 2, BOARD_SIZE // 2)
                    game_started = False
                    first_turn = True
        if not game_ended and game_started:
            if bot_turn:
                # last_move = best_move(board, possible_moves)
                last_move = best_move_2(board, possible_moves)
                if evaluate_new_board(board, possible_moves, *last_move, BOT_PLAYER):
                    winner = BOT_PLAYER
                    game_ended = True
                bot_turn = False
            elif player_move:
                first_turn = False
                if evaluate_new_board(board, possible_moves, *last_move, -BOT_PLAYER):
                    winner = -BOT_PLAYER
                    game_ended = True
                    continue
                player_move = False
                bot_turn = True
        draw_board(board, screen, last_move, first_turn)
        if not game_started:
            draw_start_text(screen)
        if game_ended:
            draw_end_game_result(screen, winner)
        mouse = pygame.mouse.get_pos()
        pygame.display.update()

start_game_against_bot()
# start_game_bot_vs_bot()

