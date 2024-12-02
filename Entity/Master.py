import os
import sys
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

from Entity.Server import Server
from Entity.GameServer import GameServer
from Algorithm.LoadBalancing import ConsistentHashing
from Buffer.Result_pb2 import Result
import Entity.Result

import grpc
import Service.MasterService_pb2_grpc as rpc

class Master(Server, rpc.MasterServicer):
    def __init__(self, ip="localhost", port=7777, registeredServers=None):
        super().__init__(ip, port)
        self.loadBalancer = ConsistentHashing()
        self.registeredServers = {} if registeredServers is None else registeredServers
        
    def __str__(self):
        return f"Master Server running at {self.IP}:{self.port}"

    def registerServer(self, request, context):
        try:
            server = GameServer.pbToObject(request.GameServer)
            if server is None:
                return Result(
                    isSuccess=False,
                    message="Invalid server details",
                )
        except Exception as e:
            return Result(
                isSuccess=False,
                message=f"Error reading {context}: {e}",
            )
        try:
            if server not in self.registeredServers:
                self.registeredServers[server] = True
                self.loadBalancer.addServer(server.getAddress())
                message = f"Server {server.getAddress()} registered successfully"
            else:
                self.registeredServers[server] = True 
                message = f"Server {server.getAddress()} already registered"
            
            return Result(
                isSuccess=True,
                message=message,
            )
            
        except Exception as e:
            return Result(
                isSuccess=False,
                message=f"Error registering server {server.getAddress()}: {e}",
            )
        
        
        
m = Master()

print(Entity.Result.Result.pbToObject(m.registerServer(None, None)))
