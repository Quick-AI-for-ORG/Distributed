import os
import sys
import asyncio
import tracemalloc
tracemalloc.start()
sys.path.append(os.path.dirname("Entity"))

from Entity.Master import Master
from Entity.GameServer import GameServer
from Entity.Game import Game
from Entity.Player import Player

        
m = Master()

server1 = GameServer()
game = Game()
      
dodo = Player(name="Dodo")
mony = Player(name="Mony")
khaloudy = Player(name="Khaloudy")
game.addPlayer(dodo)
game.addPlayer(mony)
game.addPlayer(khaloudy)

print(game)
server1.resource.sessions.append(game)


# server2 = GameServer()
# server2.listen()
async def main():
    await asyncio.gather(m.runServicer(), server1.listen())
    
asyncio.run(main())