import traci
import time
import traci.constants as tc
from obd_emulator import response_generator
import random

from obu import OBU

SUMO_BINARY = "sumo"
SUMO_CMD = [SUMO_BINARY, "-c", "sumo/osm.sumocfg"]

emulator_car_map = {}

# TODO fix to many files error
# link : http://woshub.com/too-many-open-files-error-linux/

def main():
    DEFAULT_PORT = 8000
    current_port = 0
    MAX_PORT = 1
    
    max_cars = 0
    
    while True:
        # just a variable to verify the max cars that the simulation has

        # initialize response generator
        generator = response_generator.ResponseGenerator()

        traci.start(SUMO_CMD, port=9500)

        while traci.simulation.getMinExpectedNumber() > 0:
            
            list_current_step_cars = traci.vehicle.getIDList()

            curent_cars = len(list_current_step_cars)
            if curent_cars > max_cars:
                max_cars = curent_cars
                print(f'Currently, there are {max_cars} car(s) sending information to backend infrastructure.')

            for veh_id in list_current_step_cars:

                position = traci.vehicle.getPosition(veh_id)
                position = traci.simulation.convertGeo(position[0], position[1])
                position = (position[1], position[0])
                speed = traci.vehicle.getSpeed(veh_id)

                if speed > 90:
                    if random.random() > 0.000000001:
                        speed = 75 + random.randint(2, 15)
                    else:
                        speed += random.randint(2, 15)

                co2_emissions = traci.vehicle.getCO2Emission(veh_id)

                # verify if its the first time that the car pops on the net
                if not veh_id in emulator_car_map:
                    """ if the car appears on the network for the first time
                        add it to the map
                    """

                    emulator_car_map[veh_id] = OBU(veh_id, generator, port=DEFAULT_PORT + current_port)
                    emulator_car_map[veh_id].connect2OBD2(position, speed, co2_emissions)

                    current_port = (current_port + 1) % MAX_PORT

                    #print(f'Currently, there are {max_cars} car(s) sending information to backend infrastructure.')
                    
                else:
                    """ if the car was already initialized
                        just update it
                    """
                    emulator_car_map[veh_id].obd2.update(position, speed, co2_emissions)

                # send information of the vehicle to the RSU
                emulator_car_map[veh_id].forward_info_2_RSU()
                #print(f'Car with id {veh_id} sent his data to RSU') 

            for vehicle in emulator_car_map:
                if vehicle not in list_current_step_cars:
                    emulator_car_map[vehicle].close()   
                    del emulator_car_map[vehicle]

            traci.simulationStep()

            # simulate the delay of 3 second
            # cars should send data each second
            time.sleep(3)

        traci.close()

        print(f'Max of cars sending data to the backend infrastructure was {max_cars}.')

        # close sockets
        for obu in emulator_car_map.values():
            obu.close()

if __name__ == "__main__":
    main()