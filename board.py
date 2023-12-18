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
        self.pawns_blue = []
        self.pawns_red = []
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
        self.pawns_blue = []
        self.pawns_red = []
        self.add_pawn()              
        self.selected_pawn: Pawn = None
        self.possible_moves = []
        self.turn = BLUE
        
    def isAI(self, ai):
        self.ai = ai
        
    def draw(self):
        self.draw_board()
        self.draw_possible_moves()
        self.draw_board_border()
        self.draw_pawn()
        self.draw_turn()

    def add_pawn(self):
        for i in range(75, SCREEN_WIDTH-75, 90):
            self.pawns_red.append(Pawn((i-75)//90 + 1, RED, i+45, 85))
            self.pawns_blue.append(Pawn((i-75)//90 + 1, BLUE, i+45, SCREEN_HEIGHT-90))

    def draw_pawn(self):

        for pawn in self.pawns_blue:
            pawn.draw(self.screen)
            
        for pawn in self.pawns_red:
            pawn.draw(self.screen)
            
        for row in self.board:
            for cell in row:
                if cell == []:
                    continue
                cell[-1].draw(self.screen)

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
        if self.turn == BLUE or self.ai == False:
            self.click_board(pos)
            self.click_pawn(pos)
            if self.selected_pawn:
                color, value = self.selected_pawn.color, self.selected_pawn.value
                self.possible_moves = self.find_possible_moves(self.board, color, value)
            else:
                self.possible_moves = []
        
            
    def click_pawn(self, pos):
        (x, y) = pos
        selecting = False
        
        pawn_list = []
        
        if self.turn == BLUE:
            pawn_list.extend(self.pawns_blue)
        else:
            pawn_list.extend(self.pawns_red)
            
        for row in self.board:
            for cell in row:
                if cell == []:
                    continue
                if cell[-1].color == self.turn:
                    pawn_list.append(cell[-1])
            
        for pawn in pawn_list:
            if pawn.color != self.turn:
                continue
            
            # if pawn.row != -1 and pawn.col != -1 and self.board[pawn.row][pawn.col][-1] != pawn:
            #     continue
            
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
                
                if self.selected_pawn in self.pawns_blue:
                    self.pawns_blue.remove(self.selected_pawn)
                elif self.selected_pawn in self.pawns_red: 
                    self.pawns_red.remove(self.selected_pawn)
                    
                self.selected_pawn.set_board_position(row, col)
                self.selected_pawn.set_position(board_x + SQUARE//2, board_y + SQUARE//2)
                self.selected_pawn.unselect()
                self.possible_moves = []
                self.selected_pawn = None
                self.switch_turn()
                return
                    
        
    def find_possible_moves(self, board, color, value):
        possible_moves = []
        for row in range(RC):
            for col in range(RC):
                if board[row][col] != [] and board[row][col][-1].color == color:
                    continue
                if board[row][col] == [] or board[row][col][-1].value < value:
                    possible_moves.append((row, col))
                    
        return possible_moves
    
    def get_possible_boards(self, board, pawns_blue: list[Pawn], pawns_red: list[Pawn], color):
        possible_boards = []
        pawns = []
       
        if color == RED:
            pawns.extend(pawns_red)
        else : pawns.extend(pawns_blue)
        
        for row in board:
            for cell in row:
                if cell == []:
                    continue
                if cell[-1].color == color:
                    pawns.append(cell[-1])
        
        for pawn in pawns:
            possible_moves = self.find_possible_moves(board, pawn.color, pawn.value)
            
            for move in possible_moves:
                (row, col) = move
                temp_board = [
                    [[], [], []],
                    [[], [], []],
                    [[], [], []]
                ]
                
                for r in range(RC):
                    for c in range(RC):
                        temp_board[r][c].extend(board[r][c])
                # print("temp_board ", temp_board[0], temp_board[1], temp_board[2], sep='\n')
                
                # exit()
                
                reds = []
                blues = []
                reds.extend(pawns_red)
                blues.extend(pawns_blue)
                
                if pawn in blues:
                    blues.remove(pawn)
                elif pawn in reds:
                    reds.remove(pawn)
                else:
                    temp_board[pawn.row][pawn.col].pop()
                    
                pawn: Pawn
                new_pawn = Pawn(pawn.value, pawn.color, pawn.x, pawn.y)
                
                board_x = (75 + col * SQUARE)
                board_y = (175 + row * SQUARE)
                
                new_pawn.set_board_position(row, col)
                new_pawn.set_position(board_x + SQUARE//2, board_y + SQUARE//2)
                
                temp_board[row][col].append(new_pawn)
                possible_boards.append((temp_board, blues, reds))
                
        return possible_boards
                    
    def draw_possible_moves(self):
        if self.possible_moves == []:
            return
        
        for move in self.possible_moves:
            (row, col) = move
            pygame.draw.rect(self.screen, GREEN, (col*SQUARE +75, row*SQUARE+175, SQUARE, SQUARE))
            
    def switch_turn(self):
        if self.turn == BLUE:
            # print("board_before ", self.board[0], self.board[1], self.board[2], sep='\n')
            # print("winner ", self.check_winner(self.board, log=True))
            self.turn = RED
            if self.ai:
                # self.bestMove()
                evaluation, best_board, pawns_blue, pawns_red = self.minimax(self.board, self.pawns_blue, self.pawns_red, 3)
                # print("evaluation ", evaluation)
                # print("best_board ", best_board[0], best_board[1], best_board[2], sep='\n')
                # print("pawns_blue ", pawns_blue)
                # print("pawns_red ", pawns_red)
                if evaluation > -1:
                    self.board = best_board
                    self.pawns_blue = pawns_blue
                    self.pawns_red = pawns_red
                # for row in range(RC):
                #     for col in range(RC):
                #         if len(self.board[row][col]) != 0:
                #             # print("TIPE= ",self.board[row][col][-1].row, self.board[row][col][-1].col)
                #             if self.board[row][col][-1] in self.pawns_red:
                #                 self.pawns_red.remove(self.board[row][col][-1])
                #             self.board[row][col][-1].row = row
                #             self.board[row][col][-1].col = col
                #             self.board[row][col][-1].x = 75 + col * SQUARE + SQUARE//2
                #             self.board[row][col][-1].y = 175 + row * SQUARE + SQUARE//2
                            
                            # print("HABIS= ",self.board[row][col][-1].row, self.board[row][col][-1].col)
                            # self.board[row][col][-1](row, col)
                            # self.board[row][col][-1](75 + col * SQUARE + SQUARE//2, 175 + row * SQUARE + SQUARE//2)
                self.turn = BLUE
                
                
        else:
            self.turn = BLUE
        # pawns = []
        # if self.turn == BLUE:
        #     pawns.extend(self.pawns_red)
        #     self.turn = RED
        # else:
        #     pawns.extend(self.pawns_blue)
        #     self.turn = BLUE
            
        # for row in self.board:
        #     for cell in row:
        #         if cell == []:
        #             continue
        #         if cell[-1].color == self.turn:
        #             pawns.append(cell[-1])
                
        # print(self.get_possible_boards(self.board, pawns))

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
    
    def check_winner_board(self):
        return self.check_winner(self.board)
    
    def check_winner(self, board, log=False):
        col = 0
        row = 0
        winner = None
        # print("board_check ", board[0], board[1], board[2], sep='\n') if log else None

        
        for a in range(RC):
            if self.pawn_existed(board[a][col],board[a][col+1], board[a][col+2]) :
                if self.pawn_in_row(board[a][col][-1].color, board[a][col+1][-1].color, board[a][col+2][-1].color):
                    if winner == None or winner == board[a][col][-1].color:
                        winner = board[a][col][-1].color
                    else:
                        return GREEN
                    
        for b in range(RC):
            if self.pawn_existed(board[row][b], board[row+1][b], board[row+2][b]) :
                if self.pawn_in_row(board[row][b][-1].color, board[row+1][b][-1].color, board[row+2][b][-1].color):
                    if winner == None or winner == board[row][b][-1].color:
                        winner = board[row][b][-1].color
                    else:
                        return GREEN
                
        if self.pawn_existed(board[row][col], board[row+1][col+1], board[row+2][col+2]) :
                if self.pawn_in_row(board[row][col][-1].color, board[row+1][col+1][-1].color, board[row+2][col+2][-1].color):
                    if winner == None or winner == board[row][col][-1].color:
                        winner = board[row][col][-1].color
                    else:
                        return GREEN
        if self.pawn_existed(board[row][col+2], board[row+1][col+1], board[row+2][col]) :
                if self.pawn_in_row(board[row][col+2][-1].color, board[row+1][col+1][-1].color, board[row+2][col][-1].color):
                    if winner == None or winner == board[row][col+2][-1].color:
                            winner = board[row][col+2][-1].color
                    else:
                        return GREEN
        
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
    
    # def evaluate(self, board, is_max):
    #     pawns_red = []
    #     pawns_blue = []

    #     for row in board:
    #         for cell in row:
    #             if cell == []:
    #                 continue
    #             if cell[-1].color == BLUE:
    #                 pawns_blue.append(cell[-1])
    #             if cell[-1].color == RED:
    #                 pawns_red.append(cell[-1])
        
    #     # print ("red ", len(pawns_red), " blue ", pawns_blue)
        
    #     if is_max:    
    #         return len(pawns_red)/(len(pawns_red)+len(pawns_blue))
    #     else:
    #         return - (len(pawns_blue)/(len(pawns_red)+len(pawns_blue)))
     
    def minimax(self, board, pawns_blue: list[Pawn], pawns_red: list[Pawn], depth, is_max: bool = True):
        winner = self.check_winner(board)
            
        
        if  winner != None or depth == 1:
            if winner is RED:
                return [1, board, pawns_blue, pawns_red]
            elif winner is BLUE:
                return [-1, board, pawns_blue, pawns_red]
            else:
                return [0, board, pawns_blue, pawns_red]
            
        if is_max:
            max_eval = float('-inf')
            best_move = None
            best_pawns_red = pawns_red
            
            for move, _, reds in self.get_possible_boards(board, pawns_blue, best_pawns_red, RED):
                evaluation = self.minimax(move, pawns_blue, best_pawns_red, depth-1, False)[0]
                max_eval = max(evaluation, max_eval)
                if evaluation == max_eval:
                    best_move = move
                    best_pawns_red  = reds
        
            return [max_eval, best_move, pawns_blue, best_pawns_red]
        
        else :
            min_eval = float('inf')
            best_move = None
            best_pawns_blue = pawns_blue
            
            for move, blues, _ in self.get_possible_boards(board, best_pawns_blue, pawns_red, BLUE):
                evaluation = self.minimax(move, best_pawns_blue, pawns_red, depth-1, True)[0]
                min_eval = min(evaluation, min_eval)
                if evaluation == min_eval:
                    best_move = move
                    best_pawns_blue  = blues
        
            return [min_eval, best_move, best_pawns_blue, pawns_red]