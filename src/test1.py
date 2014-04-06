import unittest
import piServer.piServer as piServer
import piClient.piClient as piClient

import time
import socket

class Test_Server(unittest.TestCase):
    def test_create(self):
        server = piServer.Server(3031)
        server.start()
        server.stop()

    def test_simple_connect(self):
        server = piServer.Server(3032)
        server.start()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server.host, server.port))
        time.sleep(1)
        self.assertTrue(server.connectionsMade >= 1)
        server.stop()


class Test_Client(unittest.TestCase):
     def test_client_without_server(self):
        client = piClient.Client()
        self.assertFalse(client.connect('127.0.0.1', 3040))
        client.close()

class Test_Integration(unittest.TestCase):
    def test_send_one(self):
        server = piServer.Server(3060)
        server.start()      
        client = piClient.Client()
        client.connect('127.0.0.1', 3060)
        client.send('1')
        time.sleep(1)
        self.assertTrue(server.connectionsMade >= 1)
        self.assertTrue(server.messagesReceived >= 1)
        client.close()
        server.stop()


if __name__ == '__main__':
    unittest.main()
