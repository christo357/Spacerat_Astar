""" code file of the gui interface for visualizing the projects
"""

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

class MultiGridGUI:
    def __init__(self, file_data, window_title):
        self.file_data = file_data  # List of tuples: [(file_name, bot_name), ...]
        self.grid_size = (30, 30)  # Fixed grid size
        self.cell_size = 10
        self.screen_size = (self.grid_size[0] * self.cell_size * 2, 
                            self.grid_size[1] * self.cell_size * 2)
        self.bot_images = {}
        self.rat_images = {}
        self.timesteps = []
        self.current_timestep = 0  # Initialize current timestep
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(window_title)
        self.load_assets()
        self.parse_files()

    def load_assets(self):
        bot_image = pygame.image.load("images/bot1.png").convert_alpha()
        bot_image = pygame.transform.scale(bot_image, (self.cell_size, self.cell_size))
        rat_image = pygame.image.load("images/rat.png").convert_alpha()
        rat_image = pygame.transform.scale(rat_image, (self.cell_size, self.cell_size))
        for i in range(4):
            self.bot_images[f"bot{i+1}"] = bot_image
            self.rat_images[f"rat{i+1}"] = rat_image

    def parse_files(self):
        for file_name, bot_name in self.file_data:
            with open(file_name, "r") as file:
                content = file.read().split("-" * 40)
                timesteps = []
                for step in content[1:]:
                    if step.strip():
                        lines = step.strip().split("\n")
                        grid_lines = lines[1:-3]
                        bot_info = lines[-2].split(": ")[1].strip("()").split(", ")
                        rat_info = lines[-1].split(": ")[1].strip("()").split(", ")
                        timesteps.append({
                            "grid": grid_lines,
                            "bot_pos": (int(bot_info[0]), int(bot_info[1])),
                            "rat_pos": (int(rat_info[0]), int(rat_info[1]))
                        })
                self.timesteps.append(timesteps)

    def draw_grid(self, grid_data, offset_x, offset_y):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                cell_value = grid_data["grid"][row][col]
                if cell_value == 'o':
                    color = WHITE  # Open space
                elif cell_value == 'b':
                    color = BLACK  # Blocked
                else:
                    color = WHITE
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    pygame.Rect(
                        offset_x + col * self.cell_size,
                        offset_y + row * self.cell_size,
                        self.cell_size, self.cell_size
                    )
                )
                pygame.draw.rect(
                    self.screen, BLACK,
                    pygame.Rect(
                        offset_x + col * self.cell_size,
                        offset_y + row * self.cell_size,
                        self.cell_size, self.cell_size), 1)

        # Draw bot and rat
        bot_x, bot_y = grid_data["bot_pos"]
        rat_x, rat_y = grid_data["rat_pos"]
        self.screen.blit(
            self.bot_images["bot1"], 
            (offset_x + bot_y * self.cell_size, offset_y + bot_x * self.cell_size))
        self.screen.blit(
            self.rat_images["rat1"], 
            (offset_x + rat_y * self.cell_size, offset_y + rat_x * self.cell_size))

    def draw_separators(self):
        """Draw lines to separate the grids."""
        mid_x = self.grid_size[0] * self.cell_size
        mid_y = self.grid_size[1] * self.cell_size

        # Vertical line in the center
        pygame.draw.line(self.screen, BLUE, (mid_x, 0), (mid_x, self.screen_size[1]), 2)

        # Horizontal line in the center
        pygame.draw.line(self.screen, BLUE, (0, mid_y), (self.screen_size[0], mid_y), 2)

    def run(self):
        max_timesteps = max(len(steps) for steps in self.timesteps)
        while self.running and self.current_timestep < max_timesteps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(WHITE)  # Clear screen
            for i, bot_timesteps in enumerate(self.timesteps):
                grid_offset_x = (i % 2) * self.grid_size[0] * self.cell_size
                grid_offset_y = (i // 2) * self.grid_size[1] * self.cell_size
                
                # Handle bots with fewer timesteps
                if self.current_timestep < len(bot_timesteps):
                    grid_data = bot_timesteps[self.current_timestep]
                else:
                    # Freeze at the last state
                    grid_data = bot_timesteps[-1]
                
                self.draw_grid(grid_data, grid_offset_x, grid_offset_y)

            # Draw separators
            self.draw_separators()

            pygame.display.update()
            sleep(0.5)  # Synchronize timestep progression
            self.current_timestep += 1

        sleep(2)
        pygame.quit()
        sys.exit()