import pygame
import sys
import re
from time import sleep
from multiprocessing import Process

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class GridGUI:
    def __init__(self, file_name, window_title):
        self.file_name = file_name
        self.grid_size = (30, 30)  # Fixed grid size
        self.cell_size = 20
        self.bot_pos = (0, 0)
        self.rat_pos = (0, 0)
        self.visited_cells = set()
        self.timesteps = []
        self.current_timestep = 0
        # self.load_data()
        self.screen_size = (
            self.grid_size[0] * self.cell_size,
            self.grid_size[1] * self.cell_size,
        )
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(window_title)
        # self.font = pygame.font.Font(None, 24)
        # self.clock = pygame.time.Clock()
        self.running = True
        self.bot_image = pygame.image.load("images/bot1.png").convert_alpha()
        self.bot_image = pygame.transform.scale(self.bot_image, (self.cell_size, self.cell_size))
        self.rat_image = pygame.image.load("images/rat.png").convert_alpha()
        self.rat_image = pygame.transform.scale(self.rat_image, (self.cell_size, self.cell_size))

    
                
    def run(self):
        rat_image = pygame.image.load("images/rat.png")
        rat_image = pygame.transform.scale(rat_image, (self.cell_size, self.cell_size))

        bot_image = pygame.image.load("images/bot1.png")
        bot_image = pygame.transform.scale(bot_image, (self.cell_size, self.cell_size))
        
        with open(self.file_name, "r") as file:
            content = file.read().split("-" * 40)
            
            # Read metadata (first part before the first separator)
            metadata = content.pop(0).strip().split("\n")
            # grid_size = re.search(r"Grid Size: (\d+)x(\d+)", metadata[0])
            # grid_width = int(grid_size.group(1))
            # grid_height = int(grid_size.group(2))
            
            # Get bot initial location and switch location
            # initial_bot_loc = re.search(r"Initial Bot Location: \((\d+), (\d+)\)", metadata[1])
            # rat_loc = re.search(r"Rat Location: \((\d+), (\d+)\)", metadata[2])
            # rat_row = int(rat_loc.group(1))
            # rat_col = int(rat_loc.group(2))
            # bot_r = int(initial_bot_loc.group(1))
            # bot_c = int(initial_bot_loc.group(2))
            
            for step in content:
                if step.strip():
                    lines = step.strip().split("\n")
                    timestep_line = lines[0]  # Timestep line
                    grid_lines = lines[1:-3]  # Grid state
                    
                    startpos_info = lines[-3].split(": ")[1].strip("()").split(", ")
                    startpos_row, startpos_col = int(startpos_info[0]), int(startpos_info[1])
                    startpos =  (startpos_row, startpos_col)
                    
                    bot_info = lines[-2].split(": ")[1].strip("()").split(", ")
                    bot_row, bot_col = int(bot_info[0]), int(bot_info[1])
                    bots_pos =  (bot_row, bot_col)
                    
                    rat_info = lines[-1].split(": ")[1].strip("()").split(", ")
                    rat_row, rat_col = int(rat_info[0]), int(rat_info[1])
                    rats_pos =  (rat_row, rat_col)
                    
                    # Recreate grid display
                    for row in range(self.grid_size[0]):
                        for col in range(self.grid_size[1]):
                            cell_value = grid_lines[row][col]

                            if (row, col) == startpos and startpos != (0,0):
                                color = BLUE
                                pygame.draw.rect(self.screen, color, pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                            if cell_value == 'o':
                                color = WHITE  # Open space cells
                                pygame.draw.rect(self.screen, color, pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                            elif cell_value == 'b':
                                color = BLACK  # Default ship area
                                pygame.draw.rect(self.screen, color, pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

                            # Draw grid lines
                            pygame.draw.rect(self.screen, BLACK, pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)

                    # Redraw bot and switch
                    self.screen.blit(rat_image, (rat_col * self.cell_size, rat_row * self.cell_size))
                    self.screen.blit(bot_image, (bot_col * self.cell_size, bot_row * self.cell_size))
                    pygame.display.update()

                    sleep(.5)  # Delay between timesteps
                    
            sleep(2)
            pygame.quit()
            sys.exit()