import os
import sys
sys.path.append(os.path.dirname("Buffer"))
import Buffer.Player_pb2 as pb2

class Player:
    count = 0
    
    def pbToObject(pb):
        if not pb: return None
        return Player(pb.id, pb.name, pb.health, pb.score)
    
    def objectToPb(obj):
        return pb2.Player(
            id= obj.id,
            name=obj.name,
            health=obj.health,
            score=obj.score,
        )
    
    def __init__(self, id=0, name="Player", health=3, score=0):
        if not id > 0: 
            Player.count += 1
            self.id = Player.count
        else:
            self.id = id
        self.name = name
        self.health = health
        self.score = score

    def __str__(self):
        return f"Player {self.id} : {self.name} with {self.health} health and {self.score} score"
