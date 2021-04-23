import socket
import json
import argparse
import sys
import datetime

from obd2_sumo_integration import OBD2

class OBU:
    def __init__(self, host='', port=8000):
        self.host = host
        self.port = port

        # the OBU as direct communication with the obd2 emulator
        # the OBU pulls info from obd2
        self.obd2 = None

        self.connect2RSU()

    def connect2RSU(self):
        """ Connect OBU to RSU (via socket)"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def close(self):
        """ Close communication with RSU """
        self.socket.close()

    def connect2OBD2(self, position, speed, co2Emissions):
        """ Initialize the OBD2 object """
        self.obd2 = OBD2(position, speed, co2Emissions)

    def forward_info_2_RSU(self):
        """ Forward the car data to the RSU """
        # TODO fazer verificação dos campos
        self.send_msg({
            'tm' : str(datetime.datetime.now()),
            'position' : self.obd2.get_position,
            'speed' : self.obd2.get_speed,
            'co2_emissions' : self.obd2.get_co2_emissions,
            'air_temperature' : self.obd2.get_air_temperature,
            'light_sensor' : self.obd2.get_light_sensor,
            'rain_sensor' : self.obd2.get_rain_sensor,
            'fog_light_sensor' : self.obd2.get_fog_light_sensor,
        })

    def send_msg(self, msg):
        """ Send message to the RSU device """
        # TODO fazer verificação da msg que está a ser enviada
        try:
            self.socket.sendall(json.dumps(msg).encode('utf-8'))
        except BrokenPipeError:
            sys.exit('The connection was lost.')

    def recv_msg(self):
        # TODO verificar se é para receber info ou não das RSU
        # TODO usar um header para indicar tamanho da msg
        return self.socket.recv(1024)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="symbolic name for the host", default='')
    parser.add_argument("--port", help="port used for communication", default=8000)
    args = parser.parse_args()

    obu = OBU(args.host, args.port)

    obu.exp_middleware()