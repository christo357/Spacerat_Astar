from ship import Ship

class Logger():
    def __init__(self, size, ship, resultPath):
        self.size = size
        self.ship = ship
        self.resultPath = resultPath
        self.bot_start = (0,0)

    # Function to log metadata (grid size, bot, and switch location) to result.txt
    def log_metadata(self):
        
        with open(self.resultPath, "w") as file:
            file.write(f"Grid Size: {self.size}x{self.size}\n")
            # file.write(f"Flammability: {ship.get_q()}\n")
            # file.write(f'Bot : {bot.get_Id()}\n')
            bot_row, bot_col = self.ship.getStartBotLoc()
            rat_row, rat_col = self.ship.getRatloc()
            file.write(f"Initial Bot Location: ({bot_row}, {bot_col})\n")
            file.write(f"Rat Location: ({rat_row}, {rat_col})\n")
            file.write("-" * 40 + "\n")
            
    def log_grid_state(self, timestep, bot, rat, loc_find = 0):
        with open(self.resultPath, "a") as file:
            file.write(f"Timestep: {timestep}\n")
            for row in range(self.size):
                for col in range(self.size):
                    # if (row, col) == bot:
                    #     v = 'B'
                    # elif (row, col) == rat:
                    #     v = "R"
                    # else:
                    v = self.ship.get_cellval(row, col)
                    file.write(f"{v} ")
                file.write("\n")
            
            if isinstance(loc_find, tuple) and len(loc_find) == 2 and all(isinstance(i, int) for i in loc_find):
                self.bot_start = loc_find
            
            file.write(f"Bot start: {self.bot_start}\n")
            file.write(f"Bot: {bot}\n")
            file.write(f"Rat: {rat}\n")
            # for i in range(0, bot_count):
            #     bot_row, bot_col = ship.getBotLoc(i)
            #     file.write(f"Bot {i+1}: ({bot_row}, {bot_col})\n")
            file.write("-" * 40 + "\n")      
            
            
    # Function to log the grid state to result.txt at each timestep
    def log_botposition(self,  timestep, bot_count):
        with open(self.resultPath, "a") as file:
            file.write(f"Timestep: {timestep}\n")
            # for row in range(self.size):
            #     for col in range(self.size):
            #         file.write(self.ship.get_cellval(row, col))
            #     file.write("\n")
            # for i in range(bot_count):
            #     bot_row, bot_col = self.ship.getBotLoc(i)
            #     file.write(f"Bot {i+1}: ({bot_row}, {bot_col})\n")
            # rat_row, rat_col = self.ship.getRatloc()
            # file.write(f"Rat :{rat_row}, {rat_col}")
            for i in range(bot_count):
                bot_row, bot_col = self.ship.getBotLoc(i)
                file.write(f"({i}, {i})",end = ",")
            rat_row, rat_col = self.ship.getRatloc()
            file.write(f"({rat_row}, {rat_col})")
            file.write("-" * 40 + "\n")
            
    # def log_grid_state(self, timestep, botcount):
    #     with open(self.resultPath, "a") as file:
    #         file.write(f"Timestep: {timestep}\n")
    #         for row in range(self.size):
    #             for col in range(self.size):
    #                 file.write(self.ship.get_cellval(row, col))
    #             file.write("\n")
            
    #         file.write("-"*40+"\n")
            
            