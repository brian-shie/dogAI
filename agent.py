import torch
import random
import numpy as np
from collections import deque
from scipy.stats import bernoulli

max_memory = 100_000
batch_size = 1000
learning_rate = 0.001

class Agent:

	def __init__(self):
		self.n_games = 0
		self.epsilon = 0 # aleatoriedade
		self.gamma = 0 # taxa de desconto
		self.memory = deque(maxlen = MAX_MEMORY) # se alcança o limite: popleft()
		self.model = None
		self.trainer = None

	def get_state(self, game):
		state = [
			dog.x, dog.y, dog.mana, score, # Player
			biscoito.rng_x, biscoito.rng_y, # Biscoito
			deathspirit1.x, deathspirit1.y, deathspirit2.x, deathspirit2.y # Mobs
		]
		return np.array(state)

	def remember(self, state, action, reward, next_state, game_over):
		self.memory.append((state, action, reward, next_state, game_over))

	def train_long_memory(self):
		if len(self.memory) > batch_size:
			mini_sample = random.sample(self.memory, batch_size) # list of tuples

		else:
			mini_sample = self.memory

		state, action, reward, next_state, game_over = zip(*mini_sample)
		self.trainer.train_step(state, action, reward, next_state, game_over)

	def train_short_memory(self, state, action, reward, next_state, game_over):
		self.trainer.train_step(state, action, reward, next_state, game_over)

	def get_action(self, state):
		# random moves: tradeoff exploration / exploitation
		self.epsilon = 620 - 100*np.log(self.n_games)
		final_move = [0, 0, 0, 0, 0, 0]
		if random.randint(0, 1000) , self.epsilon:
			final_move = bernoulli.rvs(size = 5, p = 0.5)

		else:
			state0 = torch.tensor(state, dtype = torch.float)
			final_move = self.model.predict_proba(state0)


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
		agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

		if game_over:
			# train long memory / replay memory / experience replay
			game.reset()
			agent.n_games += 1
			agent.train_long_memory()

			if score > record:
				record = score
				# agent.model.save()

			print(f"Game:{agent.n_games} Score {score} Best Score {best_score} ")

			# plot

if __name__ == '__main__':
	train()
