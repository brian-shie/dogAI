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

deathspiritLeft = [pygame.image.load('images/deathspirit/deathspirit_22.png'),
			pygame.image.load('images/deathspirit/deathspirit_23.png'),
			pygame.image.load('images/deathspirit/deathspirit_24.png'),
			pygame.image.load('images/deathspirit/deathspirit_23.png')]
deathspiritRight = [pygame.image.load('images/deathspirit/deathspirit_34.png'),
			 pygame.image.load('images/deathspirit/deathspirit_35.png'),
			 pygame.image.load('images/deathspirit/deathspirit_36.png'),
			 pygame.image.load('images/deathspirit/deathspirit_35.png')]
deathspiritUp = [pygame.image.load('images/deathspirit/deathspirit_46.png'),
		  pygame.image.load('images/deathspirit/deathspirit_47.png'),
		  pygame.image.load('images/deathspirit/deathspirit_48.png'),
		  pygame.image.load('images/deathspirit/deathspirit_47.png')]
deathspiritDown = [pygame.image.load('images/deathspirit/deathspirit_10.png'),
			pygame.image.load('images/deathspirit/deathspirit_11.png'),
			pygame.image.load('images/deathspirit/deathspirit_12.png'),
			pygame.image.load('images/deathspirit/deathspirit_11.png')]

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
		self.mana = 150

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

		pygame.draw.rect(win, (0, 0, 255), (10, 520, self.mana, 10))

class Deathspirit:
	def __init__(self, x, y, width, height, type):
		self.x = x
		self.y = y
		self.width = int(width)
		self.height = int(height)
		self.type = type
		self.vel = 3
		self.left = False
		self.right = False
		self.up = False
		self.down = False
		self.walkCount = 0
		self.mana = 150

	def draw(self):
		if self.walkCount == 15:
			self.walkCount = 0

		if self.left:
			win.blit(deathspiritLeft[self.walkCount // 4], (self.x, self.y))
			self.walkCount += 1
		elif self.right:
			win.blit(deathspiritRight[self.walkCount // 4], (self.x, self.y))
			self.walkCount += 1
		elif self.up:
			win.blit(deathspiritUp[self.walkCount // 8], (self.x, self.y))
			self.walkCount += 1
		else:
			win.blit(deathspiritDown[self.walkCount // 8], (self.x, self.y))
			self.walkCount += 1

	def movement(self, type):
		if self.type == 1:
			if self.x + 5 < dog.x:
				self.x += self.vel
				self.down = False
				self.up = False
				self.left = False
				self.right = True

			elif self.x - 5 > dog.x:
				self.x -= self.vel
				self.down = False
				self.up = False
				self.left = True
				self.right = False
			#
			elif self.y < dog.y:
				self.y += self.vel
				self.down = True
				self.up = False
				self.left = False
				self.right = False

			elif self.y > dog.y:
				self.y -= self.vel
				self.down = False
				self.up = True
				self.left = False
				self.right = False

		else:
			if self.y + 5 < dog.y:
				self.y += self.vel
				self.down = True
				self.up = False
				self.left = False
				self.right = False

			elif self.y - 5 > dog.y:
				self.y -= self.vel
				self.down = False
				self.up = True
				self.left = False
				self.right = False

			elif self.x < dog.x:
				self.x += self.vel
				self.down = False
				self.up = False
				self.left = False
				self.right = True

			elif self.x > dog.x:
				self.x -= self.vel
				self.down = False
				self.up = False
				self.left = True
				self.right = False

        
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
	win.blit(text, (15, 530))
	dog.draw()
	biscoito.draw()
	deathspirit1.draw()
	deathspirit2.draw()
	pygame.display.update()


# main
dog = Player(200, 200, 64, 64)
deathspirit1 = Deathspirit(0, 0, 64, 64, 1)
deathspirit2 = Deathspirit(736, 536, 64, 64, 0)
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

	if keys[pygame.K_RIGHT] and dog.x <= scrW - dog.width - dog.vel:
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

	if keys[pygame.K_UP] and dog.y >= dog.vel:
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

	if keys[pygame.K_DOWN] and dog.y <= scrH - dog.height - dog.vel:
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

	if biscoito.rng_x * 40 - 64 <= dog.x <= biscoito.rng_x * 40 + 48 and biscoito.rng_y * 40 - 64 <= dog.y <= biscoito.rng_y * 40 + 32:
		biscoito.rng_x = random.randint(2, 18)
		biscoito.rng_y = random.randint(2, 13)
		dog.mana += 10
		sound_bis.play()
		score += 1
		deathspirit1.vel += 0.1
		deathspirit2.vel += 0.1

	deathspirit1.movement(1)
	deathspirit2.movement(2)

	if deathspirit1.x - 40 <= dog.x <= deathspirit1.x + 40 and deathspirit1.y - 40 <= dog.y <= deathspirit1.y + 40:
		dog = Player(200, 200, 64, 64)
		deathspirit1 = Deathspirit(0, 0, 64, 64, 1)
		deathspirit2 = Deathspirit(736, 536, 64, 64, 0)
		biscoito = Objects()
		score = 0
		pygame.mixer.music.load('sound/nintendogs.mp3')
		pygame.mixer.music.play(-1)

	if deathspirit2.x - 40 <= dog.x <= deathspirit2.x + 40 and deathspirit2.y - 40 <= dog.y <= deathspirit2.y + 40:
		dog = Player(200, 200, 64, 64)
		deathspirit1 = Deathspirit(0, 0, 64, 64, 1)
		deathspirit2 = Deathspirit(736, 536, 64, 64, 0)
		biscoito = Objects()
		score = 0
		pygame.mixer.music.load('sound/nintendogs.mp3')
		pygame.mixer.music.play(-1)

	if keys[pygame.K_1]:
		break

	if dog.mana < 150:
		dog.mana += 1/10

	redraw()

pygame.quit()
