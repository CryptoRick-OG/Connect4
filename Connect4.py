import numpy as np
import pygame
import sys
import math

BLUE = (0,0,222) #Background colour
BLACK = (0,0,0) #Colour of empty slots
RED = (222,0,0) #Player 1 colour
YELLOW = (222,222,0) #Player 2 colour


ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
  board = np.zeros((ROW_COUNT,COLUMN_COUNT)) #Matrix of zeros to represent the board
  return board

def drop_piece(board, row, col, piece):
  board[row][col] = piece 

def is_valid_location(board, col):
  return board[ROW_COUNT-1][col] == 0 #checks if the las row on the board has been filled

def get_next_open_row(board, col): #this  function checks the slot where the piece drops
  for r in range(ROW_COUNT): 
    if board[r][col] == 0: #this condition checks where is the next 0 in the row
      return r 

def print_board(board):
  print(np.flip(board, 0)) #Flip the matrix so that players input starts at the bottom of the board instead of the top

def winning_move(board, piece):

  #Check horizontal win
  for c in range(COLUMN_COUNT-3):
    for r in range(ROW_COUNT):
      if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
        return True
  
  #Check for vertical win
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT-3):
      if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
        return True

  #Check for  +ve diagonal win
  for c in range(COLUMN_COUNT-3):
    for r in range(ROW_COUNT-3):
      if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
        return True

  #Check for -ive diagonal win
  for c in range(COLUMN_COUNT-3):
    for r in range(3, ROW_COUNT):
      if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
        return True

def draw_board(board):
  for c in range(COLUMN_COUNT): #loop through each slot in the column (6 total)
    for r in range(ROW_COUNT): #loop through each column (7 total)
      #this double loop allows to cover each space in the matrix (i.e. the board)
      pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)) #pygame.draw is the module for drawing shapes in Python. Here we draw a BLUE rectangle as the board
      pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), (int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2))), RADIUS) #Here we draw the empty slots with a black circle of radius

  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      if board[r][c] == 1:
        pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-(int(r*SQUARESIZE+SQUARESIZE/2))), RADIUS)
      elif board[r][c] == 2:
        pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-(int(r*SQUARESIZE+SQUARESIZE/2))), RADIUS)
  pygame.display.update()


board = create_board()
print_board(board)
game_over = False #while this is False, the game is still going.
turn = 0 # 0 represents the turn of Player 1. Turn value will hancge from 0 to 1 to indicate who's turn it is

pygame.init()

#Game display
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    
    if event.type == pygame.MOUSEMOTION:
      pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
      posx = event.pos[0]
      if turn == 0:
        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
      else:
        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
      pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
      pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
      # print(event.pos)
      # #Ask Player 1 input
      if turn == 0:
        posx = event.pos[0]
        col = int(math.floor(posx/SQUARESIZE))

        if is_valid_location(board, col): 
          row = get_next_open_row(board, col)
          drop_piece(board, row, col, 1) #the Player's piece is dropped in the next open row if the location is valid (i.e. there are still 0's remaining in the column)

          if winning_move(board, 1):
            label = myfont.render("Player 1 wins! CONGRATS!!!", 1, RED)
            screen.blit(label, (40,10))
            game_over = True

      # #Ask for PLayer 2 input
      else:
        posx = event.pos[0]
        col = int(math.floor(posx/SQUARESIZE))
        
        if is_valid_location(board, col):
          row = get_next_open_row(board, col)
          drop_piece(board, row, col, 2)

          if winning_move(board, 2):
            label = myfont.render("Player 2 wins! CONGRATS!!!", 1, YELLOW)
            screen.blit(label, (40,10))
            game_over = True
      
      print_board(board)
      draw_board(board)

      turn += 1 #increase turn by 1 so that it doesn't stay at 0
      turn = turn % 2 #this module alternates turn value between 1 and 0 (i.e. player 1 and player 2)

      if game_over:
        pygame.time.wait(10000)
