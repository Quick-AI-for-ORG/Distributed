"""Import libraries"""
import os
import sys
import grpc
import random
import asyncio
import tracemalloc
import pandas as pd
import concurrent.futures as futures

"""Import Folder Paths"""
sys.path.append(os.path.dirname("Data"))
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

"""Import gRPC files as __RPC"""
import Service.MasterService_pb2_grpc as masterRPC
import Service.GameService_pb2_grpc as gameServerRPC

"""Import Entity Classes"""
from Entity.Game import Game
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
        resource = Resource.objectToPb(obj.resource)
        return GameServerPB.GameServer(
            ip= obj.ip,
            port=obj.port,
            resourceLimit=obj.resourceLimit,
            resource=resource,
        )
    
    def loadWordPacks(self):
        try:
            packs = {}
            for packName in os.listdir("./Data"):
                if packName.endswith(".csv"):
                    pack = pd.read_csv(f"./Data/{packName}")
                    packs[packName.split(".")[0]] = pack.values.flatten()
            return packs
        except Exception as e:
            print(Result(False,f"Error loading word packs: {e}"))
            
    def __init__(self, ip="localhost", port=None, resourceLimit=4, resource=None, master=None):
        super().__init__(ip, port)
        self.resourceLimit = resourceLimit
        self.resource = Resource(resourceLimit) if resource is None else resource
        self.master = "localhost:7777" if master is None else master
        self.clients = {}
        self.packs = self.loadWordPacks()
        
    def __str__(self):
        return f"Game Server running at {self.ip}:{self.port} with {self.resource}"
    
    async def registerServer(self):
        async with grpc.aio.insecure_channel(self.master) as channel:
            self.masterStub = masterRPC.MasterStub(channel)
            try:
                result = await self.masterStub.registerServer(GameServer.objectToPb(self))
                print(Result.pbToObject(result))
                return result
            except Exception as e:
                print( Result(
                    isSuccess=False,
                    message=f"Error connecting to Master: {e}",
                ))
                return Result(isSuccess=False, message=f"Error connecting to Master: {e}")
            
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
                    self.clients[ip].assignKey(ip)
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
                player = self.clients[ip]
                for session in self.resource.sessions:
                    if player in session.players:
                        session.removePlayer(player)
                        
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
                    message=f"Game Server {self.getAddress()} is healthy"
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
            for session in self.resource.sessions:
                if session.id == request.game:
                    player = self.clients[IPDecoder.getIP(context)[0]]
                    if session.round != 0:
                        await self.checkInput(session, player, request.update)
                        return ResultPB.Response(
                            result = ResultPB.create(
                                isSuccess=True,
                                message=f"Game {request.game} updated successfully",
                            ),
                            game = Game.objectToPb(session),
                            player = Player.objectToPb(session.getPlayer(player))
                        )
                    else:
                        session.playersInput = [f"{session.getWinner().name} won with {session.getWinner().score}"]
                        for temp in self.resource.sessions:
                            if temp.id == request.game:
                                for player in temp.players:
                                    await player.disconnectPlayer()
                                self.resource.removeSession(temp)
                        return ResultPB.Response(
                            result = ResultPB.create(
                                isSuccess=True,
                                message=f"End of Game",
                            ),
                            game = Game.objectToPb(session),
                            player = Player.objectToPb(session.getPlayer(player))
                        )
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Game {request.game} not found",
                )
            )
        except Exception as e:
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Error updating game {request.game}: {e}"
                )
            )
            
    async def recieveUpdate(self, request, context):
        try:
            for session in self.resource.sessions:
                if session.id == request.game:
                    player = self.clients[IPDecoder.getIP(context)[0]]
                    if session.round != 0:
                        if len(session.playersInput) > 1:
                            if session.playersInput[0].split()[-1] == session.getPreviousWord(): 
                                session.playersInput.remove(session.playersInput[0])
                        return ResultPB.Response(
                            result = ResultPB.create(
                                isSuccess= await self.checkRound(session),
                                message=f"Game {request.game} updated successfully",
                            ),
                            game = Game.objectToPb(session),
                            player = Player.objectToPb(session.getPlayer(player))
                        )
                    else:
                        session.playersInput = [f"{session.getWinner().name} Won with {session.getWinner().score}"]
                        for temp in self.resource.sessions:
                            if temp.id == request.game:
                                self.resource.removeSession(temp)
                        return ResultPB.Response(
                            result = ResultPB.create(
                                isSuccess=True,
                                message=f"End of Game",
                            ),
                            game = Game.objectToPb(session),
                            player = Player.objectToPb(session.getPlayer(player))
                        )
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Game {request.game} not found",
                )
            )
        except Exception as e:
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Error updating game {request.game}: {e}"
                )
            )
    async def createGame(self, request, context):
       try:
            settings = (request.setting.duration, request.setting.packs)
            if not settings:
                return ResultPB.Response(result=ResultPB.create(
                    isSuccess=False,
                    message="Invalid Game Settings"
                ))
            ip = IPDecoder.getIP(context)[0]
            player = self.clients[ip]
            words = self.pickWords(settings)
            game = Game(settings= settings, words=words) 
            game.addPlayer(player)
            self.resource.sessions.append(game)
            try:
                result = await self.registerServer()
                return ResultPB.Response(result=ResultPB.create(
                    isSuccess=True,
                    message=f"Game {game.id} created successfully"
                    ), game=Game.objectToPb(game))
                
            except Exception as e:
                return ResultPB.Response(result=ResultPB.create(
                    isSuccess=False,
                    message=f"Error creating game: {e}"
                ))
                
       except Exception as e:
            return ResultPB.Response(result=ResultPB.create(
                isSuccess=False,
                message=f"Error creating game: {e}"
            ))
           
    async def connectToGame(self, request, context):
        try:
            player = Player.pbToObject(request.player)
            if player is None:
                return ResultPB.Response(
                    result = ResultPB.create(
                    isSuccess=False,
                    message="Invalid Player Details"
                ))
        except Exception as e:
            return ResultPB.Response(
                result = ResultPB.create(
                isSuccess=False,
                message=f"Error reading player details from {context.peer()}: {e}"
            ))
        try:
            for session in self.resource.sessions:
                if session.id == request.game:
                    ip = IPDecoder.getIP(context)[0]
                    if session.getAvalableSlots() > 0:
                        self.clients[ip]= player
                        self.clients[ip].assignKey(ip)
                        session.removePlayer(self.clients[ip])
                        session.addPlayer(self.clients[ip])
                        try:
                            result = await self.registerServer()
                            return ResultPB.Response(
                                result = ResultPB.create(
                                    isSuccess=True,
                                    message=f"Connected to {request.game} successfully",
                            ),
                                game = Game.objectToPb(session)
                            )
                        except Exception as e:
                            print(f"Error updating: {e}")
                            return ResultPB.Response(
                                result = ResultPB.create(
                                    isSuccess=False,
                                    message=f"Error connecting to game {request.game}: {e}",
                            ))
                    else:
                        return ResultPB.Response(
                            result = ResultPB.create(
                                isSuccess=False,
                                message=f"Game {request.game} is full",
                        )                
                            )
          
            return ResultPB.Response(
                result = ResultPB.create(
                    isSuccess=False,
                    message=f"Game {request.game} not found",
                )
            )
        except Exception as e:
            print(f"Error connecting to game: {e}")
            return ResultPB.Response(
                result = ResultPB.create(
                isSuccess=False,
                message=f"Error connecting to game {request.game}: {e}"
            ))
        
    async def startGame(self, request, context):
      try:
            for session in self.resource.sessions:
                if session.id == request.game:
                    if session.getAvalableSlots() > 0:
                      return ResultPB.Response(
                          result = ResultPB.create(
                              isSuccess=False,
                              message=f"Game {request.game} is not full",
                          ),
                          game = Game.objectToPb(session)
                      )
                    else:
                      return ResultPB.Response(
                      result = ResultPB.create(
                          isSuccess=True,
                          message=f"Game {request.game} started successfully",
                      ),
                      game = Game.objectToPb(session)
                  )
            return ResultPB.Response(
                    result = ResultPB.create(
                    isSuccess=False,
                    message=f"Game {request.game} not found",
                )
             )  
      except Exception as e:
            return ResultPB.Response(
                result = ResultPB.create(
                isSuccess=False,
                message=f"Error starting game {request.game}: {e}"
            )
        ) 
            
    def pickWords(self,settings):
        num = 8 if settings[0] == 'short' else 16
        packs = settings[1]
        words = []
        while len(words) != num:
            for pack in settings[1]:
                if len(words) == num:
                    break
                words.append(self.packs[pack][random.randint(0,len(self.packs[pack]))])
        return words
          
            
    async def listen(self):
       await asyncio.gather(
            self.registerServer(),
            self.runServicer()
            )


    async def checkInput(self, game, player, input):
        if game.getClueGiver().key == player.key:
            if input == 'SKIP PLEASE' :
                word = game.getWord()
                game.nextRound()
                game.playersInput.append(
                f"{player.name} asked to skip. Skipping this round. Correct guess was {word}"
            )             
            elif game.validateClue(input):
                player.updateScore(5)
                game.addInput(f"{player.name} : {input}")
            else:
                player.updateScore(-10)
                game.playersInput.append(f"{player.name} : ********************************")
                player.reduceHealth()
                if player.health == 0:
                    word = game.getWord()
                    game.nextRound()
                    game.playersInput.append(
                    f"{player.name} keeps typing invalid clues. Skipping this round. Correct guess was {word}"
            )
        else:
            game.addInput(f"{player.name} : {input}")
            if game.validateGuess(input):
                if player.health == 3:
                    player.updateScore(25)
                elif player.health == 2:
                    player.updateScore(20)
                elif player.health == 1:
                    player.updateScore(15)
                word = game.getWord()
                game.nextRound()
                game.playersInput.append(f"{player.name} guessed it Correctly. Word was {word}")
            else:
                player.reduceHealth()

        game.updatePlayer(player)



    async def checkRound(self, game):
        if game.round != 0:
            clueGiver = game.getClueGiver()

            if clueGiver.health == 0:
                word = game.getWord()
                game.nextRound()
                game.playersInput.append(
                    f"{clueGiver.name} keeps typing invalid clues. Skipping this round. Correct guess was {word}"
                )
                return False

            tries = 0
            for player in game.players:
                if game.getClueGiver().key != player.key:
                    tries += player.health

            if tries == 0:
                for player in game.players:
                    if game.getClueGiver().key == player.key:
                        player.updateScore(-15)
                    else:
                        player.updateScore(-10)
                    game.updatePlayer(player)
                word=game.getWord()
                game.nextRound()
                game.playersInput.append(
                    f"Guessers are out of tries, {game.getClueGiver().name} failed. Skipping this round. Correct guess was {word}"
                )
                return False
            else:
                return True
            
        return False


                    
            
        
                