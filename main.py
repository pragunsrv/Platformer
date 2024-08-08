import pygame
import sys
import random

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
JUMPING_ENEMY_COLOR = (255, 0, 255)
COLLECTIBLE_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
GRAVITY = 0.5
JUMP_STRENGTH = 10
LEVEL_WIDTH = 2000  # Width of each level

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game - Version 8")

# Font for displaying score and level
font = pygame.font.Font(None, 36)

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
        self.score = 0

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
        self.check_collectible_collisions()
        self.check_level_transition()

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

    def check_collectible_collisions(self):
        hits = pygame.sprite.spritecollide(self, collectibles, True)
        for hit in hits:
            self.score += 1

    def check_level_transition(self):
        if self.rect.right > SCREEN_WIDTH - 50:
            if current_level == 1:
                start_level(2)
            elif current_level == 2:
                print("You completed the game!")
                pygame.quit()
                sys.exit()

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Basic Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, move_type='horizontal'):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 2
        self.move_type = move_type
        self.jump_height = 100
        self.jump_speed = 5
        self.initial_y = y

    def update(self):
        if self.move_type == 'horizontal':
            self.rect.x += self.direction * self.speed
            if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
                self.direction *= -1
        elif self.move_type == 'vertical':
            if self.rect.y <= self.initial_y - self.jump_height or self.rect.y >= self.initial_y:
                self.jump_speed *= -1
            self.rect.y += self.jump_speed

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLLECTIBLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Function to start a new level
def start_level(level):
    global current_level
    current_level = level
    all_sprites.empty()
    platforms.empty()
    enemies.empty()
    collectibles.empty()
    if level == 1:
        # Level 1
        platforms.add(Platform(100, 400, 200, 20))
        platforms.add(Platform(400, 300, 200, 20))
        platforms.add(Platform(800, 250, 200, 20))
        platforms.add(Platform(1200, 350, 200, 20))
        platforms.add(Platform(1600, 450, 200, 20))
        all_sprites.add(*platforms)
        enemies.add(Enemy(500, 500, 50, 50, ENEMY_COLOR, 'horizontal'))
        enemies.add(Enemy(700, 300, 50, 50, JUMPING_ENEMY_COLOR, 'vertical'))
        all_sprites.add(*enemies)
        collectibles.add(Collectible(300, 350, 30, 30))
        collectibles.add(Collectible(700, 200, 30, 30))
        collectibles.add(Collectible(1100, 300, 30, 30))
        collectibles.add(Collectible(1500, 400, 30, 30))
        all_sprites.add(*collectibles)
    elif level == 2:
        # Level 2 (more complex or different layout)
        platforms.add(Platform(100, 500, 200, 20))
        platforms.add(Platform(400, 400, 200, 20))
        platforms.add(Platform(800, 300, 200, 20))
        platforms.add(Platform(1200, 200, 200, 20))
        platforms.add(Platform(1600, 100, 200, 20))
        all_sprites.add(*platforms)
        enemies.add(Enemy(500, 550, 50, 50, ENEMY_COLOR, 'horizontal'))
        enemies.add(Enemy(1000, 350, 50, 50, JUMPING_ENEMY_COLOR, 'vertical'))
        all_sprites.add(*enemies)
        collectibles.add(Collectible(300, 450, 30, 30))
        collectibles.add(Collectible(700, 250, 30, 30))
        collectibles.add(Collectible(1100, 200, 30, 30))
        collectibles.add(Collectible(1500, 150, 30, 30))
        all_sprites.add(*collectibles)

# Initialize level
current_level = 1
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Start the first level
start_level(1)

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
camera = Camera(LEVEL_WIDTH, SCREEN_HEIGHT)

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

    # Display the score and level
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {current_level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
