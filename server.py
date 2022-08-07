from threading import Thread
import socket

sock, peers = None, []
clients = []

class IMS(object):
    MAX_CONNECTIONS = 5

    def __init__(self):
        self.setup()
        for i in range(IMS.MAX_CONNECTIONS):
            thread = IMS.Connection()
            thread.daemon = True
            thread.start()

    def setup(self):
        global sock
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 9999,))
        sock.listen(10)

    def send_message(self, message):
        for i, peer in enumerate(peers):
            peer.sendall(bytes(f'{clients[i]}: {message}', 'utf-8'))

    class Connection(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            peer, addr = sock.accept()
            clients.append(addr)
            peers.append(peer)
            print(f"{addr} was connected")

            for other in peers:
                other.sendall(bytes(f"{addr} was connected", 'utf-8'))

            while True:
                message = peer.recv(1024)
                if message:
                    print(f'{addr}: {message}')
                for other in peers:
                    if other != peer:
                        other.sendall(bytes(f'{addr}: {message}', 'utf-8'))


ims = IMS()
try:
    while True:
        message = input('')
        ims.send_message(bytes(message, 'utf-8'))
except KeyboardInterrupt:
    sock.close()
    for peer in peers:
        peer.close()

