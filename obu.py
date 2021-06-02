import socket
import json
import argparse
import sys
import datetime
import math
import os
import time
import threading

from obd2_sumo_integration import OBD2
import random

class OBU:
    def __init__(self, vehicle_id, generator, host=os.environ.get('RSU_HOST', '0.0.0.0'), port=8000):
        self.host = host
        self.port = port
        self.vehicle_id = vehicle_id
        self.generator = generator

        # possible defective sensors
        self.light_sensor = False
        self.rain_sensor = False
        self.fog_sensor = False

        # 4% probability of having a defective sensor
        self.defective_sensor()

        # the OBU have direct communication with the obd2 emulator
        # the OBU pulls information from obd2
        self.obd2 = None

        self.connect2RSU()

        ## receive data from RSU
        # TODO fazer flag para que a thread termine caso não hajam comunicações há algum tempo
        self.header = 4
        self.receive_message_from_rsu = threading.Thread(target=self.receive_message, args=(), daemon=True)
        self.receive_message_from_rsu.start()

    def defective_sensor(self):
        sensors = [self.light_sensor, self.rain_sensor, self.fog_sensor]
        if random.random() < 0.04:
            #print('Car with defective sensor(s)')
            
            # random number of broken sensors
            for i in range(random.randrange(1, len(sensors))):

                # choose which one of the sensors is defective
                index = random.randrange(0, len(sensors))
                sensors[index] = True
                sensors.pop(index)

    def connect2RSU(self):
        """ Connect OBU to RSU (via socket)"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def close(self):
        """ Close communication with RSU """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def connect2OBD2(self, position, speed, co2Emissions):
        """ Initialize the OBD2 object """
        self.obd2 = OBD2(self.generator, position, speed, co2Emissions)

    def forward_info_2_RSU(self):
        """ Forward the car data to the RSU """
        self.send_msg({
            'tm' : str(datetime.datetime.now()),
            'vehicle_id' : self.vehicle_id,
            'position' : self.obd2.get_position,
            'speed' : self.convert_speed(),
            'co2_emissions' : self.convert_co2_emissions(),
            'air_temperature' : round(self.obd2.get_air_temperature, 2),
            'light_sensor' : self.obd2.get_light_sensor if not self.light_sensor else not self.obd2.get_light_sensor,
            'rain_sensor' : self.obd2.get_rain_sensor if not self.rain_sensor else not self.obd2.get_rain_sensor,
            'fog_light_sensor' : self.obd2.get_fog_light_sensor if not self.fog_sensor else not self.obd2.get_fog_light_sensor,
        })

    def convert_speed(self):
        """ Convert ms/s to km/h """
        return math.ceil((self.obd2.get_speed * 3600) / 1000)

    def convert_co2_emissions(self):
        """ Convert mg/s to g/s """
        return round(self.obd2.get_co2_emissions / 10000, 5)

    def send_msg(self, msg):
        """ Send message to the RSU device """
        json_msg = json.dumps(msg).encode('utf-8')

        try:
            self.socket.sendall(len(json_msg).to_bytes(4, byteorder='big'))               # send header with the length of message
            self.socket.sendall(json_msg)
        except KeyboardInterrupt:
            self.close()
            sys.exit('Ending obu execution.')
        except Exception as e:
            print(f'Error: {e}')
            self.reconnect_2_rsu()

            # try to send the message again
            self.send_msg(msg)

    
    def reconnect_2_rsu(self):
        # if an error occured, than the obu should try to reconnect to RSU
        # unless it was supposed to fail
        connected = False

        while not connected:
            try: 
                self.connect2RSU()
                connected = True
            except Exception as e:
                print(f'Error: {e}')

                # wait a second
                time.sleep(2)

    """ Thread with the purpose of receiving messages from the RSU """
    def receive_message(self):
        while True:
            # receive 4 bytes indicating the length of the message
            try:
                payload_length = self.socket_receive_message(self.header)
            except socket.error:
                break

            if payload_length:
                try:
                    # receive the expected message
                    payload = self.socket_receive_message(
                        int.from_bytes(payload_length, byteorder='big'))
                except socket.error:
                    break
                if payload:
                    json_payload = json.loads(payload.decode('utf-8'))
                    if json_payload["vehicle_id"] != self.vehicle_id:
                        print(f'Id {self.vehicle_id} received: Car Speeding -- vehicle id = {json_payload["vehicle_id"]}, speed = {json_payload["speed"]}')
            else:
                break

    def socket_receive_message(self, payload_length):
        payload = b''

        while len(payload) != payload_length:
            # have in mind that the connection can be lost
            # the while loop can not run indeterminately
            try:
                payload_recv = self.socket.recv(payload_length - len(payload))

                if not payload_recv:
                    return None

                payload += payload_recv

            except BlockingIOError as io:
                # having this error the connection can still exist
                # just need to wait
                print(f'Socket IOError: {io}')
            except Exception as e:
                print(f'Socket error: {e}')
                return None

        return payload
