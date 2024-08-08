import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (0, 128, 255)
PLATFORM_COLOR = (255, 0, 0)
ENEMY_COLOR = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
GRAVITY = 0.5
JUMP_STRENGTH = 10

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game - Version 4")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel_y = 0
        self.on_ground = False

    def update(self):
        self.vel_y += GRAVITY
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_STRENGTH
        self.rect.y += self.vel_y

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.vel_y = 0
        else:
            self.on_ground = False

        self.check_platform_collisions()
        self.check_enemy_collisions()

    def check_platform_collisions(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.rect.bottom = hits[0].rect.top
            self.on_ground = True
            self.vel_y = 0

    def check_enemy_collisions(self):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        if hits:
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.vel_y = 0

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create a player instance
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create platforms
platforms = pygame.sprite.Group()
platform1 = Platform(100, 400, 200, 20)
platform2 = Platform(400, 300, 200, 20)
platform3 = Platform(800, 250, 200, 20)
platform4 = Platform(1200, 350, 200, 20)
platform5 = Platform(1600, 450, 200, 20)
platforms.add(platform1, platform2, platform3, platform4, platform5)
all_sprites.add(platform1, platform2, platform3, platform4, platform5)

# Create enemies
enemies = pygame.sprite.Group()
enemy1 = Enemy(500, 500, 50, 50)
enemies.add(enemy1)
all_sprites.add(enemy1)

# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        x = min(0, x)  # stop scrolling at the left edge
        y = min(0, y)  # stop scrolling at the top edge
        x = max(-(self.width - SCREEN_WIDTH), x)  # stop scrolling at the right edge
        y = max(-(self.height - SCREEN_HEIGHT), y)  # stop scrolling at the bottom edge
        self.camera = pygame.Rect(x, y, self.width, self.height)

# Create a camera instance
camera = Camera(2000, 600)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    camera.update(player)

    screen.fill(BACKGROUND_COLOR)
    for entity in all_sprites:
        screen.blit(entity.image, camera.apply(entity))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
