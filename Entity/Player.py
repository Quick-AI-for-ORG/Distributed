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
import Service.ClientService_pb2_grpc as playerRPC

"""Import Entity Classes"""
from Entity.Result import Result

"""Import Protocol Buffers as __PB"""
import Buffer.Result_pb2 as ResultPB
import Buffer.Player_pb2 as PlayerPB
import Buffer.GameServer_pb2 as GameServerPB

class Player:
    count = 0
    
    def pbToObject(pb):
        if not pb: return None
        return Player(pb.id, pb.name, pb.health, pb.score)
    
    def objectToPb(obj):
        return PlayerPB.Player(
            id= obj.id,
            name=obj.name,
            health=obj.health,
            score=obj.score,
        )
    
    def __init__(self, id=0, name="Player", health=3, score=0, master=None):
        if not id > 0: 
            Player.count += 1
            self.id = Player.count
        else:
            self.id = id
        self.name = name
        self.health = health
        self.score = score
        self.master = "localhost:7777" if master is None else master

    def __str__(self):
        return f"Player {self.id} : {self.name} with {self.health} health and {self.score} score"

    async def connectPlayer(self):
        if self.gameServer:
            async with grpc.aio.insecure_channel(self.gameServer) as channel:
                self.gameServerStub = gameServerRPC.ServerStub(channel)
                try:
                    result = await self.gameServerStub.connectPlayer(Player.objectToPb(self))
                    print(Result.pbToObject(result))
                except Exception as e:
                    print(Result(
                        isSuccess=False,
                        message=f"Error connecting to Game Server {self.gameServer}: {e}",
                    ))
        else: print(Result(
                        isSuccess=False,
                        message=f"No Game Server provided or found",
                    ))

    async def disconnectPlayer(self):
        if self.gameServer:
             async with grpc.aio.insecure_channel(self.gameServer) as channel:
                self.gameServerStub = gameServerRPC.ServerStub(channel)
                try:
                    result = await self.gameServerStub.disconnectPlayer(Player.objectToPb(self))
                    print(Result.pbToObject(result))
                except Exception as e:
                    print(Result(
                        isSuccess=False,
                        message=f"Error connecting to Game Server {self.gameServer}: {e}",
                    ))
        else: print(Result(
                        isSuccess=False,
                        message=f"No Game Server provided or found",
                    ))


    async def requestServer(self):
        async with grpc.aio.insecure_channel(self.master) as channel:
            self.masterStub = masterRPC.MasterStub(channel)
            try:
                if self.game:
                    result = await self.masterStub.requestServer(
                    ResultPB.Register(player= Player.objectToPb(self),
                                    game= Game.objectToPb(self.game))
                )
                else:
                    result = await self.masterStub.requestServer(
                        ResultPB.Register(
                            player=Player.objectToPb(self)
                        )
                    )
                print(Result.pbToObject(result.result))
                try: self.gameServer = f"{result.gameServer.ip}:{result.gameServer.port}"
                except Exception as e:
                    print(Result(
                        isSuccess=False,
                        message=f"Invalid Game Server data recieved: {e}",
                    ))
            except Exception as e:
                  print(Result(
                    isSuccess=False,
                    message=f"Error connecting to Master: {e}",
                ))



