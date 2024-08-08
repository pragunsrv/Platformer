import pygame
import sys
import random

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
LEVEL_WIDTH = 3000  # Width of each level
POWER_UP_DURATION = 5000  # Duration of power-ups in milliseconds
OBSTACLE_MOVE_SPEED = 2

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game - Version 13")

# Load and set up the background image
background = pygame.image.load('background.png')  # Use an actual image file in practice
background = pygame.transform.scale(background, (LEVEL_WIDTH, SCREEN_HEIGHT))

# Font for displaying score, level, health, power-up status, and mini-map
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
        self.health = 100  # Player health
        self.invincible = False
        self.invincible_timer = 0
        self.extra_lives = 0

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

        if self.invincible:
            if pygame.time.get_ticks() - self.invincible_timer > POWER_UP_DURATION:
                self.invincible = False

    def check_platform_collisions(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.rect.bottom = hits[0].rect.top
            self.on_ground = True
            self.vel_y = 0

    def check_enemy_collisions(self):
        if not self.invincible:
            hits = pygame.sprite.spritecollide(self, enemies, False)
            if hits:
                self.health -= 10
                if self.health <= 0:
                    if self.extra_lives > 0:
                        self.extra_lives -= 1
                        self.health = 100
                        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    else:
                        print("Game Over!")
                        pygame.quit()
                        sys.exit()

    def check_collectible_collisions(self):
        hits = pygame.sprite.spritecollide(self, collectibles, True)
        for hit in hits:
            self.score += 1

    def check_boss_collisions(self):
        if not self.invincible:
            hits = pygame.sprite.spritecollide(self, bosses, False)
            if hits:
                self.health -= 20
                if self.health <= 0:
                    print("You defeated the boss!")
                    pygame.quit()
                    sys.exit()

    def check_power_up_collisions(self):
        hits = pygame.sprite.spritecollide(self, power_ups, True)
        for hit in hits:
            if hit.type == 'speed':
                # Temporarily increase player speed
                pass
            elif hit.type == 'invincibility':
                self.invincible = True
                self.invincible_timer = pygame.time.get_ticks()
            elif hit.type == 'extra_life':
                self.extra_lives += 1

    def check_obstacle_collisions(self):
        hits = pygame.sprite.spritecollide(self, obstacles, False)
        if hits:
            if not self.invincible:
                self.health -= 20
                if self.health <= 0:
                    if self.extra_lives > 0:
                        self.extra_lives -= 1
                        self.health = 100
                        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    else:
                        print("Game Over!")
                        pygame.quit()
                        sys.exit()

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
        self.direction = 1  # 1 for down/right, -1 for up/left

    def update(self):
        if self.move_type == 'horizontal':
            self.rect.x += self.direction * self.move_speed
            if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
                self.direction *= -1
        elif self.move_type == 'vertical':
            self.rect.y += self.direction * self.move_speed
            if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.direction *= -1

# Boss class
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BOSS_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 500
        self.move_speed = 2
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        self.rect.x += self.direction * self.move_speed
        if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
            self.direction *= -1

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLLECTIBLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Power-Up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, power_up_type):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(POWER_UP_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = power_up_type

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.move_type = random.choice(['horizontal', 'vertical'])
        self.direction = random.choice([-1, 1])
        self.move_speed = OBSTACLE_MOVE_SPEED

    def update(self):
        if self.move_type == 'horizontal':
            self.rect.x += self.direction * self.move_speed
            if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
                self.direction *= -1
        elif self.move_type == 'vertical':
            self.rect.y += self.direction * self.move_speed
            if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.direction *= -1

# Enemy classes with different behaviors
class BasicEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, move_type):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.move_type = move_type
        self.direction = 1  # 1 for right, -1 for left
        self.speed = ENEMY_SPEED

    def update(self):
        if self.move_type == 'horizontal':
            self.rect.x += self.direction * self.speed
            if self.rect.left <= 0 or self.rect.right >= LEVEL_WIDTH:
                self.direction *= -1
        elif self.move_type == 'vertical':
            self.rect.y += self.direction * self.speed
            if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.direction *= -1

class JumpingEnemy(BasicEnemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'vertical')
        self.jump_strength = 10

    def update(self):
        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.direction *= -1
        self.rect.y += self.direction * self.speed
        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.direction *= -1

# Initialize player, sprites, and groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
bosses = pygame.sprite.Group()

