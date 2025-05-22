import pygame
from pygame.locals import *

# pygame setup
pygame.init() # inicializando pygame
largura = 640
altura = 480
screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Alien's Game")

# game looping
while running:
    # loop para ver se algum evento ocorreu
    for event in pygame.event.get():
        # fechando o jogo
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60) # fps
pygame.quit()