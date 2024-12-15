
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
        teams = {'A': [], 'B': []}
        teams['A'] = pb.teams[0] if pb.teams[0] else [0,0]
        teams['B'] = pb.teams[1] if pb.teams[1] else [0,0]
        return Game(pb.id, players=players, round=pb.rounds, teams=teams, settings=pb.settings, playersInput=pb.playersInput)
    
    def objectToPb(obj):
        players = []
        for player in obj.players:
            players.append(Player.objectToPb(player))
            
        teams = []
        for team in ['A', 'B']:
            teams.append(pb2.Team(player1=obj.teams[team][0], player2=obj.teams[team][1]))

        settings = pb2.Setting(duration=obj.settings[0], packs=obj.settings[1])
          
        return pb2.Game(
            id= obj.id,
            players=players,
            rounds=obj.round,
            teams=teams,
            settings=settings,
            playersInput=obj.playersInput,
        )
    
    def __init__(self, id=0, players=None, teams=None, currentWord=None, round=1, roundTimer=None, settings=None, playersInput=None):
        if not id > 0: 
            Game.count += 1
            self.id = Game.count
        else:
            self.id = id
        self.MAX_PLAYERS = 4
        self.players = [] if players is None else players
        self.teams = {
            'A': [0,0],
            'B': [0,0],
            } if teams is None else teams
        self.round = round
        self.currentWord = currentWord
        self.roundTimer = roundTimer
        self.settings = ('long', ['commands', 'countries', 'games', 'movies', 'songs']) if settings is None else settings
        self.playersInput = [] if playersInput is None else playersInput
        self.name = "OutBurst"
       
 
    def getAvalableSlots(self):
        return self.MAX_PLAYERS - len(self.players)
        
    def addPlayer(self, player):
        if self.getAvalableSlots() > 0:
            if player not in self.players:
                self.players.append(player)
                return True
            
            else:
                print(f"Game {self.id} : already contains player")
                return True
            
        else:
            print(f"Game {self.id} : is full")
            return False
    
    def removePlayer(self, player):
        if self.getAvalableSlots() == self.MAX_PLAYERS:
             print(f"Game {self.id} : is empty")
             return True
            
        elif player in self.players:
            self.players.remove(player)
            return True
            
        else:
            print(f"Game {self.id} :  does not contain player {player}")
            return False
    
    
    def __str__(self):
        return f"Game {self.id} : {self.getAvalableSlots()} slots available"
     
    # @staticmethod
    # def canStart(game):
    #     if game.getAvalableSlots() == game.MAX_PLAYERS:
    #         print(f"Game {game.id} : is empty")
    #         return False
        
    #     elif self.getAvalableSlots() > 0:
    #         print(f"Game {game.id} : is not full")
    #         return False
        
    #     else:
    #         print(f"Game {game.id} : started")
    #         return True
        
    
        