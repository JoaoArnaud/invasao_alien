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

# funções do game
def desenhar_botao(tela, cor, x, y, largura, altura, texto, fonte, cor_texto, textoPlusX, textoPlusY):
    pygame.draw.rect(tela, cor, (x, y, largura, altura))
    texto_renderizado = fonte.render(texto, True, cor_texto)
    tela.blit(texto_renderizado, (x + textoPlusX, y + textoPlusY))

fonte = pygame.font.SysFont("Comic Sans MS", 24)

# game looping
while running:
    screen.fill((0,0,0)) # limpa a tela para evitar frames fantasma

    # loop para ver se algum evento ocorreu
    for event in pygame.event.get():
        # fechando o jogo
        if event.type == pygame.QUIT:
            running = False

    desenhar_botao(screen, (255, 255, 255), largura/2 - 100, altura/2 - 50, 200, 50, "Jogar", fonte, (0, 0, 0), 67, 10)
    pygame.display.update()
    clock.tick(30) # fps


pygame.quit()