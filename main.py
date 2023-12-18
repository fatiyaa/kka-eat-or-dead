import pygame

from cons import *
from home import Home
from board import Board
from howtoplay import HowToPlay


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load(path_icon)
pygame.display.set_caption('Eat or Death')
pygame.display.set_icon(icon)



run = True
clock = pygame.time.Clock()
home = Home(screen)
gameboard = Board(screen)
howtoplay = HowToPlay(screen)
current_screen = "HOME"

while run:
    clock.tick(60)
    screen.fill(BG)

    if current_screen == "HOME":
        home.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if home.start_button.checkMouseInput(pygame.mouse.get_pos()):
                    current_screen = "HOWTOPLAY"
                elif home.exit_button.checkMouseInput(pygame.mouse.get_pos()):
                    run = False

    elif current_screen == "HOWTOPLAY":
        howtoplay.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if howtoplay.friends_button.checkMouseInput(pygame.mouse.get_pos()):
                    gameboard.isAI(False)
                    current_screen = "GAME"
                if howtoplay.computer_button.checkMouseInput(pygame.mouse.get_pos()):
                    gameboard.isAI(True)
                    current_screen = "GAME"

    elif current_screen == "GAME":
        gameboard.draw()
        winner = gameboard.check_winner()
        if winner is not None:
            gameboard.winner(screen, winner)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if gameboard.home_button.checkMouseInput(pygame.mouse.get_pos()):
                        current_screen = "HOME"
                        gameboard.reset()
                    elif gameboard.quit_button.checkMouseInput(pygame.mouse.get_pos()):
                        run = False
        
        # if gameboard.turn == RED:
        #     if gameboard.ai:
        #             # self.bestMove()
        #             _, best_board = gameboard.minimax(gameboard.board, 0, True)
        #             print("best_board ", best_board)
        #             gameboard.board = best_board
        #             for row in range(RC):
        #                 for col in range(RC):
        #                     if len(gameboard.board[row][col]) != 0:
        #                         gameboard.board[row][col][-1].row = row
        #                         gameboard.board[row][col][-1].col = col
        #     gameboard.switch_turn()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameboard.update(pygame.mouse.get_pos())

    pygame.display.update()
            
pygame.quit()

    
    
        