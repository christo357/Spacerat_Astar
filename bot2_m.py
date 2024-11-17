from os import remove
from queue import PriorityQueue
import random
import math

# from networkx import neighbors
import numpy as np


from cell import Cell
from ship import Ship
from astar import Astar
from logger import Logger


class Bot:
    def __init__(self,  ship:Ship , r:int, c:int, alpha:float,  seed: int, resultPath: str):
        self.random = random.Random(seed)
        self.id = 1
        self.r = r
        self.c = c
        self.t = 0
        
        self.r_start = r
        self.c_start = c
        
        self.r_k = None
        self.c_k = None
        self.r_ks = None
        self.c_ks = None
        self.r_disp = 0
        self.c_disp = 0
        
        
        self.ship = ship
        self.shipSize = self.ship.getSize()
        self.imgpath = 'images/bot2.png'
        self.resultPath = resultPath
        self.alpha = alpha
        
        self.openCells = self.ship.getOpenCells()
        self.possibleloc = self.ship.getOpenCells()
        self.possibleRat = self.ship.getOpenCells()
        self.belief = np.zeros((self.shipSize, self.shipSize))
        self.visited = []
        self.b8neighbors = None
        self.movdirs =''
        self.movdisp = []

        self.logger = Logger(self.shipSize, self.ship, self.resultPath)
        
    
    def getStart(self):
        return (self.r_start, self.c_start)
        
    def getloc(self):
        return (self.r, self.c)
    
    def setloc(self, r, c):
        self.r = r 
        self.c = c
        
    def getKnownloc(self):
        return (self.r_k , self.c_k)
    
    def getKnownStart(self):
        return (self.r_ks, self.c_ks)
    
    def updateknownloc(self):
        self.r_k, self.c_k,_ = self.possibleloc[0]
    
        # print(f"Known loc: {self.r_k, self.c_k}")
        # print(f"Start loc : {self.r_start, self.c_start}")
        self.r_k += self.r_disp
        self.c_k += self.c_disp
        # print(f"Known loc: {self.r_k, self.c_k}")
        # print(f"curr loc : {self.r, self.c}")
        # self.r = self.r_k + self.r_disp
        # self.c = self.c_k + self.c_disp
        
    
        
    def invalidposition(self, r, c):
        if 0<r<self.ship.getSize()-1 and 0<c<self.ship.getSize()-1:
            return False
        else:
            return True
        
    def get_b8neighbors(self):
        """Returns  the number of blocked cells out of  8 neighbours

        Returns:
            _type_: _description_
        """
        return self.b8neighbors
        
    def get_possibleloclen(self):
        return len(self.possibleloc)
    
    def openDirs(self, r,c ):
        openDirs = ''
        if self.ship.get_cellval(r-1, c) == 'o':
            openDirs+='u'
        if self.ship.get_cellval(r, c-1) == 'o':
            openDirs+='l'
        if self.ship.get_cellval(r+1, c) == 'o':
            openDirs+='d'
        if self.ship.get_cellval(r, c+1) == 'o':
            openDirs+='r'
        return openDirs
    
    
    def createPossibleloc(self):
        '''updates the list possibleloc with all possible locations that bot can move. 
        Also stores the directions of their open neighbours.
        structure of each element: (r, c , <possible dirs>)'''
        openCells = self.ship.getOpenCells()
        for i in range(len(self.possibleloc)):
            r, c = self.possibleloc[i]
            openDirs = self.openDirs(r,c)
            self.possibleloc[i] = (r, c , openDirs)
    
    def senseNeighbors(self):
        """senses the number of blocked neighbors. And calls Updatepossibleloc

        Args:
            r_disp (_type_): displacement of bot from initial row
            c_disp (_type_): displacement of bot from initial column
        """
        # r_start,c_start = self.getStart()
        r, c = (self.r_start+self.r_disp, self.c_start+self.c_disp)
        
        count = 0
        if self.ship.get_cellval(r-1, c) == 'b':
                count += 1
        if self.ship.get_cellval(r, c-1) == 'b':
            count += 1
        if self.ship.get_cellval(r+1, c) == 'b':
            count += 1
        if self.ship.get_cellval(r, c+1) == 'b':
            count += 1
        if self.ship.get_cellval(r-1, c-1) == 'b':
            count += 1
        if self.ship.get_cellval(r-1, c+1) == 'b':
            count += 1
        if self.ship.get_cellval(r+1, c-1) == 'b':
            count += 1
        if self.ship.get_cellval(r+1, c+1) == 'b':
            count += 1
        self.b8neighbors = count
        self.updatePossibleLocations()
        # return 1
        
    def updatePossibleLocations(self):
        remove_list = []

        for r_map, c_map, dir_map in self.possibleloc:
            r = r_map + self.r_disp
            c = c_map + self.c_disp
            
            if self.invalidposition(r,c):
                    remove_list.append((r_map, c_map,"i"))
                    self.possibleloc.remove((r_map,c_map, dir_map))
            else:
                map_cell = self.ship.get_cell(r, c)
                if map_cell.get_b8neighbors()!= self.b8neighbors:
                    remove_list.append((r_map, c_map))
                    self.possibleloc = [item for item in self.possibleloc if not (item[0]==r_map and item[1]==c_map)]
        # print(f"Neighbours removed in sensing: {remove_list}")
        # print(f"possibleloc after sensing: {self.possibleloc}")
            
    def detectCommonDir(self):
        """Detect the most common open direction in the map the bot can move"""
        all_dirs = 'uldr'
        for _, _, dirs in self.possibleloc:
            all_dirs += dirs

        return self.random.choice(all_dirs)
        
    def moveBot(self, dir):
        moved = 0
        (r, c ) = self.getloc()
        print("Dir: ", dir)
        r_disp, c_disp = (0,0)
        if dir == 'u':
            r_disp, c_disp = (-1,0)
            # r_n = r+1
            # c_n = c
        if dir == 'd':
            r_disp, c_disp = (1,0)
            # r_n = r-1
            # c_n = c
        if dir == 'l':
            r_disp, c_disp = (0,-1)
            # r_n = r
            # c_n = c+1
        if dir == 'r':
            r_disp, c_disp = (0,1)
            # r_n = r
            # c_n = c-1
        # else:
        #     return (0,0)
        # print(f"Possibleloc: {self.possibleloc}")
        # print("len: ", len(self.possibleloc))
        
        if self.ship.get_cellval(r+r_disp, c+c_disp) == 'b':
            # print("blocked")
            remove_blocked = []
            for r1,c1,dir1 in self.possibleloc:
                # print("If: ", i)
                r2 = r1+self.r_disp
                c2 = c1+self.c_disp
                if self.invalidposition(r2,c2):
                    remove_blocked.append((r1,c1, "i"))
                    self.possibleloc.remove((r1,c1, dir1))
                else:
                    dir2 = self.openDirs(r2,c2)
                    if dir in dir2:
                        remove_blocked.append((r1,c1))
                        self.possibleloc.remove((r1,c1, dir1))
            # print(f"Removed in blocking: {remove_blocked}")
            return (0, 0)
        else:
            
            self.movdirs+= dir
            self.movdisp.append((r_disp, c_disp))
            remove_dir = []
            for r1,c1,dir1 in self.possibleloc:
               
                r2 = r1+self.r_disp
                c2 = c1+self.c_disp
                
                if self.invalidposition(r2,c2):
                    remove_dir.append((r1, c1,"i"))
                    self.possibleloc.remove((r1,c1, dir1))
                else:
                    dir2 = self.openDirs(r2,c2)
                    if dir not in dir2:
                        remove_dir.append((r1, c1))
                        self.possibleloc.remove((r1,c1, dir1))
                        
            # print(f"Removed in dir: {remove_dir}")
            self.setloc(r+r_disp, c+c_disp)
            self.movdirs+= dir
            self.movdisp.append((r_disp, c_disp))
            self.r_disp += r_disp
            self.c_disp += c_disp
            # print("tot_ disp: ", self.r_disp, self.c_disp)
            print(self.getloc())
            return (r_disp, c_disp)

 
    def getImgPath(self):
        return self.imgpath
        
    def getId(self):
        return self.id
    
 
    def findPosition(self):
        self.createPossibleloc()
        loc_rat = self.ship.getRatloc()
        loc_found = 0
        sensed = 0  
        while loc_found==0 :#and t<200:
            self.logger.log_grid_state(self.t, self.getloc(), loc_rat)
            # print("\nCurr_positon; ", self.getloc())
            # self.interface.update_display(self.getloc(), loc_rat)
            self.t +=1
            self.ship.moveRat(self.random)
            if sensed == 0:
                self.senseNeighbors() 
                sensed = 1
            else:
                dir = self.detectCommonDir()
                r_disp, c_disp = self.moveBot(dir)
                # print(f'T{self.t}: {r_disp, c_disp}')
                sensed = 0
            if self.get_possibleloclen() ==1:
                loc_found = 1
                self.updateknownloc()
                
        if (self.r_k, self.c_k) != self.getloc():
            # print("known location differ from original")
            return (0,0)
        else:
            self.logger.log_grid_state(self.t, self.getloc(), loc_rat, self.getKnownStart())
            return self.getKnownStart()
        
    def calcHeuristic(self,dest):
        """Calculating the Manhattan distance
        """
        r_dest, c_dest = dest
        d = self.shipSize()
        for r in range(d):
            for c in range(d):
                if self.ship.get_cellval(r,c) != 'b': 
                    h = abs(r_dest-r) + abs(c_dest-c)
                    self.ship.get_cell(r, c).set_h(h) 
        
    # def createOpenCellProb(self):
    #     for r,c in self.openCells:
    #         self.openCellProb.append((r,c,0))
    
    def initializeBelief(self):
        b = 1.0/(len(self.openCells))
        for r in range(self.shipSize):
            for c in range(self.shipSize):
                cell = self.ship.get_cell(r,c)
                if cell.get_val() == 'b':
                    self.belief[r,c] =0
                else:
                    self.belief[r,c] = b
    
    def calcManhattan(self, loc1, loc2):
       return abs(loc1[0]-loc2[0]) + abs(loc1[0]-loc2[1])
    
    def pingProbability(self, loc1 , loc2):
        d = self.calcManhattan(loc1, loc2)
        return math.exp(-self.alpha * (d - 1))
       
    
    # Function to generate a "ping" or "no ping" based on the probability
    def generate_ping(self,bot_position, rat_position):
        prob_ping = self.pingProbability(bot_position, rat_position)
        return self.random.random() < prob_ping  # True if "ping", False if "no ping"

        
        
    def updateCellProb(self, currloc, ping_received):
        """P(cell) = P(cell/curr_cell). p(curr_cell) 
        
        """
        r_curr, c_curr = currloc
        sum = 0
        new_belief = np.zeros_like(self.belief)
        for r,c in self.openCells:
            prob_ping = self.pingProbability(currloc, (r,c))
            likelihood = prob_ping if ping_received else (1 - prob_ping)
            new_belief[r,c] = likelihood * self.belief[r,c]
            
        total_belief = np.sum(new_belief)
        if total_belief>0:
            new_belief /= total_belief
            return new_belief
        else:
                self.initializeBelief()
                return self.belief
           
    
    def updateProbList(self):
        probs = []
        for r,c in self.possibleRat:
            probs.append(float(self.belief[r,c]))
        return probs
    
    def distributeCellProb(self):
        """distribute the probability of each cell  to itself and its neighbours

        Args:
            loc (_type_): _description_
        """
        new_belief = np.zeros_like(self.belief)
        for r, c in self.openCells:
            
            
            # r,c = loc
            dist_cells = self.ship.getNeighbors(r,c,'o') # cells to distribute prob. to
            dist_cells.append((r,c))
            l = len(dist_cells)
            p = self.belief[r,c]
            # self.belief[r,c] = 0
            new_p = p/l
            for r_cell, c_cell in dist_cells:
                new_belief[r_cell, c_cell] += new_p
        self.belief = new_belief.copy()
        
    # def chooseNextCellDefault(self, curr_loc):
    #     r, c = curr_loc
        
    #     # Find cells with highest probability
    #     max_prob = np.max(self.belief)
    #     high_prob_cells = [
    #         (i,j) for i,j in self.openCells 
    #         if self.belief[i,j] > max_prob * 0.9  # Consider cells with prob close to max
    #     ]
        
    #     # Choose closest high probability cell
    #     min_dist = float('inf')
    #     best_target = None
        
    #     for cell in high_prob_cells:
    #         dist = self.calcManhattan(curr_loc, cell)
    #         if dist < min_dist:
    #             min_dist = dist
    #             best_target = cell
                
    #     return best_target
    
    
    def chooseNextCell(self, curr_loc):
        r, c = curr_loc
        
        # Find cells with highest probability
        # max_prob = np.max(self.belief)
        
        region_cells = self.regions[self.current_region]
        # print(f"region cells : {region_cells}")
        
        cell_probs = [(self.belief[i, j], (i, j)) for i, j in region_cells]
        cell_probs.sort(reverse=True)  # Sort by probability descending
        max_prob = cell_probs[0][0]  # Cell with the highest probability in the current region
        # print(f"cell probs: {cell_probs}")
        
        high_prob_cells = [
            (i,j) for i,j in region_cells
            if self.belief[i,j] >= max_prob * 0.8  # Consider cells with prob close to max
        ]
        # print(f"high prob cells : {high_prob_cells}")
        
        # if not high_prob_cells:
        #     max_prob = np.max(self.belief)
        #     high_prob_cells = [
        #         (i,j) for i,j in self.openCells 
        #         if self.belief[i,j] > max_prob * 0.8  # Consider cells with prob close to max
        #     ]
            
            # print("No high probability cells available, choosing random valid cell.")
            # return random.choice(region_cells) if region_cells else None 
        # Choose closest high probability cell
        min_dist = float('inf')
        best_target = None
        
        for cell in high_prob_cells:
            dist = self.calcManhattan(curr_loc, cell)
            if dist < min_dist and dist>0:
                min_dist = dist
                best_target = cell
                
        return best_target
    
    def findRat(self):
        loc_rat = self.ship.getRatloc()
        print(f"RatLoc: {loc_rat}")
        # with open("rat_results.txt","w") as f:
        #         f.write(f"Ratloc : {loc_rat}\n")
        #         f.write(f"Bot Pos: {self.getloc()}\n")
                
        # Divide the ship into 9 regions (3x3 grid of 10x10 cells each)
        # self.regions = {
        #     0: [(i, j) for i in range(0, 10) for j in range(0, 10) if self.ship.get_cellval(i, j) == 'o' ],
        #     1: [(i, j) for i in range(0, 10) for j in range(10, 20) if self.ship.get_cellval(i, j) == 'o' ],
        #     2: [(i, j) for i in range(0, 10) for j in range(20, 30) if self.ship.get_cellval(i, j) == 'o' ],
        #     3: [(i, j) for i in range(10, 20) for j in range(0, 10) if self.ship.get_cellval(i, j) == 'o' ],
        #     4: [(i, j) for i in range(10, 20) for j in range(10, 20) if self.ship.get_cellval(i, j) == 'o' ],
        #     5: [(i, j) for i in range(10, 20) for j in range(20, 30) if self.ship.get_cellval(i, j) == 'o' ],
        #     6: [(i, j) for i in range(20, 30) for j in range(0, 10) if self.ship.get_cellval(i, j) == 'o' ],
        #     7: [(i, j) for i in range(20, 30) for j in range(10, 20) if self.ship.get_cellval(i, j) == 'o' ],
        #     8: [(i, j) for i in range(20, 30) for j in range(20, 30) if self.ship.get_cellval(i, j) == 'o' ]
        # }
        self.regions = {
            0: [(i, j) for i in range(0, 15) for j in range(0, 15) if self.ship.get_cellval(i, j) == 'o' ],
            1: [(i, j) for i in range(0, 15) for j in range(15, 30) if self.ship.get_cellval(i, j) == 'o' ],
            2: [(i, j) for i in range(15, 30) for j in range(0, 15) if self.ship.get_cellval(i, j) == 'o' ],
            3: [(i, j) for i in range(15, 30) for j in range(15, 30) if self.ship.get_cellval(i, j) == 'o' ],
        }
        self.current_region = None
                
        rat_found = 0
        self.initializeBelief()
        
        a_star = 0
        move = 0
        
        loc = self.getloc()
        r, c= loc
        while rat_found ==0:# and self.t<2000:
            self.logger.log_grid_state(self.t, self.getloc(), loc_rat)
            self.t+=1
            loc = self.getloc()
            (r,c) = loc
            loc_rat = self.ship.getRatloc()
            if loc==loc_rat:
                print(f"Rat Found at: {loc} in {self.t} timesteps")
                rat_found = 1
                break
            else:
                self.belief[r,c] = 0
            #     if loc in self.possibleRat:
            #             self.possibleRat.remove(loc)
                        
            if move==0:
                move = 1
                ping_received = self.generate_ping((r,c), loc_rat)
                # update probabilities of the cells
                self.belief = self.updateCellProb(currloc= (r,c), ping_received=ping_received)
                self.distributeCellProb()
           
            
            else:
                move =0
                if a_star ==0:
                   
                    # r, c = self.getloc()
                    self.region_probs = {} 
                    prob_list = self.updateProbList()
                    
                    # find the total probability for each region
                    for region, cells in self.regions.items():
                        self.region_probs[region] = sum(self.belief[i, j] for i, j in cells)
                        
                    max_region = max(self.region_probs, key = self.region_probs.get)
                    # If the max probability region is different from the current, switch to the new region
                    if self.current_region is None or self.region_probs[max_region]*0.9 > self.region_probs[self.current_region]:
                        self.current_region = max_region
                    
                    dest = self.chooseNextCell(loc)
                    # if dest == None:
                    #     dest = self.chooseNextCellDefault(loc)
                    # print(f"dest; {dest}")
                    # region_cells = self.regions[self.current_region]
                    # cell_probs = [(self.belief[i, j], (i, j)) for i, j in region_cells]
                    # cell_probs.sort(reverse=True)  # Sort by probability descending
                    # dest = cell_probs[0][1]  # Cell with the highest probability in the current region
                    if dest is None:
                        print(f"belief: {self.belief}")
                        print(f"region probs: {self.region_probs}")
                        print(f"current region: {self.current_region}")
                        print(f"region: {self.regions}")
                    print(f"\nT: {self.t}, dest: {dest}")
                    astar = Astar((r,c), dest, self.possibleRat,self.ship)
                    path = astar.findPath()
                    if len(path)>0:
                        a_star = 1
                        
                else:
                    loc = path[0]
                    path.remove(loc)
                    # print(f"Bot position: {loc}")
                    self.setloc(loc[0], loc[1])
                    if loc==loc_rat:
                        print(f"Bot2m, Rat Found at: {loc} in {self.t} timesteps")
                        rat_found = 1
                        break
                    else:
                        # self.possibleRat.remove(loc)
                        r, c = loc
                        self.belief[r,c] = 0
                        
                    if loc == dest:
                        a_star = 0
                   
            self.ship.moveRat(self.random)

            # with open("rat_results.txt","a") as f:
                # f.write(f"timestep t: {self.t}\n")
                # for r in range(0, self.ship.getSize()):
                #     for c in range(0, self.ship.getSize()):
                #         # cell = self.ship.get_cell(r,c)
                #         prob = self.belief[r,c]
                #         if (r,c) == loc_rat:
                #             f.write(f"R")
                #         elif (r,c) == loc:
                #             f.write(f"B")
                #         else:
                #             f.write(f"{prob:.4f} ")
                #     f.write("\n")
                    
                # f.write("\n\n")
        return self.t
          
    
    
    
    
    
