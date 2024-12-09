"""Import libraries"""
import os
import sys
import grpc
import asyncio
import tracemalloc
import concurrent.futures as futures

"""Import Folder Paths"""
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

"""Import gRPC files as __RPC"""
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
import Buffer.GameServer_pb2 as GameServerPB
import Buffer.Game_pb2 as GamePB

"""Import Algorithms"""
import Algorithm.IPDecoder as IPDecoder

"""Class Definition and Implementation"""
"""Servicer inherits from __RPC.__Servicer"""
"""Servicer methods are defined as def __(self, request, context)"""
"""Stubs are defined in __RPC. __Stub"""
"""gRPC thread executors are defined as grpc.server(futures.ThreadPoolExecutor(max_workers=#))"""
"""Servers gRPC are bound to an address with add_insecure_port("ip:port)"""
"""Clients define bound server channels as grpc.insecure_channel("ip:port")"""
class GameServer(Server): 
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
    
    def __init__(self, ip="localhost", port=None, resourceLimit=4, resource=None, master=None):
        super().__init__(ip, port)
        self.resourceLimit = resourceLimit
        self.resource = Resource(resourceLimit) if resource is None else resource
        self.master = "localhost:7777" if master is None else master
        self.clients = {}
        
    def __str__(self):
        return f"Game Server running at {self.ip}:{self.port} with {self.resource}"
    
    async def registerServer(self):
        async with grpc.aio.insecure_channel(self.master) as channel:
            self.masterStub = masterRPC.MasterStub(channel)
            try:
                result = await self.masterStub.registerServer(GameServer.objectToPb(self))
                print(Result.pbToObject(result))
            except Exception as e:
                print( Result(
                    isSuccess=False,
                    message=f"Error connecting to Master: {e}",
                ))
            
    async def connectPlayer(self, request, context):
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
                ip = IPDecoder.getIP(context)[0]
                if ip not in list(self.clients.keys()):
                    self.clients[ip]= player
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
    async def disconnectPlayer(self, request, context):
        try:
            player = Player.pbToObject(request)
            if player is None:
                return ResultPB.create(
                    isSuccess = False,
                    message = "Invalid Player Details",
                )
        except Exception as e:
            return ResultPB.create(
                isSuccess = False,
                message=f"Error reading player details from {context.peer()}: {e}",
            )
        try:
            ip = IPDecoder.getIP(context)[0]
            if ip in list(self.clients.keys()):
                del self.clients[ip] 
                message = f"Player {player.name} disconnected successfully"
            else:
                message = f"Player {player.name} not found in active players"
            
            return ResultPB.create(
                isSuccess = True,
                message = message,
            )
        except Exception as e:
            return ResultPB.create(
                isSuccess = False,
                message= f"Error disconnecting player {player.name}: {e}",
            )
        



    async def runServicer(self):
        gRPCServer = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        gameServerRPC.add_ServerServicer_to_server(self, gRPCServer)
        gRPCServer.add_insecure_port(f"{self.ip}:{self.port}")
        
        try:
            await gRPCServer.start()
            print(str(self))
            await gRPCServer.wait_for_termination() 
            
        except KeyboardInterrupt:
            await gRPCServer.stop(0)
            await gRPCServer.shutdown()
            print(f"Game Server {self.getAddress()} Stopped")
        
        
    
    async def checkHealth(self, request, context):
        try:
                    message=f"Server {self.ip} is healthy"
                    print(message)
                    return ResultPB.create(
                        isSuccess = True,
                        message= message
                    )
        except Exception as e:
            return ResultPB.create(
                isSuccess = False,
                message= f"Error checking server {self.ip} health: {e}"
            )
                
 
    async def sendUpdate(self, request, context):

        try:
            change = request.change
            timestamp = request.timestamp
            game_details = request.game

            print(f"Update received: {change} at {timestamp}")
            print(f"Game Details: {game_details}")
                #    Validate Game Logic
            for player_id, player_stub in self.clients.items():
                try:
                    await player_stub.receiveUpdate(request)
                    print(f"Update sent to player {player_id}")
                except Exception as e:
                    print(f"Failed to send update to player {player_id}: {e}")

            return ResultPB.create(
                isSuccess=True,
                message="Update sent to all players successfully."
            )

        except Exception as e:
            return ResultPB.Result(
                isSuccess=False,
                message=f"Failed to send update: {e}"
            )
            
    async def createGame(self, request, context):
       try:
           settings = (request.duration, request.packs)
           if not settings:
               return ResultPB.create(
                   isSuccess=False,
                   message="Invalid Game Settings"
               )
           game = Game(
                        players = [self.clients.get(IPDecoder(context.peer()[0]))],
                        settings= settings
                    )
           self.resource.sessions.append(game)
           return ResultPB.create(
                isSuccess=True,
                message=f"Game {game.id} created successfully"
              )
       except Exception as e:
            return ResultPB.create(
                isSuccess=False,
                message=f"Error creating game: {e}"
            )
           
    async def connectToGame(self, request, context):
        try:
            game = Game.pbToObject(request)
            if game is None:
                return ResultPB.Response(
                    result = ResultPB.create(
                    isSuccess=False,
                    message="Invalid Game Details"
                ))
        except Exception as e:
            return ResultPB.Response(
                result = ResultPB.create(
                isSuccess=False,
                message=f"Error reading game details from {context.peer()}: {e}"
            ))
        try:
            for session in self.resource.sessions:
                if session.id == game.id:
                    session.addPlayer(self.clients.get(IPDecoder(context.peer()[0])))
                    ResultPB.Response(
                        result = ResultPB.create(
                            isSuccess=True,
                            message=f"Connected to {game.id} successfully",
                    ),
                        game = Game.objectToPb(session)
            )
          
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Game {game.id} not found",
                )
            )
        except Exception as e:
            return ResultPB.create(
                isSuccess=False,
                message=f"Error connecting to game {game.id}: {e}"
            )
        
    async def listen(self):
       await asyncio.gather(
            self.runServicer(),
            self.registerServer(),)

