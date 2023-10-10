import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 400, 400

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Начальные координаты и размеры змейки
snake_x, snake_y = WIDTH // 2, HEIGHT // 2
snake_size = 20

# Начальное направление движения
direction = "RIGHT"

# Скорость змейки
speed = 10

# Начальная длина змейки
snake_length = 1
snake_coords = [(snake_x, snake_y)]

# Координаты еды
food_x, food_y = random.randint(0, WIDTH // snake_size - 1) * snake_size, random.randint(0, HEIGHT // snake_size - 1) * snake_size

# Счет
score = 0

# Уровень сложности
level = 1

# Состояния игры
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
state = MENU

# Функция для отображения текста
def message(msg, color, y_offset=0):
    font = pygame.font.Font(None, 36)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

# Главное меню
def main_menu():
    screen.fill(WHITE)
    message("Змейка", GREEN, -50)
    message("Нажмите ПРОБЕЛ, чтобы начать", GREEN, 50)

# Игровой цикл
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if state == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = PLAYING
        elif state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                if event.key == pygame.K_PLUS:
                    speed += 1
                if event.key == pygame.K_MINUS:
                    speed -= 1
                if event.key == pygame.K_p:
                    state = PAUSED
        elif state == PAUSED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                state = PLAYING
        elif state == GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = MENU
                snake_x, snake_y = WIDTH // 2, HEIGHT // 2
                direction = "RIGHT"
                speed = 10
                snake_length = 1
                snake_coords = [(snake_x, snake_y)]
                food_x, food_y = random.randint(0, WIDTH // snake_size - 1) * snake_size, random.randint(0, HEIGHT // snake_size - 1) * snake_size
                score = 0
                level = 1

    # Игровая логика
    if state == PLAYING:
        # Движение змейки
        if direction == "UP":
            snake_y -= speed
        if direction == "DOWN":
            snake_y += speed
        if direction == "LEFT":
            snake_x -= speed
        if direction == "RIGHT":
            snake_x += speed

        # Проверка на столкновение с границами
        if snake_x >= WIDTH or snake_x < 0 or snake_y >= HEIGHT or snake_y < 0:
            state = GAME_OVER

        # Проверка на столкновение с самой собой
        if (snake_x, snake_y) in snake_coords[:-1]:
            state = GAME_OVER

        # Добавление новой головы
        snake_coords.append((snake_x, snake_y))

        # Урезание хвоста
        if len(snake_coords) > snake_length:
            del snake_coords[0]

        # Проверка на съедание еды
        if snake_x == food_x and snake_y == food_y:
            snake_length += 1
            score += 1
            food_x, food_y = random.randint(0, WIDTH // snake_size - 1) * snake_size, random.randint(0, HEIGHT // snake_size - 1) * snake_size

            # Переход на следующий уровень каждые 5 съеденных кроликов
            if score % 5 == 0:
                level += 1
                speed += 1

    # Отрисовка игрового поля
    screen.fill(WHITE)

    # Отрисовка змейки
    for segment in snake_coords:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], snake_size, snake_size])

    # Отрисовка еды
    pygame.draw.rect(screen, RED, [food_x, food_y, snake_size, snake_size])

    if state == MENU:
        main_menu()
    elif state == GAME_OVER:
        message("Игра окончена", RED, -50)
        message("Нажмите ПРОБЕЛ, чтобы вернуться в меню", GREEN, 50)

    # Отображение счета и уровня
    message(f"Счет: {score}", GREEN, -190)
    message(f"Уровень: {level}", GREEN, -150)

    if state == PLAYING:
        message("Нажмите P для паузы", GREEN, 190)

    pygame.display.update()

    pygame.time.Clock().tick(20)

# Завершение игры
pygame.quit()
quit()
