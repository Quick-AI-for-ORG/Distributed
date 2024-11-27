import random

class Server:
    def __init__(self, IP="localhost", port=None):
        self.IP = IP 
        self.port = port if port is not None else int(random.randint(49152, 65535))
        self.Id = f"{self.IP}:{self.port}"
        
    def __str__(self):
        return f"{self.name} Server running at {self.IP}:{self.port}"
    
