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
player_health = 3
powerups = []
active_effects = {}
# player
player_x = width // 2
player_y = height // 2
player_speed = 8
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
invincible_timer = 0
last_idle_direction = (0,0)

def spawn_enemy():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'top':
        return {'x': random.randint(0, width), 'y': 0, 'speed': 4, 'health': 1, 'type': 'minion', 'size': 64}
    elif side == 'bottom':
        return {'x': random.randint(0, width), 'y': height, 'speed': 4, 'health': 1, 'type': 'minion', 'size': 64}
    if side == 'left':
        return {'x': 0, 'y': random.randint(0, height), 'speed': 4, 'health': 1, 'type': 'minion', 'size': 64}
    elif side == 'right':
        return {'x': width, 'y': random.randint(0, height), 'speed': 4, 'health': 1, 'type': 'minion', 'size': 64}

def spawn_boss():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'top':
        return {'x': random.randint(0, width), 'y': 0, 'speed': 2, 'health': current_wave, 'type': 'boss', 'size': 256}
    elif side == 'bottom':
        return {'x': random.randint(0, width), 'y': height, 'speed': 2, 'health': current_wave, 'type': 'boss', 'size': 256}
    if side == 'left':
        return {'x': 0, 'y': random.randint(0, height), 'speed': 2, 'health': current_wave, 'type': 'boss', 'size': 256}
    elif side == 'right':
        return {'x': width, 'y': random.randint(0, height), 'speed': 2, 'health': current_wave, 'type': 'boss', 'size': 256}

def spawn_mob():
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'top':
        return {'x': random.randint(0, width), 'y': 0, 'speed': 10, 'health': 1, 'type': 'mob', 'size': 32}
    elif side == 'bottom':
        return {'x': random.randint(0, width), 'y': height, 'speed': 10, 'health': 1, 'type': 'mob', 'size': 32}
    if side == 'left':
        return {'x': 0, 'y': random.randint(0, height), 'speed': 10, 'health': 1, 'type': 'mob', 'size': 32}
    elif side == 'right':
        return {'x': width, 'y': random.randint(0, height), 'speed': 10, 'health': 1, 'type': 'mob', 'size': 32}

def spawn_powerup(enemy):
    ptype = random.choices(['speed boost', 'nuke', 'long reach', 'rear shot', 'side shot', 'shotgun'], weights = [20, 20, 20, 20, 20, 20])[0]
    if ptype == 'speed boost':
        return {'type': 'speed boost', 'x': enemy['x'], 'y': enemy['y'], 'timer': 1000}
    if ptype == 'nuke':
        return {'type': 'nuke', 'x': enemy['x'], 'y': enemy['y'], 'timer': 1000}
    if ptype == 'long reach':
        return {'type': 'long reach', 'x': enemy['x'], 'y': enemy['y'], 'timer': 1000}
    if ptype == 'rear shot':
        return {'type': 'rear shot', 'x': enemy['x'], 'y': enemy['y'], 'timer': 1000}
    if ptype == 'side shot':
        return {'type': 'side shot', 'x': enemy['x'], 'y': enemy['y'], 'timer': 1000}
    if ptype == 'shotgun':
        return {'type': 'shotgun', 'x': enemy['x'], 'y': enemy['y'], 'timer': 1000}

def apply_powerup(ptype):
    global player_speed, score, enemies, radius
    if ptype == 'speed boost':
        player_speed = 16
        active_effects[ptype] = 300
    if ptype == 'nuke':
        score += len(enemies)
        enemies = []
        next_wave()
    if ptype == 'long reach':
        radius = 600
        active_effects[ptype] = 300
    if ptype == 'rear shot':
        active_effects[ptype] = 300
    if ptype == 'side shot':
        active_effects[ptype] = 300
    if ptype == 'shotgun':
        active_effects[ptype] = 300

def remove_powerup(ptype):
    global player_speed, radius
    if ptype == 'speed boost':
        player_speed = 8
    if ptype == 'long reach':
        radius = 200

def choose_direction():
    global direction, last_idle_direction
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
    while direction == [0, 0] or direction == last_idle_direction:
        direction = random.choice(directions)
    last_idle_direction = direction

