import os
import sys
import asyncio
import tracemalloc
tracemalloc.start()
sys.path.append(os.path.dirname("Entity"))

from Entity.Master import Master
from Entity.GameServer import GameServer

        
m = Master()


server1 = GameServer()
# server2 = GameServer()
# server2.listen()
async def main():
    await asyncio.gather(m.runServicer(), server1.listen(), m.checkHealth())
    
asyncio.run(main())