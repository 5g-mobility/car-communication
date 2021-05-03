import socket
import json
import argparse
import sys
import datetime
import math

from obd2_sumo_integration import OBD2

class OBU:
    def __init__(self, vehicle_id, host='', port=8000):
        self.host = host
        self.port = port
        self.vehicle_id = vehicle_id

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
            'vehicle_id' : self.vehicle_id,
            'position' : self.obd2.get_position,
            'speed' : self.convert_speed(),
            'co2_emissions' : self.convert_co2_emissions(),
            'air_temperature' : round(self.obd2.get_air_temperature, 2),
            'light_sensor' : self.obd2.get_light_sensor,
            'rain_sensor' : self.obd2.get_rain_sensor,
            'fog_light_sensor' : self.obd2.get_fog_light_sensor,
        })

    def convert_speed(self):
        """ Convert ms/s to km/h """
        return math.ceil((self.obd2.get_speed * 3600) / 1000)

    def convert_co2_emissions(self):
        """ Convert mg/s to g/s """
        return round(self.obd2.get_co2_emissions / 1000, 2)

    def send_msg(self, msg):
        """ Send message to the RSU device """
        # TODO fazer verificação da msg que está a ser enviada

        json_msg = json.dumps(msg).encode('utf-8')

        try:
            self.socket.sendall(len(json_msg).to_bytes(4, byteorder='big'))               # send header with the length of message
            self.socket.sendall(json_msg)
        except BrokenPipeError:
            sys.exit('The connection was lost.')
        except InterruptedError:
            sys.exit('Unable to send all payload. Connection lost.')

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