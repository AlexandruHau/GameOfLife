# Import the numpy and matplotlib libraries for creating 2D-array
# and for making animations of the time-dependent lattice. Also
# use pandas library for storing the avaialble data into a .csv 
# file and seaborn as additional plotting library. Sys library is
# imported to implement values from the terminal execution line 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import seaborn as sns
import sys

# Generate a grid representing the game of life - standard choice is
# of (50,50). Fill it with dead or alive cells as follows:
# 1 = ALIVE
# 0 = DEAD
# There are no other states, and the grid is randomly filled
def GenerateGrid(N):
	game = np.random.randint(2, size=(N,N))
	return game

# Some specific coordinates are chosen for generating a spaceship in the
# Game of Life model. In this instance, the initial cell keeps its shape 
# during the evolution time	
def GenerateSpaceship(N):
	game = np.zeros((N,N))
	i = 23
	j = 23
	game[i][j] = 1
	game[i][(j+1)%N] = 1
	game[i][(j-1)%N] = 1
	game[(i-1)%N][(j+1)%N] = 1
	game[(i-2)%N][j] = 1	
	
	return game
	
def GenerateOscillator(N):
	game = np.zeros((N,N))
	i = 20
	j = 20
	
	# Initialize all the following states with 1 for obtaining an
	# oscillating state
	game[i][j] = 1
	game[i][j+1] = 1
	game[i][j+2] = 1
	game[(i-1)%N][(j+2)%N] = 1
	game[(i+1)%N][(j+2)%N] = 1
	
	game[(i-1)%N][(j+5)%N] = 1
	game[i][(j+5)%N] = 1
	game[(i+1)%N][(j+5)%N] = 1
	
	game[i][(j+6)%N] = 1
	game[i][(j+7)%N] = 1
	game[i][(j+8)%N] = 1
	game[i][(j+9)%N] = 1
	
	game[i][(j+10)%N] = 1
	game[(i-1)%N][(j+10)%N] = 1
	game[(i+1)%N][(j+10)%N] = 1
	
	game[i][(j+13)%N] = 1
	game[(i-1)%N][(j+13)%N] = 1
	game[(i+1)%N][(j+13)%N] = 1
	
	game[i][(j+14)%N] = 1
	game[i][(j+15)%N] = 1
	
	return game

# List comprehension method for working out the number of neighbors of an element (alive neighbors). 
# The np.roll method shifts all the elements in an array to a specific direction    
def FindNeighbors(game):
	neighbors = np.roll(game, 1, axis=1) + np.roll(game, -1, axis=1) + np.roll(game, 1, axis=0) + np.roll(game, -1, axis=0) 
	neighbors += np.roll(np.roll(game, 1, axis=1), 1, axis=0)  
	neighbors += np.roll(np.roll(game, 1, axis=1), -1, axis=0) 
	neighbors += np.roll(np.roll(game, -1, axis=1), -1, axis=0)
	neighbors += np.roll(np.roll(game, -1, axis=1), 1, axis=0)    
	return neighbors

# Update the grid through the following rule: any alive cell with two or three neighbors stays alive.
# Any dead cell with exactly three neighbors becomes alive. All the other cells are dead. All the cells
# are updated automatically	
def UpdateGame(game):
	neighbors = FindNeighbors(game)
	game[np.where(((neighbors == 2) | (neighbors == 3)) & (game == 1))] = 1
	game[np.where(((neighbors < 2) | (neighbors > 3)) & (game == 1))] = 0
	game[np.where((neighbors == 3) & (game == 0))] = 1
	game[np.where((neighbors != 3) & (game == 0))] = 0
	return game

###
### PART A: PLOT THE LIVE ANIMATION OF THE GAME OF LIFE
### INVOKE THE FUNCTION BELOW FOR PART A
###

# Plot the grid at each timestep on the matplotlib platform	
def PlotGame(game):
	count = 0
	time = 0
	i = 0
	while(count < 1):
		game = UpdateGame(game)
		plt.cla()
		plt.imshow(game, animated=True)
		plt.title("Game of Life model")
		if(i == 0):
			plt.colorbar()
		plt.draw()
		plt.pause(0.001)
		i += 1

