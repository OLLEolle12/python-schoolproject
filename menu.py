import pygame
import sys

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def show_start(screen):
    screen.fill(BLACK)
    text = font.render("Tryck på valfri tangent för att starta", True, WHITE)
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - 20))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_game_over(screen, winner):
    screen.fill(BLACK)
    msg = f"{winner} vann spelet!"
    text = font.render(msg, True, WHITE)
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - 40))

    tip = small_font.render("Stäng fönstret eller starta om spelet för att spela igen", True, WHITE)
    screen.blit(tip, (screen.get_width()//2 - tip.get_width()//2, screen.get_height()//2 + 10))
    pygame.display.flip()
    pygame.time.wait(4000)
