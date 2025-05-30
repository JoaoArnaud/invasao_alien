import pygame
import random

largura, altura = 640, 480

def mostrar_game_over(screen, fonte_grande, fonte, fase):
    screen.fill((0, 0, 0))
    texto1 = fonte_grande.render("GAME OVER", True, (255, 0, 0))
    texto2 = fonte.render(f"Você alcançou a fase {fase}", True, (255, 255, 255))
    texto3 = fonte.render("Retornando ao menu...", True, (200, 200, 200))
                
    rect1 = texto1.get_rect(center=(largura // 2, altura // 2 - 40))
    rect2 = texto2.get_rect(center=(largura // 2, altura // 2 + 10))
    rect3 = texto3.get_rect(center=(largura // 2, altura // 2 + 50))

    screen.blit(texto1, rect1)
    screen.blit(texto2, rect2)
    screen.blit(texto3, rect3)

    pygame.mixer.music.load("sons\\losing-horn.mp3")
    pygame.mixer.music.play()

    pygame.display.update()
    pygame.time.wait(6000) # espera 6 segundos

def iniciar():
    # musiquinha
    pygame.mixer.music.load("sons\\musica_sans.mp3")
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((largura, altura))
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Comic Sans MS", 24)
    fonte_grande = pygame.font.SysFont("Comic Sans MS", 48)

    # Carrega as imagens
    nave_heroi_img = pygame.image.load("imagens\\nave_heroi.png").convert_alpha()
    nave_heroi_img = pygame.transform.scale(nave_heroi_img, (50, 50))
    nave_alien_img = pygame.image.load("imagens\\nave_alien.png").convert_alpha()
    nave_alien_img = pygame.transform.scale(nave_alien_img, (40, 40))

    jogador = nave_heroi_img.get_rect(center=(largura // 2, altura - 60))
    vida = 100
    tiros = []
    tiros_inimigos = []

    inimigos = []
    for _ in range(5):
        img_rect = nave_alien_img.get_rect(topleft=(random.randint(0, largura - 40), random.randint(20, 150)))
        inimigos.append(img_rect)

    fase = 1

    rodando = True
    tempo_ultimo_tiro_inimigo = 0
    intervalo_tiro_inimigo = random.randint(1000, 3000)  # entre 1s e 3s

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
            intervalo_tiro_inimigo = random.randint(1000, 3000)

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
        screen.blit(nave_heroi_img, jogador)
        for inimigo in inimigos:
            screen.blit(nave_alien_img, inimigo)
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

        # Jogador morre:
        if vida <= 0:
            print('Game Over')
            pygame.mixer.music.stop()
            mostrar_game_over(screen, fonte_grande, fonte, fase)
            rodando = False
            return
        
        pygame.display.update()
