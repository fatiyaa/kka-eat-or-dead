import pygame
from button import Button
from cons import *

class Home:
    def __init__(self, screen):
        self.screen = screen
        self.start_button = None
        self.exit_button = None

    def draw(self):
        self.draw_title()
        self.draw_logo()
        self.draw_button(self.screen)
        

    def draw_title(self):
        font = pygame.font.SysFont(None, 100)

        eat_text = font.render("Eat", True, RED)
        eat_width = eat_text.get_width()

        or_text = font.render(" or ", True, (0, 0, 0))
        or_width = or_text.get_width()

        dead_text = font.render("Dead", True, BLUE)
        dead_width = dead_text.get_width()

        total_width = eat_width + or_width + dead_width

        x_title = (SCREEN_WIDTH - total_width) // 2
        y_title = 150

        self.screen.blit(eat_text, (x_title, y_title))
        self.screen.blit(or_text, (x_title + eat_width, y_title))
        self.screen.blit(dead_text, (x_title + eat_width + or_width, y_title))
        
        

    def draw_logo(self):
        logo = pygame.image.load("assets\Icon.png")
        logo_size = 300
        
        scaled_logo = pygame.transform.scale(logo, (logo_size, logo_size))

        x_logo = (SCREEN_WIDTH - logo_size) // 2
        y_logo = (SCREEN_HEIGHT - logo_size) // 2

        self.screen.blit(scaled_logo, (x_logo, y_logo))

    def draw_button(self,screen):
        font = pygame.font.SysFont(None, 50)
        x_button = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
        y_button = SCREEN_HEIGHT - 150
        self.start_button = Button(x_button, y_button-70, 'Start', font, (0, 0, 0), BLUE, LIGHT_BLUE)
        self.exit_button  = Button(x_button, y_button, 'Exit', font, (0, 0, 0), RED, LIGHT_RED)

        for button in [self.start_button, self.exit_button]:
            button.hoverColor(pygame.mouse.get_pos())
            button.update(screen)