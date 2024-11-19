import random

from cell import Cell

class Ship:
    def __init__(self, d, seed = None):
        self.random = random.Random(seed)
        self.d = d
        self.open = []
        self.blocked = []
        self.blocked1 = []
        self.deadend = []
        self.start_botloc = None
        self.botloc = [None, None, None, None]
        self.ratloc = None
        
        self.grid = [[Cell(row, col) for col in range(self.d)] for row in range(self.d)]
        self.ratPositions = []
        
    def getSize(self):
        return self.d
    
    def get_cell(self, r,c) -> Cell:
        return self.grid[r][c]
    
    def get_cellval(self, r, c):
        return self.grid[r][c].get_val()
    
    def set_cellval(self,r,c, val):
        self.grid[r][c].set_val(val)
        
    def getOpenCells(self):
        self.displayNumbers()
        return self.open
    
    def getStartBotLoc(self):
        return self.start_botloc
        
    def setBotLoc(self, r, c, i):
        self.botloc[i] = (r, c)
        
    def getBotLoc(self, i):
        return self.botloc[i]
        
    def getRatloc(self):
        return self.ratloc
    
    def setRatloc(self, loc):
        self.ratloc = loc
        self.ratPositions = [loc]
   
    def createRat(self):
        rs, cs = self.random.choice(self.open)
        self.ratloc = (rs, cs)
        self.ratPositions.append(self.ratloc)
     
    def checkRat(self,r, c):
        if self.ratloc == (r,c):
            return True
        else: 
            return False
        
    def moveRat(self,rand):
        r, c = self.ratloc
        moveCells = self.getNeighbors(r, c, 'o')    
        moveCells.append((r,c))
        self.ratloc = rand.choice(moveCells)
        self.ratPositions.append(self.ratloc)
        
    def getRatPositions(self):
        return self.ratPositions
    
    def getNeighbors(self, r,c, celltype):
        neighbourList = []
        if r>0:
            if self.get_cellval(r-1, c) == celltype:
                neighbourList.append((r-1, c) )
        if c>0:
            if self.get_cellval(r, c-1) == celltype:
                neighbourList.append((r, c-1) )
        if r<self.d-1:
            if self.get_cellval(r+1, c) == celltype:
                neighbourList.append((r+1, c) )
        if c<self.d-1:
            if self.get_cellval(r, c+1) == celltype:
                neighbourList.append((r, c+1) )
        return neighbourList
        
    def countNeighbors(self, r,c, celltype):
        count = 0
        if r>0:
            if self.get_cellval(r-1, c) == celltype:
                count += 1
        if c>0:
            if self.get_cellval(r, c-1) == celltype:
                count += 1
        if r<self.d-1:
            if self.get_cellval(r+1, c) == celltype:
                count += 1
        if c<self.d-1:
            if self.get_cellval(r, c+1) == celltype:
                count += 1
        return count
    
    def countBlock8(self, r, c):
        count = 0
        if r>0:
            if self.get_cellval(r-1, c) == 'b':
                count += 1
        if c>0:
            if self.get_cellval(r, c-1) == 'b':
                count += 1
        if r<self.d-1:
            if self.get_cellval(r+1, c) == 'b':
                count += 1
        if c<self.d-1:
            if self.get_cellval(r, c+1) == 'b':
                count += 1
        if self.get_cellval(r-1, c-1) == 'b':
            count += 1
        if self.get_cellval(r-1, c+1) == 'b':
            count += 1
        if self.get_cellval(r+1, c-1) == 'b':
            count += 1
        if self.get_cellval(r+1, c+1) == 'b':
            count += 1
        return count
    
    def calcBlockNeighbours(self):
        for r in range(1, self.d -1):
            for c in range(1, self.d -1):
                
                if self.get_cellval(r,c) == 'o':
                    cell = self.get_cell(r,c)
                    cell.set_b8neighbor(self.countBlock8(r,c)) 
    
    def blockOuter(self):
        for r in range(0, self.d):
            for c in [0, self.d-1]:
                self.set_cellval(r, c, 'b')
        
        for r in [0, self.d-1]:
            for c in range(0, self.d-1):
                self.set_cellval(r, c, 'b')
                
    def getInnerBlockedNeighbours(self, r,c):
        neighbourList = []
        if r>1:
            if self.get_cellval(r-1, c) == 'b':
                neighbourList.append((r-1, c) )
        if c>1:
            if self.get_cellval(r, c-1) == 'b':
                neighbourList.append((r, c-1) )
        if r<self.d-2:
            if self.get_cellval(r+1, c) == 'b':
                neighbourList.append((r+1, c) )
        if c<self.d-2:
            if self.get_cellval(r, c+1) == 'b':
                neighbourList.append((r, c+1) )
        return neighbourList
        
    def createShip(self):
        # open a random blocked blocked
        r_init = random.randint(1, self.d-2)
        c_init = random.randint(1, self.d-2)
        self.set_cellval(r_init,c_init, 'o')
        
        for r in range(1,self.d-1):
            for c in range(1,self.d-1):
                if self.grid[r][c].get_val() == 'b':
                    if self.countNeighbors(r,c, 'o')==1 :
                        self.blocked1.append((r,c))
            
        #opening random cells with 1 open neighbour        
        while len(self.blocked1)>0:
            (r_new, c_new) = random.choice(self.blocked1)
            self.set_cellval(r_new, c_new, 'o')
            
            self.blocked1 = []
            for r in range(1,self.d-1):
                for c in range(1,self.d-1):
                    if self.get_cellval(r,c) == 'b':
                        if self.countNeighbors(r,c, 'o')==1 :
                            self.blocked1.append((r,c))
                
        for r in range(1,self.d-1):
            for c in range(1,self.d-1):
                if self.get_cellval(r,c) == 'o':
                    if self.countNeighbors(r,c, 'o')==1 :
                        self.deadend.append((r,c))
        
       
        self.displayNumbers()          
       
        open_count = len(self.deadend)//2
        cell_opened = 0
        dead_neighbors = []
        while ((cell_opened < open_count) and len(self.deadend)>0):
            dead_neighbors = []
            for r,c in self.deadend:
                dead_neighbors.extend(self.getInnerBlockedNeighbours(r,c)) 
            (r_new, c_new) = random.choice(dead_neighbors)
            self.set_cellval(r_new, c_new, 'o')
            cell_opened += 1
            self.deadend = []
            for r in range(1,self.d-1):
                for c in range(1,self.d-1):
                    if self.get_cellval(r,c) == 'o':
                        if self.countNeighbors(r,c, 'o')==1 :
                            self.deadend.append((r,c))
        self.displayNumbers()             
        self.calcBlockNeighbours()
        self.createRat()
        
            
    def calcHeuristic(self):
        """Calculating the Manhattan distance
        """
        r_dest, c_dest = self.getRatloc()
        d = self.getSize()
        for r in range(d):
            for c in range(d):
                if self.get_cellval(r,c) != 'b': 
                    h = abs(r_dest-r) + abs(c_dest-c)
                    self.get_cell(r, c).set_h(h) 
        
    
    def displayShip(self):
        for r in range(0,self.d):
            print()
            for c in range(0, self.d):
                print(f"{self.grid[r][c].get_val():<4}", end=' ')
        
        print(f'Switch: {self.getRatloc()}')
        
    def displayNumbers(self):
        """update the list with cell values
        """
        self.blocked = []
        self.open = []
        self.firecells = []
        for r in range(0,self.d):
            for c in range(0,self.d):
                if self.get_cellval(r,c) == 'o':
                    self.open.append((r,c))
                if self.get_cellval(r,c) == 'b':
                    self.blocked.append((r,c))
