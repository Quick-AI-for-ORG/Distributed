
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

        return Game(pb.id, players=players, round=pb.rounds, settings=pb.settings, playersInput=pb.playersInput, words=pb.words.words, clueGiver=pb.clueGiver)
    
    def objectToPb(obj):
        players = []
        for player in obj.players:
            players.append(Player.objectToPb(player))

        settings = pb2.Setting(duration=obj.settings[0], packs=obj.settings[1])
        return pb2.Game(
            id= obj.id,
            players=players,
            rounds=obj.round,
            settings=settings,
            playersInput=obj.playersInput,
            words=pb2.Word(words=obj.words),
            clueGiver=obj.clueGiver
        )
    
    def __init__(self, id=0, players=None, teams=None, currentWord=None, round=1, settings=None, playersInput=None, words=[], clueGiver=None):
        if not id > 0: 
            Game.count += 1
            self.id = Game.count
        else:
            self.id = id
        self.MAX_PLAYERS = 4
        self.players = [] if players is None else players
        self.round = round
        self.currentWord = currentWord
        self.settings = ('long', ['commands', 'countries', 'games', 'movies', 'songs']) if settings is None else settings
        self.playersInput = [] if playersInput is None else playersInput
        self.name = "OutBurst"
        self.words = words
        self.clueGiver = clueGiver
       
 
    def getAvalableSlots(self):
        return self.MAX_PLAYERS - len(self.players)
    
    def loadWordPacks(self, words):
        self.words = words
        
    def addInput(self,string):
        self.playersInput.append(string)
        return self.playersInput
    
    def clearInput(self):
        self.playersInput = []
        return self.playersInput
        
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
     
        