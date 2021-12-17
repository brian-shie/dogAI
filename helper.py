import pygame
import matplotlib.pyplot as plt
from IPython import display

#---------------------------------------------------------------------------
## Variables ---------------------------------------------------------------
#---------------------------------------------------------------------------

# Player ---------------------------------------------------------------------------
player_left = [
	pygame.image.load('images/sprites/animals/animals_13.png'),
	pygame.image.load('images/sprites/animals/animals_14.png'),
	pygame.image.load('images/sprites/animals/animals_15.png'),
	pygame.image.load('images/sprites/animals/animals_14.png')]

player_right = [
	pygame.image.load('images/sprites/animals/animals_25.png'),
	pygame.image.load('images/sprites/animals/animals_26.png'),
	pygame.image.load('images/sprites/animals/animals_27.png'),
	pygame.image.load('images/sprites/animals/animals_26.png')]

player_up = [
	pygame.image.load('images/sprites/animals/animals_37.png'),
	pygame.image.load('images/sprites/animals/animals_39.png'),
	pygame.image.load('images/sprites/animals/animals_37.png'),
	pygame.image.load('images/sprites/animals/animals_39.png')]

player_down = [
	pygame.image.load('images/sprites/animals/animals_01.png'),
	pygame.image.load('images/sprites/animals/animals_03.png'),
	pygame.image.load('images/sprites/animals/animals_01.png'),
	pygame.image.load('images/sprites/animals/animals_03.png')]


# Monster ---------------------------------------------------------------------------
monster_left = [
	pygame.image.load('images/deathspirit/deathspirit_22.png'),
	pygame.image.load('images/deathspirit/deathspirit_23.png'),
	pygame.image.load('images/deathspirit/deathspirit_24.png'),
	pygame.image.load('images/deathspirit/deathspirit_23.png')]

monster_right = [
	pygame.image.load('images/deathspirit/deathspirit_34.png'),
	pygame.image.load('images/deathspirit/deathspirit_35.png'),
	pygame.image.load('images/deathspirit/deathspirit_36.png'),
	pygame.image.load('images/deathspirit/deathspirit_35.png')]

monster_up = [pygame.image.load('images/deathspirit/deathspirit_46.png'),
	pygame.image.load('images/deathspirit/deathspirit_47.png'),
	pygame.image.load('images/deathspirit/deathspirit_48.png'),
	pygame.image.load('images/deathspirit/deathspirit_47.png')]

monster_down = [
	pygame.image.load('images/deathspirit/deathspirit_10.png'),
	pygame.image.load('images/deathspirit/deathspirit_11.png'),
	pygame.image.load('images/deathspirit/deathspirit_12.png'),
	pygame.image.load('images/deathspirit/deathspirit_11.png')]

# Others ---------------------------------------------------------------------------
bg = pygame.image.load('images/grassland11.png')

dogcookie = [pygame.image.load('images/dogc.png'), pygame.image.load('images/dogc2.png'),
			 pygame.image.load('images/dogc3.png'), pygame.image.load('images/dogc4.png')]


scrH, scrW = 600, 800

#---------------------------------------------------------------------------
## Plotting ----------------------------------------------------------------
#---------------------------------------------------------------------------
plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)
