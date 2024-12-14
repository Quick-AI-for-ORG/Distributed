import os
import sys
import asyncio
import tracemalloc
tracemalloc.start()
sys.path.append(os.path.dirname("Entity"))

from Entity.Master import Master
from Entity.GameServer import GameServer

        


server2 = GameServer()
# server2.listen()
async def main():
    await asyncio.gather(server2.listen())
    
asyncio.run(main())