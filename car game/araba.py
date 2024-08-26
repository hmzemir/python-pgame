import pygame
from pygame.locals import *
import random

pygame.init()

# Oyun penceresini oluştur
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# Renkler
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Oyun ayarları
gameover = False
speed = 2
score = 0

# Şerit işaretleri boyutu
marker_width = 10
marker_height = 50

# Yol ve kenar şerit işaretleri
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# Şeritlerin x koordinatları
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Şerit işaretlerinin hareketini animasyonlayabilmek için
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Resmi şerit boyutuna göre ölçeklendir
        image_scale = 100 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (int(new_width), int(new_height)))
       
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('Python/oyunlar/images/Car.png')
        super().__init__(image, x, y)

# Oyuncu başlangıç koordinatları
player_x = 250
player_y = 400

# Oyuncu aracını oluştur
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Diğer araç resimlerini yükle
image_filenames = ['Mini_truck.png', 'Police.png','Audi.png', 'taxi.png', 'Mini_van.png', 'truck.png', 'Black_viper.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('Python/oyunlar/images/' + image_filename)
    vehicle_images.append(image)

# Araçlar için sprite grubu
vehicle_group = pygame.sprite.Group()

# Patlama resmini yükle
crash = pygame.image.load('Python/oyunlar/images/explosion2.png')
crash_rect = crash.get_rect()

# Oyun döngüsü
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # Sol/sağ ok tuşlarıyla oyuncu aracını hareket ettir
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
            # Yan çarpışma kontrolü
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True
                    
                    # Oyuncu aracını diğer aracın yanına yerleştir
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
            
    # Çimleri çiz
    screen.fill(yellow)
    
    # Yolu çiz
    pygame.draw.rect(screen, gray, road)
    
    # Kenar şerit işaretlerini çiz
    pygame.draw.rect(screen, red, left_edge_marker)
    pygame.draw.rect(screen, red, right_edge_marker)
    
    # Şerit işaretlerini çiz
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
    
    # Oyuncu aracını çiz
    player_group.draw(screen)
    
    # En fazla iki araç ekle
    if len(vehicle_group) < 2:
        
        # Araçlar arasında yeterli boşluk olduğundan emin ol
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        
        if add_vehicle:
            
            # Rastgele şerit seç
            lane = random.choice(lanes)
            
            # Rastgele araç resmi seç
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
            
    # Araçları hareket ettir
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # Araç ekranın dışına çıktığında sil
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            # Skoru artır
            score += 1
            
            # Araçları geçtikten sonra oyunu hızlandır
            if score > 0 and score % 5 == 0:
                speed += 1
                
    # Araçları çiz
    vehicle_group.draw(screen)
    
    # Skoru göster
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' +str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)
    
    # Çarpışma kontrolü
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
    
    # Oyun bittiğinde "Game Over" ekranını göster
    if gameover:
        screen.blit(crash, crash_rect)
        
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
        
    pygame.display.update()
    
    # Oyuncunun tekrar oynamak isteyip istemediğini kontrol et
    while gameover:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False
                running = False
            
            # Oyuncunun girdisini al
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()
