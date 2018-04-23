import gevent
import json
from gevent.server import StreamServer
from gevent.event import Event
from gevent import socket
from table import STable

class PSComm(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.server_greenlet = None
        self.subs_table = STable()
        self.new_req = Event()

    def req_handler(self, sock, clientaddress):
        msg = sock.recv(1024)
        try:
            msg = json.loads(msg)
        except ValueError:
            msg = {}

        if 'subscription' in msg:
            subs = msg['subscription']
            self.subs_table.update_table(
                subs['item'], subs['subscriber'], subs['next_node'],
                subs['hops'])

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