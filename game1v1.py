import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
WIDTH, HEIGHT = 800, 600
FPS = 60

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("негры")
clock = pygame.time.Clock()

# Определение основных цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Загрузка и масштабирование фоновых изображений
backgrounds = [
    pygame.image.load("background1.jpg").convert(),
    pygame.image.load("background2.jpg").convert(),
    pygame.image.load("background3.jpg").convert(),
    pygame.image.load("background4.jpg").convert(),
    pygame.image.load("background5.jpg").convert(),
    pygame.image.load("background6.jpg").convert()
]

# Функция для масштабирования изображения под размеры экрана
def scale_background(image):
    return pygame.transform.scale(image, (WIDTH, HEIGHT))

# Масштабирование всех фоновых изображений
for i in range(len(backgrounds)):
    backgrounds[i] = scale_background(backgrounds[i])

# Выбор случайного фонового изображения
current_background = random.choice(backgrounds)

# Определение размеров персонажей, атаки и блокировки атаки
player_size = (100, 100)
attack_size = (50, 50)

# Загрузка изображений персонажей, атаки и блокировки атаки
player1_img = pygame.image.load("player1.png").convert_alpha()
player2_img = pygame.image.load("player2.png").convert_alpha()
attack_img = pygame.image.load("attack.png").convert_alpha()
block_img = pygame.image.load("block.png").convert_alpha()
sword_img = pygame.image.load("sword.png").convert_alpha()
gun_img = pygame.image.load("gun.png").convert_alpha()

# Установка размеров персонажей, атаки и блокировки атаки
player1_img = pygame.transform.scale(player1_img, player_size)
player2_img = pygame.transform.scale(player2_img, player_size)
attack_img = pygame.transform.scale(attack_img, attack_size)
block_img = pygame.transform.scale(block_img, attack_size)
sword_img = pygame.transform.scale(sword_img, (30, 30))
gun_img = pygame.transform.scale(gun_img, (30, 30))

# Установка начальных координат персонажей
player1_x, player1_y = 100, HEIGHT // 2
player2_x, player2_y = WIDTH - 200, HEIGHT // 2

# Установка скорости перемещения персонажей
player_speed = 5

# Установка здоровья персонажей
player_health = {1: 100, 2: 100}

# Определение максимального времени между атаками (в кадрах)
ATTACK_COOLDOWN = FPS // 3
player_attack_timer = {1: 0, 2: 0}

# Определение таймеров блокировки атаки для игроков
player_block_timer = {1: 0, 2: 0}

# Определение таймеров перезарядки оружия для игроков
player_reload_timer = {1: 0, 2: 0}

# Определение кулдауна для блока атаки
BLOCK_COOLDOWN = FPS * 5

# Определение оружия игроков и его перезарядки
player_weapon = {1: "sword", 2: "sword"}
weapon_reload_time = {"sword": FPS * 0.5, "gun": FPS * 1.5}

# Определение количества патронов у игроков
player_ammo = {1: 10, 2: 10}

# Определение шрифта для отображения текста
font = pygame.font.SysFont(None, 36)

# Флаг для отслеживания состояния меню
main_menu_open = True

# Функция для отрисовки главного меню
def draw_main_menu():
    # Создание поверхности для прозрачного фона главного меню
    menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    menu_surface.fill((0, 0, 0, 128))  # Прозрачный черный цвет для фона
    screen.blit(menu_surface, (0, 0))
    
    title_text = font.render("Главное меню", True, WHITE)
    instruction_text = font.render("Нажмите Enter, чтобы начать игру", True, WHITE)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 2 - 50))
    screen.blit(instruction_text, ((WIDTH - instruction_text.get_width()) // 2, HEIGHT // 2 + 50))

# Функция для отрисовки фона и персонажей
def draw_background_and_players():
    screen.blit(current_background, (0, 0))
    screen.blit(player1_img, (player1_x, player1_y))
    screen.blit(player2_img, (player2_x, player2_y))

# Функция для обработки коллизий между игроками
def check_player_collisions(player1_x, player1_y, player2_x, player2_y, player_size, player_speed):
    player1_rect = pygame.Rect(player1_x, player1_y, player_size[0], player_size[1])
    player2_rect = pygame.Rect(player2_x, player2_y, player_size[0], player_size[1])
    if player1_rect.colliderect(player2_rect):
        # Если есть коллизия, отменим перемещение в этом направлении
        if player1_x < player2_x:
            player1_x -= player_speed
        else:
            player1_x += player_speed
        if player1_y < player2_y:
            player1_y -= player_speed
        else:
            player1_y += player_speed
        if player2_x < player1_x:
            player2_x -= player_speed
        else:
            player2_x += player_speed
        if player2_y < player1_y:
            player2_y -= player_speed
        else:
            player2_y += player_speed

# Основной игровой цикл
running = True
background_change_timer = 0
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Открытие или закрытие главного меню при нажатии Enter
                main_menu_open = not main_menu_open
            elif event.key == pygame.K_1:
                player_weapon[1] = "sword"
            elif event.key == pygame.K_2:
                player_weapon[1] = "gun"
            elif event.key == pygame.K_9:
                player_weapon[2] = "sword"
            elif event.key == pygame.K_0:
                player_weapon[2] = "gun"

    # Если главное меню открыто, отрисовываем его и продолжаем следить за событиями
    if main_menu_open:
        draw_main_menu()
        pygame.display.flip()
        continue

    # Проверка на смену фона каждые 20 секунд (в 60 кадрах в секунду)
    if background_change_timer == FPS * 20:
        current_background = random.choice(backgrounds)
        background_change_timer = 0
    else:
        background_change_timer += 1

        # Управление персонажами
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_y -= player_speed
    if keys[pygame.K_s]:
        player1_y += player_speed
    if keys[pygame.K_a]:
        player1_x -= player_speed
    if keys[pygame.K_d]:
        player1_x += player_speed

    if keys[pygame.K_UP]:
        player2_y -= player_speed
    if keys[pygame.K_DOWN]:
        player2_y += player_speed
    if keys[pygame.K_LEFT]:
        player2_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player2_x += player_speed

    # Ограничение перемещения персонажей в пределах экрана
    player1_x = max(0, min(WIDTH - player_size[0], player1_x))
    player1_y = max(0, min(HEIGHT - player_size[1], player1_y))
    player2_x = max(0, min(WIDTH - player_size[0], player2_x))
    player2_y = max(0, min(HEIGHT - player_size[1], player2_y))

    check_player_collisions(player1_x, player1_y, player2_x, player2_y, player_size, player_speed)

    # Очистка экрана
    screen.fill(BLACK)


    # Отрисовка фона и персонажей
    draw_background_and_players()

    # Отрисовка индикаторов здоровья
    draw_health_indicators()

    # Проверка на окончание игры (когда здоровье опускается до 0)
    if player_health[1] <= 0:
        print("Игрок 2 победил!")
        running = False
    elif player_health[2] <= 0:
        print("Игрок 1 победил!")
        running = False

    # Обновление экрана
    pygame.display.update()

    # Управление частотой кадров
    clock.tick(FPS)

# Выход из Pygame
pygame.quit()
