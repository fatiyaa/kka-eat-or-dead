import pygame
from cons import *
from pawn import Pawn
from button import Button


class Board:
    
    def __init__(self, screen):
        self.screen = screen
        self.board = [
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ]
        self.pawns = []
        self.add_pawn()          
        self.selected_pawn: Pawn = None
        self.possible_moves = []
        self.turn = BLUE
        
    def reset(self):
        self.board = [
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ]
        self.pawns = []
        self.add_pawn()              
        self.selected_pawn: Pawn = None
        self.possible_moves = []
        self.turn = BLUE
        
    def draw(self):
        self.draw_board()
        self.draw_possible_moves()
        self.draw_board_border()
        self.draw_pawn()
        self.draw_turn()

    def add_pawn(self):
        for i in range(75, SCREEN_WIDTH-75, 90):
            self.pawns.append(Pawn((i-75)//90 + 1, RED, i+45, 85, f"assets/r{(i // 90) % 5 + 1}.png"))
            self.pawns.append(Pawn((i-75)//90 + 1, BLUE, i+45, SCREEN_HEIGHT-90, f"assets/b{(i // 90) % 5 + 1}.png"))

    def draw_pawn(self):
        for pawn in self.pawns:
            if pawn.row != -1 and pawn.col != -1 and self.board[pawn.row][pawn.col] != [] and self.board[pawn.row][pawn.col][-1] != pawn:
                continue
            pawn.draw(self.screen)

    def draw_board(self):
        for row in range(RC):
            for col in range(RC):
                if (row+col)%2:
                    pygame.draw.rect(self.screen, BLACK, (col*SQUARE +75, row*SQUARE+175, SQUARE, SQUARE))
                else:
                    pygame.draw.rect(self.screen, WHITE, (col*SQUARE +75, row*SQUARE+175, SQUARE, SQUARE))
        
    def draw_board_border(self):
        for row in range(RC):
            for col in range(RC):
                pygame.draw.rect(self.screen, RED, (col*SQUARE +75-4, row*SQUARE+175-4, SQUARE+4, SQUARE+4), 4)
         
    def update(self, pos):
        self.click_board(pos)
        self.click_pawn(pos)
        self.find_possible_moves()
        print(self.board)
            
    def click_pawn(self, pos):
        (x, y) = pos
        selecting = False
        for pawn in self.pawns:
            if pawn.color != self.turn:
                continue
            
            if pawn.row != -1 and pawn.col != -1 and self.board[pawn.row][pawn.col][-1] != pawn:
                continue
            
            if not pawn.is_collide(x, y):
                continue
            
            if self.selected_pawn:
                self.selected_pawn.unselect()
            
            self.selected_pawn = pawn
            self.selected_pawn.select()
            selecting = True
            
        if not selecting and self.selected_pawn:
            self.selected_pawn.unselect()
            self.selected_pawn = None
            
    def click_board(self, pos):
        if not self.selected_pawn:
            return
        (x, y) = pos
        for move in self.possible_moves:
            (row, col) = move
            board_x = (75 + col * SQUARE)
            board_y = (175 + row * SQUARE)
            dx = x - board_x
            dy = y - board_y
            
            if (dx >= 0 and dx <= SQUARE) and (dy >= 0 and dy <= SQUARE):
                if self.selected_pawn.row != -1 and self.selected_pawn.col != -1:
                    self.board[self.selected_pawn.row][self.selected_pawn.col].pop()
                self.board[row][col].append(self.selected_pawn)
                self.selected_pawn.set_board_position(row, col)
                self.selected_pawn.set_position(board_x + SQUARE//2, board_y + SQUARE//2)
                self.selected_pawn.unselect()
                self.possible_moves = []
                self.selected_pawn = None
                self.switch_turn()
                return
                    
        
    def find_possible_moves(self):
        if not self.selected_pawn:
            self.possible_moves = []
            return
        
        self.possible_moves = []
        for row in range(RC):
            for col in range(RC):
                if self.board[row][col] != [] and self.board[row][col][-1].color == self.turn:
                    continue
                if self.board[row][col] == [] or self.board[row][col][-1].value < self.selected_pawn.value:
                    self.possible_moves.append((row, col))
                    
    def draw_possible_moves(self):
        if self.possible_moves == []:
            return
        
        for move in self.possible_moves:
            (row, col) = move
            pygame.draw.rect(self.screen, GREEN, (col*SQUARE +75, row*SQUARE+175, SQUARE, SQUARE))
            
    def switch_turn(self):
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

    def draw_turn(self):
        if self.selected_pawn is not None:
            return 
        font_size = 80
        font = pygame.font.SysFont(None, font_size)
        text_stroke = pygame.font.SysFont(None, font_size+1)

        text = font.render("BLUE's Turn" if self.turn == BLUE else "RED's Turn", True, self.turn)
        text_stroke_surface = text_stroke.render("BLUE's Turn" if self.turn == BLUE else "RED's Turn", True, BLACK)

        text_rect= text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        text_stroke_rect  = text_rect.copy()

        self.screen.blit(text_stroke_surface, text_stroke_rect.move(3, 3))
        self.screen.blit(text_stroke_surface, text_stroke_rect.move(-3, -3))
        self.screen.blit(text_stroke_surface, text_stroke_rect.move(-3, 3)) 
        self.screen.blit(text_stroke_surface, text_stroke_rect.move(3, -3))
        self.screen.blit(text, text_rect)

        
    def pawn_existed(self, a, b, c):
        if a != [] and b != [] and c != []:
            return True
        return False
    
    def pawn_in_row(self, a, b, c):
        if a==b and b==c:
            return True
        return False
    
    def check_winner(self):
        col = 0
        row = 0
        winner = None
        
        for a in range(RC):
            if self.pawn_existed(self.board[a][col],self.board[a][col+1], self.board[a][col+2]) :
                if self.pawn_in_row(self.board[a][col][-1].color, self.board[a][col+1][-1].color, self.board[a][col+2][-1].color):
                    if winner == None or winner == self.board[a][col][-1].color:
                        winner = self.board[a][col][-1].color
                    else:
                        return GREEN
                    
        for b in range(RC):
            if self.pawn_existed(self.board[row][b], self.board[row+1][b], self.board[row+2][b]) :
                if self.pawn_in_row(self.board[row][b][-1].color, self.board[row+1][b][-1].color, self.board[row+2][b][-1].color):
                    if winner == None or winner == self.board[row][b][-1].color:
                        winner = self.board[row][b][-1].color
                    else:
                        return GREEN
                
        if self.pawn_existed(self.board[row][col], self.board[row+1][col+1], self.board[row+2][col+2]) :
                if self.pawn_in_row(self.board[row][col][-1].color, self.board[row+1][col+1][-1].color, self.board[row+2][col+2][-1].color):
                    if winner == None or winner == self.board[row][col][-1].color:
                        winner = self.board[row][col][-1].color
                    else:
                        return GREEN
        elif self.pawn_existed(self.board[row][col+2], self.board[row+1][col+1], self.board[row+2][col]) :
                if self.pawn_in_row(self.board[row][col+2][-1].color, self.board[row+1][col+1][-1].color, self.board[row+2][col][-1].color):
                    if winner == None or winner == self.board[row][col+2][-1].color:
                            winner = self.board[row][col+2][-1].color
                    else:
                        return GREEN
        
        # for a in range(RC):
        #     if self.board[a][col] != [] and self.board[a][col+1] != [] and self.board[a][col+2] != [] :
        #         if self.board[a][col][-1].color == self.board[a][col+1][-1].color and self.board[a][col+1][-1].color == self.board[a][col+2][-1].color:
        #             if winner == None or winner == self.board[a][col][-1].color:
        #                 winner = self.board[a][col][-1].color
        #             else:
        #                 return GREEN
                    
        # for b in range(RC):
        #     if self.board[row][b] != [] and self.board[row+1][b] != [] and self.board[row+2][b] != [] :
        #         if self.board[row][b][-1].color == self.board[row+1][b][-1].color and self.board[row+1][b][-1].color == self.board[row+2][b][-1].color:
        #             if winner == None or winner == self.board[row][b][-1].color:
        #                 winner = self.board[row][b][-1].color
        #             else:
        #                 return GREEN
                
        # if self.board[row][col] != [] and self.board[row+1][col+1] != [] and self.board[row+2][col+2] != [] :
        #         if self.board[row][col][-1].color == self.board[row+1][col+1][-1].color and self.board[row+1][col+1][-1].color == self.board[row+2][col+2][-1].color:
        #             if winner == None or winner == self.board[row][col][-1].color:
        #                 winner = self.board[row][col][-1].color
        #             else:
        #                 return GREEN
        # elif self.board[row][col+2] != [] and self.board[row+1][col+1] != [] and self.board[row+2][col] != [] :
        #         if self.board[row][col+2][-1].color == self.board[row+1][col+1][-1].color and self.board[row+1][col+1][-1].color == self.board[row+2][col][-1].color:
        #             if winner == None or winner == self.board[row][col+2][-1].color:
        #                     winner = self.board[row][col+2][-1].color
        #             else:
        #                 return GREEN
        
        return winner
    
    def winner(self, screen, win):
        pygame.draw.rect(screen, BG, (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3))
        pygame.draw.rect(screen, (0, 0, 0), (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3), 4)
        font = pygame.font.SysFont(None, 100)
        text = font.render("IT'S A TIE", True, ORANGE)
        if win == RED:
            text = font.render('RED IS WIN', True, RED)
        if win == BLUE:
            text = font.render('BLUE IS WIN', True, BLUE)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))

        font = pygame.font.SysFont(None, 50)
        self.home_button = Button(100, SCREEN_HEIGHT//2+40, 'Home', font, (0, 0, 0), BLUE, LIGHT_BLUE)
        self.quit_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+40, 'Quit Game', font, (0, 0, 0), RED, LIGHT_RED)

        for button in [self.home_button, self.quit_button]:
            button.hoverColor(pygame.mouse.get_pos())
            button.update(screen)