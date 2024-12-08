"""Import Folder Paths"""
import os
import sys
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))

"""Import gRPC library and files as __RPC"""
import grpc
import Service.MasterService_pb2_grpc as masterRPC
import Service.GameService_pb2_grpc as gameServerRPC
import Service.ClientService_pb2_grpc as playerRPC

"""Import Entity Classes"""
from Entity.Server import Server
from Entity.Result import Result
from Entity.Player import Player
from Entity.Resource import Resource

"""Import Protocol Buffers as __PB"""
import Buffer.Result_pb2 as ResultPB
import Buffer.Player_pb2 as PlayerPB
import Buffer.GameServer_pb2 as GameServerPB
import Buffer.Resource_pb2 as ResourcePB

"""Class Definition and Implementation"""
"""Servicer inherits from __RPC.__Servicer"""
"""Servicer methods are defined as def __(self, request, context)"""
"""Stubs are defined in __RPC. __Stub"""
"""gRPC thread executors are defined as grpc.server(futures.ThreadPoolExecutor(max_workers=#))"""
"""Servers gRPC are bound to an address with add_insecure_port("ip:port)"""
"""Clients define bound server channels as grpc.insecure_channel("ip:port")"""
class GameServer(Server, gameServerRPC.ServerServicer):
  
    def pbToObject(pb):
        if not pb: return None
        resource = Resource.pbToObject(pb.resource)
        return GameServer(pb.ip, pb.port, pb.resourceLimit, resource)
    
    def objectToPb(obj):
        return GameServerPB.GameServer(
            ip= obj.ip,
            port=obj.port,
            resourceLimit=obj.resourceLimit,
            resource=Resource.objectToPb(obj.resource),
        )
    
    def __init__(self, ip="localhost", port=None, resourceLimit=4, resource=None):
        super().__init__(ip, port)
        self.resourceLimit = resourceLimit
        self.resource = Resource(resourceLimit) if resource is None else resource
        # self.master = grpc.inseucure_channel("localhost:7777")
        # self.masterStub = masterRPC.MasterStub(master)
        self.clients = {}
        
    def __str__(self):
        return f"Game Server running at {self.ip}:{self.port} with {self.resource}"
    def registerServer(self):
        try:
            result = self.masterStub.registerServer(GameServer.objectToPb(self))
            print(Result.pbToObject(result))
        except Exception as e:
            return Result(
                isSuccess=False,
                message=f"Error connecting to Master: {e}",
            )
            
    def connectPlayer(self, request, context):
        try:
            player = Player.pbToObject(request)
            if player is None:
                return Result(
                    isSuccess=False,
                    message="invalid data",
                )
        except Exception as e:
            return ResultPB.create(
                isSuccess=False,
                message=f"Error reading {context}: {e}",
            )
        try:
                if player not in self.clients:
                    self.clients[player]=player
                    message = f"Player {player.name} registered successfully"
                else:
                    message = f"Player {player.name} already registered"
                return ResultPB.create(
                    isSuccess=True,
                    message=message,
                )
                
        except Exception as e:
                return ResultPB.create(
                    isSuccess=False,
                    message=f"Error registering player {player.name}: {e}",
                )
    def test(self):
        stub = playerRPC.ClientStub(grpc.insecure_channel("localhost:9090"))
        player = Player(1,'ded',2,12)

# self.clients[context.peer()] = playerRPC.ClientStub(grpc.insecure_channel(context.peer()))