import pygame
import time

from cons import *
from pawn import Pawn
from button import Button

class Board:
    # inisiasi
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
        self.ai = False
        self.algorithm = None
    
    # fungsi reset apabila user bermain kembali
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
        self.ai = False
        self.algorithm = None
    
    # mengisi flag jika bermain dengan AI
    def isAI(self, ai):
        self.ai = ai
    
    # menampilan elemen yang ada pada halaman game
    def draw(self):
        self.draw_board()
        self.draw_possible_moves()
        self.draw_board_border()
        self.draw_pawn()
        self.draw_turn()

    # memuat pawn object
    def add_pawn(self):
        for i in range(MARGIN_SIDE, SCREEN_WIDTH-MARGIN_SIDE, 90):
            self.pawns_red.append(Pawn((i-MARGIN_SIDE)//90 + 1, RED, i+45, 85))
            self.pawns_blue.append(Pawn((i-MARGIN_SIDE)//90 + 1, BLUE, i+45, SCREEN_HEIGHT-90))

    # menggambar pawn pada screen
    def draw_pawn(self):
        # menampilkan pawn biru yang tidak ada di papan
        for pawn in self.pawns_blue:
            pawn.draw(self.screen)
        
        # menampilkan pawn merah yang tidak ada di papan
        for pawn in self.pawns_red:
            pawn.draw(self.screen)
        
        # menampilkan pawn yang ada di papan
        for row in self.board:
            for cell in row:
                if cell == []:
                    continue
                cell[-1].draw(self.screen)

    # menggambar papan game
    def draw_board(self):
        for row in range(RC):
            for col in range(RC):
                if (row+col)%2:
                    pygame.draw.rect(self.screen, BLACK, (col*SQUARE +MARGIN_SIDE, row*SQUARE+MARGIN_TOP, SQUARE, SQUARE))
                else:
                    pygame.draw.rect(self.screen, WHITE, (col*SQUARE +MARGIN_SIDE, row*SQUARE+MARGIN_TOP, SQUARE, SQUARE))
    
    # menggambar border papan game
    def draw_board_border(self):
        for row in range(RC):
            for col in range(RC):
                pygame.draw.rect(self.screen, RED, (col*SQUARE +MARGIN_SIDE-4, row*SQUARE+MARGIN_TOP-4, SQUARE+4, SQUARE+4), 4)
    
    # update ketika menerima input dari mouse
    def update(self, pos):
        if self.turn == RED and self.ai == True:
            self.run_AI()
        if self.turn == BLUE or self.ai == False:
            self.click_board(pos)
            self.click_pawn(pos)
            if self.selected_pawn:
                color, value = self.selected_pawn.color, self.selected_pawn.value
                self.possible_moves = self.find_possible_moves(self.board, color, value)
            else:
                self.possible_moves = []
        
    # fungsi ketika pawn ditekan atau memilih pawn
    def click_pawn(self, pos):
        (x, y) = pos
        selecting = False
        pawn_list = []
        
        # memeriksa giliran
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
    
    # fungsi ketika board di tekan atau meletakkan pawn ke board 
    def click_board(self, pos):
        # return jika tidak ada pawn yang dipilih
        if not self.selected_pawn:
            return
        
        (x, y) = pos
        
        # memeriksa input mouse dan memindahkan pawn ke petak yang dipilih
        for move in self.possible_moves:
            (row, col) = move
            board_x = (MARGIN_SIDE + col * SQUARE)
            board_y = (MARGIN_TOP + row * SQUARE)
            dx = x - board_x
            dy = y - board_y
            
            if (dx >= 0 and dx <= SQUARE) and (dy >= 0 and dy <= SQUARE):
                
                if self.selected_pawn.row != -1 and self.selected_pawn.col != -1:
                    self.board[self.selected_pawn.row][self.selected_pawn.col].pop()
                
                if self.selected_pawn in self.pawns_blue:
                    self.pawns_blue.remove(self.selected_pawn)
                elif self.selected_pawn in self.pawns_red: 
                    self.pawns_red.remove(self.selected_pawn)
                    
                self.board[row][col].append(self.selected_pawn)
                self.selected_pawn.set_board_position(row, col)
                self.selected_pawn.set_position(board_x + SQUARE//2, board_y + SQUARE//2)
                self.selected_pawn.unselect()
                self.possible_moves = []
                self.selected_pawn = None
                self.switch_turn()
                return
                    
    # menemukan gerak yang mungkin dilakukan sebuah pawn
    def find_possible_moves(self, board, color, value):
        possible_moves = []
        for row in range(RC):
            for col in range(RC):
                if board[row][col] != [] and board[row][col][-1].color == color:
                    continue
                if board[row][col] == [] or board[row][col][-1].value < value:
                    possible_moves.append((row, col))
                    
        return possible_moves
    
    # menemukan kombinasi board yang mungkin
    def get_possible_boards(self, board, pawns_blue: list[Pawn], pawns_red: list[Pawn], color):
        possible_boards = []
        pawns = []
       
        # menyalin pawn
        if color == RED:
            pawns.extend(pawns_red)
        else : pawns.extend(pawns_blue)
        
        # menyalin pawn yang ada pada board
        for row in board:
            for cell in row:
                if cell == []:
                    continue
                if cell[-1].color == color:
                    pawns.append(cell[-1])
                    
        # melakukan simulasi peletakan pawn pada papan
        for pawn in pawns:
            possible_moves = self.find_possible_moves(board, pawn.color, pawn.value)
            
            for move in possible_moves:
                (row, col) = move
                temp_board = [
                    [[], [], []],
                    [[], [], []],
                    [[], [], []]
                ]
                
                # menyalin papan
                for r in range(RC):
                    for c in range(RC):
                        temp_board[r][c].extend(board[r][c])
                
                # menyalin pawn yang akan sisimulasikan
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
                
                # mengubah atribut pawn (koordinat x y dan row column)
                pawn: Pawn
                new_pawn = Pawn(pawn.value, pawn.color, pawn.x, pawn.y)
                
                board_x = (MARGIN_SIDE + col * SQUARE)
                board_y = (MARGIN_TOP + row * SQUARE)
                
                new_pawn.set_board_position(row, col)
                new_pawn.set_position(board_x + SQUARE//2, board_y + SQUARE//2)
                
                # simulasi
                temp_board[row][col].append(new_pawn)
                possible_boards.append((temp_board, blues, reds))
                
        return possible_boards
    
    # menampilkan petak yang mungkin ditempati pawn
    def draw_possible_moves(self):
        if self.possible_moves == []:
            return
        
        for move in self.possible_moves:
            (row, col) = move
            pygame.draw.rect(self.screen, GREEN, (col*SQUARE +MARGIN_SIDE, row*SQUARE+MARGIN_TOP, SQUARE, SQUARE))
    
    # mengganti giliran permainan
    def switch_turn(self):
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

    # menampilkan giliran bermain di layar
    def draw_turn(self):
        if self.selected_pawn is not None:
            return 
        font_size = 80
        font = pygame.font.SysFont(None, font_size)
        text_stroke = pygame.font.SysFont(None, font_size+1)

        text = font.render("BLUE's Turn" if self.turn == BLUE else "RED's Turn", True, self.turn)
        text_stroke_surface = text_stroke.render("BLUE's Turn" if self.turn == BLUE else "RED's Turn", True, BLACK)
        if self.turn == RED and self.ai == True:
            text = font.render ("COMPUTER's Turn", True, self.turn)
            text_stroke_surface = text_stroke.render("COMPUTER's Turn", True, BLACK)

        text_rect= text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        text_stroke_rect  = text_rect.copy()

        self.screen.blit(text_stroke_surface, text_stroke_rect.move(3, 3))
        self.screen.blit(text_stroke_surface, text_stroke_rect.move(-3, -3))
        self.screen.blit(text_stroke_surface, text_stroke_rect.move(-3, 3)) 
        self.screen.blit(text_stroke_surface, text_stroke_rect.move(3, -3))
        self.screen.blit(text, text_rect)

    # memeriksa apakah pawn pada susunan tertentu ada
    def pawn_existed(self, a, b, c):
        if a != [] and b != [] and c != []:
            return True
        return False
    
    # memeriksa apakah pawn pada susunan tertentu memiliki warna yang sama 
    def pawn_in_row(self, a, b, c):
        if a==b and b==c:
            return True
        return False
    
    # memeriksa pemenang saat ini
    def check_winner_board(self):
        return self.check_winner(self.board)
    
    # memeriksa pemenang pada board
    def check_winner(self, board, log=False):
        col = 0
        row = 0
        winner = None
        
        # memeriksa papan secara horizontal 
        for a in range(RC):
            if self.pawn_existed(board[a][col],board[a][col+1], board[a][col+2]) :
                if self.pawn_in_row(board[a][col][-1].color, board[a][col+1][-1].color, board[a][col+2][-1].color):
                    if winner == None or winner == board[a][col][-1].color:
                        winner = board[a][col][-1].color
                    else:
                        return GREEN
                    
        # memeriksa papan secara vertikal 
        for b in range(RC):
            if self.pawn_existed(board[row][b], board[row+1][b], board[row+2][b]) :
                if self.pawn_in_row(board[row][b][-1].color, board[row+1][b][-1].color, board[row+2][b][-1].color):
                    if winner == None or winner == board[row][b][-1].color:
                        winner = board[row][b][-1].color
                    else:
                        return GREEN
                
        # memeriksa papan secara diagonal [(0,0), (1,1), (2,2)]
        if self.pawn_existed(board[row][col], board[row+1][col+1], board[row+2][col+2]) :
            if self.pawn_in_row(board[row][col][-1].color, board[row+1][col+1][-1].color, board[row+2][col+2][-1].color):
                if winner == None or winner == board[row][col][-1].color:
                    winner = board[row][col][-1].color
                else:
                    return GREEN
        
        # memeriksa papan secara diagonal [(0,2), (1,1), (2,0)]
        if self.pawn_existed(board[row][col+2], board[row+1][col+1], board[row+2][col]) :
            if self.pawn_in_row(board[row][col+2][-1].color, board[row+1][col+1][-1].color, board[row+2][col][-1].color):
                if winner == None or winner == board[row][col+2][-1].color:
                        winner = board[row][col+2][-1].color
                else:
                    return GREEN
        
        return winner
    
    # membuat tampilan pemenang jika sudah mendapatkan winner
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
    

    def run_AI(self):
        # jika bermain bersama AI maka algoritma dijalankan di sini
        if self.ai:
            start = time.time()
            
            # MINIMAX
            if self.algorithm == "MINIMAX":
                algo = "minimax "
                evaluation, best_board, pawns_blue, pawns_red = self.minimax(self.board, self.pawns_blue, self.pawns_red, 3)
            
            # ALPHA BETA PRUNING
            if self.algorithm == "ALPHA-BETA":
                algo = "alpha betha pruning "
                evaluation, best_board, pawns_blue, pawns_red = self.alphabetha(self.board, self.pawns_blue, self.pawns_red, 3)
            
            end = time.time()
            print( algo, f"time: {end-start}")

            self.board = best_board
            self.pawns_blue = pawns_blue
            self.pawns_red = pawns_red
            self.turn = BLUE
            
    # fungsi evaluasi keunggulan agent atau lawan
    def evaluate(self, board, is_max):
        blue_point = 0
        red_point = 0
        total_point = 0
        
        for row in board:
            for cell in row:
                if cell == []:
                    continue
                else:
                    for i in range(len(cell)):
                        total_point+=cell[i].value
                if cell[-1].color == BLUE:
                    blue_point+=cell[-1].value
                if cell[-1].color == RED:
                    red_point+=cell[-1].value
        
        if red_point == blue_point:
            return 0

        if is_max:   
            return red_point/total_point
        else:
            return - (blue_point/total_point)
     
    # minimax algorithm
    def minimax(self, board, pawns_blue: list[Pawn], pawns_red: list[Pawn], depth, is_max: bool = True):
        winner = self.check_winner(board)
        
        # memeriksa pemenang dan depth sebagai base case
        if  winner != None or depth == 0:
            if winner is RED:
                return [1, board, pawns_blue, pawns_red]
            elif winner is BLUE:
                return [-1, board, pawns_blue, pawns_red]
            elif winner is GREEN:
                return [0, board, pawns_blue, pawns_red]
            else:
                return [self.evaluate(board, is_max), board, pawns_blue, pawns_red]
        
        # max jika giliran AI
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
        
        # min jika giliran pemain
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
        
    # alpha-beta algorithm
    def alphabetha(self, board, pawns_blue: list[Pawn], pawns_red: list[Pawn], depth, is_max: bool = True, alpha: float = float('-inf'), beta: float = float('inf')):
        winner = self.check_winner(board)
        
        # memeriksa pemenang dan depth sebagai base case
        if  winner != None or depth == 0:
            if winner is RED:
                return [1, board, pawns_blue, pawns_red]
            elif winner is BLUE:
                return [-1, board, pawns_blue, pawns_red]
            elif winner is GREEN:
                return [0, board, pawns_blue, pawns_red]
            else:
                return [self.evaluate(board, is_max), board, pawns_blue, pawns_red]
        
        # max jika giliran AI
        if is_max:
            max_eval = float('-inf')
            best_move = None
            best_pawns_red = pawns_red
            
            for move, _, reds in self.get_possible_boards(board, pawns_blue, best_pawns_red, RED):
                evaluation = self.alphabetha(move, pawns_blue, best_pawns_red, depth-1, False, alpha, beta)[0]
                max_eval = max(evaluation, max_eval)
                
                # melakukan pruning
                if max_eval>=beta:
                    break
                
                alpha = max(alpha, max_eval)
                
                if evaluation == max_eval:
                    best_move = move
                    best_pawns_red  = reds
        
            return [max_eval, best_move, pawns_blue, best_pawns_red]
        
        # min jika giliran AI
        else :
            min_eval = float('inf')
            best_move = None
            best_pawns_blue = pawns_blue
            
            for move, blues, _ in self.get_possible_boards(board, best_pawns_blue, pawns_red, BLUE):
                evaluation = self.alphabetha(move, best_pawns_blue, pawns_red, depth-1, True, alpha, beta)[0]
                min_eval = min(evaluation, min_eval)
                
                # melakukan pruning
                if min_eval < alpha:
                    break
                
                beta = min(beta, min_eval)
                
                if evaluation == min_eval:
                    best_move = move
                    best_pawns_blue  = blues
        
            return [min_eval, best_move, best_pawns_blue, pawns_red]