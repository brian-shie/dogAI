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
		self.left, self.right, self.up, self.down = False, False, False, False
		self.walkCount = 0
		self.mana = 150


class Monster:
	def __init__(self, x, y, width, height, type):
		self.x, self.y = x, y
		self.width, self.height = int(width), int(height)
		self.type = type
		self.vel = 3
		self.left, self.right, self.up, self.down = False, False, False, False
		self.walkCount = 0
		self.mana = 150


class Cookie:

	def __init__(self):
		self.x, self.y  = random.randint(2, 18), random.randint(2, 13)
		self.walkCount = 0


class DogGame():

	def __init__(self):
		self.player = Player(200, 200, 64, 64)
		self.monster_1 = Monster(0, 0, 64, 64, 1)
		self.monster_2 = Monster(736, 536, 64, 64, 0)
		self.biscoito = Cookie()
		self.inputs = [0, 0, 0, 0, 0] # Left, Right, Up, Down, Spacebar
		self.score = 0

		pygame.mixer.pre_init(44100, -16, 1, 512)
		pygame.init()

		self.win = pygame.display.set_mode((scrW, scrH))
		pygame.display.set_caption("Dog Game")

		self.clock = pygame.time.Clock()


		self.sound_bis = pygame.mixer.Sound("sound/coin.wav")
		pygame.mixer.music.load('sound/nintendogs.mp3')
		pygame.mixer.music.play(-1)
		pygame.mixer.Sound.set_volume(self.sound_bis, 0.25)

		self.font = pygame.font.SysFont("comicsans", 40, True)
		self.game_over = False

	def play_step(self):

		# 1. Collect user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		self.keys = pygame.key.get_pressed()

		if self.keys[pygame.K_LEFT]:
			self.inputs[0] = 1

		if self.keys[pygame.K_RIGHT]:
			self.inputs[1] = 1

		if self.keys[pygame.K_UP]:
			self.inputs[2] = 1

		if self.keys[pygame.K_DOWN]:
			self.inputs[3] = 1

		if self.keys[pygame.K_SPACE]:
			self.inputs[4] = 1

		# 2. Movement
		self._move()
		self._move_monsters()

		# 3. Check if game ends
		if self.monster_1.x - 40 <= self.player.x <= self.monster_1.x + 40 and self.monster_1.y - 40 <= self.player.y <= self.monster_1.y + 40:
			self.game_over = True
			return self.game_over, self.score

		if self.monster_2.x - 40 <= self.player.x <= self.monster_2.x + 40 and self.monster_2.y - 40 <= self.player.y <= self.monster_2.y + 40:
			self.game_over = True
			return self.game_over, self.score

		# 4. Check cookie colision
		if self.biscoito.x * 40 - 64 <= self.player.x <= self.biscoito.x * 40 + 48 and self.biscoito.y * 40 - 64 <= self.player.y <= self.biscoito.y * 40 + 32:
			self.biscoito.x = random.randint(2, 18)
			self.biscoito.y = random.randint(2, 13)
			self.player.mana += 10
			self.sound_bis.play()
			self.score += 1
			self.monster_1.vel += 0.1
			self.monster_2.vel += 0.1

		# 5. Redraw
		self._redraw()

		# 6. Reset inputs, return game over and score
		self.inputs = [0, 0, 0, 0, 0]
		return self.game_over, self.score

	def _move(self):

		if self.inputs[4]:
			if self.player.mana > 1:
				self.player.mana -= 1
				self.player.vel = 8

			else:
				self.player.vel = 5

		else:
			self.player.vel = 5

		if self.inputs[0] == 1 and self.player.x >= self.player.vel:
			self.player.x -= self.player.vel
			self.player.left = True
			self.player.right, self.player.up, self.player.down = False, False, False

			if self.inputs[0] == 1 and self.player.x < self.player.vel:
				self.player.x = 0
				self.player.left = True
				self.player.right, self.player.up, self.player.down = False, False, False

		if self.inputs[1] == 1 and self.player.x <= scrW - self.player.width - self.player.vel:
			self.player.x += self.player.vel
			self.player.right = True
			self.player.left, self.player.up, self.player.down = False, False, False

			if self.inputs[1] == 1 and self.player.x > scrW - self.player.width - self.player.vel:
				self.player.x = scrW - self.player.width
				self.player.right = True
				self.player.left, self.player.up, self.player.down = False, False, False

		if self.inputs[2] == 1 and self.player.y >= self.player.vel:
			self.player.y -= self.player.vel
			self.player.up = True
			self.player.down, self.player.left, self.player.right = False, False, False

			if self.inputs[2] == 1 and self.player.y < self.player.vel:
				self.player.y = 0
				self.player.up = True
				self.player.down, self.player.left, self.player.right = False, False, False

		if self.inputs[3] == 1 and self.player.y <= scrH - self.player.height - self.player.vel:
			self.player.y += self.player.vel
			self.player.down = True
			self.player.up, self.player.left, self.player.right = False, False, False

			if self.inputs[3] == 1 and self.player.y > scrH - self.player.height - self.player.vel:
				self.player.y = scrH - self.player.height
				self.player.down = True
				self.player.up, self.player.left, self.player.right = False, False, False


	def _redraw(self):

		self.win.blit(bg, (0, 0))

		pygame.draw.rect(self.win, (0, 0, 255), (10, 520, self.player.mana, 10))
		self.text = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
		self.win.blit(self.text, (15, 530))

		self._draw_player()
		self._draw_cookie()
		self._draw_monsters()

		pygame.display.update()
		self.clock.tick(30)

	def _draw_player(self):
		if self.player.walkCount == 15:
			self.player.walkCount = 0

		if self.player.left:
			self.win.blit(player_left[self.player.walkCount // 4], (self.player.x, self.player.y))
			self.player.walkCount += 1

		elif self.player.right:
			self.win.blit(player_right[self.player.walkCount // 4], (self.player.x, self.player.y))
			self.player.walkCount += 1

		elif self.player.up:
			self.win.blit(player_up[self.player.walkCount // 8], (self.player.x, self.player.y))
			self.player.walkCount += 1

		else:
			self.win.blit(player_down[self.player.walkCount // 8], (self.player.x, self.player.y))
			self.player.walkCount += 1

	def _draw_cookie(self):
		if self.biscoito.walkCount == 19:
			self.biscoito.walkCount = 0

		self.win.blit(dogcookie[self.biscoito.walkCount // 5], (self.biscoito.x * 40, self.biscoito.y * 40))
		self.biscoito.walkCount += 1

	def _draw_monsters(self):
		if self.monster_1.walkCount == 15:
			self.monster_1.walkCount = 0

		if self.monster_1.left:
			self.win.blit(monster_left[self.monster_1.walkCount // 4], (self.monster_1.x, self.monster_1.y))
			self.monster_1.walkCount += 1
		elif self.monster_1.right:
			self.win.blit(monster_right[self.monster_1.walkCount // 4], (self.monster_1.x, self.monster_1.y))
			self.monster_1.walkCount += 1
		elif self.monster_1.up:
			self.win.blit(deathspiritUp[self.monster_1.walkCount // 8], (self.monster_1.x, self.monster_1.y))
			self.monster_1.walkCount += 1
		else:
			self.win.blit(monster_down[self.monster_1.walkCount // 8], (self.monster_1.x, self.monster_1.y))
			self.monster_1.walkCount += 1

		if self.monster_2.walkCount == 15:
			self.monster_2.walkCount = 0

		if self.monster_2.left:
			self.win.blit(monster_left[self.monster_2.walkCount // 4], (self.monster_2.x, self.monster_2.y))
			self.monster_2.walkCount += 1
		elif self.monster_2.right:
			self.win.blit(monster_right[self.monster_2.walkCount // 4], (self.monster_2.x, self.monster_2.y))
			self.monster_2.walkCount += 1
		elif self.monster_2.up:
			self.win.blit(monster_up[self.monster_2.walkCount // 8], (self.monster_2.x, self.monster_2.y))
			self.monster_2.walkCount += 1
		else:
			self.win.blit(monster_down[self.monster_2.walkCount // 8], (self.monster_2.x, self.monster_2.y))
			self.monster_2.walkCount += 1

	def _move_monsters(self):
		if self.monster_1.x + 5 < self.player.x:
			self.monster_1.x += self.monster_1.vel
			self.monster_1.down = False
			self.monster_1.up = False
			self.monster_1.left = False
			self.monster_1.right = True

		elif self.monster_1.x - 5 > self.player.x:
			self.monster_1.x -= self.monster_1.vel
			self.monster_1.down = False
			self.monster_1.up = False
			self.monster_1.left = True
			self.monster_1.right = False
		#
		elif self.monster_1.y < self.player.y:
			self.monster_1.y += self.monster_1.vel
			self.monster_1.down = True
			self.monster_1.up = False
			self.monster_1.left = False
			self.monster_1.right = False

		elif self.monster_1.y > self.player.y:
			self.monster_1.y -= self.monster_1.vel
			self.monster_1.down = False
			self.monster_1.up = True
			self.monster_1.left = False
			self.monster_1.right = False

		if self.monster_2.y + 5 < self.player.y:
			self.monster_2.y += self.monster_2.vel
			self.monster_2.down = True
			self.monster_2.up = False
			self.monster_2.left = False
			self.monster_2.right = False

		elif self.monster_2.y - 5 > self.player.y:
			self.monster_2.y -= self.monster_2.vel
			self.monster_2.down = False
			self.monster_2.up = True
			self.monster_2.left = False
			self.monster_2.right = False

		elif self.monster_2.x < self.player.x:
			self.monster_2.x += self.monster_2.vel
			self.monster_2.down = False
			self.monster_2.up = False
			self.monster_2.left = False
			self.monster_2.right = True

		elif self.monster_2.x > self.player.x:
			self.monster_2.x -= self.monster_2.vel
			self.monster_2.down = False
			self.monster_2.up = False
			self.monster_2.left = True
			self.monster_2.right = False

if __name__ == '__main__':
	game = DogGame()

	while True:
		game.game_over, score = game.play_step()

		if game.game_over == True:
			break

	print('Final Score', score)
	pygame.quit()
