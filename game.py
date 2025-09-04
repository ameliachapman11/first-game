import pygame, numpy
pygame.init()

#Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
BOX_SIZE = GAME_WIDTH//3
LINE_COLOR = (121, 71, 6)
LINE_WIDTH = 18
FONT_COLOR = (0, 84, 148) 
WIN_LINE_COLOR = (0, 118, 209)
DIAG_LINE_WIDTH = 23
MESSAGE_COLOR = (207, 238, 255)
MESSAGE_BORDER_COLOR = (0, 84, 148)

#Screen
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Picnic Tac Toe')

#Background & icons
background = pygame.image.load('redblanket.jpg')
background = pygame.transform.scale(background, (GAME_WIDTH, GAME_HEIGHT))
sandwich = pygame.image.load('sandwich.png')
sandwich = pygame.transform.scale(sandwich, (180,180))
apple = pygame.image.load('apple.webp')
apple = pygame.transform.scale(apple, (160, 160))

#Sound effects & background music
pop = pygame.mixer.Sound('pop.wav')
click = pygame.mixer.Sound('click.wav')
win = pygame.mixer.Sound('bell.wav')
pygame.mixer.music.load('chill_guitar.mp3')
pygame.mixer.music.play(-1)

#Board lines
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, BOX_SIZE), (GAME_WIDTH, BOX_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, BOX_SIZE*2), (GAME_WIDTH, BOX_SIZE*2), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (BOX_SIZE, 0), (BOX_SIZE, GAME_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (BOX_SIZE*2, 0), (BOX_SIZE*2, GAME_HEIGHT), LINE_WIDTH)   

#Representation of board & functions for playing game
board = numpy.zeros((3, 3)) #0 = empty cell, 1 = player 1, 2 = player 2

def mark_square(row, col, player):
    board[row][col] = player
    
def available_square(row, col):
    return board[row][col] == 0

#Winning
def check_win(player):
    #Horizontal
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            pygame.draw.line(screen, WIN_LINE_COLOR, (20, row * BOX_SIZE + 100), (GAME_WIDTH-20, row * BOX_SIZE + 100), LINE_WIDTH)
            return True

    #Vertical
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            pygame.draw.line(screen, WIN_LINE_COLOR, (col * BOX_SIZE + 100, 20), (col * BOX_SIZE + 100, GAME_HEIGHT-20), LINE_WIDTH)
            return True
    
    #Ascending diagonal (looks like / )
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        pygame.draw.line(screen, WIN_LINE_COLOR, (20, GAME_HEIGHT-20), (GAME_WIDTH-20, 20), DIAG_LINE_WIDTH)
        return True
    
    #Descending diagonal (looks like \ )
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        pygame.draw.line(screen, WIN_LINE_COLOR, (20, 20), (GAME_WIDTH-20, GAME_HEIGHT-20), DIAG_LINE_WIDTH)
        return True
    
    return False

#Restarting game
font = pygame.font.SysFont('athelas', 40)
def draw_restart_button(player):
    message = None
    if player == 0: message = 'It\'s a tie!'
    elif player == 1: message = 'Sandwich wins!'
    elif player == 2: message = 'Apple wins!'
    
    pygame.draw.rect(screen, MESSAGE_COLOR, (BOX_SIZE-75, BOX_SIZE-30, BOX_SIZE+150, BOX_SIZE+60))
    pygame.draw.rect(screen, MESSAGE_BORDER_COLOR, (BOX_SIZE-75, BOX_SIZE-30, BOX_SIZE+150, BOX_SIZE+60), 10)
    line1 = font.render(message, True, FONT_COLOR)
    line2 = font.render('Press r to restart', True, FONT_COLOR)
    screen.blit(line1, (BOX_SIZE-20, BOX_SIZE+50))
    screen.blit(line2, (BOX_SIZE-20, BOX_SIZE+120))

def reset_board():
    for row in range(3):
        for col in range (3):
            board[row][col] = 0    
    
#Updating display
def update_display():
    #Setting background
    screen.blit(background, (0,0))
    draw_lines()
    
    #Drawing current apple & sandwich icons
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1: screen.blit(sandwich, (BOX_SIZE * col + 20, BOX_SIZE * row + 20))
            elif board[row][col] == 2: screen.blit(apple, (BOX_SIZE * col + 30, BOX_SIZE * row + 30))
    
    #Did player 1 win?       
    check_win(1)
    if check_win(1) and game_over: draw_restart_button(1)
    
    #Did player 2 win?
    check_win(2)
    if check_win(2) and game_over: draw_restart_button(2)
    
    #Is there a tie?
    board_full = True
    for row in board:
         for elem in row:
             if elem == 0: board_full = False
    if board_full and not check_win(1) and not check_win(2): draw_restart_button(0) #if there is a tie
    
    pygame.display.update()

#Main game loop
player = 1
running = True
game_over = False
while running:
    for event in pygame.event.get():
        update_display()
       
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            clicked_row = int(event.pos[1] // BOX_SIZE)
            clicked_col = int(event.pos[0] // BOX_SIZE)
            
            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                pop.play()
                if check_win(player):
                    win.play()
                    game_over = True
                player = 3 - player
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                click.play()
                game_over = False
                player = 1
                reset_board()   
pygame.quit()