# Calculate the life time of the system. Do this by registering a time variable which 
# increases by 1 after each grid update. Calculate the shift in the number of the alive
# cells (birth rate). When the birth rate becomes 0 and stays 0 for a limited number of
# updates, return the lifetime		
def LifeTime(game):

	# Variable used for running in the while loop until we reach the stable state
	count = 0
	
	# List for storing the birth rates. The variables for time limit regarding 
	# constant population level and time varoables are also there
	birth_count = []
	limit = 50
	time = 0
	constant_lvl = 0
	
	# Test array filled with elements of 2 is also required
	test_arr = np.ones(limit) * 2
	while(count < 1):
		
		# Limit case when time overreaches 5000 units
		if(time > 5000):
			return 0
				
		# Update the time and calculate the difference in population
		# (additional alive or dead cells)
		time += 1
		n_initial = len(game[game == 1])
		game = UpdateGame(game)
		n_final = len(game[game == 1])
		d_n = np.abs(n_final - n_initial)
		
		# Append the rate of population change to the array
		np.append(birth_count, d_n)
		
		# Analyse if there is no population change
		if(d_n != 0):
		
			# Set the count for constant population to 0
			constant_lvl = 0
			
		else:
			# The count for constant population is updated
			constant_lvl += 1
			
			# If the limit is reached then return the lifetime	
			if((constant_lvl == limit)):
				return (time - limit)
				count = 2
###
### PART B: INVOKE THIS FUNCTION FOR THE SECOND PART
###
				
def AnalyseLifeTime():

	# Array for storing the life time of the Game of Life. For each element in the
	# loop, a Game Of Life grid is generated. The data is saved in a .csv file
	life = []
	for i in range(2000):
		game = GenerateGrid(50)
		lifetime = LifeTime(game)
		print("Life time: " + str(lifetime) + " at simulation: " + str(i))
		if(lifetime != 0):
			life.append(lifetime)
	
	df = pd.DataFrame({"Mean lifetime" : np.array(life)})
	df.to_csv("Lifetime.csv")
				
def FindPos(game):

	# Find the length of the array
	N = len(game)
	
	# Retrieve the arrays of row and column indices
	pos = np.indices((N,N))
	
	# Find the x and y coordinates for the centre of mass
	# Do this by working out the overall number of alive cells
	n = len(game[game == 1])
	x = np.sum(np.multiply(pos[0], game)) / n
	y = np.sum(np.multiply(pos[1], game)) / n
	
	return x,y

### 
### PART C: INVOKE THIS FUNCTION FOR THE LAST PART IN THE
### GAME OF LIFE MODEL
###
	
def PlotPos():

	# Generate the spaceship
	game = GenerateSpaceship(50)

	# Create a time array
	T = np.arange(200)
	X = np.zeros(200)
	Y = np.zeros(200)
	
	# Work in the time range
	for time in T:
	
		x,y = FindPos(game)
		game = UpdateGame(game)
		X[np.argwhere(T == time)] = x
		Y[np.argwhere(T == time)] = y
		
	df = pd.DataFrame({"X_pos" : X, "Y_pos" : Y, "T_time" : T})
	df.to_csv("CM_coordinates.csv")
									
def main():
	
	ok = int(input("Introduce the following command: " + "\n" + "(0) Plot the Game of Life for random system" + "\n" 
		+ "(1) GoL Model for spaceship: " + "\n" +"(2) GoL Model for oscillator: " + "\n" + "(3) Lifetime of a grid: " + "\n"
		+ "(4) Center of Mass Evolution: \n"
		+ "Place here your command: "))
	
	# Take each case
	if(ok == 0):
		game = GenerateGrid(50)
		PlotGame(game)
	
	elif(ok == 1):
		game = GenerateSpaceship(50)
		PlotGame(game)
		
	elif(ok == 2):
		game = GenerateOscillator(50)
		PlotGame(game)
		
	elif(ok == 3):
		AnalyseLifeTime()
	
	elif(ok == 4):
		PlotPos()
		
	else:
		raise Exception("Introduce an integer between 0 and 3!!")
main()
			
