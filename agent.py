import torch
import random
import numpy as np
from collections import deque
from scipy.stats import bernoulli
from model import Linear_QNet, QTrainer
from dogAI import DogGameAI
from helper import plot

max_memory = 100_000
batch_size = 1000
learning_rate = 0.0001

class Agent:

	def __init__(self):
		self.n_games = 0
		self.epsilon = 0 # aleatoriedade
		self.gamma = 0.95 # taxa de desconto
		self.memory = deque(maxlen = max_memory) # se alcança o limite: popleft()
		self.model = Linear_QNet(18, 128, 8)
		self.trainer = QTrainer(self.model, lr=learning_rate, gamma=self.gamma)

	def _binning(x):
		return np.floor(x/20)



	def get_state(self, game):
		state = [
			np.floor(game.player.x), np.floor(game.player.y), # game.player.mana, # Player
			np.floor(game.player.x - game.biscoito.x), np.floor(game.player.y - game.biscoito.y), # Biscoito
			np.floor(game.player.x - game.monster_1.x),  np.floor(game.player.y - game.monster_1.y),
			np.floor(game.player.x - game.monster_2.x), np.floor(game.player.y - game.monster_2.y),  # Mobs

			game.monster_1.x - 40 <= game.player.x <= game.monster_1.x + 40,
			game.monster_1.y - 40 <= game.player.y <= game.monster_1.y + 40,
			game.monster_2.x - 40 <= game.player.x <= game.monster_2.x + 40,
			game.monster_2.y - 40 <= game.player.y <= game.monster_2.y + 40,

			game.biscoito.x * 40 - 64 <= game.player.x <= game.biscoito.x * 40 + 48,
			game.biscoito.y * 40 - 64 <= game.player.y <= game.biscoito.y * 40 + 32,

			game.player.x < game.player.vel,
			game.player.x > scrW - game.player.width - game.player.vel,
			game.player.y < game.player.vel,
			game.player.y > scrH - game.player.height - game.player.vel
		]

		return state

	def remember(self, state, action, reward, next_state, game_over):
		self.memory.append((state, action, reward, next_state, game_over))

	def train_long_memory(self):
		if len(self.memory) > batch_size:
			mini_sample = random.sample(self.memory, batch_size) # list of tuples

		else:
			mini_sample = self.memory

		states, actions, rewards, next_states, game_overs = zip(*mini_sample)
		self.trainer.train_step(states, actions, rewards, next_states, game_overs)

	def train_short_memory(self, state, action, reward, next_state, game_over):
		self.trainer.train_step(state, action, reward, next_state, game_over)

	def get_action(self, state):
		# random moves: tradeoff exploration / exploitation
		# self.epsilon = 620 - 100*np.log(self.n_games)
		self.epsilon = 100 - self.n_games
		final_move = [0, 0, 0, 0]
		if random.randint(0, 160) < self.epsilon:
			# final_move = bernoulli.rvs(size = 5, p = 0.5)
			move = random.randint(0,7)
			if move == 4:
				final_move = [1, 0, 1, 0]

			elif move == 5:
				final_move = [1, 0, 0, 1]

			elif move == 6:
				final_move = [0, 1, 1, 0]

			elif move == 7:
				final_move = [0, 1, 0, 1]

			else:
				final_move[move] = 1

			# print(final_move)

		else:
			# print(state)
			state0 =  torch.tensor(state, dtype=torch.float)
			prediction = self.model(state0)
			move = torch.argmax(prediction).item()

			if move == 4:
				final_move = [1, 0, 1, 0]

			elif move == 5:
				final_move = [1, 0, 0, 1]

			elif move == 6:
				final_move = [0, 1, 1, 0]

			elif move == 7:
				final_move = [0, 1, 0, 1]

			else:
				final_move[move] = 1

		return final_move

def train():
	plot_scores = []
	plot_mean_scores = []
	total_score = 0
	best_score = 0
	agent = Agent()
	game = DogGameAI()
	while True:
		# get old state
		state_old = agent.get_state(game)

		# get move
		final_move = agent.get_action(state_old)

		# perform move and get new state
		reward, done, score = game.play_step(final_move)
		state_new = agent.get_state(game)

		# train short memory
		agent.train_short_memory(state_old, final_move, reward, state_new, game.game_over)

		# remember
		agent.remember(state_old, final_move, reward, state_new, game.game_over)

		if game.game_over:
			# train long memory / replay memory / experience replay
			game.reset()
			agent.n_games += 1
			agent.train_long_memory()

			if score > best_score:
				best_score = score
				agent.model.save()

			print(f"Game:{agent.n_games} Score {score} Best Score {best_score} ")

			# plot_scores.append(score)
			# total_score += score
			# mean_score = total_score / agent.n_games
			# plot_mean_scores.append(mean_score)
			# plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
	train()
