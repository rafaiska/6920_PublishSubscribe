import json
import threading
from comm import PSComm


def parse_host(host_string):
    host_string = host_string.split(':')
    hostname = host_string[0]
    port = host_string[1]
    return hostname, int(port)


class Node(object):
    def __init__(self, name):
        self.name = name
        conexoes = self.read_conexoes()
        self.adj = []
        for entry in conexoes['conexoes'][self.name]:
            hostname, port = parse_host(conexoes['hosts'][entry])
            self.adj.append((entry, hostname, port))
        hostname, port = parse_host(conexoes['hosts'][self.name])
        self.comm = PSComm(self.name, hostname, port, self.adj)
        self.comm_thread = threading.Thread(target=self.comm.start)
        self.comm_thread.setDaemon(True)
        self.comm_thread.start()

    def __str__(self):
        ret = 'Node {}, host {}:{}\nAdjacencias:\n'.format(self.name, self.comm.hostname, self.comm.port)
        for adj in self.adj:
            nodename, hostname, port = adj
            ret += '\tNode {} em {}:{}\n'.format(nodename, hostname, port)
        ret += str(self.comm.subs_table.table)
        return ret

    def print_publications(self):
        for publication in self.comm.fetched_publications:
            print('Codigo da inscricao: {}'.format(publication[0]))
            print('Conteudo: {}'.format(publication[1]))
            print('Timestamp: {}\n'.format(publication[2]))

    def subscribe(self, item_name):
        self.comm.subs_table.update_table(item_name, self.name, self.name, 0)
        self.comm.transmit_subscription(None,
                                        {'item': item_name,
                                         'subscriber': self.name,
                                         'next_node': self.name,
                                         'hops': 0})

    def publish(self, item_name, content):
        self.comm.transmit_publications(None, item_name, content, map(lambda x: x[0], self.adj))

    def read_conexoes(self):
        conexoes = json.load(open('conexoes.json', 'r'))
        if self.name not in conexoes['conexoes'] or self.name not in conexoes['hosts']:
            raise RuntimeError('O nome de no "{}" nao esta em conexoes.json'.format(self.name))
        return conexoes
