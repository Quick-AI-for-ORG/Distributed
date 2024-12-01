class Linker:
    def __init__(self, gameServer):
        self.gameServer = gameServer
        for gameSession in gameServer.Resource.sessions:
            self.activeGames[gameSession.gameId] = gameSession
        self.isHealthy = True
        
    def __str__(self):
        return f"Game Server {self.gameServer.Id} is {'running' if self.isHealthy else 'crashed'}"
    
    def update(self):
        for gameSession in self.gameServer.Resource.sessions:
            self.activeGames[gameSession.gameId] = gameSession