import numpy as np

class Resource:
    def __init__(self, session=4):
        self.MAX_SESSIONS = session
        self.sessions = []
        
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
    
    def removePlayer(self, session):
        if self.getAvalableSessions() == self.MAX_PLAYERS:
             return True
            
        elif session in self.sessions:
            self.sessions.remove(session)
            return True
            
        else:
            return False          
    
    
    def __str__(self):
        return f"{self.getAvalableSessions()} sessions available" 

    
        