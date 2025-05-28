import pygame
import sys
import random
import menu
import hud

# Initiera pygame
pygame.init()

# Skärm
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Skjutspel mot AI")

# Färger
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Spelare & AI
player_radius = 20
player_x = WIDTH // 2
player_y = HEIGHT - 40
player_speed = 5
player_lives = 3

ai_radius = 20
ai_x = WIDTH // 2
ai_y = 40
ai_speed = 3
ai_direction = 1
ai_lives = 3

# Skott
bullet_radius = 5
player_bullets = []
ai_bullets = []
bullet_speed = 7

clock = pygame.time.Clock()

# Visa startmeny
menu.show_start(screen)

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    # Spelarrörelse
    if keys[pygame.K_LEFT] and player_x - player_radius > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_radius < WIDTH:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(player_bullets) < 3:
            player_bullets.append([player_x, player_y - player_radius])

    # AI rörelse
    ai_x += ai_speed * ai_direction
    if ai_x - ai_radius <= 0 or ai_x + ai_radius >= WIDTH:
        ai_direction *= -1

    # AI skjuter slumpmässigt
    if random.randint(1, 60) == 1 and len(ai_bullets) < 3:
        ai_bullets.append([ai_x, ai_y + ai_radius])

    # Flytta och kontrollera spelarens skott
    for bullet in player_bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            player_bullets.remove(bullet)
        elif (ai_x - ai_radius < bullet[0] < ai_x + ai_radius and
              ai_y - ai_radius < bullet[1] < ai_y + ai_radius):
            ai_lives -= 1
            player_bullets.remove(bullet)

    # Flytta och kontrollera AI:s skott
    for bullet in ai_bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] > HEIGHT:
            ai_bullets.remove(bullet)
        elif (player_x - player_radius < bullet[0] < player_x + player_radius and
              player_y - player_radius < bullet[1] < player_y + player_radius):
            player_lives -= 1
            ai_bullets.remove(bullet)

    # Rita spelare och AI
    pygame.draw.circle(screen, BLUE, (player_x, player_y), player_radius)
    pygame.draw.circle(screen, RED, (ai_x, ai_y), ai_radius)

    # Rita skott
    for bullet in player_bullets:
        pygame.draw.circle(screen, WHITE, bullet, bullet_radius)
    for bullet in ai_bullets:
        pygame.draw.circle(screen, WHITE, bullet, bullet_radius)

    # Visa liv
    hud.draw_lives(screen, player_lives, ai_lives)

    # Kontrollera vinst/förlust
    if player_lives <= 0:
        menu.show_game_over(screen, winner="AI")
        running = False
    elif ai_lives <= 0:
        menu.show_game_over(screen, winner="Spelaren")
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
