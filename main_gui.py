"""Code file for running scripts with GUI
"""
import os
import pygame
import copy
import random
import re
from time import sleep  # To add delay between steps
from cell import Cell
from multiprocessing import Process

# from fire import Fire



from logger import Logger
from ship import Ship
from gui import MultiGridGUI
import bot1 as bot1s
import bot2 as bot2s
import bot1_m as bot1m
import bot2_m as bot2m

# Constants
SIZE = 30
ALPHA = .1
CELL_SIZE = 15
RANDOM_SEED = random.randint(0, 10000)
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

resultFolder = "results"
        
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)




my_ship = Ship(SIZE, RANDOM_SEED)
my_ship.createShip()
# interface1 = ShipInterface( SIZE, CELL_SIZE, 1, my_ship.getOpenCells())
r_b, c_b = random.choice(my_ship.getOpenCells())
print(f"initial bot loc : {r_b, c_b}")
my_ship.start_botloc =  (r_b, c_b)
rat_init = my_ship.getRatloc()

### Bot 1 with stationary rat
# my_ship.setRatloc(rat_init)
b1_resultPath = resultFolder+"/b1"
create_folder_if_not_exists(b1_resultPath)
b1_path = f"{b1_resultPath}/{SIZE}_{ALPHA}"
my_bot1s = bot1s.Bot(my_ship, r_b, c_b,alpha=ALPHA, seed=RANDOM_SEED, resultPath = b1_path)
getPos = my_bot1s.findPosition()
steps1s = my_bot1s.findRat()
bot1s_rat = my_ship.getRatPositions()

### Bot 1 with moving rat
my_ship.setRatloc(rat_init)
b2_resultPath = resultFolder+"/b2"
create_folder_if_not_exists(b2_resultPath)
b2_path = f"{b2_resultPath}/{SIZE}_{ALPHA}"
my_bot1m = bot1m.Bot(my_ship, r_b, c_b,alpha=ALPHA, seed=RANDOM_SEED, resultPath = b2_path)
getPos = my_bot1m.findPosition()
steps1m = my_bot1m.findRat()
bot1m_ratpos = my_ship.getRatPositions()
bot1m_rat = my_ship.getRatloc()
    
## Bot  2 with stationary rat
my_ship.setRatloc(rat_init)
b3_resultPath = resultFolder+"/b3"
create_folder_if_not_exists(b3_resultPath)
b3_path = f"{b3_resultPath}/{SIZE}_{ALPHA}"
my_bot2s = bot2s.Bot(my_ship, r_b, c_b,alpha=ALPHA, seed=RANDOM_SEED, resultPath = b3_path)
getPos = my_bot2s.findPosition()
steps2s = my_bot2s.findRat()
bot2s_rat = my_ship.getRatPositions()

### Bot  2 with moving rat
my_ship.setRatloc(rat_init)
my_ship.setRatloc(rat_init)
b4_resultPath = resultFolder+"/b4"
create_folder_if_not_exists(b4_resultPath)
b4_path = f"{b4_resultPath}/{SIZE}_{ALPHA}"
my_bot2m = bot2m.Bot(my_ship, r_b, c_b,alpha=ALPHA,  seed=RANDOM_SEED, resultPath = b4_path)
getPos = my_bot2m.findPosition()
bot2m_ratpos = my_ship.getRatPositions()

# Input files for each GUI
files_and_titles = [
(b1_path, "Baseline Bot - stationary rat"),
(b2_path, "Baseline Bot - moving rat"),
(b3_path, "Bot 2 - stationary rat"),
(b4_path, "Bot 2 - moving rat")
]

gui = MultiGridGUI(files_and_titles, "Multi-Bot Simulation")
gui.run()





