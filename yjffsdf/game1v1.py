import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение основных цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Определение размеров экрана
WIDTH, HEIGHT = 800, 600
FPS = 30

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Простая игра файтинг на Pygame")
clock = pygame.time.Clock()

# Загрузка изображений персонажей, атаки и блокировки атаки
player1_img = pygame.image.load("player1.png").convert_alpha()
player2_img = pygame.image.load("player2.png").convert_alpha()
attack_img = pygame.image.load("attack.png").convert_alpha()
block_img = pygame.image.load("block.png").convert_alpha()

# Установка размеров персонажей, атаки и блокировки атаки
player1_img = pygame.transform.scale(player1_img, (100, 100))
player2_img = pygame.transform.scale(player2_img, (100, 100))
attack_img = pygame.transform.scale(attack_img, (50, 50))
block_img = pygame.transform.scale(block_img, (50, 50))

# Установка начальных координат персонажей
player1_x, player1_y = 100, HEIGHT // 2
player2_x, player2_y = WIDTH - 200, HEIGHT // 2

# Установка скорости перемещения персонажей
player1_speed = 5
player2_speed = 5

# Установка здоровья персонажей
player1_health = 100
player2_health = 100

# Определение максимального времени между атаками (в кадрах)
ATTACK_COOLDOWN = FPS // 2
player1_attack_timer = 0
player2_attack_timer = 0

# Определение таймеров блокировки атаки для игроков
player1_block_timer = 0
player2_block_timer = 0

# Определение кулдауна для блока атаки
BLOCK_COOLDOWN = FPS * 5

# Определение шрифта для отображения текста
font = pygame.font.SysFont(None, 36)

# Функция отрисовки персонажей и индикаторов здоровья
def draw_players():
    screen.blit(player1_img, (player1_x, player1_y))
    screen.blit(player2_img, (player2_x, player2_y))
    health_text1 = font.render(f"Player 1 Health: {player1_health}", True, RED)
    health_text2 = font.render(f"Player 2 Health: {player2_health}", True, RED)
    screen.blit(health_text1, (20, 20))
    screen.blit(health_text2, (WIDTH - health_text2.get_width() - 20, 20))
    if player1_attack_timer > 0:
        screen.blit(attack_img, (20, 60))
    if player2_attack_timer > 0:
        screen.blit(attack_img, (WIDTH - 70, 60))
    if player1_block_timer > 0:
        screen.blit(block_img, (20, 60))
    if player2_block_timer > 0:
        screen.blit(block_img, (WIDTH - 70, 60))

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление персонажами
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_y -= player1_speed
    if keys[pygame.K_s]:
        player1_y += player1_speed
    if keys[pygame.K_a]:
        player1_x -= player1_speed
    if keys[pygame.K_d]:
        player1_x += player1_speed

    if keys[pygame.K_UP]:
        player2_y -= player2_speed
    if keys[pygame.K_DOWN]:
        player2_y += player2_speed
    if keys[pygame.K_LEFT]:
        player2_x -= player2_speed
    if keys[pygame.K_RIGHT]:
        player2_x += player2_speed

    # Ограничение перемещения персонажей в пределах экрана
    player1_x = max(0, min(WIDTH - 100, player1_x))
    player1_y = max(0, min(HEIGHT - 100, player1_y))
    player2_x = max(0, min(WIDTH - 100, player2_x))
    player2_y = max(0, min(HEIGHT - 100, player2_y))

    # Проверка блокировки атаки для игрока 1
    if player1_block_timer > 0:
        player1_block_timer -= 1
        if player1_block_timer == 0:
            player1_speed = 5  # Восстановление скорости игрока 1
    else:
        # Атака игрока 1
        if keys[pygame.K_LCTRL] and player1_attack_timer <= 0:
            if abs(player1_x - player2_x) < 50 and abs(player1_y - player2_y) < 50:
                player2_health -= 10
                player1_attack_timer = ATTACK_COOLDOWN

    # Проверка блокировки атаки для игрока 2
    if player2_block_timer > 0:
        player2_block_timer -= 1
        if player2_block_timer == 0:
            player2_speed = 5  # Восстановление скорости игрока 2
    else:
        # Атака игрока 2
        if keys[pygame.K_RCTRL] and player2_attack_timer <= 0:
            if abs(player1_x - player2_x) < 50 and abs(player1_y - player2_y) < 50:
                player1_health -= 10
                player2_attack_timer = ATTACK_COOLDOWN

    # Обновление таймеров атаки
    if player1_attack_timer > 0:
        player1_attack_timer -= 1
    if player2_attack_timer > 0:
        player2_attack_timer -= 1

    # Установка блока атаки и кулдауна для игрока 1
    if keys[pygame.K_LSHIFT]:
        player1_block_timer = FPS * 2
        player1_speed = 2  # Замедление скорости игрока 1 на 2 секунды

    # Установка блока атаки и кулдауна для игрока 2
    if keys[pygame.K_RSHIFT]:
        player2_block_timer = FPS * 2
        player2_speed = 2  # Замедление скорости игрока 2 на 2 секунды

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка персонажей и индикаторов здоровья
    draw_players()

    # Проверка на окончание игры (когда здоровье опускается до 0)
    if player1_health <= 0:
        print("Игрок 2 победил!")
        running = False
    elif player2_health <= 0:
        print("Игрок 1 победил!")
        running = False

    # Обновление экрана
    pygame.display.flip()

    # Управление частотой кадров
    clock.tick(FPS)

# Выход из Pygame
pygame.quit()
sys.exit()