def kill_enemy(enemy):
    global score
    score += 1
    if random.random() <= 0.025:
        powerups.append(spawn_powerup(enemy))
    enemies.remove(enemy)

def next_wave():
    global current_wave, player_health, player_x, player_y
    current_wave += 1
    player_x = width // 2
    player_y = height // 2
    if player_health < 3:
        player_health += 1
    for i in range(current_wave):
        enemies.append(spawn_enemy())
        if i == 0 and current_wave %5 == 0:
            enemies.append(spawn_boss())
        if (i+1) % 3 == 0 and current_wave %3 == 0:
            enemies.append(spawn_mob())

def colliding(ax, ay, asize, bx, by, bsize):
    center_ax = ax+asize // 2
    center_ay = ay+asize // 2
    center_bx  = bx+bsize // 2
    center_by = by+bsize // 2
    if abs(center_ax-center_bx) <= (asize+bsize) // 2 and abs(center_ay-center_by) <= (asize+bsize) // 2:
        return True
    else:
        return False

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(new_score):
    with open("highscore.txt", "w") as file:
        file.write(str(new_score))

highscore = load_high_score()

def reset_game():
    global game_over, player_x, player_y, bullets, enemies, score, current_wave, player_health, invincible_timer
    game_over = False
    score = 0
    player_x = width // 2
    player_y = height // 2
    bullets = []
    enemies = [spawn_enemy()]
    current_wave = 1
    player_health = 3
    invincible_timer = 0


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
    if invincible_timer > 0:
        invincible_timer -= 1
    screen.fill((0,0,0))
    
    # SWORD
    angle += 0.1
    tip_x = player_x + 32 + radius * math.cos(angle)
    tip_y = player_y + 32 + radius * math.sin(angle)
    
    # INPUTS
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k or event.key == pygame.K_SPACE:
                    direction = [dx, dy]
                    if direction == [0,0]:
                        choose_direction()
                    if 'rear shot' in active_effects:
                        bullets.append([player_x, player_y, -direction[0], -direction[1]])
                    if 'side shot' in active_effects:
                        bullets.append([player_x, player_y, direction[1], direction[0]])
                        bullets.append([player_x, player_y, -direction[1], -direction[0]])
                    if 'shotgun' in active_effects:
                        for sign in [-1, 1]:
                            offset = sign*math.radians(30)
                            new_dx = dx*math.cos(offset) - dy*math.sin(offset)
                            new_dy = dx*math.sin(offset) + dy*math.cos(offset)
                            bullets.append([player_x, player_y, new_dx, new_dy])
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
    player_x =  max(0, min(player_x, width - 64))
    player_y = max(0, min(player_y, height - 64))

    if not game_over:

# MOVE ENEMIES
        for enemy in enemies:
            if enemy['x'] < player_x:
                enemy['x'] += enemy['speed']
            elif enemy['x'] > player_x:
                enemy['x'] -= enemy['speed']
            if enemy['y'] < player_y:
                enemy['y'] += enemy['speed']
            elif enemy['y'] > player_y:
                enemy['y'] -= enemy['speed']

# POWERUPS
        for powerup in powerups[:]:
            powerup['timer'] -= 1
            if powerup['timer'] == 0:
                powerups.remove(powerup)
                continue
            if colliding(player_x, player_y, 64, powerup['x'], powerup['y'], 32):
                apply_powerup(powerup['type'])
                powerups.remove(powerup)

        for effect in list(active_effects.keys()):
            active_effects[effect] -= 1
            if active_effects[effect] <= 0:
                remove_powerup(effect)
                del active_effects[effect]
            
# MOVE BULLETS
        for bullet in bullets[:]:
            bullet[0] -= bullet[2]*bullet_speed
            bullet[1] -= bullet[3]*bullet_speed

            if bullet[0] < 0 or bullet[0] > width or bullet[1] < 0 or bullet[1] > height:
                bullets.remove(bullet)
                continue
