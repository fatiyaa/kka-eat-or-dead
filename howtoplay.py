import pygame
from button import Button
from cons import *

class HowToPlay:
    def __init__(self, screen):
        self.screen = screen
        self.friends_button = None
        self.computer_button = None
        self.load_text_from_file()

    def load_text_from_file(self):
        with open('howtoplay.txt', 'r') as file:
            self.text_content = file.read().splitlines()

    def draw(self):
        self.draw_text()
        self.draw_button(self.screen)

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
