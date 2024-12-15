import os
import sys
import asyncio
import tracemalloc
tracemalloc.start()
sys.path.append(os.path.dirname("Entity"))

from Entity.Master import Master
from Entity.GameServer import GameServer
from Entity.Player import Player
from Entity.Game import Game




    
asyncio.run(server1.listen())