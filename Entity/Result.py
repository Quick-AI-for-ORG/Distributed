import os
import sys
sys.path.append(os.path.dirname("Buffer"))
import Buffer.Result_pb2 as pb2

class Result:
    
    def pbToObject(pb):
        if not pb: return None
        return Result(pb.isSuccess, pb.message)
    
    def objectToPb(obj):
        return pb2.Result(
            isSuccess=obj.isSuccess,
            message=obj.message,
        )
        
    def __init__(self, isSuccess, message):
        self.isSuccess = isSuccess
        self.message = message
        
    def __str__(self):
        return f"{'Success' if self.isSuccess else 'Failure'} : {self.message}"
    
    def __dict__(self):
        return {"isSuccess": self.isSuccess, "message": self.message}