import pygame
import sys
from multiprocessing import Process

class GridGUI:
    def __init__(self, file_name, window_title):
        self.file_name = file_name
        self.window_title = window_title
        self.grid = []
        self.timesteps = []
        self.bot_position = (0, 0)
        self.rat_position = (0, 0)
        self.bot_start_found = False
        self.cell_size = 20
        self.margin = 5

        # Read the grid and positions from the file
        self.read_file()

    def read_file(self):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
        
        grid_section = False
        timestep_section = False
        for line in lines:
            line = line.strip()
            if line.startswith("Grid Size:"):
                self.grid_size = tuple(map(int, line.split(":")[1].strip().split("x")))
            elif line.startswith("Initial Bot Location:"):
                self.bot_position = tuple(map(int, line.split(":")[1].strip().strip("()").split(", ")))
            elif line.startswith("Rat Location:"):
                self.rat_position = tuple(map(int, line.split(":")[1].strip().strip("()").split(", ")))
            elif line.startswith("Timestep:"):
                timestep_section = True
                grid_section = False
                self.timesteps.append([])
            elif line.startswith("----------------------------------------"):
                timestep_section = False
            elif timestep_section:
                self.timesteps[-1].append(line.split(" "))
            elif line and not grid_section and not timestep_section:
                grid_section = True

        # Initialize the grid with the first timestep
        if self.timesteps:
            self.grid = self.timesteps[0]

    def draw_grid(self, screen):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                x = col * (self.cell_size + self.margin) + self.margin
                y = row * (self.cell_size + self.margin) + self.margin
                
                # Determine the color for each cell
                if (row, col) == self.bot_position:
                    color = (255, 0, 0)  # Red for bot
                elif (row, col) == self.rat_position:
                    color = (0, 255, 0)  # Green for rat
                elif self.grid[row][col] == "o":
                    if self.bot_start_found and (row, col) == self.bot_position:
                        color = (0, 0, 255)  # Blue for bot's start location
                    else:
                        color = (255, 255, 255)  # White for open cells
                else:
                    color = (0, 0, 0)  # Black for closed cells
                
                # Draw the rectangle
                pygame.draw.rect(screen, color, (x, y, self.cell_size, self.cell_size))

    def update_grid(self, timestep_index):
        if timestep_index < len(self.timesteps):
            self.grid = self.timesteps[timestep_index]
            if not self.bot_start_found and self.bot_position != (0, 0):
                self.bot_start_found = True

    def run(self):
        pygame.init()
        screen_width = self.grid_size[1] * (self.cell_size + self.margin) + self.margin
        screen_height = self.grid_size[0] * (self.cell_size + self.margin) + self.margin
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(self.window_title)

        clock = pygame.time.Clock()
        timestep_index = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Update the grid for the current timestep
            self.update_grid(timestep_index)

            # Draw the grid
            screen.fill((128, 128, 128))  # Background color
            self.draw_grid(screen)

            pygame.display.flip()
            clock.tick(1)  # 1 FPS to simulate timestep changes
            timestep_index = (timestep_index + 1) % len(self.timesteps)

        pygame.quit()
        sys.exit()

