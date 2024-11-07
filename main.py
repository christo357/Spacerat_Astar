import os
import pygame
import copy
import random
import re
from time import sleep  # To add delay between steps
from cell import Cell
# from fire import Fire
from ship import Ship
import bot

# Constants
SIZE = 40
CELL_SIZE = 15
GRID_WIDTH = SIZE
GRID_HEIGHT = SIZE
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FIRE_COLOR = (255, 69, 0)


def initializePygame():
    pygame.init()
    # Create pygame window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ship Fire Simulation")
    
# Function to log metadata (grid size, bot, and switch location) to result.txt
def log_metadata(ship, resultPath):
    
    with open(resultPath, "w") as file:
        file.write(f"Grid Size: {GRID_WIDTH}x{GRID_HEIGHT}\n")
        # file.write(f"Flammability: {ship.get_q()}\n")
        # file.write(f'Bot : {bot.get_Id()}\n')
        bot_row, bot_col = ship.getStartBotLoc()
        rat_row, rat_col = ship.getRatloc()
        file.write(f"Initial Bot Location: ({bot_row}, {bot_col})\n")
        file.write(f"Switch Location: ({rat_row}, {rat_col})\n")
        file.write("-" * 40 + "\n")

# Function to log the grid state to result.txt at each timestep
def log_grid_state(ship, timestep, bot_count, resultPath):
    with open(resultPath, "a") as file:
        file.write(f"Timestep: {timestep}\n")
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                file.write(ship.get_cellval(row, col))
            file.write("\n")
        
        bot_row, bot_col = ship.getBotLoc(i)
        file.write(f"Bot {i+1}: ({bot_row}, {bot_col})\n")
        file.write("-" * 40 + "\n")
        

my_ship = Ship(SIZE)
my_ship.createShip()
r_b, c_b = random.choice(my_ship.getOpenCells())
print(f"initial bot loc : {r_b, c_b}")
my_ship.start_botloc =  (r_b, c_b)
my_bot = bot.Bot(my_ship, r_b, c_b)
my_bot.createPossibleloc()
    # run_simulation(my_ship, r_b, c_b, bot_count, simulationPath, resultPath, stepPath, fileName)
loc_found = 0
sensed = 0  
t= 0 
while loc_found==0 and t<50:
    
    print("\nCurr_positon; ", my_bot.getloc())
    t +=1
    if sensed == 0:
        my_bot.senseNeighbors() 
        sensed = 1
    else:
        dir = my_bot.detectCommonDir()
        r_disp, c_disp = my_bot.moveBot(dir)
        print(f'T{t}: {r_disp, c_disp}')
        sensed = 0
    if my_bot.get_possibleloclen() ==1:
        loc_found = 1
        my_bot.updateknownloc()
    