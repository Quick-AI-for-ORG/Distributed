import random
from Resource import Resource
from Server import Server

class GameServer(Server):
    def __init__(self, IP="localhost", port=None, resourceLimit=4):
        super().__init__(IP, port)
        self.resources = Resource(resourceLimit) 
        
    def __str__(self):
        return f"Game Server running at {self.IP}:{self.port} with {self.resources}"
