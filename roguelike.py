#Import packages
import pygame
import sys
import random
import math
# import images
# Initialise pygame
pygame.init()
game_over = False
font = pygame.font.SysFont(None, 128)
# Set up screen
width = 2000
height = 1440
screen = pygame.display.set_mode((width, height))
# Initialise variables
running = True
clock = pygame.time.Clock()
score = 0
angle = 0
radius = 200
# player
player_x = width // 2
player_y = height // 2
player_speed = 16
direction = (0, -1)
dx = 1
dy = 0
# bullets
bullets = []
bullet_speed = 32
# demons
enemies = []
enemy_speed = 8
current_wave = 1

def spawn_enemy():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'top':
        return [random.randint(0, width), 0]
    elif side == 'bottom':
        return [random.randint(0, width), height]
    if side == 'left':
        return [0, random.randint(0, height)]
    elif side == 'right':
        return [width, random.randint(0, height)]

def reset_game():
    global game_over, font, width, height, screen, running, clock, score, player_x, player_y, player_speed, direction, dx, dy, bullets, bullet_speed, enemies, enemy_speed, current_wave
    game_over = False
    font = pygame.font.SysFont(None, 128)
    # Set up screen
    width = 2000
    height = 1440
    screen = pygame.display.set_mode((width, height))
    # Initialise variables
    running = True
    clock = pygame.time.Clock()
    score = 0
    # player
    player_x = width // 2
    player_y = height // 2
    player_speed = 16
    direction = (0, -1)
    dx = 1
    dy = 0
    # bullets
    bullets = []
    bullet_speed = 32
    # demons
    enemies = []
    enemy_speed = 8
    current_wave = 1
    for i in range(1):
        enemies.append(spawn_enemy())

for i in range(1):
    enemies.append(spawn_enemy())

# initial game loop
running = True

while running:
    clock.tick(60)
    screen.fill((0,0,0))
    angle += 0.1
    tip_x = player_x + 32 + radius * math.cos(angle)
    tip_y = player_y + 32 + radius * math.sin(angle)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    bullets.append([player_x, player_y, direction[0], direction[1]])
                if game_over and event.key == pygame.K_r:
                    reset_game()
    dx = 0
    dy = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
        dx = -1
    if keys[pygame.K_d]:
        player_x += player_speed
        dx = 1
    if keys[pygame.K_s]:
        player_y += player_speed
        dy = 1
    if keys[pygame.K_w]:
        player_y -= player_speed
        dy = -1
    direction = [dx, dy]
    while direction == [0, 0]:
        direction = [random.randint(-1, 2), random.randint(-1, 2)]
    player_x =  max(0, min(player_x, width - 64))
    player_y = max(0, min(player_y, height - 64))

    if not game_over:
        for enemy in enemies:
            if enemy[0] < player_x:
                enemy[0] += enemy_speed
            elif enemy[0] > player_x:
                enemy[0] -= enemy_speed
            if enemy[1] < player_y:
                enemy[1] += enemy_speed
            elif enemy[1] > player_y:
                enemy[1] -= enemy_speed

        for bullet in bullets[:]:
            bullet[0] -= bullet[2]*bullet_speed
            bullet[1] -= bullet[3]*bullet_speed

            if bullet[0] < 0 or bullet[0] > width or bullet[1] < 0 or bullet[1] > height:
                bullets.remove(bullet)
                continue
            
            for enemy in enemies[:]:
                if abs(bullet[0] - enemy[0]) <= 64 and abs(bullet[1] - enemy[1]) <= 64:
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        continue
                    enemies.remove(enemy)
                    score += 1
                    if len(enemies) ==  0:
                        current_wave += 1
                        for i in range(current_wave):
                            enemies.append(spawn_enemy())
                    break
        for enemy in enemies[:]:
            dif_x = enemy[0] - (player_x + 32)
            dif_y = enemy[1] - (player_y + 32)
            distance = math.hypot(dif_x, dif_y)
            dif_angle = abs(math.atan2(dif_y, dif_x) - angle)  % (2 * math.pi)
            if (distance <= radius) and (dif_angle <= math.radians(30)):
                enemies.remove(enemy)
                score += 1
                if len(enemies) ==  0:
                    current_wave += 1
                    for i in range(current_wave):
                        enemies.append(spawn_enemy())
                break

        for enemy in enemies[:]:
            if abs(enemy[0] - player_x) <= 64 and abs(enemy[1] - player_y) <= 64:
                game_over = True

    pygame.draw.rect(screen, (0, 255, 0),  (player_x, player_y, 64, 64))
    # pygame.draw.rect(screen, (255, 255, 0),  (tip_x-64, tip_y-16, 128, 32))
    pygame.draw.line(screen, (255, 255, 0), (player_x+32, player_y+32), (tip_x, tip_y), 16)

    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], 64, 64))

    for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], 32, 32))

    screen.blit(font.render(f"score: {score}", True, (255,255,255)), (16, 16))
    screen.blit(font.render(f"current wave: {current_wave}", True, (255,255,255)), (512, 16))

    if game_over:
        screen.blit(font.render("doomslayer has been slayed", True, (128,0,0)), (width // 5, height // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False
    pygame.display.update()

pygame.quit()
sys.exit()