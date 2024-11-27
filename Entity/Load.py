import numpy as np

class Load:
    def __init__(self, capacity=4, of=None):
        self.of = "Game Server Load" if of is None else "Game Server " + of + " Load"
        self.capacity = capacity
        self.resources = np.full(self.capacity, None)
        
    def add(self, resource):
        if None in self.resources:
            index = np.where(self.resources == None)[0][0]
            self.resources[index] = resource
        else:
            print("Load is full")
            
        return self.resources, self.isFull()
    
    
    def remove(self, resource):
        if self.resources == np.full(self.capacity, None):
            print("Load is empty")
        
        if resource in self.resources:
            index = np.where(self.resources == resource)[0][0]
            self.resources[index] = None
            
        else:
            print("Resource " + resource + " not found in load " + self.of)
            
        return self.resources, self.isFull()
    
    def isFull(self):
        return None not in self.resources
    
    def getAvailable(self):
        return np.sum(self.resources == None) 
    
    def getOccupied(self):
        return np.sum(self.resources != None) 
    
    def __str__(self):
        return self.of + " has " + str(self.getOccupied()) + " resource(s) out of " + str(self.capacity) + " resources"
    
        