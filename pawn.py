import pygame
from cons import *
import pickle

class Pawn:
    def __init__(self, val, color, x, y, image_path):
        self.x = x
        self.y = y
        self.row = -1
        self.col = -1
        self.value = val
        self.color = color
        # self.font = pygame.font.SysFont(None, 30)
        self.selected = False
        self.image = pygame.image.load(image_path)
        self.original_image = self.image
        self.enlarged_image = pygame.transform.scale(self.original_image, (1.2 * PAWN_RAD, 1.2 * PAWN_RAD))
        self.enlarged_size = PAWN_RAD
        self.enlarged_speed = 5  # You can adjust this value for the zooming speed
    
    def is_collide(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= self.enlarged_size ** 2
    
    def set_position(self, x, y):
        self.x, self.y = x, y
    
    def set_board_position(self, x, y):
        self.row, self.col = x, y
    
    def select(self):
        self.selected = True
    
    def unselect(self):
        self.selected = False
    
    def draw(self, screen):
        if self.selected:
            # Smoothly zoom in when selected
            if self.enlarged_size < 1.2 * PAWN_RAD:
                self.enlarged_size += self.enlarged_speed
        else:
            # Smoothly zoom out when unselected
            if self.enlarged_size > PAWN_RAD:
                self.enlarged_size -= self.enlarged_speed

        # Use a smoother interpolation for scaling
        self.enlarged_image = pygame.transform.smoothscale(self.original_image, (int(2 * self.enlarged_size), int(2 * self.enlarged_size)))

        screen.blit(self.enlarged_image, (self.x - self.enlarged_size, self.y - self.enlarged_size))
        #text = self.font.render(str(self.value), True, WHITE)
        #screen.blit(text, text.get_rect(center=(self.x, self.y)))

    def __repr__(self) -> str:
        if(self.color == RED):
            name = "red "+ str(self.value)
        else:
            name = "blue "+ str(self.value)
        return name
    
    # def deepcopy(self):
    #     # Pickle and unpickle the pysurface object to create an independent copy
    #     pickled_pysurface = pickle.dumps(self.screen)
    #     copied_pysurface = pickle.loads(pickled_pysurface)

    #     # Create a new Pawn instance with the copied pysurface object
    #     return Pawn(copied_pysurface)