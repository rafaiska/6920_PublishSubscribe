import gevent
from gevent.server import StreamServer
from gevent.event import Event
from gevent import socket

class PSComm(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.server_greenlet = None
        self.new_req = Event()

    def req_handler(self, sock, clientaddress):
        print('{}, {}'.format(sock, type(sock)))
        print('{}, {}'.format(clientaddress, type(clientaddress)))
        print(sock.recv(1024))

    def start_server(self):
        print('Ouvindo requisicoes em {}:{}'.format(self.hostname, self.port))
        server = StreamServer((self.hostname, self.port), self.req_handler)
        server.serve_forever()

    def receive_req(self):
        pass

    def send_req(self, hostname, port, msg):
        sock = socket.create_connection((hostname, port), 1)
        try:
            sock.send(msg)
        finally:
            sock.close()

    def start(self):
        self.server_greenlet = gevent.spawn(self.start_server)
        while True:
            gevent.sleep(0)