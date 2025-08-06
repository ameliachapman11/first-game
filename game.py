import pygame, sys
import numpy
pygame.init()

#Initializing screen & images
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Picnic Tac Toe")
background = pygame.image.load('picnicblanket.jpg')
sandwich = pygame.image.load('sandwich.png')
sandwich = pygame.transform.scale(sandwich, (180,180))
apple = pygame.image.load('apple.webp')
apple = pygame.transform.scale(apple, (160, 160))

#Board lines
LINE_COLOR = (121, 71, 6)
LINE_WIDTH = 18
def draw_lines():
    #Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    #Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

#Adding currently placed apples & sandwiches to display
def draw_icons():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1: screen.blit(sandwich, (200 * col + 10, 200 * row + 10))
            elif board[row][col] == 2: screen.blit(apple, (200 * col + 20, 200 * row + 20))

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

#Winning
def check_win(player):
    #Horizontal win check
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horiz_win(row)
            return True

    #Vertical win check
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vert_win(col)
            return True
    
    #Ascending diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal_win()
        return True
    
    #Descending diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal_win()
        return True
    
    return False

#Restarting game
font = pygame.font.SysFont('athelas', 40)
FONT_COLOR = (0, 84, 148) 
def draw_restart_button(player):
    winner = None
    if player == 1: winner = 'Sandwich'
    elif player == 2: winner = 'Apple'
    
    pygame.draw.rect(screen, (207, 238, 255), (125, 180, 350, 255))
    line1 = font.render(winner + ' wins!', True, FONT_COLOR)
    line2 = font.render('Press r to restart', True, FONT_COLOR)
    screen.blit(line1, (170, 250))
    screen.blit(line2, (170, 320))

def restart():
    for row in range(3):
        for col in range (3):
            board[row][col] = 0    

WIN_LINE_COLOR = (0, 118, 209)
DIAG_LINE_WIDTH = 23
def draw_horiz_win(row):
    pygame.draw.line(screen, WIN_LINE_COLOR, (20, row * 200 + 100), (580, row * 200 + 100), LINE_WIDTH)

def draw_vert_win(col):
    pygame.draw.line(screen, WIN_LINE_COLOR, (col * 200 + 100, 20), (col * 200 + 100, 580), LINE_WIDTH)

def draw_asc_diagonal_win(): #for when the player win looks like /
    pygame.draw.line(screen, WIN_LINE_COLOR, (20, 580), (580, 20), DIAG_LINE_WIDTH)

def draw_desc_diagonal_win(): #for when the player win looks like \
    pygame.draw.line(screen, WIN_LINE_COLOR, (20, 20), (580, 580), DIAG_LINE_WIDTH)

player = 1
running = True
game_over = False
while running:
    for event in pygame.event.get():
        #Setting background
        screen.blit(background, (0,0))
        draw_lines()
        draw_icons()  
        check_win(1)
        if check_win(1) and game_over: draw_restart_button(1)
        check_win(2)
        if check_win(2) and game_over: draw_restart_button(2)
        pygame.display.update()
       
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            clicked_row = int(event.pos[1] // 200)
            clicked_col = int(event.pos[0] // 200)
            
            if available_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    if check_win(player): 
                        game_over = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    if check_win(player): 
                        game_over = True
                    player = 1 
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                player = 1
                restart()   
pygame.quit()