# COLLISIONS
    # ENEMY AND BULLET            
            for enemy in enemies[:]:
                if colliding(bullet[0], bullet[1], 32, enemy['x'], enemy['y'], enemy['size']):
                    try:
                        bullets.remove(bullet)
                    except ValueError:
                        continue
                    enemy['health'] -= 1
                    if enemy['health'] == 0:
                        kill_enemy(enemy)
                    if len(enemies) ==  0:
                        next_wave()
                    break

    # ENEMY AND SWORD                    
        for enemy in enemies[:]:
            dif_x = enemy['x'] - (player_x + 32)
            dif_y = enemy['y'] - (player_y + 32)
            distance = math.hypot(dif_x, dif_y)
            dif_angle = abs(math.atan2(dif_y, dif_x) - angle)  % (2 * math.pi)
            if (distance <= radius) and (dif_angle <= math.radians(30)) and enemy['type'] != 'boss':
                enemy['health'] -= 1
                if enemy['health'] == 0:
                    kill_enemy(enemy)
                if len(enemies) ==  0:
                    next_wave()
                break

    # ENEMY AND PLAYER
        for enemy in enemies[:]:
            if colliding(player_x, player_y, 64, enemy['x'], enemy['y'], enemy['size']) and invincible_timer == 0:
                player_health -= 1
                invincible_timer = 60
                if player_health <= 0:
                    game_over = True

# DRAWING
    # HEALTH BAR
    pygame.draw.rect(screen, (255, 0, 0), (16, 100, 600, 40))
    pygame.draw.rect(screen, (0, 255, 0), (16, 100, int(600*(player_health / 3)), 40))

    # PLAYER
    if invincible_timer == 0 or invincible_timer % 10 < 5:
        pygame.draw.rect(screen, (0, 255, 0),  (player_x, player_y, 64, 64))
        pygame.draw.line(screen, (255, 255, 0), (player_x+32, player_y+32), (tip_x, tip_y), 16)

    # ENEMIES
    for enemy in enemies:
        if enemy['type'] == 'minion':
            pygame.draw.rect(screen, (255, 0, 0), (enemy['x'], enemy['y'], 64, 64))
        elif enemy['type'] == 'mob':
            pygame.draw.rect(screen, (0, 255, 255), (enemy['x'], enemy['y'], 32, 32))
        else:
            pygame.draw.rect(screen, (255, 0, 255), (enemy['x'], enemy['y'], 64 + 192*(enemy['health']/current_wave), 64 + 192*(enemy['health']/current_wave)))
    # BULLETS
    for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], 32, 32))
    # POWERUPS
    for powerup in powerups:
        if powerup['type'] == 'speed boost':
            pygame.draw.circle(screen, (80, 255, 80), (powerup['x'], powerup['y']), 20)  # greenish
        if powerup['type'] == 'nuke':
            pygame.draw.circle(screen, (255, 0, 255), (powerup['x'], powerup['y']), 20) # purple
        if powerup['type'] == 'long reach':
            pygame.draw.circle(screen, (150, 75, 0), (powerup['x'], powerup['y']), 20) # brown
        if powerup['type'] == 'rear shot':
            pygame.draw.circle(screen, (255, 165, 0), (powerup['x'], powerup['y']), 20) # orange
        if powerup['type'] == 'side shot':
            pygame.draw.circle(screen, (100, 0, 100), (powerup['x'], powerup['y']), 20) # dark purple
        if powerup['type'] == 'shotgun':
            pygame.draw.circle(screen, (255, 192, 203), (powerup['x'], powerup['y']), 20) # pink

    # SCORES
    screen.blit(font.render(f"score: {score}", True, (255,255,255)), (16, 16))
    screen.blit(font.render(f"current wave: {current_wave}", True, (255,255,255)), (512, 16))
    screen.blit(font.render(f"high score: {max(highscore,score)}", True, (255,255,255)), (1280, 16))

    # HIGHSCORE
    if game_over:
        if score > highscore:
            highscore = score
            save_high_score(score)
        screen.blit(font.render("doomslayer has been slayed", True, (128,0,0)), (width // 5, height // 2))
        screen.blit(font.render("Press R to restart", True, (255,255,255)), (width // 5, height // 1.5))
        pygame.display.update()
    pygame.display.update()

pygame.quit()
sys.exit()