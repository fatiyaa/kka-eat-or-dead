import pygame
from board import Board
from cons import *
from button import Button
# from wkwk.cons import *
# from wkwk.board import Board


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load(path_icon)  # Replace with the actual path to your icon image
pygame.display.set_caption('Eat or Death')
pygame.display.set_icon(icon)


run = True
clock = pygame.time.Clock()
gameboard = Board(screen)

while run:
    clock.tick(60)
    screen.fill(BG)
    gameboard.draw()
    winner = gameboard.check_winner()
    if winner is not None:
        gameboard.winner(screen, winner)
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            gameboard.update(pygame.mouse.get_pos())
            
    pygame.display.update()
            
pygame.quit()

    
    
        