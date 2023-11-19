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
        for i in range(75, SCREEN_WIDTH-75, 90):
            self.pawns.append(Pawn((i-75)//90 + 1, RED, i+45, 85))
            self.pawns.append(Pawn((i-75)//90 + 1, BLUE, i+45, SCREEN_HEIGHT-90))
        
            
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
        for i in range(75, SCREEN_WIDTH-75, 90):
            self.pawns.append(Pawn((i-75)//90 + 1, RED, i+45, 85))
            self.pawns.append(Pawn((i-75)//90 + 1, BLUE, i+45, SCREEN_HEIGHT-90))
        
            
        self.selected_pawn: Pawn = None
        self.possible_moves = []
        
        self.turn = BLUE
        
    def draw(self):
        self.draw_board()
        self.draw_possible_moves()
        self.draw_board_border()
        for pawn in self.pawns:
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
        # print(self.board)
            
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
        
    def check_winner(self):
        col = 0
        row = 0
        winner = None
        for a in range(RC):
            if self.board[a][col] != [] and self.board[a][col+1] != [] and self.board[a][col+2] != [] :
                if self.board[a][col][-1].color == self.board[a][col+1][-1].color and self.board[a][col+1][-1].color == self.board[a][col+2][-1].color:
                    if winner == None or winner == self.board[a][col][-1].color:
                        winner = self.board[a][col][-1].color
                    else:
                        return GREEN
                    
        for b in range(RC):
            if self.board[row][b] != [] and self.board[row+1][b] != [] and self.board[row+2][b] != [] :
                if self.board[row][b][-1].color == self.board[row+1][b][-1].color and self.board[row+1][b][-1].color == self.board[row+2][b][-1].color:
                    if winner == None or winner == self.board[row][b][-1].color:
                        winner = self.board[row][b][-1].color
                    else:
                        return GREEN
                
        if self.board[row][col] != [] and self.board[row+1][col+1] != [] and self.board[row+2][col+2] != [] :
                if self.board[row][col][-1].color == self.board[row+1][col+1][-1].color and self.board[row+1][col+1][-1].color == self.board[row+2][col+2][-1].color:
                    if winner == None or winner == self.board[row][col][-1].color:
                        winner = self.board[row][col][-1].color
                    else:
                        return GREEN
        elif self.board[row][col+2] != [] and self.board[row+1][col+1] != [] and self.board[row+2][col] != [] :
                if self.board[row][col+2][-1].color == self.board[row+1][col+1][-1].color and self.board[row+1][col+1][-1].color == self.board[row+2][col][-1].color:
                    if winner == None or winner == self.board[row][col+2][-1].color:
                            winner = self.board[row][col+2][-1].color
                    else:
                        return GREEN
        
        return winner
    
    def winner(self, screen, win):
        pygame.draw.rect(screen, BG, (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3))
        pygame.draw.rect(screen, BLACK, (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3), 4)
        font = pygame.font.SysFont(None, 100)
        text = font.render("IT'S A TIE", True, ORANGE);
        if win == RED:
            text = font.render('RED IS WIN', True, RED);
        if win == BLUE:
            text = font.render('BLUE IS WIN', True, BLUE);
        screen.blit(text, text.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 -20)))
        
        font = pygame.font.SysFont(None, 50)
        play_again_button = Button(200, SCREEN_HEIGHT//2+40, 'Play Again', font, BLACK, BLUE)
        quit_button = Button(400, SCREEN_HEIGHT//2+40, 'Quit Game', font, BLACK, RED )
        
        for button in [play_again_button, quit_button]:
            button.hoverColor(pygame.mouse.get_pos())
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.checkMouseInput(pygame.mouse.get_pos()):
                    self.reset()
                if quit_button.checkMouseInput(pygame.mouse.get_pos()):
                    pygame.quit()
                
        
        
            
            
            
    
    # def create_board(self, screen):
    #     pygame.display.set_caption('Eat or Death', 'None')
    #     screen.fill((255,255,204))
    #     for row in range(RC):
    #         for col in range(RC):
    #             if (row+col)%2:
    #                 pygame.draw.rect(screen, BLACK, (col*SQUARE +75, row*SQUARE+175, SQUARE, SQUARE))
    #             else:
    #                 pygame.draw.rect(screen, WHITE, (col*SQUARE +75, row*SQUARE+175, SQUARE, SQUARE))
            
        
    # def create_pawn(self, screen):
        
        # pawn_w = [pygame.image.load('1w.png'), pygame.image.load('2w.png'), pygame.image.load('3w.png'), pygame.image.load('4w.png'), pygame.image.load('5w.png')]
        # pawn_b = [pygame.image.load('1b.png'), pygame.image.load('2b.png'), pygame.image.load('3b.png'), pygame.image.load('4b.png'), pygame.image.load('5b.png')]
        
        # for i in range(5):
        #     add = pawn_w[i].get_height()
        #     hg = 0
        #     if  add > 100:
        #         hg = add - 155
        #     screen.blit(pawn_w[i],(75+i*90, 15-hg))
        #     add = pawn_b[i].get_height()
        #     hg = 0
        #     if  add > 100:
        #         hg = add - 155
        #     screen.blit(pawn_b[i],(75+i*90, 645-hg))
            
    # def winner(self, letter):
    #     for r in range(RC):
    #         a = 0
    #         if (self.board[r][a].xo, self.board[r][a+1].xo, self.board[r][a+2].xo) == (letter, letter, letter):
    #             return True            
    #     for c in range(RC):
    #         b=0
    #         if (self.board[c][b].xo, self.board[c][b+1].xo, self.board[c][b+2].xo) == (letter, letter, letter):
    #             return True
            
    #     x=0
    #     y=0
    #     if (self.board[x][y].xo, self.board[x+1][y+1].xo, self.board[x+2][y+2].xo) == (letter, letter, letter):
    #         return True
    #     x=0
    #     y=2
    #     if (self.board[x][y].xo, self.board[x+1][y-1].xo, self.board[x+2][y-2].xo) == (letter, letter, letter):
    #         return True
        
    #     return False
        
                

    # def disp(self):
    #     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #     run = True
    #     while run:
            
    #         screen.fill((255,255,204))
    #         self.create_board(screen)
    #         self.create_pawn(screen)
            
            
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 run = False
            
    #         pygame.display.update()
                    
    #     pygame.quit()
        
# if __name__ == '__main__':
#     Board()
#     disp(screen)