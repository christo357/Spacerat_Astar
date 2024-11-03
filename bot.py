import random

from ship import Ship


class Bot:
    def __init__(self,  ship , r, c):
        self.id = 1
        self.r = r
        self.c = c
        
        self.r_k = None
        self.c_k = None
        
        self.r_start = r
        self.c_start = c
        
        self.ship = ship
        self.imgpath = 'bot1.png'
        
        self.possibleloc = self.ship.getOpenCells()
        self.visited = []
        self.b8neighbors = None
        
    
    def getStart(self):
        return (self.r_start, self.c_start)
        
    def getloc(self):
        return (self.r, self.c)
    
    def setloc(self, r, c):
        self.r = r 
        self.c = c
        
    def get_b8neighbors(self):
        return self.b8neighbors
        
    # def set_b8neighbors(self, b8neighbors):
    #     self.b8neighbors = b8neighbors
    
    def createPossibleloc(self):
        openCells = self.ship.getOpenCells()
        for i in range(len(self.possibleloc)):
            r, c = self.possibleloc[i]
            openDirs = ''
            if self.ship.get_cellval(r-1, c) == 'o':
                openDirs+='u'
            if self.ship.get_cellval(r, c-1) == 'o':
                openDirs+='l'
            if self.ship.get_cellval(r+1, c) == 'o':
                openDirs+='d'
            if self.ship.get_cellval(r, c+1) == 'o':
                openDirs+='r'
            self.possibleloc[i] = (r, c , openDirs)
    
    def senseNeighbors(self, r_disp, c_disp):
        r_start,c_start = self.getStart()
        r, c = (r_start+r_disp, c_start+c_disp)
        # cell = self.ship.get_cell(r, c)
        # return cell.get_b8neighbors()
        
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
        self.updatePossibleLocations(r_disp, c_disp)
        
    def updatePossibleLocations(self, r_disp, c_disp):
        # loc = (r_disp, c_disp, self.b8neighbors)
        # self.possibleloc.append(loc)
        for r_map, c_map in self.possibleloc:
            r = r_map + r_disp
            c = c_map + c_disp
            
            map_cell = self.ship.get_cell(r, c)
            if map_cell.get_b8neighbors()!= self.b8neighbors:
                self.possibleloc.remove((r_map, c_map))
        
    def detectCommonDir(self):
        common_dirs  = [0, 0, 0, 0]
        # for r, c in self.possibleloc:
        #     if self.ship.get_cellval(r-1, c) == 'o':
        #         common_dirs[0] += 1
        #     if self.ship.get_cellval(r, c-1) == 'o':
        #         common_dirs[1] += 1
        #     if self.ship.get_cellval(r+1, c) == 'o':
        #         common_dirs[2] += 1
        #     if self.ship.get_cellval(r, c+1) == 'o':
        #         common_dirs[3] += 1
        
        for _, _, dirs in self.possibleloc:
            if 'u' in dirs:
                common_dirs[0] += 1
            if 'l' in dirs:
                common_dirs[1] += 1
            if 'd' in dirs:
                common_dirs[2] += 1
            if 'r' in dirs:
                common_dirs[3] += 1

        
        max_value = max(common_dirs)
        max_index = common_dirs.index(max_value)
        match max_index:
            case 0:
                return 'u'
            case 1:
                return 'l'
            case 2:
                return 'd'
            case 3:
                return 'r'
            
                
        
    def moveBot(self, dir):
        moved = 0
        (r, c ) = self.getloc()
        if dir == 'u':
            r_n = r+1
        if dir == 'd':
            r_n = r-1
        if dir == 'l':
            c_n = c+1
        if dir == 'r':
            c_n = c-1
        # else:
        #     return (0,0)
        
        if self.ship.get_cellval(r_n, c_n) == 'b':
            for i in range(len(self.possibleloc)):
                if dir in self.possibleloc[i][2]:
                    self.possibleloc.pop(i)
            # for r,c,dirs in range(len(self.possibleloc)):
            #     if dir in dirs:
            #         self.possibleloc.remove((r,c))
            return False
        else:
            self.setloc(r_n,c_n)
            for i in range(len(self.possibleloc)):
                if dir not in self.possibleloc[i][2]:
                    self.possibleloc.pop(i)
            return (r-r_n, c-c_n)
        
        
    def getImgPath(self):
        return self.imgpath
        
    def getId(self):
        return self.id
    
    def explore(self):
        b8neighbors = self.senseNeighbors()
        loc = (0,0, b8neighbors)
        dirs = ['u', 'l', 'd', 'r']
        while len(self.possibleloc)>1:
            dir = random.choice(dirs)

    
    def calcBlockList(self):
        
        for r in range(0, self.ship.getSize()):
            for c in range(0, self.ship.getSize()):
                neighbors = self.ship.countNeighbors( r, c, 'b')
                if neighbors == 3: 
                    self.block3.append((r,c))
                elif neighbors == 2: 
                    self.block2.append((r,c))
                elif neighbors == 1: 
                    self.block1.append((r,c))
                else:
                    self.block0.append((r,c))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
        
        