import selectors
import socket
import argparse
import json
import logging

class RSU:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.socket = None
        self.client_sockets = []

        self.header = 4         # length of the expected header 

        self.create_logger()
        self.logger.info('RSU object initialized.')

    def create_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def accept(self, sock, mask):
        """ aceita novas ligações
            Parametros:
            sock: socket do broker que recebe as ligações
            mask: mascara
        """
        conn, addr = sock.accept()
        self.logger.info(f'accepted {conn} from {addr}')

        conn.setblocking(False) # impedir que bloqueie
        self.selector.register(conn, selectors.EVENT_READ, self.read) # registar a socket no selector
        self.client_sockets.append(conn)

    def close_socket(self, conn):
        """ fecha a ligação e remove os dados associados
            Parametros:
            conn: socket do broker associada a uma determinada entidade
        """
        self.logger.info(f'closing {conn}') 

        self.selector.unregister(conn)
        self.client_sockets.remove(conn)
        conn.close()

    def read(self, conn, mask):
        data = self.receive_message(conn, mask)  # Should be ready
        if data:
            data = json.loads(data.decode('utf-8'))
            self.logger.debug(f'Message received: {data} from {conn}')
            
            # TODO agr era necessário enviar a informação recebida para o broker no IT

    def receive_message(self, conn, mask):        
        # receive 4 bytes indicating the length of the message
        payload_length = conn.recv(self.header)

        if not payload_length:
            self.close_connection(conn)
            return None

        # receive the expected message
        payload = conn.recv(int.from_bytes(payload_length, byteorder='big'))

        if not payload:
            self.close_connection(conn)
            return None

        # return payload
        return payload

    def close_connection(self, conn):
        self.logger.error(f'Connection losted with {conn}')
        self.selector.unregister(conn)
        conn.close()

    def start(self):
        try:
            rsu.start_server()
        except Exception:
            self.logger.info('Closing server...')
            rsu.close()

    def start_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port)) # associa o endereço e a porta ao socket
        self.socket.listen(100) # cria 1 fila de espera apenas para 1 ligação, enquanto um socket estiver a correr a outra fica na lista as outras são rejeitadas
        self.socket.setblocking(False)
        self.selector.register(self.socket, selectors.EVENT_READ, self.accept)

        self.logger.info(f'RSU server listening on port {self.port}...')

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