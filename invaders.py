#Import packages
import pygame
import sys

# Initialise pygame
pygame.init()
font = pygame.font.SysFont(None, 36)
# Set up screen
width = 1600
height = 1200
screen = pygame.display.set_mode((width, height))
# Initialise variables
running = True
clock = pygame.time.Clock()
player_x = width // 2
player_y = height-(height // 32)
player_speed = 8
bullets = []
bullet_speed = 16
enemies = []
enemy_speed = 4
score = 0
for i in range(12):
    for j in range(5):
        enemies.append([i*128+width/32, j*128+height// 256])
# Initial game loop
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                bullets.append([player_x+32, player_y+32])

        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
        if player_x < 0:
            player_x = width
    if keys[pygame.K_d]:
        player_x += player_speed
        if player_x > width:
            player_x = 0
        
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
    for enemy in enemies:
        enemy[0] += 0
        enemy[1] += enemy_speed
        if enemy[1] > height:
            enemy[1] = 0
            score -= 1
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if abs(bullet[0] - enemy[0]) <= 64 and abs(bullet[1] - enemy[1]) <= 64:
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
        
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (0, 255, 0),  (player_x, player_y, 64, 32))
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], 8, 16))
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], 64, 64))
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.update()
# Exit
pygame.quit()
sys.exit()