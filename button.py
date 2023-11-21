import pygame

class Button:
    def __init__(self, x, y, text, font, text_color, base_color, hover_color):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.text_color = text_color
        self.base_color = base_color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, 200, 50)
        self.is_hovered = False

    def hoverColor(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def update(self, screen):
        padding = 5
        padded_rect = self.rect.inflate(-2 * padding, 0)

        pygame.draw.rect(screen, self.hover_color if self.is_hovered else self.base_color, padded_rect)
        pygame.draw.rect(screen, (0, 0, 0), padded_rect, 3) 
        
        font_size = 30
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def checkMouseInput(self):
        return self.is_hovered and pygame.mouse.get_pressed()[0] == 1
