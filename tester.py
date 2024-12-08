import os
import sys
import asyncio
sys.path.append(os.path.dirname("Entity"))

from Entity.Master import Master
from Entity.GameServer import GameServer

        
m = Master()


server = GameServer()
async def main():
    await asyncio.gather(m.runServicer(), server.listen())
    
asyncio.run(main())