#Import packages
import pygame
import sys
import random
# Initialise pygame
pygame.init()
font = pygame.font.SysFont(None, 36)
# Set up screen
width = 1600
height = 1200
screen = pygame.display.set_mode((width, height))
# Initialise variables
running = True
game_state = "menu"
difficulty = "generic"
clock = pygame.time.Clock()
player_x = width // 2
player_y = height-(height // 32)
player_speed = 8
bullets = []
bullet_speed = 16
enemies = []
enemy_speed = 0
enemy_bullets = []
enemy_bullet_speed = 8
chance = 0
score = 0
for i in range(12):
    for j in range(5):
        enemies.append([i*128+width/32, j*128+height// 256])
# Initial game loop
while running:
    if game_state == "menu":
        screen.fill((0,0,0))
        title = font.render("illegal invaders", True, (0, 255, 0))
        opt_1 = font.render("Press 1 for grandma difficulty", True, (0, 255, 0))
        opt_2 = font.render("Press 2 for generic difficulty", True, (200, 200, 0))
        opt_3 = font.render("Press 3 for literally impossible difficulty", True, (100, 0, 0))
        screen.blit(title, (width//2-150, height // 2-100))
        screen.blit(opt_1, (width//2-150, height // 2+50))
        screen.blit(opt_2, (width//2-150, height // 2+150))
        screen.blit(opt_3, (width//2-150, height // 2+250))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "grandma"
                    game_state = "playing"
                    enemy_speed = 1
                    chance = 0
                if event.key == pygame.K_2:
                    difficulty = "generic"
                    game_state = "playing"
                    enemy_speed = 5
                    chance = 0.001
                if event.key == pygame.K_3:
                    difficulty = "literally impossible"
                    game_state = "playing"
                    enemy_speed = 16
                    chance 0.01


     
    if game_state == "playing":
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
        
        for enemy_bullet in enemy_bullets:
            enemy_bullet[1]  += enemy_bullet_speed
            if enemy_bullet[1] < 0:
                enemy_bullets.remove(enemy_bullet)
        
        
        for enemy in enemies:
            if random.random() < chance:
                enemy_bullets.append([enemy[0]+32,  enemy[1]])

            if difficulty != "literally impossible":
                enemy[0] += enemy_speed
                if enemy[0] > width-40 or enemy[0] < 0:
                    enemy_speed *= -1
                    for enemy in enemies:
                        enemy[1]+=20
                if enemy[1] > height:
                    enemy[1] = 0
                    score -= 1
            else:
                enemy[1] += 5
                if enemy[1] > height:
                    enemy[1] = 0
                    # score -= 1
                    game_state = "game_over"

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
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(screen, (0, 0, 255), (enemy_bullet[0], enemy_bullet[1], 8, 16))
        text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.update()
    
    if game_state == "game_over":
        screen.fill((0, 0, 0,))
        game_over_text = font.render("Congratulations, you just doomed humanity because of your incompetence", True,(100, 0, 0))
        score_text = font.render(f"final score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (20, height // 2 - 100))
        screen.blit(score_text, (width // 2 - 100, height // 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Exit
pygame.quit()
sys.exit()
# may add powerups later