import pygame
from cons import *
from pawn import Pawn
from button import Button
import copy


class Board:
    
    def __init__(self, screen):
        self.screen = screen
        self.board = [
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ]
        self.pawns = []
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
        self.pawns = []
        self.pawns_red = []
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
        
    def isAI(self, ai):
        self.ai = ai

    def add_pawn(self):
        for i in range(75, SCREEN_WIDTH-75, 90):
            self.pawns_red.append(Pawn((i-75)//90 + 1, RED, i+45, 85, f"assets/r{(i // 90) % 5 + 1}.png"))
            self.pawns.append(Pawn((i-75)//90 + 1, BLUE, i+45, SCREEN_HEIGHT-90, f"assets/b{(i // 90) % 5 + 1}.png"))

    def draw_pawn(self):
        for pawn in self.pawns:
            if pawn.row != -1 and pawn.col != -1 and self.board[pawn.row][pawn.col] != [] and self.board[pawn.row][pawn.col][-1] != pawn:
                continue
            pawn.draw(self.screen)
        for pawn in self.pawns_red:
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
        if self.turn == BLUE or self.ai == False:
            self.click_board(pos)
            self.click_pawn(pos)
            self.find_possible_moves()
        print(self.board)
            
    def click_pawn(self, pos):
        (x, y) = pos
        selecting = False
        if self.turn == BLUE:
            pawn_list = self.pawns
        else:
            pawn_list = self.pawns_red
        for pawn in pawn_list:
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
                    
    def find_possible_moves2(self, pawn, board: list[list[list[Pawn]]]):
        possible_moves = []
        print(pawn)
        (color, value) = pawn
        for row in range(RC):
            for col in range(RC):
                if board[row][col] != [] and board[row][col][-1].color == color:
                    continue
                if board[row][col] == [] or board[row][col][-1].value < value:
                    possible_moves.append((row, col))
        return possible_moves
                    
    def draw_possible_moves(self):
        if self.possible_moves == []:
            return
        
        for move in self.possible_moves:
            (row, col) = move
            pygame.draw.rect(self.screen, GREEN, (col*SQUARE +75, row*SQUARE+175, SQUARE, SQUARE))
            
    def switch_turn(self):
        print(self.board)
        print(self.get_all_moves(self.get_board(), self.turn))
        if self.turn == BLUE:
            self.turn = RED
            if self.ai:
                # self.bestMove()
                _, best_board = self.minimax(self.board, 2)
                print("best_board ", best_board)
                self.board = best_board
                for row in range(RC):
                    for col in range(RC):
                        if len(self.board[row][col]) != 0:
                            # print("TIPE= ",self.board[row][col][-1].row, self.board[row][col][-1].col)
                            self.board[row][col][-1].row = row
                            self.board[row][col][-1].col = col
                            self.board[row][col][-1].x = 75 + col * SQUARE + SQUARE//2
                            self.board[row][col][-1].y = 175 + row * SQUARE + SQUARE//2
                            # print("HABIS= ",self.board[row][col][-1].row, self.board[row][col][-1].col)
                            # self.board[row][col][-1](row, col)
                            # self.board[row][col][-1](75 + col * SQUARE + SQUARE//2, 175 + row * SQUARE + SQUARE//2)
                self.turn = BLUE
                
        else:
            self.turn = BLUE
        print(self.turn)

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
    
    def check_winner2(self, board):
        col = 0
        row = 0
        winner = None
        
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
        elif self.pawn_existed(board[row][col+2], board[row+1][col+1], board[row+2][col]) :
                if self.pawn_in_row(board[row][col+2][-1].color, board[row+1][col+1][-1].color, board[row+2][col][-1].color):
                    if winner == None or winner == board[row][col+2][-1].color:
                            winner = self.board[row][col+2][-1].color
                    else:
                        return GREEN
        return winner
    
    def winner(self, screen, win):
        pygame.draw.rect(screen, BG, (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3))
        pygame.draw.rect(screen, (0, 0, 0), (20, SCREEN_HEIGHT//3, SCREEN_WIDTH-40, SCREEN_HEIGHT//3), 4)
        font = pygame.font.SysFont(None, 100)
        text = font.render("IT'S A TIE", True, ORANGE)
        if win == RED:
            text = font.render('RED WINS', True, RED)
        if win == BLUE:
            text = font.render('BLUE WINS', True, BLUE)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))

        font = pygame.font.SysFont(None, 50)
        self.home_button = Button(100, SCREEN_HEIGHT//2+40, 'Home', font, (0, 0, 0), BLUE, LIGHT_BLUE)
        self.quit_button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+40, 'Quit Game', font, (0, 0, 0), RED, LIGHT_RED)

        for button in [self.home_button, self.quit_button]:
            button.hoverColor(pygame.mouse.get_pos())
            button.update(screen)
            
    def get_board(self) -> list[list[list[dict]]]:
        res = []
        for row in self.board:
            new_row = []
            for col in row:
                new_col = []
                for pawn in col:
                    pawn: Pawn
                    new_col.append((pawn.color, pawn.value))
                
                new_row.append(new_col)
            res.append(new_row)
            
    def minimax(self, board, depth, is_max: bool = True):
        print("board ", board)

        winner = self.check_winner2(board)
        print(winner)
        if  winner != None or depth == 0:
            print("end_board ", board)
            if winner is RED:
                return[1, board]
            elif winner is BLUE:
                return [-1, board]
            else:
                return [0, board]
            
        
        if is_max:
            max_eval = float('-inf')
            best_move = None
            
            for move in self.get_all_moves(board, RED):
                print("move ", move)
                evaluation = self.minimax(move, depth-1, False)[0]
                max_eval = max(evaluation, max_eval)
                if evaluation == max_eval:
                    best_move = move
                
            print("bmax ", best_move)
            return [max_eval, best_move]
        else:
            min_eval = float('inf')
            best_move = None

            for move in self.get_all_moves(board, BLUE):
                evaluation = self.minimax(move, depth-1, True)[0]
                min_eval = min(evaluation, min_eval)
                if evaluation == min_eval:
                    best_move = move
                
            print("bmin ", best_move)
            return [min_eval, best_move]
        
    def get_all_moves(self, board: list[list[list]], color):
        moves = []
        
        if color == BLUE:
            list_pawn = self.pawns
        else: list_pawn = self.pawns_red
        
        for pawn in list_pawn:
            valid_moves = self.find_possible_moves2((pawn.color, pawn.value), board)

            print("valmove ", valid_moves)
            
            for val_move in valid_moves:
                temp_board = copy.deepcopy(board)
                # temp_piece = pawn
                new_board = self.simulate_move(pawn, val_move, temp_board)
                moves.append(new_board)
                

        return moves
    
    def simulate_move(self, pawn, position, board):
        # if pawn.row > -1:
        #     print("popped")
        #     board[pawn.row][pawn.col].pop
        print(pawn)
        (row, col) = position
        (color, value) = pawn
        print("board_start ", board)
        for i in range(RC):
            for j in range(RC):
                if board[i][j]!=[]:
                    if board[i][j][-1].value == value and board[i][j][-1].color == color:
                        board[i][j].remove(pawn)
                        print("popped", board)
        # pawn.row = row
        # pawn.col = col
        board[row][col].append(pawn)
        print("sim ", board)
        return board
    # def bestMove(self):
    #     bestScore = float('-inf');
    #     move = None;
    #     for pawn in self.pawns_red:
    #         for i in range(RC):
    #             for j in range(RC):
    #             #   // Is the spot available?
    #                 if self.board[i][j] == [] or self.board[i][j][-1].value<pawn.value:
    #                     # self.board[i][j].append(pawn)
    #                     # print("before ", self.board)
    #                     # print(pawn, self.board[i][j][-1])
    #                     temp_board = self.board.copy()
    #                     temp_board[i][j].append(pawn)
    #                     score = self.minimax(temp_board, 0, False)
    #                     # self.board[i][j].pop
    #                     # print("after ", self.board)
    #                     if (score > bestScore):
    #                         bestScore = score
    #                         move = (pawn, i, j )
    #                         print("pawn ", pawn) 
    #                         # move =  
    #             print("self board ", self.board)  
    #     print("before ",self.board)                     
    #     (pawn, i, j) = move
    #     self.board[i][j].append(pawn)
    #     self.board[i][j][-1].row = i
    #     self.board[i][j][-1].col = j
    #     self.turn = BLUE
        
    # def minimax(self, board, depth, isMaximizing):
        
    #     result = self.check_winner();
    #     if result != None:
    #         if result == RED:
    #             return 1
    #         elif result == BLUE:
    #             return -1
    #         else:
    #             return 0
    

    #     if isMaximizing :
    #         bestScore = float('-inf');

    #         for pawn in self.pawns_red:
    #             for i in range(RC):
    #                 for j in range(RC):
    #                 #   // Is the spot available?
    #                     if board[i][j] == [] or board[i][j][-1].value<pawn.value:
    #                         # board[i][j].append(pawn)
    #                         # print("before ", board)
    #                         print("max")
    #                         temp_board = board.copy()
    #                         temp_board[i][j].append(pawn)
    #                         score = self.minimax(temp_board, depth+1, False)
    #                         # board[i][j].pop
    #                         # print("after ", board)
    #                         bestScore = max(score,bestScore)
    #         return bestScore

    #     else :
    #         bestScore = float('inf')
    #         for pawn in self.pawns:
    #             for i in range(RC):
    #                 for j in range(RC):
    #                 #   // Is the spot available?
    #                     if board[i][j] == [] or board[i][j][-1].value<pawn.value:
    #                         # board[i][j].append(pawn)
    #                         # print("before ", board)
    #                         print("min")
    #                         temp_board = board.copy()
    #                         temp_board[i][j].append(pawn)
    #                         score = self.minimax(temp_board, depth+1, True)
    #                         # board[i][j].pop
    #                         # print("after ", board)
    #                         bestScore = min(score,bestScore)
    #         return bestScore