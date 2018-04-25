import gevent
import json
import datetime
from gevent.server import StreamServer
from gevent.event import Event
from gevent import socket
from table import STable

class PSComm(object):
    def __init__(self,nodename, hostname, port, adj):
        self.nodename = nodename
        self.hostname = hostname
        self.port = port
        self.adj = adj
        self.server_greenlet = None
        self.subs_table = STable()
        self.table_available = Event()
        self.table_available.set()
        self.fetched_publications = []

    def req_handler(self, sock, clientaddress):
        msg = sock.recv(1024)
        try:
            msg = json.loads(msg)
        except ValueError as e:
            print('ERRO: MENSAGEM INVALIDA: {}'.format(e.message))
            print('Recebido: {}'.format(msg))
            msg = {}
        sock.close()

        if 'from' not in msg:
            print('ERRO: MENSAGEM SEM IDENTIFICACAO')
            return

        sender = msg['from']

        if 'subscription' in msg:
            subs = msg['subscription']
            self.table_available.wait()
            self.table_available.clear()
            updated = self.subs_table.update_table(
                subs['item'], subs['subscriber'], subs['next_node'],
                subs['hops'])
            self.table_available.set()
            if updated:
                self.transmit_subscription(sender, subs)

        if 'publish' in msg:
            item_name = msg['publish']['item_name']
            content = msg['publish']['content']
            next_hops = self.subs_table.get_interested_adj(item_name)
            if self.nodename in next_hops:
                self.fetched_publications.append((item_name, content, str(datetime.datetime.now())))
            else:
                self.transmit_publications(sender, item_name, content, next_hops)

    def start_server(self):
        server = StreamServer((self.hostname, self.port), self.req_handler)
        server.serve_forever()

    def receive_req(self):
        pass

    def send_req(self, hostname, port, msg):
        try:
            sock = socket.create_connection((hostname, port))
        except socket.error:
            print('ERRO: conexao recusada para {}:{}'.format(hostname, port))
            return False
        sock.send(msg)

    def transmit_subscription(self, sender, subs):
        subs['hops'] += 1
        subs['next_node'] = self.nodename
        for adj_node in self.adj:
            nodename, hostname, port = adj_node
            if nodename != sender:
                self.send_req(hostname, port, json.dumps({
                    'from': self.nodename,
                    'subscription': subs}))

    def transmit_publications(self, sender, item_name, content, next_hops):
        already_sent = []
        for node_id in next_hops:
            if node_id == sender or node_id in already_sent:
                continue
            for adj in self.adj:
                if node_id == adj[0]:
                    self.send_req(adj[1], adj[2], json.dumps({
                        'from': self.nodename,
                        'publish': {'item_name': item_name, 'content': content}}))
                    already_sent.append(node_id)

    def start(self):
        self.server_greenlet = gevent.spawn(self.start_server)
        while True:
            gevent.sleep(1)
