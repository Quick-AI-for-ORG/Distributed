
import numpy as np

import os
import sys
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))

import Buffer.Game_pb2 as pb2
from Entity.Player import Player


def normalize_string(s):
    return ' '.join(s.lower().split())


class Game:
    count = 0
    
    def pbToObject(pb):
        if not pb: return None
        players = []
        for player in pb.players:
            players.append(Player.pbToObject(player))

        return Game(pb.id, players=players, round=pb.rounds, settings=pb.settings, playersInput=pb.playersInput, words=pb.words.words, clueGiver=Player.pbToObject(pb.clueGiver) if pb.clueGiver else None)
    
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
            clueGiver=Player.objectToPb(obj.clueGiver) if obj.clueGiver else None
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
        self.words = words
        self.clueGiver = clueGiver
       
    def getClueGiver(self):
        self.clueGiver = self.players[self.round % len(self.players)]
        return self.clueGiver
    
    def getRole(self, player):
        if player.name == self.getClueGiver().name: return 'Clue Giver'
        else: return 'Guesser'
    
    def validateGuess(self, guess):
        if normalize_string(guess) == normalize_string(self.getWord()):
            return True
        else:
            return False
        
    def validateClue(self, clue):
        if normalize_string(clue) == normalize_string(self.getWord()):
            return False
        else:
            return True
        
    def getWinner(self):
        maxPlayer = self.players[0]
        for player in self.players:
            if  player.score >= maxPlayer.score:
                maxPlayer = player
        return maxPlayer    
    def getWord(self):
        return self.words[self.round-1]
    def nextRound(self):
        self.clearInput()
        if self.round == len(self.words):
            self.round = 0
        else:
            self.round += 1
            self.playersInput = []
            for i in range(len(self.players)):
               self.players[i].resetHealth()
               
        return self.round
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
            for temp in self.players:
                if player.key == temp.key:
                    print(f"Game {self.id} : already contains player")
                    return True
                
            self.players.append(player)
            return True  
            
        else:
            print(f"Game {self.id} : is full")
            return False
    
    def getPlayer(self, temp):
        for player in self.players:
            if player.key == temp.key: return player
        return None
    def removePlayer(self, player):
        if self.getAvalableSlots() == self.MAX_PLAYERS:
             print(f"Game {self.id} : is empty")
             return True
            
        else:
            for temp in self.players:
                if temp.key == player.key:
                    self.players.remove(temp)
                    return True
                else:
                    print(f"Game {self.id} :  does not contain player {player}")
                    return False
        
    def getPreviousWord(self):
        if self.round < 2: return self.getWord()
        return self.words[self.round - 2]
    def updatePlayer(self, player):
        for temp in self.players:
            if player.key == temp.key:
                self.players.remove(temp)
                self.players.append(player)
                return True
            else:
                print(f"Game {self.id} :  does not contain player {player}")
                return False
    def __str__(self):
        return f"Game {self.id} : {self.getAvalableSlots()} slots available"
     
        