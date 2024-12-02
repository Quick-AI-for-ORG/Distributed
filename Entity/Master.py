"""Import libraries"""
import os
import sys
import grpc
import concurrent.futures as futures

"""Import Folder Paths"""
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

"""Import gRPC files as __RPC"""
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
class Master(Server): 
    def __init__(self, ip="localhost", port=7777, registeredServers=None):
        super().__init__(ip, port)
        self.loadBalancer = ConsistentHashing()
        self.registeredServers = {} if registeredServers is None else registeredServers
        
    def __str__(self):
        return f"Master Server running at {self.ip}:{self.port}"

    def registerServer(self, request, context):
        try:
            server = GameServer.pbToObject(request.GameServer)
            if server is None:
                return ResultPB.create(
                    isSuccess=False,
                    message="Invalid server details",
                )
        except Exception as e:
            return ResultPB.create(
                isSuccess=False,
                message=f"Error reading {context.peer()}: {e}",
            )
        try:
            if server.getAddress() not in [server.getAddress() for server in self.registeredServers.keys()]:
                self.registeredServers[server] = True
                self.loadBalancer.addServer(server.getAddress())
                message = f"Server {server.getAddress()} registered successfully"
            else:
                self.registeredServers[server] = True 
                message = f"Server {server.getAddress()} already registered"
            
            return ResultPB.create(
                isSuccess=True,
                message=message,
            )
            
        except Exception as e:
            return ResultPB.create(
                isSuccess=False,
                message=f"Error registering server {server.getAddress()}: {e}",
            )
        
    def requestServer(self, request, context):
        print("")
        
    def runServicer(self):
        gRPCServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        masterRPC.add_MasterServicer_to_server(self, gRPCServer)
        gRPCServer.add_insecure_port(f"{self.ip}:{self.port}")
        gRPCServer.start()
        print(str(self))
        try: 
            
            self.test()
        except KeyboardInterrupt: print(f"Master Server {self.getAddress()} stopped.")
        
    def test(self):
        stub = masterRPC.MasterStub(grpc.insecure_channel("localhost:7777"))
        server = GameServer(ip="localhost", port=7778)
        try:
            result = stub.registerServer(GameServer.objectToPb(server))
            print(Result.pbToObject(result))
        except Exception as e: print(f"Error connecting to Master: {e}")
        
        
m = Master()

m.runServicer()