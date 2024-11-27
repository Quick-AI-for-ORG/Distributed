import os
import sys
sys.path.append(os.path.dirname("Algorithms"))

from Server import Server
from Algorithms.LoadBalancing import ConsistentHashing

class Master(Server):
    def __init__(self, IP="localhost", port=7777, name="Master Server"):
        super().__init__(IP, port)
        self.name = name
        self.loadBalancer = ConsistentHashing()
        
    def __str__(self):
        return f"{self.name} running at {self.IP}:{self.port}"
server = Master()
