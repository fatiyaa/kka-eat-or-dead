import pygame
from button import Button
from cons import *

class HowToPlay:
    def __init__(self, screen):
        self.screen = screen
        self.friends_button = None
        self.computer_button = None
        self.load_text_from_file()
        self.active_choose_screen = False

    def load_text_from_file(self):
        with open('howtoplay.txt', 'r') as file:
            self.text_content = file.read().splitlines()

    def draw(self):
        self.draw_text()
        self.draw_button(self.screen)
        if self.active_choose_screen:
            self.draw_choose_screen(self.screen)

    def draw_text(self):
        font = pygame.font.SysFont(None, 25)
        text_x = 25
        text_y = 50
        gap = font.get_height()

        for line in self.text_content:
            text_surface = font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (text_x, text_y))
            text_y += gap 

    def draw_button(self, screen):
        font = pygame.font.SysFont(None, 50)
        x_button = SCREEN_WIDTH // 2
        y_button = SCREEN_HEIGHT - 120
        self.friends_button = Button(100, y_button, 'Friends', font, (0, 0, 0), BLUE, LIGHT_BLUE)
        self.computer_button = Button(x_button, y_button, 'Computer', font, (0, 0, 0), RED, LIGHT_RED)

        for button in [self.friends_button, self.computer_button]:
            button.hoverColor(pygame.mouse.get_pos())
            button.update(screen)
           
    def draw_choose_screen(self, screen):
        pygame.draw.rect(screen, BG, (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3))
        pygame.draw.rect(screen, (0, 0, 0), (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3), 4)
        font = pygame.font.SysFont(None, 80)
        text = font.render("ALGORITHMS", True, BLACK)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))

        font = pygame.font.SysFont(None, 50)
        self.minimax_button = Button(100, SCREEN_HEIGHT//2+40, 'MINIMAX', font, (0, 0, 0), BLUE, LIGHT_BLUE)
        self.alpaBeta_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+40, 'ALPA BETA', font, (0, 0, 0), RED, LIGHT_RED)

        for button in [self.minimax_button, self.alpaBeta_button]:
            button.hoverColor(pygame.mouse.get_pos())
            button.update(screen)

        
        