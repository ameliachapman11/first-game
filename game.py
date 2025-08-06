import pygame, sys
pygame.init

#Initializing screen & images
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Picnic Tac Toe")
background = pygame.image.load('picnicblanket.jpg')

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

running = True
while running:
    for event in pygame.event.get():
        #Setting background
        screen.blit(background, (0,0))
        draw_lines()
        pygame.display.update()
       
        #Exiting window
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()