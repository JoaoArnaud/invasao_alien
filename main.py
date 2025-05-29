import pygame
import math
from pygame.locals import *
import jogo

# setup do pygame
pygame.init()
largura, altura = 640, 480
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Alien's Game")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
fonte_titulo = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
jogo_iniciado = False
running = True
tempo = 0  # usado para animar o título

# carregue a imagem tela inicial
fundo_imagem = pygame.image.load("C:\\Users\\joaoa\\OneDrive\\Documents\\GitHub\\projeto_jogo\\imagens\\fundo tela inicial.jpg")
fundo_imagem = pygame.transform.scale(fundo_imagem, (largura, altura))


# funções
def desenhar_botao(tela, cor, x, y, largura, altura, texto, fonte, cor_texto):
    sombra_offset = 4
    pygame.draw.rect(tela, (50, 50, 50), (x + sombra_offset, y + sombra_offset, largura, altura), border_radius=10)
    pygame.draw.rect(tela, cor, (x, y, largura, altura), border_radius=10)
    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_renderizado, texto_rect)

def clique_botao(pos_mouse, x, y, largura, altura):
    return x <= pos_mouse[0] <= x + largura and y <= pos_mouse[1] <= y + altura

def desenhar_titulo_animado(tela, tempo):
    texto = "Invasão Alien"
    cor = (255, 255, 255)
    titulo_render = fonte_titulo.render(texto, True, cor)
    x = largura // 2 - titulo_render.get_width() // 2
    # movimento senoidal para cima e para baixo
    y_base = 80
    offset = int(10 * math.sin(tempo * 2))  # controla a velocidade e amplitude
    y = y_base + offset
    tela.blit(titulo_render, (x, y))

def inicia_jogo():
    global jogo_iniciado
    jogo_iniciado = True
    print('Jogo iniciado')

# game loop
while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            print('Jogo fechado')
            running = False

        if not jogo_iniciado and event.type == MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            if clique_botao(pos_mouse, largura // 2 - 100, altura // 2 - 50, 200, 60):
                inicia_jogo()
    # tela inical
    if not jogo_iniciado:
        screen.blit(fundo_imagem, (0, 0))  # fundo tela inicial
        desenhar_titulo_animado(screen, tempo)
        desenhar_botao(screen, (255, 255, 255), largura // 2 - 100, altura // 2 - 50, 200, 60, "Jogar", fonte, (0, 0, 0))
    else:
        # aqui começa o jogo
        jogo.iniciar()
        jogo_iniciado = False  # voltar ao menu após o game over

    pygame.display.update()
    clock.tick(30)
    tempo += 0.03  # suaviza o movimento do título

pygame.quit()
