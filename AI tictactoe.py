import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
W = WIDTH // 3
H = HEIGHT // 3
ai = 'X'
human = 'O'
currentPlayer = human

# Create the game board
board = [
    ['', '', ''], ['', '', ''], ['', '', '']]

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe with Minimax Algorithm")

def equals3(a, b, c):
    return a == b and b == c and a != ''

def checkWinner():
    winner = None

    # Check horizontal
    for i in range(3):
        if equals3(board[i][0], board[i][1], board[i][2]):
            winner = board[i][0]

    # Check vertical
    for i in range(3):
        if equals3(board[0][i], board[1][i], board[2][i]):
            winner = board[0][i]

    # Check diagonal
    if equals3(board[0][0], board[1][1], board[2][2]):
        winner = board[0][0]
    if equals3(board[2][0], board[1][1], board[0][2]):
        winner = board[2][0]

    openSpots = sum(row.count('') for row in board)
    if winner is None and openSpots == 0:
        return 'tie'
    else:
        return winner

def draw():
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 0, 0), (W, 0), (W, HEIGHT), 4)
    pygame.draw.line(screen, (0, 0, 0), (W * 2, 0), (W * 2, HEIGHT), 4)
    pygame.draw.line(screen, (0, 0, 0), (0, H), (WIDTH, H), 4)
    pygame.draw.line(screen, (0, 0, 0), (0, H * 2), (WIDTH, H * 2), 4)

    for j in range(3):
        for i in range(3):
            x = W * i + W / 2
            y = H * j + H / 2
            spot = board[i][j]
            font = pygame.font.Font(None, 32)
            r = W / 4
            if spot == human:
                pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), int(r), 2)
            elif spot == ai:
                pygame.draw.line(screen, (0, 0, 255), (x - r, y - r), (x + r, y + r), 2)
                pygame.draw.line(screen, (0, 0, 255), (x + r, y - r), (x - r, y + r), 2)

    result = checkWinner()
    if result is not None:
        font = pygame.font.Font(None, 32)
        result_surface = font.render('', True, (0, 0, 0))
        if result == 'tie':
            result_surface = font.render('Tie!', True, (0, 0, 0))
        else:
            result_surface = font.render(f'{result} wins!', True, (0, 0, 0))
        screen.blit(result_surface, (WIDTH // 2 - 50, HEIGHT // 2 - 20))

    pygame.display.flip()

def mousePressed():
    global currentPlayer
    if currentPlayer == human:
        i = math.floor(pygame.mouse.get_pos()[0] / W)
        j = math.floor(pygame.mouse.get_pos()[1] / H)
        if board[i][j] == '':
            board[i][j] = human
            currentPlayer = ai
            bestMove()
def bestMove():
    global currentPlayer
    best_score = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ''  # Undo the move

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = ai
        currentPlayer = human

def minimax(board, depth, is_maximizing):
    result = checkWinner()

    if result is not None:
        if result == ai:
            return 1
        elif result == human:
            return -1
        else:
            return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = ai
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''  # Undo the move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = human
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''  # Undo the move
                    best_score = min(score, best_score)
        return best_score

# Implement the minimax algorithm for the AI's move

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed()

    draw()
