from calendar import c
from ship import Ship
from queue import PriorityQueue
import numpy as np

class Astar:
    def __init__(self, start , dest,possibleRat,  ship: Ship):
        self.start = start
        self.dest = dest
        self.ship = ship
        self.shipSize = self.ship.getSize()
        self.possibleRat = possibleRat
        
        
        self.visited = []
        self.fringe = PriorityQueue()
        self.fringe_items = []
        
        self.h = np.full((self.shipSize, self.shipSize), 1000, dtype = np.int32)
        self.dist = np.full((self.shipSize, self.shipSize), 1000, dtype = np.int32)
        self.tot = np.full((self.shipSize, self.shipSize), 1000, dtype = np.int32)
        
        self.parent = np.empty((self.shipSize, self.shipSize), dtype=object)
        self.calcHeuristic()
        # self.findPath()
        
        
    def calcHeuristic(self):
        """Calculating the manhattan distance
        """
        r_dest, c_dest = self.dest
        d = self.shipSize
        for r in range(d):
            for c in range(d):
                if self.ship.get_cellval(r,c) != 'b': 
                    
                    h = abs(r_dest-r) + abs(c_dest-c)
                    if (r,c) not in self.possibleRat:
                        h+=1
                    self.h[r,c] = h
                    
    def tracePath(self):
        # print(f"Tracing path{self.dest}\n")
        path = []
        r, c = self.dest
        while r is not None and c is not None:
            # print(f"({r}, {c}) ", end=',')
            path.append((r,c))
            r, c = self.parent[r,c]
            if (r,c) == self.start:
                break
        path.reverse()
        # print(f'PATH: {path}')
        return path
        
                    
                    
    def update_priority(self, old_item, new_p1):
        temp_list = []
        edit_fringe = False
        
        # Temporarily store elements and remove the one to update
        while not self.fringe.empty():
            p_old, item = self.fringe.get()
            
            if item == old_item:
                # Update the priority of the target item
                if new_p1< p_old:
                    temp_list.append((new_p1, item))
                    edit_fringe = True
                else:
                    temp_list.append((p_old, item))
            else:
                temp_list.append((p_old, item))
        
        # Reinsert all elements back into the queue
        for item in temp_list:
            self.fringe.put(item)   
        return edit_fringe
    
    def findPath(self):
        r_start, c_start = self.start
        r_dest, c_dest = self.dest
        
        
        if self.start == self.dest:
            print(f"a-star : {self.start} to {self.dest}")
            return []
        
        possibleCells = self.possibleRat
        
        self.dist[r_start,c_start] = 0
        p_start = self.h[r_start, c_start]
        self.tot[r_start, c_start] = p_start
        self.fringe.put((p_start, (r_start, c_start)))
        self.fringe_items.append((r_start, c_start))
        t=0
        while not self.fringe.empty():
            t+=1
            
            p_curr, curr = self.fringe.get()
            # print(f"astar t: {t}, curr: {curr}")
            self.fringe_items.pop(0)
            
            r_curr , c_curr = curr
            self.visited.append(curr)
            
            if curr == self.dest:
                self.path = self.tracePath()
                return self.path
            
            cost = self.tot[r_curr, c_curr] + 1
            
            o_neighbors = self.ship.getNeighbors(r_curr, c_curr, 'o')
            neighbors = [neighbour for neighbour in o_neighbors if neighbour not in self.visited]
            
            for neighbor in neighbors:
                r_child, c_child = neighbor
                if neighbor in self.fringe_items:
                    if cost< self.dist[r_child,c_child]:
                        self.dist[r_child,c_child] = cost
                        self.parent[r_child, c_child] = (r_curr, c_curr)
                        
            
                else:
                    self.dist[r_child,c_child] = cost
                    self.parent[r_child, c_child] = (r_curr, c_curr)
            
        
                p = self.dist[r_child, c_child] + self.h[r_child, c_child]
                if (r_child, c_child) in self.fringe_items: 
                    fringe_edited = self.update_priority( (r_child, c_child), p)
                    if fringe_edited: 
                        self.tot[r_curr, c_curr] 
                else:
                    self.fringe.put((p, (r_child, c_child)))
                    self.tot[r_child, c_child] = p
                    self.fringe_items.append((r_child, c_child))
                
        print(f"!!! Failure in a-star !!! for {self.start} to {self.dest}")
        return []