import socket
import select
import queue
import threading
import time
import random
import sys
   

class Server:
    def __init__(self, port):
        print('init')
        self.port = port
        self.host = socket.gethostname()
        self.running = False
        self.connectionsMade = 0
        self.messagesReceived = 0

    def start(self):
        print('start')
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.processThread = threading.Thread(target=self.run)
        self.processThread.start()

    def run(self):
        while self.running:
            try:
                clientSocket, addr = self.socket.accept()
                self.connectionsMade += 1
                msg = clientSocket.recv(2014)
                self.lastMessage = msg.decode('UTF-8')
                self.messagesReceived += 1
                print(self.lastMessage)
                #ready = select.select([client,],[], [],2)
                #if ready[0]:
                #data = client.recv(4096)
                #print data
                #t.add(data)
            except Exception as msg:
                print("Socket error! %s" % msg)
                break

    def stop(self):
        print('stop')
        self.running = False
        try:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
        except:
            pass
        self.socket.close()
        self.processThread.join()




def rrun(self):
        q = self.q
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                process(value)
            except queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()
        #
        print('Exiting thread')
        if not q.empty():
            print("Elements left in the queue:")
            while not q.empty():
                print(q.get())
