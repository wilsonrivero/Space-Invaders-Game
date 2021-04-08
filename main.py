import pygame
from pygame import mixer
import random
import time


pygame.init()

## VARIABLES GLOBAL
BLACK = (0,0,0)
WHITE = (255,255,255)
WIDTH, HEIGHT = 600,600
round = 0
score = 0
health = 3
run = True


##SCREEN AND CAPTION
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astroid game")

img = pygame.image.load('./assets/images/background.jpg')
new_img = pygame.transform.scale(img, (WIDTH, HEIGHT))

#BACKGROUND SOUND
mixer.music.load('./assets/audio/background.wav')
mixer.music.play(-1)

#BULLET SOUND AND EXPLOSION SOUND 
bullet_sound = mixer.Sound('./assets/audio/laser.wav')
explosion_sound = mixer.Sound('./assets/audio/explosion.wav')

#FONT 
font = pygame.font.Font('./assets/fonts/FiraCode-Bold.ttf', 25)

#FPS
clock = pygame.time.Clock()

#Create spaceship with sprite 
class SpaceShip(pygame.sprite.Sprite):
   def __init__(self, bullets):
      super().__init__()
      self.image = pygame.image.load('./assets/images/spaceship.png')
      self.x = 280
      self.y = 543
      self.angle = 0
      self.speed = 10
      self.bullets = bullets

      self.rect = self.image.get_rect(center=(self.x, self.y))

   # Moving the spaceship
   def update(self):
      keys = pygame.key.get_pressed()

      if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
         if self.rect.x < WIDTH - 30:
            self.rect.x += self.speed
         else:
            self.rect.x = 570

      if keys[pygame.K_a] or keys[pygame.K_LEFT]:
         if self.rect.x > 0:
            self.rect.x -= self.speed
         else:
            self.rect.x = 0

      if keys[pygame.K_w] or keys[pygame.K_UP]:
         self.rect.y -= self.speed

      if keys[pygame.K_s] or keys[pygame.K_DOWN]:
         if self.rect.y < HEIGHT - 30:
            self.rect.y += self.speed
         else:
            self.rect.y = 570

   def create_fire(self):
      self.bullets.add(Bullets(*self.rect.center))

#Create bullets sprites
class Bullets(pygame.sprite.Sprite):
   def __init__(self, x, y):
      super().__init__()

      self.image = pygame.image.load('./assets/images/bullet.png')
      self.rect = self.image.get_rect(center=(x, y - 15))

   #Moving bullets
   def update(self):
      self.rect.y -= 7
      if self.rect.y < 0:
         self.kill()

#Create Enemies
class Enemies(pygame.sprite.Sprite):
   def __init__(self):
      super().__init__()
      self.imgs = random.randint(1,4)
      self.image = pygame.image.load(f'./assets/images/monster{self.imgs}.png')
      self.rect = self.image.get_rect(center=(random.randint(10, 560), -10))

   #Moving the Enemies
   def update(self):
      global health

      text_health = font.render(f'Health: {health}', False, WHITE)
      screen.blit(text_health, (10, 565))

      self.rect.y += 5
      if self.rect.y > 575:
         self.kill()
         health -= 1

      if health == 0:
         time.sleep(3)
         pygame.quit()



#Gruops fo sprites
group_spaceship = pygame.sprite.Group()
group_bullets = pygame.sprite.Group()
group_enemies = pygame.sprite.Group()
group_hearts = pygame.sprite.Group()

#Instânciando uma classs
spaceship = SpaceShip(group_bullets)
enemies = Enemies()

# Add class in a group 
group_spaceship.add(spaceship)
group_enemies.add(enemies)

#Sart Game
while run:
   clock.tick(30)
   
   # Creating a monster in game 
   if round % 100 == 0:
      group_enemies.add(Enemies())
      
      #Let more hard the game
      if score > 10:
         group_enemies.add(Enemies())

         if score > 20:
            group_enemies.add(Enemies())

            if score > 30:
               group_enemies.add(Enemies())


   # events in pygame
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         run = False
         pygame.quit() 

      #Shooting 
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_SPACE:
            bullet_sound.play()
            spaceship.create_fire()
      
   #Collision with the bullets and monster if collisoin is true destroy bullet and monster and play sound of explosion
   if pygame.sprite.groupcollide(group_bullets, group_enemies, True, True):
      explosion_sound.play()
      score += 1

   # Make a a score in screen
   text = font.render(f'Score:{score}', False, WHITE)
   
   # Render a background image in screen
   screen.blit(new_img, (0,0))

   # Render a score on screen
   screen.blit(text, (460, 30))
   
   # Draw a sprites   
   group_spaceship.draw(screen)
   group_bullets.draw(screen)
   group_enemies.draw(screen)

   # UPdates sprites
   group_spaceship.update()
   group_bullets.update()
   group_enemies.update()

   round += 1
   pygame.display.update()
   