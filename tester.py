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

        
m = Master(ip='192.168.1.44')

server1 = GameServer(ip='192.168.1.44',master='192.168.1.44:7777')
game = Game(words=['Dodo', 'Misho', 'Adoumy', 'Khaloudy', 'Mony'])

dodo = Player(name="Dodo", key="1")
mony = Player(name="Mony", key="2")
khaloudy = Player(name="Khaloudy", key="3")
game.addPlayer(dodo)
game.addPlayer(mony)
game.addPlayer(khaloudy)
server1.resource.sessions.append(game)


# server2 = GameServer()
# server2.listen()
async def main():
    await asyncio.gather(m.runServicer(), server1.listen())
    
asyncio.run(main())