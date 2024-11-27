class Game: 
    def __init__(self, name="Game", server=None):
        self.name = name
        self.server = server
        
    def __str__(self):
        return f"{self.name} Game running on {self.server}"