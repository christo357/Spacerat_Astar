import os
import pygame
import copy
import random
import re
from time import sleep  # To add delay between steps
from cell import Cell
# from fire import Fire



from logger import Logger
from ship import Ship
from ui import ShipInterface
import bot1 as bot1s
import bot2 as bot2s
import bot1_m as bot1m
import bot1_m_copy as bot2m

# Constants
SIZE = 30
ALPHA = .1
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
        
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Rat Simulation")

RANDOM_SEED = random.randint(0, 10000)
my_ship = Ship(SIZE, RANDOM_SEED)
my_ship.createShip()
interface1 = ShipInterface( SIZE, CELL_SIZE, 1, my_ship.getOpenCells())
r_b, c_b = random.choice(my_ship.getOpenCells())
print(f"initial bot loc : {r_b, c_b}")
my_ship.start_botloc =  (r_b, c_b)
rat_init = my_ship.getRatloc()



### Bot 1 with stationary rat
# my_ship.setRatloc(rat_init)
my_bot1s = bot1s.Bot(my_ship, r_b, c_b,alpha=ALPHA, interface=interface1, seed=RANDOM_SEED)
getPos = my_bot1s.findPosition()
bot1s_len = len(my_ship.ratPositions)

if getPos:
    print("FINDING RAT")
    steps1s = my_bot1s.findRat()
    bot1s_rat = my_ship.getRatPositions()
    

## Bot  2 with stationary rat
my_ship.setRatloc(rat_init)
my_bot2s = bot2s.Bot(my_ship, r_b, c_b,alpha=ALPHA, interface=interface1, seed=RANDOM_SEED)
getPos = my_bot2s.findPosition()
bot2s_len = len(my_ship.ratPositions)

if getPos:
    print("FINDING RAT")
    steps2s = my_bot2s.findRat()
    bot2s_rat = my_ship.getRatPositions()




### Bot 1 with moving rat
my_ship.setRatloc(rat_init)
my_bot1m = bot1m.Bot(my_ship, r_b, c_b,alpha=ALPHA, interface=interface1, seed=RANDOM_SEED)
getPos = my_bot1m.findPosition()
bot1m_len = len(my_ship.ratPositions)

if getPos:
    print("FINDING RAT")
    steps1m = my_bot1m.findRat()
    bot1m_ratpos = my_ship.getRatPositions()
    bot1m_rat = my_ship.getRatloc()

### Bot  2 with moving rat
my_ship.setRatloc(rat_init)
my_bot2m = bot2m.Bot(my_ship, r_b, c_b,alpha=ALPHA, interface=interface1, seed=RANDOM_SEED)
getPos = my_bot2m.findPosition()
bot2m_len = len(my_ship.ratPositions)

if getPos:
    print("FINDING RAT")
    steps2m = my_bot2m.findRat()
    bot2m_ratpos = my_ship.getRatPositions()
    bot2m_rat = my_ship.getRatloc()
    
    
    
print(f"Bot 1 rat len: {bot1s_len}")
# print(f"Bot 1 rat: {bot1s_rat}")
print(f"Total steps: bot1: {steps1s}, rat: {bot1s_rat}")


print(f"Bot 1 rat len: {bot1m_len}")
# print(f"Bot 1 rat: {bot1m_rat}")
print(f"Total steps: bot1: {steps1m}, rat: {bot2s_rat}")

print(f"Bot 2 rat len: {bot2s_len}")
# print(f"Bot 2 rat: {bot2s_rat}")
print(f"Total steps: bot2: {steps2s}, rat: {bot1m_rat}")

print(f"Bot 2 rat len: {bot2m_len}")
# print(f"Bot 2 rat: {bot2m_rat}")
print(f"Total steps: bot2: {steps2m}, rat: {bot2m_rat}")








# def initializePygame():
#     pygame.init()
#     # Create pygame window
#     window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#     pygame.display.set_caption("Ship Fire Simulation")
    
# # Function to log metadata (grid size, bot, and switch location) to result.txt
# def log_metadata(ship, resultPath):
    
#     with open(resultPath, "w") as file:
#         file.write(f"Grid Size: {GRID_WIDTH}x{GRID_HEIGHT}\n")
#         # file.write(f"Flammability: {ship.get_q()}\n")
#         # file.write(f'Bot : {bot.get_Id()}\n')
#         bot_row, bot_col = ship.getStartBotLoc()
#         rat_row, rat_col = ship.getRatloc()
#         file.write(f"Initial Bot Location: ({bot_row}, {bot_col})\n")
#         file.write(f"Switch Location: ({rat_row}, {rat_col})\n")
#         file.write("-" * 40 + "\n")

# # Function to log the grid state to result.txt at each timestep
# def log_grid_state(ship, timestep, bot_count, resultPath):
#     with open(resultPath, "a") as file:
#         file.write(f"Timestep: {timestep}\n")
#         for row in range(GRID_HEIGHT):
#             for col in range(GRID_WIDTH):
#                 file.write(ship.get_cellval(row, col))
#             file.write("\n")
        
#         bot_row, bot_col = ship.getBotLoc(i)
#         file.write(f"Bot {i+1}: ({bot_row}, {bot_col})\n")
#         file.write("-" * 40 + "\n")