import selectors
import socket
import argparse

class RSU:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.socket = None
        self.client_sockets = []

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
        self.client_sockets.append(conn)

    def close_socket(self, conn):
        """ fecha a ligação e remove os dados associados
            Parametros:
            conn: socket do broker associada a uma determinada entidade
        """
        print('closing', conn) 

        self.selector.unregister(conn)
        self.client_sockets.remove(conn)
        conn.close()

    def read(self, conn, mask):
        data = conn.recv(1000)  # Should be ready
        if data:
            print('echoing', repr(data), 'to', conn)
            conn.sendall(f"Message received: [{data}]".encode('utf-8'))  # Hope it won't block
        else:
            print('closing', conn)
            self.selector.unregister(conn)
            conn.close()

    def start(self):
        try:
            rsu.start_server()
        except Exception:
            rsu.close()

    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port)) # associa o endereço e a porta ao socket
        self.socket.listen(100) # cria 1 fila de espera apenas para 1 ligação, enquanto um socket estiver a correr a outra fica na lista as outras são rejeitadas
        self.socket.setblocking(False)
        self.selector.register(self.socket, selectors.EVENT_READ, self.accept)

        print(f'RSU server listening on port {self.port}...')

        while True: 
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    def close(self):
        """ Closing all the client sockets registered on the selector """
        for conn in self.client_sockets:
            self.close_socket(conn)

        self.selector.unregister(self.socket)
        self.socket.close()

        self.selector.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="symbolic name for the host", default='localhost')
    parser.add_argument("--port", help="port used for communication", default=8000)
    args = parser.parse_args()

    rsu = RSU(args.host, args.port)

    rsu.start()