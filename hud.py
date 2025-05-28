import pygame

font = pygame.font.SysFont(None, 28)
WHITE = (255, 255, 255)

def draw_lives(screen, player_lives, ai_lives):
    player_text = font.render(f"Spelare: {player_lives} ♥", True, WHITE)
    ai_text = font.render(f"AI: {ai_lives} ♥", True, WHITE)
    screen.blit(player_text, (10, screen.get_height() - 30))
    screen.blit(ai_text, (10, 10))
