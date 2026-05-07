import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect Coins")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2

velocity_x = 0
velocity_y = 0
acceleration = 0.5
friction = 0.1
max_speed = 7

coin_size = 15
coins = []
for i in range(10):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    coins.append(pygame.Rect(x, y, coin_size*2, coin_size*2))

score = 0
target_score = 5

font = pygame.font.SysFont(None, 40)

running = True
freeze_time = 0

while running:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if freeze_time == 0:
        if keys[pygame.K_LEFT]:
            velocity_x -= acceleration
        if keys[pygame.K_RIGHT]:
            velocity_x += acceleration
        if keys[pygame.K_UP]:
            velocity_y -= acceleration
        if keys[pygame.K_DOWN]:
            velocity_y += acceleration

    velocity_x *= (1 - friction)
    velocity_y *= (1 - friction)

    velocity_x = max(-max_speed, min(max_speed, velocity_x))
    velocity_y = max(-max_speed, min(max_speed, velocity_y))

    player_x += velocity_x
    player_y += velocity_y

    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    player = pygame.Rect(player_x, player_y, player_size, player_size)

    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1
            velocity_x = 0
            velocity_y = 0
            freeze_time = 10  

    if freeze_time > 0:
        freeze_time -= 1

    if score >= target_score:
        running = False

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, player)
    pygame.draw.rect(screen, BLUE, (player_x, player_y + 30, player_size, 20))

    for coin in coins:
        pygame.draw.circle(screen, GOLD, coin.center, coin_size)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

screen.fill(WHITE)
win_text = font.render("You Win!", True, (0, 0, 0))
screen.blit(win_text, (WIDTH//2 - 80, HEIGHT//2))
pygame.display.update()

pygame.time.delay(3000)
pygame.quit()