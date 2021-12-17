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
learning_rate = 0.005

class Agent:

	def __init__(self):
		self.n_games = 0
		self.epsilon = 0 # aleatoriedade
		self.gamma = 0 # taxa de desconto
		self.memory = deque(maxlen = max_memory) # se alcança o limite: popleft()
		self.model = Linear_QNet(10, 256, 5)
		self.trainer = QTrainer(self.model, lr=learning_rate, gamma=self.gamma)

	def get_state(self, game):
		state = [
			game.player.x, game.player.y, game.player.mana, game.score, # Player
			game.biscoito.x, game.biscoito.y, # Biscoito
			game.monster_1.x, game.monster_1.y, game.monster_2.x, game.monster_2.y # Mobs
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
		self.epsilon = 150 - self.n_games
		final_move = [0, 0, 0, 0, 0, 0]
		if random.randint(0, 200) < self.epsilon:
			final_move = torch.tensor(bernoulli.rvs(size = 5, p = 0.5), dtype = int)

		else:
			state0 =  torch.tensor(state, dtype=torch.float)
			final_move = self.model(state0)
			print(final_move)

		# print(type(final_move))

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

			plot_scores.append(score)
			total_score += score
			mean_score = total_score / agent.n_games
			plot_mean_scores.append(mean_score)
			plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
	train()
