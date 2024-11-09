from os import remove
import random
import math
impo


from cell import Cell
from ship import Ship


class Bot:
    def __init__(self,  ship:Ship , r:int, c:int, alpha:float):
        self.id = 1
        self.r = r
        self.c = c
        
        self.r_start = r
        self.c_start = c
        
        self.r_k = None
        self.c_k = None
        self.r_disp = 0
        self.c_disp = 0
        
        
        self.ship = ship
        self.imgpath = 'bot1.png'
        self.alpha = alpha
        
        self.openCells = self.ship.getOpenCells()
        self.possibleloc = self.ship.getOpenCells()
        # self.openCellProb = []
        self.visited = []
        self.b8neighbors = None
        self.movdirs =''
        self.movdisp = []
    
    def getStart(self):
        return (self.r_start, self.c_start)
        
    def getloc(self):
        return (self.r, self.c)
    
    def setloc(self, r, c):
        self.r = r 
        self.c = c
        
    def getKnownloc(self):
        return (self.r_k , self.c_k)
    
    def updateknownloc(self):
        self.r_k, self.c_k,_ = self.possibleloc[0]
    
        print(f"Known loc: {self.r_k, self.c_k}")
        print(f"Start loc : {self.r_start, self.c_start}")
        self.r_k += self.r_disp
        self.c_k += self.c_disp
        print(f"Known loc: {self.r_k, self.c_k}")
        print(f"curr loc : {self.r, self.c}")
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
    # def set_b8neighbors(self, b8neighbors):
    #     self.b8neighbors = b8neighbors
    
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
            # if self.ship.get_cellval(r-1, c) == 'o':
            #     openDirs+='u'
            # if self.ship.get_cellval(r, c-1) == 'o':
            #     openDirs+='l'
            # if self.ship.get_cellval(r+1, c) == 'o':
            #     openDirs+='d'
            # if self.ship.get_cellval(r, c+1) == 'o':
            #     openDirs+='r'
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
        # loc = (r_disp, c_disp, self.b8neighbors)
        # self.possibleloc.append(loc)
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
        print(f"Neighbours removed in sensing: {remove_list}")
        print(f"possibleloc after sensing: {self.possibleloc}")
            
    def detectCommonDir(self):
        """Detect the most common open direction in the map the bot can move"""
        all_dirs = 'uldr'
        for _, _, dirs in self.possibleloc:
            all_dirs += dirs

        return random.choice(all_dirs)

        # common_dirs  = [0, 0, 0, 0]
        # for r, c in self.possibleloc:
        #     if self.ship.get_cellval(r-1, c) == 'o':
        #         common_dirs[0] += 1
        #     if self.ship.get_cellval(r, c-1) == 'o':
        #         common_dirs[1] += 1
        #     if self.ship.get_cellval(r+1, c) == 'o':
        #         common_dirs[2] += 1
        #     if self.ship.get_cellval(r, c+1) == 'o':
        #         common_dirs[3] += 1
        
            # if 'u' in dirs:
            #     common_dirs[0] += 1
            # if 'l' in dirs:
            #     common_dirs[1] += 1
            # if 'd' in dirs:
            #     common_dirs[2] += 1
            # if 'r' in dirs:
            #     common_dirs[3] += 1

        # max_value = max(common_dirs)
        # max_index = common_dirs.index(max_value)
        # match max_index:
        #     case 0:
        #         return 'u'
        #     case 1:
        #         return 'l'
        #     case 2:
        #         return 'd'
        #     case 3:
        #         return 'r'
            
                
        
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
        print(f"Possibleloc: {self.possibleloc}")
        print("len: ", len(self.possibleloc))
        
        if self.ship.get_cellval(r+r_disp, c+c_disp) == 'b':
            print("blocked")
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
                        # self.possibleloc.pop(i)
            # for r,c,dirs in range(len(self.possibleloc)):
            #     if dir in dirs:
            #         self.possibleloc.remove((r,c))
            print(f"Removed in blocking: {remove_blocked}")
            return (0, 0)
        else:
            
            self.movdirs+= dir
            self.movdisp.append((r_disp, c_disp))
            remove_dir = []
            for r1,c1,dir1 in self.possibleloc:
                # print("If: ", i)
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
                        
            print(f"Removed in dir: {remove_dir}")
            # print("len: ", len(self.possibleloc))
            # for r1,c1,dir1 in self.possibleloc:
            #     # print("It: ", i)
            #     # print(f"Possibleloc: {self.possibleloc[i]}")
            #     if dir not in dir1:
            #         self.possibleloc.remove((r1,c1, dir1))
            # self.r_disp = self.r_start-r_n
            # self.c_disp = self.c_start-c_n
            self.setloc(r+r_disp, c+c_disp)
            self.movdirs+= dir
            self.movdisp.append((r_disp, c_disp))
            self.r_disp += r_disp
            self.c_disp += c_disp
            print("tot_ disp: ", self.r_disp, self.c_disp)
            print(self.getloc())
            return (r_disp, c_disp)

    # def updateMap(self):
    #     for disp, dir in zip(self.disp, self.dir):
    #         r_disp, c_disp = disp
    #         for 
        
    def getImgPath(self):
        return self.imgpath
        
    def getId(self):
        return self.id
    
    # def explore(self):
    #     b8neighbors = self.senseNeighbors()
    #     loc = (0,0, b8neighbors)
    #     dirs = ['u', 'l', 'd', 'r']
    #     while len(self.possibleloc)>1:
    #         dir = random.choice(dirs)

    def findPosition(self):
        self.createPossibleloc()
    # run_simulation(my_ship, r_b, c_b, bot_count, simulationPath, resultPath, stepPath, fileName)
        loc_found = 0
        sensed = 0  
        t= 0 
        while loc_found==0 and t<200:
            
            print("\nCurr_positon; ", self.getloc())
            t +=1
            if sensed == 0:
                self.senseNeighbors() 
                sensed = 1
            else:
                dir = self.detectCommonDir()
                r_disp, c_disp = self.moveBot(dir)
                print(f'T{t}: {r_disp, c_disp}')
                sensed = 0
            if self.get_possibleloclen() ==1:
                loc_found = 1
                self.updateknownloc()
                
        if (self.r_k, self.c_k) != self.getloc():
            print("known location differ from original")
            return False
        else:
            return True
        
    # def createOpenCellProb(self):
    #     for r,c in self.openCells:
    #         self.openCellProb.append((r,c,0))
    
    def calcManhattan(self, loc1, loc2):
        """Return manhattan distance b/w 2 cell location

        Args:
            loc1 (tuple): (int, int)
            loc2 (tuple): (int, int)

        Returns:
            int: _description_
        """
       
        return abs(loc1[0]-loc2[0]) + abs(loc1[0]-loc2[1])
    
    def pingProbability(self, loc1 , loc2):
        d = self.calcManhattan(loc1, loc2)
        prob = math.exp(-self.alpha * (d - 1))
        return prob
    
    # Function to generate a "ping" or "no ping" based on the probability
    def generate_ping(self,bot_position, rat_position, alpha):
        prob_ping = self.pingProbability(bot_position, rat_position, alpha)
        return random.rand() < prob_ping  # True if "ping", False if "no ping"

        
    # def updateCellProb(self, currloc, ping_recieved):
    #     """P(cell) = P(cell/curr_cell). p(curr_cell) 
        
    #     """
    #     r_curr, c_curr = currloc
    #     # ratloc = self.ship.getRatloc()
    #     # ping_curr = self.pingProbability(currloc, ratloc)
    #     # print("curr_ping: ", ping_curr)
    #     beta = 0.9
    #     for r,c in self.openCells:
    #         # p_cell = self.pingProbability(currloc, (r,c) ) * ping_curr * beta
    #         # print(p_cell)
    #         cell = self.ship.get_cell(r, c)
    #         if cell.get_val()!='b':
    #             cell_prob = cell.get_prob()+p_cell
    #             # print(cell_prob)
    #             cell.set_prob(cell_prob)
        
    def updateCellProb(self, currloc, ping_recieved):
        """P(cell) = P(cell/curr_cell). p(curr_cell) 
        
        """
        r_curr, c_curr = currloc
        # ratloc = self.ship.getRatloc()
        # ping_curr = self.pingProbability(currloc, ratloc)
        # print("curr_ping: ", ping_curr)
        sum = 0
        for r,c in self.openCells:
            prob_ping = self.pingProbability(currloc, (r,c) ) 
            likelihood = prob_ping if ping_received else (1 - prob_ping)
            new_prob = likelihood * belief[r,c]
            sum +=  new_prob
            # print(p_cell)
            cell = self.ship.get_cell(r, c)
            if cell.get_val()!='b':
                cell_prob = cell.get_prob()* likelihood
                # print(cell_prob)
                sum +=  cell_prob
                # cell.set_prob(cell_prob)
        for z in self.openCells:
            cell = self.ship.get_cell(r,c)
    
    def getNeighborProb(self, curr_loc):
        r,c = curr_loc
        neighbors = []
        probs = []
        n_loc = [(0,1), (0, -1), (1, 0), (-1, 0)]
        for r_disp, c_disp in n_loc:
            r_n = r+r_disp
            c_n = c+c_disp
            cell = self.ship.get_cell(r_n, c_n)
            # print(cell.get_val)
            if cell.get_val()!="b":
                prob = cell.get_prob()
                neighbors.append((r_n, c_n))
                probs.append(prob)
        return (neighbors, probs)
    
    def findRat(self):
        loc_rat = self.ship.getRatloc()
        print(f"RatLoc: {loc_rat}")
        with open("rat_results.txt","w") as f:
                f.write(f"Ratloc : {loc_rat}\n")
        t=0
        rat_found = 0
        while rat_found ==0 : #and t<1000:
            t+=1
            r, c = self.getloc()
            ping_received = generate_ping((r,c), rat_position)
            # update probabilities of the cells
            self.updateCellProb(currloc= (r,c), ping_received)
            # select a neighbor by weighted random sampling
            neighbors, probs = self.getNeighborProb(curr_loc=(r,c))
            # print(f"Neighbours: {neighbors}")
            # print(f"probabs: {probs}")
            next = random.choices(neighbors, weights= probs, k=1)
            r_n, c_n = next[0]
            print(f"New Loc: {next}   {t}")
            self.setloc(r_n, c_n)
            
            with open("rat_results.txt","a") as f:
                f.write(f"timestep t: {t}\n")
                for r in range(0, self.ship.getSize()):
                    for c in range(0, self.ship.getSize()):
                        cell = self.ship.get_cell(r,c)
                        prob = cell.get_prob()
                        if (r,c) == loc_rat:
                            f.write(f"R")
                        elif (r,c) == (r_n, c_n):
                            f.write(f"B")
                        else:
                            f.write(f"{prob:.4f} ")
                    f.write("\n")
                    
                f.write("\n\n")
            if loc_rat == (r_n, c_n):
                print("Rat found")
                rat_found = 1
        
        
       
        
    
    
    # def calcBlockList(self):
        
    #     for r in range(0, self.ship.getSize()):
    #         for c in range(0, self.ship.getSize()):
    #             neighbors = self.ship.countNeighbors( r, c, 'b')
    #             if neighbors == 3: 
    #                 self.block3.append((r,c))
    #             elif neighbors == 2: 
    #                 self.block2.append((r,c))
    #             elif neighbors == 1: 
    #                 self.block1.append((r,c))
    #             else:
    #                 self.block0.append((r,c))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    import numpy as np

