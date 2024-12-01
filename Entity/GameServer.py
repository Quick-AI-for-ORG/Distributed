import random
from Resource import Resource
from Server import Server

import os
import sys
sys.path.append(os.path.dirname("Service"))
import Service.GameServer_pb2 as pb2

class GameServer(Server):
    
    def pbToObject(pb):
        if not pb: return None
        resource = pb2.Resource.pbToObject(pb.resource)
        return GameServer(pb.ip, pb.port, pb.resourceLimit, resource)
    
    def objectToPb(obj):
        return pb2.GameServer(
            ip= obj.ip,
            port=obj.port,
            resourceLimit=obj.resourceLimit,
            resource=Resource.objectToPb(obj.resource),
        )
    
    def __init__(self, ip="localhost", port=None, resourceLimit=4, resource=None):
        super().__init__(ip, port)
        self.resource = Resource(resourceLimit) if resource is None else resource
        
    def __str__(self):
        return f"Game Server running at {self.IP}:{self.port} with {self.resource}"
