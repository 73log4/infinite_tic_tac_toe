import pygame
from util import *
from class_util import Square

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
    text_rect.center = (SCREEN_SIZE // 2, 35)
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

