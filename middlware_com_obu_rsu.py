import socket
import json
import argparse
import sys
import datetime

class ObuMiddleware:
    def __init__(self, host='', port=8000):
        self.host = host
        self.port = port

        self.connect2RSU()

    def connect2RSU(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def close(self):
        self.socket.close()


    def send_msg(self, msg):
        # TODO fazer verificação da msg que está a ser enviada
        try:
            self.socket.sendall(json.dumps(msg).encode('utf-8'))
        except BrokenPipeError:
            sys.exit('The connection was lost.')

    def recv_msg(self):
        # TODO usar um header para indicar tamanho da msg
        return self.socket.recv(1024)

    # TODO delete method
    def exp_middleware(self):
        while True:
            data = {'tm' : str(datetime.datetime.now())}

            msg = str(input('Qual a mensagem? '))

            if msg == 'EXIT':
                break

            data['msg'] = msg

            self.send_msg(data)        
        
        self.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="symbolic name for the host", default='')
    parser.add_argument("--port", help="port used for communication", default=8000)
    args = parser.parse_args()

    obu = ObuMiddleware(args.host, args.port)

    obu.exp_middleware()