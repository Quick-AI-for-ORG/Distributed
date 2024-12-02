import numpy as np

import os
import sys
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))

import Buffer.Resource_pb2 as pb2
from Entity.Game import Game

class Resource:
    
    def pbToObject(pb):
        if not pb: return None
        sessions = []
        for session in pb.sessions:
            session.append(Game.pbToObject(session))
        
        return Resource(pb.MAX_SESSIONS, sessions)
    
    def objectToPb(obj):
        sessions = []
        for session in obj.sessions:
            sessions.append(Game.objectToPb(session))
            
        return pb2.Resource(
            MAX_SESSIONS=obj.MAX_SESSIONS,
            sessions=sessions,
        )
    
    def __init__(self, maxSession=4, sessions=None):
        self.MAX_SESSIONS = maxSession
        self.sessions = [] if sessions is None else sessions
        
    def getAvalableSessions(self):
        return self.MAX_SESSIONS - len(self.sessions)
        
    def addSession(self, session):
        if self.getAvalableSessions() > 0:
            if session not in self.sessions:
                self.sessions.append(session)
                return True
            
            else:
                return True
            
        else:
            return False
    
    def removeSession(self, session):
        if self.getAvalableSessions() == self.MAX_SESSIONS:
             return True
            
        elif session in self.sessions:
            self.sessions.remove(session)
            return True
            
        else:
            return False          
    
    
    def __str__(self):
        return f"{self.getAvalableSessions()} sessions available" 

    
        