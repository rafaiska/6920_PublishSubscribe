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
           self.adj.append((entry, (conexoes['hosts'][entry])))
        hostname, port = parse_host(conexoes['hosts'][self.name])
        self.comm = PSComm(hostname, port)
        self.comm_thread = threading.Thread(target=self.comm.start)
        self.comm_thread.setDaemon(True)
        self.comm_thread.start()


    def __str__(self):
        ret = 'Node {}, host {}:{}\nAdjacencias:\n'.format(self.name, self.comm.hostname, self.comm.port)
        for adj in self.adj:
            hostname, port = parse_host(adj[1])
            ret += '\tNode {} em {}:{}\n'.format(adj[0], hostname, port)
        return ret

    def read_conexoes(self):
        conexoes = json.load(open('conexoes.json', 'r'))
        if self.name not in conexoes['conexoes'] or self.name not in conexoes['hosts']:
            raise RuntimeError('O nome de no "{}" nao esta em conexoes.json'.format(self.name))
        return conexoes