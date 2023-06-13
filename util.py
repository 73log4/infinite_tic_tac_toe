import math

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
