import socket
import json
import argparse

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
        # TODO use json to encode the data
        self.socket.sendall(msg)
        data = self.socket.recv(1024)
        return data

    # TODO delete method
    def exp_middleware(self):
        data = self.send_msg(b'ola server')

        print(f'Received from server: {data}')
        self.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="symbolic name for the host", default='')
    parser.add_argument("--port", help="port used for communication", default=8000)
    args = parser.parse_args()

    obu = ObuMiddleware(args.host, args.port)

    obu.exp_middleware()