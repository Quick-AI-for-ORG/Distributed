import random
from Entity.Load import Load

class Server:
    def __init__(self, IP="localhost", port=None, load=4, name="Game"):
        self.IP = IP 
        self.port = port if port is not None else int(random.randint(49152, 65535))
        
        self.serverId = f"{self.IP}:{self.port}"
        if load is not None:
            self.load = Load(capacity=load, of=self.serverId)
            
        self.name = name
        
    def __str__(self):
        return f"{self.name} Server running at {self.IP}:{self.port} with {str(self.load)}"
    
