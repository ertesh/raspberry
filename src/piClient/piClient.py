import socket

from piCommon.Types import ConnectionError

class Client:
    """description of class"""
    def __init__(self):
        pass

    def connect(self, host, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
        except Exception as msg:
            print(msg)
            return False
        else:
            return True

    def send(self, s):
        self.socket.send(bytes(s, 'UTF-8'))

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except Exception as msg:
            print(msg)