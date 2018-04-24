class STable(object):
    def __init__(self):
        self.table = dict()

    def __str__(self):
        ret = 'Tabela de Subscription:\n'
        ret += '\tItem\tSubs\tProx\tSaltos\n'
        for entry in self.table:
            ret += ('\t{}\t{}\t{}\t{}\n'.format(
                entry[0], entry[1], self.table[entry][0], self.table[entry][1]
            ))
        return ret

    def update_table(self, item_name, subscriber, next_node, hops):
        if ((item_name, subscriber) not in self.table or
                self.table[(item_name, subscriber)][1] > hops):
            self.table[(item_name, subscriber)] = (next_node, hops)
            return True
        else:
            return False

    def get_interested_adj(self, item_name):
        next_nodes = []
        for entry in self.table:
            if entry[0] == item_name:
                next_nodes.append(self.table[entry][0])
        return next_nodes
