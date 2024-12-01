import os
import sys
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Entity"))

import Service.Game_pb2 as gamePB2
import Service.Player_pb2 as playerPB2

from Entity.Game import Game
from Entity.Player import Player

playerpb = playerPB2.Player(id=1,name="Adam",health=3,score=100)
player = Player.pbToObject(playerpb)
pbPlayer = Player.objectToPb(player)


game = gamePB2.create(1,"OutBusrt 20143535",4,[pbPlayer])
game2  = Game.pbToObject(game)
print(game2.players[0])

gameP = Game.objectToPb(game2)
print(gameP.players[0])