import pygame
import sys
import random
import os

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NAVE Y METEOROS")

# Obtén el directorio actual del script
current_directory = os.path.dirname(__file__)

# Cargar imágenes desde la carpeta "sprites"
background_image = pygame.image.load(os.path.join(current_directory, "sprites", "back.jpg"))
player_image = pygame.image.load(os.path.join(current_directory, "sprites", "nave.png"))
meteorite_image = pygame.image.load(os.path.join(current_directory, "sprites", "meteoro.png"))
coin_image = pygame.image.load(os.path.join(current_directory, "sprites", "coin.png"))

# Redimensionar las imágenes según tus necesidades
background_image = pygame.transform.scale(background_image, (400, 300))
player_image = pygame.transform.scale(player_image, (30, 30))  # Ajusta el tamaño del jugador
player_image = pygame.transform.rotate(player_image, -90)        # Rota la imagen del jugador
meteorite_image = pygame.transform.scale(meteorite_image, (30, 30))          # Ajusta el tamaño de los autos
coin_image = pygame.transform.scale(coin_image, (20, 20))        # Ajusta el tamaño de las monedas

# Jugador
player_size = 20
player_x = 20
player_y = HEIGHT // 2
player_speed = 3

# Meteoros
meteorite_size = 20
meteorite_speed = 7
meteorites = []

# Monedas
coin_size = 15
coin_speed = 3
coins = []

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Vidas y monedas
lives = 3
coins_collected = 0

# Tiempo para la generación de monedas
last_coin_spawn_time = pygame.time.get_ticks()

# Función para mostrar el mensaje de inicio
def show_start_message():
    font = pygame.font.Font(None, 20)
    description_text = font.render("Juego infinito, tienes 3 vidas para recolectar monedas", True, (255, 255, 255))
    start_message = font.render("Presiona SPACE para iniciar el juego", True, (255, 255, 255))
    screen.blit(description_text, (WIDTH // 15, HEIGHT // 2.5))
    screen.blit(start_message, (WIDTH // 5, HEIGHT // 2))
    pygame.display.flip()

# Función para dibujar al jugador en la pantalla
def draw_player(x, y):
    screen.blit(player_image, (x, y))

# Función para dibujar los autos en la pantalla
def draw_meteorites(meteorites):
    for meteorite in meteorites:
        screen.blit(meteorite_image, (meteorite.x, meteorite.y))

# Función para dibujar las monedas en la pantalla
def draw_coins(coins):
    for coin in coins:
        screen.blit(coin_image, (coin.x, coin.y))

# Función principal del juego
def game():
    global player_y, meteorites, coins, lives, coins_collected, last_coin_spawn_time
    screen.blit(background_image, (0, 0))
    show_start_message()
    
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_start = False

    while lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Movimiento del jugador
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
            player_y += player_speed

        # Crear autos aleatorios
        if random.random() < 0.01:
            meteorite_y = random.randint(0, HEIGHT - meteorite_size)
            meteorites.append(pygame.Rect(WIDTH, meteorite_y, meteorite_size, meteorite_size))

        # Crear monedas cada 10 segundos
        current_time = pygame.time.get_ticks()
        if current_time - last_coin_spawn_time > 10000:  # 10000 milisegundos = 10 segundos
            coin_y = random.randint(0, HEIGHT - coin_size)
            coins.append(pygame.Rect(WIDTH, coin_y, coin_size, coin_size))
            last_coin_spawn_time = current_time

        # Actualizar la posición de los meteoros
        for meteorite in meteorites:
            meteorite.x -= meteorite_speed

        # Actualizar la posición de las monedas
        for coin in coins:
            coin.x -= coin_speed

        # Eliminar autos que salieron de la pantalla
        meteorites = [meteorite for meteorite in meteorites if meteorite.x > 0]

        # Eliminar monedas que salieron de la pantalla
        coins = [coin for coin in coins if coin.x > 0]

        # Colisiones con los autos
        for meteorite in meteorites:
            if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(meteorite):
                # Restablecer posición del jugador
                player_y = HEIGHT // 2
                # Decrementar vidas
                lives -= 1

        # Colisiones con las monedas
        for coin in coins:
            if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(coin):
                # Eliminar la moneda
                coins.remove(coin)
                # Incrementar contador de monedas recolectadas
                coins_collected += 1

        # Limpiar la pantalla
        screen.blit(background_image, (0, 0))

        # Dibujar al jugador, meteoros y monedas
        draw_player(player_x, player_y)
        draw_meteorites(meteorites)
        draw_coins(coins)

        # Mostrar vidas y monedas recolectadas
        font = pygame.font.Font(None, 20)
        lives_text = font.render("Vidas: " + str(lives), True, (0, 255, 0))
        coins_text = font.render("Monedas: " + str(coins_collected), True, (255, 255, 0))
        screen.blit(lives_text, (10, 10))
        screen.blit(coins_text, (10, 30))

        # Actualizar la pantalla
        pygame.display.flip()

        # Controlar la velocidad de actualización
        clock.tick(150)

    # Mostrar mensaje de fin de juego
    font = pygame.font.Font(None, 20)
    result_text = font.render("¡Has perdido!", True, (255, 0, 0))
    coin = font.render("Obtuviste " + str(coins_collected) + " monedas", True, (255, 255, 0))
    result_text2 = font.render("Presiona SPACE para jugar", True, (255, 0, 0))
    screen.blit(result_text2, (WIDTH // 4, HEIGHT // 2))
    screen.blit(coin, (WIDTH // 3.5, HEIGHT // 1.2))
    screen.blit(result_text, (WIDTH // 2.8, HEIGHT // 2.2))
    
    pygame.display.flip()

    # Esperar a que el usuario presione ESPACIO para reiniciar
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reiniciar juego
                screen.blit(background_image, (0, 0))
                lives = 3
                coins_collected = 0
                player_y = HEIGHT // 2
                meteorites = []
                coins = []
                last_coin_spawn_time = pygame.time.get_ticks()
                waiting_for_restart = False

    # Luego de reiniciar, llamar a la función game nuevamente
    game()

if __name__ == "__main__":
    game()
    pygame.quit()
    sys.exit()
