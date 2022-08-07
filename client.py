from threading import Thread
import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9999,))


class ReplyHandler(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            reply = sock.recv(1024)
            print(reply.decode("utf-8"))


thread = ReplyHandler()
thread.daemon = True
thread.start()

while True:
    message = input('You: ')
    if message == 'exit':
        sock.sendall(bytes('leave the chat', 'utf-8'))
        sleep(2)
        sock.close()
    # print(f'You: {message}')
    sock.sendall(bytes(message, 'utf-8'))