# Parameters
alpha = 0.1  # Sensitivity of the detector
grid_size = (30, 30)  # Ship's grid dimensions

# Initialize prior belief that the rat is equally likely to be in any cell
belief = np.full(grid_size, 1.0 / (grid_size[0] * grid_size[1]))

# # Function to calculate Manhattan distance between two cells
# def manhattan_distance(cell1, cell2):
#     return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

# Function to get the probability of a "ping" based on distance
def ping_probability(bot_position, rat_position, alpha):
    distance = manhattan_distance(bot_position, rat_position)
    return np.exp(-alpha * (distance - 1))

# Function to generate a "ping" or "no ping" based on the probability
def generate_ping(bot_position, rat_position, alpha):
    prob_ping = ping_probability(bot_position, rat_position, alpha)
    return np.random.rand() < prob_ping  # True if "ping", False if "no ping"

# Function to update the belief based on whether a ping was received
def update_belief(belief, bot_position, ping_received, alpha):
    new_belief = np.zeros_like(belief)

    # Update each cell's probability based on "ping" or "no ping"
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            rat_position = (x, y)
            prob_ping = ping_probability(bot_position, rat_position, alpha)
            likelihood = prob_ping if ping_received else (1 - prob_ping)
            new_belief[x, y] = likelihood * belief[x, y]

    # Normalize the belief to ensure it sums to 1
    total_belief = np.sum(new_belief)
    if total_belief > 0:
        new_belief /= total_belief
    else:
        # If all probabilities are zero, reset to uniform distribution
        new_belief.fill(1.0 / (grid_size[0] * grid_size[1]))
    
    return new_belief

