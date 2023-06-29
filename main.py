import random

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0, 0, 255)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player_size = (20, 20)
player = pygame.Surface(player_size)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_right = [1, 0]
player_move_left = [-1, 0]

player_rect.bottom = HEIGHT/2
player_rect.right = WIDTH/2

def  create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.Surface(enemy_size)
    enemy.fill((random.randint(0, 125), random.randint(0, 125), random.randint(0, 125)))
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT +1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

def create_benefit():
    benefit_size = (50, 50)
    benefit = pygame.Surface(benefit_size)
    benefit.fill((random.randint(126, 255), random.randint(126, 255), random.randint(126, 255)))
    benefit_rect = pygame.Rect(random.randint(0, WIDTH), 0, *benefit_size)
    benefit_move = [0, random.randint(1, 5)]
    return [benefit, benefit_rect, benefit_move]

CREATE_BENEFIT = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BENEFIT, 1500)

benefits = []

score = 0

playing = True
while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BENEFIT:
            benefits.append(create_benefit())

    main_display.fill(COLOR_BLACK)

    keys = pygame.key.get_pressed()

    # Керування квадратом
    if keys[K_DOWN]:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP]:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT]:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT]:
        player_rect = player_rect.move(player_move_left)

    # Поведінка при виході за межу екрану
    if player_rect.bottom >= HEIGHT:
        player_rect.bottom = 21

    if player_rect.top <= 0:
        player_rect.top = HEIGHT-20

    if player_rect.right >= WIDTH:
        player_rect.right = 21

    if player_rect.left <= 0:
        player_rect.left = WIDTH-20


    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            # print("Fuck")
            exit()

    for benefit in benefits:
        benefit[1] = benefit[1].move(benefit[2])
        main_display.blit(benefit[0], benefit[1])

        if player_rect.colliderect(benefit[1]):
            score += 1
            benefits.pop(benefits.index(benefit))

    
    main_display.blit(FONT.render(str(score), True, COLOR_WHITE), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    
    # print(len(enemies))
    # print(len(benefits))

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for benefit in benefits:
        if benefit[1].bottom > HEIGHT:
            benefits.pop(benefits.index(benefit))