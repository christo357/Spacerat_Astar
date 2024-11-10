from main import CELL_SIZE
import pygame
import re

CELL_SIZE = 15

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FIRE_COLOR = (255, 69, 0)


class ShipInterface:
    def __init__(self, size, bot_count):
        self.size = size
        self.bot_count = bot_count
        
        self.cell_size = CELL_SIZE
        self.window_width = self.size * self.cell_size
        self.window_height = self.size * self.cell_size
        
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Space Rat Simulation")
        
        #load images 
        self.bot_img = []
        self.rat_image = pygame.image.load('images/rat.png')
        self.rat_image = pygame.transform.scale(self.rat_image, (self.cell_size, self.cell_size))
        
        for i in range(0, self.bot_count):
            imgPath = f'botimg/bot{i+1}.png'
            bot_image = pygame.image.load(imgPath)
            bot_image = pygame.transform.scale(bot_image, (CELL_SIZE, CELL_SIZE))
            self.bots_img.append(bot_image)
            
    
    def replay_grid(self, resultPath):
        with open(resultPath, 'r') as file:
            content = file.read().split("-"*40)
            
            metadata = content.pop(0).strip().split("\n")
            initial_bot_loc = re.search(r"Initial Bot Location: \((\d+), (\d+)\)", metadata[2])
            switch_loc = re.search(r"Switch Location: \((\d+), (\d+)\)", metadata[3])
            rat_row = int(switch_loc.group(1))
            rat_col = int(switch_loc.group(2))
            bot_r = int(initial_bot_loc.group(1))
            bot_c = int(initial_bot_loc.group(2))
            bots_pos =  [(bot_r, bot_c), (bot_r, bot_c), (bot_r, bot_c), (bot_r, bot_c)]
        