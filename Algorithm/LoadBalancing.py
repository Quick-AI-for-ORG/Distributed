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


    def removeServer(self, server):
        for i in range(self.numVirtualNodes):
            virtualNodeId = f"{server}#{i}"
            hashVal = self.hashKey(virtualNodeId)
            del self.hashRing[hashVal]

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



