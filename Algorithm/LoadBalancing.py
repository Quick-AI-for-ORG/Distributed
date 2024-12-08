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

    def getServersForPlayer(self, playerId):
        hashVal = self.hashKey(str(playerId))
        sortedHashes = sorted(self.hashRing.keys())
        candidateServers = []
        for h in sortedHashes:
            if hashVal <= h:
                candidateServers.append(self.hashRing[h])

        # If no candidate found (wrap-around case), return the first server
        if not candidateServers:
            candidateServers.append(self.hashRing[sortedHashes[0]])
        return candidateServers
    def __str__(self):
        return f"Consistent Hashing Load Balancer with {self.numVirtualNodes} virtual nodes"



