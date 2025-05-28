import pygame
import random
import sys

# Initiera Pygame och fontmodulen
pygame.init()
pygame.font.init()

# Skärmstorlek
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Skjutspel mot AI")

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Spelarens klass
class Player:
    def __init__(self):
        self.radius = 20
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.speed = 5
        self.color = GREEN
        self.bullets = []

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.radius > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.radius < WIDTH:
            self.x += self.speed

    def shoot(self):
        bullet = Bullet(self.x, self.y - self.radius)
        self.bullets.append(bullet)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        for bullet in self.bullets:
            bullet.draw()

# Fiende (AI)
class Enemy:
    def __init__(self):
        self.radius = 20
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = 50
        self.speed = 3
        self.color = RED
        self.direction = 1  # 1 = höger, -1 = vänster

    def move(self):
        self.x += self.speed * self.direction
        # Byt riktning vid kanterna
        if self.x + self.radius >= WIDTH or self.x - self.radius <= 0:
            self.direction *= -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Skott
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.radius = 5
        self.color = WHITE

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Kollision mellan två cirklar
def is_collision(x1, y1, r1, x2, y2, r2):
    distance = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    return distance < r1 + r2

def main():
    player = Player()
    enemy = Enemy()

    font = pygame.font.SysFont("Arial", 30)
    game_over = False
    win = False

    shoot_cooldown = 0  # för att inte skjuta för ofta

    while True:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)

            # Skjut när mellanslag trycks, med cooldown
            if keys[pygame.K_SPACE] and shoot_cooldown == 0:
                player.shoot()
                shoot_cooldown = 15  # frames cooldown

            if shoot_cooldown > 0:
                shoot_cooldown -= 1

            enemy.move()

            # Flytta och kolla kollision på skott
            for bullet in player.bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    player.bullets.remove(bullet)
                elif is_collision(bullet.x, bullet.y, bullet.radius,
                                  enemy.x, enemy.y, enemy.radius):
                    player.bullets.remove(bullet)
                    game_over = True
                    win = True

            # Rita spelare och fiende
            player.draw()
            enemy.draw()

            # Visa instruktioner
            text = font.render("Vänster/Höger: Flytta  Mellanslag: Skjut", True, WHITE)
            screen.blit(text, (10, HEIGHT - 40))
        else:
            if win:
                msg = "Du vann! Tryck ESC för att avsluta."
            else:
                msg = "Game Over! Tryck ESC för att avsluta."
            text = font.render(msg, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()
