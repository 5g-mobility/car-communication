import traci
import traci.constants as tc
import selectors
import socket



sel = selectors.DefaultSelector()



class Server:
    def __init__(self, port=8000):
        self.port = port
        self.client_vehicles = {}
        self.vehicles_id = []

def accept(self, sock, mask):
    """ aceita novas ligações
        Parametros:
        sock: socket do broker que recebe as ligações
        mask: mascara
    """
    conn, addr = sock.accept()
    print('accepted', conn, 'from', addr)

    conn.setblocking(False) # impedir que bloqueie
    sel.register(conn, selectors.EVENT_READ,read) # registar a socket no selector



def closeSocket(self, conn):
    """ fecha a ligação e remove os dados associados
        Parametros:
        conn: socket do broker associada a uma determinada entidade
    """
    print('closing', conn) 

    sel.unregister(conn)
    conn.close()



def read(self, conn, mask):

    if conn not in self.client_vehicles:

        if len(self.vehicles_id) == 0 :

            self.closeSocket(conn)

        else:

            vehicle = self.vehicle_id.pop()




    # if tamanhoMsg == conn.recv(5):
    #     pass



def start(self):
    pass
    # traci.start(["sumo", "-c", "osm.sumocfg"], port=self.port)
    # self.vehicles_id =  traci.vehicle.getIDList()

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.bind((HOST, PORT)) # associa o endereço e a porta ao socket
    #     s.listen(100) # cria 1 fila de espera apenas para 1 ligação, enquanto um socket estiver a correr a outra fica na lista as outras são rejeitadas
    #     s.setblocking(False)
    #     sel.register(s,selectors.EVENT_READ,accept)

    #     while True: 
    #         events = sel.select()
    #         for key, mask in events:
    #             callback = key.data
    #             callback(key.fileobj, mask)


if __name__ == "__main__":
    pass

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--port", help="port used for communication", default=8000)
    # args = parser.parse_args()

    # server = Server(args.port)

    # server.start()