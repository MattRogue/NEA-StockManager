import threading
from datetime import datetime, timedelta
from time import sleep

class Client:
    active_users = {}

    def __init__(self, ip, username):
        self.username = username
        self.ip = ip
        self.timeout = datetime.now()+timedelta(seconds=10) #change this to minutes after
        self.terminated = False
        self.timeout_thread = threading.Thread(target=self.timed_out)
        self.active_users[self.ip] = self
        print(self, "has logged in")
        self.timeout_thread.start()
        print("Active clients:", self.active_users)
    
    def __str__(self):
        return f"{self.ip} ({self.username})"
    
    def timed_out(self): #Highly recommend creating timeout on client side.
        while not (datetime.now() >= self.timeout):
            sleep(1)
        if not self.terminated:
            try:
                user = self.active_users.pop(self.ip)
            except KeyError: #value already does not exist
                pass
            self.terminated = True
            print(str(self), "timed out due to inactivity")
            print("Active clients:", self.active_users)
    
    def logout(self):
        try:
            self.terminated = True
            self.active_users.pop(self.ip)
        except KeyError:
            pass
        print(str(self), "logged out manually")
        print("Active clients:", self.active_users)
    