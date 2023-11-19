import pygame

from cons import *


class Pawn:
    def __init__(self, val, color, x, y):
        self.x = x
        self.y = y
        self.row = -1
        self.col = -1
        self.value = val
        self.color = color
        self.font = pygame.font.SysFont(None, 30)
        self.selected = False
        
    # def update(self, row, col):
    #     self.x = 175+(row-1)*150+75
    #     self.y = 75+(col-1)*150+75
    
    def is_collide(self, x, y):
        return (self.x-x)**2 + (self.y-y)**2 <= PAWN_RAD**2
        
    def set_position(self, x, y):
        [self.x, self.y] = [x, y]
        
    def set_board_position(self, x, y):
        [self.row, self.col] = [x, y]
        
    def select(self):
        self.selected = True
        
    def unselect(self):
        self.selected = False
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x,  self.y), PAWN_RAD - (5-self.value)*2)
        text = self.font.render(str(self.value), True, WHITE)
        screen.blit(text, text.get_rect(center=(self.x, self.y)))
        
        if self.selected:
            pygame.draw.circle(screen, BLACK, (self.x, self.y), PAWN_RAD - (5-self.value)*2, 5)
        # screen.blit(self.icon(self.x - self.icon.get_width()//2, self.y - self.icon.get_height()//2))
        