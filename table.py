class STable(object):
    def __init__(self):
        self.table = dict()

    def __str__(self):
        ret = 'Tabela de Subscription:\n'
        ret += 'Item\tSubs\tProx\tSaltos\n'
        for entry in self.table:
            ret += ('{}\t{}\t{}\t{}\n'.format(
                entry[0], entry[1], self.table[entry][0], self.table[entry][1]
            ))
        return ret

    def update_table(self, item_name, subscriber, next_node, hops):
        if ((item_name, subscriber) not in self.table or
                self.table[(item_name, subscriber)][1] > hops):
            self.table[(item_name, subscriber)] = (next_node, hops)
