""" another gui interface for visualization ( each timestep on keypress)"""

import pygame
import sys
from time import sleep
from multiprocessing import Process

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
        self.load_data()
        self.screen_size = (
            self.grid_size[0] * self.cell_size,
            self.grid_size[1] * self.cell_size,
        )
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(window_title)
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.running = True
        self.bot_image = pygame.image.load("images/bot1.png").convert_alpha()
        self.bot_image = pygame.transform.scale(self.bot_image, (self.cell_size, self.cell_size))
        self.rat_image = pygame.image.load("images/rat.png").convert_alpha()
        self.rat_image = pygame.transform.scale(self.rat_image, (self.cell_size, self.cell_size))

    def load_data(self):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
        
        timestep_data = []
        for line in lines:
            line = line.strip()
            if line.startswith("Grid Size"):
                self.grid_size = tuple(map(int, line.split(":")[1].strip().split("x")))
            elif line.startswith("Initial Bot Location"):
                self.bot_pos = tuple(map(int, line.split(":")[1].strip()[1:-1].split(",")))
            elif line.startswith("Rat Location"):
                self.rat_pos = tuple(map(int, line.split(":")[1].strip()[1:-1].split(",")))
            elif line.startswith("Timestep"):
                if timestep_data:
                    self.timesteps.append(timestep_data)
                    timestep_data = []
            elif line:
                timestep_data.append(line.split(" "))
        if timestep_data:
            self.timesteps.append(timestep_data)

    def draw_grid(self):
        grid = self.timesteps[self.current_timestep]
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                color = (0, 0, 255) if (x, y) in self.visited_cells else (255, 255, 255) if cell == "o" else (0, 0, 0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                )
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),
                    (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    1,
                )

        # Draw the bot and rat
        self.screen.blit(self.bot_image, (self.bot_pos[0] * self.cell_size, self.bot_pos[1] * self.cell_size))
        self.screen.blit(self.rat_image, (self.rat_pos[0] * self.cell_size, self.rat_pos[1] * self.cell_size))

    def update(self):
        # Update visited cells
        self.visited_cells.add(self.bot_pos)

        # Draw the updated grid
        self.screen.fill((0, 0, 0))
        self.draw_grid()

        # Display current timestep
        timestep_text = self.font.render(f"Timestep: {self.current_timestep}", True, (255, 255, 255))
        self.screen.blit(timestep_text, (10, 10))
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.current_timestep < len(self.timesteps) - 1:
                        self.current_timestep += 1
                        self.update_positions()

            self.update()
            sleep(.5)
        pygame.quit()
        sys.exit()

    def update_positions(self):
        timestep_metadata = self.timesteps[self.current_timestep]
        for line in timestep_metadata:
            if line.startswith("Bot:"):
                self.bot_pos = tuple(map(int, line.split(":")[1].strip()[1:-1].split(",")))
            elif line.startswith("Rat:"):
                self.rat_pos = tuple(map(int, line.split(":")[1].strip()[1:-1].split(",")))
