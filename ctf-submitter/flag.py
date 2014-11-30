from datetime import datetime

class Flag(object):
    
    def __init__(flag, service, team=0, user="", time=datetime.now()):
        self.flag = flag
        self.service = service
        self.team = team
        self.user = user
        self.time = time
        
    @staticmethod
    def fromDict(values):
        return Flag(values["flag"], values["service"], values["team"], values["user"], values["time"])
