import hashlib
from Entity.Server import Server
from Entity.Resource import Resource
class ConsistentHashing:
    def __init__(self, numVirtualNodes=100):
        self.numVirtualNodes = numVirtualNodes
        self.hashRing = {}
        self.serverLoads = {}
        self.gameSessions = {} 

    def hashKey(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def addServer(self, server):
        serverId = server.serverId
        for i in range(self.numVirtualNodes):
            virtualNodeId = f"{serverId}#{i}"
            hashVal = self.hashKey(virtualNodeId)
            self.hashRing[hashVal] = serverId

        self.serverLoads[serverId] = server.load.getOccupied()

    def removeServer(self, server):
        serverId = server.serverId
        for i in range(self.numVirtualNodes):
            virtualNodeId = f"{serverId}#{i}"
            del self.hashRing[hashVal]

        del self.serverLoads[serverId]
        if serverId in self.gameSessions.values():
            self.gameSessions = {session: srv for session, srv in self.gameSessions.items() if srv != serverId}

    def getServerForPlayer(self, playerId, gameId=None):
        # If a session ID is provided, return the server associated with that session
        if gameId and gameId in self.gameSessions:
            return self.gameSessions[gameId]

        hashVal = self.hashKey(playerId)
        sortedHashes = sorted(self.hashRing.keys())

        candidateServers = []
        for h in sortedHashes:
            if hashVal <= h:
                candidateServers.append(self.hashRing[h])
        if not candidateServers:
            candidateServers.append(self.hashRing[sortedHashes[0]])

        leastLoadedServer = min(candidateServers, key=lambda serverId: self.serverLoads[serverId])

        if gameId:
            self.gameSessions[gameId] = leastLoadedServer

        return leastLoadedServer


# LoadBalancer = ConsistentHashing()
# servers = [Server(), Server(), Server()]

# LoadBalancer.addServer(servers[0])
# LoadBalancer.addServer(servers[1])
# LoadBalancer.addServer(servers[2])

# game1 = Resource(name="game1")
# game2 = Resource(name="game2")

# player1 = "Player1"
# player3 = "Player3"
# player4 = "Player4"

# temp = LoadBalancer.getServerForPlayer(player1, game1.name)
# for server in servers:
#     if temp == server.serverId:
#         server.load.add(game1)

        
# temp = LoadBalancer.getServerForPlayer(player3, game2.name)
# for server in servers:
#     if temp == server.serverId:
#         server.load.add(game2)
        
# temp = LoadBalancer.getServerForPlayer(player4, game1.name)
# for server in servers:
#     if temp == server.serverId:
#         server.load.add(game1)
        
        
# for server in servers:
#     print(server)
            
# print(LoadBalancer.gameSessions)

