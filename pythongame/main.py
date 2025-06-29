import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 650
GRID_SIZE = 30
ROWS, COLS = (HEIGHT - 50) // GRID_SIZE, WIDTH // GRID_SIZE


road_vertical = pygame.image.load("road2.png")
road_horizontal = pygame.transform.rotate(road_vertical, 90)
building_sprites = [pygame.image.load(f"building{i}.png") for i in range(1, 3)]


road_vertical = pygame.transform.scale(road_vertical, (GRID_SIZE, GRID_SIZE))
road_horizontal = pygame.transform.scale(road_horizontal, (GRID_SIZE, GRID_SIZE))
building_sprites = [pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE)) for img in building_sprites]


player_img = pygame.image.load("fire_engine.png")
exit_img = pygame.image.load("fire.png")
powerup_img = pygame.image.load("alarm_clock.png")

player_img = pygame.transform.scale(player_img, (GRID_SIZE, GRID_SIZE))
exit_img = pygame.transform.scale(exit_img, (GRID_SIZE, GRID_SIZE))
powerup_img = pygame.transform.scale(powerup_img, (GRID_SIZE, GRID_SIZE))

WHITE, BLACK, PURPLE, YELLOW, GOLD, RED, GREEN = (
    (255, 255, 255), (0, 0, 0), (128, 0, 128), (255, 255, 0), (255, 215, 0), (255, 0, 0), (0, 255, 0)
)


def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_path(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < cols - 1 and 1 <= ny < rows - 1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0
                carve_path(nx, ny)

    maze[1][1] = 0
    carve_path(1, 1)
    return maze


def determine_road_orientation(maze):

    orientations = [[None for _ in range(COLS)] for _ in range(ROWS)]

    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 0:
                up = row > 0 and maze[row - 1][col] == 0
                down = row < ROWS - 1 and maze[row + 1][col] == 0
                left = col > 0 and maze[row][col - 1] == 0
                right = col < COLS - 1 and maze[row][col + 1] == 0

                if (up and down) or (not left and not right):
                    orientations[row][col] = road_vertical
                else:
                    orientations[row][col] = road_horizontal
    return orientations


def find_exit(maze):
    exit_x, exit_y = COLS - 2, ROWS - 2
    while maze[exit_y][exit_x] == 1:
        exit_x, exit_y = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
    return exit_x, exit_y


def spawn_powerup(maze):
    while True:
        x, y = random.randint(1, COLS - 2), random.randint(1, ROWS - 2)
        if maze[y][x] == 0:
            return x, y


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fire Fighter")
font = pygame.font.Font(None, 40)


time_limit = 40
level = 1
lives = 3
powerup_active = True


def draw_timer(remaining_time, level, lives):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
    pygame.draw.rect(screen, YELLOW, (0, 0, WIDTH, 50), 5)
    timer_text = font.render(f"Time: {remaining_time}s", True, RED)
    level_text = font.render(f"Level: {level}", True, RED)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(timer_text, (20, 10))
    screen.blit(level_text, (WIDTH // 2 - 50, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))


def display_message(text, bg_color, text_color):
    screen.fill(WHITE)
    message = font.render(text, True, text_color)
    msg_width, msg_height = message.get_size()
    box_x, box_y = (WIDTH - msg_width) // 2, (HEIGHT - msg_height) // 2
    pygame.draw.rect(screen, bg_color, (box_x - 20, box_y - 10, msg_width + 40, msg_height + 20), border_radius=10)
    pygame.draw.rect(screen, WHITE, (box_x - 20, box_y - 10, msg_width + 40, msg_height + 20), 5, border_radius=10)
    screen.blit(message, (box_x, box_y))
    pygame.display.update()
    time.sleep(3)

display_message("RULES!!", BLACK, WHITE)
display_message("THE TASK IS TO EXTINGUISH THE FIRE", BLACK, WHITE)
display_message("YOU CAN COLLECT THE POWER UPS", BLACK, WHITE)
display_message("YOU HAVE 3 LIVES TO SAVE THE CITY", BLACK, WHITE)
display_message("GAME STARTS", BLACK, WHITE)

pygame.mixer.init()
pygame.mixer.music.load("firetruck2.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
powerup_sound = pygame.mixer.Sound("sound1.wav")
fire_extinguish_sound = pygame.mixer.Sound("water2.mp3")
warning_sound = pygame.mixer.Sound("warning4.mp3")
gameover_sound = pygame.mixer.Sound("gameover.wav.")






def game_loop():
    global level, time_limit, lives, powerup_active
    running = True
    while running:
        MAZE = generate_maze(ROWS, COLS)
        road_orientations = determine_road_orientation(MAZE)
        player_x, player_y = 1, 1
        exit_x, exit_y = find_exit(MAZE)
        powerup_x, powerup_y = spawn_powerup(MAZE)
        powerup_active = True
        start_time = time.time()

        building_background = [[random.choice(building_sprites) for _ in range(COLS)] for _ in range(ROWS)]

        while True:
            pygame.time.delay(100)
            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, time_limit - elapsed_time)

            if remaining_time == 0:
                pygame.mixer.music.stop()
                lives -= 1
                if lives == 0:
                    gameover_sound.play()
                    display_message("FAILED TO EXTINGUISH THE FIRE!", RED, WHITE)
                    display_message("GAME OVER!", RED, WHITE)


                    running = False
                    break
                else:
                    warning_sound.play()





                    display_message("FIRE IS GROWING! ACT FAST!", RED, WHITE)
                    display_message(f"{lives} LIVES REMAINING!!", RED, WHITE)

                    pygame.mixer.music.play(-1)
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            keys = pygame.key.get_pressed()
            new_x, new_y = player_x, player_y
            if keys[pygame.K_LEFT]: new_x -= 1
            if keys[pygame.K_RIGHT]: new_x += 1
            if keys[pygame.K_UP]: new_y -= 1
            if keys[pygame.K_DOWN]: new_y += 1

            if MAZE[new_y][new_x] == 0:
                player_x, player_y = new_x, new_y

            if player_x == exit_x and player_y == exit_y:
                pygame.mixer.music.stop()
                fire_extinguish_sound.play()
                display_message("THE FIRE WAS EXTINGUISHED!", GREEN, BLACK)
                display_message("NEXT LEVEL", GREEN, BLACK)
                level += 1
                time_limit = max(10, time_limit - 5)

                pygame.mixer.music.play(-1)
                break

            if powerup_active and player_x == powerup_x and player_y == powerup_y:
                powerup_sound.play()

                elapsed_time = int(time.time() - start_time)
                time_limit += 13
                start_time = time.time() - elapsed_time

                display_message("+10s Time Boost!", GOLD, BLACK)
                powerup_active = False

            screen.fill(BLACK)
            draw_timer(remaining_time, level, lives)

            for row in range(ROWS):
                for col in range(COLS):
                    screen.blit(building_background[row][col], (col * GRID_SIZE, row * GRID_SIZE + 50))
                    if MAZE[row][col] == 0:
                        screen.blit(road_orientations[row][col], (col * GRID_SIZE, row * GRID_SIZE + 50))

            screen.blit(player_img, (player_x * GRID_SIZE, player_y * GRID_SIZE + 50))
            screen.blit(exit_img, (exit_x * GRID_SIZE, exit_y * GRID_SIZE + 50))

            if powerup_active:
                screen.blit(powerup_img, (powerup_x * GRID_SIZE, powerup_y * GRID_SIZE + 50))



            pygame.display.update()
    pygame.mixer.music.stop()

    pygame.quit()


game_loop()
