import pygame

from cons import *

class Pawn:
    # inisialisasi
    def __init__(self, value, color, x, y):
        self.x = x
        self.y = y
        self.row = -1
        self.col = -1
        self.value = value
        self.color = color
        self.selected = False
        self.image = pygame.image.load( f"assets/{'r' if self.color == RED else 'b'}{self.value}.png")
        self.original_image = self.image
        self.enlarged_image = pygame.transform.smoothscale(self.original_image, (1.2 * PAWN_RAD, 1.2 * PAWN_RAD))
        self.enlarged_size = PAWN_RAD
        self.enlarged_speed = 5  # zooming speed
    
    # mengecek apakah pawn ditekan
    def is_collide(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= self.enlarged_size ** 2
    
    # menyimpan koordinat pawn terhadap board
    def set_position(self, x, y):
        self.x, self.y = x, y
    
    # menyimpan posisi pawn terhadap layar
    def set_board_position(self, x, y):
        self.row, self.col = x, y
    
    # menandai pawn sedang dipilih/ditekan
    def select(self):
        self.selected = True
    
    # menandai pawn sudah dilepas
    def unselect(self):
        self.selected = False
    
    # menggambar pawn
    def draw(self, screen: pygame.Surface):
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


    # merubah output menjadi self dan value apabila variabel pawn dicetak
    def __repr__(self) -> str:
        if(self.color == RED):
            name = "red "+ str(self.value)
        else:
            name = "blue "+ str(self.value)
        return name