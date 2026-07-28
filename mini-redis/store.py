# Brain of the mini database
import json
from pathlib import Path
import time

class MiniRedisStore:
    def __init__(self, filename="data.json"):
        self.filename= Path(filename)
        self.store=self.load()
        self.expirations = {}
  
    def load(self):
        if self.filename.exists():
            with open(self.filename, "r") as file:
                return json.load(file)
        return  {} 

    def save(self):
        with open(self.filename, "w")as file:
            json.dump(self.store,file)

    def set(self, key, value):
        self.store[key]=value
        self.save()
        return "OK"
    
    def get(self, key):
        if self._is_expired(key):
            return "(nil)"

        return self.store.get(key, "(nil)")
    
    def delete(self,key):
        if key in self.store:
            del self.store[key]
            self.save()
            return "OK"
        return "(nil)"
    
    def exists(self, key):
        return "1" if key in self.store else "0"
    
    def _is_expired(self, key):
        if key not in self.expirations:
            return False

        if time.time() >= self.expirations[key]:
            self.store.pop(key, None)
            self.expirations.pop(key, None)
            self.save()
            return True

        return False


    def expire(self, key, seconds):
        if key not in self.store:
            return 0

        self.expirations[key] = time.time() + seconds
        return 1


    def ttl(self, key):
        if key not in self.store:
            return -2

        if self._is_expired(key):
            return -2

        if key not in self.expirations:
            return -1

        return int(self.expirations[key] - time.time())
        
        
