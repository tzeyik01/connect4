import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COL_COUNT = 7

# Initialize board
def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board

# Dropping the piece to the correct position
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Validating that the piece can be dropped at the selected location
def  is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Get the lowest empty row where the piece will land at
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Helper function to print the board in terminal for debugging
def print_board(board):
    print(np.flip(board, 0))
    print()

# Check if the added piece will result in a win
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COL_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

# Drawing the board using pygame
def draw_board(board):
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
	
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
game_over = False
turn = 0

print_board(board)

pygame.init()

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)

width = COL_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE
size = (width, height)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

# Game Loop
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE/2)), RADIUS)
    
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
			
            # Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARE_SIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("Player 1 wins!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

			# Ask for Player 2 Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARE_SIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)

					if winning_move(board, 2):
						label = myfont.render("Player 2 wins!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)
    
   