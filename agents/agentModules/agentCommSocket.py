import socket


class commSocket:
    """class for using one socket for all master communication"""

    # TODO this may not be necessary test without it if it is add socket close to gracefull exit
    _instance = None

    def __new__(self):  # singleton
        if self._instance is None:
            self._instance = super(commSocket, self).__new__(self)
        return self._instance

    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # maybe more benefitial for it to be udp ##FOOD_FOR_THOUGHT maybe bind more than one at a time on master side

    def getTcpSocket(self):
        return self.socket

    def __del__(self):
        self.socket.close()
