#Import packages
import pygame
import sys
import random
import math
# import images
# Initialise pygame
pygame.init()
game_over = False
# Set up screen
width = 2048
height = 1500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(('Tower defense'))
clock = pygame.time.Clock()
# variables
enemies = []
towers = []
bullets = []
spawn_queue = []
spawn_timer = 0
money = 10
lives = 3
current_wave = 1
spawn_delay = 60

way_points = [
    (0, 1400),
    (1600, 1400),
    (1600, 1000),
    (250, 1000),
    (250, 500),
    (1000, 500),
    (1000, 300),
    (800, 300),
    (800, 100),
    (1000, 100),
    (1000, 0)
]

def draw_map():
    for i in range(len(way_points)-1):
        pygame.draw.line(screen, (0, 255, 255), way_points[i], way_points[i+1], 64)

def spawn_enemy():
    return {
        'x': way_points[0][0],
        'y': way_points[0][1],
        'speed': 1,
        'health': 5,
        'target': 1
    }

def spawn_tower(x, y):
    return {
        'x': x,
        'y': y, 
        'range': 500,
        'damage': 1,
        'cooldown': 0,
        'fire_rate': 16
    }

def move_enemies():
    global lives, money, game_over
    for enemy in enemies[:]:
        if enemy['target'] >= len(way_points):
            lives -= 1
            money += 1
            if lives <= 0:
                game_over = True
            enemies.remove(enemy)
            continue
        tx = way_points[enemy['target']][0]
        ty = way_points[enemy['target']][1]
        dx = tx - enemy['x']
        dy = ty - enemy['y']
        dist = math.hypot(dx, dy)
        if dist < enemy['speed']:
            enemy['target'] += 1
        else:
            enemy['x'] += (dx / dist) * enemy['speed']
            enemy['y'] += (dy / dist) * enemy['speed']

def draw_enemies():
    for enemy in enemies[:]:
        pygame.draw.circle(screen, (255, 0, 0), (int(enemy['x']), int(enemy['y'])), 32)

def draw_tower():
    for tower in towers[:]:
        pygame.draw.rect(screen, (150, 150, 150), (tower['x']-32, tower['y']-32, 64, 64))

def get_target(tower):
    # closest = None
    # closest_dist = tower['range']
    # for enemy in enemies:
    #     dist = math.hypot(enemy['x'] - tower['x'], enemy['y'] - tower['y'])
    #     if dist < closest_dist:
    #         closest = enemy
    #         closest_dist = dist
    # return closest
    furthest = None
    furthest_dist = -1
    for enemy in enemies:
        dist = math.hypot(enemy['x'] - tower['x'], enemy['y'] - tower['y'])
        if dist < tower['range']:
            if enemy['target'] > furthest_dist:
                furthest = enemy
                furthest_dist = enemy['target']
    return furthest

def fire(tower, target):
    dx = target['x'] - tower['x']
    dy = target['y'] - tower['y']
    dist = math.hypot(dx, dy)
    bullets.append({
        'x': tower['x'],
        'y': tower['y'], 
        'dx': dx / dist,
        'dy': dy / dist,
        'speed': 32,
        'damage': tower['damage']   
    })
    tower['cooldown'] = tower['fire_rate']

def update_bullets():
    global money
    for bullet in bullets[:]:
        bullet['x'] += bullet['dx'] * bullet['speed']
        bullet['y'] += bullet['dy'] * bullet['speed']
        if bullet['x'] < 0 or bullet['x'] > width or bullet['y'] < 0 or bullet['y'] > height:
            bullets.remove(bullet)
            continue
        for enemy in enemies[:]:
            dist = math.hypot(bullet['x'] - enemy['x'], bullet['y'] - enemy['y'])
            if dist < 32:
                enemy['health'] -= bullet['damage']
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy['health'] <= 0:
                    enemies.remove(enemy)
                    money += 1
                break

def update_towers():
    for tower in towers[:]:
        if tower['cooldown'] > 0:
            tower['cooldown'] -= 1
            continue
        target = get_target(tower)
        if target:
            fire(tower, target)
        
def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 220, 0), (int(bullet['x']), int(bullet['y'])), 10)

def draw_display():
    font = pygame.font.SysFont(None, 128)
    screen.blit(font.render(f"money: ${money}", True, (255,255,255)), (16, 16))
    screen.blit(font.render(f"current wave: {current_wave}", True, (255,255,255)), (16, 256))
    screen.blit(font.render(f"lives: {lives}", True, (255,255,255)), (16, 136))

def start_wave(wave_number):
    total = wave_number * 5
    for i in range(total):
        spawn_queue.append(spawn_enemy())

def update_spawning():
    global spawn_timer
    if not spawn_queue:
        return
    spawn_timer -= 1

    if spawn_timer <= 0:
        enemies.append(spawn_queue.pop(0))
        spawn_timer = spawn_delay

start_wave(1)
towers.append(spawn_tower(1200, 1200))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not game_over:
        move_enemies()
        update_towers()
        update_bullets()
        update_spawning()
    if not spawn_queue and not enemies and not game_over:
        current_wave += 1
        start_wave(current_wave)
    screen.fill((0, 0, 0))
    draw_map()
    draw_enemies()
    draw_tower()
    draw_bullets()
    draw_display()
    pygame.display.update()