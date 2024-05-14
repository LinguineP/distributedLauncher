import socket


class commSocket:

    def __new__(self): #singleton
        if not hasattr(self, 'instance'):
            self.instance = super(commSocket, self).__new__(self)
        return self.instance

    def __init__(self): #initialization of new instance
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def getTcpSocket(self):
        return self.socket
    

    def __del__(self):
        self.socket.close()