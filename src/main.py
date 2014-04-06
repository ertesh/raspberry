import piServer.piServer as piServer
import piClient.piClient as piClient
import time
import socket


if __name__ == '__main__':
    server = piServer.Server(3053)
    server.start()      
    client = piClient.Client()
    client.connect('127.0.0.1', server.port)
    time.sleep(1)
    client.send('123')
    time.sleep(3)
    client.close()
    server.stop()