#     import numpy as np

# # Parameters
# alpha = 0.1  # Sensitivity of the detector
# grid_size = (30, 30)  # Ship's grid dimensions

# # Initialize prior belief that the rat is equally likely to be in any cell
# belief = np.full(grid_size, 1.0 / (grid_size[0] * grid_size[1]))

# # # Function to calculate Manhattan distance between two cells
# # def manhattan_distance(cell1, cell2):
# #     return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

# # Function to get the probability of a "ping" based on distance
# def ping_probability(bot_position, rat_position, alpha):
#     distance = manhattan_distance(bot_position, rat_position)
#     return np.exp(-alpha * (distance - 1))

# # Function to generate a "ping" or "no ping" based on the probability
# def generate_ping(bot_position, rat_position, alpha):
#     prob_ping = ping_probability(bot_position, rat_position, alpha)
#     return np.random.rand() < prob_ping  # True if "ping", False if "no ping"

# # Function to update the belief based on whether a ping was received
# def update_belief(belief, bot_position, ping_received, alpha):
#     new_belief = np.zeros_like(belief)

#     # Update each cell's probability based on "ping" or "no ping"
#     for x in range(grid_size[0]):
#         for y in range(grid_size[1]):
#             rat_position = (x, y)
#             prob_ping = ping_probability(bot_position, rat_position, alpha)
#             likelihood = prob_ping if ping_received else (1 - prob_ping)
#             new_belief[x, y] = likelihood * belief[x, y]

#     # Normalize the belief to ensure it sums to 1
#     total_belief = np.sum(new_belief)
#     if total_belief > 0:
#         new_belief /= total_belief
#     else:
#         # If all probabilities are zero, reset to uniform distribution
#         new_belief.fill(1.0 / (grid_size[0] * grid_size[1]))
    
#     return new_belief

# # Example usage
# # Initial positions (for demonstration purposes)
# bot_position = (15, 15)  # Assume bot starts at the center of the grid
# rat_position = (20, 20)  # Assume rat starts at some random position

# # Generate "ping" or "no ping" based on the current bot and rat positions
# ping_received = generate_ping(bot_position, rat_position, alpha)

# # Update belief based on the ping result
# belief = update_belief(belief, bot_position, ping_received, alpha)

# # Output the updated belief grid
# print("Updated belief grid:")
# print(belief)
    
    
    
    
    
    
    
    
    
    
    
    
    
 