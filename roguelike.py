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
start_screen = True
# player
player_x = width // 2
player_y = height // 2
player_speed = 10
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
        return {'x': random.randint(0, width), 'y': 0, 'speed': 4, 'health': 1, 'type': 'minion'}
    elif side == 'bottom':
        return {'x': random.randint(0, width), 'y': height, 'speed': 4, 'health': 1, 'type': 'minion'}
    if side == 'left':
        return {'x': 0, 'y': random.randint(0, height), 'speed': 4, 'health': 1, 'type': 'minion'}
    elif side == 'right':
        return {'x': width, 'y': random.randint(0, height), 'speed': 4, 'health': 1, 'type': 'minion'}

def spawn_boss():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'top':
        return {'x': random.randint(0, width), 'y': 0, 'speed': 2, 'health': current_wave, 'type': 'boss'}
    elif side == 'bottom':
        return {'x': random.randint(0, width), 'y': height, 'speed': 2, 'health': current_wave, 'type': 'boss'}
    if side == 'left':
        return {'x': 0, 'y': random.randint(0, height), 'speed': 2, 'health': current_wave, 'type': 'boss'}
    elif side == 'right':
        return {'x': width, 'y': random.randint(0, height), 'speed': 2, 'health': current_wave, 'type': 'boss'}

def reset_game():
    global game_over, player_x, player_y, bullets, enemies, score, current_wave
    game_over = False
    score = 0
    player_x = width // 2
    player_y = height // 2
    bullets = []
    enemies = [spawn_enemy()]
    current_wave = 1


for i in range(1):
    enemies.append(spawn_enemy())

# initial game loop
running = True

while start_screen:
    screen.fill((0,0,0))
    screen.blit(font.render("Press P to play", True, (255, 255, 255)), (width // 3, height // 2))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                start_screen = False

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
                if event.key == pygame.K_k or event.key == pygame.K_SPACE:
                    bullets.append([player_x, player_y, direction[0], direction[1]])
                if game_over and event.key == pygame.K_r:
                    reset_game()
    dx = 0
    dy = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= player_speed
        dx = -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += player_speed
        dx = 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += player_speed
        dy = 1
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= player_speed
        dy = -1
    direction = [dx, dy]
    while direction == [0, 0]:
        direction = [random.randint(-1, 2), random.randint(-1, 2)]
    player_x =  max(0, min(player_x, width - 64))
    player_y = max(0, min(player_y, height - 64))

    if not game_over:
        for enemy in enemies:
            if enemy['x'] < player_x:
                enemy['x'] += enemy['speed']
            elif enemy['x'] > player_x:
                enemy['x'] -= enemy['speed']
            if enemy['y'] < player_y:
                enemy['y'] += enemy['speed']
            elif enemy['y'] > player_y:
                enemy['y'] -= enemy['speed']

        for bullet in bullets[:]:
            bullet[0] -= bullet[2]*bullet_speed
            bullet[1] -= bullet[3]*bullet_speed

            if bullet[0] < 0 or bullet[0] > width or bullet[1] < 0 or bullet[1] > height:
                bullets.remove(bullet)
                continue
            
            for enemy in enemies[:]:
                if abs(bullet[0] - enemy['x']) <= 64 and abs(bullet[1] - enemy['y']) <= 64:
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        continue
                    enemy['health'] -= 1
                    if enemy['health'] == 0:
                        enemies.remove(enemy)
                        score += 1
                    if len(enemies) ==  0:
                        current_wave += 1
                        for i in range(current_wave):
                            enemies.append(spawn_enemy())
                            if (i+1) % 5 == 0 and current_wave % 5 == 0:
                                enemies.append(spawn_boss())
                    break
        for enemy in enemies[:]:
            dif_x = enemy['x'] - (player_x + 32)
            dif_y = enemy['y'] - (player_y + 32)
            distance = math.hypot(dif_x, dif_y)
            dif_angle = abs(math.atan2(dif_y, dif_x) - angle)  % (2 * math.pi)
            if (distance <= radius) and (dif_angle <= math.radians(30)):
                enemy['health'] -= 1
                if enemy['health'] == 0:
                    enemies.remove(enemy)
                    score += 1
                if len(enemies) ==  0:
                    current_wave += 1
                    for i in range(current_wave):
                        enemies.append(spawn_enemy())
                        if (i+1) % 5 == 0 and current_wave %5 == 0:
                            enemies.append(spawn_boss())
                break

        for enemy in enemies[:]:
            if abs(enemy['x'] - player_x) <= 64 and abs(enemy['y'] - player_y) <= 64:
                game_over = True

    pygame.draw.rect(screen, (0, 255, 0),  (player_x, player_y, 64, 64))
    # pygame.draw.rect(screen, (255, 255, 0),  (tip_x-64, tip_y-16, 128, 32))
    pygame.draw.line(screen, (255, 255, 0), (player_x+32, player_y+32), (tip_x, tip_y), 16)

    for enemy in enemies:
        if enemy['type'] == 'minion':
            pygame.draw.rect(screen, (255, 0, 0), (enemy['x'], enemy['y'], 64, 64))
        else:
            pygame.draw.rect(screen, (255, 0, 255), (enemy['x'], enemy['y'], 256, 256))
    for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], 32, 32))

    screen.blit(font.render(f"score: {score}", True, (255,255,255)), (16, 16))
    screen.blit(font.render(f"current wave: {current_wave}", True, (255,255,255)), (512, 16))

    if game_over:
        screen.blit(font.render("doomslayer has been slayed", True, (128,0,0)), (width // 5, height // 2))
        screen.blit(font.render("Press R to restart", True, (255,255,255)), (width // 5, height // 1.5))
        pygame.display.update()
    pygame.display.update()

pygame.quit()
sys.exit()