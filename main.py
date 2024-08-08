import pygame
import sys
import random
import json
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MINI_MAP_WIDTH = 200
MINI_MAP_HEIGHT = 150
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (0, 128, 255)
PLATFORM_COLOR = (255, 0, 0)
ENEMY_COLOR = (255, 255, 0)
BOSS_COLOR = (255, 0, 0)
COLLECTIBLE_COLOR = (0, 255, 0)
POWER_UP_COLOR = (0, 255, 255)
OBSTACLE_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (0, 0, 0)
PLATFORM_MOVE_SPEED = 2
ENEMY_SPEED = 3
GRAVITY = 0.5
JUMP_STRENGTH = 10
LEVEL_WIDTH = 3000
POWER_UP_DURATION = 5000
OBSTACLE_MOVE_SPEED = 2
WEATHER_EFFECT_INTENSITY = 5
WEATHER_EFFECT_COLOR = (0, 0, 255, 100)
DIFFICULTY_LEVEL = 'hard'
LIGHT_INTENSITY = 0.7
SAVE_FILE = 'save_data.json'

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game - Version 18")

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
bosses = pygame.sprite.Group()

# Load and set up the background image
try:
    background = pygame.image.load('background.png')
    background = pygame.transform.scale(background, (LEVEL_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    background = pygame.Surface((LEVEL_WIDTH, SCREEN_HEIGHT))
    background.fill(BACKGROUND_COLOR)

# Font for displaying score, level, health, power-up status, and mini-map
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Procedural generation functions
def generate_level():
    platforms.empty()
    enemies.empty()
    collectibles.empty()
    power_ups.empty()
    obstacles.empty()
    bosses.empty()

    for _ in range(random.randint(5, 10)):
        x = random.randint(0, LEVEL_WIDTH - 100)
        y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 50)
        platforms.add(Platform(x, y, random.randint(100, 200), 20))

    for _ in range(random.randint(3, 6)):
        x = random.randint(0, LEVEL_WIDTH - 50)
        y = random.randint(0, SCREEN_HEIGHT - 50)
        enemies.add(AdvancedEnemy(x, y, 50, 50))

    for _ in range(random.randint(2, 5)):
        x = random.randint(0, LEVEL_WIDTH - 30)
        y = random.randint(0, SCREEN_HEIGHT - 30)
        collectibles.add(Collectible(x, y, 30, 30))

    for _ in range(random.randint(2, 4)):
        x = random.randint(0, LEVEL_WIDTH - 30)
        y = random.randint(0, SCREEN_HEIGHT - 30)
        power_ups.add(PowerUp(x, y, 30, 30, 'invincibility'))

    for _ in range(random.randint(1, 3)):
        x = random.randint(0, LEVEL_WIDTH - 50)
        y = random.randint(0, SCREEN_HEIGHT - 50)
        obstacles.add(Obstacle(x, y, 50, 50))

    if random.choice([True, False]):
        x = random.randint(0, LEVEL_WIDTH - 100)
        y = random.randint(0, SCREEN_HEIGHT - 100)
        bosses.add(FinalBoss(x, y, 100, 100))

    return platforms, enemies, collectibles, power_ups, obstacles, bosses

# Save and load functions
def save_game(player):
    data = {
        'player': {
            'x': player.rect.x,
            'y': player.rect.y,
            'score': player.score,
            'health': player.health,
            'extra_lives': player.extra_lives,
            'achievements': player.achievements
        }
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        return data
    return None

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
        self.health = 100
        self.invincible = False
        self.invincible_timer = 0
        self.extra_lives = 0
        self.achievements = []

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
        self.check_boss_collisions()
        self.check_power_up_collisions()
        self.check_obstacle_collisions()
        self.check_level_transition()
        self.check_achievements()

        if self.invincible:
            if pygame.time.get_ticks() - self.invincible_timer > POWER_UP_DURATION:
                self.invincible = False

    def check_platform_collisions(self):
        pass

    def check_enemy_collisions(self):
        pass

    def check_collectible_collisions(self):
        pass

    def check_boss_collisions(self):
        pass

    def check_power_up_collisions(self):
        pass

    def check_obstacle_collisions(self):
        pass

    def check_level_transition(self):
        pass

    def check_achievements(self):
        pass

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, move_type=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.move_type = move_type
        self.original_y = y
        self.original_x = x
        self.move_speed = PLATFORM_MOVE_SPEED
        self.direction = 1

    def update(self):
        if self.move_type == 'horizontal':
            self.rect.x += self.direction * self.move_speed
            if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
                self.direction *= -1
        elif self.move_type == 'vertical':
            self.rect.y += self.direction * self.move_speed
            if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.direction *= -1

# Advanced Enemy class
class AdvancedEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.move_speed = ENEMY_SPEED
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * self.move_speed
        if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
            self.direction *= -1

# Boss class
class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BOSS_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 1000
        self.move_speed = 4
        self.direction = 1
        self.attack_pattern = 'complex'

    def update(self):
        self.rect.x += self.direction * self.move_speed
        if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
            self.direction *= -1

        if self.attack_pattern == 'complex':
            # Complex behavior for final boss
            pass

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLLECTIBLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, power_type):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(POWER_UP_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.power_type = power_type

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

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

# Initialize the player and level
player = Player()

def start_level(level):
    global platforms, enemies, collectibles, power_ups, obstacles, bosses
    platforms, enemies, collectibles, power_ups, obstacles, bosses = generate_level()
    all_sprites.empty()
    all_sprites.add(*platforms, *enemies, *collectibles, *power_ups, *obstacles, *bosses, player)

current_level = 1
start_level(current_level)

# Create a camera instance
camera = Camera(LEVEL_WIDTH, SCREEN_HEIGHT)

# Function to draw the mini-map
def draw_mini_map():
    mini_map_surface = pygame.Surface((MINI_MAP_WIDTH, MINI_MAP_HEIGHT))
    mini_map_surface.fill((0, 0, 0))
    for entity in all_sprites:
        if isinstance(entity, Platform):
            pygame.draw.rect(mini_map_surface, PLATFORM_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10,
                              entity.rect.width // 10, entity.rect.height // 10))
        elif isinstance(entity, Player):
            pygame.draw.rect(mini_map_surface, PLAYER_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10,
                              entity.rect.width // 10, entity.rect.height // 10))
        elif isinstance(entity, FinalBoss):
            pygame.draw.rect(mini_map_surface, BOSS_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10,
                              entity.rect.width // 10, entity.rect.height // 10))
    screen.blit(pygame.transform.scale(mini_map_surface, (MINI_MAP_WIDTH * 2, MINI_MAP_HEIGHT * 2)), (0, SCREEN_HEIGHT - MINI_MAP_HEIGHT * 2))

# Function to draw weather effects
def draw_weather_effects():
    for _ in range(WEATHER_EFFECT_INTENSITY):
        pygame.draw.line(screen, WEATHER_EFFECT_COLOR,
                         (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
                         (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), 1)

# Function to draw the HUD
def draw_hud():
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    extra_lives_text = font.render(f"Extra Lives: {player.extra_lives}", True, (255, 255, 255))
    achievements_text = large_font.render(f"Achievements: {', '.join(player.achievements)}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    screen.blit(extra_lives_text, (10, 90))
    screen.blit(achievements_text, (10, SCREEN_HEIGHT - 100))

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(player)
            pygame.quit()
            sys.exit()

    all_sprites.update()
    camera.update(player)

    screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0), pygame.Rect(camera.camera.left, camera.camera.top, SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_weather_effects()
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))
    draw_mini_map()
    draw_hud()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
