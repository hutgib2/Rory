import pygame
import sys
from connect4classes import Board, Game
pygame.init()

rows = 5
cols = 5

cell_size = 100

width = cell_size * cols
height = cell_size * rows

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('connect4')

black = (0, 0, 0)
blue = (0 ,0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
game  = Game()

def draw_board(board):
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, blue, (col * cell_size, row*cell_size, cell_size, cell_size))
            x = col*cell_size + cell_size / 2
            y = row*cell_size + cell_size / 2
            if board.grid[row][col] == ' ':
                color = black
            elif board.grid[row][col] == 'X':
                color = red
            elif board.grid[row][col] == 'O':
                color = yellow
            pygame.draw.circle(screen, color, (x,y), cell_size / 2)

# game starts

running = True
winner = None
font = pygame.font.Font(None, 70)

while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and winner == None:
            x_pos = event.pos[0]
            col = x_pos//cell_size
            row = game.board.drop_piece(game.board, col, game.current_player)
            if row != None:
                if game.board.check_win(row, col, game.current_player):
                    winner = game.current_player
                    message = f'Player {winner} wins!'
                    text = font.render(message, True, green)
                    rect = text.get_rect(center=(width//2, height//2))
                    screen.blit(text, rect)
                elif all(game.board.grid[0][col] != ' ' for col in range(cols)):
                    message = 'it is a tie'
                    text = font.render(message, True, green)
                    rect = text.get_rect(center=(width//2, height//2))
                    winner = 'Draw'
                    screen.blit(text, rect)
                else:
                    game.switch_player()

    draw_board(game.board)
    if winner is not None:
        screen.blit(text, rect)
    pygame.display.update()

pygame.quit()
sys.exit()