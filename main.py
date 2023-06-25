import pygame
import math
import time
import random
from draw_io import draw_board, draw_end_game_result, draw_start_text
from util import *
from class_util import Square
from ai_bot import evaluate_new_board, best_move, best_move_2


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
