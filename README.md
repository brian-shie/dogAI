# DogAI
<p align="center">
  <img src="https://brian-shie.github.io/images/dog.gif" alt="drawing" width="450"/>
</p>

## Introduction
This project is a Deep Q Learning model applied to my previously coded game. The original game is pretty simple: you control the dog with the keyboard arrows, trying to get as many cookies as possible while avoiding two monsters. So I had an idea: why not make an AI learn how to play my game? <br>

## Results
When considering only the learning factor, the initial results were satisfactory: I had succeeded in applying a DQL model using real-time inputs. A common struggle when applying reinforcement learning models is the reward signaling process. As I later found out, the rewards I tried using in my game were in a way too scarce, making it difficult for the model to learn. Curiously, the AI once understood how to exploit the game by running side to side, making the monster stuck.

## Project State
Until I learn more about signaling rewards in a better way, tweak the game so it can have less scarcity, or model the neural network in a better way, this project is on hold. Feel free to message me if you have any suggestions for improving the AI.
