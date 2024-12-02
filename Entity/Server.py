import random

class Server:
    def __init__(self, ip="localhost", port=None):
        self.ip = ip
        self.port = port if port is not None else int(random.randint(49152, 65535))
        
    def __str__(self):
        return f"{self.name} Server running at {self.IP}:{self.port}"
    
    def __dict__(self):
        return {"IP": self.ip, "port": self.port}
    
    def getAddress(self):
        return f"{self.ip}:{self.port}"