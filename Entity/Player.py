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
import Buffer.Game_pb2 as GamePB
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
        
    
    def __init__(self, id=0, name="Player", health=3, score=0, master=None, gameServer=None, gameSession=None):
        if not id > 0: 
            Player.count += 1
            self.id = Player.count
        else:
            self.id = id
        self.name = name
        self.health = health
        self.score = score
        self.master = "localhost:7777" if master is None else master
        self.gameServer = None if gameServer is None else gameServer
        self.gameSession = None if gameSession is None else gameSession

    def __str__(self):
        return f"Player {self.id} : {self.name} has {self.score} score"
    
    def changeName(self,name):
        self.name = name
        
    async def connectPlayer(self, gameServer=None):
        if gameServer:
            self.gameServer = gameServer
            async with grpc.aio.insecure_channel(self.gameServer) as channel:
                self.gameServerStub = gameServerRPC.ServerStub(channel)
                try:
                    result = await self.gameServerStub.connectPlayer(Player.objectToPb(self))
                    return(Result.pbToObject(result))
                except Exception as e:
                    return(Result(
                        isSuccess=False,
                        message=f"Error connecting to Game Server {self.gameServer}: {e}",
                    ))
        else: return(Result(
                        isSuccess=False,
                        message=f"No Game Server provided or found",
                    ))

    async def disconnectPlayer(self):
        if self.gameServer:
             async with grpc.aio.insecure_channel(self.gameServer) as channel:
                self.gameServerStub = gameServerRPC.ServerStub(channel)
                try:
                    result = await self.gameServerStub.disconnectPlayer(Player.objectToPb(self))
                    return Result.pbToObject(result)
                except Exception as e:
                    return(Result(
                        isSuccess=False,
                        message=f"Error connecting to Game Server {self.gameServer}: {e}",
                    ))
        else: return(Result(
                        isSuccess=False,
                        message=f"No Game Server provided or found",
                    ))


    async def requestServer(self, gameSession=None):
        async with grpc.aio.insecure_channel(self.master) as channel:
            self.masterStub = masterRPC.MasterStub(channel)
            try:
                if gameSession:
                    self.gameSession = gameSession
                    result = await self.masterStub.requestServer(
                    ResultPB.Register(player= Player.objectToPb(self),
                                    game= self.gameSession)
                )
                else:
                    result = await self.masterStub.requestServer(
                        ResultPB.Register(
                            player=Player.objectToPb(self)
                        )
                    )
                try: 
                    self.gameServer = result.gameServerAddress
                    return result
                except Exception as e:
                    result = Result(
                        isSuccess=False,
                        message=f"Invalid Game Server data recieved: {e}",
                    )
                    return Result.objectToPb(result)
            except Exception as e:
                  result =Result(
                    isSuccess=False,
                    message=f"Error connecting to Master: {e}",
                    )
                  return Result.objectToPb(result)
              
    async def createGame(self, packs, duration):
        if self.gameServer:
            async with grpc.aio.insecure_channel(self.gameServer) as channel:
                self.gameServerStub = gameServerRPC.ServerStub(channel)
                try:
                    result = await self.gameServerStub.createGame(
                        ResultPB.Register(player= Player.objectToPb(self),
                        setting=GamePB.Setting(duration=duration, packs=packs))
                    )
                    return result
                except Exception as e:
                    return Result.objectToPb(Result(
                        isSuccess=False,
                        message=f"Error creating game {self.gameServer}: {e}",
                    ))
                    
        else: return Result.objectToPb(Result(
                        isSuccess=False,
                        message=f"No Game Server provided or found",
                    ))
        
    async def connectToGame(self,name, gameServer, gameSession):
        self.changeName(name)
        if gameServer:
            self.gameServer = gameServer
            self.gameSession = gameSession
            async with grpc.aio.insecure_channel(self.gameServer) as channel:
                self.gameServerStub = gameServerRPC.ServerStub(channel)
                try:
                    try:
                        pb =  ResultPB.Register(player= Player.objectToPb(self),
                                            game= gameSession) 
                    except Exception as e:
                        return Result(
                            isSuccess=False,
                            message=f"Invalid Game Server data recieved: {e}",
                        )
                    try:    
                        result = await self.gameServerStub.connectToGame(pb)
                        if (result.result.isSuccess): return {
                            "result": Result.pbToObject(result.result),
                            "game": result.game
                        }
                        else: return Result(
                            isSuccess=result.result.isSuccess,
                            message=result.result.message,
                        )
                    except Exception as e:
                        return Result(
                            isSuccess=False,
                            message=f"Error connecting to Game Server {self.gameServer}: {e}",
                        )
                except Exception as e:
                    return Result(
                        isSuccess=False,
                        message=f"Error connecting to Game Server {self.gameServer}: {e}",
                    )
        else: return Result(
                        isSuccess=False,
                        message=f"No Game Server provided or found",
                    )
                  
    async def startGame(self, game):
        if self.gameServer:
            async with grpc.aio.insecure_channel(self.gameServer) as channel:
                self.gameServerStub = gameServerRPC.ServerStub(channel)
                try:
                    result = await self.gameServerStub.startGame(
                        ResultPB.Register(player= Player.objectToPb(self),
                        game= game)
                    )
                    return {
                            "result": Result.pbToObject(result.result),
                            "game": result.game
                    }
                except Exception as e:
                    return Result(
                        isSuccess=False,
                        message=f"Error starting game {self.gameServer}: {e}",
                    )
        else: return Result(
                        isSuccess=False,
                        message=f"No Game Server provided or found",
                    )
    async def listen(self):
       await asyncio.gather(
            self.requestServer(),
            asyncio.sleep(3),
            self.connectPlayer(),
            self.disconnectPlayer()
            
        )    
