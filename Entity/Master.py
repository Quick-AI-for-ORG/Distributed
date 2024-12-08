"""Import libraries"""
import os
import sys
import grpc
import asyncio
import concurrent.futures as futures

"""Import Folder Paths"""
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

"""Import gRPC files as __RPC"""
import Service.MasterService_pb2_grpc as masterRPC
import Service.GameService_pb2_grpc as gameServerRPC

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
import Algorithm.IPDecoder as IPDecoder


"""Class Definition and Implementation"""
"""Servicer inherits from __RPC.__Servicer"""
"""Servicer methods are defined as def __(self, request, context)"""
"""Stubs are defined in __RPC. __Stub"""
"""gRPC thread executors are defined as grpc.server(futures.ThreadPoolExecutor(max_workers=#))"""
"""Servers gRPC are bound to an address with add_insecure_port("ip:port)"""
"""Clients define bound server channels as grpc.insecure_channel("ip:port")"""
class Master(Server): 
    def __init__(self, ip="localhost", port=7777, registeredServers=None, activeSessions=None):
        super().__init__(ip, port)
        self.loadBalancer = ConsistentHashing()
        self.registeredServers = {} if registeredServers is None else registeredServers
        self.activeSessions = {} if activeSessions is None else activeSessions
    def __str__(self):
        return f"Master Server running at {self.ip}:{self.port}"

    async def registerServer(self, request, context):
        async with grpc.aio.insecure_channel(self.getAddress) as channel:
            self.gameStub = gameServerRPC.ServerStub(channel)
        try:
            
            ip,port = IPDecoder.getIP(context)
            server = GameServer.pbToObject(request)
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
            if server.getAddress() not in list(self.registeredServers.keys()):
                self.registeredServers[server.getAddress()] = (server, True)
                self.loadBalancer.addServer(server.getAddress())
                message = f"Server {server.getAddress()} registered successfully"
            else:
                self.registeredServers[server.getAddress()] = (server, True)
                self.addSessionToServer(server)
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
        
    async def requestServer(self, request, context):
        try:
            player = Player.pbToObject(request.player)
            if player is None:
                return ResultPB.Response(
                    result = ResultPB.create(
                        isSuccess=True,
                        message=f"Server {server.getAddress()} found for game {request.game.id}",
                    ),
                )
        except Exception as e:
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Error reading {context.peer()}: {e}",
                ),
            )
        try:
            if request.game :
                if request.game in list(self.activeSessions.keys()):
                    address = self.activeSessions[request.game]
                    server = self.registeredServers[address][0]
                    return ResultPB.Response(
                        result = ResultPB.create(
                            isSuccess=True,
                            message=f"Server {server.getAddress()} found for game {request.game}",
                        ),
                        gameServer = GameServer.objectToPb(server),
                    )
                else:
                    return ResultPB.Response(
                        result = ResultPB.create(
                            isSuccess=False,
                            message=f"Game {request.game} not found",
                        ),
                    )
        except Exception as e:
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Error requesting server for {request.game} from {context.peer()}"
                ),
            )
              
        try:     
            candidateServers = self.loadBalancer.getServersForPlayer(player.id)
            found = {}
            for server in candidateServers:
                if self.registeredServers[server][1]:
                    found[self.registeredServers[server][0]] = self.registeredServers[server][0].resource.getAvalableSessions()
                    
            server = max(found, key=found.get)
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=True,
                    message=f"Server {server.getAddress()} found for player {str(player)}",
                ),
                gameServer = GameServer.objectToPb(server),
            )

        except Exception as e: 
            return ResultPB.Response(
                        result = ResultPB.create(
                            isSuccess=False,
                            message=f"Error requesting server for {request.player} from {context.peer()}"
                        ),
                    )
    
    
    def addSessionToServer(self, server):
        for game in server.resource.sessions:
            if game.id not in self.activeSessions.keys():
                self.activeSessions[game.id] = server.getAddress()

    async def runServicer(self):
        gRPCServer = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        masterRPC.add_MasterServicer_to_server(self, gRPCServer)
        gRPCServer.add_insecure_port(f"{self.ip}:{self.port}")
        
        try:
            await gRPCServer.start()
            print(str(self))
            await gRPCServer.wait_for_termination() 
            
        except asyncio.CancelledError:
            print(f"Master Server {self.getAddress()} Stopped")
        except KeyboardInterrupt:
            print(f"Master Server {self.getAddress()} Stopped")
        finally:
            await gRPCServer.stop(grace=None)
            
    async def main(self):
        await self.runServicer()

