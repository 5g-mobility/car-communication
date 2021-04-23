import selectors
import socket

class RSU:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()

def accept(self, sock, mask):
    """ aceita novas ligações
        Parametros:
        sock: socket do broker que recebe as ligações
        mask: mascara
    """
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)

    conn.setblocking(False) # impedir que bloqueie
    self.selector.register(conn, selectors.EVENT_READ, self.read) # registar a socket no selector

def closeSocket(self, conn):
    """ fecha a ligação e remove os dados associados
        Parametros:
        conn: socket do broker associada a uma determinada entidade
    """
    print('closing', conn) 

    self.selector.unregister(conn)
    conn.close()

def read(self, conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(f"Message received: [{data}]")  # Hope it won't block
    else:
        print('closing', conn)
        self.selector.unregister(conn)
        conn.close()

def start(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((self.host, self.port)) # associa o endereço e a porta ao socket
        s.listen(100) # cria 1 fila de espera apenas para 1 ligação, enquanto um socket estiver a correr a outra fica na lista as outras são rejeitadas
        s.setblocking(False)
        self.selector.register(s, selectors.EVENT_READ, self.accept)

        while True: 
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="port used for communication", default=8000)
    args = parser.parse_args()

    server = Server(port=args.port)
    server.start()