def start_level(level):
    platforms.empty()
    enemies.empty()
    collectibles.empty()
    power_ups.empty()
    obstacles.empty()
    bosses.empty()
    all_sprites.add(*platforms, *enemies, *collectibles, *power_ups, *obstacles, *bosses)
    if level == 1:
        platforms.add(Platform(100, 400, 200, 20))
        platforms.add(Platform(400, 300, 200, 20, 'horizontal'))
        platforms.add(Platform(800, 250, 200, 20, 'vertical'))
        platforms.add(Platform(1200, 350, 200, 20))
        platforms.add(Platform(1600, 450, 200, 20))
        all_sprites.add(*platforms)
        enemies.add(BasicEnemy(500, 500, 50, 50, 'horizontal'))
        enemies.add(JumpingEnemy(700, 300, 50, 50))
        all_sprites.add(*enemies)
        collectibles.add(Collectible(300, 350, 30, 30))
        collectibles.add(Collectible(700, 200, 30, 30))
        collectibles.add(Collectible(1100, 300, 30, 30))
        collectibles.add(Collectible(1500, 400, 30, 30))
        all_sprites.add(*collectibles)
        power_ups.add(PowerUp(2000, 400, 30, 30, 'invincibility'))
        power_ups.add(PowerUp(2200, 400, 30, 30, 'extra_life'))
        all_sprites.add(*power_ups)
        obstacles.add(Obstacle(1000, 500, 50, 50))
        obstacles.add(Obstacle(1500, 300, 50, 50))
        all_sprites.add(*obstacles)
        bosses.add(Boss(2500, 300, 100, 100))
        all_sprites.add(*bosses)
    elif level == 2:
        platforms.add(Platform(100, 500, 200, 20))
        platforms.add(Platform(400, 400, 200, 20, 'horizontal'))
        platforms.add(Platform(800, 300, 200, 20, 'vertical'))
        platforms.add(Platform(1200, 200, 200, 20))
        platforms.add(Platform(1600, 100, 200, 20))
        all_sprites.add(*platforms)
        enemies.add(BasicEnemy(500, 550, 50, 50, 'horizontal'))
        enemies.add(JumpingEnemy(1000, 350, 50, 50))
        all_sprites.add(*enemies)
        collectibles.add(Collectible(300, 450, 30, 30))
        collectibles.add(Collectible(700, 250, 30, 30))
        collectibles.add(Collectible(1100, 200, 30, 30))
        collectibles.add(Collectible(1500, 150, 30, 30))
        all_sprites.add(*collectibles)
        power_ups.add(PowerUp(2500, 400, 30, 30, 'speed'))
        all_sprites.add(*power_ups)
        obstacles.add(Obstacle(2000, 400, 50, 50))
        obstacles.add(Obstacle(2200, 300, 50, 50))
        all_sprites.add(*obstacles)
        bosses.add(Boss(3000, 400, 100, 100))
        all_sprites.add(*bosses)

# Initialize level
current_level = 1
start_level(current_level)

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

# Function to draw the mini-map
def draw_mini_map():
    mini_map_surface = pygame.Surface((MINI_MAP_WIDTH, MINI_MAP_HEIGHT))
    mini_map_surface.fill((0, 0, 0))
    for entity in all_sprites:
        if isinstance(entity, Platform):
            pygame.draw.rect(mini_map_surface, PLATFORM_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10, entity.rect.width // 10, entity.rect.height // 10))
        elif isinstance(entity, Collectible):
            pygame.draw.rect(mini_map_surface, COLLECTIBLE_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10, entity.rect.width // 10, entity.rect.height // 10))
        elif isinstance(entity, Enemy):
            pygame.draw.rect(mini_map_surface, ENEMY_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10, entity.rect.width // 10, entity.rect.height // 10))
        elif isinstance(entity, Boss):
            pygame.draw.rect(mini_map_surface, BOSS_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10, entity.rect.width // 10, entity.rect.height // 10))
        elif isinstance(entity, Obstacle):
            pygame.draw.rect(mini_map_surface, OBSTACLE_COLOR,
                             (entity.rect.x // 10, entity.rect.y // 10, entity.rect.width // 10, entity.rect.height // 10))
    pygame.draw.rect(mini_map_surface, PLAYER_COLOR, 
                     (player.rect.x // 10, player.rect.y // 10, PLAYER_WIDTH // 10, PLAYER_HEIGHT // 10))
    screen.blit(mini_map_surface, (SCREEN_WIDTH - MINI_MAP_WIDTH - 10, SCREEN_HEIGHT - MINI_MAP_HEIGHT - 10))

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    camera.update(player)

    screen.blit(background, camera.apply(pygame.Rect(0, 0, LEVEL_WIDTH, SCREEN_HEIGHT)))
    for entity in all_sprites:
        screen.blit(entity.image, camera.apply(entity))

    # Draw mini-map
    draw_mini_map()

    # Display the score, level, health, and power-up status
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {current_level}", True, (255, 255, 255))
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    power_up_text = font.render(f"Invincible: {'Yes' if player.invincible else 'No'}", True, (255, 255, 255))
    extra_lives_text = font.render(f"Extra Lives: {player.extra_lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(health_text, (10, 90))
    screen.blit(power_up_text, (10, 130))
    screen.blit(extra_lives_text, (10, 170))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
