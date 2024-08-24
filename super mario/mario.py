import pygame
import os
import random

# Pygame'i başlat
pygame.init()

# Oyun ekranı boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Tarzı Platform Oyunu")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Renkler
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Yerçekimi değeri
GRAVITY = 1

# Oyun için sınıflar ve fonksiyonlar
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.jump_count = 2  # İkili zıplama için
        self.is_alive = True
        
        # Mario yürüyüş animasyonları için görseller ekleyin
        for i in range(1, 4):
            img = pygame.image.load(f"images/mario_walk_{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (40, 60))
            self.images.append(img)
        
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.walk_index = 0
        self.direction = 0

    def update(self):
        if not self.is_alive:
            return

        dx = 0
        dy = 0

        # Klavye girdilerini al
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -5
            self.direction = -1
            self.walk_index += 1
        if key[pygame.K_RIGHT]:
            dx = 5
            self.direction = 1
            self.walk_index += 1
        if key[pygame.K_SPACE] and self.jump_count > 0:
            self.vel_y = -15
            self.jumped = True
            self.jump_count -= 1

        # Yerçekimi ekle
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Zıplamayı durdur
        if self.vel_y > 0:
            self.jumped = False

        # Hareket animasyonu
        if self.walk_index >= len(self.images):
            self.walk_index = 0
        self.image = self.images[self.walk_index]
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Çarpışma kontrolü
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.jump_count = 2  # Platforma inince zıplama hakkı yenilenir

        # Pozisyonu güncelle
        self.rect.x += dx
        self.rect.y += dy

        # Ekran dışına çıkmayı engelle
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            dy = 0

        screen.blit(self.image, self.rect)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        screen.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/flag.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)

# Gruplar
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# Yeni bir seviye oluşturma fonksiyonu
def create_level(level):
    global platform_group, enemy_group, flag_group, coin_group

    platform_group.empty()
    enemy_group.empty()
    flag_group.empty()
    coin_group.empty()

    # Renkler seviyeye göre değişir
    if level == 1:
        platform_color = WHITE
        bg_color = BLACK
    elif level == 2:
        platform_color = RED
        bg_color = BLUE
    elif level == 3:
        platform_color = GREEN
        bg_color = RED
    else:
        platform_color = BLUE
        bg_color = GREEN

    screen.fill(bg_color)

    # Platformlar ekle
    platform = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, platform_color)
    platform_group.add(platform)

    platform = Platform(200, SCREEN_HEIGHT - 200, 100, 20, platform_color)
    platform_group.add(platform)

    platform = Platform(500, SCREEN_HEIGHT - 300, 100, 20, platform_color)
    platform_group.add(platform)

    if level >= 2:
        platform = Platform(150, SCREEN_HEIGHT - 150, 150, 20, platform_color)
        platform_group.add(platform)

    if level >= 3:
        platform = Platform(400, SCREEN_HEIGHT - 250, 150, 20, platform_color)
        platform_group.add(platform)

    # Düşmanlar ekle
    enemy = Enemy(300, SCREEN_HEIGHT - 60)
    enemy_group.add(enemy)

    if level >= 2:
        enemy = Enemy(600, SCREEN_HEIGHT - 60)
        enemy_group.add(enemy)

    if level >= 3:
        enemy = Enemy(400, SCREEN_HEIGHT - 60)
        enemy_group.add(enemy)

    # Bayrak ekle
    flag = Flag(700, SCREEN_HEIGHT - 200)
    flag_group.add(flag)

    # Paralar ekle
    for i in range(5):
        coin_x = random.randint(100, SCREEN_WIDTH - 100)
        coin_y = random.randint(100, SCREEN_HEIGHT - 200)
        coin = Coin(coin_x, coin_y)
        coin_group.add(coin)

# Oyuncu
player = Player(100, SCREEN_HEIGHT - 100)

# Başlangıç seviyesi
current_level = 1
create_level(current_level)
score = 0
font = pygame.font.SysFont('Arial', 24)

# Oyun döngüsü
run = True
while run:
    clock.tick(FPS)

    screen.fill((0, 0, 0))

    platform_group.update()
    enemy_group.update()
    flag_group.update()
    coin_group.update()
    player.update()

    # Skor ve seviye gösterimi
    score_text = font.render(f"Level: {current_level}  Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Oyun kapanma durumu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Bayrağa çarpma durumu
    if pygame.sprite.spritecollide(player, flag_group, False):
        current_level += 1
        create_level(current_level)
        player.rect.x = 100
        player.rect.y = SCREEN_HEIGHT - 100

    # Düşmanlara çarpma durumu
    if pygame.sprite.spritecollide(player, enemy_group, False):
        player.is_alive = False
        current_level = 1
        score = 0
        create_level(current_level)
        player.rect.x = 100
        player.rect.y = SCREEN_HEIGHT - 100
        player.is_alive = True

    # Paraları toplama durumu
    coins_collected = pygame.sprite.spritecollide(player, coin_group, True)
    score += len(coins_collected)

    pygame.display.update()

pygame.quit()
