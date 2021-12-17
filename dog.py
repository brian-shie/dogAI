import os
import time
import pygame
import random
from helper import *

class Player:

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = int(width)
		self.height = int(height)
		self.vel = 5
		self.left, self.right, self.up, self.down = False
		self.walkCount = 0
		self.mana = 150

	def draw(self):
		if self.walkCount == 15:
			self.walkCount = 0

		if self.left:
			win.blit(player_left[self.walkCount // 4], (self.x, self.y))
			self.walkCount += 1

		elif self.right:
			win.blit(player_right[self.walkCount // 4], (self.x, self.y))
			self.walkCount += 1

		elif self.up:
			win.blit(player_up[self.walkCount // 8], (self.x, self.y))
			self.walkCount += 1

		else:
			win.blit(player_down[self.walkCount // 8], (self.x, self.y))
			self.walkCount += 1


class Monster:
	def __init__(self, x, y, width, height, type):
		self.x, self.y = x, y
		self.width, self.height = int(width), int(height)
		self.type = type
		self.vel = 3
		self.left, self.right, self.up, self.down = False
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


class Cookie:

	def __init__(self):
		self.x, self.y  = random.randint(2, 18), random.randint(2, 13)
		self.walkCount = 0

	def draw(self):
		if self.walkCount == 19:
			self.walkCount = 0

		win.blit(dogcookie[self.walkCount // 5], (self.rng_x * 40, self.rng_y * 40))
		self.walkCount += 1


class DogGame():

	def __init__(self):
		self.player = Player(200, 200, 64, 64)
		self.monster_1 = Deathspirit(0, 0, 64, 64, 1)
		self.monster_2 = Deathspirit(736, 536, 64, 64, 0)
		self.biscoito = Cookie()
		self.inputs = [0, 0, 0, 0, 0] # Left, Right, Up, Down, Spacebar
		self.score = 0

		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()

		self.win = pygame.display.set_mode((scrW, scrH))
		pygame.display.set_caption("Dog Game")

		self.clock = pygame.time.Clock()
		self.clock.tick(30)

		pygame.mixer.music.load('sound/nintendogs.mp3')
		pygame.mixer.music.play(-1)
		pygame.mixer.Sound.set_volume(sound_bis, 0.25)

		self.game_over = False

	def play_step(self):

		# 1. Collect user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					inputs[0] = 1

				if event.key == pygame.K_LEFT:
					inputs[1] = 1

				if event.key == pygame.K_LEFT:
					inputs[2] = 1

				if event.key == pygame.K_LEFT:
					inputs[3] = 1

				if event.key == pygame.K_LEFT:
					inputs[4] = 1

		# 2. Movement
		self._move(self.inputs)

		# 3. Check if game ends
		if self.monster_1.x - 40 <= self.dog.x <= self.monster_1.x + 40 and self.monster_1.y - 40 <= self.dog.y <= self.monster_1.y + 40:
			self.game_over = True
			return self.game_over, self.score

		if self.monster_2.x - 40 <= self.dog.x <= self.monster_2.x + 40 and self.monster_2.y - 40 <= self.dog.y <= self.monster_2.y + 40:
			self.game_over = True
			return self.game_over, self.score

		# 4. Check cookie colision
		if self.biscoito.x * 40 - 64 <= dog.x <= biscoito.x * 40 + 48 and self.biscoito.y * 40 - 64 <= dog.y <= biscoito.y * 40 + 32:
			self.biscoito.x = random.randint(2, 18)
			self.biscoito.y = random.randint(2, 13)
			self.dog.mana += 10
			sound_bis.play()
			self.score += 1
			self.monster_1.vel += 0.1
			self.monster_2.vel += 0.1

		# 5. Redraw
		self._redraw()

		# 6. Reset inputs, return game over and score
		self.inputs = [0, 0, 0, 0, 0]
		return self.game_over, self.score

	def _move(self, inputs):

		if self.inputs[4]:
			if self.dog.mana > 1:
				self.dog.mana -= 1
				self.dog.vel = 8

			else:
				self.dog.vel = 5

		if self.inputs[0] and self.dog.x >= self.dog.vel:
			self.dog.x -= dog.vel
			self.dog.left = True
			self.dog.right, self.dog.up, self.dog.down = False

			if self.inputs[0] and self.dog.x < self.dog.vel:
				self.dog.x = 0
				self.dog.left = True
				self.dog.right, self.dog.up, self.dog.down = False

		if self.inputs[1] and self.dog.x <= scrW - self.dog.width - self.dog.vel:
			self.dog.x += self.dog.vel
			self.dog.right = True
			self.dog.left, self.dog.up, self.dog.down = False

			if self.inputs[1] and self.dog.x > scrW - self.dog.width - self.dog.vel:
				self.dog.x = scrW - self.dog.width
				self.dog.right = True
				self.dog.left, self.dog.up, self.dog.down = False

		if self.inputs[2] and self.dog.y >= self.dog.vel:
			self.dog.y -= self.dog.vel
			self.dog.up = True
			self.dog.down, self.dog.left, self.dog.right = False

			if self.inputs[2] and self.dog.y < self.dog.vel:
				self.dog.y = 0
				self.dog.up = True
				self.dog.down, self.dog.left, self.dog.right = False

		if self.inputs[3] and self.dog.y <= scrH - self.dog.height - self.dog.vel:
			self.dog.y += self.dog.vel
			self.dog.down = True
			self.dog.up, self.dog.left, self.dog.right = False

			if self.inputs[3] and self.dog.y > scrH - self.dog.height - self.dog.vel:
				self.dog.y = scrH - self.dog.height
				self.dog.down = True
				self.dog.up, self.dog.left, self.dog.right = False

	def _redraw(self):
		self.win.blit(bg, (0, 0))

		pygame.draw.rect(win, (0, 0, 255), (10, 520, self.mana, 10))
		self.text = font.render("Score: " + str(score), 1, (255, 255, 255))
		self.win.blit(self.text, (15, 530))

		self.player.draw()
		self.biscoito.draw()
		self.monster_1.draw()
		self.monster_2.draw()
		pygame.display.update()


if __name__ == '__main__':
	game = DogGame()

	while True:
		game.game_over, score = game.play_step()

		if game.game_over == True:
			break

	print('Final Score', score)
	pygame.quit()
