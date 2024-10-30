

class Cell:
    def __init__(self, r, c, val='b'):
        self.r = r 
        self.c = c
        self.val = val
        
        self.parent = [(None, None), (None, None),  (None, None), (None, None)]
        
        self.h = '-'
        self.dist = ' '
        self.tot = ' '
        
    def get_r(self):
        return self.r
    
    def get_c(self):
        return self.c
        
    def set_val(self, val):
        self.val = val
    
    def get_val(self):
        return self.val
    
    def set_parent(self, parent_r, parent_c, i):
        self.parent[i] =  (parent_r, parent_c)
   
    def get_parent(self, i):
        return self.parent[i]
    
    
    def get_h(self):
        return self.h

    def set_h(self,h):
        self.h = h
        
        
    def get_dist(self):
        return self.dist

    def set_dist(self,dist):
        self.dist = dist
        
        
    def get_tot(self):
        return self.tot

    def set_tot(self,tot):
        self.tot = tot
    
    