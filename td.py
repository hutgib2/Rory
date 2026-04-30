#Import packages
import pygame
import sys
import random
import math
# import images
# Initialise pygame
pygame.init()
# font = pygame.SysFont(None, 128)
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
        'health': 1,
        'target': 1
    }

def spawn_tower(x, y):
    return {
        'x': x,
        'y': y, 
        'range': 300,
        'damage': 1,
        'cooldown': 0,
        'fire_rate': 30
    }

def move_enemies():
    for enemy in enemies[:]:
        if enemy['target'] >= len(way_points):
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
    closest = None
    closest_dist = tower['range']
    for enemy in enemies:
        dist = math.hypot(enemy['x'] - tower['x'], enemy['y'] - tower['y'])
        if dist < closest_dist:
            closest = enemy
            closest_dist = dist
    return closest

def fire(tower, target):
    dx = target['x'] - tower['x']
    dy = target['y'] - tower['y']
    dist = math.hypot(dx, dy)
    bullets.append({
        'x': tower['x'],
        'y': tower['y'], 
        'dx': dx / dist,
        'dy': dy / dist,
        'speed': 6,
        'damage': tower['damage']   
    })
    tower['cooldown'] = tower['fire_rate']

def update_bullets():
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

enemies.append(spawn_enemy())
towers.append(spawn_tower(1300, 1200))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    move_enemies()
    update_towers()
    update_bullets()
    screen.fill((0, 0, 0))
    draw_map()
    draw_enemies()
    draw_tower()
    draw_bullets()
    pygame.display.update()