import sys
import getopt

from node import Node

def print_help():
    help_str = ''
    help_str += '======================================\n'
    help_str += 'Sistema distribuido Publicar / Assinar\n'
    help_str += '======================================\n\n'
    help_str += ('Esse programa pode ser utilizado para iniciar um processo de um sistema distribuido, o qual '
                 'implementa o paradigma publicar - assinar. As conexoes entre processos devem ser descritas no arquivo'
                 '"conexoes.json", o qual deve estar no mesmo diretorio deste script.\n\n')
    help_str += ('Processos podem ser inicializados ou com a flag -p (publicadores), ou com a flag -s (assinantes). '
                 'Aqueles que nao utilizarem nenhuma das flags serao inicializados como nos intermediarios do sistema,'
                 'ficando responsaveis somente por repassar as publicacoes. Tambem e necessario passar como argumento'
                 'o nome do processo, o qual deve estar registrado no arquivo "conexoes.json"\n\n')
    help_str += 'Utilizacao basica:\n'
    help_str += '$python main.py [-p] [nome_do_processo]\n'
    help_str += '$python main.py [-s] [nome_do_processo]\n'
    help_str += '$python main.py [--help]'
    print(help_str)

def print_subs_table(table):
    print table


def main():
    def subscribe():
        item_name = raw_input('Para qual item deseja inscrever esse node?\n>')
        node.subscribe(item_name)

    def publish():
        item_name = raw_input('Qual o identificador dessa publicacao?\n>')
        content = raw_input('Qual o conteudo da publicacao?\n>')
        node.publish(item_name, content)

    process_name = 'ALPHA'
    try:
        option_list, args = getopt.getopt(sys.argv[1:], 'ps', 'help')
    except getopt.GetoptError as opterror:
        print('Erro nos parametros: {}'.format(opterror.msg))
        sys.exit(1)

    publisher = False
    subscriber = False
    for opt, arg in option_list:
        if opt == '-p':
            publisher = True
        elif opt == '-s':
            subscriber = True
        elif opt == '--help':
            print_help()
            sys.exit(0)

    if len(args) != 1:
        print('E necessario inicializar "nome_do_processo". Entre com a opcao "--help" para mais informacoes')
        sys.exit(1)
    else:
        process_name = args[0]

    if publisher and subscriber:
        print('O processo pode ser OU assinante OU publicador, nunca ambos. Entre com a opcao "--help" para mais '
              'informacoes')
        sys.exit(2)

    print('Inicializando no do sistema...')
    node = Node(process_name)
    print('Pronto')
    print(node)
    opcoes = {
        '1': lambda: print_subs_table(node.comm.subs_table),
        '2': node.print_publications,
        '3': publish,
        '4': subscribe,
        '5': lambda: sys.exit(0)
    }
    while True:
        print('\nSelecione uma opcao:')
        print('\t1) Verificar tabela de assinaturas (rotas)')
        print('\t2) Mostrar lista de publicacoes recebidas')
        print('\t3) Publicar')
        print('\t4) Assinar')
        print('\t5) Sair')

        opcao = raw_input('>')
        if opcao not in opcoes:
            print('OPCAO INCORRETA! Tente novamente.')
        else:
            opcoes[opcao]()

if __name__ == '__main__':
    main()