# Example usage
# Initial positions (for demonstration purposes)
bot_position = (15, 15)  # Assume bot starts at the center of the grid
rat_position = (20, 20)  # Assume rat starts at some random position

# Generate "ping" or "no ping" based on the current bot and rat positions
ping_received = generate_ping(bot_position, rat_position, alpha)

# Update belief based on the ping result
belief = update_belief(belief, bot_position, ping_received, alpha)

# Output the updated belief grid
print("Updated belief grid:")
print(belief)
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def calcHeuristic(self):
    #     """Calculating the Manhattan distance
    #     """
    #     r_dest, c_dest = self.ship.getSwitchLoc()
    #     d = self.ship.getSize()
    #     for r in range(d):
    #         for c in range(d):
    #             if self.ship.get_cellval(r,c) != 'b': 
    #                 h = abs(r_dest-r) + abs(c_dest-c)
    #                 self.ship.get_cell(r, c).set_h(h) 
                
    # def tracePath(self, r, c):
    #     path = []
        
    #     while r is not None and c is not None: 
    #         cell = self.ship.get_cell(r, c)
    #         path.append((cell.get_r(), cell.get_c()))
    #         r, c = cell.get_parent(0)
            
    #     path.reverse()
    #     print(f'PATH: {path}')
    #     if len(path)>1:
    #         return path[1]
    #     else:
    #         return -1
        
    
    # def getPossibleCells(self):
    #     fStartCell = self.ship.fire.getStartCell()
    #     possibleCells = self.ship.getOpenCells() + self.ship.getFireCells()
    #     possibleCells.remove(fStartCell)
        
    #     return possibleCells
        
    # def update_priority(self, pq, old_item, new_p1):
    #     temp_list = []
    #     edit_fringe = False
        
    #     # Temporarily store elements and remove the one to update
    #     while not pq.empty():
    #         p_old, item = pq.get()
            
    #         if item == old_item:
    #             # Update the priority of the target item
    #             if new_p1< p_old:
    #                 temp_list.append((new_p1, item))
    #                 edit_fringe = True
    #             else:
    #                 temp_list.append((p_old, item))
    #         else:
    #             temp_list.append((p_old, item))
        
    #     # Reinsert all elements back into the queue
    #     for item in temp_list:
    #         pq.put(item)   
    #     return edit_fringe
        
    # def move(self, ship):
    #     self.ship = ship
    #     r_bot, c_bot = self.getloc()
    #     r_dest, c_dest = self.ship.getSwitchLoc()
    #     if (r_bot, c_bot) == (r_dest, c_dest):
    #         return False
    #     visited = []
    #     fringe = PriorityQueue()
    #     fringe_items = []
    #     possibleCells = self.getPossibleCells()
       
    #     cell_start = self.ship.get_cell(r_bot, c_bot)
    #     cell_start.set_dist(0)
    #     p_start = cell_start.get_h() #+ cell_start.get_dist()
    #     cell_start.set_tot(p_start)
    #     fringe.put((p_start,  (r_bot, c_bot)))
    #     fringe_items.append(( r_bot, c_bot))
        
        
    #     while not fringe.empty():
    #         p1_curr,  curr = fringe.get()
    #         fringe_items.pop(0)
            
    #         r_curr = curr[0]
    #         c_curr = curr[1]
    #         visited.append((r_curr, c_curr))
            
    #         cell_curr =  self.ship.get_cell(r_curr, c_curr)
    #         if (r_curr, c_curr) == (r_dest, c_dest):
    #             r_next, c_next = self.tracePath(r_dest, c_dest)
    #             self.setloc(r_next, c_next)
    #             return True
            
    #         cost_to_neighbour = cell_curr.get_tot() + 1
            
    #         o_neighbours = self.ship.getNeighbours(r_curr, c_curr, 'o') + self.ship.getNeighbours(r_curr, c_curr, 'f')
    #         possible_neighbours = [neighbour for neighbour in o_neighbours if neighbour in possibleCells]
    #         neighbours = [neighbour for neighbour in possible_neighbours if neighbour not in visited]
            
    #         for neighbour in neighbours:
    #             r_child, c_child = neighbour
    #             cell_child = self.ship.get_cell(r_child, c_child)
    #             if neighbour in fringe_items:
    #                 if cost_to_neighbour< cell_child.get_dist():
    #                     cell_child.set_dist(cost_to_neighbour)
    #                     cell_child.set_parent(r_curr, c_curr , 0)
                        
    #             else:
    #                 cell_child.set_dist(cost_to_neighbour)
    #                 cell_child.set_parent(r_curr, c_curr, 0)
                
    #             p1 = cell_child.get_dist() + cell_child.get_h()
    #             if (r_child, c_child) in fringe_items: 
    #                 fringe_edited = self.update_priority(fringe, (r_child, c_child), p1)
    #                 if fringe_edited: 
    #                     cell_child.set_tot(p1)
    #             else:
    #                 fringe.put((p1, (r_child, c_child)))
    #                 cell_child.set_tot(p1)
    #                 fringe_items.append((r_child, c_child))
    #     print("!!!FAILURE IN BOT-1 A-STAR !!!!!!")
    #     return False
        
        