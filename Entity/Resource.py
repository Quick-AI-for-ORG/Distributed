
import numpy as np

class Resource:
    def __init__(self, capacity=5, name=None):
        self.name = "Resource" if not name else name.title() + " resource"
        self.capacity = capacity
        self.current = 0
        self.items =np. full(self.capacity, None)
        
    def add(self, item):
        if self.current < self.capacity:
            self.items[self.current] = item
            self.current += 1
        else:
            print("Resource is full")
            
        return self.current , self.isFull()
    
    def remove(self, item):
        if self.current == 0:
            print("Resource is empty")
            
        elif item in self.items:
            index = np.where(self.items == item)[0][0] 
            self.items[index] = None
            self.current -= 1
            
        else:
            print(self.name + " does not contain item " + item)
          
        return self.current, self.isFull()
    
    def isFull(self):
        return self.current == self.capacity
    
    def getAvailable(self):
        return self.capacity - self.current
    
    def __str__(self):
        return self.name + " has " + str(self.current) + " item(s) out of " + str(self.capacity) + " items"
        