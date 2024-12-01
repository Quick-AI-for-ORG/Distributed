import hashlib
class ConsistentHashing:
    def __init__(self, numVirtualNodes=100):
        self.numVirtualNodes = numVirtualNodes
        self.hashRing = {}

    def hashKey(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def addServer(self, server):
        for i in range(self.numVirtualNodes):
            virtualNodeId = f"{server}#{i}"
            hashVal = self.hashKey(virtualNodeId)
            self.hashRing[hashVal] = server

        # self.serverLoads[serverId] = server.sessions.getAvalableSessions()

    def removeServer(self, server):
        for i in range(self.numVirtualNodes):
            virtualNodeId = f"{server}#{i}"
            del self.hashRing[hashVal]

        # del self.serverLoads[serverId]
        # if serverId in self.gameSessions.values():
        #     self.gameSessions = {session: srv for session, srv in self.gameSessions.items() if srv != serverId}

    def getServerForPlayer(self, playerId, gameId=None):
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

        leastLoadedServer = max(candidateServers, key=lambda serverId: self.serverLoads[serverId])

        if gameId:
            self.gameSessions[gameId] = leastLoadedServer

        return leastLoadedServer
    
    def __str__(self):
        return f"Consistent Hashing Load Balancer with {self.numVirtualNodes} virtual nodes"


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
#     if temp == server.Id:
#         server.load.add(game1)

        
# temp = LoadBalancer.getServerForPlayer(player3, game2.name)
# for server in servers:
#     if temp == server.Id:
#         server.load.add(game2)
        
# temp = LoadBalancer.getServerForPlayer(player4, game1.name)
# for server in servers:
#     if temp == server.Id:
#         server.load.add(game1)
        
        
# for server in servers:
#     print(server)
            
# print(LoadBalancer.gameSessions)

