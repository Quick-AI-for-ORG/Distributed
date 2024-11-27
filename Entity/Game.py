
import numpy as np

class Game:
    count = 0
    def __init__(self, name, maxPlayers=4):
        Game.count += 1
        self.id = Game.count
        self.name = name
        self.MAX_PLAYERS = maxPlayers
        self.players = []
       
 
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

