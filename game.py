import pygame, sys
import numpy
pygame.init

#Initializing screen & images
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Picnic Tac Toe")
background = pygame.image.load('picnicblanket.jpg')
sandwich = pygame.image.load('sandwich.png')
sandwich = pygame.transform.scale(sandwich, (180,180))
apple = pygame.image.load('apple.webp')
apple = pygame.transform.scale(apple, (160, 160))

#Board lines
LINE_COLOR = (91, 58, 28)
LINE_WIDTH = 18
def draw_lines():
    #Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    #Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)
draw_lines()

#Representation of board & playing game
board = numpy.zeros((3, 3)) # 0 = empty cell, 1 = player 1, 2 = player 2

def mark_square(row, col, player):
    board[row][col] = player
    
def available_square(row, col):
    return board[row][col] == 0

def is_board_full(): #used for checking for a tie
    for row in board:
        for elem in row:
            if elem == 0: return False
    return True


player = 1 #change to random?
running = True
while running:
    for event in pygame.event.get():
        #Setting background
        screen.blit(background, (0,0))
        draw_lines()
        
        #Adding currently placed apples & sandwiches to display
        for row in range(3):
            for col in range(3):
                if board[row][col] == 1: screen.blit(sandwich, (200 * col + 10, 200 * row + 10))
                elif board[row][col] == 2: screen.blit(apple, (200 * col + 10, 200 * row + 10))
                    
        pygame.display.update()
       
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_row = int(event.pos[1] // 200)
            clicked_col = int(event.pos[0] // 200)
            
            if available_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    player = 1
            
pygame.quit()