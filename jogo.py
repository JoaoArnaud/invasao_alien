import pygame
import random

largura, altura = 640, 480

def iniciar():
    screen = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Comic Sans MS", 24)

    jogador = pygame.Rect(largura//2 - 25, altura - 60, 50, 50)
    vida = 100
    tiros = []
    tiros_inimigos = []
    inimigos = [pygame.Rect(random.randint(0, largura - 40), random.randint(20, 150), 40, 40) for _ in range(5)]
    fase = 1

    rodando = True
    tempo_ultimo_tiro_inimigo = 0
    intervalo_tiro_inimigo = 1000  # milissegundos

    # Mostra número da fase por 2 segundos antes do início
    mostrar_fase = True
    tempo_fase = pygame.time.get_ticks()

    while rodando:
        clock.tick(30)
        tempo_atual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                return

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_z:
                    tiros.append(pygame.Rect(jogador.x + jogador.width // 2 - 2, jogador.y, 5, 10))

        # Movimento do jogador com limite de tela
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador.left > 0:
            jogador.x -= 5
        if teclas[pygame.K_RIGHT] and jogador.right < largura:
            jogador.x += 5
        if teclas[pygame.K_UP] and jogador.top > 0:
            jogador.y -= 5
        if teclas[pygame.K_DOWN] and jogador.bottom < altura:
            jogador.y += 5

        # Movimento dos tiros do jogador
        for tiro in tiros:
            tiro.y -= 10
        tiros = [tiro for tiro in tiros if tiro.y > 0]

        # Disparo automático dos inimigos (estáticos)
        if tempo_atual - tempo_ultimo_tiro_inimigo > intervalo_tiro_inimigo:
            for inimigo in inimigos:
                tiros_inimigos.append(pygame.Rect(inimigo.centerx, inimigo.bottom, 5, 10))
            tempo_ultimo_tiro_inimigo = tempo_atual

        for tiro in tiros_inimigos:
            tiro.y += 7
        tiros_inimigos = [tiro for tiro in tiros_inimigos if tiro.y < altura]

        # Colisão tiro do jogador vs inimigo
        for inimigo in inimigos[:]:
            for tiro in tiros[:]:
                if inimigo.colliderect(tiro):
                    inimigos.remove(inimigo)
                    tiros.remove(tiro)
                    break

        # Colisão tiro inimigo vs jogador
        for tiro in tiros_inimigos[:]:
            if jogador.colliderect(tiro):
                vida -= 5
                tiros_inimigos.remove(tiro)

        # Próxima fase
        if len(inimigos) == 0:
            fase += 1
            inimigos = [pygame.Rect(random.randint(0, largura - 40), random.randint(20, 150), 40, 40) for _ in range(5 + fase)]  # mais inimigos
            mostrar_fase = True
            tempo_fase = tempo_atual

        # Desenho
        screen.fill((10, 10, 30))
        pygame.draw.rect(screen, (255, 255, 255), jogador)
        for inimigo in inimigos:
            pygame.draw.rect(screen, (255, 0, 0), inimigo)
        for tiro in tiros:
            pygame.draw.rect(screen, (255, 255, 0), tiro)
        for tiro in tiros_inimigos:
            pygame.draw.rect(screen, (255, 100, 100), tiro)

        texto_vida = fonte.render(f"Vida: {vida}", True, (255, 255, 255))
        screen.blit(texto_vida, (10, 10))

        if mostrar_fase:
            texto_fase = fonte.render(f"Fase {fase}", True, (255, 255, 255))
            rect = texto_fase.get_rect(center=(largura // 2, altura // 2))
            screen.blit(texto_fase, rect)
            if tempo_atual - tempo_fase > 2000:
                mostrar_fase = False

        pygame.display.update()

        if vida <= 0:
            print("Game Over")
            rodando = False
