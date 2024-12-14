
import numpy as np

import os
import sys
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))

import Buffer.Game_pb2 as pb2
from Entity.Player import Player

class Game:
    count = 0
    
    def pbToObject(pb):
        if not pb: return None
        players = []
        for player in pb.players:
            players.append(Player.pbToObject(player))
        
        return Game(pb.id, players, pb.rounds, pb.teans, pb.settings, pb.playersInput)
    
    def objectToPb(obj):
        players = []
        for player in obj.players:
            players.append(Player.objectToPb(player))
            
        teams = []
        for team in obj.teams:
            teams.append(pb2.Team(player1=team[0], player2=team[1]))
        
        settings = pb2.Setting(duration=obj.settings[0], packs=obj.settings[1])
          
        return pb2.Game(
            id= obj.id,
            players=players,
            rounds=obj.rounds,
            teams=teams,
            settings=settings,
            playersInput=obj.playersInput,
        )
    
    def __init__(self, id=0, players=None, teams=None, currentWord=None, rounds=0, roundTimer=None, settings=None, playersInput=None):
        if not id > 0: 
            Game.count += 1
            self.id = Game.count
        else:
            self.id = id
        self.MAX_PLAYERS = 4
        self.players = [] if players is None else players
        self.teams = {} if teams is None else teams
        self.rounds = rounds
        self.currentWord = currentWord
        self.roundTimer = roundTimer
        self.settings = () if settings is None else settings
        self.playersInput = [] if playersInput is None else playersInput
       
 
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
     
    @staticmethod
    def canStart(game):
        if game.getAvalableSlots() == game.MAX_PLAYERS:
            print(f"Game {game.id} : {game.name} is empty")
            return False
        
        elif self.getAvalableSlots() > 0:
            print(f"Game {game.id} : {game.name} is not full")
            return False
        
        else:
            print(f"Game {game.id} : {game.name} started")
            return True
        
    
        