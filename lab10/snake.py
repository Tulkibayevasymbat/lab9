import pygame
import psycopg2
from random import randrange
from config import load_config
import csv

# Глобальные переменные игры
RES = 500
SIZE = 25
x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
snake = [(x, y)]
dx, dy = 0, 0
score = 0
LVL = 1
pygame.init()
import pygame
import sys

# Функция для ввода имени пользователя
def get_username(screen):
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

# Основной цикл игры
def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Enter Your Name')

    username = get_username(screen)
    print('Your username is:', username)

if __name__ == '__main__':
    main()
# Подключение к базе данных
def connect_to_db():
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
        return conn
    except psycopg2.DatabaseError as error:
        print(f'Error connecting to PostgreSQL: {error}')

# Создание таблицы результатов игры в базе данных
def create_game_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_score (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                score INT NOT NULL,
                level INT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        print('Game table created successfully.')
    except psycopg2.DatabaseError as error:
        print(f'Error creating game table: {error}')

# Функция для вставки данных игры в базу данных
def insert_game_data(conn, user_id, score, level):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO user_score (us, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
        conn.commit()
        cur.close()
        print('Game data inserted successfully.')
    except psycopg2.DatabaseError as error:
        print(f'Error inserting game data: {error}')

# Функция для записи данных игры в CSV файл
def write_to_csv(user_id, score, level):
    with open('game_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, score, level])

# Генерация яблок
def generate_apples(num_apples):
    apples = []
    for _ in range(num_apples):
        apple_x, apple_y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
        apples.append((apple_x, apple_y))
    return apples

# Обновление позиций яблок
def update_apples():
    global apples, last_apple_time, apple_spawn_interval
    current_time = pygame.time.get_ticks()
    if current_time - last_apple_time >= apple_spawn_interval:
        apples = generate_apples(3)
        last_apple_time = current_time

# Основной игровой цикл
def main(FPS, user_id):
    global x, y, dx, dy, score, LVL, snake, length, apples, last_apple_time, apple_spawn_interval

    # Подключение к базе данных
    conn = connect_to_db()

    # Создание таблицы результатов игры
    create_game_table(conn)

    sc = pygame.display.set_mode((RES, RES))
    clock = pygame.time.Clock()
    font = pygame.font.Font('pobeda-regular1.ttf', 35)
    eat_sound = pygame.mixer.Sound("eat_sound.wav")

    apples = generate_apples(3)
    length = 1
    last_apple_time = pygame.time.get_ticks()
    apple_spawn_interval = 5000

    while True:
        sc.fill(pygame.Color('black'))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lvl = font.render(f"LVL: {LVL}", True, (255, 255, 255))
        sc.blit(score_text, (20, 20))
        sc.blit(lvl, (400, 20))
        [(pygame.draw.rect(sc, pygame.Color('green'), (i, j, SIZE, SIZE))) for i, j in snake]
        for apple in apples:
            pygame.draw.rect(sc, pygame.Color('red'), (*apple, SIZE, SIZE))

        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]
        pygame.display.flip()
        clock.tick(FPS)

        update_apples()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Закрытие соединения с базой данных перед выходом из игры
                conn.close()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    dx, dy = 0, -1
                elif event.key == pygame.K_s:
                    dx, dy = 0, 1
                elif event.key == pygame.K_a:
                    dx, dy = -1, 0
                elif event.key == pygame.K_d:
                    dx, dy = 1, 0

        for apple in apples:
            if snake[-1] == apple:
                apples.remove(apple)
                length += 1
                score += randrange(1, 3)
                eat_sound.play()
                if score % 4 == 0:
                    LVL += 1
                    FPS += 0.5
                break

        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
            # Вставка данных игры в базу данных перед завершением игры
            insert_game_data(conn, user_id, score, LVL)

            # Запись данных игры в CSV файл перед завершением игры
            write_to_csv(user_id, score, LVL)

            end_text = font.render('Game Over', True, (255, 255, 255))
            sc.blit(end_text, (RES // 2 - end_text.get_width() // 2, RES // 2 - end_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            # Закрытие соединения с базой данных перед выходом из игры
            conn.close()
            pygame.quit()
            exit()

if __name__ == "__main__":
    FPS = 5
    user_id = 1  # Пример идентификатора пользователя
    main(FPS, user_id)