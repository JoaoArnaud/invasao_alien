import pygame
import random

largura, altura = 640, 480

def iniciar():
    # rodando nova tela
    screen = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Comic Sans MS", 24)

    # objetos
    jogador = pygame.Rect(largura//2 - 25, altura - 60, 50, 50)
    vida = 100
    tiros = []
    inimigos = [pygame.Rect(random.randint(0, largura - 40), random.randint(-100, -40), 40, 40) for _ in range(5)]

    rodando = True

    # rodando game loop
    while rodando:
        clock.tick(30)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return  # retorna pro menu

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_z:
                    tiros.append(pygame.Rect(jogador.x + 22, jogador.y, 5, 10))

        # Movimento do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador.left > 0:
            jogador.x -= 5
        if teclas[pygame.K_RIGHT] and jogador.right < largura:
            jogador.x += 5
        if teclas[pygame.K_UP]:
            jogador.y -= 5
        if teclas[pygame.K_DOWN]:
            jogador.y += 5

        # Movimento dos tiros
        for tiro in tiros:
            tiro.y -= 10
        tiros = [tiro for tiro in tiros if tiro.y > 0]

        # Movimento dos inimigos
        for inimigo in inimigos:
            inimigo.y += 2
            if inimigo.y > altura:
                inimigo.y = random.randint(-100, -40)
                inimigo.x = random.randint(0, largura - 40)

        # Colisão tiro vs inimigo
        for inimigo in inimigos[:]:
            for tiro in tiros[:]:
                if inimigo.colliderect(tiro):
                    inimigos.remove(inimigo)
                    tiros.remove(tiro)
                    inimigos.append(pygame.Rect(random.randint(0, largura - 40), random.randint(-100, -40), 40, 40))
                    break

        # Desenho
        screen.fill((10, 10, 30))
        pygame.draw.rect(screen, (255, 255, 255), jogador)
        for inimigo in inimigos:
            pygame.draw.rect(screen, (255, 0, 0), inimigo)
        for tiro in tiros:
            pygame.draw.rect(screen, (255, 255, 0), tiro)

        texto_vida = fonte.render(f"Vida: {vida}", True, (255, 255, 255))
        screen.blit(texto_vida, (10, 10))

        pygame.display.update()
