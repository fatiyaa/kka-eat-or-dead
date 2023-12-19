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
                    current_screen = "GAME"
                elif howtoplay.computer_button.checkMouseInput(pygame.mouse.get_pos()):
                    gameboard.isAI(True)
                    howtoplay.active_choose_screen = True
                elif howtoplay.active_choose_screen:
                    if howtoplay.minimax_button.checkMouseInput(pygame.mouse.get_pos()):
                        gameboard.algorithm = "MINIMAX"
                        current_screen = "GAME"
                    if howtoplay.alpaBeta_button.checkMouseInput(pygame.mouse.get_pos()):
                        gameboard.algorithm = "ALPHA-BETA"
                        current_screen = "GAME"


    elif current_screen == "GAME":
        gameboard.draw()
        winner = gameboard.check_winner_board()
        if winner is not None:
            gameboard.winner(screen, winner)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if gameboard.home_button.checkMouseInput(pygame.mouse.get_pos()):
                        current_screen = "HOME"
                        gameboard.reset()
                        howtoplay.active_choose_screen = False
                    elif gameboard.quit_button.checkMouseInput(pygame.mouse.get_pos()):
                        run = False
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameboard.update(pygame.mouse.get_pos())

    pygame.display.update()
            
pygame.quit()

    