import os
import sys
sys.path.append(os.path.dirname("Algorithm"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Entity"))

from Server import Server
from Algorithm.Mapper import Link
from Algorithm.LoadBalancing import ConsistentHashing

import grpc
import Service.MasterService_pb2 as types
import Service.MasterService_pb2_grpc as rpc

class Master(Server, rpc.Master, rpc.MasterServicer):
    def __init__(self, ip="localhost", port=7777, registeredServers=None):
        super().__init__(ip, port)
        self.loadBalancer = ConsistentHashing()
        self.registeredServers = [] if registeredServers is None else registeredServers
        
    def __str__(self):
        return f"Master Server running at {self.IP}:{self.port}"

    def registerServer(self, req, res):
        print(req)
        server = Link(req.gameServer)
        try:
            if server not in self.registeredServers:
                self.registeredServers.append(server)
                self.loadBalancer.addServer(server)
                message = f"Server {server} registered successfully"
            else:
                message = f"Server {server} already registered"
                
            return types.res(
                isSuccess=True,
                message=message,
            )
            
        except Exception as e:
            return types.res(
                success=False,
                message=f"Error registering server: {e}",
            )
        
        
        
m = Master()
