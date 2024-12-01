
import numpy as np

import os
import sys
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Entity"))

import Service.Game_pb2 as pb2

from Entity.Player import Player

class Game:
    count = 0
    
    def pbToObject(pb):
        if not pb: return None
        players = []
        for player in pb.players:
            players.append(Player.pbToObject(player))
        
        return Game(pb.id, pb.name, pb.MAX_PLAYERS, players)
    
    def objectToPb(obj):
        players = []
        for player in obj.players:
            players.append(Player.objectToPb(player))
            
        return pb2.Game(
            id= obj.id,
            name=obj.name,
            MAX_PLAYERS=obj.MAX_PLAYERS,
            players=players,
        )
    
    def __init__(self, id=0, name="Game", maxPlayers=4, players=None):
        if not id > 0: 
            Game.count += 1
            self.id = Game.count
        else:
            self.id = id
        self.name = name
        self.MAX_PLAYERS = maxPlayers
        self.players = [] if players is None else players
       
 
    def getAvalableSlots(self):
        return self.MAX_PLAYERS - len(self.players)
        
    def addPlayer(self, player):
        if self.getAvalableSlots() > 0:
            if player not in self.players:
                self.players.append(player)
                return True
            
            else:
                print(f"Game {self.id} : {self.name} already contains player")
                return True
            
        else:
            print(f"Game {self.id} : {self.name} is full")
            return False
    
    def removePlayer(self, player):
        if self.getAvalableSlots() == self.MAX_PLAYERS:
             print(f"Game {self.id} : {self.name} is empty")
             return True
            
        elif player in self.players:
            self.players.remove(player)
            return True
            
        else:
            print(f"Game {self.id} : {self.name}  does not contain player {player}")
            return False
    
    
    def __str__(self):
        return f"Game {self.id} : {self.name} has {self.getAvalableSlots()} slots available" 

