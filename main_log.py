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
from gui import GridGUI 
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
          

# pygame.init()
# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption("Space Rat Simulation")


my_ship = Ship(SIZE, RANDOM_SEED)
my_ship.createShip()
# interface1 = ShipInterface( SIZE, CELL_SIZE, 1, my_ship.getOpenCells())
r_b, c_b = random.choice(my_ship.getOpenCells())
print(f"initial bot loc : {r_b, c_b}")
my_ship.start_botloc =  (r_b, c_b)
rat_init = my_ship.getRatloc()

# logger = Logger(SIZE, my_ship, resultPath)
# logger.log_metadata()


# ### Bot 1 with stationary rat
# # my_ship.setRatloc(rat_init)
# b1_resultPath = resultFolder+"/b1"
# create_folder_if_not_exists(b1_resultPath)
# b1_path = f"{b1_resultPath}/{SIZE}_{ALPHA}"
# my_bot1s = bot1s.Bot(my_ship, r_b, c_b,alpha=ALPHA, seed=RANDOM_SEED, resultPath = b1_path)
# getPos = my_bot1s.findPosition()
# bot1s_len = len(my_ship.ratPositions)

# if getPos is not (0,0):
#     print("FINDING RAT")
#     steps1s = my_bot1s.findRat()
#     bot1s_rat = my_ship.getRatPositions()
    
### Bot 1 with moving rat
my_ship.setRatloc(rat_init)
b2_resultPath = resultFolder+"/b2"
create_folder_if_not_exists(b2_resultPath)
b2_path = f"{b2_resultPath}/{SIZE}_{ALPHA}"
my_bot1m = bot1m.Bot(my_ship, r_b, c_b,alpha=ALPHA, seed=RANDOM_SEED, resultPath = b2_path)
getPos = my_bot1m.findPosition()
bot1m_len = len(my_ship.ratPositions)

if getPos:
    print("FINDING RAT")
    steps1m = my_bot1m.findRat()
    bot1m_ratpos = my_ship.getRatPositions()
    bot1m_rat = my_ship.getRatloc()
    
    
# ## Bot  2 with stationary rat
# my_ship.setRatloc(rat_init)
# b3_resultPath = resultFolder+"/b3"
# create_folder_if_not_exists(b3_resultPath)
# b3_path = f"{b3_resultPath}/{SIZE}_{ALPHA}"
# my_bot2s = bot2s.Bot(my_ship, r_b, c_b,alpha=ALPHA, seed=RANDOM_SEED, resultPath = b3_path)
# getPos = my_bot2s.findPosition()
# bot2s_len = len(my_ship.ratPositions)

# if getPos:
#     print("FINDING RAT")
#     steps2s = my_bot2s.findRat()
#     bot2s_rat = my_ship.getRatPositions()






### Bot  2 with moving rat
my_ship.setRatloc(rat_init)
my_ship.setRatloc(rat_init)
b4_resultPath = resultFolder+"/b4"
create_folder_if_not_exists(b4_resultPath)
b4_path = f"{b4_resultPath}/{SIZE}_{ALPHA}"
my_bot2m = bot2m.Bot(my_ship, r_b, c_b,alpha=ALPHA,  seed=RANDOM_SEED, resultPath = b4_path)
getPos = my_bot2m.findPosition()
bot2m_len = len(my_ship.ratPositions)

if getPos:
    print("FINDING RAT")
    steps2m = my_bot2m.findRat()
    bot2m_ratpos = my_ship.getRatPositions()
    bot2m_rat = my_ship.getRatloc()
    
    
    
# print(f"Bot 1s rat len: {bot1s_len}")
# # print(f"Bot 1 rat: {bot1s_rat}")
# print(f"Total steps: bot1s: {steps1s}, rat: {bot1s_rat}")


print(f"Bot 1m rat len: {bot1m_len}")
# print(f"Bot 1 rat: {bot1m_rat}")
print(f"Total steps: bot1m: {steps1m}, rat: {bot1m_rat}")

# print(f"Bot 2s rat len: {bot2s_len}")
# # print(f"Bot 2 rat: {bot2s_rat}")
# print(f"Total steps: bot2s: {steps2s}, rat: {bot2s_rat}")

print(f"Bot 2m rat len: {bot2m_len}")
# print(f"Bot 2 rat: {bot2m_rat}")
print(f"Total steps: bot2m: {steps2m}, rat: {bot2m_rat}")


# def start_gui(file_name, window_title):
#     gui = GridGUI(file_name, window_title)
#     gui.run()

# if __name__ == "__main__":
#     # Input files for each GUI
#     files_and_titles = [
#         ("grid_file1.txt", "Grid GUI 1"),
#         ("grid_file2.txt", "Grid GUI 2"),
#         ("grid_file3.txt", "Grid GUI 3")
#     ]
    
#     # Start a process for each GUI
#     processes = []
#     for file_name, window_title in files_and_titles:
#         p = Process(target=start_gui, args=(file_name, window_title))
#         p.start()
#         processes.append(p)
    
#     # Wait for all processes to complete
#     for p in processes:
#         p.join()






