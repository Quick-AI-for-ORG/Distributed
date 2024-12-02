"""Import Folder Paths"""
import os
import sys
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

"""Import gRPC library and files as __RPC"""
import grpc
import Service.MasterService_pb2_grpc as masterRPC

"""Import Entity Classes"""
from Entity.Server import Server
from Entity.Result import Result
from Entity.Player import Player
from Entity.GameServer import GameServer

"""Import Protocol Buffers as __PB"""
import Buffer.Result_pb2 as ResultPB
import Buffer.Player_pb2 as PlayerPB
import Buffer.GameServer_pb2 as GameServerPB
import Buffer.Resource_pb2 as ResourcePB

"""Import Algorithms"""
from Algorithm.LoadBalancing import ConsistentHashing


"""Class Definition and Implementation"""
"""Servicer inherits from __RPC.__Servicer"""
"""Servicer methods are defined as def __(self, request, context)"""
"""Stubs are defined in __RPC. __Stub"""
"""gRPC thread executors are defined as grpc.server(futures.ThreadPoolExecutor(max_workers=#))"""
"""Servers gRPC are bound to an address with add_insecure_port("ip:port)"""
"""Clients define bound server channels as grpc.insecure_channel("ip:port")"""
class Master(Server, masterRPC.MasterServicer): 
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
        
        
        
        def run(self):
            gRPCServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            masterRPC.add_MasterServicer_to_server(self, gRPCServer)
            gRPCServer.add_insecure_port(f"{self.IP}:{self.port}")
            gRPCServer.start()
            gRPCServer.wait_for_termination()
        
m = Master()

