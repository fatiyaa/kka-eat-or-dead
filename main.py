import pygame

from cons import *
from home import Home
from board import Board
from howtoplay import HowToPlay

# element dan inisiasi pygame dan screen base
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load(path_icon)
pygame.display.set_caption('Eat or Death')
pygame.display.set_icon(icon)

# variabel dan object yang digunakan 
run = True
clock = pygame.time.Clock()
home = Home(screen)
gameboard = Board(screen)
howtoplay = HowToPlay(screen)
current_screen = "HOME"

# run the game app
while run:
    clock.tick(60)
    screen.fill(BG)

    # menampilkan layar home 
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

    # menampilkan layar how to play
    elif current_screen == "HOWTOPLAY":
        howtoplay.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if howtoplay.friends_button.checkMouseInput(pygame.mouse.get_pos()): #bermain tanpa AI
                    current_screen = "GAME"
                elif howtoplay.computer_button.checkMouseInput(pygame.mouse.get_pos()): #bermain dengan AI
                    gameboard.isAI(True) 
                    howtoplay.active_choose_screen = True
                elif howtoplay.active_choose_screen: #memilih algoritma AI yang digunakan
                    if howtoplay.minimax_button.checkMouseInput(pygame.mouse.get_pos()):
                        gameboard.algorithm = "MINIMAX"
                        current_screen = "GAME"
                    if howtoplay.alpaBeta_button.checkMouseInput(pygame.mouse.get_pos()):
                        gameboard.algorithm = "ALPHA-BETA"
                        current_screen = "GAME"

    # menampilkan layar game
    elif current_screen == "GAME":
        gameboard.draw()
        winner = gameboard.check_winner_board()
        if winner is not None: #game akan berjalan selama belum didapatkan pemenang
            gameboard.winner(screen, winner)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if gameboard.home_button.checkMouseInput(pygame.mouse.get_pos()):
                        current_screen = "HOME"
                        gameboard.reset() #reset halaman game
                        howtoplay.active_choose_screen = False 
                    elif gameboard.quit_button.checkMouseInput(pygame.mouse.get_pos()):
                        run = False
                        
        # menerima respon input dari mouse terhadap pawn dan board
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameboard.update(pygame.mouse.get_pos())
    
    # update pygame display sesuai clock tick
    pygame.display.update()
            
pygame.quit()

    