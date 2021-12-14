import os
import time
import pygame
import random

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()

scrW = 800
scrH = 600

win = pygame.display.set_mode((scrW, scrH))

pygame.display.set_caption("Dog Game")

bg = pygame.image.load('images/grassland11.png')


walkLeft = [pygame.image.load('images/sprites/animals/animals_13.png'),
            pygame.image.load('images/sprites/animals/animals_14.png'),
            pygame.image.load('images/sprites/animals/animals_15.png'),
            pygame.image.load('images/sprites/animals/animals_14.png')]
walkRight = [pygame.image.load('images/sprites/animals/animals_25.png'),
             pygame.image.load('images/sprites/animals/animals_26.png'),
             pygame.image.load('images/sprites/animals/animals_27.png'),
             pygame.image.load('images/sprites/animals/animals_26.png')]
walkUp = [pygame.image.load('images/sprites/animals/animals_37.png'),
          pygame.image.load('images/sprites/animals/animals_39.png'),
          pygame.image.load('images/sprites/animals/animals_37.png'),
          pygame.image.load('images/sprites/animals/animals_39.png')]
walkDown = [pygame.image.load('images/sprites/animals/animals_01.png'),
            pygame.image.load('images/sprites/animals/animals_03.png'),
            pygame.image.load('images/sprites/animals/animals_01.png'),
            pygame.image.load('images/sprites/animals/animals_03.png')]
dogcookie = [pygame.image.load('images/dogc.png'), pygame.image.load('images/dogc2.png'),
             pygame.image.load('images/dogc3.png'), pygame.image.load('images/dogc4.png')]

clock = pygame.time.Clock()

score = 0

pygame.mixer.music.load('sound/nintendogs.mp3')
pygame.mixer.music.play(-1)
font = pygame.font.SysFont("comicsans", 40, True)
sound_bis = pygame.mixer.Sound("sound/coin.wav")
pygame.mixer.Sound.set_volume(sound_bis, 0.25)


class Player:

    def __init__(self, x, y, width, height):

        self.x = x
        self.y = y
        self.width = int(width)
        self.height = int(height)
        self.vel = 5
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walkCount = 0
        self.mana = 100

    def draw(self):
        if self.walkCount == 15:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount // 4], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount // 4], (self.x, self.y))
            self.walkCount += 1
        elif self.up:
            win.blit(walkUp[self.walkCount // 8], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(walkDown[self.walkCount // 8], (self.x, self.y))
            self.walkCount += 1

        pygame.draw.rect(win, (0, 0, 255), (10, 545, self.mana, 10))


class Objects:

    def __init__(self):
        self.rng_x = random.randint(2, 18)
        self.rng_y = random.randint(2, 13)
        self.walkCount = 0

    def draw(self):
        if self.walkCount == 19:
            self.walkCount = 0
        win.blit(dogcookie[self.walkCount // 5], (self.rng_x * 40, self.rng_y * 40))
        self.walkCount += 1


def redraw():
    win.blit(bg, (0, 0))

    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (10, 565))
    dog.draw()
    biscoito.draw()

    pygame.display.update()


# main
dog = Player(200, 200, 64, 64)
biscoito = Objects()
run = True
while run:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()  # KEYS

    if keys[pygame.K_LEFT] and dog.x >= dog.vel:
        dog.x -= dog.vel
        dog.left = True
        dog.right = False
        dog.up = False
        dog.down = False

        if keys[pygame.K_LEFT] and dog.x < dog.vel:
            dog.x = 0
            dog.left = True
            dog.right = False
            dog.up = False
            dog.down = False

    elif keys[pygame.K_RIGHT] and dog.x <= scrW - dog.width - dog.vel:
        dog.x += dog.vel
        dog.right = True
        dog.left = False
        dog.up = False
        dog.down = False

        if keys[pygame.K_RIGHT] and dog.x > scrW - dog.width - dog.vel:
            dog.x = scrW - dog.width
            dog.right = True
            dog.left = False
            dog.down = False
            dog.up = False
    elif keys[pygame.K_UP] and dog.y >= dog.vel:
        dog.y -= dog.vel
        dog.up = True
        dog.down = False
        dog.left = False
        dog.right = False

        if keys[pygame.K_UP] and dog.y < dog.vel:
            dog.y = 0
            dog.up = True
            dog.down = False
            dog.left = False
            dog.right = False

    elif keys[pygame.K_DOWN] and dog.y <= scrH - dog.height - dog.vel:
        dog.y += dog.vel
        dog.down = True
        dog.up = False
        dog.left = False
        dog.right = False

        if keys[pygame.K_DOWN] and dog.y > scrH - dog.height - dog.vel:
            dog.y = scrH - dog.height
            dog.down = True
            dog.up = False
            dog.left = False
            dog.right = False

    if keys[pygame.K_SPACE]:
        if dog.mana > 1:
            dog.mana -= 1
            dog.vel = 8
        else:
            dog.vel = 5

    if not keys[pygame.K_SPACE]:
        dog.vel = 5

    if biscoito.rng_x * 40 - 64 <= dog.x <= biscoito.rng_x * 40 + 48 \
            and biscoito.rng_y * 40 - 64 <= dog.y <= biscoito.rng_y * 40 + 32:
        if dog.mana <= 100:
            dog.mana += 10
        sound_bis.play()
        biscoito.rng_x = random.randint(2, 18)
        biscoito.rng_y = random.randint(2, 13)
        score += 1

    if keys[pygame.K_1]:
        main = False
    redraw()

pygame.quit()
