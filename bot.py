from queue import PriorityQueue
import random

from networkx import neighbors



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
        
        self.block3 = []
        self.block2 = []
        self.block1 = []
        self.block0 = []
        
    def getloc(self):
        return (self.r, self.c)
    
    def setloc(self, r, c):
        self.r = r 
        self.c = c
        
    def getImgPath(self):
        return self.imgpath
        
    def getId(self):
        return self.id
    
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
        
        