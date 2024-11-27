import os
import sys
sys.path.append(os.path.dirname("Algorithms"))

from Server import Server
from Linker import Linker
from Algorithms.LoadBalancing import ConsistentHashing

class Master(Server):
    def __init__(self, IP="localhost", port=7777):
        super().__init__(IP, port)
        self.loadBalancer = ConsistentHashing()
        self.registeredServers = [] #Linkers
        
    def __str__(self):
        return f"Master Server running at {self.IP}:{self.port}"

